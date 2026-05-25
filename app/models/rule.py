from sqlalchemy import Column, Integer, String, Text, UniqueConstraint

from app.db.session import Base


class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    field_name = Column(String(255), nullable=False)
    operator = Column(String(3), nullable=False)
    value = Column(Text, nullable=False)

    #TODO Need to comment this, with value a json string it's become complicated to create a index will think on that

    # # to deal with duplicate rule and race condition
    # __table_args__ = (
    #     UniqueConstraint('field_name', 'operator', 'value', name='uq_rule_combination'),
    # )


