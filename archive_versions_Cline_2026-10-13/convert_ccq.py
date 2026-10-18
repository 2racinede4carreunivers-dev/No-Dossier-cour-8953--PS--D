from PIL import Image
import os
src = "C:/Users/Utilisateur/OneDrive/Images/Numérisations/lettre_ccq.png"
dst = "c:/Demande_ajout_depot_legal/No-Dossier-cour-8953--PS--D/pipeline-depot-legal/Preuve/lettre_CCQ_incident_2026-09-25.pdf"
im = Image.open(src)
if im.mode in ("RGBA", "LA"):
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[-1])
    im = bg
elif im.mode != "RGB":
    im = im.convert("RGB")
im.save(dst, "PDF", resolution=150)
print("OK", dst, os.path.getsize(dst), "octets")
