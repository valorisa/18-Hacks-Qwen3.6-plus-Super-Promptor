# src/py_mdlint/reporter.py
"""Formattage des rapports : console, JSON, GitHub Annotations (avec mode strict)."""

import json
import sys
from pathlib import Path
from typing import Optional
from .rules.base import Violation
from .utils.colors import Colors


def _supports_emoji() -> bool:
    """Vérifie si l'encodage stdout supporte les emojis (UTF-8)."""
    if sys.stdout is None:
        return False
    encoding = getattr(sys.stdout, "encoding", None)
    if not encoding:
        return False
    return encoding.lower().startswith("utf")


class Reporter:
    """Générateur de rapports pour différents formats de sortie."""

    FORMATS = ["console", "json", "github"]
    _use_emoji = _supports_emoji()

    def __init__(self, format: str = "console", filepath: Optional[Path] = None, strict: bool = False):
        self.format = format
        self.filepath = filepath
        self.strict = strict

    def format_violation(self, violation: Violation) -> str:
        """Formate une violation selon le format de sortie."""
        if self.format == "json":
            data = violation.to_dict()
            if self.strict:
                data["severity"] = "error"
            return json.dumps(data)

        if self.format == "github":
            level = "error" if self.strict else ("warning" if not violation.fixable else "notice")
            filepath = self.filepath or "unknown"
            col = violation.column or 1
            return (
                f"::{level} file={filepath},line={violation.line_number},col={col}"
                f"::{violation.rule_id}: {violation.message}"
            )

        return self._console_output(violation)

    def _console_output(self, violation: Violation) -> str:
        """Format console colorisé."""
        parts = [
            Colors.wrap(Colors.CYAN, f"{violation.rule_id}"),
            Colors.wrap(Colors.WHITE, f"line {violation.line_number}"),
        ]
        if violation.column:
            parts.append(f"col {violation.column}")

        if self._use_emoji:
            icon = "🔴 ERROR" if self.strict else ("❌" if not violation.fixable else "⚠️")
            suggestion_icon = "💡"
        else:
            icon = "ERROR" if self.strict else ("X" if not violation.fixable else "!")
            suggestion_icon = "i"

        message = f"{icon} {violation.message}"

        if violation.suggestion and not self.strict and Colors.enabled():
            message += f"\n   {Colors.wrap(Colors.YELLOW, suggestion_icon)} {violation.suggestion}"

        return f"[{', '.join(parts)}] {message}"

    def summary(self, violations: list[Violation], fixed: int = 0) -> str:
        """Génère un résumé de l'analyse."""
        if self.format == "json":
            return json.dumps({
                "total": len(violations),
                "fixed": fixed,
                "strict": self.strict,
                "violations": [v.to_dict() for v in violations],
            })

        if self.format == "github":
            return ""

        icon_ok = "✅" if self._use_emoji else "[OK]"
        icon_fail = "🔴" if (self._use_emoji and self.strict) else ("X" if self.strict else "!")

        if not violations and fixed == 0:
            return Colors.success(f"{icon_ok} Aucune violation detectee")

        lines = []
        if fixed > 0:
            lines.append(Colors.success(f"{icon_ok} {fixed} violations corrigees"))

        remaining = len(violations)
        if remaining > 0:
            lines.append(Colors.warning(f"{icon_fail} {remaining} violations restantes"))
            if not self.strict:
                fixable = sum(1 for v in violations if v.fixable)
                lines.append(Colors.text(f"   ({fixable} auto-fixables, {remaining - fixable} manuelles)"))

        return "\n".join(lines)
