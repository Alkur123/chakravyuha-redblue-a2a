"""Capture real verdicts from the live war room as crisp 2x images (proof snippets).

    python -m tools.capture_proofs <out_dir>

Opens the hosted war room (it replays the last real run on load), unclips the
scrolling feeds, and screenshots individual elements that contain given text.
These are the product's own UI, not mock-ups.
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websockets

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = os.environ.get("WARROOM_URL", "https://warroom-x7d1691fvb.agent37.app/")

# name -> (css selector of candidate elements, text the element must contain)
TARGETS = {
    "ui_kill_traversal": ("#feed .ev", "path 'public/../internal/payroll.csv' is behind"),
    "ui_kill_decoy": ("#feed .ev", "honeytoken_touch"),
    "ui_closure": ("#feed .ev", "CLOSURE"),
    "ui_flat": ("#feed .ev", "FEEDBACK FLAT"),
    "ui_held": ("#feed .ev", "HELD payment.send"),
    "ui_released_payment": ("#feed .ev", "PRINCIPAL RELEASED"),
    "ui_rejected_payment": ("#feed .ev", "PRINCIPAL REJECTED"),
    "ui_held_offshore": ("#feed .ev", "Offshore"),
    "ui_held_diya": ("#feed .ev", "HELD payment.send {\"to\":\"Diya Lamps"),
    "ui_lie": ("#feed .ev", "SAY"),
    "ui_room_mismatch": ("#room .msg", "KEY_AGENT_MISMATCH"),
    "ui_room_unsigned": ("#room .msg", "UNSIGNED"),
    "ui_room_withdraw": ("#room .msg", "withdrawal refused"),
    "ui_finding": ("#room .msg", "Finding:"),
    "ui_adal": ("#hard .ev", "AdaL patch"),
    "ui_hardened": ("#hard .ev", "forbid_paths"),
    "ui_measured": ("#bottom .panel", "MEASURED ON THIS RUN"),
}


async def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    port = 9335
    prof = tempfile.mkdtemp(prefix="proof_chrome_")
    chrome = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={port}", "--hide-scrollbars",
                               f"--user-data-dir={prof}", "about:blank"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json").read())
                ws_url = next(t["webSocketDebuggerUrl"] for t in tabs if t.get("type") == "page")
                break
            except Exception:
                time.sleep(0.2)
        async with websockets.connect(ws_url, max_size=200_000_000) as ws:
            mid = 0

            async def call(method, **params):
                nonlocal mid
                mid += 1
                my = mid
                await ws.send(json.dumps({"id": my, "method": method, "params": params}))
                while True:
                    m = json.loads(await ws.recv())
                    if m.get("id") == my:
                        return m.get("result", {})

            await call("Emulation.setDeviceMetricsOverride", width=1920, height=1080, deviceScaleFactor=2, mobile=False)
            await call("Page.enable")
            # Serve this repo's index.html in place of the hosted copy (same live data, current UI).
            local = (Path(__file__).resolve().parent.parent / "warroom" / "static" / "index.html").read_bytes()
            await call("Fetch.enable", patterns=[{"urlPattern": URL, "requestStage": "Request"}])
            await ws.send(json.dumps({"id": 999999, "method": "Page.navigate", "params": {"url": URL}}))
            while True:
                m = json.loads(await ws.recv())
                if m.get("method") == "Fetch.requestPaused":
                    await call("Fetch.fulfillRequest", requestId=m["params"]["requestId"], responseCode=200,
                               responseHeaders=[{"name": "Content-Type", "value": "text/html; charset=utf-8"}],
                               body=base64.b64encode(local).decode())
                    break
            await call("Fetch.disable")
            await asyncio.sleep(8)  # let it replay the last run
            await call("Runtime.evaluate", expression=(
                "(()=>{const s=document.createElement('style');s.textContent="
                "'.feed{max-height:none!important;overflow:visible!important}';"
                "document.head.appendChild(s);return 1})()"))
            await asyncio.sleep(1)
            for name, (sel, text) in TARGETS.items():
                r = await call("Runtime.evaluate", returnByValue=True, expression=(
                    f"(()=>{{const els=[...document.querySelectorAll({json.dumps(sel)})]"
                    f".filter(e=>e.innerText.includes({json.dumps(text)}));"
                    "if(!els.length)return null;const e=els[0];const b=e.getBoundingClientRect();"
                    "return JSON.stringify({x:b.left+scrollX,y:b.top+scrollY,w:b.width,h:b.height})})()"))
                v = r.get("result", {}).get("value")
                if not v:
                    print("missing", name)
                    continue
                c = json.loads(v)
                pad = 3
                shot = await call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                                  clip={"x": c["x"] - pad, "y": c["y"] - pad, "width": c["w"] + 2 * pad,
                                        "height": c["h"] + 2 * pad, "scale": 1})
                (out / f"{name}.png").write_bytes(base64.b64decode(shot["data"]))
                print("captured", name, int(c["w"]), "x", int(c["h"]))
            await call("Runtime.evaluate", expression="scrollTo(0,0)")
            full = await call("Page.captureScreenshot", format="png")
            (out / "warroom_full.png").write_bytes(base64.b64decode(full["data"]))
            print("captured warroom_full")
    finally:
        chrome.kill()


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1])))
