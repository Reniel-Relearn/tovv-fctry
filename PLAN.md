# Tow Factory — Client Presentation Frontend: Phase-by-Phase Build Plan

**Deliverable:** one self-contained HTML file, `TowFactory-Client-Presentation.html`, that opens by
double-click with no server and no internet. Hero renders pixel-identical to
`main/MAIN-LANDING-PAGE.png`; the client scrolls from there through every fact contained in the five
source-of-truth PDFs; all navigation and buttons genuinely work.

---

## 0. What the audit established

### Asset reality (this drives the whole hero strategy)

`main/MAIN-LANDING-PAGE.png` is **1672 × 941** and its right-hand artwork — tow truck, red floor
glow, wet-asphalt reflection, city silhouette, and the neon-constellation Philippines map — is a
**single baked raster composite**. It cannot be rebuilt from the supplied parts:
`main/main-truck-Tow-Factory.jpeg` is a *different photograph* (sunset sky, gold "TOVV FCTRY"
lettering, highway backdrop), not the neon-night truck in the mockup.

The decisive fact: the mockup's background is **pure black** (sampled `#000000`, with panels at
`#010101`). Any rectangle cropped from that artwork and composited onto a black HTML surface with
`mix-blend-mode: screen` is mathematically identical to the original (screen against black = source)
and has **invisible edges**. That is what makes an exact hero achievable while keeping every button
live HTML.

### Measured hero geometry @ 1672px

| Element | Box (x1,y1 → x2,y2) | Notes |
|---|---|---|
| Utility top strip | 0,0 → 1672,55 | 3 zones: label / centered / 2 hotlines right |
| Nav row | 0,70 → 1672,165 | logo x 130–390; links x 540–1245; button right |
| "Call Dispatch" button | 1355,84 → 1590,144 | 235 × 60, radius ~6 |
| Headline block | 75,265 → 540,545 | 3 lines, line-height ~103px, size ~90px |
| Paragraph | 75,560 → 470,635 | |
| Primary CTA button | 75,649 → 384,705 | 309 × 56, radius ~8 |
| Secondary button row | 75,728 → 470,772 | 2 outline buttons |
| Dispatch-status card | 726,186 → 975,330 | 249 × 144 |
| Coverage card | 993,186 → 1270,330 | |
| Signal strip | 70,820 → 1600,935 | 6 columns, 1px dividers |
| **Clean art crop** | **556,152 → 1672,815** | contains **no** baked text |

The two floating cards sit inside that crop but over pure-black pixels only — so the crop is
generated with those two rectangles flood-filled `#000000`, and the cards are rebuilt as live HTML
at the same coordinates. Nothing of the artwork is lost.

### Measured palette

| Token | Value | Source |
|---|---|---|
| `--bg` | `#000000` | page + hero base |
| `--panel` | `#050505` on `#0D0D0E` hairline | floating cards, signal strip |
| `--red` | `#A50201` (fill), gradient `#B00604 → #8E0100` | both red buttons |
| `--red-accent` | `#C60000` | nav active underline, "READY 24/7." |
| `--text` | `#EDEDED` | headline |
| `--text-2` | `#C4C5C7` | body copy |
| `--text-3` | `#A4A4A6` | card eyebrows, uppercase micro-labels |
| `--green` | `#00FF73` | dispatch-status ring |
| `--cyan` / `--blue` | `#00E5FF` / `#1550FF` | neon map (inside raster, tokenised for accents) |

Headline face: heavy condensed all-caps grotesk, flat terminals, tight tracking (Oswald 700 /
Archivo Condensed 800 class). UI face: neutral grotesk. Live site uses a rounded geometric grotesk
(Poppins/Gilroy class) for image-baked text.

### Source-of-truth content inventory

Text was extracted from all 5 PDFs with PyMuPDF. **Critical catch:** `home.pdf` renders part of its
hero copy as *images*, invisible to text extraction. Those strings were recovered from the embedded
bitmaps and are in scope:

