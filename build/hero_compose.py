"""
Rebuilds build/hero_art_crop.png (and the WebP + base64 the renderer consumes)
from the client's transparent truck cutout plus the background of the approved
mockup.

Why this exists: the approved MAIN-LANDING-PAGE.png bakes the truck, the red
atmosphere, the city silhouette and the neon Philippines map into one flat
raster. Swapping the vehicle therefore means lifting the old one out of that
plate and compositing the new one back in, rather than just replacing a file.

Run:  python3 build/hero_compose.py
Then: python3 build/render.py
"""
import base64
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)

SOURCE_PLATE = os.path.join(ROOT, "main", "MAIN-LANDING-PAGE.png")
TRUCK_CUTOUT = os.path.join(ROOT, "main", "transparent-new-truck.png")
# Same framing as the cutout, but not upscaled -- used to repair the badge.
ORIGINAL_PHOTO = os.path.join(ROOT, "main", "new-truck-mmda.jpeg")
BADGE_BOX = (1085, 588, 1228, 648)
OUT_PNG = os.path.join(BUILD, "hero_art_crop.png")
OUT_WEBP = os.path.join(BUILD, "hero_art.webp")

# Region of the mockup that becomes the hero plate, and the two floating status
# cards inside it that are re-rendered as live HTML and so must be erased.
CROP_BOX = (556, 152, 1672, 815)
CARD_RECTS = [(170, 34, 419, 178), (437, 34, 714, 178)]

# Footprint of the *old* vehicle inside the crop, measured from its bodywork.
OLD_VEHICLE_BOX = (90, 185, 1080, 640)

# Placement of the new truck.
TRUCK_WIDTH = 815
TRUCK_BOTTOM_Y = 646   # wheels on the road line; also drops the beacon clear
TRUCK_LEFT_X = 26      # keeps the cab off the neon map on the right

# The cutout carries a soft grey drop-shadow in its low-alpha fringe. On a black
# backdrop that reads as haze, so anything under this alpha is discarded and the
# remainder is rescaled to keep the real silhouette anti-aliased.
ALPHA_CUT = 140.0


def dissolve(img, mask, sigma=30, gain=1.45):
    """Fade `mask` out to black with a wide feather.

    Reconstructing what stood behind the old vehicle is guesswork -- it covered
    roughly a third of the plate and the scene is stylised, so diffusion fills
    either smear the neon map across the gap or leave blotches. The complaint
    was never that the area went dark, it was that the darkness kept the
    *shape* of a truck. A heavily feathered fade removes the silhouette while
    reading as ordinary night vignetting, which this scene already has.
    """
    soft = ndi.gaussian_filter(mask.astype(float), sigma)
    soft = np.clip(soft * gain, 0, 1)[:, :, None]
    return img.astype(float) * (1.0 - soft)


