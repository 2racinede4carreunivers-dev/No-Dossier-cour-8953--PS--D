"""Répare l'encodage double (UTF-8 lu en CP1252 puis réécrit en UTF-8).

Contexte : une opération PowerShell a réécrit orchestrator_legal.py en lisant
l'UTF-8 comme de l'ANSI, produisant du « mojibake » (ex. « généré » devenu
« gÃ©nÃ©rÃ© »). Ce script inverse l'opération ligne par ligne, uniquement sur
les lignes contenant des marqueurs de corruption, afin de ne pas toucher aux
lignes saines insérées après coup.

Usage : python reparer_encodage.py <fichier>
"""
from __future__ import annotations

import io
import sys

MARQUEURS = ("Ã", "â€", "ðŸ", "Â")


def est_corrompue(ligne: str) -> bool:
    return any(m in ligne for m in MARQUEURS)


def reparer_ligne(ligne: str) -> tuple[str, bool]:
    try:
        return ligne.encode("cp1252").decode("utf-8"), True
    except (UnicodeEncodeError, UnicodeDecodeError):
        return ligne, False


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage : python reparer_encodage.py <fichier>", file=sys.stderr)
        return 2
    chemin = sys.argv[1]
    with io.open(chemin, encoding="utf-8") as f:
        lignes = f.read().splitlines(keepends=True)

    corrigees = 0
    echecs = 0
    for i, ligne in enumerate(lignes):
        if est_corrompue(ligne):
            nouvelle, ok = reparer_ligne(ligne)
            if ok:
                lignes[i] = nouvelle
                corrigees += 1
            else:
                echecs += 1
                print(f"  [échec ligne {i + 1}] {ligne.rstrip()[:120]!r}")

    if corrigees == 0 and echecs == 0:
        print("Aucune ligne corrompue détectée — fichier intact.")
        return 0

    with io.open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write("".join(lignes))
    print(f"Réparation terminée : {corrigees} ligne(s) corrigée(s), {echecs} échec(s).")
    return 0 if echecs == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
