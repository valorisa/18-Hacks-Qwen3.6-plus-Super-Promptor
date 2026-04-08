# src/py_mdlint/rules/md042.py
"""MD042: no-empty-links — No empty links."""

import re
from .base import Rule, Violation, Token


class RuleMD042(Rule):
    rule_id = "MD042"
    alias = "no-empty-links"
    description = "No empty links"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.search(r'\[[^\]]*\]\(\s*\)', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "Empty link"
                ))
            if re.search(r'\[[^\]]*\]\(#\)', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "Empty fragment link"
                ))
        return violations
