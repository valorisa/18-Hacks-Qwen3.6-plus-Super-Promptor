# src/py_mdlint/rules/md018.py
"""MD018: no-missing-space-atx — No space after hash on atx style heading."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD018(Rule):
    rule_id = "MD018"
    alias = "no-missing-space-atx"
    description = "No space after hash on atx style heading"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^#+[^#\s]', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "No space after #", True,
                    patch=Patch("replace", i, content=re.sub(r'^(#+)(\S)', r'\1 \2', line))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
