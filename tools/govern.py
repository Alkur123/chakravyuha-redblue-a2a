"""Ask Aegis before you act. Used by the AdaL skill (and any agent).

    python -m tools.govern begin "<goal>" --tools file.read,file.edit
    python -m tools.govern check <session_id> <tool> '<json args>' [--class WRITE]

`check` prints one JSON line and exits 0 on ALLOW, 3 on WARN, 4 on DENY/KILL,
5 if Aegis could not be reached (fail-closed: do not act).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

from aegis import AegisClient


def _client() -> AegisClient:
    return AegisClient(base_url=os.environ.get("AEGIS_BASE_URL", "http://localhost:8000"),
                       api_key=os.environ.get("AEGIS_API_KEY"), timeout=20)


async def _begin(goal: str, tools: list[str], classes: list[str]) -> int:
    c = _client()
    s = await c.begin_session(goal, agent_id="adal", declared_tools=tools, declared_classes=classes)
    await c.egress.register(s.session_id, tools, classes)
    print(json.dumps({"session_id": s.session_id}))
    return 0


async def _check(sid: str, tool: str, args: dict, cls: str) -> int:
    c = _client()
    step = {"index": int(os.environ.get("AEGIS_STEP", "1")), "thought": "",
            "action": {"type": "tool_call", "name": tool, "args": args, "class": cls},
            "observation": ""}
    d = await c.evaluate(sid, step)
    e = await c.egress.check(sid, tool, cls)
    verdict = "KILL" if d.killed else ("DENY" if e.get("action") != "ALLOW" else
                                       ("WARN" if d.warned else "ALLOW"))
    print(json.dumps({"verdict": verdict, "r12": d.decision, "hard_block": d.hard_block,
                      "r13": e.get("action"), "reason": d.reason or e.get("reason")}))
    return {"ALLOW": 0, "WARN": 3}.get(verdict, 4)


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("begin"); b.add_argument("goal"); b.add_argument("--tools", required=True)
    b.add_argument("--classes", default="READ,WRITE")
    k = sub.add_parser("check"); k.add_argument("session"); k.add_argument("tool")
    k.add_argument("args", nargs="?", default="{}"); k.add_argument("--class", dest="cls", default="READ")
    a = p.parse_args()
    try:
        if a.cmd == "begin":
            return asyncio.run(_begin(a.goal, a.tools.split(","), a.classes.split(",")))
        return asyncio.run(_check(a.session, a.tool, json.loads(a.args), a.cls))
    except Exception as e:
        print(json.dumps({"verdict": "UNAVAILABLE", "error": str(e)[:200]}))
        return 5


if __name__ == "__main__":
    sys.exit(main())
