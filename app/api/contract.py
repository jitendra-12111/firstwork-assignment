from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import EligibilityPayload
from app.schemas.compliance import CompliancePayload
from app.services import ComplianceService
from app.services.eligiblity import EligibilityService

router = APIRouter(prefix="/contracts", tags=["Contracts"])


# TODO: add request body schema with rule_ids + group structure
@router.post("/{contract_id}/evaluate")
def evaluate(contract_id: int, body: CompliancePayload, db: Session = Depends(get_db)):

    compliance = ComplianceService(
        db=db,
        contract_id=contract_id,
        placeholders=body.placeholders,
        rule_ids=body.rule_ids,
    )
    return compliance.evaluate_policy()

@router.post("/{company_id}/eligible-contracts")
def evaluate(company_id: int, body: EligibilityPayload, db: Session = Depends(get_db)):

    eligibility_service = EligibilityService(
    )
    return eligibility_service.eligible_contracts(
        db=db,
        company_id=company_id,
        rule_id=body.rule_id,
        placeholders=body.placeholders
    )