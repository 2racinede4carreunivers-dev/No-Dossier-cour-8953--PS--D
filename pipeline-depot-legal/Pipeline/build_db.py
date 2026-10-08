"""Construction de la base SQLite « depot_legal.db ».

La base contient :
  * sources      : documents du Barreau / textes de référence téléchargés ;
  * exigences    : points à respecter pour que la demande soit recevable ;
  * docx_elements: paragraphes du document source (.docx) ;
  * relations    : liens « schéma neuronal » exigences <-> éléments du .docx ;
  * conformite   : évaluation par l'orchestrateur (remplie par orchestrator_legal.py) ;
  * dossier      : métadonnées du dossier (incident, audience, identité…).

Usage :  python build_db.py
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sqlite3
import sys

from collect_barreau import SOURCES
from docx_reader import DEFAULT_DOCX, read_paragraphs
from chemins import DIR_PIPELINE as BASE, DIR_SOURCES, FICHIER_DB as DB_CHEMIN

# ---------------------------------------------------------------------------
# Exigences : chaque point à respecter, sa source et sa vérification.
#   verif = liste de {corpus: 'final'|'docx', motif: sous-chaîne recherchée}
#   obligatoire=True -> vérification bloquante pour la conformité
# ---------------------------------------------------------------------------
EXIGENCES: list[dict] = [
    {
        "code": "FORME-01",
        "source": "BARREAU_MTL_CQCRIM",
        "categorie": "Forme",
        "titre": "Identification complète du tribunal et du dossier",
        "detail": "Le document doit identifier la Cour, la chambre, le district, le numéro "
                  "d'incident et le numéro de dossier avant tout exposé.",
        "reference": "Pratique de la Chambre criminelle et pénale (outils du Barreau) ; "
                     "guides de la Fondation du Barreau",
        "criticite": "obligatoire",
        "cles_docx": ["incident", "dossier"],
        "verif": [
            {"corpus": "final", "motif": "CHAMBRE CRIMINELLE ET PÉNALE"},
            {"corpus": "final", "motif": "LVSEV25000954"},
            {"corpus": "final", "motif": "8953"},
        ],
        "action": "Titre d'identification généré automatiquement en tête du document.",
    },
    {
        "code": "FORME-02",
        "source": "FONDATION_SEUL_DEVANT",
        "categorie": "Forme",
        "titre": "Objet de la demande énoncé clairement",
        "detail": "L'objet de la demande doit être explicite dès les premières lignes "
                  "(« Demande d'ajout d'une preuve au dépôt légal »).",
        "reference": "Seul devant la cour, p. 36 ; guides de préparation à la cour",
        "criticite": "obligatoire",
        "cles_docx": ["Objet"],
        "verif": [{"corpus": "final", "motif": "ajout d’une preuve au dépôt légal"}],
        "action": "",
    },
    {
        "code": "FORME-03",
        "source": "FONDATION_PREP_CRIM",
        "categorie": "Forme",
        "titre": "Identité et adresse complètes du demandeur",
        "detail": "Nom complet et adresse à jour doivent figurer ; la cour et la poursuite "
                  "doivent pouvoir joindre le demandeur.",
        "reference": "Guide « Préparer la cour – criminel », avis de changement d'adresse",
        "criticite": "obligatoire",
        "cles_docx": ["Menuet", "Savard"],
        "verif": [{"corpus": "final", "motif": "rue du Menuet"}],
        "action": "",
    },
    {
        "code": "FORME-04",
        "source": "CQ_REGLES_GESTION",
        "categorie": "Forme",
        "titre": "Date, heure, salle et palais de justice de l'audience",
        "detail": "L'acte doit viser l'audience à laquelle il sera présenté "
                  "(23 octobre 2026, 9 h 30, salle 2.15, palais de justice de Québec).",
        "reference": "Règles de fonctionnement (art. 113 du Règlement de la Cour du Québec)",
        "criticite": "obligatoire",
        "cles_docx": [],
        "verif": [
            {"corpus": "final", "motif": "23 octobre 2026"},
            {"corpus": "final", "motif": "9 h 30"},
            {"corpus": "final", "motif": "2.15"},
        ],
        "action": "Informations d'audience insérées dans l'en-tête.",
    },
    {
        "code": "FORME-05",
        "source": "FONDATION_SEUL_DEVANT",
        "categorie": "Forme",
        "titre": "Signature et date",
        "detail": "L'acte est signé et daté par la personne qui le présente.",
        "reference": "Seul devant la cour : la partie assume la présentation de sa demande",
        "criticite": "obligatoire",
        "cles_docx": [],
        "verif": [{"corpus": "final", "motif": "Fait à Lévis"}],
        "action": "Bloc de signature généré en fin de document.",
    },
    {
        "code": "FORME-06",
        "source": "FONDATION_PREP_CRIM",
        "categorie": "Forme",
        "titre": "Copie transmise à la poursuite",
        "detail": "Une copie complète de la demande et des pièces est remise à la poursuite "
                  "avant l'audience.",
        "reference": "Guide « Préparer la cour » : transmission à la poursuite par lettre, "
                     "courriel ou télécopieur",
        "criticite": "obligatoire",
        "cles_docx": [],
        "verif": [{"corpus": "final", "motif": "Copie à la poursuite"}],
        "action": "Mention « Copie à la poursuite » générée.",
    },
    {
        "code": "AVIS-01",
        "source": "FONDATION_SEUL_DEVANT",
        "categorie": "Avis",
        "titre": "Avis écrit à la poursuite avant le début de l'audience",
        "detail": "La loi impose d'aviser la poursuite de l'intention de produire des "
                  "documents à l'appui de la défense avant le début du procès ; l'avis est "
                  "donné par lettre, courriel ou télécopieur.",
        "reference": "Seul devant la cour, étape 6, p. 36 (« la loi exige que vous avisiez "
                     "la poursuite »)",
        "criticite": "obligatoire",
        "cles_docx": [],
        "verif": [{"corpus": "final", "motif": "Avis à la poursuite et à la Cour"}],
        "action": "Section d'avis générée ; transmettre réellement avant le 23 octobre 2026.",
    },
    {
        "code": "AVIS-02",
        "source": "FONDATION_PREP_CRIM",
        "categorie": "Avis",
        "titre": "Avis à la Cour et à la partie adverse de l'intention de présenter la demande",
        "detail": "Il faut aviser le juge et la poursuite de l'intention de présenter la "
                  "demande ; l'avis est en principe écrit et transmis avant l'audience, "
                  "mais le juge peut en décider autrement.",
        "reference": "Guide « Préparer la cour – criminel » (requêtes) ; Seul devant la cour",
        "criticite": "obligatoire",
        "cles_docx": [],
        "verif": [{"corpus": "final", "motif": "avise la Cour et la poursuite"}],
        "action": "",
    },
    {
        "code": "AVIS-03",
        "source": "FONDATION_SEUL_DEVANT",
        "categorie": "Avis",
        "titre": "Demande structurée malgré l'absence de procédures strictes",
        "detail": "Il n'existe pas de procédures strictes pour de telles demandes : le "
                  "document doit donc se suffire à lui-même (objet, motifs, pièces, avis, "
                  "signature).",
        "reference": "Seul devant la cour : « Il n'y a pas de procédures strictes pour de "
                     "telles requêtes »",
        "criticite": "recommande",
        "cles_docx": [],
        "verif": [{"corpus": "final", "motif": "aucune procédure stricte"}],
        "action": "",
    },
    {
        "code": "PREUVE-01",
        "source": "CQ_REGLES_GESTION",
        "categorie": "Preuve",
        "titre": "Liste des pièces",
        "detail": "Le juge peut exiger une liste des pièces : chaque document à déposer doit "
                  "être désigné et numéroté.",
        "reference": "Règles de fonctionnement (art. 113 du Règlement de la Cour du Québec), "
                     "par. 2) d)",
        "criticite": "obligatoire",
        "cles_docx": ["preuve déposée", "preuve recherchée"],
        "verif": [{"corpus": "final", "motif": "Liste des pièces proposées au dépôt"}],
        "action": "Liste des pièces (A-1 : lettre et courriel ; A-2 : article) générée.",
    },
    {
        "code": "PREUVE-02",
        "source": "CQ_REGLES_GESTION",
        "categorie": "Preuve",
        "titre": "Énoncé sommaire expliquant la preuve et sa finalité",
        "detail": "Le juge peut exiger un énoncé sommaire de la preuve : le document doit "
                  "expliquer ce que la preuve démontre.",
        "reference": "Règles de fonctionnement, par. 2) a)",
        "criticite": "obligatoire",
        "cles_docx": ["Motifs de la demande"],
        "verif": [{"corpus": "final", "motif": "énoncé sommaire"}],
        "action": "",
    },
    {
        "code": "PREUVE-03",
        "source": "BARREAU_PROC_PENALE",
        "categorie": "Preuve",
        "titre": "Motifs de pertinence (lien avec les questions en litige)",
        "detail": "L'acte doit relier la preuve aux questions soulevées au dossier "
                  "(identité professionnelle, conduite de l'enquête, mise en examen).",
        "reference": "Procédure pénale (aide-mémoire du Barreau) : vérifier toute question "
                     "de preuve ressortant de la communication de la preuve",
        "criticite": "obligatoire",
        "cles_docx": ["Motifs de la demande", "influencer"],
        "verif": [{"corpus": "final", "motif": "Motifs de la demande"}],
        "action": "",
    },
    {
        "code": "PREUVE-04",
        "source": "DPCP_PRE_1",
        "categorie": "Preuve",
        "titre": "Identification précise de chaque pièce (auteur, objet, source)",
        "detail": "Chaque pièce doit être identifiable : qui l'a émise, à quelle date, quel "
                  "en est l'objet (lettre du comité de sélection, article d'environ 35 pages).",
        "reference": "Directive de pratique PRE-1 (communication de la preuve)",
        "criticite": "obligatoire",
        "cles_docx": ["Journal canadien", "Cher professeur Savard", "Géométrie du spectre"],
        "verif": [
            {"corpus": "final", "motif": "Journal canadien de mathématiques"},
            {"corpus": "final", "motif": "Cher professeur Savard"},
            {"corpus": "final", "motif": "Géométrie du spectre des nombres premiers"},
        ],
        "action": "Ajouter, si possible, la date du courriel et le nom des deux signataires.",
    },
    {
        "code": "PREUVE-05",
        "source": "FONDATION_SEUL_DEVANT",
        "categorie": "Preuve",
        "titre": "Copies en nombre suffisant et lisibles",
        "detail": "Prévoir des copies papier lisibles de chaque pièce pour la Cour, la "
                  "poursuite et le dossier.",
        "reference": "Seul devant la cour : « Renseignez-vous sur les exigences "
                     "procédurales lors du dépôt de tels documents »",
        "criticite": "recommande",
        "cles_docx": [],
        "verif": [{"corpus": "final", "motif": "exemplaires"}],
        "action": "",
    },
    {
        "code": "CONF-01",
        "source": "CC_486",
        "categorie": "Confidentialité",
        "titre": "Demande de confidentialité motivée par un fondement juridique",
        "detail": "La demande de protection de renseignements doit indiquer son fondement "
                  "(loi, Charte, pouvoir discrétionnaire de la Cour) et sa portée précise.",
        "reference": "Code criminel, art. 486 à 486.5 (fondement et avis des ordonnances "
                     "de non-publication)",
        "criticite": "obligatoire",
        "cles_docx": ["Demande de confidentialité", "confidentialité"],
        "verif": [{"corpus": "final", "motif": "fondement"}],
        "action": "Ajouter le fondement juridique invoqué par le demandeur.",
    },
    {
        "code": "CONF-02",
        "source": "FONDATION_PREP_CRIM",
        "categorie": "Confidentialité",
        "titre": "Avis de la demande de confidentialité aux parties intéressées",
        "detail": "La demande de confidentialité doit être portée à la connaissance de la "
                  "poursuite et de toute partie intéressée, sinon elle ne peut être "
                  "accordée à leur égard.",
        "reference": "Guide « Préparer la cour » : règles particulières de confidentialité",
        "criticite": "obligatoire",
        "cles_docx": ["menaces", "confidentialité"],
        "verif": [{"corpus": "final", "motif": "toute partie intéressée"}],
        "action": "",
    },
    {
        "code": "DEROUL-01",
        "source": "BARREAU_PROC_PENALE",
        "categorie": "Déroulement",
        "titre": "État de la communication (divulgation) de la preuve vérifié",
        "detail": "Avant l'audience, vérifier si la preuve a été communiquée et si des "
                  "documents demeurent non communiqués, ce qui justifie l'ajout d'une pièce "
                  "au dépôt du dossier.",
        "reference": "Procédure pénale (aide-mémoire), p. 9 ; directive PRE-1",
        "criticite": "recommande",
        "cles_docx": ["communication reçue", "communication comprend"],
        "verif": [{"corpus": "final", "motif": "communication de la preuve"}],
        "action": "",
    },
    {
        "code": "DEROUL-02",
        "source": "CQ_REGLES_GESTION",
        "categorie": "Déroulement",
        "titre": "Demande présentée oralement lors de l'appel du dossier",
        "detail": "La demande écrite est accompagnée d'une présentation orale au moment de "
                  "l'appel du dossier ; les décisions sont consignées au procès-verbal.",
        "reference": "Règles de fonctionnement (art. 113) : décisions consignées au "
                     "procès-verbal transmis aux parties",
        "criticite": "recommande",
        "cles_docx": [],
        "verif": [{"corpus": "final", "motif": "appel du dossier"}],
        "action": "",
    },
]

# ---------------------------------------------------------------------------
# Schéma de la base (le « schéma neuronal » : sources -> exigences -> éléments)
# ---------------------------------------------------------------------------
SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    id            TEXT PRIMARY KEY,
    organisme     TEXT NOT NULL,
    titre         TEXT NOT NULL,
    type          TEXT NOT NULL,
    url           TEXT,
    fichier       TEXT,
    present       INTEGER NOT NULL DEFAULT 0,
    octets        INTEGER,
    date_collecte TEXT,
    note          TEXT
);

CREATE TABLE IF NOT EXISTS exigences (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    code       TEXT UNIQUE NOT NULL,
    source_id  TEXT NOT NULL REFERENCES sources(id),
    categorie  TEXT NOT NULL,
    titre      TEXT NOT NULL,
    detail     TEXT NOT NULL,
    reference  TEXT,
    criticite  TEXT NOT NULL CHECK (criticite IN ('obligatoire', 'recommande', 'informatif')),
    action     TEXT,
    verif_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS docx_elements (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ordre   INTEGER NOT NULL,
    type    TEXT NOT NULL CHECK (type IN ('entete', 'titre', 'paragraphe', 'puces')),
    section TEXT,
    texte   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS relations (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    exigence_id    INTEGER NOT NULL REFERENCES exigences(id),
    element_id     INTEGER REFERENCES docx_elements(id) ON DELETE SET NULL,
    poids          REAL NOT NULL DEFAULT 0.5,
    type_lien      TEXT NOT NULL,
    justification  TEXT
);

CREATE TABLE IF NOT EXISTS conformite (
    exigence_id   INTEGER PRIMARY KEY REFERENCES exigences(id),
    statut        TEXT NOT NULL CHECK (statut IN ('satisfait', 'partiel', 'non_satisfait', 'informatif')),
    trouves_json  TEXT,
    manquants_json TEXT,
    commentaire   TEXT,
    eval_le       TEXT
);

CREATE TABLE IF NOT EXISTS dossier (
    cle   TEXT PRIMARY KEY,
    valeur TEXT
);

CREATE TABLE IF NOT EXISTS pieces (
    code        TEXT PRIMARY KEY,
    libelle     TEXT NOT NULL,
    chemin      TEXT,
    present     INTEGER NOT NULL DEFAULT 0,
    pages       INTEGER,
    details     TEXT,
    verifie_le  TEXT
);

CREATE INDEX IF NOT EXISTS idx_rel_ex ON relations(exigence_id);

CREATE VIEW IF NOT EXISTS vue_schema_neuronal AS
SELECT  e.code                AS exigence,
        e.categorie           AS categorie,
        e.criticite           AS criticite,
        e.titre               AS exigence_texte,
        s.organisme           AS organisme_source,
        s.titre               AS source,
        COUNT(DISTINCT r.element_id) AS elements_lies,
        COALESCE(c.statut, 'non_evalue') AS statut,
        COALESCE(c.commentaire, '')     AS commentaire
FROM      exigences e
JOIN      sources   s ON s.id = e.source_id
LEFT JOIN relations r ON r.exigence_id = e.id
LEFT JOIN conformite c ON c.exigence_id = e.id
GROUP BY  e.code;
"""


