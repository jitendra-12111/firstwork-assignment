from typing import Any

from app.models import Rule
from app.services.placeholder import PlaceholderService
from app.services.rule_context import RuleContext
from app.utils.common_utils import cast_value, compare


class RuleEngine:
    def __init__(self, ctx: RuleContext, placeholders: dict[str, Any] | None = None):
        self.ctx = ctx
        self.placeholders = PlaceholderService(placeholders)

    def evaluate(self, rule_id: int) -> bool:
        if self.ctx.is_solved(rule_id):
            return self.ctx.get_output(rule_id)

        rule = self.ctx.get_rule(rule_id)
        op = rule.operator

        if op == 'OR':
            result = any(self.evaluate(int(c)) for c in rule.value.split(','))
        elif op == 'AND':
            result = all(self.evaluate(int(c)) for c in rule.value.split(','))
        else:
            result = self._evaluate_rule(rule)

        self.ctx.set_output(rule_id, result)
        return result

    def _evaluate_rule(self, rule: Rule) -> bool:
        left_operand, operator_data_type = self._parse_left_operand(rule)
        right_operand = self._parse_right_operand(rule, operator_data_type)

        if left_operand is None:
            raise ValueError(f"rule {rule.id}: left operand could not be parsed")
        if right_operand is None:
            raise ValueError(f"rule {rule.id}: right operand could not be parsed")

        return compare(left_operand, right_operand, rule.operator)

    def _parse_left_operand(self, rule: Rule):
        model_name, field_name = rule.field_name.split('.')
        model_instance = self.ctx.model_map[model_name]

        # Model base class has custom function that get field/column datatype in table
        # This will be the common datatype for both operand of operator
        rule_data_type = model_instance.get_field_type(field_name)

        left_operand_val = getattr(model_instance, field_name)

        return left_operand_val, rule_data_type

    def _parse_right_operand(self, rule: Rule, rule_data_type: str):
        raw = self.placeholders.resolve(rule.value)
        return cast_value(rule_data_type, raw)
