# Instructions, répétitions et chemins — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. Les notions demandées sont explicitement présentes : instructions, séquences, entrées, sorties et répétitions, avec ou sans machine. L’exercice 21 propose une erreur possible pour la sortie 14, sans prétendre identifier une erreur unique. Le contrôle mobile a conduit à sortir l’état initial du bloc de code et à raccourcir la consigne du quart de tour, sans débordement.

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). 21 identifiants historiques conservés sans retirer de bloc ; 0 exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

13 PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; 16 emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; 45 anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **49 calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

- Id 3608 : Découverte - 1. Reconnaître une instruction
- Id 3609 : Découverte - 2. Entrée et sortie
- Id 3610 : Découverte - 3. Un programme en deux étapes
- Id 3611 : Découverte - 4. Coder un déplacement global
- Id 3612 : Découverte - 5. Répéter une addition
- Id 3613 : Découverte - 6. Tourner n’est pas avancer
- Id 3614 : Découverte - 7. Compresser une séquence
- Id 3615 : Entraînement - 8. Dessiner un carré
- Id 3616 : Entraînement - 9. Corriger un carré ouvert
- Id 3617 : Entraînement - 10. Un escalier régulier
- Id 3618 : Entraînement - 11. Deux ordres de calcul
- Id 3619 : Entraînement - 12. Répéter un bloc entier
- Id 3620 : Entraînement - 13. Tester plusieurs entrées
- Id 3621 : Entraînement - 14. Une suite évolutive
- Id 3622 : Problème - 15. Programmer un rectangle
- Id 3623 : Problème - 16. Un détour autour d’un obstacle
- Id 3624 : Problème - 17. Déboguer une direction
- Id 3625 : Problème - 18. Un compteur de motifs
- Id 3626 : Problème - 19. Une donnée ne change pas toute seule
- Id 3627 : Problème - 20. Limiter le nombre de pas
- Id 3628 : Problème - 21. Un petit projet autonome
