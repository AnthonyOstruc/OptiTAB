# Notion 103 — Arithmétique (Terminale, Maths expertes)

**État : prêt.** Cours 109, fiche 48 et 19 exercices au format v1, remis à niveau
au programme officiel de Maths expertes (BO 2019, copie dans
`livre/livre-maths/livre-maths-expertes/recherche/expertes-2019.pdf`).

## Texte

- **Cours réécrit** (9 parties, ordre du programme) : divisibilité, division euclidienne,
  congruences (grandes puissances, disjonction des cas, critères par 9 et 11 démontrés),
  PGCD et algorithme d'Euclide (propriété clé démontrée), Bézout et Gauss, congruences
  linéaires et équations diophantiennes, nombres premiers (crible, décomposition,
  diviseurs), petit théorème de Fermat, chiffrement affine. Les **3 démonstrations du
  programme** sont rédigées en entier (écriture du PGCD sous la forme $au + bv$ par le
  plus petit élément, Gauss, infinité des nombres premiers) ; codes Python exécutés.
- **Erreurs de fond corrigées** :
  - le petit théorème de Fermat était présenté comme « non exigible au Bac » : il est
    au programme (contenus) — corrigé ; sections « Bonus » supprimées ;
  - exercice 1150 (« Écriture astucieuse ») : réponses **incomplètes** (diviseurs
    négatifs oubliés) : Q1 $\{1, 3, 5, 7, 11, 25\}$ (et non $\{5, 7, 11, 25\}$),
    Q2 $\{1, 3, 5, 7, 13\}$, Q4 12 valeurs dont $0, 2, 3, 4$ ; encadré « Erreur fréquente » ajouté ;
  - exercice 1153 Q3 : affirmation fausse (« la méthode fonctionne pour toute expression
    $a^{2n} + ba^n + c$ ») remplacée par la vraie condition ;
  - exercice 1148 Q3 et 1144 Q2 : le PPCM (hors programme) est calculé par les
    décompositions ou avec la relation admise explicitement.
- **Exercices** : tous restructurés façon pilote (méthode / étapes / résultat,
  Solution courte cohérente) ; tableaux natifs (tables de congruences, Euclide,
  vérifications) au lieu des tableaux cassés de la conversion ; DS 1155 en
  « Partie A… / Question A1… » ; 1159 : question 2 ajoutée (même résultat par les
  congruences, conforme au titre « Récurrence et Congruences ») ; preuves rendues
  rigoureuses (disjonction des cas modulo 3 et 8, Gauss cité, réciproques des équations).
- **Fiche** réduite à l'essentiel (≈ 2 écrans) avec un encadré des 5 pièges.
- `verif_arithmetique.py` : **695 contrôles, tous justes** (chaque reste, PGCD, couple
  de Bézout, inverse, ensemble de solutions par force brute, valeurs des figures).

## Figures (style livres, `figures/figures.py`)

