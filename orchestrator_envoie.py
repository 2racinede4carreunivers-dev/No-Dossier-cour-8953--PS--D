"""Orchestrateur d'envoi greffe + DPCP — 8953-PS-D / LVSEV25000954.
Base : guide_transmission_poursuite.md + checklist Barreau.
Usage : python orchestrator_envoie.py [--verifier-seul]
"""
import hashlib
import os
import shutil
import sys
from datetime import date

BASE = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D"
DOSSIER = "8953 - PS-D"
INCIDENT = "LVSEV25000954"
AUDIENCE = "23 octobre 2026 a 9 h 30, salle 2.15, Palais de justice de Quebec"
GREFFE_COURRIEL = "greffe-fds-criminel.CQ.Quebec@justice.gouv.qc.ca"
DPCP_CCI = "penal.quebec@dpcp.gouv.qc.ca"
PERSO_CCI = "philippethomassavard@gmail.com"
OBJET = (f"Dossier {DOSSIER} / {INCIDENT} — Demande art. 723(2) + demande d'ajout d'une preuve "
         f"au dépôt légal — Audience 23 oct. 2026 — Savard")
# DEUX demandes SEPARÉES (aucune demande de rapport présentenciel) :
#  1) Demande d'ajout d'un acte à l'instruction en vue du jugement (art. 723(2) C.cr.)
#  2) Demande d'ajout d'une preuve au dépôt légal de la preuve
PIECES = [
    (r"demande_ajout_act.pdf",
     "Demande 1 — Ajout d'un acte a l'instruction en vue du jugement (art. 723(2) C.cr.)"),
    (r"pipeline-depot-legal\Demande_ajout_depot_legal\demande_ajout_preuve.pdf",
     "Demande 2 — Ajout d'une preuve au depot legal de la preuve"),
    (r"pipeline-depot-legal\Preuve\lettre_ccq.pdf", "Piece A-1a lettre CCQ"),
    (r"pipeline-depot-legal\Preuve\lettre_refus.pdf", "Piece A-1b lettre refus"),
    (r"pipeline-depot-legal\Preuve\Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf", "Piece A-2 article"),
    (r"pipeline-depot-legal\Preuve\LISEZMOI_A3_CCQ_2026-09-25.md", "Piece A-3 note CCQ"),
    (r"pipeline-depot-legal\Preuve\lettre_CCQ_incident_2026-09-25.pdf", "Piece A-3b scan lettre CCQ 25 sept. 2026 (cyberattaque 24 aout 2026)"),
]
DEST_GREFFE = os.path.join(BASE, "Philippe_Savard_greffe_penal", "Envoi_greffe_penal_criminel")
DEST_DPCP = os.path.join(BASE, "Philippe_Savard_greffe_penal", "Philippe_Savard_DPCP", "Envoi_DPCP")

