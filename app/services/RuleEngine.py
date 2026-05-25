from typing import Any

from app.models import Rule
from app.services.placeholder import PlaceholderService
from app.services.rule_context import RuleContext
from app.utils.common_utils import cast_value, compare
""" 
For a rule either composite or normal, start evaluation recursively
Depth first search. Add cache solved rule and db instance along the side
in RuleContext(Tree state independent of nodes)
"""

class RuleEngine:
    def __init__(self, ctx: RuleContext, placeholder: dict[str, Any] | None = None):
        self.ctx = ctx
        self.placeholder = PlaceholderService(placeholder)

    # Starting Point of evaluation
    # recursively go deep until rule is no composite and then solve that rule
    def evaluate(self, rule_id: int) -> bool:
        # If rule all ready solved use it
        if self.ctx.is_solved(rule_id):
            return self.ctx.get_output(rule_id)

        # fetch rule from tree state
        rule = self.ctx.get_rule(rule_id)

        # incase invalid rule id given
        if rule is None:
            raise Exception(f"Rule {rule_id}: not exists in db")

        op = rule.operator

        if op == 'OR':
            # value is comma separate sub rule id '1,2,3'
            # return true if at least one rule true
            result = any(self.evaluate(int(c)) for c in rule.value.split(','))
        elif op == 'AND':
            # value is comma separate sub rule id '1,2,3'
            # return true if all rules are true
            result = all(self.evaluate(int(c)) for c in rule.value.split(','))
        else:
            # Level 0 rule, evaluate it
            result = self._evaluate_rule(rule)

        # Cache result of rule_id, to avoid next time calculation
        self.ctx.set_output(rule_id, result)
        return result

    # Evaluate level 0 rule
    def _evaluate_rule(self, rule: Rule) -> bool:
        left_operand, operator_data_type = self._parse_left_operand(rule)
        right_operand = self._parse_right_operand(rule, operator_data_type)

        if left_operand is None:
            raise ValueError(f"rule {rule.id}: left operand could not be parsed")
        if right_operand is None:
            raise ValueError(f"rule {rule.id}: right operand could not be parsed")

        return compare(left_operand, right_operand, rule.operator)


    def _parse_left_operand(self, rule: Rule):
        # field name e.g User.age -> User, age
        model_name, field_name = rule.field_name.split('.')

        # model_name e.g User -> get model instance
        model_instance = self.ctx.model_map[model_name]

        # Model base class has custom function that get field/column datatype in table
        # This will be the common datatype for both operand of operator
        rule_data_type = model_instance.get_field_type(field_name)

        left_operand_val = getattr(model_instance, field_name)

        return left_operand_val, rule_data_type

    def _parse_right_operand(self, rule: Rule, rule_data_type: str):
        # placeholder parse first based on bindings
        raw = self.placeholder.resolve(rule.value)

        return cast_value(rule_data_type, raw)
