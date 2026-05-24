from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from app.db.session import Base


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=False)
    country = Column(String(2), nullable=False) # country code
    bank_deposit = Column(DECIMAL(12,2), nullable=False)


    # Only ORM relationship, not in db
    contracts = relationship("Contract", back_populates="company")