from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.compliance import CompliancePayload
from app.services import ComplianceService
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

# @router.get("/{company_id}/{rule_id}")
# def get_eligible_contracts(company_id, rule_id, db: Session = Depends(get_db)):
#     return contract_service.get_eligible_contracts(db, company_id, rule_id)