def background_plate():
    """The approved mockup with the status cards and the old vehicle removed."""
    plate = Image.open(SOURCE_PLATE).convert("RGB").crop(CROP_BOX)
    a = np.array(plate).astype(int)
    h, w, _ = a.shape

    # Blank the baked status cards -- they exist as live HTML in the page.
    for x1, y1, x2, y2 in CARD_RECTS:
        a[max(0, y1 - 2):y2 + 2, max(0, x1 - 2):x2 + 2] = 0

    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lum = a.mean(axis=2)

    # Inside the old vehicle's footprint keep only the scene: the neon map, and
    # red atmosphere. The luminance cap is what separates dim scene glow from
    # the truck's lamps and lit bodywork, which are also red-dominant. The
    # strong red-dominance test keeps merely-warm anti-aliased edges out.
    is_map = (b > r + 14) | (g > r + 14)
    is_glow = (r > g + 38) & (r > b + 38) & (lum < 95)

    foot = np.zeros((h, w), bool)
    x1, y1, x2, y2 = OLD_VEHICLE_BOX
    foot[y1:y2, x1:x2] = True

    blank = foot & ~(is_map | is_glow)

    # Hard-zero first so no bodywork survives, then feather the same region so
    # the removal has no readable outline.
    a[blank] = 0
    a = dissolve(a, blank)

    # The map is the one thing that must not be touched: it sits behind the old
    # vehicle's rear, so the feather would otherwise eat into Visayas/Mindanao.
    orig = np.array(plate).astype(float)
    a[is_map] = orig[is_map]

    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def repair_badge(arr):
    """Restore the grille badge from the untouched photograph.

    The supplied cutout has been AI-upscaled, and the upscaler misread the
    ISUZU wordmark as "I5UZU". Both files share the same framing, so the badge
    can be lifted straight across; it only needs exposure matching, because the
    upscale also lifted the whole image by roughly 7%.
    """
    if not os.path.exists(ORIGINAL_PHOTO):
        print("badge      : original photo missing, left as-is")
        return arr

    orig = np.array(Image.open(ORIGINAL_PHOTO).convert("RGB")).astype(float)
    if orig.shape[:2] != arr.shape[:2]:
        print("badge      : source sizes differ, left as-is")
        return arr

    x1, y1, x2, y2 = BADGE_BOX
    pad = 14

    # Match exposure using a ring just outside the badge, so the patch sits at
    # the cutout's brightness rather than the photograph's.
    ring_o = orig[y1 - pad:y1 - 2, x1:x2].reshape(-1, 3).mean(axis=0)
    ring_c = arr[y1 - pad:y1 - 2, x1:x2, :3].reshape(-1, 3).mean(axis=0)
    gain = np.clip(ring_c / np.maximum(ring_o, 1.0), 0.8, 1.4)

    patch = np.clip(orig[y1:y2, x1:x2] * gain, 0, 255)

    # Feather the edges so the repair has no visible border.
    h, w = patch.shape[:2]
    fy = np.minimum(np.arange(h), np.arange(h)[::-1]) / max(pad, 1)
    fx = np.minimum(np.arange(w), np.arange(w)[::-1]) / max(pad, 1)
    mask = np.clip(np.minimum.outer(fy, fx), 0, 1)[..., None]

    arr[y1:y2, x1:x2, :3] = arr[y1:y2, x1:x2, :3] * (1 - mask) + patch * mask
    print("badge      : repaired from original photo (gain {})".format(gain.round(3)))
    return arr


def graded_truck():
    """The cutout, de-hazed, scaled, and lit to match a night scene."""
    arr = np.array(Image.open(TRUCK_CUTOUT).convert("RGBA")).astype(float)
    arr = repair_badge(arr)
    arr[:, :, 3] = np.clip((arr[:, :, 3] - ALPHA_CUT) / (255.0 - ALPHA_CUT), 0, 1) * 255.0
    t = Image.fromarray(arr.astype(np.uint8))

    ys, xs = np.where(np.array(t)[:, :, 3] > 8)
    t = t.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    t = t.resize((TRUCK_WIDTH, round(t.height * TRUCK_WIDTH / t.width)), Image.LANCZOS)
    tw, th = t.size

    rgba = np.array(t).astype(float)
    rgb, al = rgba[:, :, :3], rgba[:, :, 3:4] / 255.0

    rgb *= 0.62                      # the source is a daylight shot
    rgb[:, :, 0] *= 1.10             # warm what remains toward the scene
    rgb[:, :, 2] *= 0.92
    mean = rgb.mean(axis=2, keepdims=True)
    rgb = mean + (rgb - mean) * 1.12

    # Red rim off the road glow at lower-left, warm spill from the city at right.
    yy, xx = np.mgrid[0:th, 0:tw]
    left = np.clip(1.0 - xx / (tw * 0.55), 0, 1) * np.clip(yy / (th * 0.9), 0, 1)
    right = np.clip((xx - tw * 0.6) / (tw * 0.4), 0, 1)
    # Gate every added highlight by alpha. Without this the glow paints onto
    # fringe pixels and haloes the whole silhouette.
    gate = al[:, :, 0]
    rgb[:, :, 0] += (left * 70 + right * 38) * gate
    rgb[:, :, 1] += (left * 10 + right * 14) * gate
    rgb[:, :, 2] += (right * 6) * gate

    return Image.fromarray(
        np.concatenate([np.clip(rgb, 0, 255), al * 255], axis=2).astype(np.uint8)
    )


