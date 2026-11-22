"""Agent-to-agent message signing (Ed25519).

Every message an agent posts into the BAND room carries a signed envelope.
Each agent holds its own private key; only the public half is registered with
Aegis (bring-your-own-key), so Aegis can verify but never sign on an agent's
behalf. The canonical bytes match Aegis's Mandala verifier exactly: sorted
keys, compact separators, UTF-8.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(env: dict) -> bytes:
    body = {k: env[k] for k in (
        "sender_agent_id", "recipient_agent_id", "tenant_id", "key_id",
        "payload", "session_id", "nonce", "issued_at")}
    return json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


@dataclass
class AgentKey:
    agent_id: str
    private_key: Ed25519PrivateKey = field(default_factory=Ed25519PrivateKey.generate)
    key_id: str = ""  # assigned by Aegis when the public key is registered

    @property
    def public_key_hex(self) -> str:
        raw = self.private_key.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        return raw.hex()

    def sign(self, recipient: str, payload: dict, *, tenant_id: str = "demo",
             session_id: str = "", claimed_sender: str | None = None,
             nonce: str | None = None, issued_at: str | None = None) -> dict:
        """Build and sign an envelope.

        `claimed_sender` lets the Red agent *lie* about who it is (the spoofing
        attack): the signature is still made with Red's own key, which is
        exactly what the verifier catches (KEY_AGENT_MISMATCH).
        """
        env = {
            "sender_agent_id": claimed_sender or self.agent_id,
            "recipient_agent_id": recipient,
            "tenant_id": tenant_id,
            "key_id": self.key_id,
            "payload": payload,
            "session_id": session_id,
            "nonce": nonce or uuid.uuid4().hex,
            "issued_at": issued_at or _now_iso(),
        }
        sig = self.private_key.sign(canonical_bytes(env)).hex()
        return {"envelope": env, "signature_hex": sig}
