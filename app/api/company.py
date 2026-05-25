from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import EligibilityPayload
from app.services.eligiblity import EligibilityService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/{company_id}/eligible-contracts")
def eligible_contracts(company_id: int, body: EligibilityPayload, db: Session = Depends(get_db)):
    """Return contract ids (under this company) that pass the rule, per placeholder set."""
    eligibility_service = EligibilityService()
    return eligibility_service.eligible_contracts(
        db=db,
        company_id=company_id,
        rule_id=body.rule_id,
        placeholders=body.placeholders,
    )
