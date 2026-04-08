# src/py_mdlint/rules/md044.py
"""MD044: proper-names — Proper names should have the correct capitalization."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD044(Rule):
    rule_id = "MD044"
    alias = "proper-names"
    description = "Proper names should have the correct capitalization"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        names = config.get("names", [])
        code_blocks = config.get("code_blocks", True)
        html_elements = config.get("html_elements", True)

        in_code = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code = not in_code

            for name in names:
                pattern = re.compile(r'\b' + re.escape(name) + r'\b', re.IGNORECASE)
                for match in pattern.finditer(line):
                    if match.group() != name:
                        if in_code and not code_blocks:
                            continue
                        violations.append(Violation(
                            self.rule_id, i, match.start() + 1,
                            f"Incorrect capitalization: '{match.group()}' (expected '{name}')", True,
                            patch=Patch("replace", i, content=pattern.sub(name, line))
                        ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
