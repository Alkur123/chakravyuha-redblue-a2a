"""Deploy to Agent37: an Aegis API instance, then the war room pointed at it.

    python -m tools.agent37_deploy aegis   (fresh demo secrets; MONGO_URL_DEMO from .env)
    python -m tools.agent37_deploy warroom <aegis https url>

Secrets are read from env files at run time and sent only to Agent37's
instance API (write-only env). Nothing secret is written to this repo.
"""
from __future__ import annotations

import json
import os
import secrets
import sys

import httpx
from dotenv import dotenv_values

API = "https://api.agent37.com/v1"
HERE = dotenv_values(".env")


def _post(path: str, body: dict) -> dict:
    r = httpx.post(f"{API}{path}", json=body, timeout=600,
                   headers={"Authorization": f"Bearer {HERE['AGENT37_API_KEY']}"})
    if r.status_code >= 300:
        raise SystemExit(f"{r.status_code}: {r.text[:600]}")
    return r.json()


def aegis(_unused: str = "") -> None:
    """Fresh, demo-only secrets: nothing is reused from any other Aegis deployment.
    The one input is MONGO_URL_DEMO in this repo's .env (set it yourself; use a
    database user that can reach only a demo database). Without it, Aegis boots
    degraded: gating works, the audit vault reports itself unavailable."""
    api_key = secrets.token_urlsafe(32)
    admin_key = secrets.token_urlsafe(32)
    env = {
        "MONGO_URL": HERE.get("MONGO_URL_DEMO") or "mongodb://unset.invalid:27017",
        "AUDIT_SIGNING_KEY": secrets.token_hex(32), "CONCH_PEPPER": secrets.token_hex(32),
        "API_KEY_PEPPER": secrets.token_hex(32), "ASTRA_SIGNING_KEY": secrets.token_hex(32),
        "ADMIN_API_KEY": admin_key, "API_KEY": api_key, "DB_NAME": "hackathon_demo",
        "OPENAI_API_KEY": "", "R12_FAIL_CLOSED": "true", "R12_THRESHOLD_JITTER": "0",
        "RATE_LIMIT": "2000/minute", "CHEAP_RATE_LIMIT": "2000/minute",
        "EXPENSIVE_RATE_LIMIT": "120/minute", "CORS_ORIGINS": "http://localhost:5173",
        "AUDIT_ANCHOR_PATH": "/tmp/audit_anchors_hackathon.jsonl", "GUNICORN_WORKERS": "1",
    }
    inst = _post("/instances", {"template": "aegis-api", "name": "aegis-api", "env": env,
                                "auto_sleep": False,
                                "public_ports": [{"port": 8000, "prefix": "aegis", "label": "Aegis API"}]})
    url = next((p.get("url") for p in inst.get("public_ports", []) if p.get("url")), None) \
        or f"https://aegis-{inst['id']}.agent37.app"
    with open(".env", "a") as f:     # local .env is gitignored
        f.write(f"AEGIS_HOSTED_URL={url}\nAEGIS_HOSTED_API_KEY={api_key}\n"
                f"AEGIS_HOSTED_ADMIN_KEY={admin_key}\n")
    print(json.dumps({"id": inst.get("id"), "status": inst.get("status"), "url": url}))


def warroom(aegis_url: str) -> None:
    keep = ("BAND_CHAT_ID", "BAND_KEY_BLUE", "BAND_KEY_RED", "BAND_PRINCIPAL_ID",
            "LYZR_API_KEY", "LYZR_AGENT_ID", "LYZR_USER_ID")
    env = {k: HERE[k] for k in keep if HERE.get(k)}
    env.update({"AEGIS_BASE_URL": aegis_url, "AEGIS_API_KEY": HERE["AEGIS_HOSTED_API_KEY"],
                "AEGIS_ADMIN_KEY": HERE["AEGIS_HOSTED_ADMIN_KEY"],
                "WARROOM_BAND": "1", "PORT": "8080"})
    inst = _post("/instances", {"template": "chakravyuha-warroom", "name": "chakravyuha-warroom",
                                "env": env, "auto_sleep": False,
                                "public_ports": [{"port": 8080, "prefix": "warroom", "label": "War room"}]})
    url = next((p.get("url") for p in inst.get("public_ports", []) if p.get("url")), None) \
        or f"https://warroom-{inst['id']}.agent37.app"
    with open(".env", "a") as f:
        f.write(f"WARROOM_URL={url}\n")
    print(json.dumps({"id": inst.get("id"), "status": inst.get("status"), "url": url}))


if __name__ == "__main__":
    {"aegis": aegis, "warroom": warroom}[sys.argv[1]](*(sys.argv[2:3] or [""]))
