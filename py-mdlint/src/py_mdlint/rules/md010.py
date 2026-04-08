# src/py_mdlint/rules/md010.py
"""MD010: no-hard-tabs — Hard tabs."""

from .base import Rule, Violation, Token, Patch


class RuleMD010(Rule):
    rule_id = "MD010"
    alias = "no-hard-tabs"
    description = "Hard tabs"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        spaces = config.get("spaces_per_tab", 1)

        for i, line in enumerate(lines, 1):
            if "\t" in line:
                col = line.index("\t") + 1
                fixed = line.replace("\t", " " * spaces)
                violations.append(Violation(
                    self.rule_id, i, col, "Hard tab detected", True,
                    patch=Patch("replace", i, content=fixed)
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
