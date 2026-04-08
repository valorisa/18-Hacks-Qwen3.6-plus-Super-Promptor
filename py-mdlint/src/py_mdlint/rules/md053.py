# src/py_mdlint/rules/md053.py
"""MD053: link-image-reference-definitions — Link and image reference definitions should be needed."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD053(Rule):
    rule_id = "MD053"
    alias = "link-image-reference-definitions"
    description = "Link and image reference definitions should be needed"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        defs: dict[str, int] = {}
        refs: set[str] = set()

        for i, line in enumerate(lines, 1):
            def_match = re.match(r'^\s*\[([^\]]+)\]:\s', line)
            if def_match:
                defs[def_match.group(1).lower()] = i

            ref_match = re.findall(r'\[([^\]]+)\](?!\(|:)', line)
            for ref in ref_match:
                refs.add(ref.lower())

        for label, line_num in defs.items():
            if label not in refs:
                violations.append(Violation(
                    self.rule_id, line_num, 1,
                    f"Unused reference definition: [{label}]", True,
                    patch=Patch("delete", line_num)
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
