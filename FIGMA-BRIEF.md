# Figma Build Brief — Tow Factory Towing Services

Paste everything below into the Figma-MCP-connected Claude session.

---

Here are the brand assets and specs. One important correction to the page list first, then everything you asked for.

## Correction to the proposed scope

The proposal listed **"Request a Tow (emergency flow)"** and **"Enterprise/Partners"** pages. Neither exists in this brand's actual content — there is no B2B/enterprise partnership offering and no multi-step request flow. Building those would produce screens with nothing to fill them.

The real structure is a **single-scroll marketing homepage** with anchored sections, not separate page routes. Conversion is a **phone call**, not a form funnel — users are stranded motorists in an emergency, so the primary action everywhere is a `tel:` link.

Please build to the actual structure in §5. If enterprise/B2B is genuinely planned, treat it as net-new and flag it — I'd need to write that content first.

## 1. Brand assets

- **Logo:** `main/logo.png` — graffiti-style wordmark "TOW FACTORY", black ink, transparent background, 587×425 (trimmed content 580×410). It is **black artwork**, so it needs a light/knockout treatment on the dark UI — in the live build it renders white-on-black. Please set up both a dark-surface and light-surface variant.
- **Hero image:** flatbed tow truck carrying a black SUV, on wet asphalt with red city glow and a neon map of the Philippines. Single flat raster, 1116×663.
- **Secondary image:** same truck on a highway at sunset, 1116×717.

## 2. Color — dark-mode-first

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

**Accent — red is the approved default.** Three alternates exist as a live client-facing preview; please build all four as Figma variable modes so the client can toggle.

| Token | Red (default) | Amber | Blue | Green |
|---|---|---|---|---|
| `accent-500` (button fill) | `#a50201` | `#92400e` | `#1d4ed8` | `#15803d` |
| `accent-600` (gradient end) | `#8e0100` | `#78350f` | `#1e40af` | `#14532d` |
| `accent-700` | `#5d0304` | `#5c2a0c` | `#1e3a8a` | `#052e16` |
| `accent-grad-start` | `#b00604` | `#b45309` | `#2563eb` | `#0f7a37` |
| `accent` (icons, large text) | `#c60000` | `#f59e0b` | `#3b82f6` | `#22c55e` |
| `accent-text` (small text) | `#e94040` | `#fbbf24` | `#60a5fa` | `#4ade80` |

**Please preserve the `accent` / `accent-text` split** — it is an accessibility decision, not duplication. `accent-text` meets AA (≥4.5:1 on black) for small text; `accent` is reserved for large text, icons, and decorative fills where the 3:1 graphical-object threshold applies. Collapsing them into one swatch will break contrast compliance.

**Status colors:** `green #00ff73` (dispatch-available dot), `cyan #2fe5ec` (map/tech accents).

Primary buttons use a vertical gradient: `accent-grad-start → accent-600`, with shadow `0 10px 24px -8px rgba(accent-500, 0.55)`.

## 3. Typography

Both from Google Fonts.

- **Display — Anton**, weight 400 only. **Always uppercase.** Used for h1/h2/h3 and the brand-chip marquee. Fallbacks: Arial Narrow, Roboto Condensed, Impact.
- **UI — Inter**, weights 400/500/600/700/800. All body, nav, buttons, labels. Fallbacks: system-ui, Segoe UI.

| Style | Font | Size | Line height | Letter-spacing | Notes |
|---|---|---|---|---|---|
| H1 (hero) | Anton 400 | `clamp(2.75rem, 5.4vw, 5.625rem)` → 44–90px | 1.06 | 0.002em | UPPERCASE |
| H2 (section) | Anton 400 | `clamp(1.9rem, 3vw, 2.75rem)` → 30.4–44px | 1.08 | 0.002em | UPPERCASE |
| H3 (card) | Inter 700 | 18px | — | — | Sentence case |
| Body | Inter 400 | 16px | 1.5 | — | |
| Card body | Inter 400 | 14.5px | 1.65 | — | |
| Button | Inter 700 | 15px | — | 0.01em | Padding 16×26 |
| Eyebrow/label | Inter 700 | 13px | — | 0.08em | UPPERCASE, `accent-text` |
| Brand chip | Anton 400 | 26px | — | 0.03em | UPPERCASE |

