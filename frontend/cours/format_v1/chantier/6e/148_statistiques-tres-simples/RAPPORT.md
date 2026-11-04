# Statistiques très simples — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. Aucune moyenne ni médiane obligatoire : le programme 2025 attend ici la collecte, les tableaux, le filtrage et les lectures usuelles. Les parts simples réinvestissent fractions et pourcentages. La question de majorité de l’exercice 20 est reformulée sans ambiguïté.

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). 0 identifiants historiques conservés sans retirer de bloc ; 21 exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

5 PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; 10 emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; 0 anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **41 calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

- Id nouveau-1 : Découverte - 1. Comprendre un effectif
- Id nouveau-2 : Découverte - 2. Un total de catégories
- Id nouveau-3 : Découverte - 3. Lire une case
- Id nouveau-4 : Découverte - 4. Lire des barres
- Id nouveau-5 : Découverte - 5. Des graduations de deux
- Id nouveau-6 : Découverte - 6. Une évolution dans le temps
- Id nouveau-7 : Découverte - 7. Lire une moitié de disque
- Id nouveau-8 : Entraînement - 8. Un effectif absent
- Id nouveau-9 : Entraînement - 9. Une proportion simple
- Id nouveau-10 : Entraînement - 10. Croiser deux critères
- Id nouveau-11 : Entraînement - 11. Au moins deux livres
- Id nouveau-12 : Entraînement - 12. Compter les objets, pas les personnes
- Id nouveau-13 : Entraînement - 13. Vérifier un pourcentage
- Id nouveau-14 : Entraînement - 14. Ne pas inventer entre deux points
- Id nouveau-15 : Problème - 15. Comparer des groupes de tailles différentes
- Id nouveau-16 : Problème - 16. Une échelle trompeuse
- Id nouveau-17 : Problème - 17. Un graphique complet
- Id nouveau-18 : Problème - 18. Deux relevés successifs
- Id nouveau-19 : Problème - 19. Reconstituer un diagramme circulaire
- Id nouveau-20 : Problème - 20. Un résultat à justifier
- Id nouveau-21 : Problème - 21. Choisir et argumenter
