# src/py_mdlint/rules/md027.py
"""MD027: no-multiple-space-blockquote — Multiple spaces after blockquote symbol."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD027(Rule):
    rule_id = "MD027"
    alias = "no-multiple-space-blockquote"
    description = "Multiple spaces after blockquote symbol"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^>\s{2,}', line):
                violations.append(Violation(
                    self.rule_id, i, 2, "Multiple spaces after >", True,
                    patch=Patch("replace", i, content=re.sub(r'^(>\s+)', '> ', line))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
