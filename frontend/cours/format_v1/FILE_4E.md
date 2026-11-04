# 4e — passage au format v1 (GO de l'utilisateur le 2026-11-03, soir)

Consigne du propriétaire : « je te laisse commencer maintenant la 4e, 2 agents max ».
Même exigence que la 3e : exercices complets, pédagogiques, bien structurés.
UN agent par chapitre, 2 à la fois (3 autorisés exceptionnellement de 19 h 40 jusqu'à la fin du prochain chapitre, puis retour à 2 : « limite du PC »), effort high, sans heure limite ; import dès
« pret » avec `outils/publier_lot.ps1 4e <id>`, puis lancement du chapitre suivant.

Contenu de départ : 18 notions × 21 exercices faits le 27/10 en ANCIEN format
(HTML), figures matplotlib. Export + conversion automatique refaits le 03/11
(`chantier/4e/`).

## Consigne de lot (à lire par chaque agent)

1. **Programme** : cycle 4, attendus de fin de 4e (programme en vigueur, ajustements
   2025 compris). Ce qui relève de la 3e (ex. trigonométrie sinus/tangente, fonctions
   affines, homothétie) n'est pas exigé en 4e. Titres de cours et fiche = intitulé de
   la notion. Tout ce qui est hors programme ou faible est réécrit (« même si
   nécessaire de refaire de zéro, tu refais »).
2. **Conversion propre** : la conversion automatique est un point de départ. Relire
   CHAQUE bloc : cours structuré façon manuel (définitions, propriétés, méthodes,
   exemples, erreurs fréquentes, à retenir), fiche dense et claire.
3. **Exercices complets et pédagogiques** (priorité du propriétaire) : énoncé clair
   avec questions numérotées ; corrigé (`Étapes:`) avec méthode, étapes détaillées,
   résultat encadré, erreur fréquente / à retenir ; `Solution:` courte. Progression
   Découverte → Entraînement → Problème → Type brevet. Doublons et exercices
   faibles remplacés (même Id, nouveau titre permis). Titres « Type - Sujet ».
4. **Figures** : TOUTES refaites au style des livres (`figures_livre.py`), aucune
   ancienne image matplotlib conservée. Présentes partout où elles aident : cours,
   fiche, énoncé (sans donner la réponse) ET corrigé (complétée en vert). Jamais de
   texte sur un trait, rien ne déborde, lisible sur téléphone. Scratch : vrais blocs
   avec le module `chantier/3e/248_*/figures/scratch.py` (le copier, ne pas le modifier).
5. **Calculs** : tout vérifié avec sympy (`verif_*.py`), programmes exécutés.
6. **Téléphone** : regarder les captures ; découper toute formule coupée ou réduite.
7. **Fin** : `verifier_notion.py --navigateur` = 0 problème (si Chrome bloque à la
   fermeture : vérificateur sans navigateur + `controle_apercu.mjs` avec délai,
   n'arrêter que ses propres processus). `etat.json` = « pret », RAPPORT.md complet.

Interdits : aucune écriture en base, aucun git, seulement ses dossiers, aucun bloc
supprimé, aucune ligne `Id:` existante modifiée. Respecter `outils/.verrous`.
Fichiers temporaires préfixés par l'id de la notion (dossier temporaire partagé).

Modèles : les notions de 3e finies (`chantier/3e/`), en particulier 244 Pythagore,
232 Thalès, 245 Trigonométrie, 248 Algorithmique, 242 Statistiques.

## File (un agent par chapitre, 2 à la fois)

| Notion | Statut |
|---|---|
| 249 Calculer avec les nombres relatifs | IMPORTÉ 18 h 45 |
| 251 Fractions et nombres premiers | IMPORTÉ 19 h 11 |
| 252 Puissances et notation scientifique | IMPORTÉ 20 h 13 |
| 254 Carrés et racines carrées | IMPORTÉ 20 h 07 |
| 255 Calcul littéral et distributivité | IMPORTÉ 21 h 07 |
| 256 Équations et résolution de problèmes | IMPORTÉ 21 h 05 |
| 257 Proportionnalité et pourcentages | IMPORTÉ 21 h 30 |
| 258 Grandeurs composées et unités | IMPORTÉ 22 h 17 |
| 259 Relier des grandeurs et lire des graphiques | IMPORTÉ 22 h 18 |
| 260 Statistiques et diagrammes | IMPORTÉ 04/11 08 h 57 |
| 281 Probabilités | IMPORTÉ 04/11 09 h 29 |
| 282 Construire et comparer des triangles | IMPORTÉ 04/11 09 h 58 |
| 283 Théorème de Pythagore | IMPORTÉ 04/11 10 h 11 |
| 286 Théorème de Thalès (triangles emboîtés) | IMPORTÉ 04/11 11 h 20 |
| 287 Cosinus dans le triangle rectangle | IMPORTÉ 04/11 10 h 40 |
| 288 Translations, agrandissements et réductions | IMPORTÉ 04/11 10 h 54 |
| 289 Pyramides, cônes et volumes | IMPORTÉ 04/11 11 h 54 |
| 290 Algorithmique et programmation | IMPORTÉ 04/11 11 h 35 |

## Journal
- 2026-11-03 soir : ré-export des 18 notions (378 exercices) + conversion automatique (0 problème de syntaxe). 249 et 251 lancés.
- ~20 h 15 : consigne du propriétaire : finir 252, 254, 255 (en cours) + 4 chapitres (256, 257, 258, 259), puis STOP pour ce soir. 2 agents max. Reprise de 260, 281… sur GO.
- 20 h 07 : 254 IMPORTÉ ; pas de relance (retour à 2 agents : 252 et 255 tournent).
- 20 h 13 : 252 IMPORTÉ ; 256 lancé (2 agents : 255, 256).
- ~20 h 50 : le propriétaire demande 3 agents pour finir 255–259 vers 22 h–22 h 30 ; 257 lancé (255, 256, 257). 258 et 259 dès qu'un agent se libère, puis STOP.
- 21 h 05 : 256 IMPORTÉ ; 258 lancé (255, 257, 258).
- 21 h 07 : 255 IMPORTÉ ; 259 lancé (257, 258, 259) = derniers de la soirée.
- 21 h 30 : 257 IMPORTÉ ; pas de relance (fin de soirée : restent 258, 259 en cours).
- 22 h 18 : 258 et 259 IMPORTÉS → 9 notions sur 18 en ligne (249, 251, 252, 254–259). ARRÊT pour ce soir comme demandé ; aucun agent ne tourne.
  Reste (sur GO) : 260, 281, 282, 283, 286, 287, 288, 289, 290.
- 22 h 20 : moteur `optitabDoc.js` (local, à pousser) : une unité écrite après une espace insécable reste collée à la formule (« $1\,000$ L »), signalé par 258.

## Session du 04/11 (GO « je te laisse finir la classe 4e »)
- 07 h 50 : 260 et 281 lancés (2 agents max). Puis 282, 283, 286, 287, 288, 289, 290 au fil de l'eau.
- 08 h 57 : 260 IMPORTÉ → 10/18 ; 282 lancé (281, 282).
- 09 h 29 : 281 IMPORTÉ → 11/18 ; 283 lancé (282, 283).
- 09 h 35 : le propriétaire demande 3 agents (« pour ne pas être impair ») ; 286 lancé (282, 283, 286). Restent 287, 288, 289, 290.
- 09 h 58 : 282 IMPORTÉ → 12/18 ; 287 lancé (283, 286, 287).
- 10 h 11 : 283 IMPORTÉ → 13/18 ; 288 lancé (286, 287, 288). Restent 289, 290.
- 10 h 40 : 287 IMPORTÉ → 14/18 ; 289 lancé (286, 288, 289). Reste 290.
- 10 h 54 : 288 IMPORTÉ → 15/18 ; 290 lancé (286, 289, 290) = derniers.
- 11 h 20 : 286 IMPORTÉ → 16/18 ; plus rien à lancer (289, 290 en cours).
- 11 h 35 : 290 IMPORTÉ → 17/18 ; reste 289 en cours.
- **FIN 4e — 2026-11-04, 11 h 54 : 18/18 notions en v1 en production.** Aucun agent ne tourne. Suite : 5e sur GO (max 10 exercices/chapitre).