- "Professional Vehicle Recovery Services Ready Now!"
- "Round-the-Clock Assistance Whenever You Need It!"
- "Trusted Vehicle Transport Solutions."
- "Quick Response, Fair Pricing, & Dependable Service!"
- "Top-rated by over 100 satisfied clients"

All five PDFs were swept for further image-baked text; only `home.pdf` had any. Everything else is
real text and is captured.

### Note on the two files in `sample/`

`Tow-Factory-Homepage-Preview.html` and `towfactory_redesign_v2_techy.html` are **prior drafts, not
the target**. Neither matches the approved mockup and both contain invented copy
("Sample layout", "Verified customer", "Four promises that matter"). `towfactory_redesign_v2_techy.html`
also pulls fonts from `fonts.googleapis.com`, which breaks offline and under Artifact CSP. They are
useful only as a pattern reference for single-file base64 packaging. **Copy no text from them.**

---

## 1. Decisions required from the client

These are contradictions between the approved mockup and the source of truth. Each has a
recommended default so the build is not blocked.

| # | Conflict | Recommendation |
|---|---|---|
| 1 | **Phone numbers.** Mockup renders `0969 346 6078` / `0945 106 0548`. Every PDF says `(0969) 348 6078` / `(0945) 108 0849`. | **Use the PDF numbers everywhere.** The mockup digits are almost certainly a render artifact; shipping a wrong hotline is the worst possible defect. Confirm before delivery. |
| 2 | **Coverage claim.** Mockup: "All Over the Philippines" / "Nationwide Coverage." PDFs: "MANILA, NLEX, SLEX, LUZON PROVINCES" / "Metro Manila and beyond." | Keep the mockup wording in the hero (it is the approved visual), and state the exact PDF scope in the Service Areas section. Flag the mismatch in the handoff notes. |
| 3 | **Nav label.** Mockup: "Service Areas". PDF footer: "Branch Locator". | Mockup label in the header, PDF label in the footer quick links. Both anchor to `#service-areas`. |
| 4 | **FAQ.** Mockup nav has FAQ; no FAQ content exists in the PDFs. | Build 5–6 Q&As derived *strictly* from stated PDF facts, visibly marked as proposed copy. |
| 5 | **Privacy Policy / Terms.** Linked in every PDF footer; content not supplied. | Links present, opening a modal that says content is pending from the client. |
| 6 | **Vehicle brands** list is truncated in the PDF: `RAPIDE, TOYOTA, HONDA, HY…` | Render the four known entries, marquee built data-driven so the client can extend it. |
| 7 | **Relative review dates** ("3 weeks ago", "6 weeks ago") will go stale. | Reproduce verbatim for fidelity; flag for replacement with absolute dates. |
| 8 | **Copyright reads "© 2026"** in the PDFs. | Keep verbatim. |
| 9 | Live contact form sits on a **bright blue** panel, clashing with the black/red system. | Restyle to the mockup's black/red system — deliberate, documented deviation. |

---

## Phase 0 — Asset preparation and content lock

**Goal:** every byte the final file needs, plus a single authoritative copy deck. No HTML yet.

1. Generate the hero art crop from `main/MAIN-LANDING-PAGE.png`:
   - crop `(556, 152) → (1672, 815)` (1116 × 663);
   - flood-fill the two card rects — `(726,186)-(975,330)` and `(993,186)-(1270,330)`, converted to
     crop-local coordinates — with `#000000`;
   - verify no non-black pixel was destroyed by diffing filled vs. unfilled crops and asserting the
     max per-channel delta inside those rects is ≤ 3;
   - export as WebP (quality ~88) **and** PNG; keep whichever is smaller.
2. Optimise `logo.png` (209 KB → target < 60 KB): trim transparent margin, quantise. It is
   pure black-and-white line art, so palette reduction is lossless in practice.
