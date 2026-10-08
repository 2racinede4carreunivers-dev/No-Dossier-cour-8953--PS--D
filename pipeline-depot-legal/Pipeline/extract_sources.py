"""Extrait le texte de tous les PDF/HTML de sources vers des fichiers .txt."""
from __future__ import annotations

import pathlib
import re
import sys

from pypdf import PdfReader

from chemins import DIR_SOURCES as SRC


def extract_pdf(path: pathlib.Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        pages.append(f"\n--- [{path.name} p.{i}] ---\n" + (page.extract_text() or ""))
    return "\n".join(pages)


def extract_html(path: pathlib.Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = re.sub(r"&nbsp;", " ", raw)
    raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n", raw)
    return raw


def main() -> int:
    if not SRC.exists():
        print("dossier sources_barreau introuvable", file=sys.stderr)
        return 1
    for path in sorted(SRC.iterdir()):
        try:
            if path.suffix.lower() == ".pdf" and path.stat().st_size > 0:
                text = extract_pdf(path)
            elif path.suffix.lower() in (".html", ".htm") and path.stat().st_size > 0:
                text = extract_html(path)
            else:
                continue
            out = path.with_suffix(".txt")
            out.write_text(text, encoding="utf-8")
            print(f"{path.name:60s} -> {len(text):8d} caracteres")
        except Exception as exc:  # noqa: BLE001
            print(f"ERREUR {path.name}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
