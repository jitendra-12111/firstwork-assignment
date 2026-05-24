from pydantic import BaseModel, ConfigDict


class RuleCreate(BaseModel):
    field_name: str
    operator: str
    value: str

class RuleUpdate(BaseModel):
    field_name: str |None = None
    operator: str| None = None
    value: str | None = None


class RuleResponse(BaseModel):
    id: int
    field_name: str
    operator: str
    value: str

    # It convert model to pydantic response with attribute based check
    model_config = ConfigDict(from_attributes=True)

