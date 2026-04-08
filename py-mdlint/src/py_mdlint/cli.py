# src/py_mdlint/cli.py
"""Entry point principal + routing interactive/batch/watch."""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional

from .config import load_config
from .fixer import Fixer
from .interactive import InteractiveMenu
from .parser import parse_markdown
from .registry import load_rules
from .reporter import Reporter
from .utils.colors import Colors
from .utils.fs import find_markdown_files, read_file_safe


def run_linter(
    paths: list[str],
    config_path: Optional[str] = None,
    fix: bool = False,
    report_format: str = "console",
    ignore_rules: list[str] = None,
    strict: bool = False,
) -> int:
    """
    Exécute le linter sur les chemins donnés.

    Returns:
        Code de sortie: 0 = succès, 1 = violations, 2 = erreur
    """
    ignore_rules = ignore_rules or []
    config = load_config(config_path)
    rules = load_rules()

    active_rules = {k: v for k, v in rules.items() if k not in ignore_rules}

    all_violations = []
    total_fixed = 0

    for file_path in find_markdown_files(paths[0] if paths else "."):
        try:
            content = read_file_safe(file_path)
            use_cache = not strict and os.getenv("PY_MDLINT_NO_CACHE") != "1"
            tokens, lines = parse_markdown(content, use_cache=use_cache)

            violations = []
            for rule_id, rule in active_rules.items():
                if not config.is_rule_enabled(rule_id):
                    continue
                rule_params = config.get_rule_params(rule_id)
                rule.params = rule_params
                violations.extend(rule.check(tokens, lines, config.model_dump()))

            if fix and violations:
                fixer = Fixer(active_rules)
                new_lines, fixed_count = fixer.apply_fixes(violations, lines.copy())

                new_content = "\n".join(new_lines)
                new_content, global_fixed = fixer.apply_global_fixes(violations, new_content)
                fixed_count += global_fixed
                new_lines = new_content.splitlines()

                if fixed_count > 0:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    total_fixed += fixed_count
                    tokens, lines = parse_markdown(new_content, use_cache=False)
                    violations = []
                    for rule_id, rule in active_rules.items():
                        if not config.is_rule_enabled(rule_id):
                            continue
                        violations.extend(rule.check(tokens, lines, config.model_dump()))

            reporter = Reporter(report_format, filepath=file_path, strict=strict)
            for v in violations:
                print(reporter.format_violation(v))
                all_violations.append(v)

        except Exception as e:
            error_msg = f"ERROR on {file_path}: {type(e).__name__}"
            print(error_msg, file=sys.stderr)
            return 2

    if report_format == "console":
        reporter = Reporter("console", strict=strict)
        print(reporter.summary(all_violations, total_fixed))

    has_hard_errors = any(not v.fixable for v in all_violations)
    if strict and all_violations:
        return 1
    if has_hard_errors:
        return 1
    return 0


def generate_github_workflow(project_dir: str) -> None:
    """Génère un fichier de workflow GitHub Actions."""
    workflow_content = '''# .github/workflows/mdlint-check.yml
name: Markdown Lint

on:
  push:
    paths:
      - '**.md'
      - '.markdownlint.json'
      - '.markdownlint.yaml'
      - 'pyproject.toml'
  pull_request:
    paths:
      - '**.md'
      - '.markdownlint.json'
      - '.markdownlint.yaml'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install py-mdlint
        run: pip install py-mdlint
      
      - name: Run linter
        run: py-mdlint --batch --report github .
        env:
          NO_COLOR: 1
'''
    workflow_path = Path(project_dir) / ".github" / "workflows" / "mdlint-check.yml"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(workflow_content, encoding="utf-8")
    icon = "OK" if Reporter._use_emoji else "[OK]"
    print(Colors.success(f"{icon} {workflow_path} cree !"))


def main() -> int:
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(
        description="py-mdlint — Markdown linter compatible avec markdownlint",
        epilog="Sans options : lance le menu interactif. Avec options : mode batch CI."
    )
    parser.add_argument("paths", nargs="*", help="Chemins à linter (fichiers ou dossiers)")
    parser.add_argument("--batch", "--no-interactive", action="store_true", 
                       help="Mode non-interactif (pour CI/scripts)")
    parser.add_argument("--watch", action="store_true",
                       help="Mode développement: re-lint automatique sur modification")
    parser.add_argument("--config", "-c", help="Chemin du fichier de config")
    parser.add_argument("--fix", "-f", action="store_true",
                       help="Applique les corrections auto-fixables")
    parser.add_argument("--report", "-r", choices=Reporter.FORMATS, default="console",
                       help="Format de sortie: console (défaut), json, github")
    parser.add_argument("--rules", help="Règles à activer (ex: MD001,MD003)")
    parser.add_argument("--ignore", "-i", help="Règles à ignorer (ex: MD013,MD026)")
    parser.add_argument("--version", action="version", version="py-mdlint 1.0.0")
    parser.add_argument("--strict", action="store_true",
                       help="Mode strict : transforme tous les avertissements en erreurs CI (exit 1)")
    
    args = parser.parse_args()
    
    # Mode interactif par défaut (si aucune option et pas de paths)
    if not args.batch and not sys.argv[1:] and not args.watch:
        menu = InteractiveMenu()
        menu.run()
        return 0
    
    # Mode watch (optionnel)
    if args.watch:
        try:
            from .watcher import start_watch
            
            def on_change(path: Path):
                run_linter(
                    paths=[str(path)],
                    config_path=args.config,
                    fix=args.fix,
                    report_format=args.report,
                    ignore_rules=args.ignore.split(",") if args.ignore else None,
                )
            
            observer = start_watch(
                path=Path(args.paths[0] if args.paths else "."),
                callback=on_change,
                exclude_patterns=[".git/*", "node_modules/*"],
            )
            
            # Boucle principale pour garder le watcher actif
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                observer.join()
                icon = "!" if Reporter._use_emoji else ">"
                print(f"\n{Colors.success(f'{icon} Surveillance arretee')}")
                return 0
                
        except ImportError:
            icon = "!" if not Reporter._use_emoji else "⚠️"
            print(Colors.warning(
                f"{icon}  Mode --watch necessite 'watchdog'.\n"
                "Installez avec: pip install py-mdlint[watch]"
            ), file=sys.stderr)
            return 2
    
    # Mode batch direct
    return run_linter(
        paths=args.paths,
        config_path=args.config,
        fix=args.fix,
        report_format=args.report,
        ignore_rules=args.ignore.split(",") if args.ignore else None,
        strict=args.strict,
    )


if __name__ == "__main__":
    sys.exit(main())
