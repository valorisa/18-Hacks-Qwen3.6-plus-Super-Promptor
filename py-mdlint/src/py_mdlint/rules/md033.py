# src/py_mdlint/rules/md033.py
"""MD033: no-inline-html — Inline HTML should be avoided or restricted."""

import re
from .base import Rule, Violation, Token


class RuleMD033(Rule):
    rule_id = "MD033"
    alias = "no-inline-html"
    description = "Inline HTML should be avoided or restricted"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        allowed_elements = set(e.lower() for e in config.get("allowed_elements", []))
        html_pattern = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9\-]*)(?:\s[^>]*)?\s*/?>')

        found_tags = set()

        for t in tokens:
            if t.type == "html_inline" or t.type == "html_block":
                content = t.content.strip()
                match = html_pattern.match(content)
                if match:
                    tag_name = match.group(2).lower()
                    if tag_name not in allowed_elements and tag_name not in found_tags:
                        found_tags.add(tag_name)
                        violations.append(Violation(
                            self.rule_id, t.line_number, 1,
                            f"Inline HTML [Element: {tag_name}]"
                        ))

        for i, line in enumerate(lines, 1):
            if "<" in line and ">" in line:
                for match in html_pattern.finditer(line):
                    tag_name = match.group(2).lower()
                    if tag_name not in allowed_elements and tag_name not in found_tags:
                        found_tags.add(tag_name)
                        violations.append(Violation(
                            self.rule_id, i, 1,
                            f"Inline HTML [Element: {tag_name}]"
                        ))
        return violations
