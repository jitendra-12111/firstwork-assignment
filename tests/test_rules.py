import uuid

from tests.client import create_rule, update_rule


def _unique(name: str) -> str:
    return f"{name}_{uuid.uuid4().hex[:6]}"


# ── CREATE ──────────────────────────────────────────────────────────────

def test_create_valid_rule():
    resp = create_rule({
        "name": _unique("MinAge21"),
        "field_name": "User.age",
        "operator": ">=",
        "value": "21",
    })
    assert resp.status_code == 201


def test_create_valid_placeholder_rule():
    resp = create_rule({
        "name": _unique("TplCountry"),
        "field_name": "User.nationality",
        "operator": "==",
        "value": "{{country}}",
    })
    assert resp.status_code == 201


def test_create_invalid_operator():
    resp = create_rule({
        "name": _unique("BadOp"),
        "field_name": "User.age",
        "operator": "??",
        "value": "18",
    })
    assert resp.status_code == 422


def test_create_invalid_composite_operator():
    resp = create_rule({
        "name": _unique("BadComposite"),
        "field_name": "__composite__",
        "operator": "XOR",
        "value": "1,2",
    })
    assert resp.status_code == 422


def test_create_invalid_composite_value():
    resp = create_rule({
        "name": _unique("BadCompositeValue"),
        "field_name": "__composite__",
        "operator": "AND",
        "value": "a,b,c",
    })
    assert resp.status_code == 422


# ── UPDATE ──────────────────────────────────────────────────────────────

def test_update_valid():
    resp = update_rule(1, {"value": "21"})
    assert resp.status_code == 200


def test_update_invalid_operator():
    resp = update_rule(1, {"operator": "!!"})
    assert resp.status_code == 422
