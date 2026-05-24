from app.models import Contract, Rule
from app.utils.common_utils import cast_value, compare, is_placeholder


class RuleEngine:

    def __init__(self, contract: Contract):
        self.model_map = {
            'Contract': contract,
            'User': contract.user,
            'Company': contract.company
        }

    def evaluate(self, rule: Rule, placeholder=None) -> bool:
        left_operand, right_operand = self.parse_operands(
            rule=rule,
            placeholder=placeholder
        )
        result = compare(left_operand, right_operand, rule.operator)
        return result

    def parse_operands(self, rule: Rule, placeholder):
        left_operand, rule_data_type = self.parse_left_operand(rule)
        right_operand = self.parse_right_operand(
            rule=rule,
            rule_data_type=rule_data_type,
            placeholder=placeholder
        )

        if left_operand is None:
            raise Exception('Parsing error in left operand')

        if right_operand is None:
            raise Exception('Parsing error in right operand')

        return left_operand, right_operand

    def parse_left_operand(self, rule: Rule):
        model_name, field_name = rule.field_name.split('.')
        model_instance = self.model_map[model_name]

        # Model base class has custom function that get field/column datatype in table
        # This will be the common datatype for both operand of operator
        rule_data_type = model_instance.get_field_type(field_name)

        left_operand_val = getattr(model_instance, field_name)

        return left_operand_val, rule_data_type


    def parse_right_operand(self, rule, rule_data_type, placeholder):
        # DB str value of rule, not a placeholder
        raw_value = rule.value

        # In case placeholder, we got a place in extra params
        if is_placeholder(rule.value):
            print(rule.value)
            if placeholder is None:
                raise Exception('placeholder field is None')

            # DB and Placeholder now in same data type, later parse with rule datatype
            raw_value = str(placeholder)


        # parse raw_value to rule_data_type
        # rule_data_type is a common datatype for operator
        return cast_value(rule_data_type, raw_value)





