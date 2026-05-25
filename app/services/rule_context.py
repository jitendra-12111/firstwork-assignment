from sqlalchemy.orm import Session

from app.models import Contract
from app.repositories import rule_repo


class RuleContext:
    def __init__(self, db: Session, contract: Contract, placeholders: dict | None = None):
        self.db = db
        self.contract = contract
        self.placeholders = placeholders or {}
        self._rule_cache = {}
        self._output_cache = {}
        self.model_map = {
            'Contract': contract,
            'User': contract.user,
            'Company': contract.company,
        }

    def get_rule(self, rule_id: int):
        if rule_id not in self._rule_cache:
            self._rule_cache[rule_id] = rule_repo.get_by_id(self.db, rule_id)
        return self._rule_cache[rule_id]

    def get_output(self, rule_id: int) -> bool:
        return self._output_cache[rule_id]

    def set_output(self, rule_id: int, result: bool) -> None:
        self._output_cache[rule_id] = result

    def is_solved(self, rule_id: int) -> bool:
        return rule_id in self._output_cache
