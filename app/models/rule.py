from sqlalchemy import Column, Integer, String, UniqueConstraint

from app.db.session import Base


class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    field_name = Column(String(255), nullable=False)
    operator = Column(String(3), nullable=False)  # max 3 chars e.g. ">=", "!="
    value = Column(String(255), nullable=False)

    # to deal with duplicate rule and race condition
    __table_args__ = (
        UniqueConstraint('field_name', 'operator', 'value', name='uq_rule_combination'),
    )


