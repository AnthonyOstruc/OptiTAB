# -*- coding: utf-8 -*-
"""Corrections de fond du chapitre pilote (relecture du 2026-10-27).

À rejouer après chaque conversion automatique :
    python corrections.py

Chaque correction vise un passage exact ; le script s'arrête si un passage
est introuvable (la conversion a changé : la correction doit être revue).
Erreurs relevées dans le contenu en ligne : signe faux de f', tableaux de
variations incomplets, ensemble solution faux (tan x ≤ 1), notations hors
programme (cot, sec, équivalents, changement de variable, formules de
transformation somme-produit), rédaction imprécise (« décroît vers −∞ »).
"""
from pathlib import Path

ICI = Path(__file__).resolve().parent

# Le cours et la fiche ont été réécrits en production le 2026-10-27 (session
# « lycée v2 ») : leurs anciennes corrections sont sans objet. Le nouveau
# contenu, relu, ne demande pas de correction de fond.
# Le tableau de variations (image matplotlib) devient un tableau tkz-tab natif.
COURS = [
    (r"""[IMAGE_3]""", r"""::: tableau Variations de $\cos$ sur $[-\pi\,;\pi]$
x : -\pi, 0, \pi
-\sin(x) : , +, z, -,
\cos(x) : -/-1, +/1, -/-1
:::"""),
]

FICHE = [
    (r"""[IMAGE_2]""", r"""::: tableau Variations de $\cos$ sur $[-\pi\,;\pi]$
x : -\pi, 0, \pi
-\sin(x) : , +, z, -,
\cos(x) : -/-1, +/1, -/-1
:::"""),
]

