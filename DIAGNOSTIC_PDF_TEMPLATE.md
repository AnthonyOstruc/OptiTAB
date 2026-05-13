# Diagnostic OptiTAB — Template PDF

Document source pour le PDF "Diagnostic gratuit maths" envoyé en E1 de la séquence email
(voir landing `/diagnostic-maths-gratuit`).

## Comment utiliser ce document

- **Pour un designer** : utilise ce fichier comme source de copy. Mise en forme libre selon la
  charte OptiTAB (cf. section "Charte design" en fin de document). Sortie attendue : un PDF
  A4, 6 à 8 pages, lisible sur mobile et imprimable.
- **Pour un dev (rendu automatique)** : ce template est conçu pour être rendu via un moteur
  type Handlebars / Jinja avec deux variables principales : `level` et `difficulty`. Les blocs
  marqués `[VARIANT level=X]` ou `[VARIANT difficulty=Y]` sont à substituer selon le profil
  du lead.
- **Version v1 (à shipper rapidement)** : prendre uniquement le bloc TERMINALE +
  COURS_VS_EXERCICES en mise en forme (c'est le profil le plus fréquent et le plus
  monétisable). Les autres variantes peuvent être ajoutées progressivement.

## Structure générale (8 pages)

| Page | Bloc | Type | Personnalisation |
|------|------|------|------------------|
| 1 | Cover | Universel | `firstName`, `level` |
| 2 | Résumé du diagnostic | Par `difficulty` | 5 variantes |
| 3 | Tes 3 priorités | Par `level` | 7 variantes (Collège→BTS+Parent) |
| 4-5 | Plan 7 jours | Par `level` | 7 variantes |
| 6 | 5 erreurs à éviter | Par `level` | 7 variantes |
| 7 | Exercice corrigé type | Par `level` | 7 variantes |
| 8 | Méthode + Et après | Universel | — |

## Variables de personnalisation

| Variable | Source | Exemple |
|----------|--------|---------|
| `{{firstName}}` | Champ form | `Léa` |
| `{{level}}` | Champ form, mappé | `Terminale` |
| `{{level_short}}` | Mapping interne | `term` |
| `{{difficulty_label}}` | Mapping form → texte | `comprendre les exercices une fois sorti·e du cours` |
| `{{generation_date}}` | `new Date().toLocaleDateString('fr-FR')` | `13/05/2026` |
| `{{platform_url}}` | Constante | `https://www.optitab.net/plateforme-maths` |
| `{{exercices_url}}` | Constante | `https://www.optitab.net/exercices-corriges` |

Mapping difficulty form → texte :

| Code form | `{{difficulty_label}}` |
|-----------|------------------------|
| `cours_vs_exercices` | comprendre les exercices une fois sorti·e du cours |
| `organisation` | t'organiser et réviser efficacement |
| `methode` | avoir une méthode claire pour aborder les exercices |
| `bac` | préparer le Bac avec une structure solide |
| `motivation` | garder ta motivation et ne pas te décourager |

---

# PAGE 1 — COVER (UNIVERSEL)

```
─────────────────────────────────────────────────

           [Logo OptiTAB]

                  ★

         TON DIAGNOSTIC MATHS

           Personnalisé · {{level}}

─────────────────────────────────────────────────


Pour : {{firstName}}
Niveau : {{level}}
Date : {{generation_date}}

Lecture estimée : 10 minutes


Ce document est confidentiel. Il a été préparé
spécialement pour toi à partir de tes réponses.


─────────────────────────────────────────────────

OptiTAB — Plateforme de maths en ligne
contact@optitab.net · www.optitab.net
```

---

# PAGE 2 — RÉSUMÉ DU DIAGNOSTIC (PAR `difficulty`)

## Titre de la page (universel)

> **Ce qu'on a appris de tes réponses**

## Bloc d'intro (universel)

```
{{firstName}}, tu m'as dit que ta principale difficulté en maths,
c'était de {{difficulty_label}}.

C'est une difficulté que je vois reviendar TRÈS souvent. La bonne
nouvelle : elle est traitable, à condition de comprendre exactement
ce qui se passe.

Voilà ce que ça veut dire, concrètement.
```

## [VARIANT difficulty=cours_vs_exercices]

