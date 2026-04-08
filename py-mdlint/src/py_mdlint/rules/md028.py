# src/py_mdlint/rules/md028.py
"""MD028: no-blanks-blockquote — Blank line inside blockquote."""

from .base import Rule, Violation, Token, Patch


class RuleMD028(Rule):
    rule_id = "MD028"
    alias = "no-blanks-blockquote"
    description = "Blank line inside blockquote"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        in_blockquote = False
        bq_start_line = 0
        bq_end_line = 0

        for t in tokens:
            if t.type == "blockquote_open":
                in_blockquote = True
                bq_start_line = t.line_number
            elif t.type == "blockquote_close":
                in_blockquote = False
                bq_end_line = t.line_number

                # Check for blank lines within this blockquote range
                for i in range(bq_start_line, bq_end_line):
                    if i - 1 < len(lines) and i - 1 >= 0:
                        line = lines[i - 1]
                        if line.strip() == "":
                            # Check if this blank line is truly inside the blockquote
                            # (surrounded by blockquote content, not at edges)
                            prev_has_content = False
                            next_has_content = False
                            for j in range(i - 2, bq_start_line - 2, -1):
                                if j >= 0 and j < len(lines):
                                    if lines[j].strip() != "":
                                        prev_has_content = True
                                        break
                            for j in range(i, bq_end_line):
                                if j < len(lines) and lines[j].strip() != "":
                                    next_has_content = True
                                    break
                            if prev_has_content and next_has_content:
                                violations.append(Violation(
                                    self.rule_id, i, 1,
                                    "Blank line inside blockquote", True,
                                    patch=Patch("delete", i)
                                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
