"""
Thin HTTP client. One function per API endpoint.
Tests import these so URLs aren't repeated everywhere.
"""

from fastapi.testclient import TestClient

from main import app

_client = TestClient(app)


def create_rule(payload: dict):
    return _client.post("/rule/", json=payload)


def update_rule(rule_id: int, payload: dict):
    return _client.patch(f"/rule/{rule_id}", json=payload)


def evaluate_compliance(contract_id: int, payload: dict):
    return _client.post(f"/contracts/{contract_id}/evaluate", json=payload)


def eligible_contracts(company_id: int, payload: dict):
    return _client.post(f"/contracts/{company_id}/eligible-contracts", json=payload)
