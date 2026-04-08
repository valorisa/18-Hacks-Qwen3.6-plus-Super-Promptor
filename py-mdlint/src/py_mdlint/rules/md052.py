# src/py_mdlint/rules/md052.py
"""MD052: reference-links-images — Reference links and images should use a label that is defined."""

import re
from .base import Rule, Violation, Token


class RuleMD052(Rule):
    rule_id = "MD052"
    alias = "reference-links-images"
    description = "Reference links and images should use a label that is defined"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        defs: set[str] = set()
        refs: list[tuple[int, str]] = []

        for i, line in enumerate(lines, 1):
            def_match = re.match(r'^\s*\[([^\]]+)\]:\s', line)
            if def_match:
                defs.add(def_match.group(1).lower())

            ref_match = re.findall(r'\[([^\]]+)\](?!\(|:)', line)
            for ref in ref_match:
                refs.append((i, ref))

        for line_num, ref in refs:
            if ref.lower() not in defs:
                violations.append(Violation(
                    self.rule_id, line_num, 1,
                    f"Missing definition for reference: [{ref}]"
                ))
        return violations
