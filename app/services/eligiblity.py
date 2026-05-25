from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import contract_repo
from app.services import contract_service
from app.services.rule_context import RuleContext


class EligibilityService:
    def eligible_contracts(
        self,
        db: Session,
        company_id: int,
        rule_id: int,
        placeholders: list[dict[str, Any]] | None = None,
    ):
        """Get company contracts (with user + company joined to avoid 2N+1)"""
        contracts = contract_repo.get_company_contracts(db, company_id)

        if len(contracts) == 0:
            raise HTTPException(status_code=404, detail="Company has no contracts")

        placeholder_sets = placeholders if placeholders else [{}]

        response = []
        try:
            for placeholder in placeholder_sets:
                eligible_ids = []
                for contract in contracts:
                    """Rule Context is common for all sub rules of each contract"""
                    ctx = RuleContext(db=db, contract=contract, placeholder=placeholder)
                    results = contract_service.evaluate_rules(ctx, [rule_id])
                    if results[0]['result']:
                        eligible_ids.append(contract.id)
                response.append({
                    "placeholder": placeholder,
                    "eligible_contract_ids": eligible_ids,
                })
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return {"evaluations": response}
