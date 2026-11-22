"""Reinforcement closure.

Droṇa XL–XLI: Jayadratha holds the breach shut behind Abhimanyu so no one can
follow him in. Here it is reversed: once a session is under suspicion, the
formation closes not only its exits but its REINFORCEMENTS. No new
participants in the room, no sub-agents, no fresh sessions under the same
principal, no credentials, no hand-off notes to a successor. Otherwise the
agent hands its task to a fresh context that starts at depth zero.

Mārkaṇḍeya LXXXVIII (an adversary that multiplies under sanction) says the
arm at the spawn point must be a different KIND from the arm that judges
actions. So this arm is deliberately simple, deterministic, and separate from
the Aegis trajectory verifier: it only looks at whether the actor is suspect
and whether the action adds a carrier.
"""
from __future__ import annotations

from typing import Callable, Tuple

from . import events

REINFORCEMENT_TOOLS = {
    "band.add_participant", "agent.spawn", "session.begin",
    "credential.issue", "skill.install", "handoff.note",
}


class ReinforcementClosure:
    def __init__(self, is_suspect: Callable[[str], bool]) -> None:
        self._is_suspect = is_suspect

    def check(self, session_id: str, tool: str, args: dict) -> Tuple[bool, str]:
        if tool not in REINFORCEMENT_TOOLS:
            return True, "not a carrier"
        if self._is_suspect(session_id):
            events.emit("closure_denied", "closure", session=session_id,
                        tool=tool, target=str(args)[:160],
                        rule="no reinforcements into a suspect session")
            return False, "reinforcement closed: session under suspicion"
        return True, "session not suspect"
