from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.compliance import CompliancePayload
from app.services import ComplianceService

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/{contract_id}/evaluate")
def evaluate(contract_id: int, body: CompliancePayload, db: Session = Depends(get_db)):
    """Evaluate the given rule_ids against a contract, once per placeholder set."""
    compliance = ComplianceService(
        db=db,
        contract_id=contract_id,
        rule_ids=body.rule_ids,
        placeholders=body.placeholders,
    )
    return compliance.evaluate_policy()
