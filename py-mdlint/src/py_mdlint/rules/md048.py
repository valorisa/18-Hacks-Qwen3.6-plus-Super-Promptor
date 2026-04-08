# src/py_mdlint/rules/md048.py
"""MD048: code-fence-style — Code fence style."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD048(Rule):
    rule_id = "MD048"
    alias = "code-fence-style"
    description = "Code fence style"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "backtick")

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("~~~") and style == "backtick":
                violations.append(Violation(
                    self.rule_id, i, 1, "Expected ```", True,
                    patch=Patch("replace", i, content=stripped.replace("~~~", "```"))
                ))
            elif stripped.startswith("```") and style == "tilde":
                violations.append(Violation(
                    self.rule_id, i, 1, "Expected ~~~", True,
                    patch=Patch("replace", i, content=stripped.replace("```", "~~~"))
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
