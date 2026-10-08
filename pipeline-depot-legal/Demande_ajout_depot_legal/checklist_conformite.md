# Checklist du dépôt complet — conformité Barreau / audience du 23 octobre 2026

**Généré le :** 2026-10-07 16:30 — `pipeline_checkliste.py`

**But du dépôt :** requête en ajout d'une preuve au dépôt légal **+** dépôt d'un rapport présenténciel (art. 721 (1) C.cr.) pour le verdict — **audience du vendredi 23 octobre 2026 à 9 h 30, salle 2.15, Palais de justice de Québec** (Cour du Québec, Chambre criminelle et pénale, district de Québec ; incident LVSEV25000954).

**Échelle :** 0 (le plus bas) à 10 (le plus haut) ; ≥ 9 Conforme · 7 à 8,9 À améliorer · 4 à 6,9 Partiel · < 4 Non conforme.

## 1. Bilan

| Indicateur | Valeur |
|---|---|
| **Note globale pondérée /10** | **9.82** |
| Verdict | 🟢 NIVEAU ACCEPTABLE — dépôt conforme à son but et aux exigences du Barreau |
| Seuil de réussite retenu | 8.0/10 |
| Points évalués | 34 (16 de structure + 18 exigences Barreau) |
| Points obligatoires | 28 |
| Note la plus faible parmi les obligatoires | 10.0/10 |

## 2. Table A — Points de structure du dépôt (présence + conformité documentation)

| Code | Point | Référence (Barreau / organisme) | Criticité | Présence /10 | Conformité /10 | **Note /10** | Statut | Détail |
|---|---|---|---|---:|---:|---:|---|---|
| `DEP-01` | Documents d'orientation du dépôt (README racine et du pipeline) | Pratique de rédaction claire (Barreau du Québec) ; identification du tribunal et du dossier | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | 2/2 motifs de contenu trouvés |
| `DEP-02` | Pipeline logiciel complet (6 scripts) | Traçabilité de la démarche (guides pratiques du Barreau) | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | présence seule (aucun motif de contenu requis) |
| `DEP-03` | Base de traçabilité SQLite (sources, exigences, conformité, pièces) | Règles de fonctionnement (art. 113) ; méthode du pipeline | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | 7/7 tables ; 18 exigences ; 18/18 conformes ; 10/10 sources présentes |
| `DEP-04` | Sources officielles téléchargées (Barreau, Fondation, Cour du Québec, DPCP, C.cr.) | Barreau du Québec — guides pratiques et aide-mémoires ; Fondation du Barreau « Seul devant la cour » ; Cour du Québec ; DPCP PRE-1 | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | présence seule (aucun motif de contenu requis) |
| `DEP-05` | Coordonnées actualisées de la poursuite et de la Cour (DPCP / Cour du Québec) | DPCP — coordonnées des points de service ; Cour du Québec — nous joindre | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | 3/3 motifs de contenu trouvés |
| `DEP-06` | Extraits de recherche par mots-clés (avis, dépôt, greffe, pièces, requêtes) | Traçabilité — collecte et recherche dans les sources officielles | recommande | 10.0 | 10.0 | **10.0** | Conforme | présence seule (aucun motif de contenu requis) |
| `DEP-07` | Pièces de preuve A-1 (lettre de décision) et A-2 (article scientifique) | Règles de fonctionnement (art. 113) : liste et identification des pièces | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | présence seule (aucun motif de contenu requis) |
| `DEP-08` | Pièce A-3 (lettre CCQ du 25 septembre 2026) — si retenue | Preuve/LISEZMOI_A3_CCQ_2026-09-25.md | recommande | 0.0 | 0.0 | **0.0** | Non conforme | présence seule (aucun motif de contenu requis) ; fichiers absents : lettre_CCQ_vol_donnees_2026-09-25.pdf |
| `DEP-09` | Livrables de la demande (LaTeX, PDF, dossier complet paginé) | Fondation du Barreau « Seul devant la cour » ; règles de rédaction claire | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | 2/2 motifs de contenu trouvés |
| `DEP-10` | Pagination et cohérence de l'assemblage du dossier complet | Règles de fonctionnement (art. 113) : présentation des pièces | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | demande = 9 pages ; dossier complet = 49 pages ; attendu = 49 (demande + 2 intercalaires + A-1 (2) + A-2 (36)) ; cohérence OK |
| `DEP-11` | Rapport de conformité procédurale (18/18 exigences) | Guides pratiques du Barreau — vérification de conformité | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | 2/2 motifs de contenu trouvés |
| `DEP-12` | Document source .docx (README_LEGAL) conservé pour traçabilité | Traçabilité — conservation des sources | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | présence seule (aucun motif de contenu requis) |
| `DEP-13` | Rapport présenténciel / observations (art. 721 (1) C.cr.) — LaTeX et PDF | Code criminel, art. 721 (1) ; guides de la Fondation du Barreau (peine) | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | 3/3 motifs de contenu trouvés |
| `DEP-14` | Aucun marqueur non rempli ([N° DE DOSSIER], [NOM DE L'ACCUSÉ]…) dans les actes | Exigence de complétude et d'exactitude (Barreau — rédaction claire) | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | aucun marqueur non rempli détecté |
| `DEP-15` | Cohérence du numéro de dossier (documents vs nom du dossier local) | Identification du dossier exigée par la pratique de la Chambre criminelle et pénale | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | numéros dans les actes : ['8953'] ; nom du dossier local : ['8953'] ; incident LVSEV25000954 : présent |
| `DEP-16` | Guide de transmission à la poursuite (procédure chronologique + coordonnées) | Fondation du Barreau « Seul devant la cour » (avis par lettre, courriel ou télécopieur) ; DPCP — coordonnées du district de Québec | obligatoire | 10.0 | 10.0 | **10.0** | Conforme | 4/4 motifs de contenu trouvés |

## 3. Table B — Exigences du Barreau pour la documentation de la requête

| Code | Catégorie | Exigence | Référence | Criticité | **Note /10** | Statut | Vérification |
|---|---|---|---|---|---:|---|---|
| `FORME-01` | Forme | Identification complète du tribunal et du dossier | Pratique de la Chambre criminelle et pénale (outils du Barreau) ; guides de la Fondation du Barreau | obligatoire | **10.0** | Conforme | 3/3 motifs trouvés |
| `FORME-02` | Forme | Objet de la demande énoncé clairement | Seul devant la cour, p. 36 ; guides de préparation à la cour | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `FORME-03` | Forme | Identité et adresse complètes du demandeur | Guide « Préparer la cour – criminel », avis de changement d'adresse | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `FORME-04` | Forme | Date, heure, salle et palais de justice de l'audience | Règles de fonctionnement (art. 113 du Règlement de la Cour du Québec) | obligatoire | **10.0** | Conforme | 3/3 motifs trouvés |
| `FORME-05` | Forme | Signature et date | Seul devant la cour : la partie assume la présentation de sa demande | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `FORME-06` | Forme | Copie transmise à la poursuite | Guide « Préparer la cour » : transmission à la poursuite par lettre, courriel ou télécopieur | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `AVIS-01` | Avis | Avis écrit à la poursuite avant le début de l'audience | Seul devant la cour, étape 6, p. 36 (« la loi exige que vous avisiez la poursuite ») | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `AVIS-02` | Avis | Avis à la Cour et à la partie adverse de l'intention de présenter la demande | Guide « Préparer la cour – criminel » (requêtes) ; Seul devant la cour | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `AVIS-03` | Avis | Demande structurée malgré l'absence de procédures strictes | Seul devant la cour : « Il n'y a pas de procédures strictes pour de telles requêtes » | recommande | **10.0** | Conforme | 1/1 motifs trouvés |
| `PREUVE-01` | Preuve | Liste des pièces | Règles de fonctionnement (art. 113 du Règlement de la Cour du Québec), par. 2) d) | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `PREUVE-02` | Preuve | Énoncé sommaire expliquant la preuve et sa finalité | Règles de fonctionnement, par. 2) a) | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `PREUVE-03` | Preuve | Motifs de pertinence (lien avec les questions en litige) | Procédure pénale (aide-mémoire du Barreau) : vérifier toute question de preuve ressortant de la communication de la preuve | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `PREUVE-04` | Preuve | Identification précise de chaque pièce (auteur, objet, source) | Directive de pratique PRE-1 (communication de la preuve) | obligatoire | **10.0** | Conforme | 3/3 motifs trouvés |
| `PREUVE-05` | Preuve | Copies en nombre suffisant et lisibles | Seul devant la cour : « Renseignez-vous sur les exigences procédurales lors du dépôt de tels documents » | recommande | **10.0** | Conforme | 1/1 motifs trouvés |
| `CONF-01` | Confidentialité | Demande de confidentialité motivée par un fondement juridique | Code criminel, art. 486 à 486.5 (fondement et avis des ordonnances de non-publication) | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `CONF-02` | Confidentialité | Avis de la demande de confidentialité aux parties intéressées | Guide « Préparer la cour » : règles particulières de confidentialité | obligatoire | **10.0** | Conforme | 1/1 motifs trouvés |
| `DEROUL-01` | Déroulement | État de la communication (divulgation) de la preuve vérifié | Procédure pénale (aide-mémoire), p. 9 ; directive PRE-1 | recommande | **10.0** | Conforme | 1/1 motifs trouvés |
| `DEROUL-02` | Déroulement | Demande présentée oralement lors de l'appel du dossier | Règles de fonctionnement (art. 113) : décisions consignées au procès-verbal transmis aux parties | recommande | **10.0** | Conforme | 1/1 motifs trouvés |

