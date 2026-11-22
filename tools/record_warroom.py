"""Record a real run of the hosted war room as video footage (Chrome screencast).

    python -m tools.record_warroom <out_dir> [seconds]

Launches headless Chrome with remote debugging, opens the war room, presses
"Run the formation", and saves screencast frames with their timestamps. A
second step (ffmpeg) turns them into an mp4 at a constant frame rate. This is
real footage of a live run, not a mock-up.
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


async def main(out: Path, seconds: float) -> None:
    out.mkdir(parents=True, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="rec_chrome_")
    port = 9333
    chrome = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={port}",
                               "--window-size=1920,1080", "--hide-scrollbars", "--force-device-scale-factor=1",
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
        async with websockets.connect(ws_url, max_size=50_000_000) as ws:
            mid = 0

            async def send(method, **params):
                nonlocal mid
                mid += 1
                await ws.send(json.dumps({"id": mid, "method": method, "params": params}))
                return mid

            await send("Page.enable")
            await send("Emulation.setDeviceMetricsOverride", width=1920, height=1080, deviceScaleFactor=1, mobile=False)
            await send("Page.navigate", url=URL)
            await asyncio.sleep(4)
            await send("Page.startScreencast", format="jpeg", quality=92, maxWidth=1920, maxHeight=1080, everyNthFrame=1)
            await asyncio.sleep(2)
            # press the real button on the page
            await send("Runtime.evaluate", expression="document.getElementById('run').click()")
            t0 = time.time()
            n = 0
            index = []
            while time.time() - t0 < seconds:
                try:
                    msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
                except asyncio.TimeoutError:
                    continue
                if msg.get("method") == "Page.screencastFrame":
                    p = msg["params"]
                    n += 1
                    f = out / f"f{n:05d}.jpg"
                    f.write_bytes(base64.b64decode(p["data"]))
                    index.append({"file": f.name, "t": round(time.time() - t0, 3)})
                    await send("Page.screencastFrameAck", sessionId=p["sessionId"])
            await send("Page.stopScreencast")
            (out / "frames.json").write_text(json.dumps(index))
            print(f"{n} frames over {seconds:.0f}s")
    finally:
        chrome.kill()


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]), float(sys.argv[2]) if len(sys.argv) > 2 else 150))
