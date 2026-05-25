from app.services.RuleEngine import RuleEngine
from app.services.rule_context import RuleContext


class ContractService:
    def evaluate_rules(self, ctx: RuleContext, rule_ids: list[int]):
        # RuleEngine is initiation of rule like a root node as it access child those child also got initiated
        engine = RuleEngine(ctx, ctx.placeholder)
        response = []
        for rule_id in rule_ids:
            """
                Each rule_id can be level 2 or level 1 or level 0 rule
                Some rule_id has common level 1 or level 0 rule
                So cached those rule db instance, result,
                It optimised overall computation
                so common rule evaluate once and placeholder is common for contract
            """
            output = engine.evaluate(rule_id)
            response.append({'id': rule_id, 'result': output})
        return response


contract_service = ContractService()