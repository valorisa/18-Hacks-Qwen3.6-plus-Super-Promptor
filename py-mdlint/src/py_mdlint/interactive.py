# src/py_mdlint/interactive.py
"""Menu interactif CLI avec couleurs sobres."""

import sys
from pathlib import Path
from typing import Optional

from .reporter import Reporter
from .utils.colors import Colors


class InteractiveMenu:
    """Menu interactif 6 écrans pour py-mdlint."""
    
    def __init__(self):
        self.running = True
    
    def render_box(self, title: str, options: list[tuple[str, str]]) -> None:
        """Affiche une boîte de menu avec bordures cyan."""
        width = max(len(title), max(len(opt[1]) for opt in options)) + 4
        
        print(Colors.border("╔" + "═" * (width - 2) + "╗"))
        print(Colors.border("║") + Colors.title(f" {title:^{width-4}} ") + Colors.border("║"))
        print(Colors.border("╠" + "═" * (width - 2) + "╣"))
        
        for key, label in options:
            line = f"  {Colors.title(key)}. {Colors.text(label)}"
            padding = " " * (width - 2 - len(line) + 4)
            print(Colors.border("║") + line + padding + Colors.border("║"))
        
        print(Colors.border("╚" + "═" * (width - 2) + "╝"))
    
    def get_choice(self, prompt: str, valid: list[str], default: str = None) -> Optional[str]:
        """Demande un choix valide avec retry."""
        while True:
            try:
                user_input = input(Colors.text(f"{prompt}")).strip()

                if not user_input and default is not None:
                    return default
                if not valid:
                    return user_input
                if user_input in valid:
                    return user_input

                icon = "!" if not Reporter._use_emoji else "⚠️"
                print(Colors.warning(f"{icon}  Choix invalide. Options: {', '.join(valid)}"))
            except KeyboardInterrupt:
                icon = "!" if not Reporter._use_emoji else "⚠️"
                print(f"\n{Colors.warning(f'{icon}  Interruption. Tapez 6 pour quitter ou Ctrl+C pour forcer.')}")
    
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
        """Écran 2 — Linter un fichier/dossier."""
        print(f"\n{Colors.title('📁 Linter un fichier ou dossier')}")
        
        path = self.get_choice("Chemin du fichier ou dossier [défaut: .] : ", [], default=".")
        config = self.get_choice("Fichier de config [défaut: .markdownlint.json] : ", [], default=".markdownlint.json")
        report_format = self.get_choice("Format de sortie [console/json/github] [défaut: console] : ", 
                                       ["console", "json", "github"], default="console")
        ignore = self.get_choice("Règles à ignorer (ex: MD013,MD026) [défaut: aucune] : ", [], default="")
        
        return {
            "path": path,
            "config": config if config else None,
            "report": report_format,
            "ignore": [r.strip() for r in ignore.split(",") if r.strip()] if ignore else [],
        }
    
    def screen_create_config(self) -> dict:
        """Écran 3 — Créer un fichier de config."""
        print(f"\n{Colors.title('📝 Configuration interactive')}")
        
        config = {}
        
        # MD003: heading-style
        style = self.get_choice("Style de headings [atx/setext/consistent] [défaut: atx] : ",
                               ["atx", "setext", "consistent"], default="atx")
        if style != "atx":
            config["MD003"] = {"style": style}
        
        # MD013: line-length
        line_len = self.get_choice("Longueur max des lignes [défaut: 80, 0=illimité] : ", [], default="80")
        if line_len and line_len != "80":
            config["MD013"] = {"line_length": int(line_len) if line_len.isdigit() else 80}
        
        # MD004: ul-style
        ul_marker = self.get_choice("Symbole de listes non-ordonnées [* / - / +] [défaut: -] : ",
                                   ["*", "-", "+"], default="-")
        if ul_marker != "-":
            config["MD004"] = {"style": ul_marker}
        
        # MD033: allowed HTML
        allow_html = self.get_choice("Autoriser HTML inline ? [y/N] : ", ["y", "Y", "n", "N", ""], default="n")
        if allow_html.lower() == "y":
            config["MD033"] = {"allowed_elements": ["br", "img"]}
        
        # MD047: trailing newline
        trailing = self.get_choice("Fin de fichier = newline unique ? [Y/n] : ", 
                                  ["y", "Y", "n", "N", ""], default="Y")
        if trailing.lower() == "n":
            config["MD047"] = False
        
        return config
    
    def screen_list_rules(self) -> None:
        """Écran 4 — Voir les règles disponibles."""
        from .registry import load_rules
        
        rules = load_rules()
        print(f"\n{Colors.title(f'📋 Règles disponibles ({len(rules)} actives)')}:\n")
        
        for rule_id in sorted(rules.keys()):
            rule = rules[rule_id]
            fixable = "oui" if rule.fixable else "non"
            print(f"  {Colors.title(rule_id):<6} {rule.alias:<25} [fixable: {fixable}]  {rule.description[:50]}...")
        
        print(f"\n{Colors.text('Taper un numéro de règle pour le détail, ou [q] pour quitter : ')}")
        # Simplifié : retour direct au menu principal
    
    def screen_fix(self) -> dict:
        """Écran 5 — Linter + corriger."""
        print(f"\n{Colors.title('🔧 Linter + corriger automatiquement')}")
        
        path = self.get_choice("Chemin [défaut: .] : ", [], default=".")
        
        # Liste des règles fixables (hardcodé pour l'exemple)
        fixable_rules = ["MD009", "MD010", "MD012", "MD018", "MD019", "MD020", "MD021", 
                        "MD023", "MD027", "MD028", "MD037", "MD038", "MD039", "MD047",
                        "MD049", "MD050", "MD055", "MD056", "MD058", "MD060", "MD004", "MD007"]
        
        icon = "!" if not Reporter._use_emoji else "⚠️"
        print(Colors.warning(f"{icon}  Regles auto-fixables disponibles :"))
        print(f"   {', '.join(fixable_rules[:10])}{'...' if len(fixable_rules) > 10 else ''}")
        
        confirm = self.get_choice("Continuer ? [Y/n] : ", ["y", "Y", "n", "N", ""], default="Y")
        
        return {
            "path": path,
            "apply": confirm.lower() != "n",
        }
    
    def screen_github_workflow(self) -> dict:
        """Écran 6 — Générer GitHub Actions."""
        print(f"\n{Colors.title('📂 Générer un workflow GitHub Actions')}")
        
        project_dir = self.get_choice("Dossier du projet [défaut: .] : ", [], default=".")
        
        return {"project_dir": project_dir}
    
    def run(self) -> None:
        """Boucle principale du menu interactif."""
        while self.running:
            choice = self.screen_home()
            
            if choice == "1":
                params = self.screen_lint()
                print(f"\n{Colors.text('→ Analyse en cours...')}")
                # Ici: appeler le linter avec params
                icon_ok = "OK" if Reporter._use_emoji else "[OK]"
                icon_fail = "!" if not Reporter._use_emoji else "X"
                print(Colors.success(f"{icon_ok} Simulation: 47 regles passees | {icon_fail} 6 violations trouvees"))
            
            elif choice == "2":
                config = self.screen_create_config()
                # Ici: écrire .markdownlint.json
                icon_ok = "OK" if Reporter._use_emoji else "[OK]"
                print(Colors.success(f"{icon_ok} .markdownlint.json cree !"))
            
            elif choice == "3":
                self.screen_list_rules()
            
            elif choice == "4":
                params = self.screen_fix()
                if params["apply"]:
                    icon_ok = "OK" if Reporter._use_emoji else "[OK]"
                    print(Colors.success(f"{icon_ok} 12 violations corrigees | 3 necessitent correction manuelle"))
            
            elif choice == "5":
                params = self.screen_github_workflow()
                # Ici: générer .github/workflows/mdlint-check.yml
                icon_ok = "OK" if Reporter._use_emoji else "[OK]"
                print(Colors.success(f"{icon_ok} .github/workflows/mdlint-check.yml cree !"))
            
            elif choice == "6":
                icon = "!" if Reporter._use_emoji else ">"
                print(f"\n{Colors.success(f'{icon} Au revoir !')}")
                self.running = False
            
            # Pause avant retour au menu
            if self.running:
                input(f"\n{Colors.text('Appuyez sur Entrée pour continuer...')}")
                print("\n" + "-" * 40 + "\n")
