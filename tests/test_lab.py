import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from src.lab.controller import Lab
from src.lab.models import RuleError
from src.lab.hooks import AuditTrail
from src.lab.cli import evaluate

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.lab = Lab()

    def proposal(self):
        return self.lab.request({"order_id": "DEMO-101", "intent": "refund"})["id"]

    def approved(self):
        key = self.proposal()
        self.lab.decide(key, "approve", "human_reviewer")
        return key

    def test_scenarios(self):
        self.assertTrue(evaluate()["passed"])

    def test_unknown_and_foreign_are_indistinguishable(self):
        results = [self.lab.request({"order_id": x, "intent": "lookup"}) for x in ("DEMO-104", "DEMO-999")]
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[0]["reason"], "ORDER_UNAVAILABLE")

    def test_invalid_requests(self):
        for body in ([], {}, {"order_id": 2, "intent": "refund"},
                     {"order_id": "DEMO-101", "intent": "refund", "amount": 1}):
            with self.subTest(body=body):
                self.assertEqual(self.lab.request(body)["reason"], "INVALID_REQUEST")

    def test_tool_allowlist(self):
        self.assertEqual(self.lab.request({"order_id": "DEMO-101", "intent": "export_customers"})["reason"], "TOOL_NOT_ALLOWED")

    def test_lookup_does_not_propose(self):
        self.lab.request({"order_id": "DEMO-101", "intent": "lookup"})
        self.assertEqual(len(self.lab.proposals), 0)

    def test_identical_proposal_reused(self):
        self.assertEqual(self.proposal(), self.proposal())

    def test_execute_requires_approval(self):
        with self.assertRaisesRegex(RuleError, "APPROVAL_REQUIRED"):
            self.lab.execute(self.proposal())
        self.assertFalse(self.lab.receipts)

    def test_reviewer_role_required(self):
        with self.assertRaisesRegex(RuleError, "REVIEWER_REQUIRED"):
            self.lab.decide(self.proposal(), "approve", "planner")

    def test_rejection_blocks_execution(self):
        key = self.proposal()
        self.lab.decide(key, "reject", "human_reviewer")
        with self.assertRaisesRegex(RuleError, "APPROVAL_REQUIRED"):
            self.lab.execute(key)

    def test_repeated_decision_rejected(self):
        key = self.approved()
        with self.assertRaisesRegex(RuleError, "INVALID_TRANSITION"):
            self.lab.decide(key, "approve", "human_reviewer")

    def test_invalid_decision(self):
        with self.assertRaisesRegex(RuleError, "INVALID_DECISION"):
            self.lab.decide(self.proposal(), "maybe", "human_reviewer")

    def test_missing_proposal(self):
        with self.assertRaisesRegex(RuleError, "PROPOSAL_UNAVAILABLE"):
            self.lab.execute("missing")

    def test_simulated_receipt(self):
        result = self.lab.execute(self.approved())
        self.assertFalse(result["real_effect"])
        self.assertEqual(result["amount"], 85)
        self.assertEqual(result["status"], "SIMULATED")

    def test_concurrent_retry_exactly_one_local_receipt(self):
        key = self.approved()
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: self.lab.execute(key), range(20)))
        self.assertTrue(all(r == results[0] for r in results))
        self.assertEqual(len(self.lab.receipts), 1)

    def test_connector_failure_keeps_approval_and_retry_works(self):
        key = self.approved()
        with self.assertRaisesRegex(RuleError, "SIMULATED_CONNECTOR_FAILURE"):
            self.lab.execute(key, True)
        self.assertFalse(self.lab.receipts)
        self.assertEqual(self.lab.proposals[key].status, "APPROVED")
        self.assertEqual(self.lab.execute(key)["status"], "SIMULATED")

    def test_stale_policy(self):
        key = self.approved()
        self.lab.policy["max_refund"] = 101
        with self.assertRaisesRegex(RuleError, "STALE_PROPOSAL"):
            self.lab.execute(key)

    def test_stale_order_even_without_version_change(self):
        key = self.approved()
        self.lab.orders["DEMO-101"]["amount"] = 84
        with self.assertRaisesRegex(RuleError, "STALE_PROPOSAL"):
            self.lab.execute(key)

    def test_same_order_cannot_be_compensated_twice(self):
        self.lab.execute(self.approved())
        self.lab.policy["version"] = "next-policy"
        self.assertEqual(self.lab.request({"order_id": "DEMO-101", "intent": "refund"})["reason"], "ALREADY_COMPENSATED")

    def test_before_hook_failure_prevents_action(self):
        key = self.approved()
        with patch.object(self.lab.audit, "append", side_effect=RuntimeError("hook unavailable")):
            with self.assertRaises(RuntimeError):
                self.lab.execute(key)
        self.assertFalse(self.lab.receipts)

    def test_audit_detects_edit(self):
        self.lab.execute(self.approved())
        events = self.lab.snapshot()["events"]
        self.assertTrue(AuditTrail.verify(events))
        events[0]["outcome"] = "altered"
        self.assertFalse(AuditTrail.verify(events))

    def test_snapshot_is_a_copy(self):
        self.proposal()
        state = self.lab.snapshot()
        state["events"].clear()
        state["proposals"][0]["status"] = "APPROVED"
        self.assertTrue(self.lab.audit.events)
        self.assertEqual(next(iter(self.lab.proposals.values())).status, "PENDING_APPROVAL")

