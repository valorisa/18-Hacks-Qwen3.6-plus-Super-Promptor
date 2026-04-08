# src/py_mdlint/rules/md051.py
"""MD051: link-fragments — Link fragments should be valid."""

import re
from .base import Rule, Violation, Token


class RuleMD051(Rule):
    rule_id = "MD051"
    alias = "link-fragments"
    description = "Link fragments should be valid"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        headings = {}
        for i, t in enumerate(tokens):
            if t.type == "heading_open":
                content = ""
                for j in range(i + 1, len(tokens)):
                    if tokens[j].type == "inline":
                        content = tokens[j].content.strip()
                        break
                anchor = content.lower().strip().replace(" ", "-")
                headings[anchor] = t.line_number

        link_pattern = re.compile(r'\[([^\]]*)\]\(#([^)]+)\)')
        for i, line in enumerate(lines, 1):
            for match in link_pattern.finditer(line):
                link_text = match.group(1)
                fragment = match.group(2)
                if fragment not in headings:
                    violations.append(Violation(
                        self.rule_id, i, 1,
                        f"Invalid link fragment: #{fragment}"
                    ))
        return violations
