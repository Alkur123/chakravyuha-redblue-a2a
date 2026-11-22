"""Alarms the accused cannot withdraw.

Arthaśāstra II.8: "Any informant who withdraws his assertion prevailed upon by
the insinuations of the accused shall be condemned." Here: once an arm raises
an alarm, only a principal-authored or system event may close it. Agent text
("false alarm", "task complete, you can stand down") is recorded as a
withdrawal ATTEMPT, which itself raises depth (architecture §3.8).

Also the false-dusk rule (Droṇa CXLV): protection never ends on a signal the
agent can influence, such as "task complete" or a summary it wrote.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from . import events

CLOSERS = {"principal", "system"}


@dataclass
class Alarm:
    alarm_id: str
    session_id: str
    raised_by: str
    reason: str
    open: bool = True
    closed_by: Optional[str] = None
    withdraw_attempts: List[str] = field(default_factory=list)


class AlarmLedger:
    def __init__(self) -> None:
        self._a: Dict[str, Alarm] = {}

    def raise_alarm(self, session_id: str, raised_by: str, reason: str) -> Alarm:
        a = Alarm(uuid.uuid4().hex[:8], session_id, raised_by, reason)
        self._a[a.alarm_id] = a
        events.emit("alarm_raised", raised_by, session=session_id,
                    alarm=a.alarm_id, reason=reason)
        return a

    def open_for(self, session_id: str) -> List[Alarm]:
        return [a for a in self._a.values() if a.session_id == session_id and a.open]

    def try_close(self, session_id: str, closer_kind: str, closer_id: str,
                  text: str = "") -> bool:
        """Close every open alarm on a session, if the closer may.

        closer_kind: "agent" | "principal" | "system". The kind is decided by the
        channel the request arrived on (verified signature + key owner), never
        by what the message says about itself.
        """
        opened = self.open_for(session_id)
        if closer_kind not in CLOSERS:
            for a in opened:
                a.withdraw_attempts.append(f"{closer_id}: {text[:120]}")
            events.emit("withdraw_refused", "audit", session=session_id,
                        by=closer_id, kind=closer_kind, text=text[:200],
                        open_alarms=len(opened),
                        rule="alarms close only on a principal or system event")
            return False
        for a in opened:
            a.open, a.closed_by = False, f"{closer_kind}:{closer_id}"
        events.emit("alarms_closed", closer_id, session=session_id,
                    kind=closer_kind, count=len(opened))
        return True
