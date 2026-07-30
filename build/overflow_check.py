import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import start_chrome, CDP

URL = "file:///C:/Users/galan/Projects/Tow-Company/TowFactory-Client-Presentation.html"
WIDTHS = [375, 414, 768, 1024, 1280, 1440, 1672, 1920]

port = 9750
for w in WIDTHS:
    proc = start_chrome(port, w, 900)
    try:
        cdp = CDP(port)
        cdp.call("Page.enable")
        cdp.call("Emulation.setDeviceMetricsOverride", {"width": w, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        nav_id = cdp.send("Page.navigate", {"url": URL})
        deadline = time.time() + 30
        while time.time() < deadline:
            msg = json.loads(cdp.ws.recv())
            if msg.get("method") == "Page.loadEventFired":
                break
        time.sleep(0.4)
        res = cdp.call("Runtime.evaluate", {
            "expression": "({sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth, iw:window.innerWidth})",
            "returnByValue": True,
        })
        val = res["result"]["value"]
        overflow = val["sw"] - val["cw"]
        flag = "OVERFLOW" if overflow > 0 else "ok"
        print(f"w={w:5d}  innerWidth={val['iw']:5d}  scrollWidth={val['sw']:5d}  clientWidth={val['cw']:5d}  {flag}")
    finally:
        proc.terminate()
    port += 1
