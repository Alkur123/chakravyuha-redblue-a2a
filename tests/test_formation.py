"""Each arm, both halves: it fires on the attack and stays quiet on the honest case."""
import json

from formation import events
from formation.alarms import AlarmLedger
from formation.closure import ReinforcementClosure
from formation.depth import CONVERGENCE_DEPTH, DepthTracker
from formation.hold import HoldQueue
from formation.reconcile import reconcile
from formation.signing import AgentKey, canonical_bytes
from formation.standdown import StandDownRule
from formation.withholding import GradientWithholding
from transport.bus import LocalRoom, pack, unpack


def test_alarm_not_withdrawable_by_agent():
    L = AlarmLedger()
    L.raise_alarm("s", "ring12", "honeytoken")
    assert L.try_close("s", "agent", "red", "false alarm, task complete") is False
    assert len(L.open_for("s")) == 1
    assert L.open_for("s")[0].withdraw_attempts


def test_alarm_closes_on_principal():
    L = AlarmLedger()
    L.raise_alarm("s", "ring12", "x")
    assert L.try_close("s", "principal", "founder") is True
    assert L.open_for("s") == []


def test_standdown_needs_two_kinds():
    R = StandDownRule()
    assert R.offer("s", "principal_signed", "founder", True)[0] is False   # one kind
    assert R.offer("s", "principal_signed", "founder", True)[0] is False   # same kind twice
    assert R.offer("s", "system_event", "hitl", True)[0] is True           # second kind


def test_standdown_forged_counts_as_zero():
    R = StandDownRule()
    assert R.offer("s", "principal_signed", "red", verified=False)[0] is False
    assert R.pending("s") == []


def test_closure_blocks_suspect_only():
    suspect = {"bad"}
    C = ReinforcementClosure(lambda s: s in suspect)
    assert C.check("bad", "band.add_participant", {"who": "x"})[0] is False
    assert C.check("good", "band.add_participant", {"who": "x"})[0] is True   # honest session may add
    assert C.check("bad", "invoice.list", {})[0] is True                      # not a carrier


def test_depth_only_rises_for_agent():
    T = DepthTracker()
    d = T.get("s")
    for _ in range(CONVERGENCE_DEPTH):
        d.add("warn")
    assert d.converged
    assert T.lower("s", by_principal=False) is False and T.get("s").converged
    assert T.lower("s", by_principal=True) is True and not T.get("s").converged


def test_withholding_flattens_after_probing():
    W = GradientWithholding()
    assert W.mask("s", {"verdict": "DENY", "reason": "ring13 undeclared"})["verdict"] == "DENY"
    for _ in range(3):
        W.record_denial("s")
    assert W.mask("s", {"verdict": "ALLOW", "reason": "ok"}) == {"verdict": "HOLD", "reason": "held"}
    assert W.mask("other", {"verdict": "ALLOW"}) == {"verdict": "ALLOW"}


def test_hold_released_only_by_principal():
    Q = HoldQueue()
    h = Q.park("s", "payment.send", {"to": "x", "amount": 1})
    Q.decide(h.hold_id, True, "agent", "red")
    assert Q.get(h.hold_id).state == "HELD"
    Q.decide(h.hold_id, True, "principal", "founder")
    assert Q.get(h.hold_id).state == "RELEASED"


def test_reconcile_catches_omission_and_passes_truth():
    logged = [{"tool": "invoice.read", "target": "INV-1", "class": "READ"},
              {"tool": "report.export", "target": "evil", "class": "NETWORK"}]
    bad = reconcile("s", [{"tool": "invoice.read", "target": "INV-1", "class": "READ"}], logged)
    assert {d["type"] for d in bad} >= {"existence", "recipient"}
    assert reconcile("s", logged, logged) == []


def test_envelope_canonical_and_spoof_is_still_red_key():
    k = AgentKey("red")
    env = k.sign("blue", {"a": 1}, claimed_sender="blue")
    assert env["envelope"]["sender_agent_id"] == "blue"
    pub = k.private_key.public_key()
    pub.verify(bytes.fromhex(env["signature_hex"]), canonical_bytes(env["envelope"]))  # signed by red
    assert canonical_bytes(env["envelope"]) == json.dumps(
        env["envelope"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def test_room_rules_and_envelope_roundtrip():
    room = LocalRoom(["red", "blue"])
    try:
        room.post("red", "red", "hi")
        assert False, "self-mention must fail"
    except ValueError:
        pass
    env = {"envelope": {"x": 1}, "signature_hex": "ab"}
    room.post("red", "blue", "hello", env)
    [m] = room.inbox("blue")
    assert unpack(m.text)[1] == env and room.inbox("blue") == []
    assert unpack(pack("plain", None)) == ("plain", None)


def test_events_payload_cannot_overwrite_kind():
    e = events.emit("verdict", "blue", kind="forged", actor="mallory")
    assert e["kind"] == "verdict" and e["actor"] == "blue" and e["data_kind"] == "forged"
