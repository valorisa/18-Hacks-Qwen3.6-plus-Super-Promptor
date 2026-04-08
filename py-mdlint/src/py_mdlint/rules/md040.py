# src/py_mdlint/rules/md040.py
"""MD040: fenced-code-language — Fenced code blocks should have a language specified."""

from .base import Rule, Violation, Token


class RuleMD040(Rule):
    rule_id = "MD040"
    alias = "fenced-code-language"
    description = "Fenced code blocks should have a language specified"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        allowed = config.get("allowed_languages", [])

        for t in tokens:
            if t.type == "fence":
                info = t.meta.get("info", "").strip() if t.meta else ""
                if not info:
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        "Fenced code block missing language"
                    ))
                elif allowed and info.split()[0] not in allowed:
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        f"Language '{info}' not in allowed list"
                    ))
        return violations
