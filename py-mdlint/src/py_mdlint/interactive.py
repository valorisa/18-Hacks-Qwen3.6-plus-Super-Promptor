# src/py_mdlint/interactive.py
"""Menu interactif CLI avec couleurs sobres."""
import json
import sys
from pathlib import Path
from typing import Optional

from .reporter import Reporter
from .utils.colors import Colors


class InteractiveMenu:
    """Menu interactif 6 écrans pour py-mdlint."""

    def __init__(self) -> None:
        self.running = True

    def render_box(self, title: str, options: list[tuple[str, str]]) -> None:
        """Affiche une boîte de menu avec bordures cyan."""
        title_len = len(title)
        option_len = max(len(f"  {k}. {v}") for k, v in options)
        width = max(title_len, option_len) + 6
        
        print(Colors.border("+" + "-" * (width - 2) + "+"))
        print(Colors.border("|") + f" {title} ".center(width - 2) + Colors.border("|"))
        print(Colors.border("+" + "-" * (width - 2) + "+"))
        for key, label in options:
            line = f"  {key}. {label}"
            print(Colors.border("|") + line.ljust(width - 2) + Colors.border("|"))
        print(Colors.border("+" + "-" * (width - 2) + "+"))

    def get_choice(self, prompt: str, valid: list[str], default: str = None) -> Optional[str]:
        """Demande un choix valide avec retry."""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input and default is not None:
                    return default
                if not valid:
                    return user_input
                if user_input in valid:
                    return user_input
                print(Colors.warning(f"! Choix invalide. Options: {', '.join(valid)}"))
            except KeyboardInterrupt:
                print(f"\n{Colors.warning('⚠️ Interruption. Tapez 6 pour quitter.')}")
                return "6"

    def screen_home(self) -> Optional[str]:
        """Écran 1 — Accueil."""
        options = [
            ("1", "Linter un fichier/dossier"),
            ("2", "Créer un fichier de config"),
            ("3", "Voir les règles disponibles"),
            ("4", "Linter + corriger automatiquement"),
            ("5", "Générer un workflow GitHub Actions"),
            ("6", "Quitter"),
        ]
        self.render_box("py-mdlint — Markdown Linter", options)
        return self.get_choice("Choix [1-6] : ", [str(i) for i in range(1, 7)])

    def screen_lint(self) -> dict:
        """Écran 2 — Paramètres pour linter un fichier/dossier."""
        print(f"\n{Colors.title('--- Linter un fichier ou dossier ---')}")
        path = self.get_choice("Chemin du fichier ou dossier [défaut: .] : ", [], default=".")
        config = self.get_choice("Fichier de config [défaut: .markdownlint.json] : ", [], default=".markdownlint.json")
        report_format = self.get_choice(
            "Format de sortie [console/json/github] [défaut: console] : ",
            ["console", "json", "github"], default="console"
        )
        ignore = self.get_choice("Règles à ignorer (ex: MD013,MD026) [défaut: aucune] : ", [], default="")
        return {
            "path": path,
            "config": config if config else None,
            "report": report_format,
            "ignore": [r.strip() for r in ignore.split(",") if r.strip()] if ignore else []
        }

    def screen_create_config(self) -> dict:
        """Écran 3 — Configuration interactive."""
        print(f"\n{Colors.title('--- Configuration interactive ---')}")
        config: dict = {}

        style = self.get_choice("Style de headings [atx/setext/consistent] [défaut: atx] : ",
                                ["atx", "setext", "consistent"], default="atx")
        if style != "atx":
            config["MD003"] = {"style": style}

        line_len = self.get_choice("Longueur max des lignes [défaut: 80, 0=illimité] : ", [], default="80")
        if line_len and line_len != "80":
            config["MD013"] = {"line_length": int(line_len) if line_len.isdigit() else 80}

        ul_marker = self.get_choice("Symbole de listes non-ordonnées [* / - / +] [défaut: -] : ",
                                    ["*", "-", "+"], default="-")
        if ul_marker != "-":
            config["MD004"] = {"style": ul_marker}

        allow_html = self.get_choice("Autoriser HTML inline ? [y/N] : ", ["y", "Y", "n", "N", ""], default="n")
        if allow_html.lower() == "y":
            config["MD033"] = {"allowed_elements": ["br", "img"]}

        trailing = self.get_choice("Fin de fichier = newline unique ? [Y/n] : ",
                                   ["y", "Y", "n", "N", ""], default="Y")
        if trailing.lower() == "n":
            config["MD047"] = False

        return config

    def screen_list_rules(self) -> None:
        """Écran 4 — Voir les règles disponibles."""
        from .registry import load_rules
        print(f"\n{Colors.title('--- Règles disponibles ---')}")
        rules = load_rules()
        for rule_id in sorted(rules.keys()):
            rule = rules[rule_id]
            fixable = "✅ oui" if rule.fixable else "❌ non"
            print(f"  {Colors.title(rule_id):<6} {rule.alias:<25} [fixable: {fixable}]  {rule.description}")
        print(f"\n{Colors.success(f'Total: {len(rules)} règles actives.')}")

    def screen_fix(self) -> dict:
        """Écran 5 — Linter + corriger automatiquement."""
        print(f"\n{Colors.title('--- Linter + corriger automatiquement ---')}")
        path = self.get_choice("Chemin [défaut: .] : ", [], default=".")
        
        fixable_rules = ["MD009", "MD010", "MD012", "MD018", "MD019", "MD020", "MD021",
                         "MD023", "MD027", "MD028", "MD037", "MD038", "MD039", "MD047"]
        print(Colors.warning(f"⚠️ Règles auto-fixables disponibles : {', '.join(fixable_rules[:8])}..."))
        
        confirm = self.get_choice("Continuer ? [Y/n] : ", ["y", "Y", "n", "N", ""], default="Y")
        return {"path": path, "apply": confirm.lower() != "n"}

    def screen_github_workflow(self) -> dict:
        """Écran 6 — Générer GitHub Actions."""
        print(f"\n{Colors.title('--- Générer un workflow GitHub Actions ---')}")
        project_dir = self.get_choice("Dossier du projet [défaut: .] : ", [], default=".")
        return {"project_dir": project_dir}

    def run(self) -> None:
        """Boucle principale du menu interactif."""
        from .cli import run_linter, generate_github_workflow
        from .config import MarkdownlintConfig
        
        while self.running:
            choice = self.screen_home()
            try:
                if choice == "1":
                    params = self.screen_lint()
                    print("\n> Analyse en cours...")
                    exit_code = run_linter(
                        paths=[params["path"]],
                        config_path=params["config"],
                        report_format=params["report"],
                        ignore_rules=params["ignore"]
                    )
                    status_msg = "✅ Analyse terminée : Aucune violation détectée." if exit_code == 0 \
                        else f"⚠️ Analyse terminée : {exit_code} violation(s) détectée(s)."
                    print(Colors.success(status_msg) if exit_code == 0 else Colors.warning(status_msg))

                elif choice == "2":
                    config_data = self.screen_create_config()
                    config_data.setdefault("default", True)
                    config = MarkdownlintConfig(**config_data)
                    config_path = Path(".markdownlint.json")
                    config_path.write_text(config.model_dump_json(indent=2), encoding="utf-8")
                    print(Colors.success(f"✅ Fichier '{config_path}' créé avec succès !"))

                elif choice == "3":
                    self.screen_list_rules()

                elif choice == "4":
                    params = self.screen_fix()
                    if params["apply"]:
                        print("\n> Correction automatique en cours...")
                        exit_code = run_linter(
                            paths=[params["path"]],
                            fix=True,
                            report_format="console"
                        )
                        status_msg = "✅ Corrections appliquées avec succès." if exit_code == 0 \
                            else "⚠️ Corrections partielles ou erreurs. Vérifiez les logs ci-dessus."
                        print(Colors.success(status_msg) if exit_code == 0 else Colors.warning(status_msg))

                elif choice == "5":
                    params = self.screen_github_workflow()
                    generate_github_workflow(params["project_dir"])
                    print(Colors.success("✅ Workflow GitHub généré dans `.github/workflows/mdlint-check.yml`"))

                elif choice == "6":
                    print(f"\n{Colors.success('👋 Au revoir !')}")
                    self.running = False

            except KeyboardInterrupt:
                print(f"\n{Colors.warning('⚠️ Interruption clavier.')}")
                self.running = False
            except Exception as e:
                print(Colors.warning(f"❌ Erreur inattendue : {e}"))

            if self.running:
                input("\nAppuyez sur Entrée pour continuer...")
                print("\n" + "-" * 40 + "\n")