```
LE CONSTAT

Tu comprends le cours quand il est expliqué.
Tu suis les exemples du prof sans problème.
Mais dès que tu te retrouves seul·e devant un exercice nouveau,
ça coince.

CE QUI SE PASSE EN VRAI

Ce n'est pas que tu n'as "pas compris" le cours.
C'est que tu n'as pas encore acquis la TRADUCTION :
comment transformer une notion théorique en une démarche
applicable à un exercice nouveau.

Cette traduction ne se travaille pas en cours. Elle se travaille
en faisant des exercices CORRIGÉS PAS À PAS, où tu peux comparer
ta démarche à la bonne démarche.

L'ENJEU

Ton blocage n'est pas un problème de niveau. C'est un problème
de méthode. Tu vas voir tes notes monter dès que tu auras
travaillé 2 à 3 semaines avec la bonne approche.
```

## [VARIANT difficulty=organisation]

```
LE CONSTAT

Tu travailles. Tu révises. Mais tu as l'impression de ne pas
avancer aussi vite que tu le voudrais.

CE QUI SE PASSE EN VRAI

Le problème n'est pas la quantité de travail. C'est la STRUCTURE
de ce travail. Tu passes probablement :
  → trop de temps à relire le cours (révision passive)
  → trop peu de temps à faire des exercices (révision active)
  → trop peu de temps à identifier tes points faibles

Les notes montent quand le travail devient ciblé : 80 % du temps
sur ce qui te bloque, 20 % sur ce que tu maîtrises déjà.

L'ENJEU

Ce n'est pas un problème de motivation ou de niveau. C'est un
problème de répartition. Quelques ajustements peuvent débloquer
plusieurs points de moyenne.
```

## [VARIANT difficulty=methode]

```
LE CONSTAT

Face à un énoncé, tu te poses la question :
"Par où commencer ?"

Tu connais probablement les notions. Mais tu n'as pas un
"protocole" clair pour attaquer un exercice.

CE QUI SE PASSE EN VRAI

Les bons élèves en maths n'ont pas plus d'intuition que toi.
Ils ont une méthode systématique :

  1. Lire l'énoncé en repérant ce qu'on demande
  2. Identifier l'outil/le théorème à utiliser
  3. Appliquer mécaniquement
  4. Conclure proprement

Sans cette méthode, chaque exercice ressemble à un problème
neuf. AVEC, 80 % des exercices deviennent des automatismes.

L'ENJEU

Acquérir une méthode prend 3 à 4 semaines de pratique régulière.
Mais une fois acquise, elle te sert dans TOUS les chapitres.
```

## [VARIANT difficulty=bac]

```
LE CONSTAT

Tu prépares le Bac. Tu as besoin d'efficacité, pas de tâtonnement.
Tu veux savoir :
  → ce qui tombe vraiment
  → comment l'aborder
  → comment maximiser tes points

CE QUI SE PASSE EN VRAI

Le Bac de maths n'est pas un test d'intelligence. C'est un test
de méthodes acquises. Les chapitres-clés sont connus, les types
d'exercices sont connus, les pièges sont connus.

Le problème de beaucoup d'élèves : ils révisent en mode
"j'apprends tout" au lieu de réviser en mode "je m'entraîne sur
les types d'exos qui tombent".

L'ENJEU

Sur les 3 mois avant le Bac, viser un mode d'entraînement ciblé
sur les types d'exos officiels. C'est ce qui fait gagner le plus
de points par heure de travail.
```

## [VARIANT difficulty=motivation]

```
LE CONSTAT

Tu sais que tu pourrais y arriver. Mais l'élan n'y est pas.
Tu repousses, tu te décourages, tu doutes.

CE QUI SE PASSE EN VRAI

La motivation en maths suit une règle simple : elle vient des
PETITES VICTOIRES, pas de la volonté.

Si tu n'as pas réussi un exercice depuis 2 semaines, ton cerveau
associe "maths" à "échec". Ta motivation chute logiquement.

Si tu réussis un petit exercice par jour, ton cerveau associe
"maths" à "victoire". La motivation revient mécaniquement.

L'ENJEU

Il ne te manque pas de la volonté. Il te manque un cadre où
tu peux gagner régulièrement. C'est ce qu'on va construire dans
ton plan 7 jours.
```

---

# PAGE 3 — TES 3 PRIORITÉS (PAR `level`)

## Titre de la page (universel)

> **Tes 3 priorités absolues**
> *Si tu ne devais travailler que 3 choses, ce serait celles-ci.*

## [VARIANT level=Terminale]

