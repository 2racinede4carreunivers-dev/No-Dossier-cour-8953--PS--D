SRC = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act.tex"
DST = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act_FINAL_MIKTEX_CORRIGE_2026-10-13.tex"
with open(SRC, encoding="utf-8") as f:
    tex = f.read()
lim = r"""
% ===== PAGE LIMINAIRE CORRIGEE 13 OCT 2026 — CONFORME ART. 9 ET 71 + LANGAGE CLAIR BARREAU — SEUL AJOUT =====
% Conformite : format lettre, un seul cote (classe article oneside), police style Arial 12 pt (helvet + 12pt, \normalsize partout),
% interligne et demi (\onehalfspacing herite du preambule), marges 2,5 cm (geometry), pagination haut centre (fancyhdr),
% paragraphes numerotes (enumerate chiffres arabes), noir et blanc uniquement (aucune couleur, aucun fond), langage clair Barreau.
\thispagestyle{empty}
\onehalfspacing
\begin{center}
Cour du Qu\'ebec --- Chambre criminelle et p\'enale, District de Qu\'ebec --- Palais de justice de Qu\'ebec, salle 2.15\par
\vspace{0.2cm}
\rule{\textwidth}{0.4pt}\\[0.3em]
{\normalsize\bfseries PAGE LIMINAIRE --- FONDEMENTS JURIDIQUES}\\[0.2em]
Ajout\'ee le 13 octobre 2026 --- contenu original inchang\'e \`a compter de la page 2\\[0.2em]
\rule{\textwidth}{0.4pt}
\end{center}
\begin{center}
Dossier : \textbf{8953 -- PS-D} \quad Incident : \textbf{LVSEV25000954} \quad Audience : \textbf{23 octobre 2026, 9 h 30, salle 2.15}\par
Personne accus\'ee : Philippe Savard (se repr\'esente seule) --- Plaidoyer : non-culpabilit\'e\par
\end{center}
\vspace{0.2cm}
\noindent\fbox{\parbox{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}{\begin{center}\textbf{BUT : demander \`a la Cour de RECEVOIR et PRENDRE EN CONNAISSANCE le document ci-joint + demande de rapport pr\'esentenciel}\end{center}}}
\vspace{0.3cm}
\noindent\textbf{Fondements --- lire en premier (d\'etaill\'es dans le document original) :}
\begin{enumerate}[label=\arabic*.,leftmargin=*,itemsep=2pt,topsep=2pt,parsep=2pt]
\item \textbf{Art.\ 723 (2) C.cr.\ :} <<~Le tribunal prend connaissance des \'el\'ements de preuve pertinents que lui pr\'esentent les parties.~>> --- fondement principal (observations \'ecrites, art.\ 723 (1) et (2)).
\item \textbf{Art.\ 721 (1) C.cr.\ :} rapport pr\'esentenciel \`a la demande du tribunal (contenu : 721 (3) et (4)).
\item \textbf{Art.\ 723 (3) C.cr.\ :} production d'office d'\'el\'ements de preuve pour la peine, apr\`es audition des parties.
\item \textbf{Art.\ 113 du R\`eglement de la Cour du Qu\'ebec (+ art.\ 9 et 71) :} gestion de l'instance criminelle, liste des pi\`eces par.\ 2)d), pr\'esentation des actes.
\end{enumerate}
\vspace{0.2cm}
\rule{\textwidth}{0.4pt}
\emph{Transparence : page 1 ajout\'ee le 13 oct.\ 2026 pour lecture rapide, sans couleur et en 12 points \`a interligne et demi comme le reste de l'acte. Pages suivantes : contenu original int\'egral du 8 oct.\ 2026, inchang\'e. Sources du Barreau, de la Fondation, de la Cour et du DPCP archiv\'ees dans pipeline-depot-legal. Outil de travail, personne se repr\'esentant seule --- ne remplace pas l'avis d'un avocat.}
\newpage
% ===== FIN LIMINAIRE CORRIGEE =====
"""
m = r"\thispagestyle{empty}"
assert m in tex
tex2 = tex.replace(m, lim, 1)
open(DST, "w", encoding="utf-8").write(tex2)
print("OK corrige ecrit", len(tex2))
