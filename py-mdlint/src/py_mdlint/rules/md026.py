# src/py_mdlint/rules/md026.py
"""MD026: no-trailing-punctuation — Trailing punctuation in heading."""

from .base import Rule, Violation, Token, Patch


class RuleMD026(Rule):
    rule_id = "MD026"
    alias = "no-trailing-punctuation"
    description = "Trailing punctuation in heading"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        punct = config.get("punctuation", ".,;:!")

        for t in tokens:
            if t.type == "inline":
                # Check if previous token was heading_open
                idx = tokens.index(t)
                if idx > 0 and tokens[idx - 1].type == "heading_open":
                    content = t.content.strip()
                    if content and content[-1] in punct:
                        violations.append(Violation(
                            self.rule_id, t.line_number, 1,
                            f"Trailing punctuation in heading: '{content[-1]}'", True,
                            patch=Patch("replace", t.line_number, content=content[:-1])
                        ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