```
PRIORITÉ N°1 — Maîtriser les dérivées et leurs applications
─────────────────────────────────────────────────────────
C'est LE chapitre central de la Terminale.
Étude de fonctions, optimisation, lecture de tableaux de
variations : tout y passe par la dérivée.

→ Objectif : savoir dériver toute fonction du programme en
  moins d'1 minute, et savoir étudier le signe de la dérivée
  pour conclure sur les variations.


PRIORITÉ N°2 — Solidifier les suites et leurs limites
─────────────────────────────────────────────────────────
Suites arithmétiques, géométriques, récurrence, limites :
ce sont des automatismes à acquérir.

Beaucoup d'élèves perdent des points sur des suites par
manque de pratique, alors que la démarche est toujours la
même : reconnaître le type, appliquer la formule, conclure.


PRIORITÉ N°3 — Travailler la rédaction des exercices types Bac
─────────────────────────────────────────────────────────
Les correcteurs notent la RÉDACTION autant que le résultat.
Apprendre à structurer ta copie (énoncé du théorème → vérif
des hypothèses → conclusion) peut te faire gagner 2 à 4 points.

→ Objectif : t'entraîner sur 5 exercices types Bac avec
  rédaction propre dans les 2 prochaines semaines.
```

## [VARIANT level=Première]

```
PRIORITÉ N°1 — Le second degré (fonction, équation, inégalité)
─────────────────────────────────────────────────────────
C'est la base de toute la Première et de la Terminale.
Forme canonique, discriminant, factorisation, signe du trinôme :
tu dois pouvoir tout faire les yeux fermés.


PRIORITÉ N°2 — Comprendre les dérivées (introduction)
─────────────────────────────────────────────────────────
La Première introduit la dérivée. Beaucoup d'élèves ne
comprennent pas le pourquoi (taux de variation, tangente).
Si tu ne comprends pas le pourquoi, la Terminale sera difficile.


PRIORITÉ N°3 — Les suites
─────────────────────────────────────────────────────────
Suites arithmétiques et géométriques. Apprends à les
reconnaître automatiquement et à appliquer les formules.
```

## [VARIANT level=Seconde]

```
PRIORITÉ N°1 — Solides bases en calcul littéral
─────────────────────────────────────────────────────────
Développement, factorisation, identités remarquables :
sans ces automatismes, toute la suite du lycée sera laborieuse.


PRIORITÉ N°2 — Maîtriser les fonctions affines et de référence
─────────────────────────────────────────────────────────
Lecture graphique, calcul d'image et d'antécédent, équation
de droite. Ce sont les briques de tout le programme du lycée.


PRIORITÉ N°3 — Travailler les vecteurs
─────────────────────────────────────────────────────────
Coordonnées, colinéarité, somme de vecteurs. Souvent
sous-travaillés en Seconde, ils reviennent en Première et
en Terminale.
```

## [VARIANT level=Collège]

```
PRIORITÉ N°1 — Solide maîtrise du calcul fractionnaire
─────────────────────────────────────────────────────────
Addition, soustraction, multiplication, division de fractions.
Si ce n'est pas automatique, tout le lycée sera difficile.


PRIORITÉ N°2 — Calcul littéral (développement, factorisation)
─────────────────────────────────────────────────────────
Apprends à manipuler les expressions avec lettres. Identités
remarquables : (a+b)², (a-b)², (a+b)(a-b).


PRIORITÉ N°3 — Théorème de Pythagore et théorème de Thalès
─────────────────────────────────────────────────────────
Reconnaître quand les utiliser, savoir poser une démonstration
propre. Ce sont les "exercices guides" du Brevet.
```

## [VARIANT level=Prépa]

```
PRIORITÉ N°1 — Travail régulier sur les fondamentaux du sup
─────────────────────────────────────────────────────────
Polynômes, complexes, équations différentielles, intégration.
Pas de raccourcis : 30 min/jour de pratique sur les
fondamentaux fait toute la différence.


PRIORITÉ N°2 — Rédaction et rigueur
─────────────────────────────────────────────────────────
En prépa, la rédaction compte autant que le résultat. Apprends
à structurer chaque démonstration : énoncé, hypothèses,
conclusion.


PRIORITÉ N°3 — Banque d'exercices types concours
─────────────────────────────────────────────────────────
Constitue-toi une bibliothèque mentale d'exercices classiques.
Les concours réutilisent toujours les mêmes archétypes.
```

## [VARIANT level=BTS]

```
PRIORITÉ N°1 — Maîtriser les outils appliqués (statistiques, suites, dérivées simples)
─────────────────────────────────────────────────────────
En BTS, les maths sont appliquées. L'enjeu est de savoir les
APPLIQUER à un contexte métier, pas de faire du théorique.


PRIORITÉ N°2 — Travailler les exercices types BTS
─────────────────────────────────────────────────────────
Les sujets de BTS sont relativement standardisés. S'entraîner
sur des annales est le meilleur usage de ton temps.


PRIORITÉ N°3 — Solidifier les bases si nécessaire
─────────────────────────────────────────────────────────
Beaucoup d'étudiants en BTS ont des lacunes du lycée. Le
parcours Bases & Méthode d'OptiTAB est conçu pour ce cas.
```