## 4. Synthèse par catégorie (moyenne /10)

| Catégorie | Moyenne /10 |
|---|---:|
| Avis | 10.0 |
| Confidentialité | 10.0 |
| Déroulement | 10.0 |
| Forme | 10.0 |
| Preuve | 10.0 |
| Structure du dépôt | 9.4 |

## 5. Recommandations avant le 23 octobre 2026 (points sous 8/10)

1. **`DEP-08` — Pièce A-3 (lettre CCQ du 25 septembre 2026) — si retenue : 0.0/10** (Non conforme). Détail : présence seule (aucun motif de contenu requis) ; fichiers absents : lettre_CCQ_vol_donnees_2026-09-25.pdf.

## 6. Sources officielles téléchargées / présentes

| Fichier source | État |
|---|---|
| `barreau_guides_pratiques.html` | present |
| `barreau_procedure-penale.pdf` | present |
| `barreaumontreal_cq-crim.html` | present |
| `code_criminel_486.4.html` | present |
| `code_criminel_657.1.html` | present |
| `cq_nous-joindre.html` | present |
| `cq_regle_fonctionnement_gestion_instance_criminel.pdf` | present |
| `dpcp_coordonnees_capitale-nationale.html` | present |
| `dpcp_coordonnees_generales.html` | present |
| `dpcp_directive_PRE-1_communication_preuve.pdf` | present |
| `fondation_preparer-cour-criminelle-2025.pdf` | present |
| `fondation_preparer-cour-matiere-penale-2025.pdf` | present |
| `fondation_seul-devant-la-cour-criminelle-penale.pdf` | present |
