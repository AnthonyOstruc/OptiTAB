# File d'attente — passe de finition (demande du 2026-11-02)

**18 h 42 : GO de l'utilisateur « je te laisse tout finir jusqu'au brevet, tu attends mon go ».**
→ finir TOUS les lots ci-dessous (Terminale ET Seconde), puis STOP : prévenir et ATTENDRE le GO avant la 3e.
2 agents à la fois (3 autorisés exceptionnellement depuis 20 h 40 pour finir plus tôt), effort high ; import (relier_nouveaux + ré-export + simulation + --appliquer) dès « pret ».

## Consigne de la passe de finition (à lire par chaque agent)

Ordre de priorité du propriétaire :
1. **Revérifier TOUTES les figures existantes** (cours, fiche, exercices) : détecteur
   texte/trait de `figures_livre.py` + CHAQUE image regardée à l'œil (chevauchement,
   texte sur un trait, débordement, justesse mathématique : la courbe correspond à sa
   fonction et les valeurs à l'énoncé, lisibilité téléphone : texte assez grand).
   Refaire toute figure imparfaite.
2. **Figures partout où elles aident** : cours, fiche, énoncé ET corrigé (`Étapes:`),
   version du corrigé complétée en vert. Pas de figure décorative ; pas de figure
   d'énoncé qui donnerait la réponse. Style livre via `figures_livre.py`.
3. **Assez d'exercices** : une notion qui a moins de 10 exercices est enrichie
   (exercices `Id: nouveau-N` à la fin de `exercices.txt`) jusqu'à 10–12, en couvrant
   les compétences du programme officiel peu travaillées, niveaux répartis
   (Découverte, Entraînement, Problème, Type examen). Exercices COMPLETS : méthode,
   étapes détaillées, résultat encadré, erreur fréquente.
4. **Titres** : « Type - Sujet » (sans le nom du chapitre répété, sans majuscules
   abusives). Cours et fiche = intitulé officiel de la notion.
5. **Qualité** : tout exercice faible, faux ou hors programme est réécrit
   (« même si nécessaire de refaire de zéro, tu refais »). Tout calcul nouveau ou
   modifié est vérifié avec sympy (code Python : exécuté réellement).
6. **Téléphone** : regarder les captures ; découper toute formule coupée ou réduite.
7. **Fin** : `verifier_notion.py --navigateur` = 0 problème (si Chrome reste bloqué à
   la fermeture : vérificateur sans navigateur + `controle_apercu.mjs` avec délai,
   n'arrêter que ses propres processus). `etat.json` = « pret », section
   « Finition 2026-11-02 » dans RAPPORT.md.

Interdits : aucune écriture en base, aucun git, travailler seulement dans ses
dossiers, ne supprimer aucun bloc, ne modifier aucune ligne `Id:` existante.
Respecter les verrous `outils/.verrous` (d'autres sessions compilent aussi).

## Lots

| Lot | Notions | Statut |
|---|---|---|
| P1 | 1re 153, 154 | IMPORTÉ 13 h 23 |
| P2 | 1re 155, 157, 159 | IMPORTÉ 13 h 19 |
| B1 | Tle 369 « Sujets type bac » (thème 118) | IMPORTÉ + ACTIVÉ 13 h 45 (exercice 4956) |
| T1 | Tle 81, 82, 83 | IMPORTÉ 16 h 11 (83 n'a que 5 exercices → lot E1) |
| T2 | Tle 84, 85, 86 | IMPORTÉ 16 h 36 |
| T7 | Tle 96, 98 | IMPORTÉS (98 17 h 02 ; 96 17 h 17, enrichi à 11 exercices 17 h 44) |
| F1 | VÉRIF FIGURES 2nde 165–171 | IMPORTÉ 15 h 50 |
| T3 | Tle 87, 88 | IMPORTÉ 19 h 35 (87 : 13 ex., 88 : 12 ex.) |
| T4 | Tle 89, 90 | IMPORTÉ 19 h 41 (89 : 14 ex., 90 : 12 ex.) |
| T5 | Tle 180, 92, 93 | IMPORTÉ 20 h 31 |
| T6 | Tle 95, 97, 179 | IMPORTÉ 20 h 33 (12 ex. chacune) — 179 : rappels de 1re gardés dans le cours (à valider) |
| T8 | Tle 102, 103, 104 (expertes ; 104 a 9 exercices → enrichir) | IMPORTÉ 22 h 02 (104 : 12 ex.) |
| T9 | Tle 99, 100 (5 exercices chacun → enrichir ; 100 → « Algorithmes du programme de Terminale », renommer en base) | IMPORTÉ 21 h 32 (99 : 11 ex., 100 : 12 ex., renommée) |
| E1 | Tle 83, 98 : enrichissement seul (5 exercices chacun → 10–12) | IMPORTÉ 22 h 15 (11 ex. chacune) |
| S1 | 2nde 165, 166, 167 (figures déjà vérifiées : finition seule) | IMPORTÉ 22 h 16 (12, 12, 17 ex.) |
| S2 | 2nde 168, 169, 170 (figures déjà vérifiées : finition seule) | IMPORTÉ 22 h 39 |
| S3 | 2nde 171, 172, 173, 178 (172, 173, 178 : vérifier aussi les figures) | IMPORTÉ 23 h 06 |
| S4 | 2nde 174, 175, 176, 177 (vérifier aussi les figures ; 177 a 9 exercices → enrichir) | IMPORTÉ 23 h 32 (177 : 12 ex.) |

## Historique
- 18 h 42 : 169 exercices (Tle 15 notions + 2nde 166) affichaient l'ANCIEN énoncé (champ
  `contenu` non mis à jour par l'importeur du 28/10, et la page lit `contenu` avant
  `question`) → `outils/synchro_contenu.py --appliquer` (sauvegarde
  `sauvegardes/synchro_contenu_20261102-184205.json`). 0 restant.
- 16 h 37 : arrêt demandé ; 14 h : arrêt propre puis reprise de T1, T2, F1.
- 22 h 03 : titres des cours/fiches alignés en base sur la ligne « Titre: » des fichiers (`outils/titres_docs.py`, désormais appelé par `publier_lot.ps1`) : 32 titres corrigés (1re, Tle). 369 laissé tel quel (apostrophe typographique en base).

## FIN — 2026-11-02, 23 h 32
- TOUS LES LOTS IMPORTÉS : Première, Terminale (22 notions + bac 369), Seconde (14 notions).
- Aucun agent ni processus de contrôle ne tourne ; verrous vides.
- STOP : attendre le GO de l'utilisateur pour la 3e (brevet), déjà exportée et convertie dans chantier/3e/.
- Points laissés à la relecture du propriétaire : barème du bac 18 + 2 ; rappels de Première gardés dans le cours Tle 179 ;
  le moteur (optitabDoc.js) peut laisser « : » ou « ; » seul en début de ligne sur téléphone (espace avant ponctuation).
