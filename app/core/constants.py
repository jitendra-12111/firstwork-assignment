VALID_OPERATORS = {"==", "!=", ">", "<", ">=", "<="}
COMPOSITE_OPERATORS = {"AND", "OR"}

PLACEHOLDER_PATTERN = r"\{\{(\w+)\}\}"


ALLOWED_FIELDS = {
    "User.name", "User.age", "User.nationality", "User.date_of_birth",
    "Company.name", "Company.industry", "Company.country", "Company.bank_deposit",
    "Contract.start_date", "Contract.end_date", "Contract.country", "Contract.is_active",
}
