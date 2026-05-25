from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import contract_repo
from app.services import contract_service
from app.services.rule_context import RuleContext


class EligibilityService:
    def eligible_contracts(self, db: Session,  company_id: int, rule_id: int, placeholders: dict | None = None):

        contracts = contract_repo.get_contract_by_company_id_join_user_company(db, company_id)

        if len(contracts) == 0:
            raise Exception('No contracts found')

        response = []

        for contract in contracts:
            ctx = RuleContext(
                db=db,
                contract=contract,
                placeholders=placeholders
            )

            try:
                results = contract_service.evaluate_rules(ctx, [rule_id])
                response.append({'contract_id' : contract.id, 'eligible' : results[0] })
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))


        return response