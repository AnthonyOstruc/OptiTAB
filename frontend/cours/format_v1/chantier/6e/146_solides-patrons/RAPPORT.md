# Solides & patrons — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. Les patrons relèvent explicitement de la consolidation des acquis CM1/CM2 ; les attendus nouveaux de sixième portent sur la vision des assemblages de cubes. Le pliage de la croix et l’échec du rectangle 2 × 3 sont contrôlés par transport exact de repères.

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). 0 identifiants historiques conservés sans retirer de bloc ; 21 exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

11 PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; 20 emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; 0 anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **17 calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

- Id nouveau-1 : Découverte - 1. Reconnaître les solides
- Id nouveau-2 : Découverte - 2. Faces, arêtes et sommets
- Id nouveau-3 : Découverte - 3. Un pavé droit
- Id nouveau-4 : Découverte - 4. Prisme ou pyramide
- Id nouveau-5 : Découverte - 5. Cylindre et cône
- Id nouveau-6 : Découverte - 6. Ce qu’est un patron
- Id nouveau-7 : Découverte - 7. Observer une croix de six carrés
- Id nouveau-8 : Entraînement - 8. Le faux patron rectangulaire
- Id nouveau-9 : Entraînement - 9. Construire un patron à la règle
- Id nouveau-10 : Entraînement - 10. Apparier les faces du pavé
- Id nouveau-11 : Entraînement - 11. Des arêtes incompatibles
- Id nouveau-12 : Entraînement - 12. Nommer les bases
- Id nouveau-13 : Entraînement - 13. Une pyramide triangulaire
- Id nouveau-14 : Entraînement - 14. Voir les arêtes cachées
- Id nouveau-15 : Problème - 15. Fabriquer une boîte ouverte
- Id nouveau-16 : Problème - 16. Budget de papier
- Id nouveau-17 : Problème - 17. Trouver une erreur de vocabulaire
- Id nouveau-18 : Problème - 18. Faces opposées dans la croix
- Id nouveau-19 : Problème - 19. Ajouter une languette
- Id nouveau-20 : Problème - 20. Un solide à partir de ses faces
- Id nouveau-21 : Problème - 21. Deux dessins, un seul bon patron
