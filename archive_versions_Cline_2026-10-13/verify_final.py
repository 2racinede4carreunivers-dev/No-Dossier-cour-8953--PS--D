from pypdf import PdfReader
SRC_FINAL = "c:/Demande_ajout_depot_legal/No-Dossier-cour-8953--PS--D/demande_ajout_act_FINAL_2026-10-13.pdf"
SRC_ORIG = "c:/Demande_ajout_depot_legal/No-Dossier-cour-8953--PS--D/demande_ajout_act.pdf"
rf = PdfReader(SRC_FINAL)
ro = PdfReader(SRC_ORIG)
# Vérifie que pages 2..51 du FINAL == pages 1..50 de l'original (texte identique)
ok = True
for i in range(len(ro.pages)):
    tf = (rf.pages[i+1].extract_text() or "").strip()
    to = (ro.pages[i].extract_text() or "").strip()
    if tf != to:
        ok = False
        print(f"DIFF page finale {i+2} vs orig {i+1}: len {len(tf)} vs {len(to)}")
        break
print("pages final:", len(rf.pages), "| pages orig:", len(ro.pages), "| contenu original intact:", ok)
print("page1 contient 723(2):", "723" in (rf.pages[0].extract_text() or ""))
print("page1 contient 721(1):", "721" in (rf.pages[0].extract_text() or ""))
print("page1 contient art 113:", "113" in (rf.pages[0].extract_text() or ""))
