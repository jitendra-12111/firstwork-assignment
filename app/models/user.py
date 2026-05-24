from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    nationality = Column(String(2), nullable=False) # country code
    date_of_birth = Column(Date, nullable=False)

    # Only ORM relationship, not in db
    contracts = relationship("Contract", back_populates="user")


