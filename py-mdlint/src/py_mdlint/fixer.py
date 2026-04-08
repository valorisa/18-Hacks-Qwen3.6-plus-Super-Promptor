# src/py_mdlint/fixer.py
"""Orchestrateur pour le mode --fix (idempotent, support Patch)."""

from .rules.base import Rule, Violation, Patch


class Fixer:
    """Applique les corrections auto-fixables de manière idempotente."""

    def __init__(self, rules: dict[str, Rule]):
        self.rules = rules

    def apply_fixes(
        self,
        violations: list[Violation],
        lines: list[str]
    ) -> tuple[list[str], int]:
        """
        Applique les corrections sur les lignes via le système Patch.
        """
        patches: list[Patch] = []
        for v in violations:
            if v.patch:
                patches.append(v.patch)
            elif v.fixed_line is not None:
                patches.append(Patch("replace", v.line_number, content=v.fixed_line))

        fixable_patches = [p for p in patches if p.line_number <= len(lines) + 1]
        if not fixable_patches:
            return lines, 0

        fixable_patches.sort(key=lambda p: p.line_number, reverse=True)

        fixed_count = 0
        for patch in fixable_patches:
            idx = patch.line_number - 1
            if patch.type == "insert":
                lines.insert(idx, patch.content or "")
                fixed_count += 1
            elif patch.type == "delete" and 0 <= idx < len(lines):
                lines.pop(idx)
                fixed_count += 1
            elif patch.type == "replace" and 0 <= idx < len(lines):
                if lines[idx] != patch.content:
                    lines[idx] = patch.content or ""
                    fixed_count += 1

        return lines, fixed_count

    def apply_global_fixes(
        self,
        violations: list[Violation],
        content: str,
    ) -> tuple[str, int]:
        """
        Applique les corrections globales (MD012, MD047).
        """
        import re

        fixed_count = 0

        if any(v.rule_id == "MD047" for v in violations):
            content = content.rstrip("\n") + "\n"
            fixed_count += 1

        md012_violations = [v for v in violations if v.rule_id == "MD012"]
        if md012_violations:
            content = re.sub(r"\n{3,}", "\n\n", content)
            fixed_count += len(md012_violations)

        return content, fixed_count

    def is_idempotent(self, original: list[str], fixed: list[str]) -> bool:
        return original != fixed
