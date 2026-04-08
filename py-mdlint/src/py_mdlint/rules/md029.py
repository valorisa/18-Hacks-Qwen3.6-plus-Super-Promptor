# src/py_mdlint/rules/md029.py
"""MD029: ol-prefix — Ordered list item prefix."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD029(Rule):
    rule_id = "MD029"
    alias = "ol-prefix"
    description = "Ordered list item prefix"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style = config.get("style", "one_or_ordered")
        count = 0

        for t in tokens:
            if t.type == "list_item_open":
                line = lines[t.line_number - 1].strip()
                match = re.match(r'^(\d+)\.', line)
                if match:
                    actual = int(match.group(1))
                    count += 1

                    if style == "one" and actual != 1:
                        violations.append(Violation(
                            self.rule_id, t.line_number, 1,
                            f"Expected 1.; Actual {actual}.", True,
                            patch=Patch("replace", t.line_number, content=f"1. {line[match.end():]}")
                        ))
                    elif style == "ordered" and actual != count:
                        violations.append(Violation(
                            self.rule_id, t.line_number, 1,
                            f"Expected {count}.; Actual {actual}.", True,
                            patch=Patch("replace", t.line_number, content=f"{count}. {line[match.end():]}")
                        ))
                    elif style == "zero" and actual != 0:
                        violations.append(Violation(
                            self.rule_id, t.line_number, 1,
                            f"Expected 0.; Actual {actual}.", True,
                            patch=Patch("replace", t.line_number, content=f"0. {line[match.end():]}")
                        ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
