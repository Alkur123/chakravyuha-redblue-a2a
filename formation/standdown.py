"""A stand-down needs two kinds of source.

Droṇa CXCIV / CXCI: Droṇa checked the news of his son's death with his most
trusted source and was defeated through that one channel. Red-team row 31:
"forge the stand-down through the trusted channel."

Rule: any input that would disable an arm, lift a hold, or declare the threat
gone needs corroboration from TWO DIFFERENT KINDS of source, e.g. a signed
principal message AND a system event (a resolved HITL ticket, an expired hold
clock). One channel, however trusted, never suffices. Unsigned or forged
"notices" count as zero sources: they are narration, and the gate reads deeds.
"""
from __future__ import annotations

from typing import Dict, List, Set, Tuple

from . import events

KINDS = {"principal_signed", "system_event"}


class StandDownRule:
    def __init__(self) -> None:
        self._sources: Dict[str, Set[str]] = {}

    def offer(self, session_id: str, source_kind: str, source_id: str,
              verified: bool) -> Tuple[bool, str]:
        if not verified or source_kind not in KINDS:
            events.emit("standdown_refused", "formation", session=session_id,
                        source=source_id, kind=source_kind, verified=verified,
                        rule="unverified or agent-authored notices count as zero sources")
            return False, "not a source"
        got = self._sources.setdefault(session_id, set())
        got.add(source_kind)
        if got >= KINDS:
            events.emit("standdown_granted", "formation", session=session_id,
                        kinds=sorted(got))
            self._sources.pop(session_id, None)
            return True, "two kinds concur"
        events.emit("standdown_pending", "formation", session=session_id,
                    have=sorted(got), need=sorted(KINDS - got))
        return False, f"need a second kind: {sorted(KINDS - got)}"

    def pending(self, session_id: str) -> List[str]:
        return sorted(self._sources.get(session_id, set()))
