"""Pipeline « checkliste » du dépôt complet — conformité Barreau / audience du 23 octobre 2026.

But du pipeline
---------------
1. Établir la table des points qui font partie du dépôt complet local et qui DOIVENT y être
   présents pour atteindre le but du dépôt :
      * requête en ajout d'une preuve au dépôt légal ;
      * dépôt d'un rapport présenténciel (art. 721 (1) C.cr.) pour le verdict ;
      * audience du vendredi 23 octobre 2026 à 9 h 30, salle 2.15, Palais de justice de
        Québec — Cour du Québec, Chambre criminelle et pénale, district de Québec.
2. Vérifier, pour chacun de ces points, si la documentation incluse est bien conforme au but du
   dépôt et si elle remplit les exigences du Barreau du Québec et des organismes de référence
   (Fondation du Barreau, Cour du Québec, DPCP, Code criminel) relevées dans les sources
   téléchargées (collect_barreau.py / Dependence_Pipeline/sources/).
3. Noter chaque point de 0 à 10 (0 = le plus bas, 10 = le plus haut), calculer une note globale
   pondérée, un verdict et des recommandations.

Étapes
------
  1. (ré)collecte des sources officielles (Barreau du Québec, Fondation du Barreau,
     Cour du Québec, DPCP, Code criminel) — optionnellement en forçant le re-téléchargement ;
  2. extraction du texte des livrables (PDF : pypdf ; .tex/.md/.txt : UTF-8) ;
  3. évaluation :
       A. points de structure du dépôt (codes DEP-xx) ;
       B. exigences de documentation (FORME / AVIS / PREUVE / CONF / DEROUL) reprises de
          build_db.EXIGENCES, c'est-à-dire les exigences du Barreau déjà modélisées ;
  4. rapport markdown `checklist_conformite.md` + affichage console + code de retour.

Usage
-----
    cd pipeline-depot-legal\\Pipeline
    python pipeline_checkliste.py [--rafraichir] [--sans-telechargement] [--seuil 8.0]
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import re
import sqlite3
import ssl
import sys
import urllib.request

try:  # console UTF-8 (accents + émojis du rapport)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
except Exception:  # pragma: no cover
    pass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from pypdf import PdfReader  # noqa: E402

import build_db  # noqa: E402
from chemins import (  # noqa: E402
    DOCX_SOURCE_COPY,
    DIR_EXTRAITS,
    DIR_PREUVE,
    DIR_RACINE,
    DIR_SOURCES,
    DIR_SORTIE,
    FICHIER_DB,
    FICHIER_PDF_DEMANDE,
    FICHIER_PDF_DOSSIER_COMPLET,
    FICHIER_RAPPORT,
    FICHIER_TEX_DEMANDE,
    PIECE_ARTICLE_PDF,
    PIECE_LETTRE_DOCX,
    PIECE_LETTRE_PDF,
)
from collect_barreau import SOURCES  # noqa: E402

# ---------------------------------------------------------------------------
# Emplacements (racine du dépôt local = parent de pipeline-depot-legal/)
# ---------------------------------------------------------------------------
DIR_DEPOT = DIR_RACINE.parent
README_RACINE = DIR_DEPOT / "README.md"
README_PIPELINE = DIR_RACINE / "README.md"
RAPPORT_PRESENT_TEX = DIR_DEPOT / "rapport_presentenciel_2026-10-23.tex"
RAPPORT_PRESENT_PDF = DIR_DEPOT / "rapport_presentenciel_2026-10-23.pdf"
GUIDE_POURSUITE = DIR_SORTIE / "guide_transmission_poursuite.md"
PIECE_A3_CCN = DIR_PREUVE / "lettre_CCQ_vol_donnees_2026-09-25.pdf"

# Sources additionnelles : coordonnées de la poursuite et de la Cour (téléchargées par ce
# pipeline afin que le guide de transmission repose sur des données officielles à jour).
SOURCES_POURSUITE: list[dict] = [
    {
        "id": "DPCP_GEN",
        "organisme": "DPCP",
        "titre": "Coordonnées générales du DPCP",
        "type": "page_web",
        "url": (
            "https://www.quebec.ca/gouvernement/ministeres-organismes/"
            "directeur-poursuites-criminelles-penales/coordonnees-structure/generales"
        ),
        "fichier": "dpcp_coordonnees_generales.html",
        "note": "418 643-4085 / 1 855 643-4085 ; info@dpcp.gouv.qc.ca ; siège : 1200, "
                "route de l'Église, bur. 210, Québec G1V 4M1.",
    },
    {
        "id": "DPCP_CAPITALE",
        "organisme": "DPCP",
        "titre": "Points de service du DPCP — Capitale-Nationale (district de Québec)",
        "type": "page_web",
        "url": (
            "https://www.quebec.ca/gouvernement/ministeres-organismes/"
            "directeur-poursuites-criminelles-penales/coordonnees-structure/regionales/"
            "bureaux/capitale-nationale"
        ),
        "fichier": "dpcp_coordonnees_capitale-nationale.html",
        "note": "Bureau des affaires pénales : 418 649-3500 poste 1 ; "
                "penal.quebec@dpcp.gouv.qc.ca ; PJQ, 300, boul. Jean-Lèsage ; téléc. 418 646-4919.",
    },
    {
        "id": "CQ_NOUS_REJOINDRE",
        "organisme": "Cour du Québec",
        "titre": "Nous joindre — Cour du Québec",
        "type": "page_web",
        "url": "https://courduquebec.new.volcan.design/a-propos-de-la-cour/nous-joindre",
        "fichier": "cq_nous-joindre.html",
        "note": "info@courduquebec.ca ; adresse du Palais de justice de Québec ; renseignements "
                "auprès des greffes.",
    },
]

# ---------------------------------------------------------------------------
# Utilitaires : texte, pages, téléchargement
# ---------------------------------------------------------------------------
_CACHE_TEXTE: dict[pathlib.Path, str] = {}

PAT_PLACEHOLDER = re.compile(r"\[[A-ZÀ-Þ][^\[\]]{0,48}\s[^\[\]]{0,48}\]")


def normaliser(texte: str) -> str:
    """Minuscules, apostrophes/tirets unifiés, espaces réduits : pour les comparaisons."""
    texte = (
        texte.replace("’", "'")
        .replace("‘", "'")
        .replace("–", "-")
        .replace("—", "-")
        .replace(" ", " ")
    )
    return re.sub(r"\s+", " ", texte).lower()


def texte_de(chemin: pathlib.Path) -> str:
    """Texte d'un fichier (PDF -> pypdf ; binaire -> vide ; sinon UTF-8 avec repli)."""
    if chemin in _CACHE_TEXTE:
        return _CACHE_TEXTE[chemin]
    texte = ""
    try:
        if chemin.exists() and chemin.stat().st_size > 0:
            suffixe = chemin.suffix.lower()
            if suffixe == ".pdf":
                lecteur = PdfReader(str(chemin))
                texte = " ".join((page.extract_text() or "") for page in lecteur.pages)
            elif suffixe in {".docx", ".db", ".bin", ".pyc", ".onnx"}:
                texte = ""
            else:
                try:
                    texte = chemin.read_text(encoding="utf-8")
                except (UnicodeDecodeError, UnicodeError):
                    texte = chemin.read_text(encoding="latin-1", errors="replace")
    except Exception:  # noqa: BLE001  (PDF illisible : traité comme texte absent)
        texte = ""
    _CACHE_TEXTE[chemin] = texte
    return texte


