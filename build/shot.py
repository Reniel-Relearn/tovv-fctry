"""
Reliable full-fidelity headless screenshot tool using the Chrome DevTools Protocol
directly (bypasses the `--screenshot` CLI flag, which clamps small viewports to a
~500px minimum width regardless of --window-size).

Usage:
  python3 build/shot.py <url> <out.png> <width> <height> [--full] [--selector CSS] [--scroll Y]

  --full            capture full scrollable page height instead of just the viewport
  --selector CSS    capture only the bounding box of the first matching element
  --scroll Y        scroll to Y before capturing (px)
  --wait MS         extra wait after load before capturing (default 150ms)
"""
import json
import os
import subprocess
import sys
import time
import base64
import uuid
import urllib.request

import websocket

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

PROFILE_ROOT = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "claude-cdp-profile")


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("Chrome not found")


def start_chrome(port, width, height):
    chrome = find_chrome()
    profile = PROFILE_ROOT + f"-{port}"
    os.makedirs(profile, exist_ok=True)
    args = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-color-profile=srgb",
        "--force-device-scale-factor=1",
        f"--user-data-dir={profile}",
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--window-size={width},{height}",
        "about:blank",
    ]
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # wait for devtools endpoint
    for _ in range(100):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=0.5) as r:
                json.loads(r.read())
                return proc
        except Exception:
            time.sleep(0.1)
    raise SystemExit("Chrome devtools endpoint did not come up")


class CDP:
    def __init__(self, port):
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=5) as r:
            targets = json.loads(r.read())
        pages = [t for t in targets if t.get("type") == "page"]
        if not pages:
            raise RuntimeError("no page targets found")
        self.ws_url = pages[0]["webSocketDebuggerUrl"]
        self.ws = websocket.create_connection(self.ws_url, timeout=30)
        self.msg_id = 0
        self._buf = []

    def send(self, method, params=None):
        self.msg_id += 1
        mid = self.msg_id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        return mid

    def recv_until(self, mid, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            raw = self.ws.recv()
            msg = json.loads(raw)
            if msg.get("id") == mid:
                return msg
            self._buf.append(msg)
        raise TimeoutError(f"timed out waiting for response id={mid}")

    def call(self, method, params=None, timeout=30):
        mid = self.send(method, params)
        msg = self.recv_until(mid, timeout)
        if "error" in msg:
            raise RuntimeError(f"{method} failed: {msg['error']}")
        return msg.get("result", {})


def main():
    args = sys.argv[1:]
    if len(args) < 4:
        print(__doc__)
        raise SystemExit(1)
    url, out, width, height = args[0], args[1], int(args[2]), int(args[3])
    full = "--full" in args
    selector = None
    scroll_y = None
    wait_ms = 150
    if "--selector" in args:
        selector = args[args.index("--selector") + 1]
    if "--scroll" in args:
        scroll_y = int(args[args.index("--scroll") + 1])
    if "--wait" in args:
        wait_ms = int(args[args.index("--wait") + 1])

    port = 9333 + (uuid.uuid4().int % 5000)
    proc = start_chrome(port, width, height)
    try:
        cdp = CDP(port)
        cdp.call("Page.enable")
        cdp.call("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height, "deviceScaleFactor": 1, "mobile": False,
        })
        nav_id = cdp.send("Page.navigate", {"url": url})
        # wait for Page.loadEventFired
        deadline = time.time() + 30
        loaded = False
        while time.time() < deadline:
            raw = cdp.ws.recv()
            msg = json.loads(raw)
            if msg.get("method") == "Page.loadEventFired":
                loaded = True
                break
            if msg.get("id") == nav_id and "error" in msg:
                raise RuntimeError(msg["error"])
        if not loaded:
            raise TimeoutError("page did not fire load event")

        time.sleep(wait_ms / 1000.0)

        if scroll_y is not None:
            cdp.call("Runtime.evaluate", {"expression": f"window.scrollTo(0,{scroll_y})"})
            time.sleep(0.1)

        clip = None
        if selector:
            expr = (
                "(function(){var el=document.querySelector(" + json.dumps(selector) + ");"
                "if(!el) return null; var r=el.getBoundingClientRect();"
                "return {x:r.x,y:r.y,width:r.width,height:r.height};})()"
            )
            res = cdp.call("Runtime.evaluate", {"expression": expr, "returnByValue": True})
            val = res.get("result", {}).get("value")
            if not val:
                raise RuntimeError(f"selector not found: {selector}")
            clip = {"x": val["x"], "y": val["y"], "width": val["width"], "height": val["height"], "scale": 1}
            # Element may sit beyond the emulated viewport height; grow the
            # metrics override to cover it so captureBeyondViewport has real
            # layout to read from (clip.y/height alone isn't enough).
            need_h = int(val["y"] + val["height"]) + 50
            if need_h > height:
                cdp.call("Emulation.setDeviceMetricsOverride", {
                    "width": width, "height": need_h, "deviceScaleFactor": 1, "mobile": False,
                })
                time.sleep(0.1)
        elif full:
            res = cdp.call("Runtime.evaluate", {
                "expression": "({w:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight})",
                "returnByValue": True,
            })
            val = res["result"]["value"]
            cdp.call("Emulation.setDeviceMetricsOverride", {
                "width": width, "height": max(val["h"], height), "deviceScaleFactor": 1, "mobile": False,
            })
            time.sleep(0.1)

        shot_params = {"format": "png", "captureBeyondViewport": True}
        if clip:
            shot_params["clip"] = clip
        result = cdp.call("Page.captureScreenshot", shot_params, timeout=60)
        data = base64.b64decode(result["data"])
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "wb") as f:
            f.write(data)
        print(f"wrote {out} ({len(data)} bytes)")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
