# src/py_mdlint/rules/md046.py
"""MD046: code-block-style — Code block style."""

import re
from .base import Rule, Violation, Token


class RuleMD046(Rule):
    rule_id = "MD046"
    alias = "code-block-style"
    description = "Code block style"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "fenced")

        for i, line in enumerate(lines, 1):
            if style == "fenced" and re.match(r'^    ', line) and not re.match(r'^    \s*$', line):
                violations.append(Violation(
                    self.rule_id, i, 1, "Expected fenced code blocks", True
                ))
            elif style == "indented" and line.strip().startswith("```"):
                violations.append(Violation(
                    self.rule_id, i, 1, "Expected indented code blocks", True
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
