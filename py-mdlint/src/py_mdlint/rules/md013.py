# src/py_mdlint/rules/md013.py
"""MD013: line-length — Line length."""

from .base import Rule, Violation, Token


class RuleMD013(Rule):
    rule_id = "MD013"
    alias = "line-length"
    description = "Line length"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        limit = config.get("line_length", 80)
        if limit == 0:
            return violations

        skip_code = config.get("code_blocks", True)
        skip_tables = config.get("tables", True)
        skip_headings = config.get("headings", True)
        strict = config.get("strict", False)

        in_code = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code = not in_code

            if len(line) > limit:
                if in_code and skip_code:
                    continue
                if "|" in line and skip_tables:
                    continue
                if stripped.startswith("#") and skip_headings:
                    continue

                has_space_beyond = len(line) > limit and " " in line[limit:]
                if not strict and not has_space_beyond:
                    continue

                violations.append(Violation(
                    self.rule_id, i, limit + 1,
                    f"Line length {len(line)} > {limit}"
                ))
        return violations
