# src/py_mdlint/rules/md009.py
"""MD009: no-trailing-spaces — Trailing whitespace at end of line."""

import re
from .base import Rule, Violation, Token


class RuleMD009(Rule):
    """
    MD009: no-trailing-spaces

    Lines should not have trailing whitespace.
    Exception: spaces before <br> or when br_spaces > 0.
    """

    rule_id = "MD009"
    alias = "no-trailing-spaces"
    description = "Trailing spaces at end of line"
    fixable = True

    def check(
        self,
        tokens: list[Token],
        lines: list[str],
        config: dict
    ) -> list[Violation]:
        violations = []
        br_spaces = config.get("br_spaces", 0)

        for idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            match = re.search(r'([ \t]+)$', line)
            if match:
                trailing = match.group(1)

                if br_spaces > 0 and len(trailing) == br_spaces:
                    if idx < len(lines) and lines[idx].strip().startswith("<br"):
                        continue

                violations.append(Violation(
                    rule_id=self.rule_id,
                    line_number=idx,
                    column=len(line) - len(trailing) + 1,
                    message=f"Trailing spaces [Expected: 0 or {br_spaces}; Actual: {len(trailing)}]",
                    fixable=True,
                    fixed_line=line.rstrip(),
                    suggestion="Supprimer les espaces en fin de ligne"
                ))

        return violations

    def fix(self, violation: Violation, lines: list[str]) -> str:
        if violation.fixed_line is not None:
            return violation.fixed_line
        return lines[violation.line_number - 1].rstrip()
