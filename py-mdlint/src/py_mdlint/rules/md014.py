# src/py_mdlint/rules/md014.py
"""MD014: commands-show-output — Dollar signs used before commands without showing output."""

from .base import Rule, Violation, Token, Patch


class RuleMD014(Rule):
    rule_id = "MD014"
    alias = "commands-show-output"
    description = "Dollar signs used before commands without showing output"
    fixable = True

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        in_code = False
        code_start = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("```"):
                if not in_code:
                    in_code = True
                    code_start = i
                else:
                    in_code = False
                continue
            if in_code and stripped.startswith("$ "):
                # Check if next line has output (not a $ command or fence)
                if i < len(lines):
                    next_line = lines[i].strip()
                    if next_line and not next_line.startswith("$") and not next_line.startswith("```"):
                        continue
                violations.append(Violation(
                    self.rule_id, i, 1,
                    "Dollar sign before command", True,
                    patch=Patch("replace", i, content=stripped[2:])
                ))
        return violations

    def fix(self, v: Violation, lines: list[str]) -> str:
        if v.patch and v.patch.content:
            return v.patch.content
        if v.fixed_line:
            return v.fixed_line
        return lines[v.line_number - 1]
