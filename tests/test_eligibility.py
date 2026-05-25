"""
Tests for POST /companies/{company_id}/eligible-contracts

Response shape (always):
    {
      "evaluations": [
        { "placeholder": {...}, "eligible_contract_ids": [<int>, ...] },
        ...
      ]
    }

When `placeholders` is omitted or [], the service returns one evaluation
with placeholder={} (single static pass).

Seed reference (C1 = company id 1):
    contract 1 = U1 (28, IN) active   → adult
    contract 2 = U2 (17, US) active   → minor
"""

from tests.client import eligible_contracts


def _only(body):
    """Most tests use a single eval pass; return its dict."""
    assert "evaluations" in body
    assert len(body["evaluations"]) == 1
    return body["evaluations"][0]


def test_eligibility_rule():
    # rule 1 = Adult — contract 1 passes, contract 2 fails
    resp = eligible_contracts(1, {"rule_id": 1})
    assert resp.status_code == 200

    e = _only(resp.json())
    assert 1 in e["eligible_contract_ids"]
    assert 2 not in e["eligible_contract_ids"]


def test_eligibility_with_placeholder():
    # rule 14 = DrivingAge IN/18 — only U1(IN,28) qualifies
    resp = eligible_contracts(1, {
        "rule_id": 14,
        "placeholders": [{"country": "IN", "age": "18"}],
    })
    assert resp.status_code == 200

    e = _only(resp.json())
    assert e["placeholder"] == {"country": "IN", "age": "18"}
    assert 1 in e["eligible_contract_ids"]
    assert 2 not in e["eligible_contract_ids"]


def test_eligibility_composite_level1():
    # rule 10 = AdultActive (AND) — only contract 1 passes
    resp = eligible_contracts(1, {"rule_id": 10})
    assert resp.status_code == 200

    e = _only(resp.json())
    assert 1 in e["eligible_contract_ids"]
    assert 2 not in e["eligible_contract_ids"]


def test_eligibility_composite_level2():
    # rule 13 = FullCompliance (level 2 nested AND) — only contract 1 passes
    resp = eligible_contracts(1, {"rule_id": 13})
    assert resp.status_code == 200

    e = _only(resp.json())
    assert 1 in e["eligible_contract_ids"]
    assert 2 not in e["eligible_contract_ids"]


def test_eligibility_bulk_placeholders():
    # Two placeholder sets: IN/18 → contract 1 eligible; US/18 → neither eligible.
    resp = eligible_contracts(1, {
        "rule_id": 14,
        "placeholders": [
            {"country": "IN", "age": "18"},
            {"country": "US", "age": "18"},
        ],
    })
    assert resp.status_code == 200

    body = resp.json()
    assert len(body["evaluations"]) == 2

    first, second = body["evaluations"]
    assert 1 in first["eligible_contract_ids"]
    assert second["eligible_contract_ids"] == []


def test_eligibility_response_shape():
    """Every evaluation has placeholder (dict) and eligible_contract_ids (list[int])."""
    resp = eligible_contracts(1, {"rule_id": 1})
    assert resp.status_code == 200

    body = resp.json()
    assert set(body.keys()) == {"evaluations"}

    for e in body["evaluations"]:
        assert set(e.keys()) == {"placeholder", "eligible_contract_ids"}
        assert isinstance(e["placeholder"], dict)
        assert isinstance(e["eligible_contract_ids"], list)
        for cid in e["eligible_contract_ids"]:
            assert isinstance(cid, int)
