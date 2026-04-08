# src/py_mdlint/rules/md043.py
"""MD043: required-headings — Required heading structure."""

from .base import Rule, Violation, Token


class RuleMD043(Rule):
    rule_id = "MD043"
    alias = "required-headings"
    description = "Required heading structure"
    fixable = False

    def check(self, tokens: list[Token], lines: list[str], config: dict) -> list[Violation]:
        violations = []
        required = config.get("headings", [])
        if not required:
            return violations

        match_case = config.get("match_case", False)
        actual_headings = []
        for i, t in enumerate(tokens):
            if t.type == "heading_open":
                level = int(t.tag[1:])
                content = ""
                for j in range(i + 1, len(tokens)):
                    if tokens[j].type == "inline":
                        content = tokens[j].content.strip()
                        break
                    if tokens[j].type in ("heading_close", "paragraph_open"):
                        break
                actual_headings.append((level, content, t.line_number))

        req_idx = 0
        actual_idx = 0

        while req_idx < len(required) and actual_idx < len(actual_headings):
            req = required[req_idx]
            act_level, act_content, act_line = actual_headings[actual_idx]

            if req == "*":
                actual_idx += 1
                continue
            elif req == "+":
                if actual_idx >= len(actual_headings):
                    violations.append(Violation(
                        self.rule_id, act_line, 1,
                        f"Expected at least one heading for '{req}'"
                    ))
                actual_idx += 1
                req_idx += 1
                continue
            elif req == "?":
                actual_idx += 1
                req_idx += 1
                continue

            req_level = req.count("#")
            req_text = req.lstrip("# ").strip()

            if act_level != req_level:
                violations.append(Violation(
                    self.rule_id, act_line, 1,
                    f"Expected level h{req_level}, got h{act_level}"
                ))
            elif match_case and act_content != req_text:
                violations.append(Violation(
                    self.rule_id, act_line, 1,
                    f"Expected heading '{req_text}', got '{act_content}'"
                ))
            elif not match_case and act_content.lower() != req_text.lower():
                violations.append(Violation(
                    self.rule_id, act_line, 1,
                    f"Expected heading '{req_text}', got '{act_content}'"
                ))

            req_idx += 1
            actual_idx += 1

        while req_idx < len(required):
            if required[req_idx] not in ("*", "+", "?"):
                violations.append(Violation(
                    self.rule_id, len(lines), 1,
                    f"Missing required heading: '{required[req_idx]}'"
                ))
            req_idx += 1

        return violations
