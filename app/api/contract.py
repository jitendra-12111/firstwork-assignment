from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import contract_service
router = APIRouter(prefix="/contracts", tags=["Contracts"])


# TODO: add request body schema with rule_ids + group structure
@router.post("/{contract_id}/evaluate")
def evaluate(contract_id: int, db: Session = Depends(get_db)):
    return contract_service.evaluate(db, contract_id)

# @router.get("/{company_id}/{rule_id}")
# def get_eligible_contracts(company_id, rule_id, db: Session = Depends(get_db)):
