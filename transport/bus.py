"""Transport: the BAND room, or an in-process stand-in with the same rules.

BAND rules we keep in both modes: every message @mentions at least one
participant, nobody mentions themselves, and agents only see the room they
are in. A signed envelope rides inside the message text after a marker, so
the human principal watching the BAND room sees readable text and the
machine-checkable envelope together.

Who sent a message is decided by the TRANSPORT (BAND's authenticated
sender_id / sender_type), never by what the message says about itself. That
is what lets Blue tell the human principal apart from an agent that types
"this is the admin speaking".
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

MARK = "```aegis-envelope"
_ENV_RE = re.compile(r"```aegis-envelope\s*(\{.*?\})\s*```", re.S)


@dataclass
class Msg:
    sender: str            # display name / handle, as authenticated by the transport
    sender_kind: str       # "agent" | "principal"
    text: str
    envelope: Optional[dict] = None
    id: str = ""


def pack(text: str, envelope: Optional[dict]) -> str:
    if not envelope:
        return text
    return f"{text}\n{MARK}\n{json.dumps(envelope, separators=(',', ':'))}\n```"


def unpack(content: str) -> tuple[str, Optional[dict]]:
    m = _ENV_RE.search(content or "")
    if not m:
        return content, None
    try:
        env = json.loads(m.group(1))
    except json.JSONDecodeError:
        env = None
    return content[:m.start()].strip(), env


class LocalRoom:
    """In-process room. Used by tests and the offline demo."""

    def __init__(self, members: List[str], principal: str = "principal") -> None:
        self.members = set(members) | {principal}
        self.principal = principal
        self.log: List[Msg] = []
        self._cursor: Dict[str, int] = {}
        self.mode = "local"

    def post(self, sender: str, to: str, text: str, envelope: Optional[dict] = None,
             sender_kind: str = "agent") -> Msg:
        if to == sender:
            raise ValueError("BAND rule: no self-mention")
        if to not in self.members:
            raise ValueError(f"@{to} is not in the room")
        m = Msg(sender, sender_kind, f"@{to} {pack(text, envelope)}", envelope,
                id=str(len(self.log) + 1))
        m.to = to  # type: ignore[attr-defined]
        self.log.append(m)
        return m

    def inbox(self, me: str) -> List[Msg]:
        start = self._cursor.get(me, 0)
        out = [m for m in self.log[start:] if getattr(m, "to", None) == me]
        self._cursor[me] = len(self.log)
        return out

    def add_participant(self, by: str, who: str) -> dict:
        self.members.add(who)
        return {"added": who, "by": by}


class BandRoom:
    """The real BAND room via band-sdk's REST client.

    Env: BAND_CHAT_ID, and per agent BAND_KEY_<NAME> (e.g. BAND_KEY_BLUE).
    BAND_PRINCIPAL_ID = the human owner's user id (messages from it are the
    principal channel).
    """

    def __init__(self, agents: List[str]) -> None:
        from band_rest import RestClient
        self.mode = "band"
        self.chat_id = os.environ["BAND_CHAT_ID"]
        self.principal_id = os.environ.get("BAND_PRINCIPAL_ID", "")
        self.clients: Dict[str, object] = {}
        self.ident: Dict[str, dict] = {}
        self._seen: set = set()       # message ids already handed to an agent
        for name in agents:
            key = os.environ.get(f"BAND_KEY_{name.upper()}")
            if not key:
                continue
            c = RestClient(api_key=key, base_url=os.environ.get("BAND_BASE_URL"))  \
                if os.environ.get("BAND_BASE_URL") else RestClient(api_key=key)
            me = c.agent_api_identity.get_agent_me().data
            self.clients[name] = c
            self.ident[name] = {"id": me.id, "handle": me.handle, "name": me.name}

    def _mention(self, to: str) -> dict:
        if to in self.ident:
            return self.ident[to]
        return {"id": self.principal_id, "name": to, "handle": to}

    def post(self, sender: str, to: str, text: str, envelope: Optional[dict] = None,
             sender_kind: str = "agent") -> Msg:
        from band_rest import ChatMessageRequest, ChatMessageRequestMentionsItem
        mt = self._mention(to)
        content = f"@{mt['handle']} {pack(text, envelope)}"
        self.clients[sender].agent_api_messages.create_agent_chat_message(
            self.chat_id,
            message=ChatMessageRequest(content=content, mentions=[
                ChatMessageRequestMentionsItem(id=mt["id"], handle=mt["handle"], name=mt["name"])]),
        )
        return Msg(sender, sender_kind, content, envelope)

    def inbox(self, me: str) -> List[Msg]:
        c = self.clients[me]
        resp = c.agent_api_messages.list_agent_messages(self.chat_id)
        out: List[Msg] = []
        by_id = {v["id"]: k for k, v in self.ident.items()}
        for m in resp.data:
            if (me, m.id) in self._seen:
                continue
            self._seen.add((me, m.id))
            text, env = unpack(m.content)
            is_principal = (m.sender_type or "").lower() == "user" and (
                not self.principal_id or m.sender_id == self.principal_id)
            sender = by_id.get(m.sender_id, m.sender_name or m.sender_id)
            out.append(Msg(sender, "principal" if is_principal else "agent", text, env, id=m.id))
            for mark in ("mark_agent_message_processing", "mark_agent_message_processed"):
                try:
                    getattr(c.agent_api_messages, mark)(self.chat_id, m.id)
                except Exception as e:
                    self.mark_errors = getattr(self, "mark_errors", 0) + 1
                    self.last_mark_error = str(e)[:200]
        return out

    def add_participant(self, by: str, who_id: str) -> dict:
        from band_rest import ParticipantRequest
        r = self.clients[by].agent_api_participants.add_agent_chat_participant(
            self.chat_id, participant=ParticipantRequest(participant_id=who_id))
        return {"added": who_id, "by": by, "raw": str(r)[:200]}