class ExplainResetTests(unittest.TestCase):
    """U11: per-condition explanation (R29) and explicit session reset (R28)."""
    def setUp(self):
        self.lab = Lab()

    def failed(self, amount, days, status="delivered"):
        result = self.lab.explain({"amount": amount, "days_since_delivery": days, "status": status})
        self.assertEqual([c["rule"] for c in result["conditions"]], ["NOT_DELIVERED", "OUTSIDE_WINDOW", "ABOVE_LIMIT"])
        return result, [c["rule"] for c in result["conditions"] if not c["ok"]]

    def test_explain_reports_both_failures_at_once(self):
        result, failed = self.failed(180, 20)
        self.assertEqual(failed, ["OUTSIDE_WINDOW", "ABOVE_LIMIT"])
        self.assertFalse(result["eligible"])
        self.assertEqual(result["conditions"][1], {"rule": "OUTSIDE_WINDOW", "ok": False, "observed": 20, "limit": 14})
        self.assertEqual(result["conditions"][2], {"rule": "ABOVE_LIMIT", "ok": False, "observed": 180, "limit": 100})
        self.assertEqual((result["status"], result["policy_version"], result["real_effect"]), ("EXPLAINED", "demo-policy-1", False))

    def test_explain_ten_days_leaves_only_amount(self):
        self.assertEqual(self.failed(180, 10)[1], ["ABOVE_LIMIT"])

    def test_explain_eligible_request(self):
        result, failed = self.failed(50, 5)
        self.assertEqual(failed, [])
        self.assertTrue(result["eligible"])

    def test_explain_not_delivered_status(self):
        result, failed = self.failed(50, 5, "in_transit")
        self.assertEqual(failed, ["NOT_DELIVERED"])
        self.assertEqual(result["conditions"][0], {"rule": "NOT_DELIVERED", "ok": False, "observed": "in_transit", "limit": "delivered"})

    def test_explain_accepts_every_fixture_status(self):
        # U12: one vocabulary; every status in the order fixtures can be explained, the retired "shipped" cannot.
        for status in {o["status"] for o in self.lab.orders.values()}:
            with self.subTest(status=status):
                self.assertEqual(self.failed(50, 5, status)[1], [] if status == "delivered" else ["NOT_DELIVERED"])
        with self.assertRaisesRegex(RuleError, "INVALID_REQUEST"):
            self.lab.explain({"amount": 50, "days_since_delivery": 5, "status": "shipped"})

    def test_explain_thresholds_come_from_policy(self):
        self.lab.policy["max_refund"] = 200
        self.assertEqual(self.failed(180, 20)[1], ["OUTSIDE_WINDOW"])

    def test_explain_rejects_invalid_input(self):
        valid = {"amount": 50, "days_since_delivery": 5, "status": "delivered"}
        for body in ([], {}, dict(valid, amount="50"), dict(valid, amount=-1), dict(valid, days_since_delivery=100001),
                     dict(valid, amount=True), dict(valid, days_since_delivery=5.0), dict(valid, status="shipped"),
                     dict(valid, status=1), dict(valid, order_id="DEMO-101"), {"amount": 50, "status": "delivered"}):
            with self.subTest(body=body), self.assertRaisesRegex(RuleError, "INVALID_REQUEST"):
                self.lab.explain(body)

    def test_explain_creates_no_proposal_receipt_or_event(self):
        self.lab.request({"order_id": "DEMO-101", "intent": "refund"})
        before = self.lab.snapshot()
        self.failed(50, 5)
        with self.assertRaises(RuleError):
            self.lab.explain({})
        self.assertEqual(self.lab.snapshot(), before)

    def test_reset_after_full_flow_empties_session(self):
        key = self.lab.request({"order_id": "DEMO-101", "intent": "refund"})["id"]
        self.lab.decide(key, "approve", "human_reviewer")
        self.lab.execute(key)
        state = self.lab.reset()
        self.assertEqual((state["proposals"], state["receipts"], state["events"]), ([], [], []))
        self.assertTrue(state["audit_chain_valid"])
        self.assertEqual(state, self.lab.snapshot())

    def test_request_after_reset_creates_new_proposal(self):
        key = self.lab.request({"order_id": "DEMO-101", "intent": "refund"})["id"]
        self.lab.decide(key, "approve", "human_reviewer")
        self.lab.execute(key)
        self.lab.reset()
        result = self.lab.request({"order_id": "DEMO-101", "intent": "refund"})
        self.assertEqual(result["status"], "PENDING_APPROVAL")
        self.assertEqual(self.lab.snapshot()["events"][0]["sequence"], 1)
