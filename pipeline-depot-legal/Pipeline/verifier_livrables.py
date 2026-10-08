"""Vérification finale des livrables du pipeline (PDF, pages, accents, conformité DB)."""
from __future__ import annotations

import sqlite3
import sys

from pypdf import PdfReader

from chemins import (
    FICHIER_DB,
    FICHIER_PDF_DEMANDE,
    FICHIER_PDF_DOSSIER_COMPLET,
    FICHIER_RAPPORT,
    PIECE_ARTICLE_PDF,
    PIECE_LETTRE_PDF,
)


def pages(pdf) -> int:
    return len(PdfReader(str(pdf)).pages)


def extrait(pdf, n: int = 1) -> str:
    r = PdfReader(str(pdf))
    txt = (r.pages[n - 1].extract_text() or "").strip()
    return " ".join(txt.split())[:600]


def main() -> int:
    print("== NOMBRE DE PAGES ==")
    p_dem = pages(FICHIER_PDF_DEMANDE)
    p_let = pages(PIECE_LETTRE_PDF)
    p_art = pages(PIECE_ARTICLE_PDF)
    p_tot = pages(FICHIER_PDF_DOSSIER_COMPLET)
    print(f"  Demande seule        : {p_dem} pages")
    print(f"  Pièce A-1 (lettre)   : {p_let} pages")
    print(f"  Pièce A-2 (article)  : {p_art} pages")
    print(f"  Dossier complet      : {p_tot} pages")
    attendu = p_dem + 2 + p_let + p_art  # 2 pages intercalaires
    print(f"  Attendu (demande + 2 intercalaires + pièces) : {attendu}")
    print(f"  Cohérence assemblage : {'OK' if p_tot == attendu else 'À VÉRIFIER'}")

    print("\n== EXTRAIT PAGE 1 DE LA DEMANDE (contrôle des accents) ==")
    print(" ", extrait(FICHIER_PDF_DEMANDE))

    print("\n== EXTRAIT PAGE INTERCALAIRE A-1 ==")
    print(" ", extrait(FICHIER_PDF_DOSSIER_COMPLET, p_dem + 1))

    print("\n== CONFORMITÉ EN BASE ==")
    conn = sqlite3.connect(str(FICHIER_DB))
    for statut, nb in conn.execute(
        "SELECT statut, COUNT(*) FROM conformite GROUP BY statut ORDER BY statut"
    ):
        print(f"  {statut:15s} : {nb}")
    print("\n  Pièces consignées :")
    for code, libelle, present, pages_ in conn.execute(
        "SELECT code, libelle, present, pages FROM pieces ORDER BY code"
    ):
        print(f"  {code} | présent={present} | pages={pages_} | {libelle}")
    conn.close()

    print(f"\n== RAPPORT ==\n  {FICHIER_RAPPORT} ({FICHIER_RAPPORT.stat().st_size} octets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
