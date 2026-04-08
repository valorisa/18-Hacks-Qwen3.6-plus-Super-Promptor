# src/py_mdlint/rules/md024.py
"""MD024: no-duplicate-heading — Multiple headings with the same content."""

from .base import Rule, Violation, Token


class RuleMD024(Rule):
    rule_id = "MD024"
    alias = "no-duplicate-heading"
    description = "Multiple headings with the same content"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        seen: dict[str, int] = {}
        siblings_only = config.get("siblings_only", False)
        current_level = 0

        for t in tokens:
            if t.type == "heading_open":
                current_level = int(t.tag[1]) if t.tag.startswith("h") and len(t.tag) > 1 else 0
            elif t.type == "inline":
                content = t.content.strip()
                if not content:
                    continue
                key = f"{current_level}:{content}" if siblings_only else content

                if key in seen:
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        f"Duplicate heading: \"{content}\""
                    ))
                else:
                    seen[key] = t.line_number
        return violations
