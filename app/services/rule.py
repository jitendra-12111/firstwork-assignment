
# cache = {}
# result = {}
# contract = ''
# def get_rule(rule_id):
#     #TODO read cache and update cache
#     return cache.get(rule_id)
#
# def solve(rule_id, operator, value) -> int:
#     if rule_id in result:
#         return result[rule_id]
#
#     if operator == 'OR':
#         for child_rule_id in value.split(','):
#             if child_rule_id not in result:
#                 if child_rule_id in cache:
#                     child_rule  = cache[child_rule_id]
#                 else:
#                     child_rule = get_rule(child_rule_id)
#
#                 result[child_rule_id] = solve(child_rule_id, child_rule.operator, child_rule.value)
#
#             if result[child_rule_id] == 1:
#                 return 1
#
#         return 0
#
#     elif operator == 'AND':
#         for child_rule_id in value.split(','):
#             if child_rule_id not in result:
#                 if child_rule_id in cache:
#                     child_rule = cache[child_rule_id]
#                 else:
#                     child_rule = get_rule(child_rule_id)
#
#                 result[child_rule_id] = solve(child_rule_id, child_rule.operator, child_rule.value)
#
#             if result[child_rule_id] == 0:
#                 return 0
#
#         return 1
#
#     else:
#         return solve_parse(rule_id, contract)
#
#
#
# def solve_parse(rule_id, contract):
#     pass