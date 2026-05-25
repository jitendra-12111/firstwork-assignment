"""
Tests for POST /contracts/{contract_id}/evaluate

Response shape (always):
    {
      "evaluations": [
        { "placeholder": {...}, "compliant": <bool>,
          "rules": [{"rule_id": <int>, "result": <bool>}, ...] },
        ...
      ]
    }

When `placeholders` is omitted or [], the service still returns one evaluation

Seed reference:
    contract 1 = U1 (age 28, IN) + C1 active
    contract 2 = U2 (age 17, US) + C1 active
    rules: 1=Adult  10=AdultActive(AND)  12=IndianOrDeposit(OR)
           13=FullCompliance(Level2)  14=DrivingAge(placeholder AND)
"""

from tests.client import evaluate_compliance


def _only(body):
    """Convenience: most tests use a single eval pass; return its dict."""
    assert "evaluations" in body
    assert len(body["evaluations"]) == 1
    return body["evaluations"][0]


# ── WITHOUT PLACEHOLDERS (static rules) ────────────────────────────────

def test_rule_pass():
    # rule 1 = Adult (age >= 18); U1 age is 28 → pass
    resp = evaluate_compliance(1, {"rule_ids": [1]})
    assert resp.status_code == 200

    e = _only(resp.json())
    assert e["compliant"] is True
    assert e["rules"] == [{"rule_id": 1, "result": True}]


def test_composite_and_pass():
    # rule 10 = AdultActive (Adult AND ActiveContract)
    resp = evaluate_compliance(1, {"rule_ids": [10]})
    assert resp.status_code == 200

    e = _only(resp.json())
    assert e["compliant"] is True
    assert e["rules"] == [{"rule_id": 10, "result": True}]


def test_level1_or_pass():
    # rule 12 = IndianOrDeposit (Indian OR deposit50k)
    resp = evaluate_compliance(1, {"rule_ids": [12]})
    assert resp.status_code == 200

    e = _only(resp.json())
    assert e["compliant"] is True
    assert e["rules"] == [{"rule_id": 12, "result": True}]


def test_composite_level2_pass():
    # rule 13 = FullCompliance (level 2 nested AND)
    resp = evaluate_compliance(1, {"rule_ids": [13]})
    assert resp.status_code == 200

    e = _only(resp.json())
    assert e["compliant"] is True
    assert e["rules"] == [{"rule_id": 13, "result": True}]


# ── WITH PLACEHOLDERS ───────────────────────────────────────────────────

def test_placeholder_driving_age_pass():
    # rule 14 = DrivingAge (nationality=={{country}} AND age>{{age}})
    # U1: IN, 28 — matches country=IN, age>18
    resp = evaluate_compliance(1, {
        "rule_ids": [14],
        "placeholders": [{"country": "IN", "age": "18"}],
    })
    assert resp.status_code == 200

    e = _only(resp.json())
    assert e["placeholder"] == {"country": "IN", "age": "18"}
    assert e["compliant"] is True
    assert e["rules"] == [{"rule_id": 14, "result": True}]


def test_bulk_placeholders():
    # Two placeholder sets for rule 14 against contract 1 (U1: IN, 28).
    # Set 1 (IN/18) → passes; Set 2 (US/18) → fails (nationality mismatch).
    resp = evaluate_compliance(1, {
        "rule_ids": [14],
        "placeholders": [
            {"country": "IN", "age": "18"},
            {"country": "US", "age": "18"},
        ],
    })
    assert resp.status_code == 200

    body = resp.json()
    assert len(body["evaluations"]) == 2

    first, second = body["evaluations"]
    assert first["compliant"] is True
    assert second["compliant"] is False


# ── RESPONSE SHAPE ─────────────────────────────────────────────────────

def test_compliance_response_shape():
    """Every evaluation has placeholder, compliant, and rules (list of {rule_id, result})."""
    resp = evaluate_compliance(1, {"rule_ids": [1, 10]})
    assert resp.status_code == 200

    body = resp.json()
    assert set(body.keys()) == {"evaluations"}

    for e in body["evaluations"]:
        assert set(e.keys()) == {"placeholder", "compliant", "rules"}
        assert isinstance(e["placeholder"], dict)
        assert isinstance(e["compliant"], bool)
        for rule in e["rules"]:
            assert set(rule.keys()) == {"rule_id", "result"}
            assert isinstance(rule["rule_id"], int)
            assert isinstance(rule["result"], bool)
