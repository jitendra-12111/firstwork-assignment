from typing import Any
from pydantic import BaseModel, Field


class EligibilityPayload(BaseModel):
    rule_id: int
    placeholders: list[dict[str, Any]] = Field(default_factory=list)
