# src/py_mdlint/rules/md011.py
"""MD011: no-reversed-links — Reversed link syntax."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD011(Rule):
    rule_id = "MD011"
    alias = "no-reversed-links"
    description = "Reversed link syntax"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        pattern = re.compile(r'\(([^)]+)\)\[([^\]]+)\]')

        for i, line in enumerate(lines, 1):
            match = pattern.search(line)
            if match:
                url = match.group(1)
                text = match.group(2)
                fixed_line = line[:match.start()] + f'[{text}]({url})' + line[match.end():]
                violations.append(Violation(
                    self.rule_id, i, match.start() + 1,
                    "Reversed link syntax", True,
                    patch=Patch("replace", i, content=fixed_line)
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
