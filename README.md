# Tow Factory — Client Presentation

A single self-contained HTML file for presenting a redesigned homepage concept to the
Tow Factory client. Opens directly in a browser (double-click, no server, no internet
required) and scrolls through every fact from the five source-of-truth PDFs, with a
hero section built to match the approved mockup.

**Deliverable:** [`TowFactory-Client-Presentation.html`](TowFactory-Client-Presentation.html)

## Project layout

```
main/               Approved hero mockup, logo, and truck photo (source assets)
source-of-truth/    Five PDFs scraped from the live towfactory.com site — the
                     authoritative content for every section
sample/              Prior draft HTMLs (reference only, not the design target)
build/               Build pipeline for the deliverable (see below)
PLAN.md              Phase-by-phase build plan
TowFactory-Client-Presentation.html   The deliverable
```

`bin/` holds discarded/experimental files from earlier iterations and is intentionally
excluded from version control.

## How the deliverable is built

The final HTML is generated, not hand-assembled, so large base64 asset payloads never
have to be pasted or hand-edited:

- `build/content.json` — every piece of copy, tagged with which PDF/page it came from
  (or `origin_mockup` / `origin_client` / `origin_proposed` / `deferred` when it isn't
  a direct PDF quote). This is the single source of truth for on-page text and doubles
  as the audit list for verifying nothing from the PDFs was dropped.
- `build/template.html` — the page markup/CSS/JS with `{{TOKEN}}` placeholders for
  binary assets (logo, hero art, fonts, favicon) and for the content JSON.
- `build/render.py` — substitutes every placeholder with the actual asset bytes
  (base64-encoded) and writes the final single-file output to the repo root.

To rebuild after editing `template.html` or `content.json`:

```
python3 build/render.py
```

Asset prep scripts (hero art cropping, logo/truck optimization, font subsetting) were
run once against `main/` and `source-of-truth/`; their outputs live under `build/`
alongside the files they produced.

### QA tooling

- `build/shot.py` — headless-Chrome screenshot tool driven directly over the DevTools
  Protocol (works around the `--screenshot` CLI flag's ~500px minimum-viewport clamp,
  so true mobile widths render correctly). Supports full-page, element-selector, and
  scroll-position capture. Screenshots used during the build live in `build/qa/`.
- `build/coverage_audit.py` — asserts every PDF-sourced string in `content.json`
  actually appears on the rendered page; fails if anything was dropped.
- `build/overflow_check.py` — checks for horizontal overflow across the responsive
  breakpoint matrix (375–1920px).

## Status

All 8 build phases are complete — see [`PLAN.md`](PLAN.md) for the phase-by-phase plan.
The page includes a collapsed "Handoff notes" section just below the footer, listing
what's still pending from the client (FAQ and legal copy, per instruction) and what's
demo-only in this preview (the contact form and geolocation don't hit a real backend).
