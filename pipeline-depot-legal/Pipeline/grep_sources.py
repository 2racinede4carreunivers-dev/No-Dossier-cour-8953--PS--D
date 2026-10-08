"""Recherche par mots-clés dans les textes extraits des sources (usage : python grep_sources.py <mot-clé>...)."""
from __future__ import annotations

import pathlib
import re
import sys

from chemins import DIR_SOURCES as SRC

CONTEXTE = 260


def main() -> int:
    terms = sys.argv[1:] or ["dépôt"]
    pattern = re.compile("|".join(terms), re.IGNORECASE)
    for txt in sorted(SRC.glob("*.txt")):
        contenu = txt.read_text(encoding="utf-8", errors="replace")
        print(f"\n{'=' * 80}\n{txt.name}\n{'=' * 80}")
        found = 0
        for m in pattern.finditer(contenu):
            found += 1
            if found > 25:
                print("  ... (occurrences supplémentaires omises)")
                break
            debut = max(0, m.start() - CONTEXTE)
            fin = min(len(contenu), m.end() + CONTEXTE)
            extrait = " ".join(contenu[debut:fin].split())
            print(f"\n  [{m.start():6d}] …{extrait}…")
        if not found:
            print("  (aucune occurrence)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
