# Pièce A-3 proposée — Lettre CCQ du 25 septembre 2026 (vol de données)

**Dossier : 8953 – PS-D | Incident : LVSEV25000954 | Infraction : possession dans le but de trafic**

## Où déposer le fichier ?
Déposez la numérisation de la lettre dans ce dossier `Preuve/` sous le nom :
`lettre_CCQ_vol_donnees_2026-09-25.pdf`
(Conservez aussi l'original papier pour l'audience du 23 octobre 2026.)

## Pourquoi c'est pertinent selon votre demande
- Lettre adressée à : Philippe Savard.
- Émetteur : Commission de la construction du Québec (CCQ).
- Date : 25 septembre 2026.
- Objet annoncé : vol de données incluant nom, date de naissance, adresse, numéro d'assurance sociale (NAS).
- Mention d'un risque de fraude ciblée.
- Votre situation : retraité de l'industrie (électricien) depuis 2 ans, pension versée en un chèque complet, plus de paie active — étonnement que des données confidentielles soient encore conservées.


Pratique suggérée :
1. Préparer une version CAVIARDÉE pour le dossier public (ex. : NAS : XXX-XXX-123 — ne montrer que si exigé, adresse partiellement masquée).
2. Apporter l'original + une copie complète sous enveloppe scellée pour le juge seul, si la Cour l'autorise.
3. Demander que la pièce complète soit mise sous scellé / confidentielle.

## Insertion prévue dans la demande existante
Fichier actuel : `Demande_ajout_depot_legal/demande_ajout_preuve.tex`
- Pièces actuelles : A-1 (lettre Revue canadienne de mathématiques — « Cher Professeur Savard »), A-2 (article Géométrie du spectre... 36 pages).
- Pièce à ajouter : A-3 (lettre CCQ).
- Sections à mettre à jour : 1 (Objet), 2 (Contenu), 3 (Motifs — identité civile Philippe Savard vs identité professionnelle), Liste des pièces, Conclusion, Avis à la poursuite, Annexe méthodologique.

Ne modifiez pas le .tex à la main tant que le PDF de la lettre n'est pas placé ici — le pipeline (`Pipeline/orchestrator_legal.py` + `chemins.py`) devra ensuite être mis à jour pour intégrer A-3 automatiquement et régénérer le dossier complet de 49 pages.

## Prochaine étape attendue de vous
1. Placer `lettre_CCQ_vol_donnees_2026-09-25.pdf` dans `Preuve/`.
2. N° de dossier confirmé : **8953 – PS-D** (corrigé dans le .docx source, les actes et les PDF le 7 octobre 2026) ; n° d'incident : **LVSEV25000954**.
3. Indiquer si vous voulez version caviardée ou intégrale au dépôt.
