# src/py_mdlint/rules/md049.py
"""MD049: emphasis-style — Emphasis style."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD049(Rule):
    rule_id = "MD049"
    alias = "emphasis-style"
    description = "Emphasis style"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "asterisk")
        marker = "*" if style == "asterisk" else "_"
        other = "_" if style == "asterisk" else "*"

        for i, line in enumerate(lines, 1):
            if re.search(rf'{re.escape(other)}[^{re.escape(other)}]+{re.escape(other)}', line):
                violations.append(Violation(
                    self.rule_id, i, 1, f"Expected {marker} for emphasis", True,
                    patch=Patch("replace", i, content=re.sub(
                        rf'({re.escape(other)})([^{re.escape(other)}]+)({re.escape(other)})',
                        rf'{marker}\2{marker}', line
                    ))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
