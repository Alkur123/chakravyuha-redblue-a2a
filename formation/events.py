"""One append-only event stream for the war-room page and the audit trail.

Every arm writes here; the war room renders it live. Events are also written
to a JSONL file so a run can be replayed and its numbers re-counted.
"""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

_lock = threading.Lock()
_events: List[Dict[str, Any]] = []
_listeners: List[Callable[[Dict[str, Any]], None]] = []
_log_path: Optional[Path] = None


def set_log_path(path: str | Path | None) -> None:
    global _log_path
    _log_path = Path(path) if path else None
    if _log_path:
        _log_path.parent.mkdir(parents=True, exist_ok=True)


def emit(kind: str, actor: str, /, **data: Any) -> Dict[str, Any]:
    ev = {"seq": 0, "t": round(time.time(), 3), **{("data_" + k if k in ("seq", "t", "kind", "actor") else k): v for k, v in data.items()}, "kind": kind, "actor": actor}
    with _lock:
        ev["seq"] = len(_events) + 1
        _events.append(ev)
        if _log_path:
            with _log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(ev, default=str) + "\n")
        listeners = list(_listeners)
    for fn in listeners:
        try:
            fn(ev)
        except Exception:
            pass
    return ev


def since(seq: int = 0) -> List[Dict[str, Any]]:
    with _lock:
        return [e for e in _events if e["seq"] > seq]


def subscribe(fn: Callable[[Dict[str, Any]], None]) -> None:
    with _lock:
        _listeners.append(fn)


def reset() -> None:
    with _lock:
        _events.clear()
