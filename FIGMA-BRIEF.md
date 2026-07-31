# Figma Build Brief — Tow Factory Towing Services

Paste everything below into the Figma-MCP-connected Claude session.

---

Here are the brand assets and specs. Two things up front — what this needs to *feel* like, and a correction to the proposed page list.

## 0. The headline requirement: this has to move

The client is not buying static screens. They want to **experience the site** in the prototype — the reference they keep pointing at is [Draftly](https://www.draftly.space/): cinematic, scroll-driven, depth, motion, things that animate as you move through the page.

So the deliverable is a **working prototype the client can click into and feel**, not a flat mockup with redlines. Please treat motion as a first-class part of the design, not a note for the developer.

**One constraint to design around, honestly:** Figma has **no scroll-position trigger**. You cannot bind an animation's progress to scroll offset the way Draftly does — that request has been open for 5+ years and still isn't implemented. So we can't literally scrub a frame sequence on scroll inside Figma.

What Figma *can* do, and what I want used:

| Technique | Use it for |
|---|---|
| **Fixed / sticky scroll behavior** on layers | The depth effect — pin the hero art and let content scroll over it, pin the header |
| **After Delay + Smart Animate loops** | Ambient motion that plays by itself: the beacon pulse, the brand marquee, the truck bob |
| **Smart Animate between full-viewport frames** | Cinematic section-to-section transitions (the closest thing to Draftly's feel) |
| **Interactive components** (While hovering / While pressing) | Every button, nav link, and card hover |
| **Video fill** *(paid plans — confirm against ours)* | The single biggest win for the hero, see below |
| **Overflow scrolling** frames | The real, continuously scrollable page |

**Please deliver two prototypes, not one:**

- **A — "Experience" flow.** Full-viewport section frames wired with Smart Animate and After-Delay chains, so it plays like a cinematic walkthrough. This is what gets shown to the client. Prioritise feel over fidelity to the DOM.
- **B — "Structural" page.** One long overflow-scroll frame with sticky header, fixed hero art, real hover states, and all components in place. This is what the developer reads. Prioritise accuracy.

**On the hero specifically:** we can generate video (Higgsfield). If our Figma plan supports **video fill**, tell me the format and size limits you want and I'll supply a looping clip of the truck — that gets us genuinely close to Draftly inside Figma. If video fill isn't available, fall back to an After-Delay Smart Animate loop between 3–4 near-identical hero frames.

## 0b. Motion spec — match these values

A fully animated HTML build already exists. Reproducing its timings keeps the prototype and the real site consistent. **Primary easing throughout is expo-out: `cubic-bezier(0.16, 1, 0.3, 1)`.**

| Element | Motion | Duration | Easing | Notes |
|---|---|---|---|---|
| Section reveals | Fade + rise 24px | 600ms | expo-out | **55ms stagger** between grid siblings, capped at 6 steps |
| Card reveals | Fade + rise + scale 0.985→1 | 600ms | expo-out | Same stagger |
| Hero entrance | Fade + rise 16px | 700ms | expo-out | Staged: H1 0ms → paragraph 90ms → CTAs 170ms → secondary CTAs 230ms |
| Hero art entrance | Fade only, no move | 900ms | expo-out | 120ms delay |
| Truck "suspension bob" | Vertical ±2.8px, continuous | ~2.3s loop | sine, seamless | Two detuned waves so it never reads as a loop |
| Amber beacon pulse | Opacity 0.15 → 1 → 0.28 → 0.92 → 0.15 | 2.4s loop | ease-in-out | Double-flash rhythm, like a real light bar |
| Road light streaks | Slide R→L, fade in/out | 2.9s / 2.2s / 3.6s | linear | Three streaks, staggered 0 / 0.7s / 1.5s |
| Brand marquee | Continuous horizontal scroll | 22s loop | linear | Pauses on hover |
| Eyebrow underline | Scale X 0→1 from left | 800ms | expo-out | 140ms delay after the heading appears |
| Hero art parallax | Moves at 0.12× scroll speed | — | — | Cards move at 0.30×, section image at 0.16× |
| Nav scroll | Eased scroll to anchor | 400–900ms | ease-in-out cubic | Scales with distance |

**Beacon position matters:** the amber light bar sits at **44.4% across, 31.1% down** the hero artwork. The glow must be an **ellipse** (the bar is a 170×17 strip) — a circle wide enough to cover it bleeds up onto the Coverage card and reads as a bug.

**Hover states to build:** buttons lift/brighten, nav links underline, service cards raise slightly, marquee pauses, theme swatches scale up.

## 1. Correction to the proposed scope

The proposal listed **"Request a Tow (emergency flow)"** and **"Enterprise/Partners"** pages. Neither exists in this brand's actual content — there is no B2B/enterprise partnership offering and no multi-step request flow. Building those would produce screens with nothing to fill them.

The real structure is a **single-scroll marketing homepage** with anchored sections, not separate page routes. Conversion is a **phone call**, not a form funnel — users are stranded motorists in an emergency, so the primary action everywhere is a `tel:` link.

Please build to the actual structure in §6. If enterprise/B2B is genuinely planned, treat it as net-new and flag it — I'd need to write that content first.

## 2. Brand assets

- **Logo:** `main/logo.png` — graffiti-style wordmark "TOW FACTORY", black ink, transparent background, 587×425 (trimmed content 580×410). It is **black artwork**, so it needs a knockout treatment on the dark UI — in the live build it renders white-on-black. Set up both a dark-surface and light-surface variant.
- **Hero image:** flatbed tow truck carrying a black SUV, on wet asphalt with red city glow and a neon map of the Philippines. Single flat raster, 1116×663.
- **Secondary image:** same truck on a highway at sunset, 1116×717.

**Note on the hero art:** it is one flat image — truck, glow, city, and map are all baked together. So true multi-layer parallax isn't possible from this asset. If you want separated planes (truck / glow / map moving at different speeds, which would look considerably better), say so and I'll have new layered art generated.

## 3. Color — dark-mode-first

The entire site is built on **pure black**. Do not set up a light theme; there isn't one.

**Surfaces & text**
| Token | Hex | Use |
|---|---|---|
| `bg` | `#000000` | Page background |
| `panel` | `#050505` | Cards, panels |
| `panel-2` | `#0b0b0c` | Raised/nested surfaces |
| `border` | `rgba(255,255,255,0.10)` | Default hairlines |
| `border-strong` | `rgba(255,255,255,0.18)` | Emphasised edges |
| `text-1` | `#ededed` | Headings, primary |
| `text-2` | `#c4c5c7` | Body |
| `text-3` | `#a9a9ac` | Secondary/meta |
| `text-4` | `#7c7c80` | Disabled/faint |

**Accent — red is the approved default.** Three alternates exist as a live client-facing preview; please build all four as Figma variable modes so the client can toggle them in the prototype.

| Token | Red (default) | Amber | Blue | Green |
|---|---|---|---|---|
| `accent-500` (button fill) | `#a50201` | `#92400e` | `#1d4ed8` | `#15803d` |
| `accent-600` (gradient end) | `#8e0100` | `#78350f` | `#1e40af` | `#14532d` |
| `accent-700` | `#5d0304` | `#5c2a0c` | `#1e3a8a` | `#052e16` |
| `accent-grad-start` | `#b00604` | `#b45309` | `#2563eb` | `#0f7a37` |
| `accent` (icons, large text) | `#c60000` | `#f59e0b` | `#3b82f6` | `#22c55e` |
| `accent-text` (small text) | `#e94040` | `#fbbf24` | `#60a5fa` | `#4ade80` |

**Please preserve the `accent` / `accent-text` split** — it is an accessibility decision, not duplication. `accent-text` meets AA (≥4.5:1 on black) for small text; `accent` is reserved for large text, icons, and decorative fills where the 3:1 graphical-object threshold applies. Collapsing them into one swatch breaks contrast compliance.

**Status colors:** `green #00ff73` (dispatch-available dot, gently pulsing), `cyan #2fe5ec` (map/tech accents).

Primary buttons use a vertical gradient `accent-grad-start → accent-600`, with shadow `0 10px 24px -8px rgba(accent-500, 0.55)`.

Beacon glow gradient: `rgba(255,190,96,0.92)` core → `rgba(255,146,26,0.40)` at 45% → transparent.

## 4. Typography

Both from Google Fonts.

- **Display — Anton**, weight 400 only. **Always uppercase.** Used for h1/h2/h3 and the brand-chip marquee. Fallbacks: Arial Narrow, Roboto Condensed, Impact.
- **UI — Inter**, weights 400/500/600/700/800. All body, nav, buttons, labels. Fallbacks: system-ui, Segoe UI.

| Style | Font | Size | Line height | Letter-spacing | Notes |
|---|---|---|---|---|---|
| H1 (hero) | Anton 400 | 44–90px fluid | 1.06 | 0.002em | UPPERCASE |
| H2 (section) | Anton 400 | 30.4–44px fluid | 1.08 | 0.002em | UPPERCASE |
| H3 (card) | Inter 700 | 18px | — | — | Sentence case |
| Body | Inter 400 | 16px | 1.5 | — | |
| Card body | Inter 400 | 14.5px | 1.65 | — | |
| Button | Inter 700 | 15px | — | 0.01em | Padding 16×26 |
| Eyebrow/label | Inter 700 | 13px | — | 0.08em | UPPERCASE, `accent-text` |
| Brand chip | Anton 400 | 26px | — | 0.03em | UPPERCASE |

Headings are fluid — build the 44px and 90px ends as separate text styles so the dev has both bounds.

## 5. Layout, spacing, breakpoints

- **Container:** max 1520px, gutter `min(4vw, 75px)`
- **Header height:** 132px desktop / 92px mobile (sticky)
- **Section padding:** 88px block desktop, 64px below 800px
- **Radii:** sm 6px, md 8px (buttons), lg 14px (cards), pill 999px

**Breakpoints in use:** 480, 560, 600, 640, 800, 900, 1023, 1279/1280. The main desktop↔mobile switch is **1280px**.

Build frames at **390 (mobile), 768 (tablet), 1440 (desktop)**, plus **1672** — that last one is the width the approved hero mockup was designed against, so it's the fidelity reference. **The animated prototype only needs 1440 and 390**; the middle sizes can stay static.

## 6. Actual page structure

**Home** — one scrolling page, these sections in order:
1. Top utility strip — 24/7 label, coverage label, two phone numbers
2. Sticky header — logo, nav (Home, Services ▾, Service Areas, About, Reviews, FAQ, Contact), red "Call Dispatch" button
3. Hero — H1 "Affordable. / Reliable. / Ready 24/7.", paragraph, primary call CTA + two outline CTAs, two floating status cards (Dispatch Status, Coverage), truck artwork **(this is the money shot — most of the motion budget goes here)**
4. Signal strip — 6 icon+label trust items
5. Positioning — image + copy, "Your Trusted Partner in Vehicle Recovery"
6. Pillars — 4 icon cards
7. Promise cards — 3 cards
8. Commitment — full-width statement panel
9. Services — 6 service cards, each anchor-linked from the nav dropdown
10. Service Areas — branch panel + coverage panel (addresses, phones, service area)
11. About — vision/mission stack
12. Brand marquee — infinite scroll: Honda, Hyundai, BMW, Rapide, Toyota
13. Reviews — 6 testimonial cards (name, date, star rating, quote)
14. FAQ — accordion *(content pending — build the component, use placeholders)*
15. Contact — form (First/Last Name, Email, Phone, Message, Submit) + contact rail
16. Final CTA band — "Need Help? Call" + numbers
17. Footer — logo, quick links, contact block, legal links

**Also needed:** mobile drawer nav (animated open/close), services dropdown (desktop, animated), legal modal shell *(Privacy / Terms content pending)*, back-to-top button, mobile sticky action bar (Call / Location / Get Quote).

## 7. Components to build with variants

- **Button** — primary (gradient), outline, small, block, icon+label; states: default / **hover** / active / focus-visible / disabled
- **Nav link** — default / hover / active (active has a 2px accent underline that animates in)
- **Service card** — icon, heading, body, arrow link; hover raises the card
- **Pillar card** — accent-bordered icon tile
- **Promise card**, **Review card** (5-star row, avatar initials, name, date), **Mission card**
- **Floating status card** — icon, uppercase eyebrow, value, sub-line *(no border — see §8)*
- **Signal item** — icon + two-line label, with divider
- **Form field** — label, input/textarea, error state, success state
- **Section head** — eyebrow (with animated accent underline) + H2 + optional intro
- **Brand chip**, **Accordion row** (animated expand), **CTA band**, **Footer column**

Use interactive components so hover states work inside the prototype without extra wiring.

## 8. Details that are easy to get wrong

All decided deliberately in the live build, several by pixel-diffing the client-approved mockup:

1. **The floating hero cards have no border.** Sampling the approved mockup showed their fill is identical to the page background with only a ~13/255 edge — effectively invisible. A border makes them read as boxes sitting on top of the art instead of embedded in it. Use a soft `rgba(0,0,0,0.45)` fill, no stroke.
2. **"All Over the Philippines" must never wrap.** One line at every width; the coverage card has a 270px min-width to guarantee it.
3. **Phone numbers are `(0969) 348 6078` and `(0945) 108 0849`.** The original mockup image rendered different digits — that was an artifact. These are correct.
4. **The logo is black artwork** and must be knocked out to white on dark surfaces.
5. **Nav "Services" has a dropdown** listing all 6 services, each deep-linking to its card.
6. **Don't animate the two hero status cards on entrance.** In the live build their box sits at a fractional pixel and animating them shifted their text ~2px off the approved mockup. They should simply be present. Ambient parallax on them is fine.

## 9. Deliverable checklist

- [ ] Figma variables: color (4 accent modes), type, spacing, radii — named to match the tables above so they map 1:1 to CSS custom properties
- [ ] **Prototype A — "Experience"**: cinematic, animated, client-facing. Auto-playing ambient loops, Smart Animate section transitions, working hover states
- [ ] **Prototype B — "Structural"**: long scrollable page, sticky header, fixed hero art, all components, Dev Mode ready
- [ ] Static frames at 390 / 768 / 1440 / 1672
- [ ] Components with variants + Auto Layout throughout
- [ ] A short note listing anything in §0b you *couldn't* reproduce in Figma, so I know what only exists in code

A fully built, animated HTML implementation already exists and can be supplied as reference for any timing or spacing question. Where Figma and that build disagree, **the build is the source of truth** — it was matched pixel-for-pixel against the client-approved hero mockup.
