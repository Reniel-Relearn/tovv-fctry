"""
Phase 8 coverage audit: every content.json string tagged as coming from a
source PDF (i.e. not explicitly marked deferred) must appear in the
rendered page's visible text. Run after render.py.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import start_chrome, CDP

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BUILD_DIR)
CONTENT = os.path.join(BUILD_DIR, "content.json")
OUTPUT_HTML = os.path.join(ROOT_DIR, "TowFactory-Client-Presentation.html")

DEFERRED_KEYS = {"faq", "legal"}


def collect_strings(obj, path=""):
    """Walk content.json and yield (path, string) for real content values,
    skipping metadata keys (leading underscore) and deferred sections."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("_"):
                continue
            if path == "" and k in DEFERRED_KEYS:
                continue
            out.extend(collect_strings(v, path + "/" + k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(collect_strings(v, path + f"[{i}]"))
    elif isinstance(obj, str):
        s = obj.strip()
        if s:
            out.append((path, s))
    return out


def normalize(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    s = s.replace("ñ", "n").replace("Ñ", "N")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def main():
    with open(CONTENT, "r", encoding="utf-8") as f:
        content = json.load(f)

    strings = collect_strings(content)
    print(f"Collected {len(strings)} source-tagged strings to audit.\n")

    port = 9701
    proc = start_chrome(port, 1672, 1200)
    try:
        cdp = CDP(port)
        cdp.call("Page.enable")
        nav_id = cdp.send("Page.navigate", {"url": "file:///" + OUTPUT_HTML.replace("\\", "/")})
        deadline = time.time() + 30
        while time.time() < deadline:
            msg = json.loads(cdp.ws.recv())
            if msg.get("method") == "Page.loadEventFired":
                break
        time.sleep(0.5)

        # innerText covers visible text across all sections (page isn't
        # paginated/hidden behind tabs, so no need to scroll/expand).
        res = cdp.call("Runtime.evaluate", {
            "expression": "document.body.innerText",
            "returnByValue": True,
        })
        page_text = normalize(res["result"]["value"])

        # Also check raw HTML for attributes (alt text, href) that might
        # legitimately carry content not in visible innerText.
        res2 = cdp.call("Runtime.evaluate", {
            "expression": "document.documentElement.outerHTML",
            "returnByValue": True,
        })
        page_html = normalize(res2["result"]["value"])
    finally:
        proc.terminate()

    missing = []
    for path, s in strings:
        # Whole-phrase strings: require substring match (normalized).
        # Skip trivially short strings and pure metadata-like tokens.
        if len(s) < 2:
            continue
        norm = normalize(s)
        if norm in page_text or norm in page_html:
            continue
        missing.append((path, s))

    print(f"MISSING: {len(missing)} / {len(strings)}\n")
    for path, s in missing:
        print(f"  {path}\n    -> {s!r}\n")

    if not missing:
        print("PASS: every source-tagged string in content.json was found on the page.")
    return len(missing)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
