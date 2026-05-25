import re

from pydantic import BaseModel, ConfigDict, model_validator

from app.core.constants import ALLOWED_FIELDS, COMPOSITE_OPERATORS, VALID_OPERATORS

COMPOSITE_VALUE_PATTERN = re.compile(r"^\d+(,\d+)*$")  # "1,2,3"


def validate_rule_fields(op: str | None, fn: str | None, val: str | None) -> None:

    if op is not None and op not in VALID_OPERATORS | COMPOSITE_OPERATORS:
        raise ValueError(
            f"Invalid operator '{op}'. "
            f"Leaf: {VALID_OPERATORS}  Composite: {COMPOSITE_OPERATORS}"
        )

    if op in COMPOSITE_OPERATORS:
        if fn is not None and fn != "__composite__":
            raise ValueError(
                f"Composite rule (operator={op}) must have field_name='__composite__', got '{fn}'"
            )
        if val is not None and not COMPOSITE_VALUE_PATTERN.match(val):
            raise ValueError(
                f"Composite value must be comma-separated rule ids e.g. '1,2,3', got '{val}'"
            )

    elif op in VALID_OPERATORS:
        if fn is not None and fn not in ALLOWED_FIELDS:
            raise ValueError(
                f"Invalid field_name '{fn}'. Allowed: {sorted(ALLOWED_FIELDS)}"
            )
        if val is not None:
            if not val.strip():
                raise ValueError("value cannot be empty")


class RuleCreate(BaseModel):
    name: str
    field_name: str
    operator: str
    value: str

    @model_validator(mode="after")
    def validate_rule(self):
        # Here fields are not None, so all filed should have present
        validate_rule_fields(self.operator, self.field_name, self.value)
        return self


class RuleUpdate(BaseModel):
    name: str | None = None
    field_name: str | None = None
    operator: str | None = None
    value: str | None = None

    @model_validator(mode="after")
    def validate_rule(self):
        validate_rule_fields(self.operator, self.field_name, self.value)
        return self


class RuleResponse(BaseModel):
    id: int
    name: str
    field_name: str
    operator: str
    value: str

    model_config = ConfigDict(from_attributes=True)
