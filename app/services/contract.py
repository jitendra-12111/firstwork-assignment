from app.services.evaluate import RuleEngine
from app.services.rule_context import RuleContext


class ContractService:
    def evaluate_rules(self, ctx: RuleContext, rule_ids: list[int]):

        engine = RuleEngine(ctx, ctx.placeholders)
        response = []
        for rule_id in rule_ids:
            output = engine.evaluate(rule_id)
            response.append({'id': rule_id, 'result': output})
        return response


contract_service = ContractService()