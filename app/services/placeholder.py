import re
from typing import Any

from app.core.constants import PLACEHOLDER_PATTERN

class PlaceholderService:
    PATTERN = re.compile(PLACEHOLDER_PATTERN)

    def __init__(self, bindings: dict[str, Any] | None = None):
        self.bindings = bindings or {}

    @classmethod
    def is_placeholder(cls, value: str) -> bool:
        return bool(cls.PATTERN.fullmatch(value))

    def resolve(self, value: str) -> str:
        m = self.PATTERN.fullmatch(value)
        if not m:
            return value
        name = m.group(1)
        if name not in self.bindings:
            raise KeyError(f"missing binding for placeholder '{name}'")
        return str(self.bindings[name])
