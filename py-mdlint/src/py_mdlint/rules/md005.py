# src/py_mdlint/rules/md005.py
"""MD005: list-indent — Inconsistent indentation for list items at the same level."""

from .base import Rule, Violation, Token


class RuleMD005(Rule):
    rule_id = "MD005"
    alias = "list-indent"
    description = "Inconsistent indentation for list items at the same level"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        list_indents: dict[int, int] = {}
        current_list_level = 0

        for t in tokens:
            if t.type == "bullet_list_open":
                current_list_level += 1
                indent = len(lines[t.line_number - 1]) - len(lines[t.line_number - 1].lstrip())
                list_indents[current_list_level] = indent
            elif t.type == "bullet_list_close":
                current_list_level = max(0, current_list_level - 1)
            elif t.type == "ordered_list_open":
                current_list_level += 1
                indent = len(lines[t.line_number - 1]) - len(lines[t.line_number - 1].lstrip())
                list_indents[current_list_level] = indent
            elif t.type == "ordered_list_close":
                current_list_level = max(0, current_list_level - 1)
            elif t.type == "list_item_open":
                indent = len(lines[t.line_number - 1]) - len(lines[t.line_number - 1].lstrip())
                expected = list_indents.get(current_list_level, 0)
                if current_list_level > 0 and indent != expected:
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        "Inconsistent list indentation", True
                    ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
