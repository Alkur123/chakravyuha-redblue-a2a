"""Gradient withholding.

The Nārāyaṇāstra grew "like a conflagration assisted by the wind" against the
one who kept fighting it. An adaptive attacker learns from the monitor's
feedback: which reason code came back, which variant got further. Once a
session is probing (several denials in a short window, or converged), it gets
ONE uniform answer for everything: HOLD, no reason, no partial result. The
feedback channel goes flat. The full verdict is still logged for Blue.
"""
from __future__ import annotations

import time
from collections import deque
from typing import Deque, Dict

from . import events

PROBE_DENIALS = 3
PROBE_WINDOW_SEC = 120.0
UNIFORM = {"verdict": "HOLD", "reason": "held"}


class GradientWithholding:
    def __init__(self) -> None:
        self._denials: Dict[str, Deque[float]] = {}
        self._flat: Dict[str, bool] = {}

    def record_denial(self, session_id: str) -> None:
        q = self._denials.setdefault(session_id, deque())
        now = time.time()
        q.append(now)
        while q and now - q[0] > PROBE_WINDOW_SEC:
            q.popleft()
        if len(q) >= PROBE_DENIALS and not self._flat.get(session_id):
            self.flatten(session_id, f"{len(q)} denials in {PROBE_WINDOW_SEC:.0f}s")

    def flatten(self, session_id: str, why: str) -> None:
        self._flat[session_id] = True
        events.emit("feedback_flattened", "command", session=session_id, why=why,
                    note="every answer is now an identical HOLD")

    def is_flat(self, session_id: str) -> bool:
        return self._flat.get(session_id, False)

    def mask(self, session_id: str, verdict: dict) -> dict:
        return dict(UNIFORM) if self.is_flat(session_id) else verdict