def pages_de(chemin: pathlib.Path) -> int | None:
    """Nombre de pages d'un PDF (None si illisible ou non-PDF)."""
    if chemin.exists() and chemin.suffix.lower() == ".pdf":
        try:
            return len(PdfReader(str(chemin)).pages)
        except Exception:  # noqa: BLE001
            return None
    return None


def telecharger_source(src: dict, rafraichir: bool = False) -> str:
    """Télécharge une source officielle. Retourne : present | telecharge | hors-ligne."""
    destination = DIR_SOURCES / src["fichier"]
    if destination.exists() and destination.stat().st_size > 0 and not rafraichir:
        return "present"
    try:
        requete = urllib.request.Request(
            src["url"],
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        contexte = ssl.create_default_context()
        with urllib.request.urlopen(requete, timeout=60, context=contexte) as reponse:
            donnees = reponse.read()
        if not donnees:
            return "hors-ligne"
        destination.write_bytes(donnees)
        return "telecharge"
    except Exception:  # noqa: BLE001  (réseau indisponible : on garde la copie locale)
        return "present" if destination.exists() else "hors-ligne"


def recueillir_sources(rafraichir: bool = False) -> dict:
    """(Ré)collecte les sources Barreau + coordonnées poursuite/Cour. Retourne les états."""
    etats: dict[str, str] = {}
    for source in SOURCES + SOURCES_POURSUITE:
        etats[source["fichier"]] = telecharger_source(source, rafraichir=rafraichir)
    return etats


# ---------------------------------------------------------------------------
# TABLE A — Points de structure du dépôt (présence + conformité de la documentation)
#   fichiers  : éléments qui doivent être présents ;
#   motifs    : sous-chaînes devant figurer dans la documentation de ces éléments
#               (conformité au but du dépôt / aux exigences relevées) ;
#   controle  : vérification spéciale ('db' | 'placeholders' | 'dossier' | 'pages').
# ---------------------------------------------------------------------------
POINTS_DEPOT: list[dict] = [
    {
        "code": "DEP-01",
        "titre": "Documents d'orientation du dépôt (README racine et du pipeline)",
        "but": "Annonce le dossier (incident LVSEV25000954), l'objectif du dépôt et l'audience "
               "du 23 octobre 2026 : tout lecteur (greffe, poursuite) doit situer l'acte.",
        "reference": "Pratique de rédaction claire (Barreau du Québec) ; identification du "
                     "tribunal et du dossier",
        "criticite": "obligatoire",
        "fichiers": [README_RACINE, README_PIPELINE],
        "motifs": ["LVSEV25000954", "23 octobre 2026"],
    },
    {
        "code": "DEP-02",
        "titre": "Pipeline logiciel complet (6 scripts)",
        "but": "chemins, collecte des sources, base, orchestration, vérification des livrables "
               "et checkliste : permettent de régénérer et de contrôler les actes à tout moment.",
        "reference": "Traçabilité de la démarche (guides pratiques du Barreau)",
        "criticite": "obligatoire",
        "fichiers": [
            DIR_RACINE / "Pipeline" / "chemins.py",
            DIR_RACINE / "Pipeline" / "collect_barreau.py",
            DIR_RACINE / "Pipeline" / "build_db.py",
            DIR_RACINE / "Pipeline" / "orchestrator_legal.py",
            DIR_RACINE / "Pipeline" / "verifier_livrables.py",
            DIR_RACINE / "Pipeline" / "pipeline_checkliste.py",
        ],
        "motifs": [],
    },
    {
        "code": "DEP-03",
        "titre": "Base de traçabilité SQLite (sources, exigences, conformité, pièces)",
        "but": "Établit le lien « sources du Barreau -> exigences -> conformité -> pièces » "
               "de la demande : preuve de la méthodologie devant la Cour.",
        "reference": "Règles de fonctionnement (art. 113) ; méthode du pipeline",
        "criticite": "obligatoire",
        "fichiers": [FICHIER_DB],
        "motifs": [],
        "controle": "db",
    },
    {
        "code": "DEP-04",
        "titre": "Sources officielles téléchargées (Barreau, Fondation, Cour du Québec, DPCP, C.cr.)",
        "but": "Les exigences invoquées dans la demande doivent reposer sur les textes "
               "officiels conservés dans le dépôt (10 sources).",
        "reference": "Barreau du Québec — guides pratiques et aide-mémoires ; Fondation du "
                     "Barreau « Seul devant la cour » ; Cour du Québec ; DPCP PRE-1",
        "criticite": "obligatoire",
        "fichiers": [DIR_SOURCES / src["fichier"] for src in SOURCES],
        "motifs": [],
    },
    {
        "code": "DEP-05",
        "titre": "Coordonnées actualisées de la poursuite et de la Cour (DPCP / Cour du Québec)",
        "but": "Le guide de transmission à la poursuite doit reposer sur des coordonnées "
               "officielles téléchargées (courriel et téléphone du bureau du district de Québec).",
        "reference": "DPCP — coordonnées des points de service ; Cour du Québec — nous joindre",
        "criticite": "obligatoire",
        "fichiers": [DIR_SOURCES / src["fichier"] for src in SOURCES_POURSUITE],
        "motifs": [
            "penal.quebec@dpcp.gouv.qc.ca",
            "418 649-3500",
            "418 643-4085",
        ],
    },
    {
        "code": "DEP-06",
        "titre": "Extraits de recherche par mots-clés (avis, dépôt, greffe, pièces, requêtes)",
        "but": "Démontre que les exigences retenues ont été relevées dans les sources, "
               "et non inventées.",
        "reference": "Traçabilité — collecte et recherche dans les sources officielles",
        "criticite": "recommande",
        "fichiers": [
            DIR_EXTRAITS / "grep_avis.txt",
            DIR_EXTRAITS / "grep_depot.txt",
            DIR_EXTRAITS / "grep_greffe.txt",
            DIR_EXTRAITS / "grep_pieces.txt",
            DIR_EXTRAITS / "grep_requetes.txt",
        ],
        "motifs": [],
    },
    {
        "code": "DEP-07",
        "titre": "Pièces de preuve A-1 (lettre de décision) et A-2 (article scientifique)",
        "but": "Ce sont les pièces que la demande demande d'ajouter au dépôt légal : sans elles, "
               "la requête est privée d'objet.",
        "reference": "Règles de fonctionnement (art. 113) : liste et identification des pièces",
        "criticite": "obligatoire",
        "fichiers": [PIECE_LETTRE_DOCX, PIECE_LETTRE_PDF, PIECE_ARTICLE_PDF],
        "motifs": [],
    },
    {
        "code": "DEP-08",
        "titre": "Pièce A-3 (lettre CCQ du 25 septembre 2026) — si retenue",
        "but": "Le LISEZMOI A-3 prévoit cette lettre comme troisième pièce : sa présence "
               "ou son exclusion doit être tranchée avant transmission.",
        "reference": "Preuve/LISEZMOI_A3_CCQ_2026-09-25.md",
        "criticite": "recommande",
        "fichiers": [PIECE_A3_CCN],
        "motifs": [],
    },
    {
        "code": "DEP-09",
        "titre": "Livrables de la demande (LaTeX, PDF, dossier complet paginé)",
        "but": "Acte à déposer et à transmettre à la poursuite : doit porter l'objet "
               "« ajout d'une preuve au dépôt légal », l'incident et le dossier.",
        "reference": "Fondation du Barreau « Seul devant la cour » ; règles de rédaction claire",
        "criticite": "obligatoire",
        "fichiers": [FICHIER_TEX_DEMANDE, FICHIER_PDF_DEMANDE, FICHIER_PDF_DOSSIER_COMPLET],
        "motifs": ["ajout d'une preuve au dépôt légal", "LVSEV25000954"],
    },
    {
        "code": "DEP-10",
        "titre": "Pagination et cohérence de l'assemblage du dossier complet",
        "but": "Le dossier remis à la Cour et à la poursuite doit être complet et paginé "
               "(demande + 2 intercalaires + pièces).",
        "reference": "Règles de fonctionnement (art. 113) : présentation des pièces",
        "criticite": "obligatoire",
        "fichiers": [FICHIER_PDF_DEMANDE, FICHIER_PDF_DOSSIER_COMPLET],
        "motifs": [],
        "controle": "pages",
    },
    {
        "code": "DEP-11",
        "titre": "Rapport de conformité procédurale (18/18 exigences)",
        "but": "Documente l'évaluation des exigences du Barreau : pièce interne de diligence "
               "à verser au dossier de travail.",
        "reference": "Guides pratiques du Barreau — vérification de conformité",
        "criticite": "obligatoire",
        "fichiers": [FICHIER_RAPPORT],
        "motifs": ["18 / 18", "23 octobre 2026"],
    },
    {
        "code": "DEP-12",
        "titre": "Document source .docx (README_LEGAL) conservé pour traçabilité",
        "but": "Source des faits de la demande : permet de vérifier que rien n'a été inventé.",
        "reference": "Traçabilité — conservation des sources",
        "criticite": "obligatoire",
        "fichiers": [DOCX_SOURCE_COPY],
        "motifs": [],
    },
    {
        "code": "DEP-13",
        "titre": "Rapport présenténciel / observations (art. 721 (1) C.cr.) — LaTeX et PDF",
        "but": "Second objet du dépôt : demande de confection du rapport présenténciel pour le "
               "verdict, avec citation de l'article 721 (1), de la date et de la salle.",
        "reference": "Code criminel, art. 721 (1) ; guides de la Fondation du Barreau (peine)",
        "criticite": "obligatoire",
        "fichiers": [RAPPORT_PRESENT_TEX, RAPPORT_PRESENT_PDF],
        "motifs": ["721", "23 octobre 2026", "2.15"],
    },
    {
        "code": "DEP-14",
        "titre": "Aucun marqueur non rempli ([N° DE DOSSIER], [NOM DE L'ACCUSÉ]…) dans les actes",
        "but": "Un acte transmis avec un marqueur non rempli est irrémissible et humillant devant "
               "la Cour : il doit être complété avant tout envoi.",
        "reference": "Exigence de complétude et d'exactitude (Barreau — rédaction claire)",
        "criticite": "obligatoire",
        "fichiers": [
            FICHIER_TEX_DEMANDE,
            FICHIER_PDF_DEMANDE,
            RAPPORT_PRESENT_TEX,
            RAPPORT_PRESENT_PDF,
        ],
        "motifs": [],
        "controle": "placeholders",
    },
    {
        "code": "DEP-15",
        "titre": "Cohérence du numéro de dossier (documents vs nom du dossier local)",
        "but": "Un numéro erroné (8952 vs 8953) expose à un refus administratif du greffe ou à "
               "un retrait du document : doit être tranché avant transmission.",
        "reference": "Identification du dossier exigée par la pratique de la Chambre criminelle "
                     "et pénale",
        "criticite": "obligatoire",
        "fichiers": [],
        "motifs": [],
        "controle": "dossier",
    },
    {
        "code": "DEP-16",
        "titre": "Guide de transmission à la poursuite (procédure chronologique + coordonnées)",
        "but": "Condition de recevabilité pratique : avis écrit à la poursuite avant l'audience, "
               "avec coordonnées officielles du DPCP et procédure exacte.",
        "reference": "Fondation du Barreau « Seul devant la cour » (avis par lettre, courriel ou "
                     "télécopieur) ; DPCP — coordonnées du district de Québec",
        "criticite": "obligatoire",
        "fichiers": [GUIDE_POURSUITE],
        "motifs": [
            "penal.quebec@dpcp.gouv.qc.ca",
            "418 649-3500",
            "23 octobre 2026",
            "greffe",
        ],
    },
]

# ---------------------------------------------------------------------------
# Contrôles spéciaux (retour : présence, conformité, note, détail)
# ---------------------------------------------------------------------------
def controle_base() -> dict:
    """DEP-03 : intégrité de la base SQLite de traçabilité."""
    if not FICHIER_DB.exists():
        return {"presence": 0.0, "conformite": 0.0, "note": 0.0,
                "detail": "base depot_legal.db absente"}
    conn = sqlite3.connect(str(FICHIER_DB))
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        attendues = {"sources", "exigences", "docx_elements", "relations",
                     "conformite", "dossier", "pieces"}
        ratio_tables = len(tables & attendues) / len(attendues)
        nb_exigences = (
            conn.execute("SELECT COUNT(*) FROM exigences").fetchone()[0]
            if "exigences" in tables else 0
        )
        nb_conformes = (
            conn.execute("SELECT COUNT(*) FROM conformite WHERE statut='satisfait'").fetchone()[0]
            if "conformite" in tables else 0
        )
        nb_sources = (
            conn.execute("SELECT COUNT(*) FROM sources WHERE present=1").fetchone()[0]
            if "sources" in tables else 0
        )
    except Exception as exc:  # noqa: BLE001
        return {"presence": 0.0, "conformite": 0.0, "note": 0.0, "detail": f"base illisible : {exc}"}
    finally:
        conn.close()
    presence = round(
        10 * (0.5 * ratio_tables + 0.5 * min(nb_sources / max(len(SOURCES), 1), 1)), 1
    )
    conformite = round(
        10 * (0.5 * min(nb_exigences / 18, 1) + 0.5 * min(nb_conformes / 18, 1)), 1
    )
    return {
        "presence": presence,
        "conformite": conformite,
        "note": round((presence + conformite) / 2, 1),
        "detail": (
            f"{len(tables & attendues)}/{len(attendues)} tables ; {nb_exigences} exigences ; "
            f"{nb_conformes}/18 conformes ; {nb_sources}/{len(SOURCES)} sources présentes"
        ),
    }


def controle_placeholders(fichiers: list[pathlib.Path]) -> dict:
    """DEP-14 : marqueurs non remplis du type [NOM DE L'ACCUSÉ] dans les actes."""
    presents = [f for f in fichiers if f.exists() and f.stat().st_size > 0]
    presence = round(10 * len(presents) / max(len(fichiers), 1), 1)
    trouves: dict[str, str] = {}
    for fichier in presents:
        for marqueur in PAT_PLACEHOLDER.findall(texte_de(fichier)):
            trouves.setdefault(marqueur, fichier.name)
    conformite = 10.0 if not trouves else max(0.0, round(10 - 2.5 * len(trouves), 1))
    if trouves:
        detail = "marqueurs non remplis : " + "; ".join(
            f"{m} ({nom})" for m, nom in sorted(trouves.items())
        )
    else:
        detail = "aucun marqueur non rempli détecté"
    return {
        "presence": presence,
        "conformite": conformite,
        "note": round((presence + conformite) / 2, 1),
        "detail": detail,
    }


def controle_dossier(corpus_docs: str) -> dict:
    """DEP-15 : cohérence 8952/8953 entre les actes et le nom du dossier local."""
    if not corpus_docs.strip():
        return {"presence": 0.0, "conformite": 0.0, "note": 0.0,
                "detail": "aucun document lisible pour comparer les numéros"}
    noms = sorted({n for n in ("8952", "8953") if n in corpus_docs})
    local = sorted(set(re.findall(r"895\d", DIR_DEPOT.name)))
    incident = "présent" if "lvsev25000954" in corpus_docs else "ABSENT"
    if len(noms) == 1 and noms == local:
        note, conformite = 10.0, 10.0
    elif len(noms) == 1:
        note, conformite = 6.0, 6.0
    elif len(noms) == 2:
        note, conformite = 4.0, 4.0
    else:
        note, conformite = 3.0, 3.0
    return {
        "presence": 10.0,
        "conformite": conformite,
        "note": note,
        "detail": (
            f"numéros dans les actes : {noms or 'aucun'} ; nom du dossier local : {local or 'aucun'} ; "
            f"incident LVSEV25000954 : {incident}"
        ),
    }


def controle_pages() -> dict:
    """DEP-10 : pagination de la demande et cohérence de l'assemblage du dossier complet."""
    p_dem = pages_de(FICHIER_PDF_DEMANDE)
    p_dos = pages_de(FICHIER_PDF_DOSSIER_COMPLET)
    p_let = pages_de(PIECE_LETTRE_PDF)
    p_art = pages_de(PIECE_ARTICLE_PDF)
    lisibles = sum(v is not None for v in (p_dem, p_dos))
    presence = round(10 * lisibles / 2, 1)
    if lisibles < 2:
        return {"presence": presence, "conformite": 0.0, "note": 0.0,
                "detail": "PDF de la demande ou du dossier complet illisible/absent"}
    attendu = (p_dem or 0) + 2 + (p_let or 0) + (p_art or 0)
    ok_dem = p_dem >= 5
    ok_dos = p_dos >= 40
    ok_coh = (p_dos == attendu) if None not in (p_let, p_art) else False
    conformite = round(10 * (0.4 * ok_dem + 0.3 * ok_dos + 0.3 * ok_coh), 1)
    return {
        "presence": presence,
        "conformite": conformite,
        "note": round((presence + conformite) / 2, 1),
        "detail": (
            f"demande = {p_dem} pages ; dossier complet = {p_dos} pages ; "
            f"attendu = {attendu} (demande + 2 intercalaires + A-1 ({p_let}) + A-2 ({p_art})) ; "
            f"cohérence {'OK' if ok_coh else 'À VÉRIFIER'}"
        ),
    }


# ---------------------------------------------------------------------------
# Évaluation : statut, pondération, table A (structure), table B (exigences)
# ---------------------------------------------------------------------------
def statut_de(note: float) -> str:
    if note >= 9:
        return "Conforme"
    if note >= 7:
        return "À améliorer"
    if note >= 4:
        return "Partiel"
    return "Non conforme"


def poids_de(criticite: str, table: str) -> float:
    """Exigences du Barreau (table B) pesées doublement ; structure : 1,5 si obligatoire."""
    if table == "B":
        return 2.0 if criticite == "obligatoire" else 1.0
    return 1.5 if criticite == "obligatoire" else 1.0


def evaluer_structure(corpus_docs: str) -> list[dict]:
    """Table A : présence des points du dépôt + conformité de leur documentation."""
    lignes: list[dict] = []
    for point in POINTS_DEPOT:
        controle = point.get("controle")
        if controle == "db":
            resultat = controle_base()
        elif controle == "placeholders":
            resultat = controle_placeholders(point["fichiers"])
        elif controle == "dossier":
            resultat = controle_dossier(corpus_docs)
        elif controle == "pages":
            resultat = controle_pages()
        else:
            fichiers = point.get("fichiers", [])
            presents = [f for f in fichiers if f.exists() and f.stat().st_size > 0]
            presence = round(10 * len(presents) / len(fichiers), 1) if fichiers else 10.0
            motifs = point.get("motifs", [])
            morceaux: list[str] = []
            if motifs:
                contenu = normaliser(" ".join(texte_de(f) for f in presents))
                trouves = [m for m in motifs if normaliser(m) in contenu]
                manquants = [m for m in motifs if m not in trouves]
                conformite = round(10 * len(trouves) / len(motifs), 1)
                note = round((presence + conformite) / 2, 1)
                morceaux.append(f"{len(trouves)}/{len(motifs)} motifs de contenu trouvés")
                if manquants:
                    morceaux.append("manquant : " + ", ".join(manquants))
            else:
                conformite = presence
                note = presence
                morceaux.append("présence seule (aucun motif de contenu requis)")
            absents = [f.name for f in fichiers if not (f.exists() and f.stat().st_size > 0)]
            if absents:
                morceaux.append("fichiers absents : " + ", ".join(absents))
            resultat = {
                "presence": presence,
                "conformite": conformite,
                "note": note,
                "detail": " ; ".join(morceaux),
            }
        lignes.append(
            {
                "table": "A",
                "code": point["code"],
                "categorie": "Structure du dépôt",
                "titre": point["titre"],
                "reference": point["reference"],
                "criticite": point["criticite"],
                "presence": resultat["presence"],
                "conformite": resultat["conformite"],
                "note": resultat["note"],
                "statut": statut_de(resultat["note"]),
                "detail": resultat["detail"],
            }
        )
    return lignes


def evaluer_exigences(corpus_final: str) -> list[dict]:
    """Table B : exigences du Barreau (build_db.EXIGENCES) vérifiées dans les actes."""
    presence_doc = (
        10.0
        if any(
            f.exists() and f.stat().st_size > 0
            for f in (FICHIER_PDF_DEMANDE, FICHIER_TEX_DEMANDE)
        )
        else 0.0
    )
    corpus = normaliser(corpus_final)
    lignes: list[dict] = []
    for exigence in build_db.EXIGENCES:
        motifs = [v["motif"] for v in exigence["verif"] if v.get("corpus") == "final"]
        trouves = [m for m in motifs if normaliser(m) in corpus]
        manquants = [m for m in motifs if m not in trouves]
        note = round(10 * len(trouves) / len(motifs), 1) if motifs else 10.0
        detail = f"{len(trouves)}/{len(motifs)} motifs trouvés"
        if manquants:
            detail += " ; manquants : " + ", ".join(manquants)
        lignes.append(
            {
                "table": "B",
                "code": exigence["code"],
                "categorie": exigence["categorie"],
                "titre": exigence["titre"],
                "reference": exigence.get("reference", ""),
                "criticite": exigence["criticite"],
                "presence": presence_doc,
                "conformite": note,
                "note": note,
                "statut": statut_de(note),
                "detail": detail,
            }
        )
    return lignes


def synthetiser(lignes: list[dict]) -> dict:
    """Note globale pondérée, minimum des points obligatoires, moyennes par catégorie."""
    total_poids = sum(poids_de(l["criticite"], l["table"]) for l in lignes) or 1.0
    globale = sum(l["note"] * poids_de(l["criticite"], l["table"]) for l in lignes) / total_poids
    obligatoires = [l["note"] for l in lignes if l["criticite"] == "obligatoire"]
    categories: dict[str, list[float]] = {}
    for ligne in lignes:
        categories.setdefault(ligne["categorie"], []).append(ligne["note"])
    return {
        "globale": round(globale, 2),
        "min_obligatoire": min(obligatoires) if obligatoires else 10.0,
        "categories": {
            cat: round(sum(valeurs) / len(valeurs), 1)
            for cat, valeurs in sorted(categories.items())
        },
        "nb_points": len(lignes),
        "nb_obligatoires": len(obligatoires),
    }


def verdict_de(globale: float, min_obligatoire: float) -> str:
    if globale >= 9.0 and min_obligatoire >= 9.0:
        return "🟢 NIVEAU ACCEPTABLE — dépôt conforme à son but et aux exigences du Barreau"
    if globale >= 8.0 and min_obligatoire >= 7.0:
        return "🟡 NIVEAU ACCEPTABLE SOUS RÉSERVES — corriger les points sous 8/10 avant transmission"
    if globale >= 8.0:
        return ("🟠 BON NIVEAU GLOBAL MAIS POINTS OBLIGATOIRES BLOQUANTS — corriger les points "
                "obligatoires sous 7/10 AVANT tout envoi à la poursuite")
    if globale >= 6.5:
        return "🟠 NIVEAU INSUFFISANT — corrections requises avant le 23 octobre 2026"
    return "🔴 NON CONFORME — refonte nécessaire avant le 23 octobre 2026"


# ---------------------------------------------------------------------------
# Rapport markdown + affichage console
# ---------------------------------------------------------------------------
def _md(valeur) -> str:
    return str(valeur).replace("|", "\\|").replace("\n", " ").strip()


def ecrire_rapport(
    table_a: list[dict],
    table_b: list[dict],
    synthese: dict,
    verdict: str,
    etat_sources: dict,
    seuil: float,
    horodatage: str,
) -> pathlib.Path:
    """Écrit le rapport de checklist (table des points, scores 0-10, recommandations)."""
    lignes: list[str] = []
    ajouter = lignes.append
    ajouter("# Checklist du dépôt complet — conformité Barreau / audience du 23 octobre 2026")
    ajouter("")
    ajouter(f"**Généré le :** {horodatage} — `pipeline_checkliste.py`")
    ajouter("")
    ajouter(
        "**But du dépôt :** requête en ajout d'une preuve au dépôt légal **+** dépôt d'un "
        "rapport présenténciel (art. 721 (1) C.cr.) pour le verdict — **audience du vendredi "
        "23 octobre 2026 à 9 h 30, salle 2.15, Palais de justice de Québec** "
        "(Cour du Québec, Chambre criminelle et pénale, district de Québec ; incident "
        "LVSEV25000954)."
    )
    ajouter("")
    ajouter("**Échelle :** 0 (le plus bas) à 10 (le plus haut) ; "
            "≥ 9 Conforme · 7 à 8,9 À améliorer · 4 à 6,9 Partiel · < 4 Non conforme.")
    ajouter("")
    ajouter("## 1. Bilan")
    ajouter("")
    ajouter("| Indicateur | Valeur |")
    ajouter("|---|---|")
    ajouter(f"| **Note globale pondérée /10** | **{synthese['globale']:.2f}** |")
    ajouter(f"| Verdict | {verdict} |")
    ajouter(f"| Seuil de réussite retenu | {seuil:.1f}/10 |")
    ajouter(f"| Points évalués | {synthese['nb_points']} "
            f"({len(table_a)} de structure + {len(table_b)} exigences Barreau) |")
    ajouter(f"| Points obligatoires | {synthese['nb_obligatoires']} |")
    ajouter(f"| Note la plus faible parmi les obligatoires | {synthese['min_obligatoire']:.1f}/10 |")
    ajouter("")
    ajouter("## 2. Table A — Points de structure du dépôt (présence + conformité documentation)")
    ajouter("")
    ajouter("| Code | Point | Référence (Barreau / organisme) | Criticité | Présence /10 | "
            "Conformité /10 | **Note /10** | Statut | Détail |")
    ajouter("|---|---|---|---|---:|---:|---:|---|---|")
    for l in table_a:
        ajouter(
            f"| `{l['code']}` | {_md(l['titre'])} | {_md(l['reference'])} | {l['criticite']} | "
            f"{l['presence']:.1f} | {l['conformite']:.1f} | **{l['note']:.1f}** | "
            f"{l['statut']} | {_md(l['detail'])} |"
        )
    ajouter("")
    ajouter("## 3. Table B — Exigences du Barreau pour la documentation de la requête")
    ajouter("")
    ajouter("| Code | Catégorie | Exigence | Référence | Criticité | **Note /10** | Statut | "
            "Vérification |")
    ajouter("|---|---|---|---|---|---:|---|---|")
    for l in table_b:
        ajouter(
            f"| `{l['code']}` | {l['categorie']} | {_md(l['titre'])} | {_md(l['reference'])} | "
            f"{l['criticite']} | **{l['note']:.1f}** | {l['statut']} | {_md(l['detail'])} |"
        )
    ajouter("")
    ajouter("## 4. Synthèse par catégorie (moyenne /10)")
    ajouter("")
    ajouter("| Catégorie | Moyenne /10 |")
    ajouter("|---|---:|")
    for categorie, moyenne in synthese["categories"].items():
        ajouter(f"| {categorie} | {moyenne:.1f} |")
    ajouter("")
    ajouter("## 5. Recommandations avant le 23 octobre 2026 (points sous 8/10)")
    ajouter("")
    faibles = sorted(
        (l for l in table_a + table_b if l["note"] < 8),
        key=lambda l: (l["note"], l["code"]),
    )
    if not faibles:
        ajouter("_Aucun point sous 8/10 : le dépôt atteint le niveau attendu._")
    else:
        for l in faibles:
            ajouter(
                f"1. **`{l['code']}` — {l['titre']} : {l['note']:.1f}/10** ({l['statut']}). "
                f"Détail : {_md(l['detail'])}."
            )
    ajouter("")
    ajouter("## 6. Sources officielles téléchargées / présentes")
    ajouter("")
    ajouter("| Fichier source | État |")
    ajouter("|---|---|")
    for fichier, etat in sorted(etat_sources.items()):
        ajouter(f"| `{fichier}` | {etat} |")
    ajouter("")
    chemin = DIR_SORTIE / "checklist_conformite.md"
    chemin.write_text("\n".join(lignes), encoding="utf-8")
    return chemin


def afficher_console(
    table_a: list[dict],
    table_b: list[dict],
    synthese: dict,
    verdict: str,
    rapport: pathlib.Path,
) -> None:
    """Tableau récapitulatif en console (sans émoji : compatibilité Windows)."""
    print("=" * 118)
    print("CHECKLIST DU DÉPÔT COMPLET — Barreau du Québec / audience 23 octobre 2026, 9 h 30, salle 2.15")
    print("=" * 118)
    print(f"{'CODE':<9} {'CATÉGORIE':<20} {'POINT / EXIGENCE':<58} {'NOTE':>6}  STATUT")
    print("-" * 118)
    for ligne in table_a + table_b:
        titre = ligne["titre"][:56] + ("…" if len(ligne["titre"]) > 56 else "")
        print(
            f"{ligne['code']:<9} {ligne['categorie'][:20]:<20} {titre:<58} "
            f"{ligne['note']:>5.1f}  {ligne['statut']}"
        )
    print("-" * 118)
    print(f"NOTE GLOBALE PONDÉRÉE : {synthese['globale']:.2f} / 10   |   "
          f"minimum obligatoire : {synthese['min_obligatoire']:.1f} / 10")
    print(f"VERDICT : {verdict}")
    print(f"Rapport : {rapport}")
    print("=" * 118)


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------
def construire_corpus_final() -> str:
    """Texte des actes destinés au tribunal (demande + dossier complet paginé)."""
    return " ".join(
        texte_de(f)
        for f in (FICHIER_TEX_DEMANDE, FICHIER_PDF_DEMANDE, FICHIER_PDF_DOSSIER_COMPLET)
    )


def construire_corpus_docs() -> str:
    """Texte normalisé des documents servant à comparer numéros de dossier et incident."""
    return normaliser(
        " ".join(
            texte_de(f)
            for f in (
                FICHIER_TEX_DEMANDE,
                FICHIER_PDF_DEMANDE,
                FICHIER_PDF_DOSSIER_COMPLET,
                RAPPORT_PRESENT_TEX,
                RAPPORT_PRESENT_PDF,
                README_RACINE,
                README_PIPELINE,
            )
        )
    )


def main(argv: list[str] | None = None) -> int:
    analyseur = argparse.ArgumentParser(
        description=(
            "Checklist du dépôt complet : points de présence + conformité de la "
            "documentation aux exigences du Barreau, notés de 0 à 10."
        )
    )
    analyseur.add_argument(
        "--rafraichir",
        action="store_true",
        help="re-télécharger toutes les sources officielles (ignore les copies locales)",
    )
    analyseur.add_argument(
        "--sans-telechargement",
        action="store_true",
        help="ne rien télécharger : n'utilise que les copies déjà présentes (hors ligne)",
    )
    analyseur.add_argument(
        "--seuil",
        type=float,
        default=8.0,
        help="note globale minimale pour un code retour 0 (défaut : 8.0)",
    )
    args = analyseur.parse_args(argv)

    horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    print("[1/4] Collecte des sources officielles (Barreau, Fondation, Cour du Québec, DPCP)…")
    if args.sans_telechargement:
        etat_sources = {
            source["fichier"]: (
                "present" if (DIR_SOURCES / source["fichier"]).exists() else "non téléchargé"
            )
            for source in SOURCES + SOURCES_POURSUITE
        }
    else:
        etat_sources = recueillir_sources(rafraichir=args.rafraichir)
    nb_disponibles = sum(1 for v in etat_sources.values() if v in ("present", "telecharge"))
    print(f"      {nb_disponibles}/{len(etat_sources)} sources disponibles.")

    print("[2/4] Extraction du texte des livrables…")
    corpus_final = construire_corpus_final()
    corpus_docs = construire_corpus_docs()
    print(
        f"      corpus actes : {len(corpus_final)} caractères ; "
        f"corpus documents : {len(corpus_docs)} caractères."
    )

    print("[3/4] Évaluation de la table des points (échelle 0 à 10)…")
    table_a = evaluer_structure(corpus_docs)
    table_b = evaluer_exigences(corpus_final)
    synthese = synthetiser(table_a + table_b)
    verdict = verdict_de(synthese["globale"], synthese["min_obligatoire"])
    print(
        f"      {synthese['nb_points']} points évalués ; "
        f"globale = {synthese['globale']:.2f}/10 ; "
        f"minimum obligatoire = {synthese['min_obligatoire']:.1f}/10."
    )

    print("[4/4] Génération du rapport…")
    rapport = ecrire_rapport(
        table_a, table_b, synthese, verdict, etat_sources, args.seuil, horodatage
    )
    afficher_console(table_a, table_b, synthese, verdict, rapport)

    conforme = synthese["globale"] >= args.seuil and synthese["min_obligatoire"] >= 6.0
    return 0 if conforme else 1


if __name__ == "__main__":
    raise SystemExit(main())








