# src/py_mdlint/rules/md050.py
"""MD050: strong-style — Strong style."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD050(Rule):
    rule_id = "MD050"
    alias = "strong-style"
    description = "Strong style"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "asterisk")
        marker = "**" if style == "asterisk" else "__"
        other = "__" if style == "asterisk" else "**"

        for i, line in enumerate(lines, 1):
            if other in line:
                violations.append(Violation(
                    self.rule_id, i, 1, f"Expected {marker} for strong", True,
                    patch=Patch("replace", i, content=line.replace(other, marker))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
