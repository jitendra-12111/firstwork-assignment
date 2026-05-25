from typing import Any
from pydantic import BaseModel, Field


class EligibilityPayload(BaseModel):
    rule_id: int
    placeholders: dict[str, Any] = Field(default_factory=dict)
