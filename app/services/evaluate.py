from sqlalchemy.orm import Session

from app.models import Contract, Rule
from app.repositories import rule_repo
from app.utils.common_utils import is_placeholder, cast_value, compare


class RuleEvaluateService:
    def __init__(self, db: Session, contract: Contract):
        self.contract = contract
        self.db = db
        self.rule_cache  = {}
        self.rule_eval = {}

        self.model_map = {
            'Contract': contract,
            'User': contract.user,
            'Company': contract.company
        }

    def _get_rule(self, rule_id: int) -> Rule:
        if rule_id not in self.rule_cache:
            self.rule_cache[rule_id] = rule_repo.get_by_id(self.db, rule_id)

        return self.rule_cache[rule_id]

    def run(self, rule_id: int, payload: dict):
        return self._solve(rule_id, payload)

    def _solve(self, rule_id: int, payload: dict):
        if rule_id in self.rule_eval:
            return self.rule_eval[rule_id]

        rule = self._get_rule(rule_id)

        if rule.operator == 'OR':
            result = any(self._solve(int(sub_rule_id), payload) for sub_rule_id in rule.value.split(','))

        elif rule.operator == 'AND':
            result = all(self._solve(int(sub_rule_id), payload) for sub_rule_id in rule.value.split(','))

        else:
            result = self._evaluate_rule(rule, payload)

        self.rule_eval[rule_id] = result

        return result

    def _evaluate_rule(self, rule: Rule, payload: dict):

        left_operand, rule_data_type = self.parse_left_operand(rule)

        right_operand = self.parse_right_operand(
            rule=rule,
            rule_data_type=rule_data_type,
            payload=payload
        )

        if left_operand is None:
            raise Exception('Parsing error in left operand')

        if right_operand is None:
            raise Exception('Parsing error in right operand')

        return compare(left_operand, right_operand, rule.operator)

    def parse_left_operand(self, rule: Rule):
        print(rule.operator, rule.field_name)
        model_name, field_name = rule.field_name.split('.')
        model_instance = self.model_map[model_name]

        # Model base class has custom function that get field/column datatype in table
        # This will be the common datatype for both operand of operator
        rule_data_type = model_instance.get_field_type(field_name)

        left_operand_val = getattr(model_instance, field_name)

        return left_operand_val, rule_data_type

    def parse_right_operand(self, rule, rule_data_type, payload):
        # DB str value of rule, not a placeholder
        raw_value = rule.value

        # In case placeholder, we got a place in extra params
        if is_placeholder(rule.value):
            # parsing_value
            placeholder_value = payload.get(rule.value[2:-2], None)
            print(placeholder_value)

            if placeholder_value is None:
                raise Exception('Parsing error in right operand')

            # DB and Placeholder now in same data type, later parse with rule datatype
            raw_value = str(placeholder_value)

        # parse raw_value to rule_data_type
        # rule_data_type is a common datatype for operator
        return cast_value(rule_data_type, raw_value)