The hero H1 is fluid — please build the 44px and 90px ends as separate text styles so the dev has both bounds.

## 4. Layout, spacing, breakpoints

- **Container:** max 1520px, gutter `min(4vw, 75px)`
- **Header height:** 132px desktop / 92px mobile (sticky)
- **Section padding:** 88px block desktop, 64px below 800px
- **Radii:** sm 6px, md 8px (buttons), lg 14px (cards), pill 999px

**Breakpoints in use:** 480, 560, 600, 640, 800, 900, 1023, 1279/1280. The main desktop↔mobile switch is **1280px**.

Please build frames at **390 (mobile), 768 (tablet), 1440 (desktop)**, plus **1672** — that last one is the width the approved hero mockup was designed against, so it's the fidelity reference.

## 5. Actual page structure

**Home** — one scrolling page, these sections in order:
1. Top utility strip — 24/7 label, coverage label, two phone numbers
2. Sticky header — logo, nav (Home, Services ▾, Service Areas, About, Reviews, FAQ, Contact), red "Call Dispatch" button
3. Hero — H1 "Affordable. / Reliable. / Ready 24/7.", paragraph, primary call CTA + two outline CTAs, two floating status cards (Dispatch Status, Coverage), truck artwork
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

**Also needed:** mobile drawer nav, services dropdown (desktop), legal modal shell *(Privacy / Terms content pending)*, back-to-top button, mobile sticky action bar (Call / Location / Get Quote).

## 6. Components to build with variants

- **Button** — primary (gradient), outline, small, block, icon+label; states: default/hover/active/focus-visible/disabled
- **Nav link** — default / hover / active (active has a 2px accent underline)
- **Service card** — icon, heading, body, arrow link
- **Pillar card** — accent-bordered icon tile
- **Promise card**, **Review card** (5-star row, avatar initials, name, date), **Mission card**
- **Floating status card** — icon, uppercase eyebrow, value, sub-line *(no border — see §7)*
- **Signal item** — icon + two-line label, with divider
- **Form field** — label, input/textarea, error state, success state
- **Section head** — eyebrow (with accent underline) + H2 + optional intro
- **Brand chip**, **Accordion row**, **CTA band**, **Footer column**

## 7. Details that are easy to get wrong

These were all decided deliberately in the live build:

1. **The floating hero cards have no border.** Sampling the approved mockup showed their fill is identical to the page background with only a ~13/255 edge — effectively invisible. An added border makes them read as boxes sitting on top of the art instead of embedded in it. Use a soft `rgba(0,0,0,0.45)` fill, no stroke.
2. **"All Over the Philippines" must never wrap.** It sits on one line at every width; the coverage card has a 270px min-width to guarantee it.
3. **Phone numbers are `(0969) 348 6078` and `(0945) 108 0849`.** The original mockup image rendered different digits — that was an artifact. These are correct.
4. **The logo is black artwork** and must be knocked out to white on dark surfaces.
5. **Nav "Services" has a dropdown** listing all 6 services, each deep-linking to its card.

## 8. Deliverable

- Figma variables for color (4 accent modes), type, spacing, radii
- Frames at 390 / 768 / 1440 / 1672
- Components with variants and Auto Layout throughout
- Dev Mode–ready: named tokens matching the table names above, so the CSS custom properties map 1:1

A fully built, pixel-accurate HTML implementation already exists and can be supplied as reference for any spacing question. Where Figma and that build disagree, **the build is the source of truth** — it was matched pixel-for-pixel against the client-approved hero mockup.
