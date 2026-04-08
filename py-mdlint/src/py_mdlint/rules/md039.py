# src/py_mdlint/rules/md039.py
"""MD039: no-space-in-links — Spaces inside link text."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD039(Rule):
    rule_id = "MD039"
    alias = "no-space-in-links"
    description = "Spaces inside link text"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.search(r'\[\s+[^\]]+\s+\]', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "Spaces inside link text", True,
                    patch=Patch("replace", i, content=re.sub(r'\[\s+', '[', re.sub(r'\s+\]', ']', line)))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
