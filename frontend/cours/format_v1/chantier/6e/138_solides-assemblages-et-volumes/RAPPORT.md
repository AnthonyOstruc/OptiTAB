# Solides, assemblages et volumes — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. Volume déterminé par dénombrement de cubes unités ; pas de formule générale de pavé imposée. Deux perspectives supplémentaires relient les assemblages à leurs vues et à leurs plans.

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). 21 identifiants historiques conservés sans retirer de bloc ; 0 exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

5 PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; 6 emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; 45 anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **52 calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

- Id 3545 : Découverte - 1. Le cube unité
- Id 3546 : Découverte - 2. Une couche rectangulaire
- Id 3547 : Découverte - 3. Deux couches identiques
- Id 3548 : Découverte - 4. Comparer sans se laisser tromper
- Id 3549 : Découverte - 5. Lire un plan de hauteurs
- Id 3550 : Découverte - 6. Voir de face
- Id 3551 : Découverte - 7. Réorganiser les cubes
- Id 3552 : Entraînement - 8. Un bloc à trois étages
- Id 3553 : Entraînement - 9. Retirer une colonne
- Id 3554 : Entraînement - 10. Compléter un pavé
- Id 3555 : Entraînement - 11. Des couches différentes
- Id 3556 : Entraînement - 12. Deux volumes égaux
- Id 3557 : Entraînement - 13. Des cubes invisibles
- Id 3558 : Entraînement - 14. La vue ne suffit pas
- Id 3559 : Problème - 15. Une réserve pour construire
- Id 3560 : Problème - 16. Un escalier de cubes
- Id 3561 : Problème - 17. Un trou traversant
- Id 3562 : Problème - 18. Reconstruire d’après deux vues
- Id 3563 : Problème - 19. Changer d’unité de cube
- Id 3564 : Problème - 20. Ajouter un cube sans changer la face
- Id 3565 : Problème - 21. Le défi des 24 cubes
