# src/py_mdlint/rules/md054.py
"""MD054: link-image-style — Link and image style."""

import re
from .base import Rule, Violation, Token


class RuleMD054(Rule):
    rule_id = "MD054"
    alias = "link-image-style"
    description = "Link and image style"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        autolink = config.get("autolink", True)
        full = config.get("full", True)
        collapsed = config.get("collapsed", True)
        shortcut = config.get("shortcut", True)
        inline = config.get("inline", True)

        for i, line in enumerate(lines, 1):
            if re.search(r'<https?://[^>]+>', line) and not autolink:
                violations.append(Violation(self.rule_id, i, 1, "Autolink detected"))
            if re.search(r'\[[^\]]+\]\[[^\]]+\]', line) and not full:
                violations.append(Violation(self.rule_id, i, 1, "Full reference link detected"))
        return violations