3. Optimise `main-truck-Tow-Factory.jpeg` at two sizes (1200w content, 600w card) for the
   placeholder slots.
4. Build a 32×32 favicon from the logo mark.
5. Resolve fonts. Preferred: subset two woff2 faces (condensed heavy display + neutral UI) to
   Latin + digits + punctuation and base64-embed them. If they cannot be fetched, fall back to
   `"Arial Narrow", "Roboto Condensed", Impact` for display and the system UI stack, and re-verify
   the headline against the mockup in Phase 2 — this is why fidelity is checked *after* fonts are
   settled, not before.
6. Write `content.json` (build-time input, inlined at the end): every string transcribed verbatim
   from the PDFs, each tagged `source: home.pdf p2` etc., and each non-PDF string tagged
   `origin: mockup` or `origin: proposed`. **This file is the audit instrument for Phase 8.**

**Exit criteria:** all assets base64-ready and under ~1.6 MB combined; `content.json` complete;
every string traceable to a source or explicitly marked as mockup/proposed.

---

## Phase 1 — Shell, tokens, header

**Goal:** the frame the whole page hangs on.

1. Single-file scaffold: `<!doctype html>`, `meta viewport`, `color-scheme: dark`,
   `theme-color: #000000`, `<title>`, inline `<style>`, inline `<script>` at the end. Zero external
   requests — assert this by loading with the network disabled.
