#!/usr/bin/env python3
"""
Linter personnalisé pour fichiers hybrides XML/Markdown
Respecte :
- Balises XML <tag>...</tag>
- Variables {{VAR}} et {{VAR_with_underscores}}
- Syntaxe fonctionnelle [TAG], [?mot], etc.
- Corrige uniquement les violations Markdown SANS toucher au XML/variables
"""

import re
import sys
from pathlib import Path


def extract_xml_blocks(content: str) -> tuple[str, list[str]]:
    """Extrait les blocs XML et les remplace par des placeholders."""
    xml_blocks = []
    # Pattern pour balises XML auto-fermantes ou avec contenu
    xml_pattern = re.compile(
        r'(<[\w:][\w:\-]*>.*?</[\w:][\w:\-]*>)|(<[\w:][\w:\-]*/?>)',
        re.DOTALL
    )
    
    def replacer(match):
        idx = len(xml_blocks)
        xml_blocks.append(match.group(0))
        return f'<!-- XML_BLOCK_{idx} -->'
    
    cleaned = xml_pattern.sub(replacer, content)
    return cleaned, xml_blocks


def restore_xml_blocks(content: str, xml_blocks: list[str]) -> str:
    """Restaure les blocs XML depuis les placeholders."""
    for idx, block in enumerate(xml_blocks):
        content = content.replace(f'<!-- XML_BLOCK_{idx} -->', block)
    return content


def protect_variables(content: str) -> tuple[str, list[str]]:
    """Protège les variables {{VAR}} contre les modifications."""
    variables = []
    var_pattern = re.compile(r'\{\{[\w:\-]+\}\}')
    
    def replacer(match):
        idx = len(variables)
        variables.append(match.group(0))
        return f'<!-- VAR_BLOCK_{idx} -->'
    
    cleaned = var_pattern.sub(replacer, content)
    return cleaned, variables


def restore_variables(content: str, variables: list[str]) -> str:
    """Restaure les variables {{VAR}}."""
    for idx, var in enumerate(variables):
        content = content.replace(f'<!-- VAR_BLOCK_{idx} -->', var)
    return content


def protect_functional_brackets(content: str) -> tuple[str, list[str]]:
    """Protège les crochets fonctionnels [TAG], [?mot], [MODE:API], etc."""
    brackets = []
    # Match [WORD], [?WORD], [WORD:SUB], [À CLARIFIER], etc.
    bracket_pattern = re.compile(
        r'\[([^\]]+)\]'
    )
    
    def replacer(match):
        idx = len(brackets)
        brackets.append(match.group(0))
        return f'<!-- BRACKET_BLOCK_{idx} -->'
    
    cleaned = bracket_pattern.sub(replacer, content)
    return cleaned, brackets


def restore_functional_brackets(content: str, brackets: list[str]) -> str:
    """Restaure les crochets fonctionnels."""
    for idx, bracket in enumerate(brackets):
        content = content.replace(f'<!-- BRACKET_BLOCK_{idx} -->', bracket)
    return content


def fix_markdown_violations(content: str) -> str:
    """
    Corrige uniquement les violations Markdown SANS toucher au XML/variables.
    Rules appliquées :
    - MD022: Lignes vides autour des headings
    - MD032: Lignes vides autour des listes
    - MD047: Newline en fin de fichier
    - MD009: Espaces en fin de ligne
    - MD012: Lignes vides consécutives multiples
    - MD031: Lignes vides autour des fenced code blocks
    """
    lines = content.split('\n')
    fixed = []
    
    for i, line in enumerate(lines):
        # MD009: Trailing spaces
        if line.rstrip() != line and not line.strip().startswith('<!--'):
            line = line.rstrip()
        
        # MD022: Headings need blank lines around them
        if re.match(r'^#{1,6}\s', line):
            if fixed and fixed[-1].strip() != '' and not fixed[-1].startswith('#'):
                # Check if previous line is not already a heading
                if not re.match(r'^#{1,6}\s', fixed[-1]):
                    fixed.append('')
        
        # MD032: Lists need blank lines before them
        if re.match(r'^(\s*[-*+]|\s*\d+\.)\s', line):
            if fixed and fixed[-1].strip() != '':
                # Check if we're not already in a list
                if not re.match(r'^(\s*[-*+]|\s*\d+\.)\s', fixed[-1]):
                    # Don't add blank line if it's the first line after a heading
                    if fixed and not re.match(r'^#{1,6}\s', fixed[-1]):
                        fixed.append('')
        
        fixed.append(line)
    
    # MD047: Single trailing newline
    result = '\n'.join(fixed)
    result = result.rstrip('\n') + '\n'
    
    # MD012: Multiple blank lines -> single blank line
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result


def lint_hybrid_file(filepath: str, dry_run: bool = True) -> dict:
    """Main lint function for hybrid XML/Markdown files."""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ Fichier non trouvé: {filepath}")
        return {"success": False}
    
    content = path.read_text()
    original_content = content
    
    # Step 1: Protect XML blocks
    content, xml_blocks = extract_xml_blocks(content)
    print(f"🔒 {len(xml_blocks)} bloc(s) XML protégé(s)")
    
    # Step 2: Protect variables {{VAR}}
    content, variables = protect_variables(content)
    print(f"🔒 {len(variables)} variable(s) {{...}} protégée(s)")
    
    # Step 3: Protect functional brackets [TAG], [?mot], etc.
    content, brackets = protect_functional_brackets(content)
    print(f"🔒 {len(brackets)} crochet(s) fonctionnel(s) protégé(s)")
    
    # Step 4: Apply Markdown fixes
    fixed_content = fix_markdown_violations(content)
    
    # Step 5: Restore protected elements
    fixed_content = restore_functional_brackets(fixed_content, brackets)
    fixed_content = restore_variables(fixed_content, variables)
    fixed_content = restore_xml_blocks(fixed_content, xml_blocks)
    
    # Compare
    if fixed_content == original_content:
        print("✅ Aucune violation corrigeable détectée (ou fichier déjà propre)")
        return {"success": True, "changes": 0}
    else:
        changes = fixed_content.count('\n') - original_content.count('\n')
        print(f"📝 {abs(changes)} modification(s) proposée(s)")
        
        if not dry_run:
            path.write_text(fixed_content)
            print(f"✅ Fichier corrigé: {filepath}")
            # Backup original
            backup = path.with_suffix('.md.bak')
            backup.write_text(original_content)
            print(f"💾 Backup créé: {backup}")
        else:
            print("🔍 Mode DRY RUN - aucune modification appliquée")
            # Show diff
            import difflib
            diff = list(difflib.unified_diff(
                original_content.splitlines(keepends=True),
                fixed_content.splitlines(keepends=True),
                fromfile='original',
                tofile='fixed',
                n=3
            ))
            if diff:
                print("\n--- DIFF ---")
                for line in diff[:50]:  # Limit output
                    print(line, end='')
                if len(diff) > 50:
                    print(f"\n... (+{len(diff) - 50} lines)")
        
        return {"success": True, "changes": abs(changes)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_hybrid.py <file.md> [--apply]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    dry_run = "--apply" not in sys.argv
    
    print(f"{'🔍 DRY RUN' if dry_run else '✅ APPLY'} MODE")
    print(f"📄 Fichier: {filepath}")
    print("-" * 60)
    
    result = lint_hybrid_file(filepath, dry_run=dry_run)
    
    if result.get("success"):
        sys.exit(0)
    else:
        sys.exit(1)
