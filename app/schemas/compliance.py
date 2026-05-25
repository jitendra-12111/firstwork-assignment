from typing import Any

from pydantic import BaseModel, Field


class CompliancePayload(BaseModel):
    rule_ids: list[int]
    placeholders: list[dict[str, Any]] = Field(default_factory=list)
