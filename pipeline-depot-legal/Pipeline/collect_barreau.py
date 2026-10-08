"""Collecte des sources juridiques (Barreau du Québec et textes de référence).

Télécharge dans ./sources_barreau tous les documents servant à construire la
base d'exigences, puis lance l'extraction du texte (extract_sources.py).

Usage :  python collect_barreau.py
"""
from __future__ import annotations

import pathlib
import ssl
import subprocess
import sys
import urllib.request

from chemins import DIR_PIPELINE as BASE, DIR_SOURCES as DEST

# Chaque source : organisme, titre, type, url, fichier local.
SOURCES: list[dict] = [
    {
        "id": "BARREAU_GUIDES",
        "organisme": "Barreau du Québec",
        "titre": "Guides pratiques et aide-mémoires",
        "type": "page_web",
        "url": (
            "https://www.barreau.qc.ca/fr/membres-ordre/ressources/"
            "normes-outils-references-guides/guides-pratiques-aide-memoires/"
        ),
        "fichier": "barreau_guides_pratiques.html",
        "note": "Sommaire des outils officiels du Barreau (rédaction, procédure, langage clair).",
    },
    {
        "id": "BARREAU_PROC_PENALE",
        "organisme": "Barreau du Québec",
        "titre": "Procédure pénale — aide-mémoire",
        "type": "guide",
        "url": "https://www.barreau.qc.ca/media/osyeiodv/procedure-penale.pdf",
        "fichier": "barreau_procedure-penale.pdf",
        "note": "Aide-mémoire du Barreau sur le déroulement d'une instance criminelle.",
    },
    {
        "id": "BARREAU_MTL_CQCRIM",
        "organisme": "Barreau de Montréal",
        "titre": "Cour du Québec – Chambre criminelle et pénale (outils)",
        "type": "page_web",
        "url": "https://www.barreaudemontreal.qc.ca/avocats/outils/avocats-de-litige/cq-crim/",
        "fichier": "barreaumontreal_cq-crim.html",
        "note": "Règles de fonctionnement, formulaires et liens de dépôt de la Chambre criminelle.",
    },
    {
        "id": "FONDATION_SEUL_DEVANT",
        "organisme": "Fondation du Barreau du Québec",
        "titre": "Seul devant la cour : criminelle et pénale",
        "type": "guide",
        "url": "https://fondationdubarreau.qc.ca/assets/documents/seul-devant-la-cour-criminelle-penale-fr.pdf",
        "fichier": "fondation_seul-devant-la-cour-criminelle-penale.pdf",
        "note": "Guide pour les personnes non représentées : avis à la poursuite, dépôt de documents.",
    },
    {
        "id": "FONDATION_PREP_CRIM",
        "organisme": "Fondation du Barreau du Québec",
        "titre": "Comment se préparer pour la cour en matière criminelle",
        "type": "guide",
        "url": (
            "https://fondationdubarreau.qc.ca/assets/documents/"
            "Guide_Comment-se-pr%C3%A9parer-pour-la-cour-en-mati%C3%A8re-criminelle-VF-2025.pdf"
        ),
        "fichier": "fondation_preparer-cour-criminelle-2025.pdf",
        "note": "Forme des requêtes, avis, confidentialité (2024/2025).",
    },
    {
        "id": "FONDATION_PREP_PEN",
        "organisme": "Fondation du Barreau du Québec",
        "titre": "Comment se préparer pour la cour en matière pénale",
        "type": "guide",
        "url": (
            "https://fondationdubarreau.qc.ca/assets/documents/"
            "Guide_Comment-se-pr%C3%A9parer-pour-la-cour-en-mati%C3%A8re-p%C3%A9nale-VF-2025.pdf"
        ),
        "fichier": "fondation_preparer-cour-matiere-penale-2025.pdf",
        "note": "Version poursuites provinciales du même guide.",
    },
    {
        "id": "CQ_REGLES_GESTION",
        "organisme": "Cour du Québec",
        "titre": (
            "Règles de fonctionnement sur la gestion de l'instance en matière "
            "criminelle et pénale (art. 113 du Règlement de la Cour du Québec)"
        ),
        "type": "regle",
        "url": (
            "https://courduquebec.new.volcan.design/fileadmin/cour-du-quebec/"
            "centre-de-documentation/chambre-criminelle-et-penale/"
            "RegleFonctionnementGestionInstanceCriminel.pdf"
        ),
        "fichier": "cq_regle_fonctionnement_gestion_instance_criminel.pdf",
        "note": "Liste de pièces, énoncé sommaire de la preuve, procès-verbal des décisions.",
    },
    {
        "id": "DPCP_PRE_1",
        "organisme": "Directeur des poursuites criminelles et pénales (Québec)",
        "titre": "Directive de pratique PRE-1 — Communication de la preuve par le poursuivant",
        "type": "directive",
        "url": "https://cdn-contenu.quebec.ca/cdn-contenu/adm/org/dpcp/PDF/directives/DIR_PRE-1_DPCP.pdf",
        "fichier": "dpcp_directive_PRE-1_communication_preuve.pdf",
        "note": "Règles de divulgation de la preuve par la poursuite.",
    },
    {
        "id": "CC_657_1",
        "organisme": "Gouvernement du Canada",
        "titre": "Code criminel, art. 657.1 — Avis avant production d'une déclaration sous serment",
        "type": "loi",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/c-46/section-657.1.html",
        "fichier": "code_criminel_657.1.html",
        "note": "Avis écrit et copie raisonnable à l'autre partie avant la production (657.1(3)).",
    },
    {
        "id": "CC_486",
        "organisme": "Gouvernement du Canada",
        "titre": "Code criminel, art. 486.4 — Ordonnance visant à ne pas publier de renseignements",
        "type": "loi",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/c-46/section-486.4.html",
        "fichier": "code_criminel_486.4.html",
        "note": "Fondement possible d'une demande de confidentialité (avis aux parties requis).",
    },
]

# Documents d'autres juridictions (conservés à titre de référence documentaire,
# mais exclus de la construction des exigences du Québec).
A_EXCLURE_DE_L_ANALYSE = [
    "regles_procedure_criminelle_cour_2016.pdf",
    "regles_procedure_criminelle_cour_2016.html",
]


def telecharger(src: dict) -> bool:
    dest = DEST / src["fichier"]
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[déjà présent] {src['fichier']}")
        return True
    requete = urllib.request.Request(
        src["url"],
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    try:
        contexte = ssl.create_default_context()
        with urllib.request.urlopen(requete, timeout=90, context=contexte) as reponse:
            donnees = reponse.read()
        dest.write_bytes(donnees)
        print(f"[OK]          {src['fichier']}  ({len(donnees)} octets)")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[ERREUR]      {src['fichier']} : {exc}")
        return False


def main() -> int:
    DEST.mkdir(exist_ok=True)
    telecharges = 0
    for src in SOURCES:
        telecharges += int(telecharger(src))

    print(f"\n{telecharges}/{len(SOURCES)} sources disponibles.")
    print("Extraction du texte…")
    resultat = subprocess.run([sys.executable, str(BASE / "extract_sources.py")], check=False)
    return 0 if resultat.returncode == 0 and telecharges else 1


if __name__ == "__main__":
    raise SystemExit(main())