def normaliser(texte: str) -> str:
    """Minuscules, apostrophes droites : pour les comparaisons."""
    return texte.lower().replace("’", "'")


def charger_sources(conn: sqlite3.Connection) -> None:
    """Insère/met à jour la table des sources à partir du manifeste de collecte."""
    now = datetime.date.today().isoformat()
    for src in SOURCES:
        chemin = DIR_SOURCES / src["fichier"]
        present = int(chemin.exists() and chemin.stat().st_size > 0)
        conn.execute(
            """INSERT INTO sources (id, organisme, titre, type, url, fichier, present,
                                    octets, date_collecte, note)
               VALUES (?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET
                 organisme=excluded.organisme, titre=excluded.titre, type=excluded.type,
                 url=excluded.url, fichier=excluded.fichier, present=excluded.present,
                 octets=excluded.octets, date_collecte=excluded.date_collecte,
                 note=excluded.note""",
            (
                src["id"], src["organisme"], src["titre"], src["type"], src["url"],
                src["fichier"], present,
                chemin.stat().st_size if present else None,
                now, src.get("note", ""),
            ),
        )


def charger_exigences(conn: sqlite3.Connection) -> None:
    for ex in EXIGENCES:
        conn.execute(
            """INSERT INTO exigences (code, source_id, categorie, titre, detail, reference,
                                      criticite, action, verif_json)
               VALUES (?,?,?,?,?,?,?,?,?)
               ON CONFLICT(code) DO UPDATE SET
                 source_id=excluded.source_id, categorie=excluded.categorie,
                 titre=excluded.titre, detail=excluded.detail, reference=excluded.reference,
                 criticite=excluded.criticite, action=excluded.action,
                 verif_json=excluded.verif_json""",
            (
                ex["code"], ex["source"], ex["categorie"], ex["titre"], ex["detail"],
                ex.get("reference", ""), ex["criticite"], ex.get("action", ""),
                json.dumps(ex["verif"], ensure_ascii=False),
            ),
        )