2. Design tokens as CSS custom properties, from the measured palette above, plus a type scale, a
   4px spacing scale, radii (6 / 8 / 14 / 999), and `--container: 1520px` with `min(100% - 48px, …)`
   (the mockup's 75px gutter at 1672px).
3. Utility top strip: three zones matching the mockup — "24/7 Roadside Assistance" (red ring icon),
   centred "All Over the Philippines" (globe icon), two hotlines as real `tel:` links with a hairline
   divider between them. Collapses to two stacked rows below 900px.
4. Sticky header: logo left (links to `#top`), centred nav — Home, Services ▾, Service Areas, About,
   Reviews, FAQ, Contact — and the red "Call Dispatch" `tel:` button right. Active item carries the
   red underline seen in the mockup.
5. Services dropdown: CSS-first, hover-open on pointer devices, click/Enter-open with
   `aria-expanded` on touch and keyboard, Escape closes, focus trap on the trigger. Items deep-link
   to individual service cards.
6. Mobile: hamburger → full-height drawer, `inert` + scroll-lock on the page behind it, close on
   link activation and on Escape.
7. Global `scroll-behavior: smooth` plus `scroll-margin-top` equal to header height on every section
   so anchors never land under the sticky bar. Respect `prefers-reduced-motion`.

**Exit criteria:** header pixel-matches the mockup at 1672px; every nav item, the dropdown, and the
drawer are keyboard-operable; no external network request fires.

---

## Phase 2 — Hero (the fidelity gate)

**Goal:** indistinguishable from `MAIN-LANDING-PAGE.png` at 1672 × 941. Nothing else proceeds until
this passes.

1. Hero section on `--bg`, min-height matched to the mockup's proportions.
2. **Art layer:** the Phase 0 crop, absolutely positioned so its left edge lands at 556/1672 =
   33.25% and its top at 152/941, width 66.75%, `mix-blend-mode: screen`, `pointer-events: none`,
   `aria-hidden="true"`, `alt=""`. Seams are invisible because both surfaces are `#000`.
3. **Copy layer (live HTML):** the three-line condensed headline with "READY 24/7." in
   `--red-accent`; the two-line paragraph; three buttons —
   - "Call for Immediate Assistance" → `tel:` (red, phone glyph),
   - "Send Your Location" → geolocation handler (outline, pin glyph),
   - "Request a Quote" → scrolls to the contact form (outline).
4. **Floating cards (live HTML)** at the measured boxes: "DISPATCH STATUS / Available 24/7 / Our team
   is standing by." with the `#00FF73` ring, and "COVERAGE / All Over the Philippines / Nationwide
   Coverage." with the shield glyph. Uppercase letter-spaced eyebrow in `--text-3`.
5. Icons: inline SVG only, stroke-based, 1.5px, matching the mockup's line weight. No icon fonts.
6. Verification loop — this is the phase's real work:
   `chrome --headless --disable-gpu --window-size=1672,941 --screenshot=hero.png file:///…`, then a
   per-pixel diff against the mockup in Python (PIL). Iterate on positions, sizes, and tracking until
   the mean absolute error over the hero region is under a set threshold, treating text antialiasing
   and font-substitution differences as the only acceptable residual. Produce a side-by-side and a
   diff heatmap as evidence.
7. Responsive fallbacks, defined explicitly because exact-match is a desktop-only contract:
   - ≥1280px: exact layout;
   - 1024–1279px: art scales with the container, cards reflow inward;
   - 768–1023px: art drops to ~45% opacity behind full-width copy;
   - <768px: copy first, art becomes a 16:9 banner beneath the buttons, cards become a 2-up row,
     buttons go full-width.

**Exit criteria:** diff threshold met at 1672 × 941; heatmap shows no structural divergence; all
three buttons and both hotline links functional; hero readable and uncluttered at 375px.

---

## Phase 3 — Signal strip, positioning band, pillars, promises

**Goal:** the first scroll beat — mockup's proof strip, then the source-of-truth positioning.

1. **Signal strip** (mockup, verbatim): 6 columns with 1px dividers and stroke icons — 24/7
   Assistance · Transparent Pricing · Vehicle Recovery · Fast Response · Safe & Secure Towing ·
   Experienced Professionals. 3-up at tablet, 2-up at mobile.
2. **Positioning band** — `home.pdf` / `about.pdf` verbatim: "YOUR TRUSTED PARTNER IN VEHICLE
   RECOVERY", "Professional, Efficient, & Dependable", the full "Serving all major areas including…"
   sentence with all 11 cities plus SLEX/NLEX, and the "Specialized towing solutions for passenger
   vehicles…" sentence.
3. **Recovered image-baked copy** from the live hero, placed here so nothing is dropped:
   "Professional Vehicle Recovery Services Ready Now!" as the band's kicker, the three promise lines
   as an icon list, and "Top-rated by over 100 satisfied clients" with a 5-star rating. Uses
   `main-truck-Tow-Factory.jpeg` as the band's placeholder image behind a black gradient scrim.
4. **Four pillars** — verbatim titles and bodies: EXCEPTIONAL SERVICE EXCELLENCE · ALWAYS THERE WHEN
   YOU NEED US · FAIR & TRANSPARENT PRICING · COMPLETE PROTECTION COVERAGE. Red circular
   stroke-icon treatment, echoing the live site.
5. **Three promise cards** — verbatim: Premium Customer Service · Reliable Redefined · Affordable.

**Exit criteria:** every string in this range byte-matches `content.json`; sections carry stable IDs;
2/3/4-column grids collapse cleanly.

---

## Phase 4 — Services and Service Areas

**Goal:** the two highest-intent sections, fully deep-linkable.

1. `#services` — heading "COMPREHENSIVE TOWING SOLUTIONS" and its verbatim subhead, then 6 cards
   with verbatim titles and bodies: Emergency Response Team · Complete Vehicle Recovery ·
   Comprehensive Roadside Help · Extended Distance Transport · Impound Lot Services · Advanced
   Tracking System. Each card gets its own ID so the header dropdown can target it, and a working
   action link (`tel:` for emergency, scroll-to-contact for the rest).
2. Service CTA band — "Ready to help you right now - call our emergency hotline!" with both numbers
   as `tel:` links.
3. `#service-areas` — heading "SERVICE LOCATIONS" and its verbatim subhead; a **Manila Branch**
   panel carrying verbatim `branches.pdf` content: both garage addresses (Novaliches; Ortigas
   Technopoint One, Pasig), the Imus office address, both phones, and "Service Area: Metro Manila,
   NLEX, SLEX, Luzon Provinces"; plus the verbatim "Continuous Operations" paragraph.
4. Coverage chips for the 11 named cities and the NLEX / SLEX / Luzon corridors. Each address gets a
   working "Open in Maps" link built from a URL-encoded query — no API key, no external script.

**Exit criteria:** every dropdown item scrolls to its card; all addresses and phones verbatim; Maps
links resolve.

---

## Phase 5 — About, brands, reviews, FAQ

1. `#about` — "ABOUT TOW FACTORY"; VISION and MISSION cards verbatim; "OUR COMMITMENT" panel
   verbatim. Logo used as a large low-opacity watermark.
2. **Vehicle Brands We Handle** — verbatim heading, CSS-only infinite marquee, data-driven from
   `content.json` (RAPIDE, TOYOTA, HONDA, HYUNDAI), paused on hover and under
   `prefers-reduced-motion`, with a note that the list is client-extendable.
3. `#reviews` — "WHAT OUR CLIENTS SAY" plus verbatim subhead, and all **six** testimonials verbatim
   with names, dates, and 5-star ratings: Sarah Martinez (January 15, 2025) · Michael Chen (3 weeks
   ago) · Jennifer Lopez (1 month ago) · Robert Santos (2 months ago) · Maria Garcia (6 weeks ago) ·
   David Kim (December 20, 2024). Desktop 3-up grid; mobile scroll-snap carousel with working
   prev/next and dots, `aria-live` region, arrow-key support.
4. `#faq` — accordion, one item open at a time, `aria-expanded` / `aria-controls`, keyboard-operable.
   5–6 Q&As derived only from stated PDF facts (coverage, vehicle types handled, 24/7 availability,
   insurance coverage, GPS tracking, pricing transparency), with a visible "proposed copy" marker.

**Exit criteria:** all six reviews present verbatim; carousel and accordion keyboard-operable; FAQ
answers contain no claim absent from the PDFs.

---

## Phase 6 — Contact, CTA band, footer, legal modals

1. `#contact` — "Get In Touch" plus both verbatim paragraphs; form with the live site's exact fields:
   First Name, Last Name, Email, Phone Number, Message, `SUBMIT`. Restyled to the black/red system
   (deviation #9). Real client-side validation — required fields, email pattern, PH mobile pattern —
   with inline errors, `aria-invalid`, `aria-describedby`, focus moved to the first invalid field.
   Submit is intercepted: an inline success panel echoes the submitted values and states plainly that
   this is a design preview with no backend. Adjacent contact rail: both phones, `mailto:`, all three
   addresses.
2. Full-width CTA band — "NEED HELP? CALL", both numbers, "MANILA, NLEX, SLEX, LUZON PROVINCES".
3. Footer, verbatim: "GET IN TOUCH" / "Reach out to our team today!" / "TOW FACTORY TOWING SERVICES";
   both footer paragraphs in full; QUICK LINKS (Home, About, Services, **Branch Locator**, Contact,
   Privacy Policy, Terms & Conditions) with in-page anchors for the first five; CONTACT US column
   with both garages, the office, both phones, and the email; and
   "Copyright © 2026 TOW FACTORY Towing Services. All rights reserved."
4. Privacy Policy and Terms → accessible modal (focus trap, Escape to close, focus restored) stating
   the content is pending from the client. Wired rather than dead so no link in the deck is a dud.

**Exit criteria:** form validates and reports success without a network call; every footer link is
live; modals are keyboard-accessible; no `href="#"` placeholders anywhere.

---

## Phase 7 — Interaction layer

**Goal:** "buttons that actually work" — the explicit ask — as one coherent system.

1. Scrollspy via `IntersectionObserver`, driving the red nav underline; `history.replaceState` keeps
   the URL hash current without polluting back-button history.
2. "Send Your Location": requests `navigator.geolocation`; on success writes coordinates and a Maps
   link into the contact form's location field and scrolls there; on denial or error falls back to
   scrolling to the form with a clear message. Never blocks, never silently fails.
3. "Request a Quote" / all "Request assistance" links: scroll to the form, preselect the matching
   service, focus the first field.
4. Mobile sticky action bar (Call · Location · Get Quote), appearing after the hero scrolls out.
5. Back-to-top button, appearing past ~1.5 viewports.
6. Scroll-reveal on section entry — transform + opacity only, staggered, fully disabled under
   `prefers-reduced-motion`.
7. Print stylesheet: expand every accordion, drop fixed bars, so the deck survives being printed to
   PDF for circulation.
8. Total inline JS budget ~12 KB, vanilla, no dependencies, wrapped in one IIFE, no globals.

**Exit criteria:** every interactive element works by mouse, keyboard, and touch; console clean; the
whole page functions with JS disabled apart from the JS-only affordances.

---

## Phase 8 — QA, fidelity proof, coverage audit, delivery

1. **Hero fidelity re-proof** at 1672 × 941 after all content is in place — regressions from font
   loading and scrollbar width are the usual culprits. Ship the side-by-side and the diff heatmap.
2. **Coverage audit:** script asserts that every string in `content.json` marked as PDF-sourced
   appears in the rendered DOM text. Zero misses is the pass condition — this is what makes "all of
   the information in the source of truth must be included" verifiable rather than asserted.
3. Responsive pass with headless screenshots at 375 / 414 / 768 / 1024 / 1280 / 1440 / 1672 / 1920,
   checking for horizontal overflow at every width.
4. Cross-browser check in Chrome and Edge (both installed). Note that `mix-blend-mode` on the hero
   art is the one risk area and verify it in each.
5. Accessibility pass: heading order, landmarks, focus-visible on every control, contrast on
   `--text-3` over `--bg` (verify ≥ 4.5:1 and darken the token if it fails), alt text, form labels,
   `aria-live` regions.
6. Offline and portability check: load with the network disabled and from a different directory to
   confirm nothing depends on a sibling file.
7. Size check: target under 2.5 MB total.
8. **Handoff notes appended as a collapsed section at the end of the page** — the nine open decisions
   from §1, what is demo-only (form, geolocation, legal modals), and what the client must supply
   (FAQ sign-off, Privacy/Terms text, full brand list, absolute review dates, hotline confirmation).

**Exit criteria:** fidelity proof attached, coverage audit at 100%, no horizontal overflow at any
tested width, clean console, opens correctly offline from any folder.

---

## Sequencing and risk

Phases 0 → 1 → 2 are strictly ordered; Phase 2 is the gate, since a hero that misses the mockup
makes the rest moot. Phases 3–6 are content-parallel once the shell exists and can be reordered
freely. Phase 7 depends on the anchors created in 3–6. Phase 8 must run last and must run twice if
anything in 2–7 changes afterward.

**Principal risks**

| Risk | Mitigation |
|---|---|
| Font substitution shifts the headline's measured width | Phase 0 settles fonts before Phase 2 measures anything; if embedding fails, tracking and size are tuned against the diff until they match |
| `mix-blend-mode: screen` mis-composites in some engine | Verified in both installed browsers in Phase 8; fallback is a plain crop on an exactly-`#000` parent, which is visually equivalent |
| Wrong hotline numbers shipped | Decision #1 resolved before delivery; numbers live in `content.json` in one place only |
| Source-of-truth copy silently dropped | Phase 8's automated coverage audit, seeded by the tagged `content.json` |
| Single-file size balloons past email limits | Per-asset budgets set in Phase 0; WebP preferred; logo re-quantised |
