# 5e — refonte au niveau 3e/4e, 10 exercices par chapitre (GO du 2026-11-04, midi)

Consigne du propriétaire : « de la 5e au CP, mettre max 10 exercices, comme ça ça
devient beaucoup plus rapide ; je te laisse refaire si besoin les exercices, solutions
et schémas de zéro ; qu'il couvre tout le programme officiel et que ce soit impeccable ».
UN agent par chapitre, 5 à la fois (3 autorisés à 12 h 27, 4 à 13 h 45, 5 à 13 h 47), effort high, import dès « pret »
(`outils/publier_lot.ps1 5e <id>` PUIS `outils/retirer_exercices.py` pour supprimer en
base les exercices retirés, avec sauvegarde).

État de départ : 20 notions × 21 exercices déjà au format v1 (import du 30/10, autre
session), mais moins complètes que la 3e/4e (erreur fréquente ~17 %, schémas ~45 %).
Ré-export du 04/11 dans `chantier/5e/*/source_en_ligne/` = l'état EN LIGNE (fait foi).

## Consigne de chapitre (à lire par chaque agent)
0. **Vrais exercices de 5e** (consigne du propriétaire, 04/11) : chaque exercice est un
   exercice comme on en fait en classe de 5e en France — conforme au programme officiel
   et au niveau des manuels français de 5e, ni hors programme ni trop difficile ; complet.
   Aucune mention du brevet (titres, énoncés, cours).
