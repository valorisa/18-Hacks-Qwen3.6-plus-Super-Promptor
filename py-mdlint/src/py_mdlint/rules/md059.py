# src/py_mdlint/rules/md059.py
"""MD059: descriptive-link-text — Link text should be descriptive."""

import re
from .base import Rule, Violation, Token


class RuleMD059(Rule):
    rule_id = "MD059"
    alias = "descriptive-link-text"
    description = "Link text should be descriptive"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            matches = re.findall(r'\[([^\]]*)\]\([^)]+\)', line)
            for text in matches:
                text = text.strip()
                if not text or text.lower() in ("click here", "here", "link", "read more", "more"):
                    violations.append(Violation(
                        self.rule_id, i, 1,
                        f"Non-descriptive link text: '{text}'"
                    ))
        return violations
