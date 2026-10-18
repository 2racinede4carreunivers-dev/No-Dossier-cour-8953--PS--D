SRC = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act.tex"
DST = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act_FINAL_EPURE_2026-10-13.tex"
with open(SRC, encoding="utf-8") as f:
    tex = f.read()
lim = r"""
% Page liminaire — fondements juridiques
\thispagestyle{empty}
\onehalfspacing
\begin{center}
Cour du Qu\'ebec --- Chambre criminelle et p\'enale, District de Qu\'ebec --- Palais de justice de Qu\'ebec, salle 2.15\par
\vspace{0.2cm}
\rule{\textwidth}{0.4pt}\\[0.3em]
{\normalsize\bfseries PAGE LIMINAIRE --- FONDEMENTS JURIDIQUES}\\[0.3em]
\rule{\textwidth}{0.4pt}
\end{center}
\begin{center}
Dossier : \textbf{8953 -- PS-D} \quad Incident : \textbf{LVSEV25000954} \quad Audience : \textbf{23 octobre 2026, 9 h 30, salle 2.15}\par
Personne accus\'ee : Philippe Savard (se repr\'esente seule) --- Plaidoyer : non-culpabilit\'e\par
\end{center}
\vspace{0.2cm}
\noindent\fbox{\parbox{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}{\begin{center}\textbf{BUT : demander \`a la Cour de RECEVOIR et PRENDRE EN CONNAISSANCE le document ci-joint + demande de rapport pr\'esentenciel}\end{center}}}
\vspace{0.3cm}
\noindent\textbf{Fondements :}
\begin{enumerate}[label=\arabic*.,leftmargin=*,itemsep=2pt,topsep=2pt,parsep=2pt]
\item \textbf{Art.\ 723 (2) C.cr.\ :} <<~Le tribunal prend connaissance des \'el\'ements de preuve pertinents que lui pr\'esentent les parties.~>> --- fondement principal (observations \'ecrites, art.\ 723 (1) et (2)).
\item \textbf{Art.\ 721 (1) C.cr.\ :} rapport pr\'esentenciel \`a la demande du tribunal (contenu : 721 (3) et (4)).
\item \textbf{Art.\ 723 (3) C.cr.\ :} production d'office d'\'el\'ements de preuve pour la peine, apr\`es audition des parties.
\item \textbf{Art.\ 113 du R\`eglement de la Cour du Qu\'ebec (+ art.\ 9 et 71) :} gestion de l'instance criminelle, liste des pi\`eces par.\ 2)d), pr\'esentation des actes.
\end{enumerate}
\newpage
"""
m = r"\thispagestyle{empty}"
assert m in tex
tex2 = tex.replace(m, lim, 1)
# Retirer la note de bas de document qui s'adresse a l'auteur (orientation interne)
old_tail = r"""\vspace{0.8cm}
\hrule
\vspace{0.4em}
\small\emph{Document assemblé automatiquement par le pipeline \texttt{pipeline\_rapport\_presentenciel.py} à partir de la base SQLite \texttt{rapport\_presentenciel.db} (réseau de recevabilité, art. 723 (2) C.cr.) et de l'extrait factuel fourni. Il doit être revu par un membre du Barreau du Québec avant tout dépôt au greffe.}"""
assert old_tail in tex2, "queue introuvable"
tex2 = tex2.replace(old_tail, "", 1)
# Retirer la phrase d'orientation interne sur la base SQLite du pipeline (section Sources)
old_src = "Sources téléchargées et mises en relation dans la base SQLite du pipeline :"
assert old_src in tex2, "phrase sources introuvable"
tex2 = tex2.replace(old_src, "Sources et pi\\`eces consult\\'ees :", 1)
open(DST, "w", encoding="utf-8").write(tex2)
print("OK epure ecrit", len(tex2))
