# src/py_mdlint/rules/md019.py
"""MD019: no-multiple-space-atx — Multiple spaces after hash on atx style heading."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD019(Rule):
    rule_id = "MD019"
    alias = "no-multiple-space-atx"
    description = "Multiple spaces after hash on atx style heading"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^#+\s{2,}', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "Multiple spaces after #", True,
                    patch=Patch("replace", i, content=re.sub(r'^(#+)\s+', r'\1 ', line))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
