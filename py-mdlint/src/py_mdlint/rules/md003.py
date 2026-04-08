# src/py_mdlint/rules/md003.py
"""MD003: heading-style — Heading style should be consistent."""

import re
from .base import Rule, Violation, Token, Patch


class RuleMD003(Rule):
    rule_id = "MD003"
    alias = "heading-style"
    description = "Heading style should be consistent"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        style_param = config.get("style", "atx")
        dominant_style = self._detect_dominant_style(tokens, lines) if style_param == "consistent" else style_param

        for i, t in enumerate(tokens):
            if t.type == "heading_open":
                (actual_style, actual_level) = self._get_heading_style(t, lines)
                if actual_style and actual_style != dominant_style:
                    content = self._get_heading_content(tokens, i, lines)
                    tag = f"h{actual_level}"
                    fixed_line = self._convert_heading_style(
                        lines[t.line_number - 1], actual_style, dominant_style, tag, content
                    )
                    violations.append(Violation(
                        self.rule_id, t.line_number, 1,
                        f"Heading style [Expected: {dominant_style}; Actual: {actual_style}]", True,
                        patch=Patch("replace", t.line_number, content=fixed_line)
                    ))
        return violations

    def _get_heading_content(self, tokens: list[Token], heading_idx: int, lines: list[str]) -> str:
        heading_token = tokens[heading_idx]
        token_line = heading_token.line_number - 1
        
        if heading_token.tag == "h1" and token_line < len(lines):
            line = lines[token_line]
            if line.strip().startswith("#"):
                parts = line.lstrip("#").strip()
                if parts:
                    return parts
        
        if token_line > 0:
            prev_line = lines[token_line - 1].strip()
            if not prev_line.startswith("#") and prev_line and not prev_line.startswith("=") and not prev_line.startswith("-"):
                return prev_line
        
        for j in range(heading_idx + 1, len(tokens)):
            if tokens[j].type == "inline" and tokens[j].content.strip():
                return tokens[j].content.strip()
        
        for j in range(heading_idx - 1, -1, -1):
            if tokens[j].type == "inline" and tokens[j].content.strip():
                return tokens[j].content.strip()
        
        return lines[token_line].strip() if token_line < len(lines) else ""

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]

    def _get_heading_style(self, token: Token, lines: list[str]) -> tuple[str | None, int]:
        if token.line_number <= len(lines):
            line = lines[token.line_number - 1].strip()
            if line.startswith("#"):
                level = line.count("#")
                return ("atx", level)
            if token.line_number < len(lines):
                next_line = lines[token.line_number].strip()
                if re.match(r'^={3,}$', next_line):
                    return ("setext", 2)
                if re.match(r'^-{3,}$', next_line):
                    return ("setext", 1)
        return (None, 1)

    def _detect_dominant_style(self, tokens: list[Token], lines: list[str]) -> str:
        atx_count = 0
        setext_count = 0
        for t in tokens:
            if t.type == "heading_open":
                (style, _) = self._get_heading_style(t, lines)
                if style == "atx":
                    atx_count += 1
                elif style == "setext":
                    setext_count += 1
        return "atx" if atx_count >= setext_count else "setext"

    def _convert_heading_style(self, line: str, from_style: str, to_style: str, tag: str, content: str) -> str:
        if from_style == to_style:
            return line
        if to_style == "atx":
            hashes = "#" if tag == "h1" else "##"
            return f"{hashes} {content}"
        if to_style == "setext":
            underline = "=" if tag == "h1" else "-"
            return f"{content}\n{underline * len(content)}"
        return line
