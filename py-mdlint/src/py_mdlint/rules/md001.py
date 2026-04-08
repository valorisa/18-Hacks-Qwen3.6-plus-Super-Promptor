# src/py_mdlint/rules/md001.py
"""MD001: heading-increment — Heading levels should only increment by one."""

from .base import Rule, Violation, Token


class RuleMD001(Rule):
    """
    MD001: heading-increment
    
    Heading levels should only increment by one level at a time.
    Expected: h2; Actual: h3 → violation.
    """
    
    rule_id = "MD001"
    alias = "heading-increment"
    description = "Heading levels should only increment by one level at a time"
    fixable = False  # Requiert validation humaine pour le contexte sémantique
    
    def check(
        self, 
        tokens: list[Token], 
        lines: list[str], 
        config: dict
    ) -> list[Violation]:
        violations = []
        prev_level = 0
        prev_line = 0
        
        for token in tokens:
            if token.type == "heading_open":
                # Extraction du niveau: h1→1, h2→2, etc.
                try:
                    current_level = int(token.tag[1:])
                except (IndexError, ValueError):
                    continue  # Tag invalide, ignorer
                
                # Vérifie saut de niveau > 1 (ex: h1 → h3)
                if prev_level > 0 and current_level > prev_level + 1:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        line_number=token.line_number,
                        column=1,  # Heading commence toujours au début
                        message=(
                            f"Heading levels should only increment by one level at a time "
                            f"[Expected: h{prev_level + 1}; Actual: h{current_level}]"
                        ),
                        fixable=False,
                        suggestion=(
                            f"Remplacer {'#' * current_level} par {'#' * (prev_level + 1)} "
                            f"à la ligne {token.line_number}"
                        )
                    ))
                
                prev_level = current_level
                prev_line = token.line_number
        
        return violations
