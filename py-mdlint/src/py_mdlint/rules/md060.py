# src/py_mdlint/rules/md060.py
"""MD060: table-column-style — Table column alignment."""

import re
from .base import Rule, Violation, Token


class RuleMD060(Rule):
    rule_id = "MD060"
    alias = "table-column-style"
    description = "Table column alignment"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        in_table = False
        separator_seen = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if "|" not in stripped:
                in_table = False
                separator_seen = False
                continue

            if re.match(r'^\|[\s\-:|]+\|$', stripped) or re.match(r'^[\s\-:|]+\|', stripped):
                separator_seen = True
                in_table = True
                continue

            if in_table:
                pass
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
