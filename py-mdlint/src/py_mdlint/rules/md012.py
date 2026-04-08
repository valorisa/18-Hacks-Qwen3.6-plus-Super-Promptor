# src/py_mdlint/rules/md012.py
"""MD012: no-multiple-blanks — Multiple consecutive blank lines."""

from .base import Rule, Violation, Token, Patch


class RuleMD012(Rule):
    rule_id = "MD012"
    alias = "no-multiple-blanks"
    description = "Multiple consecutive blank lines"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        max_consecutive = config.get("maximum", 1)
        blank_count = 0
        start_line = 0

        for idx, line in enumerate(lines, start=1):
            is_blank = line.strip() == ""
            if is_blank:
                if blank_count == 0:
                    start_line = idx
                blank_count += 1
                if blank_count > max_consecutive:
                    violations.append(Violation(
                        self.rule_id, idx, 1,
                        f"Multiple consecutive blank lines [Expected: {max_consecutive}; Actual: {blank_count}]",
                        True, patch=Patch("delete", idx)
                    ))
            else:
                blank_count = 0
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
