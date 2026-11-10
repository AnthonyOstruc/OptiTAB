// Exemples de corrections qui défilent en haut de l'accueil (un toutes les 2 s).
// La carte n'affiche que l'énoncé, la méthode, l'étape clé (celle qui a un
// schéma, sinon la dernière) et le résultat ; les autres étapes restent ici
// pour le texte lu par les lecteurs d'écran (champ « alt »).
//
// Chaque exemple suit la présentation de la plateforme : énoncé, méthode, étapes,
// résultat. Les formules sont écrites en LaTeX et PRÉ-RENDUES par KaTeX :
// après toute modification, relancer `node scripts/vitrine-math.mjs` (depuis frontend/).
//
// Écriture d'une ligne : une liste de morceaux.
//   'texte'      texte simple
//   m`…`         formule
//   a`…`, b`…`   formule surlignée en bleu (a) ou en vert (b) : la même couleur
//                relie la formule de la méthode aux termes du calcul
//   nowrap(…)    morceaux qui ne doivent pas être coupés en fin de ligne
// Virgule décimale : écrire 0{,}5 (sinon KaTeX ajoute une espace après la virgule).

const m = (s, ...v) => ({ tex: String.raw(s, ...v) })
const a = (s, ...v) => ({ tex: String.raw(s, ...v), pill: 'a' })
const b = (s, ...v) => ({ tex: String.raw(s, ...v), pill: 'b' })
const nowrap = (...groupe) => ({ groupe })

