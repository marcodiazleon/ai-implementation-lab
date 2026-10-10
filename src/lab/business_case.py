"""Business case: guided diagnosis and cost/benefit estimate (S01 R28, R29).

Deterministic and offline. Mirrored for the public build in web/public-demo.js; tests/test_parity.py
compares both. A missing answer becomes an open question, never a confirmed requirement, and every
figure is an estimate from stated assumptions, never a saving obtained.
"""
import math

TEXT_FIELDS = ["company", "problem", "users", "current_process", "constraints", "success"]
NUMBER_FIELDS = {"monthly_volume": (1, 1000000), "minutes_per_case": (0.1, 600)}
CHOICE_FIELDS = {"data_sensitivity": ("none", "internal", "personal"),
                 "action_type": ("inform", "recommend", "execute")}
DIAGNOSIS_FIELDS = TEXT_FIELDS + list(NUMBER_FIELDS) + list(CHOICE_FIELDS)

ESTIMATE_FIELDS = {"monthly_volume": (1, 1000000), "manual_minutes": (0.1, 600),
                   "assisted_minutes": (0, 600), "review_rate": (0, 1), "hourly_cost": (0, 100000),
                   "implementation_cost": (0, 10000000), "monthly_operation_cost": (0, 1000000)}
# Visible sensitivity factors: slower assisted work and more manual escalations in the conservative case.
SCENARIOS = [("conservative", 1.25, 0.10), ("base", 1.0, 0.0), ("optimistic", 0.8, -0.05)]
LOW_VOLUME_MINUTES = 600
# A pilot is recommended only when the base scenario repays the implementation within this many months.
PAYBACK_LIMIT_MONTHS = 12


def money(value):
    """Two-decimal rounding with the same arithmetic in Python and JavaScript."""
    return math.floor(value * 100 + 0.5) / 100


def is_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def diagnose(body):
    if not isinstance(body, dict) or set(body) - set(DIAGNOSIS_FIELDS):
        return {"status": "INVALID_INPUT", "fields": ["_shape"]}
    invalid, answers = [], {}
    for field in TEXT_FIELDS:
        value = body.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        if not isinstance(value, str) or len(value.strip()) > 500:
            invalid.append(field)
        else:
            answers[field] = value.strip()
    for field, (low, high) in NUMBER_FIELDS.items():
        value = body.get(field)
        if value is None:
            continue
        if not is_number(value) or not low <= value <= high:
            invalid.append(field)
        else:
            answers[field] = value
    for field, options in CHOICE_FIELDS.items():
        value = body.get(field)
        if value is None or value == "":
            continue
        if value not in options:
            invalid.append(field)
        else:
            answers[field] = value
    if invalid:
        return {"status": "INVALID_INPUT", "fields": invalid}

    missing = [field for field in DIAGNOSIS_FIELDS if field not in answers]
    action = answers.get("action_type")
    level = {"inform": "ASSIST", "recommend": "PROPOSE_AND_APPROVE",
             "execute": "PROPOSE_AND_APPROVE"}.get(action)
    risks = []
    if answers.get("data_sensitivity") == "personal":
        risks.append("PERSONAL_DATA")
    if action == "execute":
        risks.append("EXECUTION_NEEDS_APPROVAL")
    if "monthly_volume" in answers and "minutes_per_case" in answers:
        if answers["monthly_volume"] * answers["minutes_per_case"] < LOW_VOLUME_MINUTES:
            risks.append("LOW_VOLUME")
    else:
        risks.append("UNMEASURED_BASELINE")
    return {"status": "BRIEF_INCOMPLETE" if missing else "BRIEF_READY",
            "confirmed": [{"field": f, "value": answers[f]} for f in DIAGNOSIS_FIELDS if f in answers],
            "open_questions": missing, "recommended_level": level, "risks": risks,
            "first_increment": {"ASSIST": "DRAFT_WITH_HUMAN_DECISION",
                                "PROPOSE_AND_APPROVE": "PROPOSAL_WITH_APPROVAL_GATE"}.get(level, "DEFINE_ACTION_FIRST"),
            "estimate_inputs": {k: answers[k] for k in ("monthly_volume", "minutes_per_case") if k in answers}}


def scenario(name, values, assisted_factor, review_shift):
    assisted = values["assisted_minutes"] * assisted_factor
    review = min(1, max(0, values["review_rate"] + review_shift))
    minutes_saved = values["monthly_volume"] * (1 - review) * (values["manual_minutes"] - assisted)
    hours_saved = minutes_saved / 60
    gross = hours_saved * values["hourly_cost"]
    net = gross - values["monthly_operation_cost"]
    payback = values["implementation_cost"] / net if net > 0 else None
    return {"scenario": name, "assisted_minutes": money(assisted), "review_rate": money(review),
            "hours_saved_per_month": money(hours_saved), "gross_benefit_per_month": money(gross),
            "net_benefit_per_month": money(net),
            "payback_months": None if payback is None else money(payback),
            "first_year_net": money(net * 12 - values["implementation_cost"])}


def estimate(body):
    if not isinstance(body, dict) or set(body) != set(ESTIMATE_FIELDS):
        return {"status": "INVALID_INPUT", "fields": ["_shape"]}
    invalid = [f for f, (low, high) in ESTIMATE_FIELDS.items()
               if not is_number(body[f]) or not low <= body[f] <= high]
    if invalid:
        return {"status": "INVALID_INPUT", "fields": invalid}
    rows = [scenario(n, body, a, r) for n, a, r in SCENARIOS]
    base = rows[1]["payback_months"]
    return {"status": "ESTIMATE", "kind": "ESTIMATE_NOT_OBSERVED", "currency": "DEMO",
            "observed_savings": 0, "inputs": dict(body), "scenarios": rows,
            "recommendation": "PILOT" if base is not None and base <= PAYBACK_LIMIT_MONTHS else "REVISIT_SCOPE",
            "payback_limit_months": PAYBACK_LIMIT_MONTHS,
            "factors": [{"scenario": n, "assisted_factor": a, "review_shift": r} for n, a, r in SCENARIOS]}
