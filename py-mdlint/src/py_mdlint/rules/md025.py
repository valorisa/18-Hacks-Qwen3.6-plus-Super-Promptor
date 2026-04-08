# src/py_mdlint/rules/md025.py
"""MD025: single-title — Multiple top-level headings in the same document."""

import re
from .base import Rule, Violation, Token


class RuleMD025(Rule):
    """
    MD025: single-title

    Documents should have exactly one top-level heading (h1 / #).
    Front-matter titles can be excluded via config.
    """

    rule_id = "MD025"
    alias = "single-title"
    description = "Multiple top-level headings in the same document"
    fixable = False

    def check(
        self,
        tokens: list[Token],
        lines: list[str],
        config: dict
    ) -> list[Violation]:
        violations = []
        title_level = config.get("level", 1)
        front_matter_pattern = config.get("front_matter_title", r"^\s*title\s*[:=]")

        h1_tokens = [t for t in tokens if t.type == "heading_open" and t.tag == f"h{title_level}"]

        if len(h1_tokens) > 1:
            in_front_matter = False
            front_matter_end = 0

            if lines and lines[0].strip() == "---":
                for idx, line in enumerate(lines[1:], start=2):
                    if line.strip() == "---":
                        front_matter_end = idx
                        in_front_matter = True
                        break

            content_h1s = [
                t for t in h1_tokens
                if not (in_front_matter and t.line_number <= front_matter_end)
            ]

            if len(content_h1s) > 1:
                for token in content_h1s[1:]:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        line_number=token.line_number,
                        column=1,
                        message=f"Multiple top-level headings in the same document [Context: \"{token.content.strip()[:50]}...\"]",
                        fixable=False,
                        suggestion="Conserver un seul titre principal (h1) ou utiliser des sous-titres (h2+)"
                    ))

        return violations