Les règles de `FILE_4E.md` (« Consigne de lot ») s'appliquent, adaptées au programme
de 5e (cycle 4, attendus de fin de 5e, ajustements 2025), avec ces changements :
1. **10 exercices au maximum** (8 à 10), qui couvrent ENSEMBLE toutes les capacités
   du programme officiel du chapitre. Progression : 3 Découverte, 3 Entraînement,
   2-3 Problème, 1-2 Synthèse (PAS de « Type brevet » : il n'y a pas de brevet en 5e — consigne du propriétaire ; « Synthèse - <sujet> » = exercice complet mêlant plusieurs capacités). On GARDE en priorité les
   meilleurs exercices existants (leur `Id:` ne change pas, on peut les réécrire en
   entier) ; un exercice peut être refait de zéro (même Id, nouveau titre). On ne crée
   des `nouveau-N` que si une capacité du programme n'est couverte par aucun exercice
   existant gardé.
2. **Exercices retirés** : leurs blocs sont SUPPRIMÉS de `exercices.txt` et leurs Id
   listés dans `exercices_retires.txt` (un Id par ligne, suivi d'un commentaire
   « # titre — raison »). Le vérificateur les accepte ; l'orchestrateur les supprime
   en base après l'import (sauvegarde automatique).
3. **Corrigés complets** : méthode, étapes détaillées, résultat encadré, erreur
   fréquente / à retenir dans CHAQUE exercice ; `Solution:` courte. Titres
   « Type - Sujet ».
4. **Cours façon manuel et fiche dense** relus et corrigés (refaits si faibles) ; titres
   = intitulé de la notion. Exemples du cours différents des exercices.
5. **Figures** : style des livres partout où elles aident (cours, fiche, énoncé sans la
   réponse, corrigé complété en vert) ; anciennes figures imparfaites refaites ; jamais
   de texte sur un trait ; lisibles sur téléphone. Scratch : module
   `chantier/3e/248_*/figures/scratch.py` (copie).
6. **Calculs** vérifiés avec sympy (`verif_<id>.py`), programmes exécutés.
7. **Fin** : `verifier_notion.py --navigateur` = 0 problème ; captures téléphone
   regardées en UNE ou DEUX passes groupées (pas de boucles) ; `etat.json` =
   « pret » ; RAPPORT.md (section « Refonte 10 exercices 2026-11-04 »).
Interdits : aucune écriture en base, aucun git, seulement son dossier ; ne jamais
modifier une ligne `Id:` d'un exercice gardé ; respecter `outils/.verrous` ; fichiers
temporaires préfixés par l'id de la notion.

Modèles : les notions de 4e finies (`chantier/4e/`), même structure, au niveau 5e.

## File
| Notion | Statut |
|---|---|
| 261 Opérations et priorités | IMPORTÉ 12 h 25 (10 ex., 11 copies supprimées) |
| 262 Multiples, diviseurs et partages | IMPORTÉ 12 h 23 (10 ex., 11 doublons supprimés) |
| 263 Découvrir les nombres relatifs | IMPORTÉ 13 h 12 (11 copies supprimées) |
| 264 Additionner et soustraire des relatifs | IMPORTÉ 13 h 08 (11 copies supprimées) |
| 265 Fractions, quotients et comparaisons | IMPORTÉ 13 h 09 (11 copies supprimées) |
| 266 Additionner et soustraire des fractions | IMPORTÉ 13 h 35 (11 copies supprimées ; calculs de 4e retirés) |
| 267 Carrés et cubes | IMPORTÉ 13 h 34 (11 supprimés) |
| 268 Lettres, formules et motifs | IMPORTÉ 13 h 40 (11 copies supprimées) |
| 269 Développer, réduire et démontrer | IMPORTÉ 14 h 03 (11 copies supprimées) |
| 270 Inconnues et équations simples | IMPORTÉ 13 h 59 (11 copies supprimées) |
| 271 Proportionnalité et pourcentages | IMPORTÉ 14 h 09 (11 copies supprimées ; pas de ratio : retiré du programme 2026) |
| 272 Repérage et grandeurs en fonction d'une autre | IMPORTÉ 14 h 29 (11 copies supprimées) |
| 273 Angles et droites parallèles | IMPORTÉ 14 h 38 (11 copies supprimées) |
| 274 Construire et comprendre les triangles | IMPORTÉ 14 h 33 (11 copies supprimées) |
| 275 Symétries et demi-tour | IMPORTÉ 14 h 48 (11 copies supprimées) |
| 276 Parallélogrammes et aires | IMPORTÉ 14 h 49 (11 copies supprimées) |
| 277 Solides, disques et volumes | IMPORTÉ 15 h 12 (11 copies supprimées) |
| 278 Organiser et interpréter des données | IMPORTÉ 15 h 13 (11 retirés ; histogramme hors programme 2026) |
| 279 Hasard et probabilités | IMPORTÉ 15 h 11 (11 retirés ; événement contraire = 4e) |
| 280 Penser et programmer par blocs | IMPORTÉ 15 h 18 (11 copies supprimées) |

## Journal
- 2026-11-04 midi : GO ; ré-export ; outils `retirer_exercices.py` (suppression avec
  sauvegarde) et `exercices_retires.txt` reconnu par `verifier_notion.py`. 261 et 262 lancés.
- 12 h 23 : 262 IMPORTÉ (importer_v1 ignore désormais les Id de exercices_retires.txt) + 11 doublons supprimés ; 263 lancé.
- 12 h 25 : 261 IMPORTÉ + 11 copies supprimées. 12 h 27 : limite d'utilisation atteinte (reprise 12 h 40) : agent 263 interrompu, à reprendre. Le propriétaire autorise 3 agents.
- 12 h 41 : limite levée ; 263 repris, 264 et 265 lancés (3 agents).
- 12 h 50 : propriétaire : « en 5e il n'y a pas de brevet » → « Type brevet » remplacé par « Synthèse » (261, 262 republiés) ; consigne « vrais exercices de 5e » ajoutée ; agents 263-265 prévenus.
- 13 h 09 : 264, 265 IMPORTÉS (+ 22 copies supprimées) → 4/20 ; 266, 267 lancés (263, 266, 267).
- 13 h 12 : 263 IMPORTÉ → 5/20 ; 268 lancé (266, 267, 268).
- 13 h 35 : 266, 267 IMPORTÉS → 7/20 ; 269, 270 lancés (268, 269, 270).
- 13 h 40 : 268 IMPORTÉ → 8/20 ; 271 lancé (269, 270, 271).
- 13 h 45 : le propriétaire demande un 4e agent ; 272 lancé (269, 270, 271, 272).
- 13 h 47 : 5e agent demandé ; 273 lancé (269–273).
- 13 h 59 : 270 IMPORTÉ → 9/20 ; 274 lancé (269, 271, 272, 273, 274).
- 14 h 03 : 269 IMPORTÉ → 10/20 ; 275 lancé (271–275).
- 14 h 09 : 271 IMPORTÉ → 11/20 ; 276 lancé (272–276).
- 14 h 29 : 272 IMPORTÉ → 12/20 ; 277 lancé (273–277).
- 14 h 33 : 274 IMPORTÉ → 13/20 ; 278 lancé (273, 275, 276, 277, 278).
- 14 h 38 : 273 IMPORTÉ → 14/20 ; 279 lancé (275–279). Reste 280.
- 14 h 49 : 275, 276 IMPORTÉS → 15/20 (… 16 avec 274) ; 280 lancé. Défaut signalé par 275 : quadrillage non aligné (style `grille` sans step=1) → corrigé et republié en 4e 288 et 3e 246 (14 h 59).
- 15 h 13 : 277, 278, 279 IMPORTÉS → 19/20 ; reste 280 en cours.
- **FIN 5e — 2026-11-04, 15 h 18 : 20/20 notions, 200 exercices (10 par chapitre), tous v1, 0 mention du brevet (vérifié en base). 220 doublons supprimés (sauvegardes retirer_exercices_*.json).** Suite : 6e sur GO.
