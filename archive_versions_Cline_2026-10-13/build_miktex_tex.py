import shutil

SRC = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act.tex"
DST = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act_FINAL_MIKTEX_2026-10-13.tex"

with open(SRC, encoding="utf-8") as f:
    tex = f.read()

liminaire = r"""
% ===== PAGE LIMINAIRE AJOUTEE LE 13 OCTOBRE 2026 — RIEN D'AUTRE MODIFIE =====
\thispagestyle{empty}
\begin{center}
{\small Cour du Qu\'ebec --- Chambre criminelle et p\'enale\\
District de Qu\'ebec --- Palais de justice de Qu\'ebec, salle 2.15\\}
\vspace{0.2cm}
\rule{\textwidth}{0.4pt}\\[0.3em]
{\Large\bfseries PAGE LIMINAIRE --- FONDEMENTS JURIDIQUES}\\[0.2em]
{\small Ajout\'ee le 13 octobre 2026 --- contenu original inchang\'e \`a compter de la page 2}\\[0.3em]
\rule{\textwidth}{0.4pt}
\end{center}
\begin{center}
{\small Dossier : \textbf{8953 -- PS-D} \quad Incident : \textbf{LVSEV25000954} \quad Audience : \textbf{23 octobre 2026, 9 h 30, salle 2.15}}\\
{\small Personne accus\'ee : Philippe Savard (se repr\'esente seule) --- Plaidoyer : non-culpabilit\'e}
\end{center}
\vspace{0.3cm}
\noindent\fbox{\parbox{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}{%
\begin{center}
\textbf{BUT DE LA REQU\^ETE : demander \`a la Cour de RECEVOIR et PRENDRE EN CONNAISSANCE}\\
\textbf{le document ci-joint (\guillemotleft~ajout d'un acte \`a l'instruction~\guillemotright)}\\
\textbf{+ demande de rapport pr\'esentenciel}
\end{center}%
}}
\vspace{0.4cm}
\noindent\textbf{Fondements invoqu\'es --- lire en premier (d\'etaill\'es aux pages suivantes du document original) :}
\begin{enumerate}[label=\arabic*.,leftmargin=*,itemsep=2pt,topsep=2pt]
\item \textbf{Art.\ 723 (2) C.cr.\ --- \'El\'ements de preuve :} \guillemotleft~Le tribunal prend connaissance des \'el\'ements de preuve pertinents que lui pr\'esentent les parties.~\guillemotright\ --- Fondement principal de la demande de recevoir le document (observations \'ecrites de la d\'efense, art.\ 723 (1) et (2)).
\item \textbf{Art.\ 721 (1) C.cr.\ --- Rapport pr\'esentenciel :} \`a la demande du tribunal, l'agent de probation pr\'epare et d\'epose un rapport \'ecrit concernant l'accus\'e pour aider \`a la d\'etermination de la peine (voir aussi 721 (3) et (4) sur le contenu).
\item \textbf{Art.\ 723 (3) C.cr.\ --- Production d'\'el\'ements de preuve :} le tribunal peut exiger d'office des \'el\'ements de preuve pour la d\'etermination de la peine, apr\`es avoir entendu les parties.
\item \textbf{Art.\ 113 du R\`eglement de la Cour du Qu\'ebec + art.\ 9 et 71 :} gestion de l'instance criminelle (liste des pi\`eces, par.\ 2)d))~; pr\'esentation des actes (format lettre, Arial 12, interligne et demi, marges 2,5 cm).
\end{enumerate}
\vspace{0.2cm}
\rule{\textwidth}{0.4pt}
{\small\emph{Note de transparence : cette page 1 est un ajout de pr\'esentation du 13 octobre 2026 pour faciliter la lecture d\`es l'ouverture. Les pages suivantes sont le contenu original int\'egral et inchang\'e du document du 8 octobre 2026. Table des mati\`eres originale conserv\'ee. Outil de travail pr\'epar\'e par une personne se repr\'esentant seule --- ne remplace pas l'avis d'un avocat.}}
\newpage
% ===== FIN PAGE LIMINAIRE — SUIT LE CONTENU ORIGINAL INCHANGÉ =====

"""

marker = r"\thispagestyle{empty}"
assert marker in tex, "marqueur introuvable"
tex2 = tex.replace(marker, liminaire, 1)

with open(DST, "w", encoding="utf-8") as f:
    f.write(tex2)
print(f"OK tex final ecrit : {DST} ({len(tex2)} caracteres, original {len(tex)} )")
