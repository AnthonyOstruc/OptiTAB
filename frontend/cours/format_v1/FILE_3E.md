# 3e (brevet) — passage au format v1 (GO de l'utilisateur le 2026-11-03)

Consigne du propriétaire : « vas-y 3e ; il faut faire attention à avoir des exercices
complets, pédagogiques et bien structurés ». 2 agents à la fois, effort high, import
dès « pret » avec `outils/publier_lot.ps1 3e <ids…>`.

Contenu de départ : 18 notions × 21 exercices + notion 253 « Sujets type brevet »
(10 sujets), faits le 27/10 en ANCIEN format (HTML), figures matplotlib.
Export + conversion automatique refaits le 03/11 (`chantier/3e/`).

## Consigne de lot (à lire par chaque agent)

1. **Programme** : cycle 4, attendus de fin de 3e (programme en vigueur, ajustements
   2025 compris). Titres de cours et fiche = intitulé de la notion. Tout ce qui est
   hors programme ou faible est réécrit (« même si nécessaire de refaire de zéro, tu refais »).
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
   texte sur un trait, rien ne déborde, lisible sur téléphone. Scratch : rendu propre
   et lisible (blocs) si la notion en a.
5. **Calculs** : tout vérifié avec sympy (`verif_*.py`), programmes exécutés.
6. **Téléphone** : regarder les captures ; découper toute formule coupée ou réduite.
7. **Fin** : `verifier_notion.py --navigateur` = 0 problème (si Chrome bloque à la
   fermeture : vérificateur sans navigateur + `controle_apercu.mjs` avec délai,
   n'arrêter que ses propres processus). `etat.json` = « pret », RAPPORT.md complet.

Interdits : aucune écriture en base, aucun git, seulement ses dossiers, aucun bloc
supprimé, aucune ligne `Id:` existante modifiée. Respecter `outils/.verrous`.

## Lots

| Lot | Notions | Statut |
|---|---|---|
| C1 | 232 Thalès et triangles semblables, 244 Pythagore | IMPORTÉ 10 h 07 |
| C2 | 233 Rationnels et fractions, 234 Puissances, racines, écriture scientifique | IMPORTÉ 10 h 28 |
| C3 | 235 Arithmétique, 236 Calcul littéral | IMPORTÉ 10 h 09 |
| C4 | 237 Équations, 238 Proportionnalité et pourcentages | IMPORTÉ 10 h 44 |
| C5 | 239 Grandeurs et mesures, 240 Notion de fonction | IMPORTÉ 10 h 58 |
| C6 | 241 Fonctions linéaires et affines, 242 Statistiques | IMPORTÉS (241 11 h 33, 242 11 h 53 — 242 : corrigés 2332, 2334 Q2/Q5 à enrichir, vue téléphone des corrigés modifiés à faire) |
| C7 | 243 Probabilités (IMPORTÉ 11 h 34), 245 Trigonométrie (à faire) |  |
| C8 | 246 Transformations du plan, 247 Géométrie dans l'espace | à faire |
| C9 | 248 Algorithmique et programmation, 250 Raisonner et démontrer | à faire |
| C10 | 253 Sujets type brevet (10 sujets + méthode + fiche) | à faire |

Après le dernier lot : prévenir l'utilisateur. (Rappel : la 4e est aussi en ancien format.)

## Session du 03/11 (consigne : 3 agents, la MOITIÉ des chapitres, STOP à 12 h 00 au plus tard)
- 09 h 10 : C1, C2, C3 lancés ; heure limite donnée aux agents : « pret » à 11 h 30.
- C4/C5 lancés seulement s'il reste assez de temps (≥ 75 min avant 11 h 30) ; sinon pour la prochaine session.
- 11 h 30–12 h 00 : imports puis arrêt complet.
- 10 h 28 : C2 importé ; pas de nouveau lot (moins de 75 min avant 11 h 30) — objectif de la session = C1–C5 (10 notions).
- 10 h 58 : C1–C5 IMPORTÉS (10 notions sur 19 : 232–240, 244). ARRÊT de la session comme demandé (moitié des chapitres).
  Reste : C6 (241, 242), C7 (243, 245), C8 (246, 247), C9 (248, 250), C10 (253 sujets brevet). Reprendre seulement sur GO.
- 11 h 13 : 3 agents, UN par chapitre : 241, 242, 243 ; limite « pret » 11 h 55 (≈ 45 min demandé).
- 11 h 53 : 241, 242, 243 IMPORTÉS → 13 notions sur 19. Arrêt. Reste 245, 246, 247, 248, 250, 253 (brevet).

## Session du 03/11 après-midi (GO « je te laisse finir brevet » à 13 h 21)
- Objectif : finir la 3e (245, 246, 247, 248, 250, 253). 3 agents, UN par chapitre ; quand un agent finit → import, puis lancement du suivant.
- 13 h 22 : 245, 246, 247 lancés ; limite « pret » 14 h 35. Ensuite 248, 250, 253.
- 13 h 25 : le propriétaire supprime toute heure limite : « il faut tout finir ». Agents prévenus ; on va jusqu'au bout des 6 chapitres.
- 14 h 06 : 245 IMPORTÉ ; 14 h 08 : 246 IMPORTÉ → 15 sur 19. 14 h 10 : 248 et 250 lancés (247 en vérification). 253 brevet lancé quand 247 finit.
- 14 h 23 : 247 IMPORTÉ (22 ex., nouvel exercice 5567) → 16 sur 19. 253 découpé en 2 agents successifs (même fichier) :
  partie A = cours, fiche, sujets 01–05 (lancée 14 h 25) ; partie B = sujets 06–10 + contrôle final, après A.
- 253 partie A finie (cours, fiche, sujets 01–05 ; format vérifié : note de service BO n° 33 du 04/09/2025, partie 2 = 12 pts + 2 pts rédaction) → partie B (sujets 06–10) lancée.
- 16 h 15 : 253 IMPORTÉ (10 sujets, 939 contrôles ; erreurs corrigées : traversée s10, inéquation s08, script s08, √50 s09).
- **FIN 3e — 2026-11-03, 16 h 15 : 19/19 notions en v1 en production** (399 exercices, tous `contenu` = `question`).
  Reste mineur : 242 (corrigés 2332, 2334 Q2/Q5 à enrichir ; vue téléphone 2323, 2325, 2326 à regarder).
- 16 h 45 : 242 (finition) et 1re 164 (12 exercices, 5568–5570) IMPORTÉS ; contrôle après import : vérificateur OK sur les deux. TOUT EST FINI (sauf 4e, non demandée).
- 16 h 35 : moteur `optitabDoc.js` (local, à pousser) : « $x$ : », « $x$ ; », « « $x$ » » liés (otm-nb) → plus de ponctuation seule en début de ligne après une formule.
- 16 h 25 : « finis tout mais ne fais pas la 4e » → 2 agents : finition 242 + enrichissement 1re 164 (9 → 11-12 exercices).
- 15 h 42 : 250 IMPORTÉ (9 exercices hors sujet remplacés ; déroulé du brevet retiré du cours → 253) → 18 sur 19. Reste 253 partie B.
- 15 h 22 : 248 IMPORTÉ (tableur retiré : hors chapitre ; module Scratch réutilisable `248_*/figures/scratch.py`) → 17 sur 19.
