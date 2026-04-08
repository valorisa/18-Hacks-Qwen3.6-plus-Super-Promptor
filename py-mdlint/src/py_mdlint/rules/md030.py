# src/py_mdlint/rules/md030.py
"""MD030: list-marker-space — Spaces after list markers."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD030(Rule):
    rule_id = "MD030"
    alias = "list-marker-space"
    description = "Spaces after list markers"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        ul_single = config.get("ul_single", 1)
        ol_single = config.get("ol_single", 1)

        for t in tokens:
            if t.type == "list_item_open":
                line = lines[t.line_number - 1]
                ul_match = re.match(r'^(\s*)([\-\*\+])(\s*)', line)
                ol_match = re.match(r'^(\s*)(\d+\.)(\s*)', line)

                if ul_match:
                    spaces = len(ul_match.group(3))
                    if spaces != ul_single:
                        new_line = ul_match.group(1) + ul_match.group(2) + " " * ul_single + line[ul_match.end():]
                        violations.append(Violation(
                            self.rule_id, t.line_number, 1,
                            f"Expected {ul_single} space(s) after marker", True,
                            patch=Patch("replace", t.line_number, content=new_line)
                        ))
                elif ol_match:
                    spaces = len(ol_match.group(3))
                    if spaces != ol_single:
                        new_line = ol_match.group(1) + ol_match.group(2) + " " * ol_single + line[ol_match.end():]
                        violations.append(Violation(
                            self.rule_id, t.line_number, 1,
                            f"Expected {ol_single} space(s) after marker", True,
                            patch=Patch("replace", t.line_number, content=new_line)
                        ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
