"""Centralisation de tous les chemins d'accès pour le pipeline."""
from __future__ import annotations

from pathlib import Path

# Dossier racine du projet
DIR_PIPELINE = Path(__file__).resolve().parent
DIR_RACINE = DIR_PIPELINE.parent

# 1. Dossier des dépendances de conception / sources officielles
DIR_DEPENDANCES = DIR_RACINE / "Dependence_Pipeline"
DIR_SOURCES = DIR_DEPENDANCES / "sources"
DIR_EXTRAITS = DIR_DEPENDANCES / "extraits"
DOCX_SOURCE_COPY = DIR_DEPENDANCES / "README_LEGAL_source.docx"

# Source originale sur le système
DOCX_ORIGINAL = Path(
    r"C:\Users\thomasphiliippesavar\OneDrive\Documents\README_LEGAL.docx"
)

# 2. Pipeline et base de données
FICHIER_DB = DIR_PIPELINE / "depot_legal.db"

# 3. Pièces de preuve
DIR_PREUVE = DIR_RACINE / "Preuve"
PIECE_LETTRE_DOCX = DIR_PREUVE / "lettre_refus.docx"
PIECE_LETTRE_PDF = DIR_PREUVE / "lettre_refus.pdf"
PIECE_ARTICLE_PDF = DIR_PREUVE / "Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf"

# Emplacements sources des pièces (pour référence et traçabilité)
LETTRE_SOURCE_ORIGINALE = Path(r"C:\ARTICLE\Article\tex\lettre_refus.docx")
ARTICLE_SOURCE_ORIGINALE = Path(
    r"C:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf"
)
ARTICLE_SOURCE_SECONDAIRE = Path(
    r"C:\ARTICLE\Article\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf"
)

# 4. Dossier de sortie final
DIR_SORTIE = DIR_RACINE / "Demande_ajout_depot_legal"
FICHIER_TEX_DEMANDE = DIR_SORTIE / "demande_ajout_preuve.tex"
FICHIER_PDF_DEMANDE = DIR_SORTIE / "demande_ajout_preuve.pdf"
FICHIER_PDF_DOSSIER_COMPLET = (
    DIR_SORTIE / "Dossier_complet_demande_depot_legal_LVSEV25000954.pdf"
)
FICHIER_RAPPORT = DIR_SORTIE / "rapport_conformite.md"
