SRC = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act.tex"
DST = r"c:\Demande_ajout_depot_legal\No-Dossier-cour-8953--PS--D\demande_ajout_act_FINAL_MIKTEX_2026-10-13.tex"
with open(SRC, encoding="utf-8") as f:
    tex = f.read()
lim = r"""
% ===== PAGE LIMINAIRE 13 OCT 2026 — SEUL AJOUT, RESTE INCHANGE =====
\thispagestyle{empty}
{\singlespacing
\begin{center}
{\footnotesize Cour du Québec — Chambre criminelle et pénale, District de Québec — Palais de justice de Québec, salle 2.15\par}
\vspace{0.1cm}
\rule{\textwidth}{0.4pt}\\[0.2em]
{\large\bfseries PAGE LIMINAIRE — FONDEMENTS JURIDIQUES}\\[0.1em]
{\footnotesize Ajoutée le 13 octobre 2026 — contenu original inchangé à compter de la page 2}\\[0.15em]
\rule{\textwidth}{0.4pt}
\end{center}
\begin{center}
{\footnotesize Dossier : \textbf{8953 – PS-D} \quad Incident : \textbf{LVSEV25000954} \quad Audience : \textbf{23 octobre 2026, 9 h 30, salle 2.15}\par}
{\footnotesize Personne accusée : Philippe Savard (se représente seule) — Plaidoyer : non-culpabilité\par}
\end{center}
\vspace{0.1cm}
\noindent\fbox{\parbox{\dimexpr\textwidth-2\fboxsep-2\fboxrule\relax}{\begin{center}{\small\textbf{BUT : demander à la Cour de RECEVOIR et PRENDRE EN CONNAISSANCE le document ci-joint + demande de rapport présentenciel}}\end{center}}}
\vspace{0.15cm}
\noindent{\small\textbf{Fondements — lire en premier (détaillés dans le document original) :}}
\begin{enumerate}[label=\arabic*.,leftmargin=*,itemsep=1pt,topsep=1pt,parsep=0pt]
{\small
\item \textbf{Art. 723 (2) C.cr. :} « Le tribunal prend connaissance des éléments de preuve pertinents que lui présentent les parties. » — fondement principal (observations écrites, art. 723 (1) et (2)).
\item \textbf{Art. 721 (1) C.cr. :} rapport présentenciel à la demande du tribunal (contenu : 721 (3) et (4)).
\item \textbf{Art. 723 (3) C.cr. :} production d'office d'éléments de preuve pour la peine, après audition des parties.
\item \textbf{Art. 113 Règlement Cour du Québec (+ art. 9 et 71) :} gestion instance criminelle, liste pièces par. 2)d), présentation actes.
}
\end{enumerate}
\vspace{0.05cm}
\rule{\textwidth}{0.4pt}
{\footnotesize\emph{Transparence : page 1 ajoutée le 13 oct. 2026 pour lecture rapide. Pages suivantes : contenu original intégral du 8 oct. 2026, inchangé. Outil de travail, personne se représentant seule — ne remplace pas l'avis d'un avocat.}}
\par}
\newpage
% ===== FIN LIMINAIRE =====
"""
m = r"\thispagestyle{empty}"
assert m in tex
tex2 = tex.replace(m, lim, 1)
open(DST, "w", encoding="utf-8").write(tex2)
print("OK rebuilt", len(tex2))
