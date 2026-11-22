"""End to end against a running Aegis (skipped when none is reachable)."""
import asyncio
import os

import httpx
import pytest

BASE = os.environ.get("AEGIS_BASE_URL", "http://localhost:8000")


def _up() -> bool:
    try:
        return httpx.get(f"{BASE}/api/health", timeout=3).status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _up(), reason="no Aegis reachable")


def test_story_and_measure():
    from dotenv import load_dotenv
    load_dotenv()
    import run_demo

    class A:
        band = False
        story_only = False

    s = asyncio.run(run_demo.main(A))
    m = s["measured"]
    assert m["attacks_stopped"] == m["attacks"]
    assert m["benign_blocked"] == 0
    assert s["rekha_after"].get("forbid_paths") == ["internal"]
    # the hidden arm behind the flat HOLD is the closure arm
    rec = next(r for r in m["rows"] if r["playbook"] == "recruit after probe")
    assert rec["shown_to_red"][-1] == "HOLD" and rec["arms"][-1] == "closure"
