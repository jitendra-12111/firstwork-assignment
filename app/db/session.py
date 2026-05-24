from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):

    @classmethod
    def get_field_type(cls, field_name):
        column = cls.__table__.columns.get(field_name)
        if column is not None:
            return column.type
        return None

def get_db():
    with Session(engine) as db:
        yield db