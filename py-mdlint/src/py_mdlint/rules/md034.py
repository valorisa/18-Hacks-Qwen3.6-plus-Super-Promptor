# src/py_mdlint/rules/md034.py
"""MD034: no-bare-urls — Bare URL used."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD034(Rule):
    rule_id = "MD034"
    alias = "no-bare-urls"
    description = "Bare URL used"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.search(r'(?<!<)https?://[^\s>)]+(?!>)', line) and not re.search(r'\[.*\]\(.*\)', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "Bare URL detected", True,
                    patch=Patch("replace", i, content=re.sub(r'(https?://[^\s>)]+)', r'<\1>', line))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
