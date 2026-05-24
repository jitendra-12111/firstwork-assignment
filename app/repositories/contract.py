from sqlalchemy.orm import Session, joinedload
from app.models import Contract


class ContractRepository:
    def get_by_id(self, db: Session, contract_id: int):
        return db.get(Contract, contract_id)

    def get_with_join_by_user_company(self, db: Session, contract_id: int):
        return (
            db.query(Contract)
            .options(
                joinedload(Contract.user),
                joinedload(Contract.company)
            )
            .filter(Contract.id == contract_id)
            .first()
        )




contract_repo = ContractRepository()