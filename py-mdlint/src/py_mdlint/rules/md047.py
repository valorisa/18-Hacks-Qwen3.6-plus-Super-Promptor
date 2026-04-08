# src/py_mdlint/rules/md047.py
"""MD047: single-trailing-newline — Files should end with a single newline character."""

from .base import Rule, Violation, Token


class RuleMD047(Rule):
    """
    MD047: single-trailing-newline

    Files should end with exactly one newline character.
    """

    rule_id = "MD047"
    alias = "single-trailing-newline"
    description = "Files should end with a single newline character"
    fixable = True

    def check(
        self,
        tokens: list[Token],
        lines: list[str],
        config: dict
    ) -> list[Violation]:
        violations = []

        if not lines:
            violations.append(Violation(
                rule_id=self.rule_id,
                line_number=1,
                column=1,
                message="Files should end with a single newline character [Expected: 1; Actual: 0]",
                fixable=True,
                fixed_line="\n",
                suggestion="Ajouter un saut de ligne à la fin du fichier"
            ))
            return violations

        last_line = lines[-1]

        if not last_line.endswith('\n'):
            violations.append(Violation(
                rule_id=self.rule_id,
                line_number=len(lines),
                column=len(last_line) + 1,
                message="Files should end with a single newline character [Expected: 1; Actual: 0]",
                fixable=True,
                fixed_line=None,
                suggestion="Ajouter un saut de ligne à la fin du fichier"
            ))
        elif last_line.endswith('\n\n'):
            trailing_newlines = len(last_line) - len(last_line.rstrip('\n'))
            violations.append(Violation(
                rule_id=self.rule_id,
                line_number=len(lines),
                column=1,
                message=f"Files should end with a single newline character [Expected: 1; Actual: {trailing_newlines}]",
                fixable=True,
                fixed_line=None,
                suggestion="Conserver un seul saut de ligne à la fin du fichier"
            ))

        return violations

    def fix(self, violation: Violation, lines: list[str]) -> str:
        if violation.fixed_line is not None:
            return violation.fixed_line
        return lines[violation.line_number - 1]
