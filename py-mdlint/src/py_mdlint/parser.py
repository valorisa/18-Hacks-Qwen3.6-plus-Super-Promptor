# src/py_mdlint/parser.py
"""Wrapper markdown-it-py → AST normalisé avec cache de parsing."""

import json
import hashlib
from pathlib import Path
from typing import Optional
from markdown_it import MarkdownIt
from .rules.base import Token

_md_parser = MarkdownIt("default", {"breaks": True, "html": True}).enable(["table", "strikethrough"])
CACHE_DIR = Path(".py-mdlint-cache")


def _token_to_dict(token: Token) -> dict:
    return {
        "type": token.type, "tag": token.tag, "content": token.content,
        "line_number": token.line_number, "column": token.column,
        "level": token.level, "attrs": token.attrs, "meta": token.meta
    }


def _dict_to_token(d: dict) -> Token:
    return Token(
        type=d["type"], tag=d["tag"], content=d["content"],
        line_number=d["line_number"], column=d["column"],
        level=d["level"], attrs=d["attrs"], children=[], meta=d.get("meta", {})
    )


def parse_markdown(content: str, use_cache: bool = True, source: Optional[str] = None) -> tuple[list[Token], list[str]]:
    """
    Parse Markdown en tokens normalisés avec cache optionnel.

    Args:
        content: Contenu Markdown brut
        use_cache: Active/désactive le cache AST
        source: Nom du fichier (pour logs/debug)
    """
    lines = content.splitlines(keepends=False)

    if not use_cache:
        return _parse_raw(content, lines)

    content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{content_hash}.json"

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if cache_file.exists():
        try:
            data = json.loads(cache_file.read_text("utf-8"))
            if data.get("hash") == content_hash:
                return [_dict_to_token(t) for t in data["tokens"]], lines
        except (json.JSONDecodeError, KeyError):
            pass

    tokens = _parse_raw(content, lines)[0]
    cache_data = {"hash": content_hash, "tokens": [_token_to_dict(t) for t in tokens]}
    cache_file.write_text(json.dumps(cache_data), "utf-8")

    return tokens, lines


def _parse_raw(content: str, lines: list[str]) -> tuple[list[Token], list[str]]:
    raw_tokens = _md_parser.parse(content)
    tokens = []
    for token in raw_tokens:
        tokens.append(Token(
            type=token.type, tag=token.tag or "", content=token.content or "",
            line_number=token.map[0] + 1 if token.map else 1, column=1,
            level=token.level, attrs=dict(token.attrs) if token.attrs else {},
            children=[], meta={
                "original_line": lines[token.map[0]] if token.map and lines else "",
                "indent": len(lines[token.map[0]]) - len(lines[token.map[0]].lstrip()) if token.map and lines else 0,
                "fence_char": token.info[0] if token.type == "fence" and token.info else None,
                "info": token.info if token.type == "fence" else "",
            }
        ))
    return tokens, lines


def get_heading_tokens(tokens: list[Token]) -> list[Token]:
    return [t for t in tokens if t.type == "heading_open"]
