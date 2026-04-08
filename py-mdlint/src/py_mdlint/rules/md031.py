# src/py_mdlint/rules/md031.py
"""MD031: blanks-around-fences — Fenced code blocks should be surrounded by blank lines."""

from .base import Rule, Violation, Token


class RuleMD031(Rule):
    rule_id = "MD031"
    alias = "blanks-around-fences"
    description = "Fenced code blocks should be surrounded by blank lines"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        check_list_items = config.get("list_items", True)

        for idx, token in enumerate(tokens):
            if token.type == "fence":
                fence_line = token.line_number

                # Check line before (skip if start of doc)
                if fence_line > 1:
                    prev_line = lines[fence_line - 2].strip() if fence_line - 2 < len(lines) else ""
                    if prev_line and not prev_line.startswith("```") and not prev_line.startswith("~~~"):
                        in_list = self._is_in_list(tokens, idx, lines, fence_line)
                        if not in_list or check_list_items:
                            violations.append(Violation(
                                self.rule_id, fence_line, 1,
                                "Fenced code blocks should be surrounded by blank lines [Context: \"```\"]",
                                fixable=True,
                                suggestion="Ajouter une ligne vide avant ce bloc de code"
                            ))

                # Check line after fence (look for fence_close)
                for j in range(idx + 1, len(tokens)):
                    next_token = tokens[j]
                    if next_token.type == "fence_close":
                        close_line = next_token.line_number
                        if close_line < len(lines):
                            next_line = lines[close_line].strip() if close_line < len(lines) else ""
                            if next_line:
                                violations.append(Violation(
                                    self.rule_id, fence_line, 1,
                                    "Fenced code blocks should be surrounded by blank lines [Context: \"```\"]",
                                    fixable=True,
                                    suggestion="Ajouter une ligne vide après ce bloc de code"
                                ))
                        break
                    if next_token.type == "fence":
                        break

        return violations

    def _is_in_list(self, tokens: list[Token], fence_idx: int, lines: list[str], fence_line: int) -> bool:
        if fence_line - 1 < len(lines):
            line = lines[fence_line - 1]
            indent = len(line) - len(line.lstrip())
            return indent >= 2
        return False

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
