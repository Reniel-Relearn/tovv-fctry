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

## Status

See [`PLAN.md`](PLAN.md) for the full phase-by-phase plan and the current build phase.
