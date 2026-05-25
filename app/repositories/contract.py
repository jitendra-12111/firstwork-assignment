from sqlalchemy.orm import Session, joinedload
from app.models import Contract



class ContractRepository:
    def get_by_id(self, db: Session, contract_id: int):
        return db.get(Contract, contract_id)

    """ Using joined to avoid 2N+1 operations when i fetch company or user in rule"""
    def get_contract_by_id_join_user_company(self, db: Session, contract_id: int):
        return (
            db.query(Contract)
            .options(
                joinedload(Contract.user),
                joinedload(Contract.company)
            )
            .filter(Contract.id == contract_id)
            .first()
        )


    """ Using joined to avoid 2N+1 operations when i fetch company or user in rule"""
    def get_company_contracts(self, db: Session, company_id: int):
        return (
            db.query(Contract)
            .options(
                joinedload(Contract.user),
                joinedload(Contract.company)
            )
            .filter(
                Contract.company_id == company_id
            )
            .all()
        )



# single cache object dynamic based on session
contract_repo = ContractRepository()