from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import contract_repo, rule_repo
from app.services.evaluate import RuleEvaluateService
from app.utils.common_utils import is_placeholder


class ContractService:
    def evaluate(self, db: Session, contract_id: int):
        contract = contract_repo.get_with_join_by_user_company(db, contract_id)

        if contract is None:
            raise HTTPException(status_code=404, detail="Contract not found")

        # TODO: rule_ids should come from request body, not hardcoded
        response = []
        evaluate_rule = RuleEvaluateService(db, contract)
        for rule in rule_repo.get_all(db):
            if not is_placeholder(rule.value):
                print(rule.id)
                rule_result = evaluate_rule.run(rule.id, {})
                print(rule_result)
                response.append({'id': rule.id, 'result': rule_result})

        return response


contract_service = ContractService()