- **2 refaites** : les 2 images en ligne (division posée colorée, schéma « a = q x b + r »
  ambigu, style ancien) sont remplacées par une droite des entiers ($-17 = 4 \times (-5) + 3$)
  et le pavage du rectangle $252 \times 198$ par des carrés (algorithme d'Euclide).
- **6 ajoutées** : cycle des restes de $3^n$ modulo 7 (cours + DS), crible
  d'Ératosthène jusqu'à 100, arbre de décomposition de 360, cycles $3^n$ mod 10,
  $7^n$ mod 11 (exercice 1161) et $7^n$ mod 10 (exercice 1158).
- 0 conservée, 0 retirée sans remplacement. Aucun texte sur un trait (contrôle
  automatique ; seul avertissement : la cote « 252 », normal). Largeurs ≤ 823 px.

## Contrôles

- `verifier_notion.py --navigateur` : 0 problème (après raccourcissement des lignes de
  code Python, trop larges sur téléphone).

## Remarques pour l'orchestrateur

- Moteur : `## Question A1 : …` (recommandé par le guide pour les DS) n'obtient pas la
  pastille numérotée (l'expression régulière n'accepte que `\d+[a-z]?`) : rendu en
  titre simple, lisible.
- Contrôle Chrome : un bloc de code plus large que l'écran est signalé « trop large »
  alors que `.otm-code` défile (`overflow-x: auto` dans la feuille de style ; la
  détection de `controle_apercu.mjs` ne reconnaît que `.otm-scroll` ou un style en
  ligne) ; contourné en gardant des lignes de code courtes (≤ 33 caractères).

## Finition 2026-11-02

**État : prêt** (agent-finition-T8). 19 exercices ; 12 ont désormais une figure (3 avant).

### Exercices réécrits (Id, type et difficulté conservés)
- **1153** « Entraînement - Chiffrement affine » (remplace « Récurrence et divisibilité 2 », quasi-doublon de 1151) : chiffrement du programme absent des exercices. Clé $y \equiv 5x + 8 \pmod{26}$ : MATHS → QIZRU ; inverse $21$ de $5$ modulo $26$ ; équivalence $y \equiv 5x + 8 \iff x \equiv 21y + 14$ démontrée dans les deux sens ; NPIJA → BRAVO ; clé $13x + 8$ inutilisable (A et C → I, $\mathrm{PGCD}(13, 26) = 13$).
- **1146** « Entraînement - Synthèse : PGCD, Bézout et équation diophantienne » (l'ancien était décousu : $n = 1\,260$ sans lien, PPCM hors programme, rappel sans rapport) : décompositions de $504$ et $420$, PGCD $84$ (deux méthodes), Bézout, résolution complète de $504x + 420y = 168$ (Gauss + réciproque : $(2 + 5k\,;-2 - 6k)$), $504x + 420y = 100$ impossible.
- **1144** « Découverte - PGCD par l'algorithme d'Euclide » : questions PPCM (hors programme) remplacées par les diviseurs communs ($=$ diviseurs du PGCD) et un problème de carrelage (plaque $84 \times 60$ → carreaux de $12$ cm, $35$ carreaux).
- **1148 Q3** : PPCM remplacé par $84x + 30y = 18$ (solution $(-3, 9)$) et $84x + 30y = 20$ (impossible).
- **1157 Q3** : doublon exact de 1147 Q4 ($n^3 - n$ divisible par $6$) remplacé par « $n^5 - n$ divisible par $30$ » (factorisation + question 2 + nombres premiers entre eux, erreur fréquente).
- 1143 : renvoi « exercice suivant » supprimé (l'ordre en ligne n'est pas garanti).

### Titres
18 titres répétaient « Arithmétique - » : tous refaits « Type - Sujet » (ex. « Découverte - Premières congruences modulo 5 », « Entraînement - Restes de grandes puissances », « Problème - Principe du chiffrement RSA ») ; « DS - … Devoir Surveillé Complet » → « Type examen - Divisibilité, congruences et nombres premiers ».

### Figures
- **Revérifiées** : les 8 existantes (seul avertissement : la cote « 252 », normal).
- **Ajoutées (11)** : cours `cours_chiffrement` (schéma E → 4 → 5 → F et retour) ; exercices `horloge_mod5` (1145, classes modulo 5), `ex1143_division` (84 = 60 × 1 + 24), `ex1144_euclide` (pavage 84 × 60 par carrés) et `ex1144_plaque` (35 carreaux), `ex1147_cycle` (2ⁿ mod 7), `ex1148_euclide` (algorithme d'Euclide en tableau, le diviseur et le reste descendent, PGCD entouré), `ex1149_arbre` (2 023 = 7 × 17²), `ex1146_droite` (points entiers de $6x + 5y = 2$), `ex1153_chiffrement` (schéma de chiffrement / déchiffrement), `ex1154_rsa` (clé publique / clé secrète).
- Sans figure, par choix (calcul pur, pas de figure décorative) : 1150, 1152, 1159, 1151, 1160 ; 1156 et 1157 ont leurs tableaux de congruences en tableaux natifs.

### Contrôles
- `verif_arithmetique.py` : 719 contrôles, tous justes (contrôles PPCM/récurrence remplacés par ceux des contenus nouveaux, chiffrement testé lettre à lettre et pour toutes les clés).
- `figures_livre.py` : 19/19, 0 erreur (avertissements = cotes).
- `verifier_notion.py --navigateur` : OK, 0 problème (avant les dernières retouches téléphone). Après les retouches, Chrome est resté bloqué à la fermeture : contrôle refait selon la consigne, `verifier_notion.py` sans navigateur = OK et `controle_apercu.mjs --rapide` = 118 vues, toutes à 0 (débordement, formules, images, blocs trop larges).
- Captures téléphone regardées (1153, 1146, 1157, 1144, 1148) : 6 formules réduites ou coupées redécoupées (décompositions de 504 et 420 en chaînes alignées, équivalences remplacées par « équivaut à », réciproque de 1146 alignée, relation de Bézout + couple sur deux lignes) ; tableau de congruences de 1157 Q1 raccourci (il débordait) ; schémas de chiffrement resserrés (869 → ~770 px).
- Le contrôle Chrome reste bloqué à la fermeture après les captures (connu) : seuls mes propres processus `controle_apercu.mjs` ont été arrêtés.
