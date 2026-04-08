# src/py_mdlint/watcher.py
"""Mode développement --watch avec watchdog (dépendance optionnelle)."""

import time
from pathlib import Path
from typing import Callable, Optional

from .utils.colors import Colors


try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class MarkdownEventHandler(FileSystemEventHandler):
    """Gestionnaire d'événements pour les fichiers .md."""
    
    def __init__(
        self, 
        callback: Callable[[Path], None],
        exclude_patterns: list[str] = None
    ):
        self.callback = callback
        self.exclude_patterns = exclude_patterns or []
        self._last_event = {}  # Debounce: path → timestamp
    
    def on_modified(self, event):
        if not isinstance(event, FileModifiedEvent):
            return
        
        path = Path(event.src_path)
        
        # Filtrer par extension et exclusions
        if path.suffix != ".md":
            return
        if any(path.match(pattern) for pattern in self.exclude_patterns):
            return
        
        # Debounce: ignorer événements trop rapprochés (<500ms)
        now = time.time()
        if path in self._last_event and now - self._last_event[path] < 0.5:
            return
        self._last_event[path] = now
        
        # Exécuter le callback (lint)
        try:
            print(f"\n{Colors.title('🔄')} Changement détecté: {path}")
            self.callback(path)
        except Exception as e:
            print(f"{Colors.warning(f'⚠️  Erreur: {e}')}")


def start_watch(
    path: Path,
    callback: Callable[[Path], None],
    exclude_patterns: list[str] = None,
    recursive: bool = True
) -> Observer:
    """
    Démarre la surveillance d'un dossier pour les fichiers .md.
    
    Args:
        path: Chemin à surveiller
        callback: Fonction appelée sur modification (reçoit le Path modifié)
        exclude_patterns: Patterns à exclure
        recursive: Surveillance récursive
    
    Returns:
        Observer à garder en référence pour .stop()
    """
    if not WATCHDOG_AVAILABLE:
        raise RuntimeError(
            "Mode --watch requires 'watchdog'. Install with: pip install py-mdlint[watch]"
        )
    
    handler = MarkdownEventHandler(callback, exclude_patterns)
    observer = Observer()
    observer.schedule(handler, str(path), recursive=recursive)
    observer.start()
    
    print(f"{Colors.success('✅')} Surveillance active sur {path}")
    print(f"{Colors.text('💡')} Appuyez sur Ctrl+C pour arrêter\n")
    
    return observer
