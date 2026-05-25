from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Rule
from app.schemas.rule import RuleResponse, RuleCreate, RuleUpdate

router = APIRouter(prefix="/rule", tags=["Rule"])


@router.post("/", response_model=RuleResponse, status_code=201)
def create_rule(body: RuleCreate, db: Session = Depends(get_db)):
    # create a db model instance
    rule = Rule(**body.model_dump())

    # adding in session and not commited
    db.add(rule)

    # In commit, db check for duplicate or race condition based on table unique constraint index
    # capturing data integrity exception
    try:
        db.commit()
    except IntegrityError:
        # reset the session
        db.rollback()
        raise HTTPException(status_code=409, detail='Duplicate rule, already exists')
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    # after refresh, rule will get generate id
    db.refresh(rule)

    # Return response model handle rule(model instance) -> pydantic object creation -> dict -> json string for ui
    return rule


@router.patch('/{rule_id}', response_model=RuleResponse)
def update_rule(rule_id: int, body: RuleUpdate, db: Session = Depends(get_db)):
    # Checking first rule exists or not
    rule = db.get(Rule, rule_id)

    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    updates = body.model_dump(exclude_none=True)

    for key, value in updates.items():
        setattr(rule, key, value)

    try:
        db.commit()
    #Exception of integrity won't work now as i removed unique index
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Duplicate rule, already exists')
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    db.refresh(rule)
    return rule



@router.get('/', response_model=List[RuleResponse])
def get_rules(db: Session = Depends(get_db)):
    return db.query(Rule).all()
