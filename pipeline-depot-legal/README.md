# Pipeline — Demande d'ajout d'une preuve au dépôt légal

**Cour du Québec, Chambre criminelle et pénale — District de Québec**
**Dossier n° 8953 – PS-D | Incident n° LVSEV25000954**
**Infraction : possession dans le but de trafic | Représentation : personne accusée se représentant seule (sans avocat)**
**Audience : 23 octobre 2026, 9 h 30, salle 2.15, Palais de justice de Québec**

Ce projet automatise la préparation d'une demande d'ajout de preuve au dossier de la Cour,
en vérifiant sa conformité aux sources officielles (Barreau du Québec, Barreau de Montréal,
Fondation du Barreau du Québec, Cour du Québec, DPCP, Code criminel).

## Structure des dossiers

| Dossier | Contenu |
|---|---|
| `Dependence_Pipeline/` | **Toutes les sources ayant servi à concevoir le pipeline** (traçabilité) : documents officiels téléchargés (`sources/`), extraits de recherche par mots-clés (`extraits/`), copie du document de travail `README_LEGAL_source.docx`. Rien n'a été supprimé. |
| `Pipeline/` | **Le pipeline logiciel** : scripts Python et base SQLite `depot_legal.db` (schéma relationnel sources → exigences → éléments du document → conformité → pièces). |
| `Preuve/` | **Les pièces de preuve** : `lettre_refus.docx` (original), `lettre_refus.pdf` (conversion), `Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf` (article, 36 pages). |
| `Demande_ajout_depot_legal/` | **Les livrables finaux** : `demande_ajout_preuve.pdf` (9 pages, dont l'annexe méthodologique), `Dossier_complet_demande_depot_legal_LVSEV25000954.pdf` (49 pages : demande + intercalaires A-1/A-2 + pièces), `rapport_conformite.md`, source `demande_ajout_preuve.tex`. |

## Exécution

```powershell
cd Pipeline
python orchestrator_legal.py            # pipeline complet (PDF inclus)
python orchestrator_legal.py --sans-pdf # sans compilation PDF
python verifier_livrables.py            # contrôle final des livrables
```

Le moteur de compilation est XeLaTeX (MiKTeX) avec la police Times New Roman ;
les pièces sont assemblées dans un seul PDF paginé avec pages intercalaires.

## Scripts (Pipeline/)

| Script | Rôle |
|---|---|
| `chemins.py` | Centralisation de tous les chemins du projet. |
| `collect_barreau.py` | Téléchargement des sources officielles. |
| `extract_sources.py` | Extraction du texte des PDF/HTML vers `.txt`. |
| `grep_sources.py` | Recherche par mots-clés dans les sources extraites. |
| `docx_reader.py` | Lecture du `.docx` de travail (titres gras, puces, paragraphes). |
| `build_db.py` | Construction de la base `depot_legal.db` (18 exigences, relations). |
| `orchestrator_legal.py` | Orchestration : génération LaTeX, compilation, assemblage, conformité, rapport. |
| `reparer_encodage.py` | Outil de réparation d'encodage (conservé pour traçabilité). |
| `verifier_livrables.py` | Vérification finale : pages PDF, cohérence d'assemblage, conformité. |

## Provenance des pièces

- **Pièce A-1** : `C:\ARTICLE\Article\tex\lettre_refus.docx` — courriel « CJM 260814-savard — Décision »
  de la *Revue canadienne de mathématiques* (Henry H. Kim et Robert McCann, rédacteurs en chef),
  salutation « Cher Professeur Savard ».
- **Pièce A-2** : `C:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf`.

> Note : le document de travail mentionnait « Journal canadien de mathématiques » ; la lettre
> émane officiellement de la *Revue canadienne de mathématiques*. La demande générée rappelle
> les deux appellations pour exactitude devant la Cour.