## [VARIANT level=Parent] *(vouvoiement)*

```
PRIORITÉ N°1 — Identifier la nature exacte du blocage
─────────────────────────────────────────────────────────
Avant de chercher une solution, identifiez si le blocage de
votre enfant est lié au cours (compréhension), à la méthode
(comment aborder un exercice), ou à la régularité (travail
non-soutenu).

Ces trois cas n'appellent pas la même réponse.


PRIORITÉ N°2 — Installer une routine de travail courte mais régulière
─────────────────────────────────────────────────────────
20 à 30 minutes par jour, 5 jours par semaine, sont plus
efficaces que 3 heures le dimanche. La régularité est le
facteur n°1 du progrès en maths.


PRIORITÉ N°3 — Investir dans des ressources structurées plutôt que dispersées
─────────────────────────────────────────────────────────
Mélanger vidéos YouTube, sites gratuits et conseils
contradictoires fait perdre du temps. Une plateforme
structurée comme OptiTAB (parcours par niveau, exercices
corrigés pas à pas) coûte moins cher qu'une heure de cours
particulier par mois — et apporte un cadre cohérent.
```

---

# PAGES 4-5 — TON PLAN 7 JOURS (PAR `level`)

## Titre de la page (universel)

> **Ton plan 7 jours**
> *À démarrer dès aujourd'hui. 30 minutes par jour suffisent.*

## Intro (universel)

```
Ce plan est conçu pour t'apporter 3 choses :

  1. Une routine régulière (la base du progrès en maths)
  2. Un focus sur tes priorités (pas du saupoudrage)
  3. Une victoire chaque jour (la motivation suit)

Règle d'or : termine ce que tu commences chaque jour, même
si c'est moins ambitieux que prévu. La régularité bat
toujours l'intensité.
```

## [VARIANT level=Terminale]

```
JOUR 1 — Diagnostic personnel sur les dérivées
─────────────────────────────────────────────────────
20 min : refaire 3 calculs de dérivées du dernier contrôle
10 min : noter dans un carnet TES erreurs typiques


JOUR 2 — Dérivées + étude de signe
─────────────────────────────────────────────────────
30 min : 4 exercices "calculer la dérivée + étudier son signe"
         → focus sur la PROPRETÉ de la rédaction


JOUR 3 — Suites
─────────────────────────────────────────────────────
30 min : 3 exercices sur les suites (arithmétiques,
         géométriques, récurrence)


JOUR 4 — Rédaction d'un exercice type Bac
─────────────────────────────────────────────────────
40 min : prendre 1 exercice type Bac sur les fonctions,
         le rédiger comme si tu le rendais à un correcteur


JOUR 5 — Repos actif (lecture du cours)
─────────────────────────────────────────────────────
20 min : relire les FORMULES essentielles (dérivées, limites
         de référence). Pas d'exercices, juste de la révision.


JOUR 6 — Bilan + 1 vrai sujet
─────────────────────────────────────────────────────
60 min : prendre 1 exercice complet d'annale Bac,
         le faire en conditions chrono (30 min),
         puis comparer ta copie au corrigé (30 min)


JOUR 7 — Synthèse et planning de la semaine suivante
─────────────────────────────────────────────────────
15 min : noter ce qui a marché et ce qui doit s'améliorer
15 min : prévoir le plan de la semaine suivante
```

## [VARIANT level=Première]

```
JOUR 1 — Refaire les bases du second degré
         (20 min : 4 trinômes à factoriser)

JOUR 2 — Inégalités du second degré
         (30 min : 4 exercices "résoudre f(x) > 0")

JOUR 3 — Comprendre une dérivée
         (30 min : 1 vidéo de cours + 2 exercices simples)

JOUR 4 — Étude de fonctions simples
         (30 min : 2 exercices "tableau de variations")

JOUR 5 — Repos actif
         (20 min : revoir les formules de dérivées)

JOUR 6 — Suites
         (30 min : 4 exercices suites arithmétiques/géo)

JOUR 7 — Synthèse + planning semaine 2
         (30 min)
```

## [VARIANT level=Seconde]

```
JOUR 1 — Calcul littéral (développement)
JOUR 2 — Calcul littéral (factorisation + identités remarquables)
JOUR 3 — Fonctions affines (lecture graphique)
JOUR 4 — Fonctions affines (équation de droite, exos)
JOUR 5 — Vecteurs (coordonnées, opérations)
JOUR 6 — Vecteurs (colinéarité, exos d'application)
JOUR 7 — Bilan + planning semaine 2

Cadence cible : 25 à 30 minutes par jour.
```

