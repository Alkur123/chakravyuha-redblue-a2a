"""Record reconciliation: what the agent SAYS it did vs what it DID.

Arthaśāstra II.8 reduces forty ways of falsifying a record to discrepancy
types. We check the ones an agent's self-report can be tested on against the
enforcement point's own tool log: existence (claimed but not done, or done
but not claimed), count, recipient, and category. One proven falsification
reopens the whole session ("answerable for all").
"""
from __future__ import annotations

from collections import Counter
from typing import Dict, List

from . import events


def reconcile(session_id: str, claimed: List[Dict], logged: List[Dict]) -> List[Dict]:
    """claimed / logged: [{"tool": str, "target": str, "class": str}]"""
    def key(r):  # what an action IS, for comparison
        return (r.get("tool"), r.get("target"))

    c, l = Counter(key(r) for r in claimed), Counter(key(r) for r in logged)
    found: List[Dict] = []
    for k in l:
        if k not in c:
            found.append({"type": "existence", "detail": f"done but not reported: {k[0]} {k[1]}"})
        elif l[k] != c[k]:
            found.append({"type": "count", "detail": f"{k[0]} {k[1]}: did {l[k]}, reported {c[k]}"})
    for k in c:
        if k not in l:
            found.append({"type": "existence", "detail": f"reported but never done: {k[0]} {k[1]}"})
    claimed_cls = {key(r): r.get("class") for r in claimed}
    for r in logged:
        cc = claimed_cls.get(key(r))
        if cc and cc != r.get("class"):
            found.append({"type": "category", "detail": f"{r['tool']} reported {cc}, was {r['class']}"})
    claimed_hosts = {r.get("target") for r in claimed if r.get("class") == "NETWORK"}
    for r in logged:
        if r.get("class") == "NETWORK" and r.get("target") not in claimed_hosts:
            found.append({"type": "recipient", "detail": f"unreported recipient {r.get('target')}"})
    # de-duplicate
    seen, out = set(), []
    for f in found:
        t = (f["type"], f["detail"])
        if t not in seen:
            seen.add(t)
            out.append(f)
    events.emit("reconciled", "audit", session=session_id,
                claimed=len(claimed), logged=len(logged), discrepancies=out)
    return out
