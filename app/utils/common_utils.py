from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import Date, DateTime, DECIMAL, Integer, Boolean


def cast_value(field_type, value: str):
    # Cast str value to db field type

    if isinstance(field_type, Boolean):
        return value.strip().lower() == "true"
    elif isinstance(field_type, Date):
        return date.fromisoformat(value)
    elif isinstance(field_type, DateTime):
        return datetime.fromisoformat(value)
    elif isinstance(field_type, DECIMAL):
        return Decimal(value)
    elif isinstance(field_type, Integer):
        return int(value)

    return value


def is_placeholder(value):
    return value.startswith("{{") and value.endswith("}}")

def compare(left_operand, right_operand, operator: str):
    print(f"({left_operand} {operator} {right_operand})")
    if operator == '==':
        return left_operand == right_operand
    elif operator == '!=':
        return left_operand != right_operand
    elif operator == '>':
        return left_operand > right_operand
    elif operator == '<':
        return left_operand < right_operand
    elif operator == '>=':
        return left_operand >= right_operand
    elif operator == '<=':
        return left_operand <= right_operand

    raise Exception(f"Invalid operator: {operator}")