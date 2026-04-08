# src/py_mdlint/rules/md035.py
"""MD035: hr-style — Horizontal rule style."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD035(Rule):
    rule_id = "MD035"
    alias = "hr-style"
    description = "Horizontal rule style"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "consistent")
        first_hr = None

        for i, line in enumerate(lines, 1):
            if re.match(r'^\s*[-*_]{3,}\s*$', line):
                stripped = line.strip()
                if first_hr is None:
                    first_hr = stripped
                    if style == "consistent":
                        continue
                    target = style
                else:
                    target = style if style != "consistent" else first_hr

                if stripped != target:
                    violations.append(Violation(
                        self.rule_id, i, 1,
                        f"Expected {target}; Actual {stripped}", True,
                        patch=Patch("replace", i, content=target)
                    ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