def charger_elements(conn: sqlite3.Connection, paragraphes: list[dict]) -> None:
    """Réinitialise les éléments du .docx dans la base (entete / titre / paragraphe / puces)."""
    conn.execute("DELETE FROM docx_elements")
    conn.execute("DELETE FROM relations WHERE element_id IS NOT NULL")
    section = None
    for p in paragraphes:
        texte = p["text"].strip()
        if p["i"] <= 2:
            type_el = "entete"
        elif p["bold"] and not p["bullet"] and len(texte) < 90:
            type_el = "titre"
            section = re.sub(r"^Objet\s*:\s*", "", texte)
        elif p["bullet"]:
            type_el = "puces"
        else:
            type_el = "paragraphe"
        conn.execute(
            "INSERT INTO docx_elements (ordre, type, section, texte) VALUES (?,?,?,?)",
            (p["i"], type_el, section, texte),
        )


def lier_exigences(conn: sqlite3.Connection) -> int:
    """Construit les relations exigences <-> éléments du .docx (le « schéma neuronal »)."""
    conn.execute("DELETE FROM relations")
    lignes = conn.execute("SELECT id, type, texte FROM docx_elements ORDER BY ordre").fetchall()
    insertion = (
        "INSERT INTO relations (exigence_id, element_id, poids, type_lien, justification) "
        "VALUES (?,?,?,?,?)"
    )
    nb = 0
    for ex in EXIGENCES:
        exigence_id = conn.execute(
            "SELECT id FROM exigences WHERE code=?", (ex["code"],)
        ).fetchone()[0]
        if not ex["cles_docx"]:
            conn.execute(
                insertion,
                (exigence_id, None, 0.0, "completement_par_titre",
                 "Exigence comblée par les sections générées par le pipeline."),
            )
            nb += 1
            continue
        trouve = False
        for id_el, type_el, texte in lignes:
            cible = normaliser(texte)
            if any(normaliser(cle) in cible for cle in ex["cles_docx"]):
                poids = 1.0 if type_el in ("titre", "entete") else 0.6
                conn.execute(
                    insertion,
                    (exigence_id, id_el, poids, "traite_de",
                     "Mot-clé de l'exigence présent dans ce paragraphe du .docx."),
                )
                nb += 1
                trouve = True
        if not trouve:
            conn.execute(
                insertion,
                (exigence_id, None, 0.0, "absent_du_docx",
                 "Aucun paragraphe du .docx ne traite de cette exigence : le titre généré "
                 "doit la combler."),
            )
            nb += 1
    return nb


