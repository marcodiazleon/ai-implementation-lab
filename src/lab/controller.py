"""Deterministic orchestration of a fictional shop. No LLM, network, money or email."""
from copy import deepcopy
from pathlib import Path
from threading import RLock
import json
from .models import Proposal, RuleError
from .hooks import AuditTrail, digest

ROOT = Path(__file__).resolve().parents[2]
# Same vocabulary as data/orders.json and scripts/validate_data.py (D25).
EXPLAIN_STATUSES = ("delivered", "in_transit", "returned", "cancelled")

def load_data(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))

class Lab:
    def __init__(self):
        self.orders = {row["id"]: row for row in load_data("orders.json")}
        self.policy = load_data("policy.json")
        self.proposals = {}
        self.receipts = {}
        self.audit = AuditTrail()
        self.lock = RLock()

    def _before(self, action):
        self.audit.append("before", action, "CHECKING")

    def _after(self, action, outcome, reference=""):
        self.audit.append("after", action, outcome, reference)

    def _order(self, order_id):
        order = self.orders.get(order_id)
        # Do not disclose whether a resource outside this workspace exists.
        if not order or order["workspace"] != "sample-store":
            raise RuleError("ORDER_UNAVAILABLE")
        return order

    def _eligible(self, order):
        if any(r["order_id"] == order["id"] for r in self.receipts.values()):
            raise RuleError("ALREADY_COMPENSATED")
        if order["status"] != "delivered":
            raise RuleError("NOT_DELIVERED")
        if order["days_since_delivery"] > self.policy["window_days"]:
            raise RuleError("OUTSIDE_WINDOW")
        if order["amount"] > self.policy["max_refund"]:
            raise RuleError("ABOVE_LIMIT")

    def request(self, body):
        with self.lock:
            self._before("request")
            try:
                if not isinstance(body, dict) or set(body) != {"order_id", "intent"}:
                    raise RuleError("INVALID_REQUEST")
                if not all(isinstance(value, str) for value in body.values()):
                    raise RuleError("INVALID_REQUEST")
                if body["intent"] not in {"lookup", "refund"}:
                    raise RuleError("TOOL_NOT_ALLOWED")
                order = self._order(body["order_id"])
                if body["intent"] == "lookup":
                    result = {"status": "READ_ONLY", "order": deepcopy(order)}
                else:
                    self._eligible(order)
                    # Repeated identical proposals do not create new execution identities.
                    key = digest({"order": order, "policy": self.policy})[:20]
                    if key not in self.proposals:
                        self.proposals[key] = Proposal(key, order["id"], order["amount"],
                                                       order["version"], digest(order), digest(self.policy))
                    result = self.proposals[key].as_dict()
                self._after("request", result["status"], order["id"])
                return result
            except RuleError as exc:
                self._after("request", exc.code)
                return {"status": "BLOCKED", "reason": exc.code}

    def decide(self, proposal_id, decision, actor):
        with self.lock:
            self._before("decision")
            try:
                if actor != "human_reviewer":
                    raise RuleError("REVIEWER_REQUIRED")
                if decision not in {"approve", "reject"}:
                    raise RuleError("INVALID_DECISION")
                proposal = self.proposals.get(proposal_id)
                if proposal is None:
                    raise RuleError("PROPOSAL_UNAVAILABLE")
                if proposal.status != "PENDING_APPROVAL":
                    raise RuleError("INVALID_TRANSITION")
                proposal.status = "APPROVED" if decision == "approve" else "REJECTED"
                self._after("decision", proposal.status, proposal.id)
                return proposal.as_dict()
            except RuleError as exc:
                self._after("decision", exc.code)
                raise

    def execute(self, proposal_id, fail_connector=False):
        with self.lock:
            self._before("execute")
            try:
                proposal = self.proposals.get(proposal_id)
                if proposal is None:
                    raise RuleError("PROPOSAL_UNAVAILABLE")
                if proposal_id in self.receipts:
                    self._after("execute", "REPLAY", proposal_id)
                    return deepcopy(self.receipts[proposal_id])
                if proposal.status != "APPROVED":
                    raise RuleError("APPROVAL_REQUIRED")
                order = self._order(proposal.order_id)
                if proposal.policy_digest != digest(self.policy) or proposal.order_version != order["version"] or proposal.order_digest != digest(order):
                    raise RuleError("STALE_PROPOSAL")
                self._eligible(order)
                if fail_connector:
                    raise RuleError("SIMULATED_CONNECTOR_FAILURE")
                # This is a local receipt only, never a financial operation.
                receipt = {"id": "SIM-" + proposal.id, "order_id": order["id"],
                           "amount": proposal.amount, "currency": "DEMO",
                           "status": "SIMULATED", "real_effect": False}
                self.receipts[proposal.id] = receipt
                proposal.status = "SIMULATED"
                self._after("execute", "SIMULATED", proposal.id)
                return deepcopy(receipt)
            except RuleError as exc:
                self._after("execute", exc.code)
                raise

    def reset(self):
        """Visitor-confirmed reset of the in-memory sample session (R28)."""
        with self.lock:
            self.proposals.clear()
            self.receipts.clear()
            self.audit = AuditTrail()
            return self.snapshot()

    def explain(self, body):
        """Pure query (R29): every condition with its own result; no proposal, receipt or event."""
        if not isinstance(body, dict) or set(body) != {"amount", "days_since_delivery", "status"}:
            raise RuleError("INVALID_REQUEST")
        if not all(type(body[k]) is int and 0 <= body[k] <= 100000 for k in ("amount", "days_since_delivery")):
            raise RuleError("INVALID_REQUEST")
        if body["status"] not in EXPLAIN_STATUSES:
            raise RuleError("INVALID_REQUEST")
        with self.lock:
            policy = deepcopy(self.policy)
        order = dict(body, id="CUSTOM", workspace="sample-store")
        # Same order and thresholds as _eligible, but every condition is evaluated.
        conditions = [
            {"rule": "NOT_DELIVERED", "ok": order["status"] == "delivered", "observed": order["status"], "limit": "delivered"},
            {"rule": "OUTSIDE_WINDOW", "ok": order["days_since_delivery"] <= policy["window_days"],
             "observed": order["days_since_delivery"], "limit": policy["window_days"]},
            {"rule": "ABOVE_LIMIT", "ok": order["amount"] <= policy["max_refund"], "observed": order["amount"], "limit": policy["max_refund"]}]
        return {"status": "EXPLAINED", "eligible": all(c["ok"] for c in conditions), "conditions": conditions,
                "policy_version": policy["version"], "real_effect": False}

    def snapshot(self):
        with self.lock:
            return deepcopy({"mode": "DETERMINISTIC_DEMO", "model_calls": 0,
                "external_requests": 0, "real_effects": 0,
                "proposals": [p.as_dict() for p in self.proposals.values()],
                "receipts": list(self.receipts.values()), "events": self.audit.events,
                "audit_chain_valid": self.audit.verify(self.audit.events),
                "limitations": ["Memory-only session", "Reviewer role is simulated, not real authentication",
                                "No LLM quality or production readiness claim"]})
