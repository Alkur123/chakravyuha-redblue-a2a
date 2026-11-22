"""Lyzr: Blue's remediation analyst, and an extra Responsible-AI stop.

Two uses, both optional (unset env = skipped and logged, never faked):
  * remediation(finding): a hosted Lyzr agent writes the fix advice.
  * injection_check(text): Lyzr's prompt-injection check. It can only ADD a
    stop at the gate; it can never lift one. A language-model check can be
    talked down (our D9 study measured a fake "system notice" raising an LLM
    monitor's misses from 1.2% to 19.7%), so it never holds a veto alone.

Responses are cached on disk so a rehearsal does not spend the free credits.
Env: LYZR_API_KEY, LYZR_AGENT_ID, LYZR_USER_ID (your Lyzr login email).
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Optional, Tuple

import httpx

from formation import events

CHAT_URL = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"
RAI_URL = os.environ.get("LYZR_RAI_URL", "")
CACHE = Path(".cache/lyzr.json")


class Lyzr:
    def __init__(self, api_key: str, agent_id: str, user_id: str) -> None:
        self.api_key, self.agent_id, self.user_id = api_key, agent_id, user_id
        self._cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

    @classmethod
    def from_env(cls) -> Optional["Lyzr"]:
        k, a = os.environ.get("LYZR_API_KEY"), os.environ.get("LYZR_AGENT_ID")
        if not (k and a):
            events.emit("sponsor", "lyzr", status="not configured (skipped)")
            return None
        return cls(k, a, os.environ.get("LYZR_USER_ID", "blue-agent"))

    def _save(self) -> None:
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(self._cache, indent=1))

    async def _chat(self, message: str, session: str) -> str:
        h = hashlib.sha256(message.encode()).hexdigest()[:16]
        if h in self._cache:
            return self._cache[h]
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(CHAT_URL, headers={"x-api-key": self.api_key},
                             json={"user_id": self.user_id, "agent_id": self.agent_id,
                                   "session_id": session, "message": message})
            r.raise_for_status()
            body = r.json()
        text = body.get("response") or body.get("message") or json.dumps(body)[:800]
        self._cache[h] = text
        self._save()
        return text

    async def remediation(self, finding: dict) -> Optional[str]:
        prompt = ("You are a security engineer. A red-team agent reported this finding "
                  "against our invoice service. Give a 3-line fix: code change, policy "
                  f"rule, and a test.\nFinding: {json.dumps(finding)[:1200]}")
        try:
            t = await self._chat(prompt, "blue-remediation")
            events.emit("sponsor", "lyzr", status="remediation", text=t[:300])
            return t
        except Exception as e:
            events.emit("sponsor", "lyzr", status="error", error=str(e)[:200])
            return None

    async def injection_check(self, text: str) -> Tuple[bool, str]:
        if not RAI_URL:
            return False, "rai not configured"
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(RAI_URL, headers={"x-api-key": self.api_key}, json={"text": text[:4000]})
                body = r.json()
            flagged = bool(body.get("is_injection") or body.get("flagged") or body.get("detected"))
            events.emit("sponsor", "lyzr", status="rai", flagged=flagged)
            return flagged, json.dumps(body)[:160]
        except Exception as e:
            events.emit("sponsor", "lyzr", status="rai_error", error=str(e)[:200])
            return False, "rai unavailable"  # additive arm: its absence never blocks or passes alone
