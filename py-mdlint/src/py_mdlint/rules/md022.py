# src/py_mdlint/rules/md022.py
"""MD022: blanks-around-headings — Headings should be surrounded by blank lines."""

from .base import Rule, Violation, Token


class RuleMD022(Rule):
    """
    MD022: blanks-around-headings

    Headings should be surrounded by blank lines (configurable: above/below).
    """

    rule_id = "MD022"
    alias = "blanks-around-headings"
    description = "Headings should be surrounded by blank lines"
    fixable = True

    def check(
        self,
        tokens: list[Token],
        lines: list[str],
        config: dict
    ) -> list[Violation]:
        violations = []
        lines_above = config.get("lines_above", 1)
        lines_below = config.get("lines_below", 1)

        for token in tokens:
            if token.type == "heading_open" and token.line_number <= len(lines):
                heading_line = token.line_number

                if lines_above > 0:
                    for offset in range(1, lines_above + 1):
                        check_line = heading_line - offset
                        if check_line > 0:
                            if lines[check_line - 1].strip() != "":
                                violations.append(Violation(
                                    rule_id=self.rule_id,
                                    line_number=heading_line,
                                    column=1,
                                    message=f"Headings should be surrounded by blank lines [Expected: {lines_above}; Actual: 0; Above]",
                                    fixable=True,
                                    fixed_line=None,
                                    suggestion=f"Ajouter {lines_above} ligne(s) vide(s) avant ce heading"
                                ))
                                break

                if lines_below > 0:
                    for offset in range(1, lines_below + 1):
                        check_line = heading_line + offset
                        if check_line <= len(lines):
                            if lines[check_line - 1].strip() != "":
                                violations.append(Violation(
                                    rule_id=self.rule_id,
                                    line_number=heading_line,
                                    column=1,
                                    message=f"Headings should be surrounded by blank lines [Expected: {lines_below}; Actual: 0; Below]",
                                    fixable=True,
                                    fixed_line=None,
                                    suggestion=f"Ajouter {lines_below} ligne(s) vide(s) après ce heading"
                                ))
                                break

        return violations

    def fix(self, violation: Violation, lines: list[str]) -> str:
        return lines[violation.line_number - 1]
