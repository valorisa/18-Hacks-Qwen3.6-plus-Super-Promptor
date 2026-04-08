# src/py_mdlint/rules/md023.py
"""MD023: heading-start-left — Headings must start at the beginning of the line."""

from .base import Rule, Violation, Token, Patch


class RuleMD023(Rule):
    rule_id = "MD023"
    alias = "heading-start-left"
    description = "Headings must start at the beginning of the line"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        for t in tokens:
            if t.type == "heading_open":
                line = lines[t.line_number - 1]
                if line.startswith(" "):
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        "Heading has leading spaces", True,
                        patch=Patch("replace", t.line_number, content=line.lstrip())
                    ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
