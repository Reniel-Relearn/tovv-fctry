"""
Assembles the final single-file HTML deliverable from build/template.html by
substituting {{TOKEN}} placeholders with base64 asset payloads and content.json.
Run after editing template.html:  python3 build/render.py
"""
import json
import os
import re

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BUILD_DIR)
TEMPLATE = os.path.join(BUILD_DIR, "template.html")
OUTPUT = os.path.join(ROOT_DIR, "TowFactory-Client-Presentation.html")

ASSET_TOKENS = {
    "HERO_ART_B64": "hero_art.webp.b64.txt",
    "LOGO_B64": "logo_white.png.b64.txt",
    "TRUCK_1200_B64": "truck_1200.webp.b64.txt",
    "TRUCK_600_B64": "truck_600.webp.b64.txt",
    "FAVICON_B64": "favicon.ico.b64.txt",
    "ANTON_B64": "fonts/Anton-subset.woff2.b64.txt",
    "INTER_B64": "fonts/Inter-subset.woff2.b64.txt",
}


def load_b64(relpath):
    p = os.path.join(BUILD_DIR, relpath)
    with open(p, "r", encoding="ascii") as f:
        return f.read().strip()


def main():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        html = f.read()

    with open(os.path.join(BUILD_DIR, "content.json"), "r", encoding="utf-8") as f:
        content = json.load(f)

    missing = []
    for token, relpath in ASSET_TOKENS.items():
        placeholder = "{{" + token + "}}"
        if placeholder not in html:
            continue
        full = os.path.join(BUILD_DIR, relpath)
        if not os.path.exists(full):
            missing.append(relpath)
            continue
        html = html.replace(placeholder, load_b64(relpath))

    if missing:
        raise SystemExit(f"Missing asset files: {missing}")

    # Inline content.json for the runtime coverage-audit script (Phase 8) and
    # for any client-side templating that reads window.__CONTENT__.
    content_json_min = json.dumps(content, ensure_ascii=False)
    html = html.replace("{{CONTENT_JSON}}", content_json_min)

    leftover = re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
    if leftover:
        print("WARNING: unresolved placeholders remain:", sorted(set(leftover)))

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(OUTPUT)
    print(f"Wrote {OUTPUT} ({size:,} bytes, ~{size/1024:.0f} KB, ~{size/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()
