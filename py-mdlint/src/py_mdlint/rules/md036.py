# src/py_mdlint/rules/md036.py
"""MD036: no-emphasis-as-heading — Emphasis used instead of a heading."""

import re
from .base import Rule, Violation, Token


class RuleMD036(Rule):
    rule_id = "MD036"
    alias = "no-emphasis-as-heading"
    description = "Emphasis used instead of a heading"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        punct = config.get("punctuation", ".,;:!?")

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if re.match(r'^\*\*[^*]+\*\*\s*$', stripped) or re.match(r'__[^_]+__\s*$', stripped):
                if not any(stripped.endswith(p) for p in punct):
                    violations.append(Violation(
                        self.rule_id, i, 1, "Emphasis used instead of a heading"
                    ))
            elif re.match(r'^\*[^*]+\*\s*$', stripped) or re.match(r'_[^_]+_\s*$', stripped):
                if not any(stripped.endswith(p) for p in punct):
                    violations.append(Violation(
                        self.rule_id, i, 1, "Emphasis used instead of a heading"
                    ))
        return violations
