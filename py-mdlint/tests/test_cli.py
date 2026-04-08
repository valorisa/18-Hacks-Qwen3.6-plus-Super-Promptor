# tests/test_cli.py
"""Tests d'intégration pour la CLI."""

import subprocess
import sys
import os
from pathlib import Path


def test_cli_version():
    """py-mdlint --version retourne la version."""
    result = subprocess.run(
        [sys.executable, "-m", "py_mdlint", "--version"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    assert result.returncode == 0
    assert "1.0.0" in result.stdout


def test_cli_help():
    """py-mdlint --help affiche l'aide."""
    result = subprocess.run(
        [sys.executable, "-m", "py_mdlint", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    assert result.returncode == 0
    assert "--batch" in result.stdout
    assert "--fix" in result.stdout
    assert "--report" in result.stdout


def test_cli_batch_on_clean_file(tmp_path):
    """Mode batch sur fichier valide → code 0."""
    md_file = tmp_path / "test.md"
    md_file.write_text("# Title\n\n## Subtitle\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "py_mdlint", "--batch", str(md_file)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )

    assert result.returncode == 0
