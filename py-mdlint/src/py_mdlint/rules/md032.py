# src/py_mdlint/rules/md032.py
"""MD032: blanks-around-lists — Lists should be surrounded by blank lines."""

import re
from .base import Rule, Violation, Token


class RuleMD032(Rule):
    """
    MD032: blanks-around-lists

    Lists should be surrounded by blank lines.
    """

    rule_id = "MD032"
    alias = "blanks-around-lists"
    description = "Lists should be surrounded by blank lines"
    fixable = True

    def check(
        self,
        tokens: list[Token],
        lines: list[str],
        config: dict
    ) -> list[Violation]:
        violations = []

        list_starts = []
        list_ends = []

        for idx, token in enumerate(tokens):
            if token.type in ("bullet_list_open", "ordered_list_open"):
                list_starts.append((token.line_number, idx))
            elif token.type in ("bullet_list_close", "ordered_list_close"):
                list_ends.append((token.line_number, idx))

        for start_line, start_idx in list_starts:
            if start_line > 1:
                prev_line_content = lines[start_line - 2].strip() if start_line - 2 < len(lines) else ""
                if prev_line_content and not self._is_list_marker(prev_line_content):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        line_number=start_line,
                        column=1,
                        message="Lists should be surrounded by blank lines [Expected: 1; Actual: 0; Above]",
                        fixable=True,
                        fixed_line=None,
                        suggestion="Ajouter une ligne vide avant cette liste"
                    ))

        for end_line, end_idx in list_ends:
            if end_line < len(lines):
                next_line_content = lines[end_line].strip() if end_line < len(lines) else ""
                if next_line_content and not self._is_list_marker(next_line_content):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        line_number=end_line,
                        column=1,
                        message="Lists should be surrounded by blank lines [Expected: 1; Actual: 0; Below]",
                        fixable=True,
                        fixed_line=None,
                        suggestion="Ajouter une ligne vide après cette liste"
                    ))

        return violations

    def _is_list_marker(self, line: str) -> bool:
        return bool(re.match(r'^[\s]*[\-\*\+]\s|^[\s]*\d+\.\s', line))

    def fix(self, violation: Violation, lines: list[str]) -> str:
        return lines[violation.line_number - 1]
