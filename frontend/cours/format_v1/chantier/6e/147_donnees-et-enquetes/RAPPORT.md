# Données et enquêtes — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. Une enquête complète remplace une simple lecture mécanique : question neutre, population, protocole, tableaux, filtre et interprétation prudente.

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). 21 identifiants historiques conservés sans retirer de bloc ; 0 exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

2 PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; 3 emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; 44 anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **24 calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

- Id 3566 : Découverte - 1. Poser une question précise
- Id 3567 : Découverte - 2. Qui interroger ?
- Id 3568 : Découverte - 3. Compter des réponses brutes
- Id 3569 : Découverte - 4. Une mesure avec son unité
- Id 3570 : Découverte - 5. Lire un tableau croisé
- Id 3571 : Découverte - 6. Compléter des données
- Id 3572 : Découverte - 7. Une donnée manquante
- Id 3573 : Entraînement - 8. Filtrer un catalogue
- Id 3574 : Entraînement - 9. Contrôler un comptage
- Id 3575 : Entraînement - 10. Mesurer de façon comparable
- Id 3576 : Entraînement - 11. Choisir une représentation
- Id 3577 : Entraînement - 12. Regrouper sans changer le total
- Id 3578 : Entraînement - 13. Noter des réponses multiples
- Id 3579 : Entraînement - 14. Préparer une enquête sur les déchets
- Id 3580 : Problème - 15. Choisir une excursion
- Id 3581 : Problème - 16. Éviter une conclusion abusive
- Id 3582 : Problème - 17. Retrouver une case croisée
- Id 3583 : Problème - 18. Corriger une saisie
- Id 3584 : Problème - 19. Construire puis vérifier des barres
- Id 3585 : Problème - 20. Un projet de sondage
- Id 3586 : Problème - 21. Comparer deux relevés
