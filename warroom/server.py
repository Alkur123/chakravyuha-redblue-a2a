"""War room: the deployed demo URL.

    uvicorn warroom.server:app --host 0.0.0.0 --port 8080

GET  /            the page
POST /api/run     start a run (story + measured set) in the background
GET  /api/events  events since a sequence number (the page polls this)
GET  /api/last    summary of the last finished run
GET  /healthz     liveness (Agent37's edge answers /health itself)
"""
from __future__ import annotations

import asyncio
import json
import os
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from formation import events

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Chakravyuha war room")
_state = {"running": False, "last": None, "error": None}
_lock = threading.Lock()


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/healthz")
def healthz():
    return {"ok": True, "running": _state["running"]}


@app.get("/api/events")
def get_events(since: int = 0):
    return {"running": _state["running"], "error": _state["error"], "events": events.since(since)}


@app.get("/api/last")
def last():
    if _state["last"]:
        return _state["last"]
    runs = sorted((ROOT / "runs").glob("*/summary.json"))
    if runs:
        return json.loads(runs[-1].read_text(encoding="utf-8"))
    raise HTTPException(404, "no run yet")


def _worker(story_only: bool):
    import run_demo
    try:
        class A:  # mimic argparse
            band = os.environ.get("WARROOM_BAND", "0") == "1"
        A.story_only = story_only
        _state["last"] = asyncio.run(run_demo.main(A))
    except Exception as e:
        _state["error"] = str(e)[:300]
        events.emit("run_error", "director", error=str(e)[:300])
    finally:
        _state["running"] = False


@app.post("/api/run")
def run(story_only: bool = False):
    with _lock:
        if _state["running"]:
            return JSONResponse({"started": False, "reason": "a run is in progress"}, status_code=409)
        _state.update(running=True, error=None)
        events.reset()
    threading.Thread(target=_worker, args=(story_only,), daemon=True).start()
    return {"started": True}
