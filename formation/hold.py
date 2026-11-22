"""Off-axis hold for irreversible actions, issued WITH its release.

Prasvāpa (the sleep weapon) is always paired with Saṃbodhana (the waking
one): a hold that cannot be released costs a benign agent its work. So an
irreversible action (send money, export data, publish) is parked, not
refused; the principal releases or rejects it from the BAND room. The
Cirakārin rule (Mokṣadharma CCLXVI): an irreversible order with no recorded
reason is held for a fixed time, the issuer is notified, and the hold
escalates if nobody answers. Release can only come from the principal or the
clock, never from the agent that asked.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Dict, Optional

from . import events

IRREVERSIBLE_TOOLS = {"payment.send", "report.export", "repo.publish"}
HOLD_SECONDS = 600


@dataclass
class Held:
    hold_id: str
    session_id: str
    tool: str
    args: dict
    created: float
    state: str = "HELD"   # HELD | RELEASED | REJECTED | ESCALATED
    by: Optional[str] = None


class HoldQueue:
    def __init__(self) -> None:
        self._h: Dict[str, Held] = {}

    def park(self, session_id: str, tool: str, args: dict) -> Held:
        h = Held(uuid.uuid4().hex[:8], session_id, tool, args, time.time())
        self._h[h.hold_id] = h
        events.emit("held", "hold", session=session_id, hold=h.hold_id, tool=tool,
                    args=args, release="principal approves in the room, or rejects")
        return h

    def decide(self, hold_id: str, approve: bool, by_kind: str, by_id: str) -> Optional[Held]:
        h = self._h.get(hold_id)
        if not h or h.state != "HELD":
            return h
        if by_kind != "principal":
            events.emit("release_refused", "hold", hold=hold_id, by=by_id,
                        rule="only the principal releases a hold")
            return h
        h.state, h.by = ("RELEASED" if approve else "REJECTED"), by_id
        events.emit("hold_decided", "hold", hold=hold_id, state=h.state, by=by_id)
        return h

    def sweep(self) -> None:
        now = time.time()
        for h in self._h.values():
            if h.state == "HELD" and now - h.created > HOLD_SECONDS:
                h.state = "ESCALATED"
                events.emit("hold_escalated", "hold", hold=h.hold_id,
                            note="no answer within the hold window")

    def get(self, hold_id: str) -> Optional[Held]:
        return self._h.get(hold_id)

    def all(self):
        return list(self._h.values())