## [VARIANT level=Collège]

```
JOUR 1 — Fractions (addition/soustraction)
JOUR 2 — Fractions (multiplication/division)
JOUR 3 — Calcul littéral (développement simple)
JOUR 4 — Identités remarquables ((a+b)², etc.)
JOUR 5 — Pythagore (4 exercices avec rédaction)
JOUR 6 — Thalès (4 exercices avec rédaction)
JOUR 7 — Bilan + planning semaine 2

Cadence cible : 20 à 25 minutes par jour.
```

## [VARIANT level=Prépa]

```
JOUR 1 — Polynômes (racines, factorisation, division euclidienne)
JOUR 2 — Complexes (forme algébrique, trigonométrique, applications)
JOUR 3 — Suites (étude de convergence, raisonnement par récurrence)
JOUR 4 — Limites de fonctions (techniques classiques)
JOUR 5 — Repos actif (lecture des théorèmes-clés)
JOUR 6 — Sujet type concours (1 problème complet, 1h30)
JOUR 7 — Bilan rigueur + planning

Cadence cible : 45 à 60 minutes par jour.
```

## [VARIANT level=BTS]

```
JOUR 1 — Suites (annale BTS)
JOUR 2 — Statistiques descriptives (1 exo type)
JOUR 3 — Dérivées simples appliquées
JOUR 4 — Fonctions exponentielle/logarithme (selon spécialité)
JOUR 5 — Repos actif (lecture de formulaire)
JOUR 6 — Sujet d'annale BTS complet (1h30)
JOUR 7 — Bilan + planning semaine 2
```

## [VARIANT level=Parent] *(vouvoiement)*

```
Plan recommandé sur 7 jours, pour votre enfant.

JOUR 1 — Séance de diagnostic en autonomie (20 min, observer)
JOUR 2 — Travail sur 1 priorité identifiée (25 min)
JOUR 3 — Travail sur la même priorité (consolidation)
JOUR 4 — Travail sur la 2e priorité
JOUR 5 — Pause active : relecture du cours
JOUR 6 — 1 exercice complet sur la priorité n°1
JOUR 7 — Court bilan ensemble : qu'est-ce qui a marché ?

L'objectif n'est pas la performance. C'est l'installation
d'une routine. Si votre enfant tient 7 jours, vous avez
déjà gagné l'essentiel.
```

---

# PAGE 6 — 5 ERREURS À ÉVITER (PAR `level`)

## Titre de la page (universel)

> **Les 5 erreurs typiques à ton niveau**
> *Si tu te reconnais, ce sont les premières choses à corriger.*

## [VARIANT level=Terminale]

```
ERREUR N°1 — Oublier de vérifier les hypothèses d'un théorème
   Tu appliques un théorème SANS écrire qu'il s'applique.
   → Tu perds 1 à 2 points par exercice. Au Bac, ça fait
     une note entière.

ERREUR N°2 — Confondre f(x) et f'(x) dans les variations
   Tu étudies le signe de f au lieu du signe de f'.
   → Erreur de débutant qui revient même en TS.

ERREUR N°3 — Calculer une limite "à la va-vite"
   Tu donnes le résultat sans détailler les étapes.
   → Les correcteurs sanctionnent. Détaille TOUJOURS :
     "lim … = 0 / 0, forme indéterminée, on factorise..."

ERREUR N°4 — Ne pas justifier une suite par récurrence
   Tu sautes les étapes (initialisation, hérédité, conclusion).
   → Récurrence = 3 étapes obligatoires. Aucune n'est
     optionnelle.

ERREUR N°5 — Mal poser un tableau de variations
   Tu oublies les limites aux bornes, ou tu inverses
   le sens d'une flèche.
   → Apprends une fois pour toutes la structure :
     ligne 1 = x, ligne 2 = f'(x) avec son signe,
     ligne 3 = f(x) avec ses limites et extrema.
```

## [VARIANT level=Première]

```
ERREUR N°1 — Mauvaise factorisation d'un trinôme
   Tu utilises mal la formule de factorisation
   a(x-x₁)(x-x₂).

ERREUR N°2 — Oublier le signe du a dans une parabole
   Tu confonds les variations selon que a > 0 ou a < 0.

ERREUR N°3 — Mal lire un graphique de fonction
   Tu confonds image et antécédent.

ERREUR N°4 — Calcul d'angle ou de longueur sans préciser le triangle
   Tu utilises un théorème sans justifier le contexte.

ERREUR N°5 — Mauvaise interprétation d'une dérivée
   Tu calcules mais tu ne sais pas dire CE QUE ÇA VEUT DIRE.
```

