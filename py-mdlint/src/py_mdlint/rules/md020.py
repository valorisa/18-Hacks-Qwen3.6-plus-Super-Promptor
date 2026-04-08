# src/py_mdlint/rules/md020.py
"""MD020: no-missing-space-closed-atx — No space inside hashes on closed atx style heading."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD020(Rule):
    rule_id = "MD020"
    alias = "no-missing-space-closed-atx"
    description = "No space inside hashes on closed atx style heading"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^#+\S.*#+\s*$', line) and not re.match(r'^#+\s', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "No space after opening #", True,
                    patch=Patch("replace", i, content=re.sub(r'^(#+)(\S)', r'\1 \2', line))
                ))
            elif re.match(r'^#+\s.*[^#\s]#+$', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "No space before closing #", True,
                    patch=Patch("replace", i, content=re.sub(r'(\S)(#+)$', r'\1 \2', line))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
