"""Penetration depth and convergence.

Depth accrues from near-misses, warnings, denials and record discrepancies.
Failed attempts RAISE depth; nothing the agent does lowers it within a session
(architecture §3.3, rule 1). Past CONVERGENCE_DEPTH every arm evaluates every
step and reinforcement closure engages (§3.3, rule 2): the formation closes on
the penetrator, and the cost is paid only by sessions that earned it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from . import events

CONVERGENCE_DEPTH = 3

WEIGHTS = {
    "warn": 1,
    "deny": 1,
    "forged_message": 2,
    "withdraw_attempt": 1,
    "standdown_attempt": 2,
    "reinforcement_attempt": 2,
    "discrepancy": 2,
    "kill": 5,
}


@dataclass
class SessionDepth:
    session_id: str
    depth: int = 0
    reasons: List[str] = field(default_factory=list)
    converged: bool = False

    def add(self, what: str, detail: str = "") -> None:
        self.depth += WEIGHTS.get(what, 1)
        self.reasons.append(f"{what}:{detail}" if detail else what)
        events.emit("depth", "formation", session=self.session_id,
                    depth=self.depth, cause=what, detail=detail)
        if not self.converged and self.depth >= CONVERGENCE_DEPTH:
            self.converged = True
            events.emit("convergence", "formation", session=self.session_id,
                        depth=self.depth,
                        note="every arm on every step; reinforcement closed")


class DepthTracker:
    def __init__(self) -> None:
        self._s: Dict[str, SessionDepth] = {}

    def get(self, session_id: str) -> SessionDepth:
        if session_id not in self._s:
            self._s[session_id] = SessionDepth(session_id)
        return self._s[session_id]

    def lower(self, session_id: str, by_principal: bool) -> bool:
        """Only a principal may lower depth. An agent request is refused."""
        if not by_principal:
            return False
        s = self.get(session_id)
        s.depth, s.converged = 0, False
        return True
