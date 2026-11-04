# Comprendre le hasard — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. Le vocabulaire savant est expliqué sans être exigé en autonomie. Les modèles simples distinguent équiprobabilité, indépendance et proportion observée ; le tirage sans remise ne demande qu’une mise à jour des effectifs, sans probabilité conditionnelle formalisée.

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). 21 identifiants historiques conservés sans retirer de bloc ; 0 exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

7 PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; 10 emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; 36 anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **38 calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

- Id 3587 : Découverte - 1. Ce qui relève du hasard
- Id 3588 : Découverte - 2. Possible, impossible ou certain
- Id 3589 : Découverte - 3. Un tirage parmi quatre jetons
- Id 3590 : Découverte - 4. La moitié des faces
- Id 3591 : Découverte - 5. Une roue régulière
- Id 3592 : Découverte - 6. Une échelle de probabilités
- Id 3593 : Découverte - 7. Une pièce ne se souvient pas
- Id 3594 : Entraînement - 8. Des cartes numérotées
- Id 3595 : Entraînement - 9. Une couleur ou une autre
- Id 3596 : Entraînement - 10. Comparer deux sacs
- Id 3597 : Entraînement - 11. Des résultats observés
- Id 3598 : Entraînement - 12. Prévoir sans promettre
- Id 3599 : Entraînement - 13. Une roue aux parts inégales
- Id 3600 : Entraînement - 14. Un tableau de deux lancers
- Id 3601 : Problème - 15. Corriger une probabilité impossible
- Id 3602 : Problème - 16. Un jeu équitable
- Id 3603 : Problème - 17. Observer un sac inconnu
- Id 3604 : Problème - 18. Changer la composition
- Id 3605 : Problème - 19. Sans remise
- Id 3606 : Problème - 20. Au moins un pile
- Id 3607 : Problème - 21. Comparer deux séries
