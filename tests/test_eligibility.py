"""
Tests for POST /contracts/{company_id}/eligible-contracts

Response shape (per item):
    {"contract_id": <int>, "eligible": <bool>}

Seed reference (C1 = company id 1):
    contract 1 = U1 (28, IN) active
    contract 2 = U2 (17, US) active
"""

from tests.client import eligible_contracts


def _to_dict(response_json):
    """Flatten the response into {contract_id: eligible_bool} for easy asserts."""
    return {item["contract_id"]: item["eligible"] for item in response_json}


def test_eligibility_rule():
    # rule 1 = Adult — contract 1 (U1 age 28) pass, contract 2 (U2 age 17) fail
    resp = eligible_contracts(1, {"rule_id": 1})
    assert resp.status_code == 200

    results = _to_dict(resp.json())
    assert results[1] is True
    assert results[2] is False


def test_eligibility_with_placeholder():
    # rule 14 = DrivingAge IN/18 — U1(IN,28) pass, U2(US,17) fail
    resp = eligible_contracts(1, {
        "rule_id": 14,
        "placeholder": {"country": "IN", "age": "18"},
    })
    assert resp.status_code == 200

    results = _to_dict(resp.json())
    assert results[1] is True
    assert results[2] is False


def test_eligibility_composite_level1():
    # rule 10 = AdultActive (AND) — contract 1 pass, contract 2 fail
    resp = eligible_contracts(1, {"rule_id": 10})
    assert resp.status_code == 200

    results = _to_dict(resp.json())
    assert results[1] is True
    assert results[2] is False


def test_eligibility_composite_level2():
    # rule 13 = FullCompliance (level 2 nested AND)
    resp = eligible_contracts(1, {"rule_id": 13})
    assert resp.status_code == 200

    results = _to_dict(resp.json())
    assert results[1] is True
    assert results[2] is False


def test_eligibility_response_shape():
    """Each item must have exactly 'contract_id' (int) and 'eligible' (bool)."""
    resp = eligible_contracts(1, {"rule_id": 1})
    assert resp.status_code == 200

    body = resp.json()
    assert isinstance(body, list) and len(body) > 0
    for item in body:
        assert set(item.keys()) == {"contract_id", "eligible"}
        assert isinstance(item["contract_id"], int)
        assert isinstance(item["eligible"], bool)