EXERCICES = [
    # Ex. 4 Q3 : remarque en double, limite en 2π
    (r"""- **Remarque :** On peut montrer que $h(x) = \frac{\sin(x)}{1 + \cos(x)} = \tan\left(\frac{x}{2}\right)$

Donc :""",
     r"""Avec $h(x) = \tan\left(\frac{x}{2}\right)$ (remarque précédente) :"""),
    (r"""h(x) : -/0, +D-/+\infty/-\infty, +/\to 0""", r"""h(x) : -/0, +D-/+\infty/-\infty, +/0"""),
    # Ex. 4 Q5 : tan n'est pas définie en π/2
    (r"""m'(x) : z, +,
m(x) : -/0, +/+\infty""",
     r"""m'(x) : z, +, d
m(x) : -/0, +D/+\infty"""),
    # Ex. 5 Q1 : méthode du programme (égalité de deux sinus)
    (r"""::: methode
Utilisation des formules trigonométriques
:::

::: etape Formule de différence
$$\sin(3x) - \sin(x) = 2\cos(2x)\sin(x) = 0$$
:::

::: etape Factorisation
$\displaystyle 2\cos(2x)\sin(x) = 0$

- $\cos(2x) = 0$ ou $\sin(x) = 0$
:::

::: etape Solutions
$$
\begin{aligned}
\cos(2x) = 0 &\Rightarrow 2x = \frac{\pi}{2} + k\pi \\
&\Rightarrow x = \frac{\pi}{4} + \frac{k\pi}{2}
\end{aligned}
$$

- $\displaystyle\sin(x) = 0 \Rightarrow x = k\pi$
:::""",
     r"""::: methode
Égalité de deux sinus : $\sin(a) = \sin(b) \iff a = b + 2k\pi$ ou $a = \pi - b + 2k\pi$, avec $k \in \mathbb{Z}$
:::

::: etape Premier cas
$$3x = x + 2k\pi \iff 2x = 2k\pi \iff x = k\pi$$
:::

::: etape Second cas
$$3x = \pi - x + 2k\pi \iff 4x = \pi + 2k\pi \iff x = \frac{\pi}{4} + \frac{k\pi}{2}$$
:::"""),
    # Ex. 5 Q2 : rédaction des limites, intervalles fermés, carré non nul sur le domaine
    (r"""- $f'(x) = \frac{\cos(x)}{(1 + \sin(x))^2}$ où $(1 + \sin(x))^2 > 0$ toujours""",
     r"""- $f'(x) = \frac{\cos(x)}{(1 + \sin(x))^2}$ où $(1 + \sin(x))^2 > 0$ sur le domaine de $f$"""),
    (r"""  - Quand $x \to \left(\frac{3\pi}{2}\right)^-$ (par la gauche), $f$ décroît vers $-\infty$
  - Quand $x \to \left(\frac{3\pi}{2}\right)^+$ (par la droite), $f$ décroît vers $-\infty$
  - Sur l'intervalle $]\frac{3\pi}{2}, 2\pi]$, la fonction $f$ est croissante (car $f'(x) > 0$)""",
     r"""  - Quand $x \to \frac{3\pi}{2}$, le numérateur tend vers $-1$ et le dénominateur tend vers $0$ par valeurs positives : $\lim_{x \to \frac{3\pi}{2}} f(x) = -\infty$ (à gauche comme à droite)
  - Sur $\left]\frac{3\pi}{2}, 2\pi\right]$, $f$ est croissante (car $f'(x) > 0$) et remonte de $-\infty$ à $f(2\pi) = 0$"""),
    (r"""$f$ croît sur $[0, \frac{\pi}{2}[$ et $]\frac{3\pi}{2}, 2\pi]$, décroît sur $]\frac{\pi}{2}, \frac{3\pi}{2}[$
:::""",
     r"""$f$ croît sur $\left[0, \frac{\pi}{2}\right]$ et $\left]\frac{3\pi}{2}, 2\pi\right]$, décroît sur $\left[\frac{\pi}{2}, \frac{3\pi}{2}\right[$
:::"""),
    (r"""$f$ croît sur $[0, \frac{\pi}{2}[$ et $]\frac{3\pi}{2}, 2\pi]$, décroît sur $]\frac{\pi}{2}, \frac{3\pi}{2}[$, asymptote verticale en $x = \frac{3\pi}{2}$.""",
     r"""$f$ croît sur $\left[0, \frac{\pi}{2}\right]$ et $\left]\frac{3\pi}{2}, 2\pi\right]$, décroît sur $\left[\frac{\pi}{2}, \frac{3\pi}{2}\right[$, asymptote verticale d'équation $x = \frac{3\pi}{2}$."""),
    # Ex. 6 Q3 : sans cotangente ni équivalents (hors programme)
    (r"""\tan(x) &= \tan\left(u + \frac{\pi}{2}\right) \\
&= -\cot(u) \\
&= -\frac{\cos(u)}{\sin(u)}""",
     r"""\tan(x) &= \frac{\sin\left(u + \frac{\pi}{2}\right)}{\cos\left(u + \frac{\pi}{2}\right)} \\
&= \frac{\cos(u)}{-\sin(u)} \\
&= -\frac{\cos(u)}{\sin(u)}"""),
    (r"""::: etape Calcul de la limite avec équivalents
- Pour $u \to 0$, on utilise les équivalents : $\sin(u) \sim u$ et $\cos(u) \sim 1$
- Donc : $\displaystyle \frac{\cos(u)}{u\sin(u)} \sim \frac{1}{u \cdot u} = \frac{1}{u^2}$
- Par conséquent : $-\frac{\cos(u)}{u\sin(u)} \sim -\frac{1}{u^2} \to -\infty$ quand $u \to 0$
- **Justification rigoureuse :** $\lim_{u \to 0} \frac{\cos(u)}{u\sin(u)} = \lim_{u \to 0} \frac{\cos(u)}{u^2} \cdot \frac{u}{\sin(u)} = +\infty$ (car $\frac{u}{\sin(u)} \to 1$ et $\frac{\cos(u)}{u^2} \to +\infty$)
- Donc : $\displaystyle \lim_{u \to 0} \frac{-\cos(u)}{u\sin(u)} = -\infty$
:::""",
     r"""::: etape Calcul de la limite
- On écrit $\displaystyle -\frac{\cos(u)}{u\sin(u)} = -\frac{\cos(u)}{u^2} \times \frac{u}{\sin(u)}$
- Quand $u \to 0$ : $\dfrac{u}{\sin(u)} \to 1$ (limite de référence) et $\dfrac{\cos(u)}{u^2} \to +\infty$ (car $\cos(u) \to 1$ et $u^2 \to 0$ par valeurs positives)
- Donc $\displaystyle \lim_{u \to 0} -\frac{\cos(u)}{u\sin(u)} = -\infty$
:::"""),
    # Ex. 7 Q5 : décomposition directe 5π/12 = π/4 + π/6
    (r"""::: etape Décomposition
$$\frac{5\pi}{12} = \frac{\pi}{3} + \frac{\pi}{12}$$
:::

::: etape Formule d'addition
$$\sin\left(\frac{\pi}{3} + \frac{\pi}{12}\right) = \sin\left(\frac{\pi}{3}\right)\cos\left(\frac{\pi}{12}\right) + \cos\left(\frac{\pi}{3}\right)\sin\left(\frac{\pi}{12}\right)$$
:::

::: etape Valeurs
$\sin\left(\frac{\pi}{3}\right) = \frac{\sqrt{3}}{2}$, $\cos\left(\frac{\pi}{3}\right) = \frac{1}{2}$

- $\displaystyle\cos\left(\frac{\pi}{12}\right) = \frac{\sqrt{2} + \sqrt{6}}{4}$ (question 2)
- $\displaystyle\sin\left(\frac{\pi}{12}\right) = \frac{\sqrt{6} - \sqrt{2}}{4}$
:::

::: etape Calcul
$$\frac{\sqrt{3}}{2} \cdot \frac{\sqrt{2} + \sqrt{6}}{4} + \frac{1}{2} \cdot \frac{\sqrt{6} - \sqrt{2}}{4} = \frac{\sqrt{6} + \sqrt{2}}{4}$$
:::""",
     r"""::: etape Décomposition
$$\frac{5\pi}{12} = \frac{\pi}{4} + \frac{\pi}{6}$$
:::

::: etape Formule d'addition
$$\sin\left(\frac{\pi}{4} + \frac{\pi}{6}\right) = \sin\left(\frac{\pi}{4}\right)\cos\left(\frac{\pi}{6}\right) + \cos\left(\frac{\pi}{4}\right)\sin\left(\frac{\pi}{6}\right)$$
:::

::: etape Calcul
$$\frac{\sqrt{2}}{2} \cdot \frac{\sqrt{3}}{2} + \frac{\sqrt{2}}{2} \cdot \frac{1}{2} = \frac{\sqrt{6} + \sqrt{2}}{4}$$
:::"""),
    # Ex. 8 Q3 : comparer aussi les valeurs aux bornes
    (r"""&= -\frac{\sqrt{2}}{2} - \frac{\sqrt{2}}{2} \\
&= -\sqrt{2}
\end{aligned}
$$
:::

::: resultat
Maximum de $f$ sur $[0, 2\pi]$ est $\sqrt{2}$ atteint en $x = \frac{\pi}{4}$
:::""",
     r"""&= -\frac{\sqrt{2}}{2} - \frac{\sqrt{2}}{2} \\
&= -\sqrt{2}
\end{aligned}
$$

Aux bornes : $f(0) = f(2\pi) = 1$.
:::

::: resultat
Le maximum de $f$ sur $[0, 2\pi]$ est $\sqrt{2}$, atteint en $x = \frac{\pi}{4}$.
:::"""),
    (r"""3. Maximum de $f$ sur $[0, 2\pi]$ est $\sqrt{2}$ atteint en $x = \frac{\pi}{4}$""",
     r"""3. Le maximum de $f$ sur $[0, 2\pi]$ est $\sqrt{2}$, atteint en $x = \frac{\pi}{4}$."""),
    # Ex. 8 Q5 : transformation d'une inéquation = équivalence
    (r"""Transformation en forme canonique""", r"""Mise sous la forme $\sqrt{2}\sin\left(x + \frac{\pi}{4}\right)$"""),
    (r"""\sqrt{2}\sin\left(x + \frac{\pi}{4}\right) \geq 1 &\Rightarrow \sin\left(x + \frac{\pi}{4}\right) \geq \frac{1}{\sqrt{2}} = \frac{\sqrt{2}}{2}""",
     r"""\sqrt{2}\sin\left(x + \frac{\pi}{4}\right) \geq 1 &\iff \sin\left(x + \frac{\pi}{4}\right) \geq \frac{\sqrt{2}}{2}"""),
    # Ex. 9 Q5 : indice de somme
    (r"""&= t_n + \sum_{j=0}^{5} \cos\left(\frac{(n+j)\pi}{3}\right)""",
     r"""&= t_n + \sum_{j=1}^{6} \cos\left(\frac{(n+j)\pi}{3}\right)"""),
    # Ex. 10 : rappel de méthode, primitive de u'/u (pas de changement de variable), résultats
    (r"""**Méthode générale :** Théorème fondamental du calcul intégral

::: rappel Formule
$\int_a^b f(x)\, dx = F(b) - F(a)$ où $F$ est une primitive de $f$
:::""",
     r"""::: rappel Calcul d'une intégrale
$\displaystyle\int_a^b f(x)\, dx = F(b) - F(a)$, où $F$ est une primitive de $f$ sur $[a, b]$.
:::"""),
    (r"""&= 1 - (-1) \\
&= 2
\end{aligned}
$$
:::""",
     r"""&= 1 - (-1) \\
&= 2
\end{aligned}
$$
:::

::: resultat
$$\int_0^{\pi} \sin(x)\, dx = 2$$
:::"""),
    (r"""&= \frac{\pi}{4} - 0 \\
&= \frac{\pi}{4}
\end{aligned}
$$
:::""",
     r"""&= \frac{\pi}{4} - 0 \\
&= \frac{\pi}{4}
\end{aligned}
$$
:::

::: resultat
$$\int_0^{\frac{\pi}{2}} \cos^2(x)\, dx = \frac{\pi}{4}$$
:::"""),
    (r"""&= -\frac{1}{2} - \left(-\frac{1}{2}\right) \\
&= 0
\end{aligned}
$$
:::""",
     r"""&= -\frac{1}{2} - \left(-\frac{1}{2}\right) \\
&= 0
\end{aligned}
$$
:::

::: resultat
$$\int_0^{\pi} \sin(2x)\, dx = 0$$
:::"""),
    (r"""::: methode
Substitution avec $u = \cos(x)$ donc $du = -\sin(x)\, dx$

$$
\begin{aligned}
\int \tan(x)\, dx &= \int \frac{\sin(x)}{\cos(x)}\, dx \\
&= -\int \frac{du}{u} \\
&= -\ln|u| + C
\end{aligned}
$$
:::""",
     r"""::: etape Forme $-\dfrac{u'}{u}$
Avec $u(x) = \cos(x)$ : $u'(x) = -\sin(x)$ et $u(x) > 0$ sur $\left[0, \frac{\pi}{4}\right]$, donc

$$\tan(x) = \frac{\sin(x)}{\cos(x)} = -\frac{u'(x)}{u(x)}$$
:::"""),
    (r"""$$F(x) = -\ln|\cos(x)| + C$$""", r"""$$F(x) = -\ln(\cos(x))$$"""),
    (r"""&= \ln(\sqrt{2}) \\
&= \frac{1}{2}\ln(2)
\end{aligned}
$$
:::""",
     r"""&= \ln(\sqrt{2}) \\
&= \frac{1}{2}\ln(2)
\end{aligned}
$$
:::

::: resultat
$$\int_0^{\frac{\pi}{4}} \tan(x)\, dx = \frac{1}{2}\ln(2)$$
:::"""),
    (r"""1. $\displaystyle 2$
2. $\displaystyle \frac{\pi}{4}$
3. $\displaystyle -\frac{\cos(2x)}{4} + C$
4. $\displaystyle 0$
5. $\displaystyle \frac{1}{2}\ln(2)$""",
     r"""1. $\displaystyle\int_0^{\pi} \sin(x)\, dx = 2$
2. $\displaystyle\int_0^{\frac{\pi}{2}} \cos^2(x)\, dx = \frac{\pi}{4}$
3. $\displaystyle\int \sin(x)\cos(x)\, dx = -\frac{\cos(2x)}{4} + C$
4. $\displaystyle\int_0^{\pi} \sin(2x)\, dx = 0$
5. $\displaystyle\int_0^{\frac{\pi}{4}} \tan(x)\, dx = \frac{1}{2}\ln(2)$"""),
]


def appliquer(nom, corrections):
    p = ICI / nom
    texte = p.read_text(encoding="utf-8")
    for avant, apres in corrections:
        n = texte.count(avant)
        if n != 1:
            raise SystemExit(f"{nom} : passage trouvé {n} fois (1 attendu) :\n{avant[:160]}")
        texte = texte.replace(avant, apres)
    p.write_text(texte, encoding="utf-8")
    return len(corrections)


if __name__ == "__main__":
    total = sum(appliquer(nom, liste) for nom, liste in (("cours.txt", COURS), ("fiche.txt", FICHE), ("exercices.txt", EXERCICES)) if liste)
    print(f"{total} corrections appliquées")
