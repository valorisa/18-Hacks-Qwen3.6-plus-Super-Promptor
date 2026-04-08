# src/py_mdlint/rules/md041.py
"""MD041: first-line-h1 — First line in file should be a top-level heading."""

from .base import Rule, Violation, Token


class RuleMD041(Rule):
    rule_id = "MD041"
    alias = "first-line-h1"
    description = "First line in file should be a top-level heading"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        allow_preamble = config.get("allow_preamble", False)
        level = config.get("level", 1)

        if not lines:
            return violations

        first_line = lines[0].strip()
        is_first_h1 = first_line.startswith("#") and first_line.lstrip("#").startswith((" ", ""))

        if not is_first_h1:
            if not allow_preamble:
                violations.append(Violation(
                    self.rule_id, 1, 1,
                    "First line should be a top-level heading"
                ))
        else:
            h1s = [t for t in tokens if t.type == "heading_open" and t.tag == f"h{level}"]
            if h1s and h1s[0].line_number > 1 and not allow_preamble:
                violations.append(Violation(
                    self.rule_id, 1, 1,
                    f"First heading is at line {h1s[0].line_number}, expected at line 1"
                ))
        return violations
