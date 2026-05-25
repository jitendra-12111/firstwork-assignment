"""
Tests for POST /companies/{company_id}/eligible-contracts

Response shape: list[int] — contract ids that pass the rule.

Seed reference (C1 = company id 1):
    contract 1 = U1 (28, IN) active   → adult
    contract 2 = U2 (17, US) active   → minor
"""

from tests.client import eligible_contracts


def test_eligibility_rule():
    # rule 1 = Adult — contract 1 passes, contract 2 fails
    resp = eligible_contracts(1, {"rule_id": 1})
    assert resp.status_code == 200

    ids = resp.json()
    assert 1 in ids
    assert 2 not in ids


def test_eligibility_with_placeholder():
    # rule 14 = DrivingAge IN/18 — only U1(IN,28) qualifies
    resp = eligible_contracts(1, {
        "rule_id": 14,
        "placeholder": {"country": "IN", "age": "18"},
    })
    assert resp.status_code == 200

    ids = resp.json()
    assert 1 in ids
    assert 2 not in ids


def test_eligibility_composite_level1():
    # rule 10 = AdultActive (AND) — only contract 1 passes
    resp = eligible_contracts(1, {"rule_id": 10})
    assert resp.status_code == 200

    ids = resp.json()
    assert 1 in ids
    assert 2 not in ids


def test_eligibility_composite_level2():
    # rule 13 = FullCompliance (level 2 nested AND) — only contract 1 passes
    resp = eligible_contracts(1, {"rule_id": 13})
    assert resp.status_code == 200

    ids = resp.json()
    assert 1 in ids
    assert 2 not in ids


def test_eligibility_response_shape():
    """Response must be a list of ints (contract ids)."""
    resp = eligible_contracts(1, {"rule_id": 1})
    assert resp.status_code == 200

    body = resp.json()
    assert isinstance(body, list)
    for item in body:
        assert isinstance(item, int)