export const vitrineExemples = [
  {
    id: 'exponentielle',
    niveau: 'Terminale · Exponentielle',
    type: 'Type bac',
    fiche: 'Exponentielle : l’essentiel',
    progression: 72,
    xp: 20,
    alt: 'Exercice de Terminale : étudier les variations de f(x) = (x − 1)eˣ. Méthode : dérivée d’un produit, (uv)′ = u′v + uv′. On trouve f′(x) = x eˣ, du signe de x. La fonction est décroissante puis croissante, de minimum f(0) = −1.',
    enonce: ['Étudier les variations de ', nowrap(m`f(x) = (x - 1)\,e^{x}`, ' sur ', m`\mathbb{R}`, '.')],
    methode: { titre: 'Dérivée d’un produit', formule: [nowrap(m`(uv)' =`, ' ', a`u'v`, ' + ', b`uv'`)] },
    etapes: [
      {
        titre: 'Dériver',
        lignes: [
          [nowrap(m`u = x - 1`, ', ', m`u' = 1`), ' ', nowrap(m`v = e^{x}`, ', ', m`v' = e^{x}`)],
          [nowrap(m`f'(x) =`, ' ', a`1 \times e^{x}`, ' + ', b`(x - 1)\,e^{x}`, ' ', m`= x\,e^{x}`)]
        ]
      },
      {
        titre: 'Signe de la dérivée',
        lignes: [[m`e^{x} > 0`, ', donc ', m`f'(x)`, ' a le signe de ', m`x`, '.']]
      },
      {
        titre: 'Tableau de variations',
        visuel: {
          type: 'variations',
          libelles: [m`x`, m`f'(x)`, m`f(x)`],
          x: [m`-\infty`, m`0`, m`+\infty`],
          signes: [m`-`, m`0`, m`+`],
          haut: [m`0`, m`+\infty`],
          bas: m`-1`
        }
      }
    ],
    resultat: ['Minimum ', nowrap(m`f(0) = -1`, ','), ' atteint en ', nowrap(m`x = 0`, '.')]
  },

  {
    id: 'pythagore',
    niveau: '4e · Théorème de Pythagore',
    type: 'Type brevet',
    fiche: 'Pythagore : l’essentiel',
    progression: 85,
    xp: 35,
    alt: 'Exercice de 4e : ABC est rectangle en A, avec AB = 6 cm et AC = 8 cm ; calculer BC. Méthode : théorème de Pythagore, BC² = AB² + AC². BC² = 36 + 64 = 100, donc BC = 10 cm.',
    enonce: [m`ABC`, ' est rectangle en ', m`A`, ', avec ', nowrap(m`AB = 6`, ' cm'), ' et ', nowrap(m`AC = 8`, ' cm'), '. Calculer ', m`BC`, '.'],
    methode: { titre: 'Théorème de Pythagore', formule: [b`BC^2 = AB^2 + AC^2`] },
    etapes: [
      {
        titre: 'Repérer l’hypoténuse',
        lignes: [['C’est le côté opposé à l’angle droit : ', m`[BC]`, '.']],
        visuel: {
          type: 'figure',
          vue: [220, 120],
          largeur: 215,
          traces: [
            { d: 'M70 22 V100 H174', style: 'trait' },
            { d: 'M70 89 H81 V100', style: 'angle' },
            { d: 'M70 22 L174 100', style: 'vert' }
          ],
          etiquettes: [
            { x: 61, y: 108, ...m`A` },
            { x: 61, y: 16, ...m`B` },
            { x: 184, y: 108, ...m`C` },
            { x: 58, y: 61, ancre: 'd', ...m`6\,\text{cm}` },
            { x: 122, y: 112, ...m`8\,\text{cm}` },
            { x: 131, y: 50, ancre: 'g', ton: 'vert', texte: 'hypoténuse' }
          ]
        }
      },
      {
        titre: 'Appliquer le théorème',
        lignes: [[nowrap(b`BC^2 = 6^2 + 8^2`, ' ', m`= 36 + 64 = 100`)]]
      },
      {
        titre: 'Conclure',
        lignes: [[nowrap(m`BC = \sqrt{100} = 10`), ' car ', nowrap(m`BC > 0`, '.')]]
      }
    ],
    resultat: [m`BC = 10`, ' cm.']
  },

  {
    id: 'second-degre',
    niveau: 'Première · Second degré',
    type: 'Entraînement',
    fiche: 'Second degré : l’essentiel',
    progression: 64,
    xp: 15,
    alt: 'Exercice de Première : résoudre 2x² − 3x − 2 = 0. Méthode : discriminant Δ = b² − 4ac, puis x = (−b ± √Δ) / 2a. Δ = 25, d’où deux solutions : −1/2 et 2, lues aussi sur la parabole.',
    enonce: ['Résoudre ', nowrap(m`2x^2 - 3x - 2 = 0`, '.')],
    methode: {
      titre: 'Discriminant',
      formule: [nowrap(a`\Delta = b^2 - 4ac`), ' puis ', nowrap(b`x = \dfrac{-b \pm \sqrt{\Delta}}{2a}`)]
    },
    etapes: [
      {
        titre: 'Calculer Δ',
        lignes: [
          [nowrap(m`a = 2`, ', ', m`b = -3`, ', ', m`c = -2`)],
          [nowrap(a`\Delta = (-3)^2 - 4 \times 2 \times (-2)`, ' ', m`= 25`)]
        ]
      },
      {
        titre: 'Δ > 0 : deux solutions',
        lignes: [[nowrap(b`x_1 = \dfrac{3 - 5}{4} = -\dfrac{1}{2}`), ' ', nowrap(b`x_2 = \dfrac{3 + 5}{4} = 2`)]]
      },
      {
        titre: 'Lire les solutions sur la courbe',
        visuel: {
          type: 'figure',
          vue: [300, 95],
          largeur: 360,
          // Parabole y = 2x² − 3x − 2 : un arc de Bézier quadratique la représente exactement.
          traces: [
            { d: 'M12 54.6 H290', style: 'axe', fleche: true },
            { d: 'M102.7 93 V4', style: 'axe', fleche: true },
            { d: 'M31.8 5.3 Q147 172.6 262.3 5.3', style: 'courbe' }
          ],
          points: [
            { c: [73.2, 54.6], ton: 'vert' },
            { c: [220.9, 54.6], ton: 'vert' }
          ],
          etiquettes: [
            { x: 286, y: 47, ...m`x` },
            { x: 111, y: 8, ...m`y` },
            { x: 66, y: 68, ancre: 'd', ton: 'vert', ...m`-\dfrac{1}{2}` },
            { x: 228, y: 67, ancre: 'g', ton: 'vert', ...m`2` }
          ]
        }
      }
    ],
    resultat: ['Deux solutions : ', m`S = \left\{ -\tfrac{1}{2}\ ;\ 2 \right\}`, '.']
  },

  {
    id: 'fractions',
    niveau: '5e · Fractions',
    type: 'Découverte',
    fiche: 'Fractions : l’essentiel',
    progression: 90,
    xp: 40,
    alt: 'Exercice de 5e : calculer 2/3 + 5/6. Méthode : mettre au même dénominateur puis additionner les numérateurs. 2/3 = 4/6, 4/6 + 5/6 = 9/6 = 3/2.',
    enonce: ['Calculer ', nowrap(m`\dfrac{2}{3} + \dfrac{5}{6}`), ' et simplifier le résultat.'],
    methode: { titre: 'Même dénominateur', formule: [nowrap(m`\dfrac{a}{c} + \dfrac{b}{c} = \dfrac{a + b}{c}`)] },
    etapes: [
      {
        titre: 'Écrire avec le même dénominateur',
        lignes: [[nowrap(m`\dfrac{2}{3} = \dfrac{2 \times 2}{3 \times 2} =`, ' ', a`\dfrac{4}{6}`)]]
      },
      {
        titre: 'Additionner les numérateurs',
        lignes: [[nowrap(a`\dfrac{4}{6}`, ' + ', b`\dfrac{5}{6}`, ' ', m`= \dfrac{9}{6}`)]],
        visuel: {
          type: 'figure',
          vue: [300, 80],
          largeur: 390,
          traces: [
            // 12 sixièmes : 4 bleus, 5 verts, 3 vides ; trait épais à chaque unité.
            { d: 'M15 30 h90 v18 h-90 Z', style: 'case-a' },
            { d: 'M105 30 h112.5 v18 h-112.5 Z', style: 'case-b' },
            { d: 'M217.5 30 h67.5 v18 h-67.5 Z', style: 'case' },
            { d: 'M37.5 30 v18 M60 30 v18 M82.5 30 v18 M105 30 v18 M127.5 30 v18 M172.5 30 v18 M195 30 v18 M217.5 30 v18 M240 30 v18 M262.5 30 v18', style: 'fin' },
            { d: 'M15 26 v26 M150 26 v26 M285 26 v26', style: 'unite' }
          ],
          etiquettes: [
            { x: 60, y: 14, ton: 'navy', ...m`\dfrac{4}{6}` },
            { x: 161.25, y: 14, ton: 'vert', ...m`\dfrac{5}{6}` },
            { x: 15, y: 63, ...m`0` },
            { x: 150, y: 63, ...m`1` },
            { x: 217.5, y: 66, ton: 'vert', ...m`\dfrac{9}{6}` },
            { x: 285, y: 63, ...m`2` }
          ]
        }
      },
      {
        titre: 'Simplifier',
        lignes: [[nowrap(m`\dfrac{9}{6} = \dfrac{3 \times 3}{2 \times 3} = \dfrac{3}{2}`)]]
      }
    ],
    resultat: [nowrap(m`\dfrac{2}{3} + \dfrac{5}{6} = \dfrac{3}{2}`), '.']
  },

  {
    id: 'probabilites',
    niveau: 'Terminale · Probabilités',
    type: 'Problème',
    fiche: 'Probabilités : l’essentiel',
    progression: 78,
    xp: 25,
    alt: 'Exercice de Terminale : 2 % de la population est malade ; le test est positif pour 95 % des malades et 10 % des personnes saines ; calculer P(T). Méthode : probabilités totales sur l’arbre pondéré. P(T) = 0,02 × 0,95 + 0,98 × 0,1 = 0,117.',
    enonce: [
      nowrap('2', ' %'), ' de la population est malade. Le test est positif pour ',
      nowrap('95', ' %'), ' des malades et ', nowrap('10', ' %'), ' des personnes saines. Calculer ', m`P(T)`, '.'
    ],
    methode: {
      titre: 'Probabilités totales',
      formule: [nowrap(m`P(T) =`, ' ', a`P(M \cap T)`, ' + ', b`P(\overline{M} \cap T)`)]
    },
    etapes: [
      {
        titre: 'Construire l’arbre pondéré',
        visuel: {
          type: 'figure',
          vue: [250, 112],
          largeur: 270,
          traces: [
            { d: 'M16 56 L100 26 M124 26 L204 12', style: 'chemin-a' },
            { d: 'M16 56 L100 86 M124 86 L204 72', style: 'chemin-b' },
            { d: 'M124 26 L204 40 M124 86 L204 100', style: 'branche' }
          ],
          points: [{ c: [16, 56], ton: 'navy' }],
          etiquettes: [
            { x: 112, y: 26, ton: 'navy', ...m`M` },
            { x: 112, y: 86, ton: 'vert', ...m`\overline{M}` },
            { x: 212, y: 12, ancre: 'g', ton: 'navy', ...m`T` },
            { x: 212, y: 40, ancre: 'g', ton: 'muted', ...m`\overline{T}` },
            { x: 212, y: 72, ancre: 'g', ton: 'vert', ...m`T` },
            { x: 212, y: 100, ancre: 'g', ton: 'muted', ...m`\overline{T}` },
            { x: 50, y: 32, ...m`0{,}02` },
            { x: 50, y: 82, ...m`0{,}98` },
            { x: 160, y: 10, ...m`0{,}95` },
            { x: 160, y: 43, ton: 'muted', ...m`0{,}05` },
            { x: 160, y: 70, ...m`0{,}1` },
            { x: 160, y: 103, ton: 'muted', ...m`0{,}9` }
          ]
        }
      },
      {
        titre: 'Additionner les deux chemins',
        lignes: [
          [nowrap(m`P(T) =`, ' ', a`0{,}02 \times 0{,}95`, ' + ', b`0{,}98 \times 0{,}1`)],
          [nowrap(m`P(T) = 0{,}019 + 0{,}098`)]
        ]
      }
    ],
    resultat: [m`P(T) = 0{,}117`, ' : ', nowrap('11,7', ' %'), ' des tests sont positifs.']
  }
]
