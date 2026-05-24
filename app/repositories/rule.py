from sqlalchemy.orm import Session, joinedload
from app.models import Rule


class RuleRepository:
    def get_by_id(self, db: Session, rule_id: int):
        return db.get(Rule, rule_id)

    def get_all(self, db: Session):
        return db.query(Rule).all()


rule_repo = RuleRepository()