def sha12(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()[:12]


def corps():
    return ("Bonjour,\n\nJe suis Philippe Savard, personne accusee se representant seule, "
        f"dossier {DOSSIER} / {INCIDENT}, audience {AUDIENCE}.\nObjet : {OBJET}\n\n"
        "Je vous transmets pour depot au dossier et connaissance de la Cour DEUX demandes separees :\n"
        "1) Demande d'ajout d'un acte a l'instruction en vue du jugement, pour etre pris en "
        "consideration par la Cour (art. 723(2) C.cr.) — fichier demande_ajout_act.pdf ;\n"
        "2) Demande d'ajout d'une preuve au depot legal de la preuve — fichier demande_ajout_preuve.pdf, "
        "avec pieces justificatives A-1a, A-1b, A-2 et A-3 (voir lettre d'explication et manifeste joints).\n"
        f"Cci : DPCP Bureau Quebec ({DPCP_CCI}) + copie personnelle ({PERSO_CCI}).\n"
        "Merci de confirmer reception (date/heure) et versement au dossier pour le 23 octobre 2026.\n\n"
        "Cordialement,\nPhilippe Savard\n")

def lettre(dt):
    L = []
    L.append("Cour du Quebec — Chambre criminelle et penale, district de Quebec")
    L.append(f"Dossier : {DOSSIER} | Incident : {INCIDENT} | Audience : {AUDIENCE}")
    L.append(f"A : Greffe penal et criminel CQ Quebec — {GREFFE_COURRIEL}")
    L.append(f"Cci : DPCP Bureau Quebec — {DPCP_CCI} ; copie personnelle — {PERSO_CCI}")
    L.append("")
    L.append("LETTRE D'EXPLICATION DE L'ENVOI (avis ecrit avant audience)")
    L.append(f"Quebec, le {dt}. Madame, Monsieur,")
    L.append("Je vous avise de mon intention de presenter a la Cour le 23 octobre 2026 9h30 salle 2.15 ")
    L.append("DEUX demandes separees :")
    L.append("1) Demande d'ajout d'un acte a l'instruction en vue du jugement, pour etre pris en")
    L.append("   consideration par la Cour (art. 723(2) C.cr.) — fichier : demande_ajout_act.pdf ;")
    L.append("2) Demande d'ajout d'une preuve au depot legal de la preuve")
    L.append("   — fichier : demande_ajout_preuve.pdf, avec pieces A-1a, A-1b, A-2 et A-3.")
    L.append("Aucune demande de rapport presentenciel n'est formulee.")
    L.append("Pieces jointes (envoi unique : A greffe, Cci DPCP + perso) :")
    for i, (rel, desc) in enumerate(PIECES, 1):
        L.append(f"  {i}. {os.path.basename(rel)} — {desc}")
    L.append("Present en personne le 23 octobre 2026 9h30 salle 2.15. Cordialement, Philippe Savard")
    return "\n".join(L) + "\n"

def assembler(dest):
    os.makedirs(dest, exist_ok=True)
    man = [f"Dossier : {DOSSIER} | Incident : {INCIDENT} | {date.today().isoformat()}",
        f"A : {GREFFE_COURRIEL}", f"Cci : {DPCP_CCI} ; {PERSO_CCI}", f"Objet : {OBJET}", ""]
    total = 0
    for rel, desc in PIECES:
        src = os.path.join(BASE, rel)
        if not os.path.exists(src):
            print(f"MANQUANT : {src}")
            return False
        dst = os.path.join(dest, os.path.basename(rel))
        shutil.copy2(src, dst)
        sz = os.path.getsize(dst)
        total += sz
        man.append(f"{os.path.basename(rel)} | {sz} octets | sha256:{sha12(dst)} | {desc}")
    man.append("")
    man.append(f"Total : {total} octets ({total/1048576:.2f} Mo)")
    open(os.path.join(dest, "manifeste_SHA256.txt"), "w", encoding="utf-8").write("\n".join(man) + "\n")
    open(os.path.join(dest, "lettre_explication_envoi.txt"), "w", encoding="utf-8").write(
        lettre(date.today().isoformat()))
    open(os.path.join(dest, "corps_courriel_a_copier.txt"), "w", encoding="utf-8").write(
        f"A : {GREFFE_COURRIEL}\nCci : {DPCP_CCI} ; {PERSO_CCI}\nObjet : {OBJET}\n\n" + corps())
    print(f"OK envoi unique : {len(PIECES)} pieces + lettre + corps + manifeste -> {dest} ({total} o)")
    return total < 20 * 1048576

def main():
    seul = "--verifier-seul" in sys.argv
    manq = [r for r, _ in PIECES if not os.path.exists(os.path.join(BASE, r))]
    if manq:
        print("MANQUANTES :")
        for m in manq:
            print(" -", m)
        sys.exit(1)
    print(f"Toutes les {len(PIECES)} pieces obligatoires presentes.")
    if seul:
        return
    ok1 = assembler(DEST_GREFFE)
    # Copie miroir DPCP : meme contenu integral pour preuve de signification
    import shutil as _sh
    if os.path.exists(DEST_DPCP):
        _sh.rmtree(DEST_DPCP)
    _sh.copytree(DEST_GREFFE, DEST_DPCP)
    print(f"OK miroir DPCP (copie integrale) -> {DEST_DPCP}")
    print("Poids < 20 Mo :", ok1)
    print("Envoi unique : A greffe, Cci DPCP + perso. Joindre TOUT le dossier Envoi_greffe_penal_criminel.")

if __name__ == "__main__":
    main()