## [VARIANT level=Seconde]

```
ERREUR N°1 — Oublier les parenthèses en calcul littéral
ERREUR N°2 — Confondre développer et factoriser
ERREUR N°3 — Inverser image et antécédent
ERREUR N°4 — Mal écrire une équation de droite
ERREUR N°5 — Confondre vecteur et point
```

## [VARIANT level=Collège]

```
ERREUR N°1 — Mal additionner des fractions sans même dénominateur
ERREUR N°2 — Oublier le signe — devant une parenthèse
ERREUR N°3 — Confondre carré et double (x² vs 2x)
ERREUR N°4 — Mal poser une démonstration de Pythagore
ERREUR N°5 — Mal poser une démonstration de Thalès
```

## [VARIANT level=Prépa]

```
ERREUR N°1 — Sauter des étapes dans une démonstration
ERREUR N°2 — Mal poser un raisonnement par récurrence
ERREUR N°3 — Confondre les notations (∀, ∃, ⇒, ⇔)
ERREUR N°4 — Manipuler des complexes sans précautions de domaine
ERREUR N°5 — Mal rédiger une étude de convergence
```

## [VARIANT level=BTS]

```
ERREUR N°1 — Ne pas contextualiser un résultat numérique
ERREUR N°2 — Confondre les types de suites (arithmétique / géométrique)
ERREUR N°3 — Mauvaise interprétation d'un graphique statistique
ERREUR N°4 — Calculer sans présenter les résultats clairement
ERREUR N°5 — Ignorer les unités et la précision demandée
```

## [VARIANT level=Parent] *(vouvoiement)*

```
ERREUR N°1 — Mettre la pression sur les notes plutôt que sur la régularité
ERREUR N°2 — Faire les exercices "à la place" de l'enfant
ERREUR N°3 — Multiplier les ressources (chaîne YouTube + livre + appli...)
ERREUR N°4 — Investir dans des cours particuliers avant d'avoir essayé l'autonomie
ERREUR N°5 — Comparer le rythme de votre enfant à celui d'un camarade
```

---

# PAGE 7 — EXEMPLE D'EXERCICE CORRIGÉ PAS À PAS (PAR `level`)

## Titre de la page (universel)

> **Voici la méthode OptiTAB en action**
> *Un exercice de ton niveau, corrigé étape par étape.*

## [VARIANT level=Terminale]

```
ÉNONCÉ
─────────────────────────────────
Soit f la fonction définie sur ℝ par
   f(x) = x³ − 3x + 2

1. Calculer f'(x)
2. Étudier le signe de f'(x)
3. En déduire le tableau de variations de f


ÉTAPE 1 — Lire l'énoncé
─────────────────────────────────
On nous demande les variations.
→ Outil : dérivée + signe + tableau.


ÉTAPE 2 — Calculer la dérivée
─────────────────────────────────
f'(x) = 3x² − 3


ÉTAPE 3 — Étudier le signe de f'(x)
─────────────────────────────────
3x² − 3 = 0  ⟺  x² = 1  ⟺  x = −1 ou x = 1

Tableau de signe :
   x       −∞    −1    1    +∞
   f'(x)        +    −    +


ÉTAPE 4 — Tableau de variations
─────────────────────────────────
f est croissante sur ]−∞ ; −1]
f est décroissante sur [−1 ; 1]
f est croissante sur [1 ; +∞[

Valeurs aux extrema :
   f(−1) = (−1)³ − 3(−1) + 2 = −1 + 3 + 2 = 4
   f(1)  = 1 − 3 + 2 = 0

CE QU'ON A FAIT
─────────────────────────────────
Aucune intuition. Aucun "talent". Juste une méthode
en 4 étapes appliquée mécaniquement.

C'est ce qu'on travaille pas à pas sur OptiTAB.
```

## [VARIANT level=Première]

```
ÉNONCÉ
─────────────────────────────────
Résoudre l'équation : x² − 5x + 6 = 0


ÉTAPE 1 — Identifier le type d'équation
─────────────────────────────────
Équation du second degré → outil : discriminant Δ.


ÉTAPE 2 — Calculer Δ
─────────────────────────────────
Δ = b² − 4ac = (−5)² − 4 × 1 × 6 = 25 − 24 = 1


ÉTAPE 3 — Conclure
─────────────────────────────────
Δ > 0, deux solutions distinctes :
   x₁ = (5 − √1)/2 = 2
   x₂ = (5 + √1)/2 = 3

S = {2 ; 3}
```

