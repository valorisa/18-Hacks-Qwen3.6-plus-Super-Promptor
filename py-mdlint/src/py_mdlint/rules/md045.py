# src/py_mdlint/rules/md045.py
"""MD045: no-alt-text — Images should have alternate text (alt text)."""

import re
from .base import Rule, Violation, Token


class RuleMD045(Rule):
    rule_id = "MD045"
    alias = "no-alt-text"
    description = "Images should have alternate text (alt text)"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for t in tokens:
            if t.type == "image" and not t.content.strip():
                violations.append(Violation(
                    self.rule_id, t.line_number, 1,
                    "Image missing alt text"
                ))
        for i, line in enumerate(lines, 1):
            if re.search(r'!\[\s*\]\(', line):
                violations.append(Violation(
                    self.rule_id, i, 1,
                    "Image missing alt text"
                ))
        return violations
