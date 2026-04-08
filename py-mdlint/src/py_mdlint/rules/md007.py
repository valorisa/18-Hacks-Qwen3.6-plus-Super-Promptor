# src/py_mdlint/rules/md007.py
"""MD007: ul-indent — Unordered list indentation."""

from .base import Rule, Violation, Token


class RuleMD007(Rule):
    rule_id = "MD007"
    alias = "ul-indent"
    description = "Unordered list indentation"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        indent = config.get("indent", 2)

        for t in tokens:
            if t.type == "bullet_list_open" and t.line_number > 1:
                curr = len(lines[t.line_number - 1]) - len(lines[t.line_number - 1].lstrip())
                if curr > 0 and curr % indent != 0:
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        f"Expected indent multiple of {indent}", True
                    ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
