# Horaires et durées — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. L’exercice 7 précise la grande aiguille légèrement après le 2 à 10 min 30 s. Les conversions décimales incluent l’erreur classique 1,30 h ≠ 1 h 30 min.

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). 21 identifiants historiques conservés sans retirer de bloc ; 0 exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

3 PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; 5 emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; 46 anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **58 calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

- Id 3419 : Découverte - 1. Instant ou durée
- Id 3420 : Découverte - 2. Minutes et secondes
- Id 3421 : Découverte - 3. De l’après-midi au soir
- Id 3422 : Découverte - 4. Passer l’heure suivante
- Id 3423 : Découverte - 5. Mesurer un intervalle
- Id 3424 : Découverte - 6. Les fractions d’heure
- Id 3425 : Découverte - 7. Lire une horloge à secondes
- Id 3426 : Entraînement - 8. Une heure et demie en décimal
- Id 3427 : Entraînement - 9. Trois quarts d’heure en décimal
- Id 3428 : Entraînement - 10. Retrouver le départ
- Id 3429 : Entraînement - 11. Ajouter des durées
- Id 3430 : Entraînement - 12. Franchir minuit
- Id 3431 : Entraînement - 13. Comparer des chronos
- Id 3432 : Entraînement - 14. Un calendrier
- Id 3433 : Problème - 15. Une correspondance possible ?
- Id 3434 : Problème - 16. Un enregistrement complet
- Id 3435 : Problème - 17. Finir avant la fermeture
- Id 3436 : Problème - 18. Une journée organisée
- Id 3437 : Problème - 19. Répartir une répétition
- Id 3438 : Problème - 20. Des temps exprimés autrement
- Id 3439 : Problème - 21. Choisir le bon départ
