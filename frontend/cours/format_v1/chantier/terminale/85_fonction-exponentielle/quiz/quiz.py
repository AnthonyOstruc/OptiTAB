# -*- coding: utf-8 -*-
"""Quiz pilote du site : Terminale, notion 85 « Fonction exponentielle ».

Format : format_v1/QUIZ.md. Figures : figures/figures.py. Vérifications : verif_quiz.py.
Construction : python outils/construire_quiz.py <dossier_notion>

Le logarithme népérien n'est pas encore vu dans ce chapitre (cours_89, fiche_30) :
aucune réponse n'utilise ln ; les valeurs exactes s'écrivent avec e.
"""

QUIZ = {
    "notion": 85,
    "titre": "Fonction exponentielle",
    "intro": "16 questions pour vérifier que tu maîtrises la fonction exponentielle, des règles de calcul à l'étude de fonction.",
    "duree": 16,
    # parties du cours (ordre du cours) : bilan « Acquis / En cours / À revoir » en fin de quiz
    "parties": [
        "Rappels de Première",
        "Limites",
        r"Fonctions de la forme $e^{u}$",
        "Étude complète d'une fonction",
        "Un modèle exponentiel",
    ],
    "questions": [

        # ------------------------------------------------------------ Découverte
        {
            "id": "q01",
            "type": "vf",
            "niveau": "Découverte",
            "theme": "Signe de l'exponentielle",
            "partie": "Rappels de Première",
            "enonce": r"L'équation $e^{x} = -2$ admet au moins une solution réelle.",
            "reponse": False,
            "explication": r"""Une exponentielle est **toujours strictement positive**.

Pour tout réel $x$, $e^{x} \gt 0$ : $e^{x}$ ne peut jamais valoir $-2$. La courbe de $\exp$ et la droite d'équation $y = -2$ n'ont aucun point commun.

::: resultat
Faux : l'équation $e^{x} = -2$ n'a **aucune** solution.
:::""",
            "figure_corrige": "q01_corrige",
        },
        {
            "id": "q02",
            "type": "qcm",
            "niveau": "Découverte",
            "theme": "Lecture graphique",
            "partie": "Rappels de Première",
            "enonce": r"Laquelle de ces courbes représente la fonction exponentielle $x \mapsto e^{x}$ ?",
            "choix_figures": ["q02_a", "q02_b", "q02_c", "q02_d"],
            "bonne": 2,
            "explication": r"""On contrôle trois propriétés de la courbe de $\exp$ :
- elle passe par le point $(0\,;1)$, car $e^{0} = 1$ ;
- elle reste au-dessus de l'axe des abscisses, car $e^{x} \gt 0$ ;
- elle monte : $\exp$ est strictement croissante.

::: resultat
C'est la courbe croissante, toujours au-dessus de l'axe des abscisses, qui passe par $(0\,;1)$ (et par $(1\,;e)$, avec $e \approx 2{,}72$).
:::

Les autres courbes : $e^{-x}$ (décroissante), $e^{x} - 1$ (passe par l'origine), $e^{x} + 1$ (passe par $(0\,;2)$).""",
            "figure_corrige": "q02_corrige",
        },
        {
            "id": "q03",
            "type": "saisie",
            "niveau": "Découverte",
            "theme": "Règles de calcul",
            "partie": "Rappels de Première",
            "enonce": r"Pour tout réel $x$, écrire $\left(e^{x}\right)^{3} \times e^{-x}$ sous la forme d'une seule exponentielle.",
            "nature": "expression",
            "reponses": ["exp(2*x)"],
            "placeholder": "par exemple e^(5x)",
            "acceptees": ["e^(2x)", "exp(2x)", "e^(2*x)", "e^(3x-x)", "(e^x)^2", "e^x*e^x", "e^(2 x)"],
            "refusees": ["e^2x", "e^(3x)", "e^(4x)", "e^(x^3-x)", "e^(-3x^2)"],
            "explication": r"""On applique $\left(e^{a}\right)^{n} = e^{na}$, puis $e^{a} \times e^{b} = e^{a+b}$.

$$\left(e^{x}\right)^{3} \times e^{-x} = e^{3x} \times e^{-x} = e^{3x - x}$$

::: resultat
$\left(e^{x}\right)^{3} \times e^{-x} = e^{2x}$
:::

::: attention Erreur fréquente
$\left(e^{x}\right)^{3} = e^{3x}$, et non $e^{x^{3}}$. Au clavier, mettre l'exposant entre parenthèses : `e^(2x)`, car `e^2x` se lit $e^{2} \times x$.
:::""",
        },
        {
            "id": "q04",
            "type": "qcm",
            "niveau": "Découverte",
            "theme": "Tangente en 0",
            "partie": "Rappels de Première",
            "enonce": r"La droite $T$ est tangente à la courbe de $x \mapsto e^{x}$ au point d'abscisse $0$. Quelle est son équation ?",
            "figure": "q04_enonce",
            "choix": [r"$y = x + 1$", r"$y = x$", r"$y = e\,x$", r"$y = x - 1$"],
            "bonne": 0,
            "explication": r"""Tangente en $a$ : $y = f'(a)(x - a) + f(a)$. Ici $f = \exp$ et $a = 0$.

- $f(0) = e^{0} = 1$ ;
- $f'(0) = e^{0} = 1$, car $\exp' = \exp$.

::: resultat
$T : y = 1 \times (x - 0) + 1$, soit $y = x + 1$.
:::

La courbe est au-dessus de sa tangente : pour tout réel $x$, $e^{x} \ge x + 1$.""",
            "figure_corrige": "q04_corrige",
        },

        # ------------------------------------------------------------ Entraînement
        {
            "id": "q05",
            "type": "multi",
            "niveau": "Entraînement",
            "theme": "Règles de calcul",
            "partie": "Rappels de Première",
            "enonce": r"Cocher les égalités vraies pour **tout** réel $x$.",
            "choix": [
                r"$e^{2x} = \left(e^{x}\right)^{2}$",
                r"$e^{-x} = \dfrac{1}{e^{x}}$",
                r"$e^{x+1} = e^{x} + e$",
                r"$e^{x^{2}} = \left(e^{x}\right)^{2}$",
                r"$\dfrac{e^{3x}}{e^{x}} = e^{2x}$",
                r"$e^{x} \times e^{2} = e^{2x}$",
            ],
            "bonnes": [0, 1, 4],
            "explication": r"""On applique les règles : $e^{a+b} = e^{a} \times e^{b}$, $e^{-a} = \dfrac{1}{e^{a}}$, $e^{a-b} = \dfrac{e^{a}}{e^{b}}$ et $\left(e^{a}\right)^{n} = e^{na}$.

- Vrai : $\left(e^{x}\right)^{2} = e^{2x}$.
- Vrai : $e^{-x} = \dfrac{1}{e^{x}}$.
- Vrai : $\dfrac{e^{3x}}{e^{x}} = e^{3x - x} = e^{2x}$.
- Faux : $e^{x+1} = e^{x} \times e$ (un produit, pas une somme).
- Faux : $\left(e^{x}\right)^{2} = e^{2x}$, et non $e^{x^{2}}$.
- Faux : $e^{x} \times e^{2} = e^{x+2}$ : on **ajoute** les exposants.

::: resultat
Trois égalités vraies : $e^{2x} = \left(e^{x}\right)^{2}$, $e^{-x} = \dfrac{1}{e^{x}}$ et $\dfrac{e^{3x}}{e^{x}} = e^{2x}$.
:::""",
        },
        {
            "id": "q06",
            "type": "vf",
            "niveau": "Entraînement",
            "theme": "Sens de variation",
            "partie": "Rappels de Première",
            "enonce": r"La fonction $f : x \mapsto e^{-2x+1}$ est croissante sur $\mathbb{R}$, car la fonction exponentielle est croissante.",
            "reponse": False,
            "explication": r"""$e^{u}$ a les **mêmes variations que $u$**. Ici $u(x) = -2x + 1$ est décroissante.

Par le calcul : $f'(x) = -2\,e^{-2x+1}$, et $e^{-2x+1} \gt 0$, donc $f'(x) \lt 0$.

::: resultat
Faux : $f$ est strictement **décroissante** sur $\mathbb{R}$.
:::""",
            "figure_corrige": "q06_corrige",
        },
        {
            "id": "q07",
            "type": "qcm",
            "niveau": "Entraînement",
            "theme": "Dérivée de exp(u)",
            "partie": r"Fonctions de la forme $e^{u}$",
            "enonce": r"Soit $f(x) = e^{-3x+1}$. Pour tout réel $x$, $f'(x)$ est égal à :",
            "choix": [r"$-3\,e^{-3x+1}$", r"$e^{-3x+1}$", r"$(-3x+1)\,e^{-3x}$", r"$3\,e^{-3x+1}$"],
            "bonne": 0,
            "explication": r"""On utilise $\left(e^{u}\right)' = u'\,e^{u}$ avec $u(x) = -3x + 1$, donc $u'(x) = -3$.

::: resultat
$f'(x) = -3\,e^{-3x+1}$
:::

::: attention Erreur fréquente
Oublier le facteur $u'$ : la dérivée de $e^{-3x+1}$ n'est pas $e^{-3x+1}$.
:::""",
        },
        {
            "id": "q08",
            "type": "saisie",
            "niveau": "Entraînement",
            "theme": "Dérivée d'un produit",
            "partie": "Étude complète d'une fonction",
            "enonce": r"Soit $f(x) = (x - 1)\,e^{x}$. Écrire $f'(x)$ sous la forme la plus simple.",
            "nature": "expression",
            "reponses": ["x*exp(x)"],
            "placeholder": "par exemple (2x+1)e^x",
            "acceptees": ["xe^x", "x*e^x", "x e^x", "x×exp(x)", "e^x*x", "e^x+(x-1)e^x", "(x-1+1)e^x", "x*e^(x)"],
            "refusees": ["e^x", "(x-1)e^x", "(x+1)e^x", "(x-2)e^x", "xe^(x-1)"],
            "explication": r"""Dérivée d'un produit : $(uv)' = u'v + uv'$ avec $u(x) = x - 1$ et $v(x) = e^{x}$, donc $u'(x) = 1$ et $v'(x) = e^{x}$.

$$
\begin{aligned}
f'(x) &= 1 \times e^{x} + (x - 1)\,e^{x} \\
&= (1 + x - 1)\,e^{x} \\
&= x\,e^{x}
\end{aligned}
$$

::: resultat
$f'(x) = x\,e^{x}$
:::

::: attention Erreur fréquente
$(uv)' \ne u'v'$ : en dérivant chaque facteur séparément, on trouverait $e^{x}$, ce qui est faux.
:::""",
        },
        {
            "id": "q09",
            "type": "saisie",
            "niveau": "Entraînement",
            "theme": "Équations",
            "partie": "Rappels de Première",
            "enonce": r"Résoudre dans $\mathbb{R}$ l'équation $e^{2x-1} = e^{x+3}$. Donner la solution.",
            "nature": "nombre",
            "reponses": ["4"],
            "placeholder": "par exemple 2,5",
            "acceptees": ["4", "4,0", "4.0", "8/2"],
            "refusees": ["2", "-4", "4/3", "e^4"],
            "explication": r"""Pour tous réels $a$ et $b$ : $e^{a} = e^{b} \iff a = b$. On compare les exposants.

$$
\begin{aligned}
e^{2x-1} = e^{x+3} &\iff 2x - 1 = x + 3 \\
&\iff x = 4
\end{aligned}
$$

::: resultat
$S = \{4\}$
:::""",
        },
        {
            "id": "q10",
            "type": "ordre",
            "niveau": "Entraînement",
            "theme": "Inéquations",
            "partie": "Rappels de Première",
            "enonce": r"Remettre dans l'ordre les étapes de la résolution de $e^{3x-2} \lt e^{x+4}$.",
            "etapes": [
                r"$\exp$ est strictement croissante : on compare les exposants.",
                r"$3x - 2 \lt x + 4$",
                r"$2x \lt 6$",
                r"$x \lt 3$",
                r"$S = \left]-\infty\,;3\right[$",
            ],
            "explication": r"""Comme $\exp$ est strictement croissante, $e^{a} \lt e^{b} \iff a \lt b$ : le sens de l'inégalité est **conservé**.

$$
\begin{aligned}
e^{3x-2} \lt e^{x+4} &\iff 3x - 2 \lt x + 4 \\
&\iff 2x \lt 6 \\
&\iff x \lt 3
\end{aligned}
$$

::: resultat
$S = \left]-\infty\,;3\right[$
:::""",
            "figure_corrige": "q10_corrige",
        },

        # ------------------------------------------------------------ Approfondissement
        {
            "id": "q11",
            "type": "multi",
            "niveau": "Approfondissement",
            "theme": "Limites",
            "partie": "Limites",
            "enonce": r"Cocher les limites exactes.",
            "choix": [
                r"$\lim\limits_{x \to -\infty} e^{x} = 0$",
                r"$\lim\limits_{x \to +\infty} x\,e^{-x} = +\infty$",
                r"$\lim\limits_{x \to +\infty} \dfrac{e^{x}}{x^{3}} = +\infty$",
                r"$\lim\limits_{x \to 0} \dfrac{e^{x} - 1}{x} = 0$",
                r"$\lim\limits_{x \to -\infty} x^{2}\,e^{x} = 0$",
            ],
            "bonnes": [0, 2, 4],
            "explication": r"""- Vrai : $\lim\limits_{x \to -\infty} e^{x} = 0$ (asymptote $y = 0$).
- Faux : $x\,e^{-x} = \dfrac{x}{e^{x}} \to 0$ en $+\infty$ (croissances comparées).
- Vrai : en $+\infty$, l'exponentielle l'emporte sur $x^{3}$.
- Faux : $\dfrac{e^{x} - 1}{x}$ est le taux d'accroissement de $\exp$ en $0$ ; il tend vers $\exp'(0) = 1$.
- Vrai : $\lim\limits_{x \to -\infty} x^{n}\,e^{x} = 0$, ici avec $n = 2$.

::: resultat
Les limites exactes : $\lim\limits_{x \to -\infty} e^{x} = 0$, $\lim\limits_{x \to +\infty} \dfrac{e^{x}}{x^{3}} = +\infty$ et $\lim\limits_{x \to -\infty} x^{2}\,e^{x} = 0$.
:::

::: attention Erreur fréquente
« $0 \times \infty$ » et « $\frac{\infty}{\infty}$ » sont des formes indéterminées : on conclut avec les croissances comparées.
:::""",
        },
        {
            "id": "q11b",
            "type": "qcm",
            "niveau": "Approfondissement",
            "theme": "Limites",
            "partie": "Limites",
            "enonce": r"Que vaut $\lim\limits_{x \to +\infty} \left(e^{2x} - 3e^{x}\right)$ ?",
            "choix": [r"$+\infty$", r"$-\infty$", r"$0$", r"On ne peut pas conclure : c'est une forme indéterminée."],
            "bonne": 0,
            "explication": r"""On a une forme « $\infty - \infty$ » : on **factorise par le terme le plus fort**, $e^{x}$.

$$e^{2x} - 3e^{x} = e^{x}\left(e^{x} - 3\right)$$

Quand $x \to +\infty$ : $e^{x} \to +\infty$ et $e^{x} - 3 \to +\infty$, donc le produit tend vers $+\infty$.

::: resultat
$\lim\limits_{x \to +\infty} \left(e^{2x} - 3e^{x}\right) = +\infty$
:::

::: attention Erreur fréquente
S'arrêter à « $\infty - \infty$, on ne peut pas conclure » : une forme indéterminée se **lève**, ici en factorisant.
:::""",
        },
        {
            "id": "q12",
            "type": "associer",
            "niveau": "Approfondissement",
            "theme": "Variations et courbes",
            "partie": r"Fonctions de la forme $e^{u}$",
            "enonce": r"Associer chaque fonction à sa courbe.",
            "gauche": [r"$x \mapsto e^{-x}$", r"$x \mapsto e^{-x^{2}}$", r"$x \mapsto e^{x^{2}}$", r"$x \mapsto x\,e^{x}$"],
            "droite_figures": ["q12_a", "q12_b", "q12_c", "q12_d"],
            "explication": r"""$e^{u}$ a les **mêmes variations que $u$**, et $e^{u} \gt 0$.

- $e^{-x}$ : $u(x) = -x$ est décroissante, donc la courbe descend ; elle passe par $(0\,;1)$.
- $e^{-x^{2}}$ : $-x^{2}$ croît puis décroît, donc courbe « en cloche », maximum $1$ en $0$.
- $e^{x^{2}}$ : $x^{2}$ décroît puis croît, donc minimum $1$ en $0$.
- $x\,e^{x}$ : elle est nulle en $0$ et négative pour $x \lt 0$ ; c'est la seule qui passe sous l'axe des abscisses.

::: resultat
Pour reconnaître une courbe : sens de variation (signe de $u'$), valeur en $0$, signe de la fonction.
:::""",
        },
        {
            "id": "q13",
            "type": "qcm",
            "niveau": "Approfondissement",
            "theme": "Suites géométriques",
            "partie": "Rappels de Première",
            "enonce": r"Soit la suite définie pour tout entier naturel $n$ par $u_n = e^{-0{,}5n}$. Cette suite est :",
            "choix": [
                r"géométrique de raison $e^{-0{,}5}$",
                r"arithmétique de raison $-0{,}5$",
                r"géométrique de raison $-0{,}5$",
                r"arithmétique de raison $e^{-0{,}5}$",
            ],
            "bonne": 0,
            "explication": r"""On exprime $u_{n+1}$ en fonction de $u_n$ avec $e^{a+b} = e^{a} \times e^{b}$ :

$$u_{n+1} = e^{-0{,}5(n+1)} = e^{-0{,}5n} \times e^{-0{,}5} = e^{-0{,}5} \times u_n$$

::: resultat
$(u_n)$ est géométrique de raison $q = e^{-0{,}5} \approx 0{,}61$ et de premier terme $u_0 = 1$.
:::

Comme $0 \lt q \lt 1$ et $u_0 \gt 0$, la suite est décroissante et tend vers $0$.""",
            "figure_corrige": "q13_corrige",
        },
        {
            "id": "q14",
            "type": "saisie",
            "niveau": "Approfondissement",
            "theme": "Étude de fonction",
            "partie": "Étude complète d'une fonction",
            "enonce": r"On étudie $f(x) = x\,e^{-x}$ sur $\mathbb{R}$. Donner la **valeur exacte** du maximum de $f$.",
            "figure": "q14_enonce",
            "nature": "nombre",
            "reponses": ["1/e"],
            "placeholder": "valeur exacte",
            "acceptees": ["1/e", "e^(-1)", "e^-1", "exp(-1)", "1/exp(1)", "1×e^(-1)"],
            "refusees": ["0,37", "1", "e", "-1/e", "e^(-2)"],
            "explication": r"""On dérive, on étudie le signe de $f'$, puis on calcule la valeur du maximum.

$$f'(x) = 1 \times e^{-x} + x \times \left(-e^{-x}\right) = (1 - x)\,e^{-x}$$

Comme $e^{-x} \gt 0$, $f'(x)$ a le signe de $1 - x$ : positif avant $1$, négatif après.

::: tableau
x : -\infty, 1, +\infty
f'(x) : , +, z, -,
f(x) : -/-\infty, +/\frac{1}{e}, -/0
:::

::: resultat
Le maximum de $f$ vaut $f(1) = 1 \times e^{-1} = \dfrac{1}{e}$.
:::

::: attention Erreur fréquente
Ne pas confondre l'abscisse du maximum ($x = 1$) et sa valeur ($\frac{1}{e}$). La valeur $0{,}37$ n'est qu'une valeur approchée.
:::""",
            "figure_corrige": "q14_corrige",
        },
        {
            "id": "q15",
            "type": "saisie",
            "niveau": "Approfondissement",
            "theme": "Modèle exponentiel",
            "partie": "Un modèle exponentiel",
            "enonce": r"La tension aux bornes d'un condensateur qui se charge vaut $u(t) = 5\left(1 - e^{-0{,}5t}\right)$ ($t$ en secondes, $u$ en volts). Calculer $u(4)$, arrondi au centième.",
            "figure": "q15_enonce",
            "nature": "nombre",
            "reponses": ["5*(1-exp(-2))"],
            "tolerance": 0.005,
            "unite": "V",
            "placeholder": "par exemple 1,23",
            "acceptees": ["4,32", "4.32", "4,323", "5(1-e^-2)", "5-5e^(-2)"],
            "refusees": ["4,3", "4,33", "0,68", "-31,95"],
            "explication": r"""On remplace $t$ par $4$ : $-0{,}5 \times 4 = -2$.

$$u(4) = 5\left(1 - e^{-2}\right) \approx 5 \times (1 - 0{,}1353) \approx 4{,}32$$

::: resultat
$u(4) \approx 4{,}32$ V
:::

La tension se rapproche de $5$ V sans jamais l'atteindre, car $e^{-0{,}5t} \gt 0$.

::: attention Erreur fréquente
Le signe de l'exposant : $-0{,}5 \times 4 = -2$, donc $e^{-2} \approx 0{,}14$ (et non $e^{2}$).
:::""",
            "figure_corrige": "q15_corrige",
        },
    ],
}