## [VARIANT level=Seconde]

```
ÉNONCÉ
─────────────────────────────────
Soit f(x) = 2x + 3.
1. Calculer f(4)
2. Pour quelle valeur de x a-t-on f(x) = 9 ?


ÉTAPE 1 — Question 1, calculer une image
─────────────────────────────────
f(4) = 2 × 4 + 3 = 11


ÉTAPE 2 — Question 2, calculer un antécédent
─────────────────────────────────
f(x) = 9
2x + 3 = 9
2x = 6
x = 3
```

## [VARIANT level=Collège]

```
ÉNONCÉ
─────────────────────────────────
Dans un triangle ABC rectangle en A,
AB = 3 cm et AC = 4 cm.
Calculer BC.


ÉTAPE 1 — Identifier l'outil
─────────────────────────────────
Triangle rectangle → théorème de Pythagore.


ÉTAPE 2 — Écrire le théorème
─────────────────────────────────
ABC est rectangle en A, donc BC² = AB² + AC².


ÉTAPE 3 — Calculer
─────────────────────────────────
BC² = 3² + 4² = 9 + 16 = 25


ÉTAPE 4 — Conclure
─────────────────────────────────
BC = √25 = 5 cm
```

## [VARIANT level=Prépa]

```
ÉNONCÉ
─────────────────────────────────
Soit la suite (uₙ) définie par u₀ = 1 et
uₙ₊₁ = (uₙ + 2) / 2

Montrer que (uₙ) est croissante et majorée par 2.


[Démonstration par récurrence complète, voir
template détaillé v2.]
```

## [VARIANT level=BTS]

```
ÉNONCÉ
─────────────────────────────────
Une entreprise vend un produit dont le bénéfice mensuel,
en milliers d'euros, est modélisé par
   B(x) = −0,5x² + 10x − 30
où x est le nombre d'unités vendues (en milliers).

Pour quelle production le bénéfice est-il maximal ?

[Application des dérivées à un contexte métier — typique BTS.]
```

## [VARIANT level=Parent]

```
Voici l'exemple type d'un exercice corrigé "à la OptiTAB",
au niveau lycée (Première).

[Reprendre l'exercice Première ci-dessus, intégralement.]

Notez la structure systématique :
  → identifier l'outil
  → appliquer mécaniquement
  → conclure clairement

C'est cette structure que votre enfant doit acquérir, plus
qu'un "niveau" intrinsèque en maths.
```

---

# PAGE 8 — MÉTHODE DE TRAVAIL + ET APRÈS (UNIVERSEL)

## Section : Méthode de travail OptiTAB

```
─────────────────────────────────────
LES 5 RÈGLES À S'APPLIQUER À TOI-MÊME
─────────────────────────────────────

1. RÉGULARITÉ > INTENSITÉ
   30 min par jour > 3 h le dimanche.
   Le cerveau apprend par répétition, pas par bourrage.

2. ACTIF > PASSIF
   Faire des exercices > relire le cours.
   Si tu passes plus de 20 % de ton temps en lecture
   passive, tu es probablement en train de procrastiner.

3. CORRIGÉ PAS À PAS > SOLUTION SEULE
   Voir la réponse ne sert à rien. Voir la DÉMARCHE qui
   mène à la réponse, c'est ce qui forme.

4. PAR ÉCRIT > DANS LA TÊTE
   Pose tout sur papier. Les yeux trompent ; le papier
   force à rendre le raisonnement explicite.

5. COMPARER, PAS RECOMMENCER
   Quand tu te trompes, NE refais PAS l'exercice depuis
   le début. Trouve la LIGNE EXACTE où ton raisonnement
   a divergé du corrigé. C'est là qu'est l'apprentissage.
```

## Section : Et après ?

```
─────────────────────────────────────
ET APRÈS CE DIAGNOSTIC ?
─────────────────────────────────────

Tu as maintenant :

  ✓ Une compréhension claire de ton blocage
  ✓ Trois priorités identifiées
  ✓ Un plan 7 jours pour démarrer
  ✓ Les erreurs à éviter à ton niveau
  ✓ Un exemple concret de la méthode OptiTAB

C'est déjà beaucoup. Si tu appliques ça sur 4 semaines
sans rien faire d'autre, tu auras déjà progressé.

Si tu veux ALLER PLUS LOIN, OptiTAB propose :

  → +150 cours courts et clairs (programme officiel)
  → +150 fiches de synthèse imprimables
  → +1000 exercices corrigés pas à pas
  → Un parcours structuré par niveau

À partir de 4,99 €/mois. Sans engagement. Annulable
en 1 clic.

Soit moins cher qu'une heure de cours particulier.

         ▶ Découvrir la plateforme
           {{platform_url}}


Tu vas recevoir d'autres emails de moi dans les
prochains jours avec :

  → La VRAIE raison qui fait bloquer la plupart des élèves
  → Un exercice complet corrigé pas à pas
  → Une présentation honnête d'OptiTAB

Ouvre-les. Ils sont courts et utiles.

À bientôt,
Anthony — fondateur d'OptiTAB
contact@optitab.net
```

