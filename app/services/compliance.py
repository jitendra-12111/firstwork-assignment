from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import contract_repo
from app.services.contract import contract_service
from app.services.rule_context import RuleContext


class ComplianceService:
    def __init__(
        self,
        db: Session,
        contract_id: int,
        rule_ids: list[int],
        placeholders: dict[str, Any] | None = None,
    ):
        self.db = db
        self.contract_id = contract_id
        self.rule_ids = rule_ids
        self.placeholders = placeholders or {}

    def evaluate_policy(self):
        contract = contract_repo.get_with_join_by_user_company(self.db, self.contract_id)
        if contract is None:
            raise HTTPException(status_code=404, detail="Contract not found")

        ctx = RuleContext(self.db, contract, self.placeholders)
        try:
            results = contract_service.evaluate_rules(ctx, self.rule_ids)
        except KeyError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return {
            "contract_id": self.contract_id,
            "compliant": all(r["result"] for r in results),
            "rules": results,
        }
