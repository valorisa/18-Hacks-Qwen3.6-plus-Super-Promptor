# src/py_mdlint/rules/md055.py
"""MD055: table-pipe-style — Table pipe style."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD055(Rule):
    rule_id = "MD055"
    alias = "table-pipe-style"
    description = "Table pipe style"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "leading_and_trailing")

        for i, line in enumerate(lines, 1):
            if "|" not in line:
                continue
            stripped = line.strip()
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue

            has_lead = stripped.startswith("|")
            has_trail = stripped.endswith("|")

            if style == "leading" and has_trail:
                violations.append(Violation(self.rule_id, i, 1, "Trailing pipe not expected", True))
            elif style == "trailing" and has_lead:
                violations.append(Violation(self.rule_id, i, 1, "Leading pipe not expected", True))
            elif style == "leading_and_trailing" and (not has_lead or not has_trail):
                violations.append(Violation(self.rule_id, i, 1, "Missing table pipe", True))
            elif style == "no_pipes" and (has_lead or has_trail):
                violations.append(Violation(self.rule_id, i, 1, "Pipe not expected", True))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
