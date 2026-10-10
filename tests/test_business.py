import http.client
import json
import threading
import unittest
from src.lab.business_case import diagnose, estimate
from src.lab.controller import load_data
from src.lab.server import make_server

CASES = {row["id"]: row for row in load_data("business_cases.json")}


class DiagnosisTests(unittest.TestCase):
    def test_complete_and_incomplete_cases_produce_different_briefs(self):
        aurora, norte = diagnose(CASES["aurora"]["diagnosis"]), diagnose(CASES["norte"]["diagnosis"])
        self.assertEqual(aurora["status"], "BRIEF_READY")
        self.assertEqual(aurora["open_questions"], [])
        self.assertEqual(norte["status"], "BRIEF_INCOMPLETE")
        self.assertEqual(set(norte["open_questions"]), {"constraints", "success", "minutes_per_case"})
        self.assertNotEqual(aurora["recommended_level"], norte["recommended_level"])
        self.assertNotEqual(aurora["risks"], norte["risks"])

    def test_missing_answers_become_open_questions_not_confirmed(self):
        brief = diagnose({"problem": "  Respuestas lentas  ", "success": "   ", "monthly_volume": None, "action_type": ""})
        self.assertEqual(brief["status"], "BRIEF_INCOMPLETE")
        self.assertEqual(brief["confirmed"], [{"field": "problem", "value": "Respuestas lentas"}])
        confirmed = {row["field"] for row in brief["confirmed"]}
        self.assertFalse(confirmed & set(brief["open_questions"]))
        self.assertIn("success", brief["open_questions"])
        self.assertIsNone(brief["recommended_level"])
        self.assertEqual(brief["first_increment"], "DEFINE_ACTION_FIRST")
        self.assertIn("UNMEASURED_BASELINE", brief["risks"])
        self.assertEqual(brief["estimate_inputs"], {})

    def test_level_and_risk_rules(self):
        inform = diagnose({"action_type": "inform", "monthly_volume": 20, "minutes_per_case": 5})
        self.assertEqual((inform["recommended_level"], inform["first_increment"]), ("ASSIST", "DRAFT_WITH_HUMAN_DECISION"))
        self.assertEqual(inform["risks"], ["LOW_VOLUME"])
        execute = diagnose({"action_type": "execute", "data_sensitivity": "personal", "monthly_volume": 600, "minutes_per_case": 1})
        self.assertEqual(execute["recommended_level"], "PROPOSE_AND_APPROVE")
        self.assertEqual(execute["risks"], ["PERSONAL_DATA", "EXECUTION_NEEDS_APPROVAL"])
        self.assertEqual(execute["estimate_inputs"], {"monthly_volume": 600, "minutes_per_case": 1})

    def test_diagnosis_rejects_invalid_input(self):
        for body, field in [({"unknown": "x"}, "_shape"), ({"monthly_volume": True}, "monthly_volume"),
                            ({"problem": "x" * 501}, "problem"), ({"action_type": "deploy"}, "action_type"),
                            ({"minutes_per_case": 0}, "minutes_per_case"), ({"company": 7}, "company")]:
            with self.subTest(field=field):
                self.assertEqual(diagnose(body), {"status": "INVALID_INPUT", "fields": [field]})
        self.assertEqual(diagnose([])["status"], "INVALID_INPUT")


class EstimateTests(unittest.TestCase):
    def test_estimate_formulas_match_hand_calculation(self):
        base = estimate(CASES["aurora"]["estimate"])["scenarios"][1]
        # 1200 cases x (1 - 0.2) x (9 - 3) min = 5760 min = 96 h; x 20 = 1920; - 250 = 1670; 6000 / 1670 = 3.59.
        self.assertEqual(base, {"scenario": "base", "assisted_minutes": 3.0, "review_rate": 0.2, "hours_saved_per_month": 96.0,
                                "gross_benefit_per_month": 1920.0, "net_benefit_per_month": 1670.0, "payback_months": 3.59,
                                "first_year_net": 14040.0})

    def test_estimate_never_presents_savings_as_obtained(self):
        result = estimate(CASES["aurora"]["estimate"])
        self.assertEqual((result["kind"], result["observed_savings"], result["currency"]), ("ESTIMATE_NOT_OBSERVED", 0, "DEMO"))
        self.assertEqual(result["inputs"], CASES["aurora"]["estimate"])

    def test_sensitivity_is_ordered_visible_and_reproducible(self):
        result = estimate(CASES["aurora"]["estimate"])
        self.assertEqual(result, estimate(CASES["aurora"]["estimate"]))
        hours = [row["hours_saved_per_month"] for row in result["scenarios"]]
        self.assertEqual([row["scenario"] for row in result["scenarios"]], ["conservative", "base", "optimistic"])
        self.assertLess(hours[0], hours[1])
        self.assertLess(hours[1], hours[2])
        self.assertEqual(result["factors"][0], {"scenario": "conservative", "assisted_factor": 1.25, "review_shift": 0.1})

    def test_unprofitable_case_recommends_revisiting_scope(self):
        norte = estimate(CASES["norte"]["estimate"])
        self.assertIsNone(norte["scenarios"][1]["payback_months"])
        self.assertLess(norte["scenarios"][1]["net_benefit_per_month"], 0)
        self.assertEqual(norte["recommendation"], "REVISIT_SCOPE")
        self.assertEqual(estimate(CASES["aurora"]["estimate"])["recommendation"], "PILOT")
        slow = dict(CASES["aurora"]["estimate"], implementation_cost=40000)
        self.assertEqual(estimate(slow)["recommendation"], "REVISIT_SCOPE")

    def test_estimate_rejects_invalid_input(self):
        valid = CASES["aurora"]["estimate"]
        missing = dict(valid); del missing["hourly_cost"]
        self.assertEqual(estimate(missing), {"status": "INVALID_INPUT", "fields": ["_shape"]})
        for field, value in [("review_rate", 1.5), ("hourly_cost", -1), ("monthly_volume", "1200"), ("manual_minutes", None)]:
            with self.subTest(field=field):
                self.assertEqual(estimate(dict(valid, **{field: value})), {"status": "INVALID_INPUT", "fields": [field]})


class BusinessHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def call(self, method, path, body=None, host=None):
        c = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        headers = {"Content-Type": "application/json"} if body is not None else {}
        if host:
            headers["Host"] = host
        c.request(method, path, None if body is None else json.dumps(body), headers)
        r = c.getresponse(); result = (r.status, json.loads(r.read())); c.close()
        return result

    def test_business_routes(self):
        status, cases = self.call("GET", "/api/business/cases")
        self.assertEqual((status, [c["id"] for c in cases]), (200, ["aurora", "norte"]))
        status, brief = self.call("POST", "/api/business/diagnose", CASES["norte"]["diagnosis"])
        self.assertEqual((status, brief["status"]), (200, "BRIEF_INCOMPLETE"))
        status, result = self.call("POST", "/api/business/estimate", CASES["aurora"]["estimate"])
        self.assertEqual((status, result["recommendation"]), (200, "PILOT"))
        status, result = self.call("POST", "/api/business/estimate", {"monthly_volume": 1})
        self.assertEqual((status, result["status"]), (400, "INVALID_INPUT"))
        self.assertEqual(self.call("GET", "/api/business/cases", host="evil.example")[0], 403)


if __name__ == "__main__":
    unittest.main()
