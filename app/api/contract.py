from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import EligibilityPayload
from app.schemas.compliance import CompliancePayload
from app.services import ComplianceService
from app.services.eligiblity import EligibilityService

router = APIRouter(prefix="/contracts", tags=["Contracts"])


"""Evaluate compliance"""
@router.post("/{contract_id}/evaluate")
def evaluate(contract_id: int, body: CompliancePayload, db: Session = Depends(get_db)):
    """Return compliant bool true or false and rules result bool"""
    compliance = ComplianceService(
        db=db,
        contract_id=contract_id,
        placeholder=body.placeholder,
        rule_ids=body.rule_ids,
    )
    return compliance.evaluate_policy()