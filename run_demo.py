"""Run the whole thing: the story, then the measured playbooks.

    python run_demo.py                 # local room, Aegis at AEGIS_BASE_URL
    python run_demo.py --band          # the real BAND room (needs BAND_* env)
    python run_demo.py --story-only

Writes runs/<stamp>/events.jsonl and runs/<stamp>/summary.json.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from aegis import AegisClient  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from agents.blue import Blue  # noqa: E402
from agents.playbooks import measure, story  # noqa: E402
from agents.red import Red  # noqa: E402
from formation import events  # noqa: E402
from sponsors.finch import Finch  # noqa: E402
from sponsors.lyzr import Lyzr  # noqa: E402
from transport.bus import BandRoom, LocalRoom  # noqa: E402


def make_target():
    url = os.environ.get("TARGET_URL")
    if url:
        import httpx
        http = httpx.Client(base_url=url, timeout=10)
    else:
        from target.app import app
        http = TestClient(app)

    def call(tool: str, args: dict) -> dict:
        if tool == "invoice.list":
            r = http.get("/invoices")
        elif tool == "invoice.read":
            r = http.get(f"/invoices/{args['id']}")
        elif tool == "file.read":
            r = http.get("/files", params={"path": args["path"]})
        elif tool == "report.export":
            r = http.post("/export", json=args)
        elif tool == "payment.send":
            r = http.post("/payments", json=args)
        else:
            return {"note": f"{tool} has no target endpoint"}
        try:
            return {"status": r.status_code, "body": r.json()}
        except Exception:
            return {"status": r.status_code, "body": r.text[:200]}
    return call


async def main(args) -> dict:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = Path("runs") / stamp
    events.set_log_path(out / "events.jsonl")

    aegis = AegisClient(base_url=os.environ.get("AEGIS_BASE_URL", "http://localhost:8000"),
                        api_key=os.environ.get("AEGIS_API_KEY"),
                        admin_key=os.environ.get("AEGIS_ADMIN_KEY"), timeout=30)
    room = BandRoom(["blue", "red"]) if args.band else LocalRoom(["blue", "red", "red-reserve"])
    lyzr = Lyzr.from_env()
    finch = Finch()
    blue = Blue(aegis, room, lyzr=lyzr, finch=finch)
    red = Red(blue, room, make_target())
    await blue.register()
    await blue.register_peer(red.key)
    events.emit("run_start", "director", room=room.mode, lyzr=bool(lyzr), stamp=stamp)
    ev = Path("evidence/adal_patch.json")
    if ev.exists():  # AdaL's governed patch: recorded evidence, shown as it was measured
        a = json.loads(ev.read_text(encoding="utf-8"))
        if a.get("accepted"):
            events.emit("sponsor", "adal", status="patch verified",
                        before=a["before"]["attack_status"], after=a["after"]["attack_status"],
                        honest=a["after"]["honest_status"], files=a.get("changed_files"))

    acts = await story(red, blue)
    summary = {"stamp": stamp, "room": room.mode, "acts": acts,
               "findings": blue.findings, "hardening": blue.hardening,
               "rekha_after": blue.rekha}
    if not args.story_only:
        summary["measured"] = await measure(red, blue)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "measured"}, indent=2, default=str)[:3000])
    if "measured" in summary:
        m = summary["measured"]
        print(f"\nattacks stopped {m['attacks_stopped']}/{m['attacks']}  "
              f"benign blocked {m['benign_blocked']}/{m['benign']}")
        for r in m["rows"]:
            print(f"  {r['kind']:6} {r['playbook']:22} {' '.join(r['verdicts']):30} {' '.join(r['arms'])}")
    print(f"\nrun written to {out}")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--band", action="store_true")
    p.add_argument("--story-only", action="store_true")
    asyncio.run(main(p.parse_args()))
