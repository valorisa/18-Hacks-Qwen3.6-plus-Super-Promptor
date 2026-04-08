# src/py_mdlint/rules/md037.py
"""MD037: no-space-in-emphasis — Spaces inside emphasis markers."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD037(Rule):
    rule_id = "MD037"
    alias = "no-space-in-emphasis"
    description = "Spaces inside emphasis markers"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if re.search(r'\*\s[^*]+\s\*|\*\*\s[^*]+\s\*\*|_\s[^_]+\s_|__\s[^_]+\s__', line):
                fixed = self._fix_line(line)
                violations.append(Violation(
                    self.rule_id, i, 1, "Spaces inside emphasis markers", True,
                    patch=Patch("replace", i, content=fixed)
                ))
        return violations

    def _fix_line(self, line: str) -> str:
        line = re.sub(r'(\S)\s+\*\*\s+([^*]+?)\s+\*\*', r'\1**\2**', line)
        line = re.sub(r'(\S)\s+\*\s+([^*]+?)\s+\*', r'\1*\2*', line)
        line = re.sub(r'(\S)\s+__\s+([^_]+?)\s+__', r'\1__\2__', line)
        line = re.sub(r'(\S)\s+_\s+([^_]+?)\s+_', r'\1_\2_', line)
        line = re.sub(r'\*\*\s+([^*]+?)\s+\*\*', r'**\1**', line)
        line = re.sub(r'\*\s+([^*]+?)\s+\*', r'*\1*', line)
        line = re.sub(r'__\s+([^_]+?)\s+__', r'__\1__', line)
        line = re.sub(r'_\s+([^_]+?)\s+_', r'_\1_', line)
        return line

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