def tint_side_window(canvas, box=(398, 200, 512, 322), factor=0.42):
    """Darken the cab's door glass.

    The glass is found by colour inside `box` rather than by a hand-drawn
    polygon, so the slanted window frame is followed exactly and the paintwork
    around it is left alone. The mask is feathered so there is no hard edge.
    """
    a = np.array(canvas).astype(float)
    x1, y1, x2, y2 = box
    reg = a[y1:y2, x1:x2]
    lum = reg.mean(axis=2)
    sat = reg.max(axis=2) - reg.min(axis=2)
    # The lower bound matters: the door panel just under the window sits in
    # shadow and otherwise matches the glass test, which tinted the bodywork.
    glass = (lum > 26) & (lum < 135) & (sat < 60)

    m = ndi.gaussian_filter(glass.astype(float), 2.0)
    m = np.clip(m * 1.25, 0, 1)[:, :, None]
    a[y1:y2, x1:x2] = reg * (1 - m) + reg * factor * m
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def add_driver(canvas, head=(612, 276), scale=0.8, strength=0.34):
    """Suggest a driver behind the windscreen.

    Deliberately a soft silhouette rather than a figure: at this size any
    detail reads as a smudge, whereas a head-and-shoulders shape darker than
    the glass is legible as a person without drawing attention. Drawn only
    where the windscreen already is, so it cannot spill onto the pillar or the
    bonnet.
    """
    a = np.array(canvas).astype(float)
    cx, cy = head
    pad = int(70 * scale)
    x1, y1 = max(0, cx - pad), max(0, cy - pad)
    x2, y2 = min(a.shape[1], cx + pad), min(a.shape[0], cy + pad)

    # Restrict to windscreen glass: mid-dark, low saturation.
    reg = a[y1:y2, x1:x2]
    lum = reg.mean(axis=2)
    sat = reg.max(axis=2) - reg.min(axis=2)
    glass = (lum > 15) & (lum < 150) & (sat < 70)

    yy, xx = np.mgrid[y1:y2, x1:x2]
    hr_x, hr_y = 13.0 * scale, 15.0 * scale
    head_m = (((xx - cx) / hr_x) ** 2 + ((yy - cy) / hr_y) ** 2) <= 1.0

    sy = cy + int(26 * scale)
    sh_x, sh_y = 27.0 * scale, 20.0 * scale
    shoulder_m = ((((xx - cx) / sh_x) ** 2 + ((yy - sy) / sh_y) ** 2) <= 1.0) & (yy >= cy + int(8 * scale))

    figure = (head_m | shoulder_m) & glass
    m = ndi.gaussian_filter(figure.astype(float), 3.0)
    m = np.clip(m * 1.15, 0, 1)[:, :, None] * strength

    a[y1:y2, x1:x2] = reg * (1 - m)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def main():
    bg = background_plate()
    w, h = bg.size
    truck = graded_truck()
    tw, th = truck.size
    px, py = TRUCK_LEFT_X, TRUCK_BOTTOM_Y - th

    canvas = bg.copy()
    shadow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(shadow).ellipse(
        [px + 95, TRUCK_BOTTOM_Y - 24, px + tw - 75, TRUCK_BOTTOM_Y + 16], fill=225
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    canvas = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), canvas, shadow)
    canvas.paste(truck, (px, py), truck)

    # Cab treatments run on the composited plate, so their coordinates are in
    # final plate space and stay valid if the truck is repositioned above.
    canvas = tint_side_window(canvas)
    canvas = add_driver(canvas)

    canvas.save(OUT_PNG)
    canvas.convert("RGB").save(OUT_WEBP, quality=90, method=6)
    with open(OUT_WEBP, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    with open(OUT_WEBP + ".b64.txt", "w", encoding="ascii") as fh:
        fh.write(b64)

    # Report the beacon's position so the CSS glow can be aimed at it.
    c = np.array(canvas).astype(int)
    r, g, b = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    amber = (r > 170) & (g > 90) & (g < 200) & (b < 80) & ((r - b) > 110)
    sub = np.zeros_like(amber)
    sub[py:py + int(th * 0.25), px:px + tw] = True
    ys, xs = np.where(amber & sub)

    print("plate       : {}x{}".format(w, h))
    print("truck       : {}x{} at ({},{})".format(tw, th, px, py))
    print("webp        : {:,} bytes".format(os.path.getsize(OUT_WEBP)))
    if len(xs):
        cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        print("beacon      : centre {:.2f}% , {:.2f}%".format(100 * cx / w, 100 * cy / h))
        print("              -> .fx-lightbar left/top in template.html")
    else:
        print("beacon      : NOT FOUND -- check the amber threshold")


if __name__ == "__main__":
    main()
