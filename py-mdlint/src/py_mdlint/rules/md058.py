# src/py_mdlint/rules/md058.py
"""MD058: blanks-around-tables — Tables should be surrounded by blank lines."""

from .base import Rule, Violation, Token, Patch


class RuleMD058(Rule):
    rule_id = "MD058"
    alias = "blanks-around-tables"
    description = "Tables should be surrounded by blank lines"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        in_table = False

        for i, line in enumerate(lines, 1):
            is_table_row = "|" in line and not line.strip().startswith(">")
            if is_table_row and not in_table:
                if i > 1 and lines[i - 2].strip() != "":
                    violations.append(Violation(
                        self.rule_id, i, 1,
                        "Missing blank line before table", True,
                        patch=Patch("insert", i, content="")
                    ))
                in_table = True
            elif not is_table_row and in_table:
                in_table = False
                if i <= len(lines) and lines[i - 1].strip() != "":
                    violations.append(Violation(
                        self.rule_id, i, 1,
                        "Missing blank line after table", True,
                        patch=Patch("insert", i, content="")
                    ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
