from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from pypdf import PdfReader, PdfWriter

SRC = "c:/Demande_ajout_depot_legal/No-Dossier-cour-8953--PS--D/demande_ajout_act.pdf"
COVER = "c:/Demande_ajout_depot_legal/No-Dossier-cour-8953--PS--D/_cover_articles.pdf"
OUT = "c:/Demande_ajout_depot_legal/No-Dossier-cour-8953--PS--D/demande_ajout_act_FINAL_2026-10-13.pdf"

styles = getSampleStyleSheet()
sTitle = ParagraphStyle("t", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=14, leading=17, alignment=TA_CENTER)
sHead = ParagraphStyle("h", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=14, alignment=TA_CENTER)
sN = ParagraphStyle("n", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=14, alignment=TA_JUSTIFY)
sBox = ParagraphStyle("b", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=14, alignment=TA_CENTER, textColor=colors.black)
sSmall = ParagraphStyle("sm", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#333333"))
sItem = ParagraphStyle("it", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=14, alignment=TA_JUSTIFY, leftIndent=12)

doc = SimpleDocTemplate(COVER, pagesize=LETTER, leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm,
                        title="Page liminaire - fondements - 8953-PS-D", author="Philippe Savard")
story = []
story.append(Paragraph("Cour du Qu&eacute;bec &mdash; Chambre criminelle et p&eacute;nale<br/>District de Qu&eacute;bec &mdash; Palais de justice de Qu&eacute;bec, salle 2.15", sSmall))
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="100%", thickness=1))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("PAGE LIMINAIRE &mdash; FONDEMENTS JURIDIQUES<br/>Ajout&eacute;e le 13 octobre 2026 &mdash; contenu original inchang&eacute; &agrave; compter de la page 2", sTitle))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Dossier : 8953 &ndash; PS-D &nbsp;|&nbsp; Incident : LVSEV25000954 &nbsp;|&nbsp; Audience : 23 octobre 2026, 9 h 30, salle 2.15<br/>Personne accus&eacute;e : Philippe Savard (se repr&eacute;sente seule) &mdash; Plaidoyer : non-culpabilit&eacute;", sSmall))
story.append(Spacer(1, 0.4*cm))

boxdata = [[Paragraph("BUT DE LA REQU&circ;TE : demander &agrave; la Cour de RECEVOIR et PRENDRE EN CONNAISSANCE<br/>le document ci-joint (&laquo; ajout d'un acte &agrave; l'instruction &raquo;)<br/>+ demande de rapport pr&eacute;sentenciel", sBox)]]
box = Table(boxdata, colWidths=[16*cm])
box.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 1.2, colors.black), ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FFF4CC")), ("TOPPADDING", (0,0), (-1,-1), 10), ("BOTTOMPADDING", (0,0), (-1,-1), 10), ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10)]))
story.append(box)
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Fondements invoqu&eacute;s &mdash; lire en premier (d&eacute;taill&eacute;s aux pages 43 et suivantes du document original) :", sHead))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("<b>1. Art. 723 (2) C.cr. &mdash; &Eacute;l&eacute;ments de preuve :</b> &laquo; Le tribunal prend connaissance des &eacute;l&eacute;ments de preuve pertinents que lui pr&eacute;sentent les parties. &raquo; &mdash; Fondement principal de la demande de recevoir le document (observations &eacute;crites de la d&eacute;fense, art. 723 (1) et (2)).", sItem))
story.append(Spacer(1, 0.15*cm))
story.append(Paragraph("<b>2. Art. 721 (1) C.cr. &mdash; Rapport pr&eacute;sentenciel :</b> &agrave; la demande du tribunal, l'agent de probation pr&eacute;pare et d&eacute;pose un rapport &eacute;crit concernant l'accus&eacute; pour aider &agrave; la d&eacute;termination de la peine (voir aussi 721 (3) et (4) sur le contenu).", sItem))
story.append(Spacer(1, 0.15*cm))
story.append(Paragraph("<b>3. Art. 723 (3) C.cr. &mdash; Production d'&eacute;l&eacute;ments de preuve :</b> le tribunal peut exiger d'office des &eacute;l&eacute;ments de preuve pour la d&eacute;termination de la peine, apr&egrave;s avoir entendu les parties.", sItem))
story.append(Spacer(1, 0.15*cm))
story.append(Paragraph("<b>4. Art. 113 du R&egrave;glement de la Cour du Qu&eacute;bec + art. 9 et 71 :</b> gestion de l'instance criminelle (liste des pi&egrave;ces, par. 2)d)) ; pr&eacute;sentation des actes (format lettre, Arial 12, interligne et demi, marges 2,5 cm).", sItem))
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="100%", thickness=0.6))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Note de transparence : cette page 1 est un ajout de pr&eacute;sentation du 13 octobre 2026 pour faciliter la lecture d&egrave;s l'ouverture. Les pages 2 et suivantes sont la reproduction int&eacute;grale et inchang&eacute;e du document du 8 octobre 2026 (50 pages). Table des mati&egrave;res originale conserv&eacute;e. Outil de travail pr&eacute;par&eacute; par une personne se repr&eacute;sentant seule &mdash; ne remplace pas l'avis d'un avocat.", sSmall))
doc.build(story)

# Fusion : cover + original inchangé
reader_cover = PdfReader(COVER)
reader_src = PdfReader(SRC)
writer = PdfWriter()
for p in reader_cover.pages:
    writer.add_page(p)
for p in reader_src.pages:
    writer.add_page(p)
writer.add_metadata({"/Title": "Demande ajout acte 8953-PS-D - FINAL avec page liminaire 13 oct 2026", "/Author": "Philippe Savard", "/Subject": "Art 723(2) + 721(1) + art 113 Rgt Cour Quebec - audience 23 oct 2026 salle 2.15"})
with open(OUT, "wb") as f:
    writer.write(f)
print(f"OK cover={len(reader_cover.pages)} src={len(reader_src.pages)} total={len(writer.pages)} -> {OUT}")