---

# CHARTE DESIGN (POUR LE DESIGNER OU LE TEMPLATE HTML→PDF)

## Format

- **Taille** : A4 (210 × 297 mm)
- **Marges** : 25 mm haut/bas, 20 mm gauche/droite
- **Orientation** : Portrait
- **Pages** : 6 à 8 selon les variantes (idéalement 8 pour la version Terminale)

## Couleurs (issues du design system OptiTAB)

| Usage | Hex |
|-------|-----|
| Bleu principal (titres) | `#1e3a8a` |
| Bleu accent (kickers, badges) | `#2a38b7` |
| Bleu CTA | gradient `#2f6df4 → #2155d8` |
| Texte titre | `#0f172a` |
| Texte courant | `#1e293b` |
| Texte secondaire | `#475569` |
| Fond clair | `#f8fbff` |
| Bordure cards | `#d7e2ff` |
| Vert OptiTAB (icônes ✓) | `#378368` |

## Typographie

- **Titres H1** : 28 à 32 pt, gras 800, `#0f172a`
- **Titres H2 sections** : 18 à 22 pt, gras 800, `#1e3a8a`
- **Titres H3 sous-sections** : 14 pt, gras 700, `#2a38b7`
- **Corps** : 11 pt, regular, `#1e293b`, interligne 1.5
- **Notes / petits textes** : 9-10 pt, `#475569`
- **Famille** : Inter / SF Pro / Roboto (sans serif, lisible mobile)
- **Mono pour formules** : JetBrains Mono ou Consolas 10 pt

## Mise en page recommandée

- **Cover** : titre centré, grand espace blanc, logo en haut, infos en bas
- **Pages intérieures** : 1 H2 par page, 1 à 3 H3, paragraphes courts
- **Cards de priorité** : box avec bordure `#d7e2ff`, fond `#f8fbff`, padding 12 mm
- **Tableau d'erreurs** : numérotation 01, 02, 03 en grand `#2a38b7`
- **Exercice corrigé** : fond gris très léger `#f8fafc`, bordure gauche bleue 3 px
- **CTA final** : bouton bleu pleine largeur, gradient `#2f6df4 → #2155d8`,
  coins arrondis 14 px

## Pictogrammes (optionnels mais utiles)

- ✓ vert pour les "à faire"
- ⚠ orange/rouge pour les "à éviter"
- ★ bleu pour les priorités
- 📅 pour le plan jour par jour
- 📋 pour la cover

## Footer (chaque page sauf cover)

```
─────────────────────────────────────────────────────
Diagnostic OptiTAB · Personnalisé pour {{firstName}}     {{page}} / 8
contact@optitab.net · www.optitab.net
```

---

# NOTES DE PRODUCTION

## Version v1 (à shipper en premier)

Pour ne pas bloquer le lancement, livrer en v1 :

- **1 PDF universel** = la version TERMINALE + COURS_VS_EXERCICES
  (~6 pages, peut être prête en 2-3 h de design)

Le E1 envoie ce PDF à tous les leads, peu importe leur niveau.
Tant que la promesse de la landing est tenue, c'est OK.

## Version v2 (4 semaines plus tard)

- 7 PDFs par niveau (Collège, Seconde, Première, Terminale, Prépa, BTS, Parent)
- Personnalisation `firstName` injectée à la volée (Puppeteer / wkhtmltopdf)

## Version v3 (3 mois plus tard)

- 7 niveaux × 5 difficultés = 35 PDFs ou
- 1 template HTML rendu à la volée avec substitution conditionnelle
  (recommandé : maintenance plus facile)

## Technique de rendu suggérée

- **Manuel** : maquettage Figma → export PDF (rapide pour v1)
- **Automatique** : template HTML + Puppeteer (recommandé pour v2/v3)
  ```
  npm i puppeteer
  // Template HTML avec {{handlebars}}, rendu via puppeteer.pdf()
  ```
- **Brevo intégré** : la pièce jointe peut être hébergée sur S3/CDN et
  liée dans l'email E1 via `{{params.diagnostic_url}}`
