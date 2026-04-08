# src/py_mdlint/rules/md056.py
"""MD056: table-column-count — Table column count."""

from .base import Rule, Violation, Token


class RuleMD056(Rule):
    rule_id = "MD056"
    alias = "table-column-count"
    description = "Table column count"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        headers = None

        for i, line in enumerate(lines, 1):
            if "|" not in line:
                continue
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue

            cols = len(stripped.split("|")) - 2
            if cols < 0:
                continue

            if headers is None:
                headers = cols
            elif "--" not in stripped:
                if cols != headers:
                    violations.append(Violation(
                        self.rule_id, i, 1,
                        f"Expected {headers} columns, got {cols}", True
                    ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
