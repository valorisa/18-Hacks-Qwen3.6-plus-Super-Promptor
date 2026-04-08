# src/py_mdlint/rules/md004.py
"""MD004: ul-style — Unordered list style."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD004(Rule):
    rule_id = "MD004"
    alias = "ul-style"
    description = "Unordered list style"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "consistent")
        markers = {"asterisk": "*", "plus": "+", "dash": "-"}
        expected = markers.get(style)
        first_marker = None

        for t in tokens:
            if t.type == "bullet_list_open":
                line = lines[t.line_number - 1].lstrip()
                marker = line[0]
                if first_marker is None:
                    first_marker = marker
                target = expected or first_marker
                if marker != target:
                    new_line = line.replace(marker, target, 1)
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        f"Expected {target}; Actual {marker}", True,
                        patch=Patch("replace", t.line_number, content=new_line)
                    ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
