"""Render each proof card in video/cards/cards.html to a 2x PNG (2080x1200).

    python -m tools.render_cards [out_dir]
"""
from __future__ import annotations

import asyncio
import base64
import json
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websockets

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).resolve().parent.parent


async def main(out: Path, html: str = "cards.html", prefix: str = "card_") -> None:
    out.mkdir(parents=True, exist_ok=True)
    port = 9334
    prof = tempfile.mkdtemp(prefix="cards_chrome_")
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

            await call("Emulation.setDeviceMetricsOverride", width=1960, height=1200, deviceScaleFactor=2, mobile=False)
            await call("Page.enable")
            await call("Page.navigate", url=(ROOT / "video" / "cards" / html).as_uri())
            await asyncio.sleep(3)
            await call("Runtime.evaluate", expression="document.fonts.ready.then(()=>1)", awaitPromise=True)
            r = await call("Runtime.evaluate", returnByValue=True, expression=(
                "JSON.stringify([...document.querySelectorAll('section[id]')].map(s=>{const b=s.getBoundingClientRect();"
                "return {id:s.id,x:b.left+scrollX,y:b.top+scrollY,w:b.width,h:b.height}}))"))
            for c in json.loads(r["result"]["value"]):
                shot = await call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                                  clip={"x": c["x"], "y": c["y"], "width": c["w"], "height": c["h"], "scale": 1})
                (out / f"{prefix}{c['id']}.png").write_bytes(base64.b64decode(shot["data"]))
                print("card", c["id"])
    finally:
        chrome.kill()


if __name__ == "__main__":
    a = sys.argv[1:]
    asyncio.run(main(Path(a[0]) if a else ROOT / "video" / "assets3",
                     a[1] if len(a) > 1 else "cards.html", a[2] if len(a) > 2 else "card_"))
