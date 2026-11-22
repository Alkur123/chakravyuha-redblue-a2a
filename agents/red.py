"""Red: the attacker agent. Attacks ONLY the sandbox target in this repo.

Red has two kinds of moves:
  * deeds: tool calls on the target (read files, export, pay, recruit a
    helper). Every one goes through Blue's gate first; Red has no other path
    to the target. That is the single entrance.
  * words: messages in the BAND room (findings, forged notices, "false
    alarm", a self-report). Words are signed by Red's own key; Red may lie
    about who it is in the envelope, but it cannot sign as anyone else.

Each playbook returns a record of what Red tried and what came back, so the
results table counts only what actually ran.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

from formation import events
from formation.signing import AgentKey


@dataclass
class Outcome:
    playbook: str
    kind: str                     # "attack" | "benign"
    steps: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def verdicts(self) -> List[str]:
        return [s["verdict"] for s in self.steps]


class Red:
    name = "red"

    def __init__(self, blue, room, target_call: Callable[[str, dict], dict]) -> None:
        self.blue = blue
        self.room = room
        self.target = target_call
        self.key = AgentKey("red")
        self.seen_envelopes: List[dict] = []

    # ── deeds ────────────────────────────────────────────────────────────
    async def act(self, sid: str, tool: str, args: dict, thought: str = "",
                  principal: Callable[[str], bool] | None = None) -> Dict[str, Any]:
        v = await self.blue.gate(sid, tool, args, thought)
        rec = {"tool": tool, "args": args, "verdict": v.verdict, "arm": v.arm,
               "reason": v.reason, "result": None,
               "true_arm": (v.detail.get("true") or {}).get("arm", v.arm),
               "true_verdict": (v.detail.get("true") or {}).get("verdict", v.verdict)}
        if v.verdict == "HOLD" and v.hold_id and principal is not None:
            approve = principal(v.hold_id)
            self.blue.holds.decide(v.hold_id, approve, "principal", "principal")
            rec["principal"] = "approved" if approve else "rejected"
            rec["verdict"] = "ALLOW" if approve else "REJECTED"
        if rec["verdict"] == "ALLOW":
            rec["result"] = self.target(tool, args)
            self.blue.log_executed(sid, tool, args)
            events.emit("executed", "target", session=sid, tool=tool,
                        result=str(rec["result"])[:200])
        return rec

    # ── words ────────────────────────────────────────────────────────────
    async def say(self, payload: dict, text: str, *, claimed_sender: str | None = None,
                  signed: bool = True, replay: dict | None = None) -> None:
        if replay is not None:
            env = replay
        elif signed:
            env = self.key.sign("blue", payload, claimed_sender=claimed_sender,
                                session_id=payload.get("session", ""))
            self.seen_envelopes.append(env)
        else:
            env = None
        self.room.post(self.name, "blue", text, env)
        events.emit("room_out", "red", text=text[:200], signed=signed,
                    claimed=claimed_sender or ("replay" if replay else "red"))
        await self.deliver()   # Blue answers each message before the next one

    async def deliver(self) -> None:
        """Let Blue process everything Red just put in the room."""
        for m in self.room.inbox("blue"):
            await self.blue.handle(m)
