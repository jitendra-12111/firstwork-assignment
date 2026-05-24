from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.orm import relationship

from app.db.session import Base


class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False) # UTC timezone
    end_date = Column(DateTime(timezone=True), nullable=False) # UTC timezone
    country = Column(String(2), nullable=False) # country code
    is_active = Column(Boolean, nullable=False, default=False)



    # Only ORM relationship, not in db
    user = relationship("User", back_populates="contracts")
    company = relationship("Company", back_populates="contracts")


    # Query time reduced, improve performance, help in scaling multiple requests
    # index_user_contract_id -> user fetch all contracts
    # index_company_contract_id -> company fetch all contracts
    # index_company_active_contract -> get all active contracts of company
    __table_args__ = (
        Index('index_user_contract_id', 'user_id'),
        Index('index_company_contract_id', 'company_id'),
        Index('index_company_active_contract', 'company_id', 'is_active'),
    )

