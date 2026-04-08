# src/py_mdlint/rules/md021.py
"""MD021: no-multiple-space-closed-atx — Multiple spaces inside hashes on closed atx style heading."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD021(Rule):
    rule_id = "MD021"
    alias = "no-multiple-space-closed-atx"
    description = "Multiple spaces inside hashes on closed atx style heading"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^#+\s{2,}', line) or re.match(r'^#+\s.+\s{2,}#+$', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "Multiple spaces inside closed atx heading", True,
                    patch=Patch("replace", i, content=re.sub(r'\s+(#+)$', ' #', re.sub(r'^(#+)\s+', r'\1 ', line)))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