def construire(
    docx_chemin: str | pathlib.Path | None = None,
    db_chemin: str | pathlib.Path = DB_CHEMIN,
    paragraphes: list[dict] | None = None,
) -> tuple[pathlib.Path, int]:
    """(Re)construit la base SQLite à partir du .docx et du manifeste des sources."""
    if paragraphes is None:
        paragraphes = read_paragraphs(str(docx_chemin or DEFAULT_DOCX))
    conn = sqlite3.connect(str(db_chemin))
    try:
        conn.executescript(SCHEMA_SQL)
        charger_sources(conn)
        charger_exigences(conn)
        charger_elements(conn, paragraphes)
        nb_relations = lier_exigences(conn)
        conn.commit()
    finally:
        conn.close()
    return pathlib.Path(db_chemin), nb_relations


def main() -> int:
    docx = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOCX
    db, nb_relations = construire(docx)
    conn = sqlite3.connect(str(db))
    stats = {
        "sources": conn.execute("SELECT COUNT(*), SUM(present) FROM sources").fetchone(),
        "exigences": conn.execute(
            "SELECT COUNT(*) FROM exigences WHERE criticite='obligatoire'"
        ).fetchone()[0],
        "elements": conn.execute("SELECT COUNT(*) FROM docx_elements").fetchone()[0],
        "relations": conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0],
    }
    conn.close()
    print(f"Base créée : {db}")
    print(f"  sources        : {stats['sources'][1]}/{stats['sources'][0]} présentes")
    print(f"  exigences      : {stats['exigences']} obligatoires")
    print(f"  éléments .docx : {stats['elements']}")
    print(f"  relations      : {stats['relations']} ({nb_relations} créées)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



