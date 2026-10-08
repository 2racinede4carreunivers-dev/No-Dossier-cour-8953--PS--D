# Rapport de conformité procédurale — Demande d'ajout au dépôt légal

**Date d'évaluation :** 29 September 2026 à 20:42
**Juridiction :** Cour du Québec, Chambre criminelle et pénale, District de Québec
**Dossier :** 8953 – PS-D | **Incident :** LVSEV25000954
**Demandeur :** Philippe Joseph Thomas Savard
**Date d'audience :** 23 octobre 2026 à 9 h 30, salle 2.15

---

## 1. Résumé exécutif de conformité

- **Exigences totales analysées :** 18
- **Satisfaites (conformes) :** 18 / 18
- **Partielles :** 0
- **Non satisfaites :** 0
- **Informatives :** 0

### Statut global : 🟢 **PLEINEMENT CONFORME AUX DIRECTIVES DU BARREAU ET DE LA COUR**

---

## 2. État des pièces au dossier (Dossier `Preuve/`)

| Pièce | Description | Format | Présente | Détails |
|---|---|---|---|---|
| **Pièce A-1** | Courriel et lettre de décision (Revue canadienne de math.) | docx / PDF | âœ“ Oui | Courriel CJM 260814-savard (Kim & McCann) ; salutation ligne 13 : *Cher Professeur Savard* |
| **Pièce A-2** | Article scientifique *« Géométrie du spectre des nombres premiers »* | PDF | âœ“ Oui | Manuscrit soumis (Savard), taille : 503 Ko |

> **Note d'harmonisation terminologique :** La lettre de refus émane officiellement de la > *Revue canadienne de mathématiques* (Canadian Journal of Mathematics). Le document source > mentionnait *Journal canadien de mathématiques*. Le pipeline a harmonisé la désignation > en rappelant les deux appellations afin d'assurer l'exactitude de la pièce devant la Cour.

---

## 3. Matrice de conformité détaillée (Schéma neuronal SQLite)

| Code | Catégorie | Criticité | Exigence | Statut | Motifs vérifiés |
|---|---|---|---|:---:|---|
| `FORME-01` | Forme | obligatoire | Identification complète du tribunal et du dossier | 🟢 Conforme | 'CHAMBRE CRIMINELLE ET PÉNALE', 'LVSEV25000954', '8953' |
| `FORME-02` | Forme | obligatoire | Objet de la demande énoncé clairement | 🟢 Conforme | 'ajout d’une preuve au dépôt légal' |
| `FORME-03` | Forme | obligatoire | Identité et adresse complètes du demandeur | 🟢 Conforme | 'rue du Menuet' |
| `FORME-04` | Forme | obligatoire | Date, heure, salle et palais de justice de l'audience | 🟢 Conforme | '23 octobre 2026', '9 h 30', '2.15' |
| `FORME-05` | Forme | obligatoire | Signature et date | 🟢 Conforme | 'Fait à Lévis' |
| `FORME-06` | Forme | obligatoire | Copie transmise à la poursuite | 🟢 Conforme | 'Copie à la poursuite' |
| `AVIS-01` | Avis | obligatoire | Avis écrit à la poursuite avant le début de l'audience | 🟢 Conforme | 'Avis à la poursuite et à la Cour' |
| `AVIS-02` | Avis | obligatoire | Avis à la Cour et à la partie adverse de l'intention de présenter la demande | 🟢 Conforme | 'avise la Cour et la poursuite' |
| `AVIS-03` | Avis | recommande | Demande structurée malgré l'absence de procédures strictes | 🟢 Conforme | 'aucune procédure stricte' |
| `PREUVE-01` | Preuve | obligatoire | Liste des pièces | 🟢 Conforme | 'Liste des pièces proposées au dépôt' |
| `PREUVE-02` | Preuve | obligatoire | Énoncé sommaire expliquant la preuve et sa finalité | 🟢 Conforme | 'énoncé sommaire' |
| `PREUVE-03` | Preuve | obligatoire | Motifs de pertinence (lien avec les questions en litige) | 🟢 Conforme | 'Motifs de la demande' |
| `PREUVE-04` | Preuve | obligatoire | Identification précise de chaque pièce (auteur, objet, source) | 🟢 Conforme | 'Journal canadien de mathématiques', 'Cher professeur Savard', 'Géométrie du spectre des nombres premiers' |
| `PREUVE-05` | Preuve | recommande | Copies en nombre suffisant et lisibles | 🟢 Conforme | 'exemplaires' |
| `CONF-01` | Confidentialité | obligatoire | Demande de confidentialité motivée par un fondement juridique | 🟢 Conforme | 'fondement' |
| `CONF-02` | Confidentialité | obligatoire | Avis de la demande de confidentialité aux parties intéressées | 🟢 Conforme | 'toute partie intéressée' |
| `DEROUL-01` | Déroulement | recommande | État de la communication (divulgation) de la preuve vérifié | 🟢 Conforme | 'communication de la preuve' |
| `DEROUL-02` | Déroulement | recommande | Demande présentée oralement lors de l'appel du dossier | 🟢 Conforme | 'appel du dossier' |

---

## 4. Livrables générés

1. **Demande en format LaTeX :** `demande_ajout_preuve.tex`
2. **Demande principale en PDF :** `demande_ajout_preuve.pdf`
3. **Dossier complet relié avec pièces intercalaires :** `Dossier_complet_demande_depot_legal_LVSEV25000954.pdf`
4. **Base relationnelle de traçabilité :** `Pipeline/depot_legal.db`
5. **Sources officielles conservées :** `Dependence_Pipeline/sources/` (10 sources)
6. **Pièces de preuve :** `Preuve/` (lettre docx, lettre PDF, article PDF)

---

## 5. Recommandations pour l'audience du 23 octobre 2026

1. **Dépôt au greffe :** déposer deux (2) exemplaires papier de la demande et de chaque pièce au greffe de la Chambre criminelle et pénale du Palais de justice de Québec avant l'audience.
2. **Transmission à la poursuite :** acheminer copie à la poursuite (DPCP) avec accusé de transmission.
3. **Présentation orale :** lors de l'appel du dossier en salle 2.15 à 9 h 30, présenter sommairement la demande en soulignant la pertinence de la lettre pour attester l'identité académique et l'activité de recherche du demandeur.
