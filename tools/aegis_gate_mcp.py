"""The Aegis action gate as an MCP server (stdio), for AdaL or any MCP client.

An agent with no shell still has to ask before it acts. This server gives it
one tool, `aegis_check_action`, that asks the real Aegis gate (Ring 12
trajectory + Ring 13 egress) and returns ALLOW / WARN / DENY / KILL. The
verdict comes from Aegis, not from text in the prompt, so the agent can trust
it where it could not trust a pasted "grant".

Register with AdaL (per project):  /mcp add aegis-gate --command <python> --args "-m,tools.aegis_gate_mcp"
"""
from __future__ import annotations

import os
from typing import Optional

from aegis import AegisClient
from mcp.server.fastmcp import FastMCP

GOAL = os.environ.get("AEGIS_GATE_GOAL", "patch the path traversal in target/app.py")
TOOLS = os.environ.get("AEGIS_GATE_TOOLS", "file.read,file.edit").split(",")
CLASSES = os.environ.get("AEGIS_GATE_CLASSES", "READ,WRITE").split(",")

mcp = FastMCP("aegis-gate")
_state = {"session": None, "step": 0}


def _client() -> AegisClient:
    return AegisClient(base_url=os.environ.get("AEGIS_BASE_URL", "http://localhost:8000"),
                       api_key=os.environ.get("AEGIS_API_KEY"), timeout=20)


@mcp.tool(name="aegis_check_action",
          description="Ask the Aegis gate before ANY file read, file edit, command or network call. "
                      "Returns verdict ALLOW, WARN, DENY or KILL. Act only on ALLOW.")
async def aegis_check_action(tool: str, path: Optional[str] = None, action_class: str = "READ") -> dict:
    c = _client()
    if _state["session"] is None:
        s = await c.begin_session(GOAL, agent_id="adal", declared_tools=TOOLS, declared_classes=CLASSES,
                                  rekha={"forbid_paths": ["internal", ".env"]})
        await c.egress.register(s.session_id, TOOLS, CLASSES)
        _state["session"] = s.session_id
    _state["step"] += 1
    args = {"path": path} if path else {}
    step = {"index": _state["step"], "thought": "", "observation": "",
            "action": {"type": "tool_call", "name": tool, "args": args, "class": action_class.upper()}}
    d = await c.evaluate(_state["session"], step)
    e = await c.egress.check(_state["session"], tool, action_class.upper())
    verdict = "KILL" if d.killed else ("DENY" if e.get("action") != "ALLOW" else ("WARN" if d.warned else "ALLOW"))
    return {"verdict": verdict, "session": _state["session"], "hard_block": d.hard_block,
            "reason": d.reason or e.get("reason")}


if __name__ == "__main__":
    mcp.run("stdio")
