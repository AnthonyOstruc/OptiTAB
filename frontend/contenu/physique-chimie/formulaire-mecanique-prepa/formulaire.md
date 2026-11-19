---
{
  "slug": "formulaire-mecanique-prepa",
  "titre": "Formulaire de mécanique : prépa, licence et master",
  "titreCourt": "Mécanique (prépa et licence)",
  "titreSeo": "Formulaire de mécanique : prépa, licence, Lagrange et Hamilton",
  "description": "Formulaire de mécanique du supérieur : coordonnées polaires, énergie, moment cinétique, forces centrales, solide, référentiel non galiléen, Lagrange.",
  "chapo": "Toutes les formules de mécanique de la prépa (MPSI, PCSI, PTSI, MP, PC, PSI) et de la licence, dans l’ordre du cours : cinématique, lois de Newton, énergie, oscillateurs, particules chargées, moment cinétique, forces centrales, solide, référentiels non galiléens, frottement, systèmes de points et mécanique analytique.",
  "resume": "Polaires, énergie, Kepler, solide, Coriolis, Lagrange",
  "vignette": "energie_potentielle_effective",
  "theme": "Mécanique",
  "niveaux": [
    "Supérieur"
  ],
  "ordre": 12,
  "publie": "2026-11-19",
  "modifie": "2026-11-19",
  "motsCles": [
    "formulaire mécanique prépa",
    "formulaire de mécanique",
    "mécanique du point",
    "formulaire physique MPSI",
    "coordonnées polaires vitesse accélération",
    "coordonnées cylindriques",
    "coordonnées sphériques",
    "théorème du moment cinétique",
    "énergie potentielle effective",
    "force centrale",
    "lois de Kepler",
    "vitesse de libération",
    "force de Lorentz",
    "rayon cyclotron",
    "moment d'inertie",
    "pendule pesant",
    "référentiel non galiléen",
    "force de Coriolis",
    "force centrifuge",
    "lois de Coulomb frottement solide",
    "théorème de König",
    "masse réduite",
    "mécanique analytique",
    "équations de Lagrange",
    "équations de Hamilton"
  ],
  "figures": [
    {
      "nom": "coordonnees_polaires",
      "alt": "Coordonnées polaires d’un point M du plan : la distance r = OM et l’angle θ mesuré depuis l’axe Ox. En M, le vecteur unitaire ur est dirigé selon OM, vers l’extérieur, et le vecteur uθ lui est perpendiculaire, dans le sens des θ croissants."
    },
    {
      "nom": "energie_potentielle_effective",
      "alt": "Graphe de l’énergie potentielle effective Ep,eff(r) d’un champ newtonien : très grande quand r tend vers 0, un minimum négatif qui correspond à l’orbite circulaire, puis une remontée vers 0. Une énergie mécanique négative donne un état lié, le mouvement radial restant entre rmin et rmax ; une énergie mécanique positive donne un état de diffusion."
    },
    {
      "nom": "particule_champ_magnetique",
      "alt": "Particule de charge positive dans un champ magnétique uniforme B dirigé vers le lecteur : sa trajectoire est un cercle de centre C et de rayon R, parcouru dans le sens des aiguilles d’une montre. La vitesse v est tangente au cercle et la force de Lorentz F = q v ∧ B est dirigée vers le centre."
    },
    {
      "nom": "pendule_pesant",
      "alt": "Pendule pesant : un solide mobile autour d’un axe horizontal Δ passant par O, perpendiculaire au plan de la figure. Son centre de gravité G est à la distance d de l’axe ; le solide est écarté d’un angle θ de la verticale, et son poids P s’applique en G, verticalement vers le bas."
    }
  ],
  "liees": [
    "physique-chimie/formules-de-mecanique",
    "physique-chimie/electrocinetique",
    "formulaires/equations-differentielles",
    "formulaires/developpements-limites"
  ],
  "faq": [
    [
      "Quelles sont la vitesse et l’accélération en coordonnées polaires ?",
      "Avec OM = r ur : la vitesse vaut v = ṙ ur + r θ̇ uθ, et l’accélération a = (r̈ − r θ̇²) ur + (2 ṙ θ̇ + r θ̈) uθ. En coordonnées cylindriques, on ajoute ż uz à la vitesse et z̈ uz à l’accélération. Les vecteurs ur et uθ tournent avec le point : dur/dt = θ̇ uθ et duθ/dt = −θ̇ ur."
    ],
    [
      "Qu’est-ce que l’énergie potentielle effective ?",
      "Pour un point soumis à une force centrale conservative, la conservation du moment cinétique permet d’écrire l’énergie mécanique Em = ½ m ṙ² + Ep,eff(r), avec Ep,eff(r) = m C² / (2 r²) + Ep(r), où C = r² θ̇ est la constante des aires. Le mouvement radial n’est possible que là où Ep,eff(r) ≤ Em : il est borné (état lié) ou non (état de diffusion)."
    ],
    [
      "Quel est le rayon de la trajectoire d’une particule chargée dans un champ magnétique ?",
      "Si la vitesse initiale est perpendiculaire au champ uniforme B, le mouvement est circulaire uniforme de rayon R = m v / (|q| B) et de pulsation ωc = |q| B / m, indépendante de la vitesse. Un proton à 1,0 × 10⁶ m/s dans un champ de 1,0 T décrit un cercle de rayon 1,0 × 10⁻² m, à la fréquence 1,5 × 10⁷ Hz."
    ],
    [
      "Comment calculer la vitesse de libération ?",
      "C’est la vitesse minimale pour échapper à l’attraction d’un astre de masse M et de rayon R : l’énergie mécanique doit être positive ou nulle, d’où v = √(2 G M / R). Pour la Terre, elle vaut environ 11,2 km/s, soit √2 fois la vitesse en orbite rasante (7,9 km/s)."
    ],
    [
      "Que dit le théorème du moment cinétique ?",
      "Dans un référentiel galiléen, la dérivée du moment cinétique en un point fixe O est égale à la somme des moments des forces en O : dLO/dt = Σ MO(F). Pour un solide en rotation autour d’un axe fixe Δ, il s’écrit J × dω/dt = Σ MΔ, où J est le moment d’inertie. Si la force est centrale, le moment cinétique se conserve : le mouvement est plan et suit la loi des aires."
    ],
    [
      "Quelles sont les équations de Lagrange ?",
      "Avec le lagrangien L = T − V, fonction des coordonnées généralisées qi et de leurs dérivées : d/dt(∂L/∂q̇i) − ∂L/∂qi = 0, une équation par degré de liberté. Pour le pendule simple, L = ½ m ℓ² θ̇² + m g ℓ cos θ donne θ̈ + (g/ℓ) sin θ = 0. Si une coordonnée n’apparaît pas dans L, son moment conjugué pi = ∂L/∂q̇i se conserve."
    ]
  ]
}
---
<!-- optitab:1 -->
::: conseil Comment lire ce formulaire
- Un point au-dessus d’une grandeur désigne sa dérivée par rapport au temps : $\dot{x} = \dfrac{\mathrm{d}x}{\mathrm{d}t}$ et $\ddot{x} = \dfrac{\mathrm{d}^2x}{\mathrm{d}t^2}$. Le symbole $\wedge$ est le produit vectoriel.
- **Première année de prépa** (MPSI, PCSI, PTSI, MP2I) : parties I à VIII. **Deuxième année** : parties IX et X. **Licence et master** : parties XI et XII.
- Les bases du lycée (poids, deuxième loi de Newton, chute libre) sont sur la page des formules de mécanique du lycée, en lien en bas de page.
:::

## I. Cinématique du point {Supérieur}

*Première année de prépa.*

::: formule Coordonnées cartésiennes
$$\begin{aligned}
\overrightarrow{OM} &= x\,\vec{u}_x + y\,\vec{u}_y + z\,\vec{u}_z \\
\vec{v} &= \dot{x}\,\vec{u}_x + \dot{y}\,\vec{u}_y + \dot{z}\,\vec{u}_z \\
\vec{a} &= \ddot{x}\,\vec{u}_x + \ddot{y}\,\vec{u}_y + \ddot{z}\,\vec{u}_z
\end{aligned}$$
:::

En coordonnées **polaires** $(r, \theta)$, le vecteur $\vec{u}_r$ est dirigé selon $\overrightarrow{OM}$ et $\vec{u}_\theta$ lui est perpendiculaire, dans le sens des $\theta$ croissants. Les coordonnées **cylindriques** ajoutent la cote $z$.

[IMAGE_1]

::: formule Coordonnées cylindriques
$$\begin{aligned}
\overrightarrow{OM} &= r\,\vec{u}_r + z\,\vec{u}_z \\
\vec{v} &= \dot{r}\,\vec{u}_r + r\dot{\theta}\,\vec{u}_\theta + \dot{z}\,\vec{u}_z \\
\vec{a} &= (\ddot{r} - r\dot{\theta}^2)\,\vec{u}_r \\
&\quad + (2\dot{r}\dot{\theta} + r\ddot{\theta})\,\vec{u}_\theta + \ddot{z}\,\vec{u}_z
\end{aligned}$$
:::

::: attention La base polaire tourne avec le point
$\vec{u}_r$ et $\vec{u}_\theta$ ne sont pas fixes : $\dfrac{\mathrm{d}\vec{u}_r}{\mathrm{d}t} = \dot{\theta}\,\vec{u}_\theta$ et $\dfrac{\mathrm{d}\vec{u}_\theta}{\mathrm{d}t} = -\dot{\theta}\,\vec{u}_r$. Oublier ces dérivées fait perdre les termes $-r\dot{\theta}^2$ et $2\dot{r}\dot{\theta}$ de l’accélération.
:::

::: formule Déplacement élémentaire en cartésiennes
$$\mathrm{d}\overrightarrow{OM} = \mathrm{d}x\,\vec{u}_x + \mathrm{d}y\,\vec{u}_y + \mathrm{d}z\,\vec{u}_z$$
:::

::: formule Déplacement élémentaire en cylindriques
$$\mathrm{d}\overrightarrow{OM} = \mathrm{d}r\,\vec{u}_r + r\,\mathrm{d}\theta\,\vec{u}_\theta + \mathrm{d}z\,\vec{u}_z$$
:::

En coordonnées **sphériques** $(r, \theta, \varphi)$, avec $\theta$ l’angle mesuré depuis l’axe $Oz$ :

::: formule Coordonnées sphériques
$$\begin{aligned}
\mathrm{d}\overrightarrow{OM} &= \mathrm{d}r\,\vec{u}_r + r\,\mathrm{d}\theta\,\vec{u}_\theta \\
&\quad + r\sin\theta\,\mathrm{d}\varphi\,\vec{u}_\varphi
\end{aligned}$$
:::

::: formule Mouvement circulaire de rayon R
$$\begin{aligned}
\vec{v} &= R\dot{\theta}\,\vec{u}_\theta \\
\vec{a} &= -R\dot{\theta}^2\,\vec{u}_r + R\ddot{\theta}\,\vec{u}_\theta
\end{aligned}$$
:::

::: formule Repère de Frenet (trajectoire plane)
$$\vec{a} = \dfrac{\mathrm{d}v}{\mathrm{d}t}\,\vec{T} + \dfrac{v^2}{\rho}\,\vec{N}$$
:::

$\vec{T}$ est tangent à la trajectoire dans le sens du mouvement, $\vec{N}$ est dirigé vers le centre de courbure, et $\rho$ est le rayon de courbure de la trajectoire.

## II. Les lois de Newton {Supérieur}

*Première année de prépa.*

::: formule Quantité de mouvement et deuxième loi de Newton
$$\vec{p} = m\,\vec{v} \qquad \dfrac{\mathrm{d}\vec{p}}{\mathrm{d}t} = \sum \vec{F}$$
:::

Pour un système fermé de masse $M$ : $\vec{p} = M\,\vec{v}(G)$ et $M\,\vec{a}(G) = \sum \vec{F}_{\mathrm{ext}}$, dans un référentiel galiléen.

| Frottement fluide | Force | Vitesse limite (chute) |
|---|---|---|
| linéaire (faible vitesse) | $-\alpha\,\vec{v}$ | $\dfrac{m g}{\alpha}$ |
| quadratique | $-k\,v\,\vec{v}$ | $\sqrt{\dfrac{m g}{k}}$ |

Dans le modèle linéaire, la vitesse tend vers sa limite avec le temps caractéristique $\tau = \dfrac{m}{\alpha}$.

::: exemple
Un parachutiste de 80 kg en chute libre à plat, avec $k = 0{,}25$ kg/m : $v_{\lim} = \sqrt{\dfrac{80 \times 9{,}81}{0{,}25}} \approx 56$ m/s, soit environ 202 km/h.
:::

::: formule Pendule simple (fil de longueur ℓ)
$$\ddot{\theta} + \dfrac{g}{\ell}\sin\theta = 0$$
:::

Pour les petits angles, $\sin\theta \approx \theta$ : oscillateur harmonique de pulsation $\omega_0 = \sqrt{\dfrac{g}{\ell}}$ et de période $T_0 = 2\pi\sqrt{\dfrac{\ell}{g}}$. Avec $\ell = 1{,}00$ m : $T_0 \approx 2{,}01$ s.

## III. Énergie : travail, puissance, énergie potentielle {Supérieur}

*Première année de prépa.*

::: formule Puissance et travail d’une force
$$\mathcal{P} = \vec{F} \cdot \vec{v} \qquad \delta W = \vec{F} \cdot \mathrm{d}\overrightarrow{OM}$$
:::

::: formule Théorèmes de la puissance et de l’énergie cinétique
$$\dfrac{\mathrm{d}E_c}{\mathrm{d}t} = \sum \mathcal{P} \qquad \Delta E_c = \sum W$$
:::

Une force est **conservative** si son travail ne dépend pas du chemin suivi : elle dérive alors d’une énergie potentielle, $\vec{F} = -\overrightarrow{\mathrm{grad}}\,E_p$ (à une dimension : $F_x = -\dfrac{\mathrm{d}E_p}{\mathrm{d}x}$).

| Force | Énergie potentielle |
|---|---|
| poids, axe $z$ vers le haut | $E_p = m g z$ |
| gravitation d’un astre de masse $M$ | $E_p = -\dfrac{G M m}{r}$ |
| ressort de raideur $k$ | $E_p = \dfrac{1}{2}\,k\,(\ell - \ell_0)^2$ |
| force électrique | $E_p = q\,V$ |

::: formule Théorème de l’énergie mécanique
$$E_m = E_c + E_p \qquad \Delta E_m = W_{\mathrm{nc}}$$
:::

$W_{\mathrm{nc}}$ est le travail des forces non conservatives, comme les frottements : l’énergie mécanique se conserve s’il est nul.

::: retenir Positions d’équilibre et stabilité (mouvement à une dimension)
- Équilibre en $x_e$ : $\dfrac{\mathrm{d}E_p}{\mathrm{d}x}(x_e) = 0$.
- Équilibre **stable** si $\dfrac{\mathrm{d}^2E_p}{\mathrm{d}x^2}(x_e) > 0$ (puits de potentiel), instable si elle est négative.
- Petits mouvements autour d’un équilibre stable : oscillations harmoniques de pulsation $\omega_0 = \sqrt{\dfrac{E_p''(x_e)}{m}}$.
:::

## IV. Les oscillateurs {Supérieur}

*Première année de prépa.*

::: formule Oscillateur harmonique (masse et ressort)
$$\ddot{x} + \omega_0^2\,x = 0 \qquad \omega_0 = \sqrt{\dfrac{k}{m}}$$
:::

Solution : $x(t) = X_m\cos(\omega_0 t + \varphi)$, et l’énergie mécanique $E_m = \dfrac{1}{2}\,k\,X_m^2$ se conserve.

::: formule Oscillateur amorti par frottement fluide
$$\ddot{x} + \dfrac{\omega_0}{Q}\,\dot{x} + \omega_0^2\,x = 0 \qquad Q = \dfrac{m\,\omega_0}{\alpha}$$
:::

| Facteur de qualité | Régime |
|---|---|
| $Q > \dfrac{1}{2}$ | pseudo-périodique, pseudo-pulsation $\omega = \omega_0\sqrt{1 - \dfrac{1}{4Q^2}}$ |
| $Q = \dfrac{1}{2}$ | critique : retour à l’équilibre le plus rapide, sans oscillation |
| $Q < \dfrac{1}{2}$ | apériodique |

C’est la même équation que celle du circuit RLC série : la masse joue le rôle de l’inductance, le ressort celui du condensateur, le frottement celui de la résistance.

## V. Particules chargées dans un champ électrique ou magnétique {Supérieur}

*Première année de prépa.*

::: formule Force de Lorentz
$$\vec{F} = q\,(\vec{E} + \vec{v} \wedge \vec{B})$$
:::

Sa puissance vaut $\mathcal{P} = q\,\vec{E} \cdot \vec{v}$ : la force magnétique est perpendiculaire à la vitesse et **ne travaille pas**. Un champ magnétique courbe la trajectoire sans changer la valeur de la vitesse.

**Champ électrique uniforme** : $\vec{a} = \dfrac{q\,\vec{E}}{m}$, mouvement à vecteur accélération constant. Accélérée depuis le repos par une tension $U$ :

::: formule Vitesse après une accélération sous la tension U
$$\dfrac{1}{2}\,m\,v^2 = |q|\,U$$
:::

::: exemple
Un électron accéléré sous 1,0 kV atteint $v = \sqrt{\dfrac{2\,e\,U}{m_e}} \approx 1{,}9 \times 10^{7}$ m/s, environ 6 % de la vitesse de la lumière : le calcul classique reste valable.
:::

**Champ magnétique uniforme**, vitesse initiale perpendiculaire à $\vec{B}$ : le mouvement est **circulaire uniforme**.

[IMAGE_3]

::: formule Rayon et pulsation cyclotron
$$R = \dfrac{m\,v}{|q|\,B} \qquad \omega_c = \dfrac{|q|\,B}{m}$$
:::

::: exemple
Un proton à $1{,}0 \times 10^{6}$ m/s dans un champ de 1,0 T : $R \approx 1{,}0 \times 10^{-2}$ m, soit 1,0 cm, et la fréquence $f_c = \dfrac{\omega_c}{2\pi} \approx 1{,}5 \times 10^{7}$ Hz, quelle que soit sa vitesse.
:::

::: attention Le sens de rotation dépend du signe de la charge
Avec $\vec{B}$ dirigé vers le lecteur, une charge positive tourne dans le sens des aiguilles d’une montre, une charge négative dans l’autre sens. Ces formules ne valent que si $v$ est très inférieure à la vitesse de la lumière.
:::

## VI. Le moment cinétique {Supérieur}

*Première année de prépa.*

::: formule Moment cinétique et moment d’une force en O
$$\vec{L}_O = \overrightarrow{OM} \wedge m\,\vec{v} \qquad \vec{\mathcal{M}}_O(\vec{F}) = \overrightarrow{OM} \wedge \vec{F}$$
:::

Par rapport à un axe orienté $\Delta$ passant par $O$ : $L_\Delta = \vec{L}_O \cdot \vec{u}_\Delta$, et $\mathcal{M}_\Delta = \pm F\,d$, où $d$ est le **bras de levier**, la distance entre l’axe et la droite d’action de la force. Pour un point qui tourne autour de l’axe à la distance $r$ : $L_\Delta = m\,r^2\,\dot{\theta}$.

::: formule Théorème du moment cinétique (point fixe O, référentiel galiléen)
$$\dfrac{\mathrm{d}\vec{L}_O}{\mathrm{d}t} = \sum \vec{\mathcal{M}}_O(\vec{F})$$
:::

::: retenir Conservation du moment cinétique
Si la somme des moments est nulle, par exemple pour une **force centrale** dirigée vers $O$, le moment cinétique en $O$ se conserve.
:::

## VII. Forces centrales et lois de Kepler {Supérieur}

*Première année de prépa.*

Pour une force centrale, la conservation de $\vec{L}_O$ entraîne un **mouvement plan** et la **loi des aires** :

::: formule Constante des aires
$$C = r^2\,\dot{\theta} \qquad \dfrac{\mathrm{d}\mathcal{A}}{\mathrm{d}t} = \dfrac{C}{2}$$
:::

::: formule Énergie potentielle effective (force centrale conservative)
$$\begin{aligned}
E_m &= \dfrac{1}{2}\,m\,\dot{r}^2 + E_{p,\mathrm{eff}}(r) \\
E_{p,\mathrm{eff}}(r) &= \dfrac{m\,C^2}{2\,r^2} + E_p(r)
\end{aligned}$$
:::

[IMAGE_2]

Le mouvement radial n’est possible que là où $E_{p,\mathrm{eff}}(r) \leq E_m$. Pour le champ newtonien, $E_p = -\dfrac{G M m}{r}$ : si $E_m < 0$, la trajectoire est bornée (**état lié**, une ellipse) ; si $E_m \geq 0$, elle ne l’est pas (**état de diffusion**). Le minimum de $E_{p,\mathrm{eff}}$ correspond à l’orbite circulaire.

::: formule Orbite circulaire de rayon r
$$\begin{aligned}
v &= \sqrt{\dfrac{G M}{r}} \qquad \dfrac{T^2}{r^3} = \dfrac{4\pi^2}{G M} \\
E_m &= -\dfrac{G M m}{2\,r} = -E_c
\end{aligned}$$
:::

::: formule Orbite elliptique de demi-grand axe a
$$E_m = -\dfrac{G M m}{2\,a} \qquad \dfrac{T^2}{a^3} = \dfrac{4\pi^2}{G M}$$
:::

::: formule Vitesses cosmiques (astre de rayon R)
$$v_1 = \sqrt{\dfrac{G M}{R}} \qquad v_2 = \sqrt{\dfrac{2\,G M}{R}}$$
:::

::: exemple
Pour la Terre : la vitesse en orbite rasante vaut $v_1 \approx 7{,}9$ km/s et la **vitesse de libération** $v_2 = \sqrt{2}\,v_1 \approx 11{,}2$ km/s.
:::

## VIII. Solide en rotation autour d’un axe fixe {Supérieur}

*Première année de prépa.*

Tous les points du solide tournent à la même vitesse angulaire $\omega = \dot{\theta}$ ; un point à la distance $r$ de l’axe a la vitesse $v = r\,\omega$.

::: formule Moment cinétique et énergie cinétique
$$L_\Delta = J_\Delta\,\omega \qquad E_c = \dfrac{1}{2}\,J_\Delta\,\omega^2$$
:::

::: formule Théorème scalaire du moment cinétique
$$J_\Delta\,\dfrac{\mathrm{d}\omega}{\mathrm{d}t} = \sum \mathcal{M}_\Delta$$
:::

Une **liaison pivot parfaite** exerce un moment nul par rapport à son axe. Un **couple** est un ensemble de forces de résultante nulle et de moment non nul ; la puissance d’un couple de moment $\Gamma$ vaut $\mathcal{P} = \Gamma\,\omega$.

| Solide homogène de masse $M$ | Moment d’inertie |
|---|---|
| cerceau ou cylindre creux mince, axe de révolution | $M R^2$ |
| disque ou cylindre plein, axe de révolution | $\dfrac{1}{2}\,M R^2$ |
| boule pleine, axe passant par le centre | $\dfrac{2}{5}\,M R^2$ |
| sphère creuse mince, axe passant par le centre | $\dfrac{2}{3}\,M R^2$ |
| tige de longueur $L$, axe perpendiculaire en son milieu | $\dfrac{1}{12}\,M L^2$ |
| tige de longueur $L$, axe perpendiculaire en une extrémité | $\dfrac{1}{3}\,M L^2$ |

::: formule Théorème de Huygens
$$J_\Delta = J_G + M\,d^2$$
:::

$J_G$ est le moment d’inertie par rapport à l’axe parallèle à $\Delta$ passant par le centre de masse $G$, et $d$ la distance entre les deux axes.

::: exemple
Un disque de 2,0 kg et de rayon 0,10 m : $J = \dfrac{1}{2} \times 2{,}0 \times 0{,}10^2 = 0{,}010$ kg·m². À 10 rad/s, son énergie cinétique vaut $E_c = \dfrac{1}{2} \times 0{,}010 \times 10^2 = 0{,}50$ J.
:::

[IMAGE_4]

::: formule Pendule pesant
$$J_\Delta\,\ddot{\theta} + m\,g\,d\,\sin\theta = 0$$
:::

Pour les petits angles : $\omega_0 = \sqrt{\dfrac{m\,g\,d}{J_\Delta}}$. L’action de l’axe n’intervient pas : son moment est nul pour une liaison pivot parfaite.

::: exemple
Une tige homogène de 1,00 m oscillant autour d’une extrémité : $J_\Delta = \dfrac{M L^2}{3}$ et $d = \dfrac{L}{2}$, d’où $T_0 = 2\pi\sqrt{\dfrac{2L}{3g}} \approx 1{,}64$ s, contre 2,01 s pour un pendule simple de même longueur.
:::

## IX. Les référentiels non galiléens {Supérieur}

*Deuxième année de prépa.*

$\mathcal{R}$ est le référentiel galiléen (absolu), $\mathcal{R}'$ le référentiel en mouvement (relatif).

::: formule Composition des vitesses et des accélérations
$$\begin{aligned}
\vec{v}_a &= \vec{v}_r + \vec{v}_e \\
\vec{a}_a &= \vec{a}_r + \vec{a}_e + \vec{a}_c
\end{aligned}$$
:::

| Mouvement de $\mathcal{R}'$ | Accélérations d’entraînement et de Coriolis |
|---|---|
| translation | $\vec{a}_e = \vec{a}(O')$ et $\vec{a}_c = \vec{0}$ |
| rotation uniforme $\vec{\Omega}$ autour d’un axe fixe | $\vec{a}_e = -\Omega^2\,\overrightarrow{HM}$ et $\vec{a}_c = 2\,\vec{\Omega} \wedge \vec{v}_r$ |

$H$ est le projeté de $M$ sur l’axe de rotation.

::: formule Deuxième loi de Newton dans un référentiel non galiléen
$$\begin{aligned}
m\,\vec{a}_r &= \sum \vec{F} + \vec{f}_{ie} + \vec{f}_{ic} \\
\vec{f}_{ie} &= -m\,\vec{a}_e \qquad \vec{f}_{ic} = -2m\,\vec{\Omega} \wedge \vec{v}_r
\end{aligned}$$
:::

En rotation uniforme, la force d’inertie d’entraînement est la **force centrifuge** $m\,\Omega^2\,\overrightarrow{HM}$ : elle dérive de l’énergie potentielle $-\dfrac{1}{2}\,m\,\Omega^2\,HM^2$.

::: exemple
Sur un manège tournant à 1,0 rad/s, une personne de 70 kg à 3,0 m de l’axe subit une force centrifuge $m\,\Omega^2\,r = 2{,}1 \times 10^{2}$ N, soit 31 % de son poids. La Terre tourne à $\Omega = 7{,}29 \times 10^{-5}$ rad/s : pour un objet lancé à 100 m/s, l’accélération de Coriolis ne dépasse pas $2\,\Omega\,v \approx 1{,}5 \times 10^{-2}$ m/s², 0,15 % de $g$.
:::

::: attention La force de Coriolis ne travaille pas
Elle est perpendiculaire à $\vec{v}_r$ : sa puissance est nulle dans $\mathcal{R}'$. Elle dévie la trajectoire sans changer l’énergie cinétique relative.
:::

## X. Le frottement solide : lois de Coulomb {Supérieur}

*Deuxième année de prépa.*

L’action de contact se décompose en une composante normale $\vec{N}$ et une composante tangentielle $\vec{T}$. Avec $f$ le coefficient de frottement :

::: formule Lois de Coulomb : sans glissement
$$\|\vec{T}\| \leq f\,\|\vec{N}\|$$
:::

::: formule Lois de Coulomb : avec glissement
$$\|\vec{T}\| = f\,\|\vec{N}\|$$
:::

En cas de glissement, $\vec{T}$ est opposée à la vitesse de glissement. La puissance totale des actions de contact est négative ou nulle, nulle en l’absence de glissement.

::: exemple
Un solide posé sur un plan incliné d’angle $\alpha$ reste immobile tant que $\tan\alpha \leq f$. Avec $f = 0{,}50$ : il commence à glisser au-delà de $\alpha \approx 27°$.
:::

## XI. Systèmes de points et problème à deux corps {Supérieur}

*Licence.*

::: formule Centre de masse et résultante cinétique
$$\overrightarrow{OG} = \dfrac{1}{M}\sum_i m_i\,\overrightarrow{OM_i} \qquad M\,\vec{a}_G = \sum \vec{F}_{\mathrm{ext}}$$
:::

Les forces intérieures se compensent deux à deux (troisième loi de Newton) : seules les forces extérieures font varier la quantité de mouvement du système.

::: formule Théorèmes de König
$$\begin{aligned}
E_c &= \dfrac{1}{2}\,M\,v_G^2 + E_c^* \\
\vec{L}_O &= \overrightarrow{OG} \wedge M\,\vec{v}_G + \vec{L}^*
\end{aligned}$$
:::

L’astérisque désigne les grandeurs calculées dans le **référentiel barycentrique**. Pour un solide qui tourne à la vitesse angulaire $\omega$ autour d’un axe passant par $G$ et de direction fixe : $E_c = \dfrac{1}{2}\,M\,v_G^2 + \dfrac{1}{2}\,J_G\,\omega^2$.

::: formule Problème à deux corps : masse réduite
$$\mu = \dfrac{m_1\,m_2}{m_1 + m_2} \qquad \mu\,\dfrac{\mathrm{d}^2\vec{r}}{\mathrm{d}t^2} = \vec{F}_{1 \to 2}$$
:::

Avec $\vec{r} = \overrightarrow{M_1M_2}$, le problème se ramène au mouvement d’un seul point de masse $\mu$. Pour l’atome d’hydrogène, $\mu \approx 0{,}9995\,m_e$ : le proton peut être considéré comme fixe.

## XII. Mécanique analytique : Lagrange et Hamilton {Supérieur}

*Licence et master.*

Le système est décrit par des **coordonnées généralisées** $q_i$, une par degré de liberté, et leurs dérivées $\dot{q}_i$.

::: formule Lagrangien et équations de Lagrange
$$\mathcal{L} = T - V \qquad \dfrac{\mathrm{d}}{\mathrm{d}t}\left(\dfrac{\partial \mathcal{L}}{\partial \dot{q}_i}\right) - \dfrac{\partial \mathcal{L}}{\partial q_i} = 0$$
:::

$T$ est l’énergie cinétique et $V$ l’énergie potentielle. Le **moment conjugué** vaut $p_i = \dfrac{\partial \mathcal{L}}{\partial \dot{q}_i}$.

::: retenir Lois de conservation (théorème de Noether)
- Si $\mathcal{L}$ ne dépend pas de $q_i$ (coordonnée **cyclique**), le moment conjugué $p_i$ se conserve.
- Si $\mathcal{L}$ ne dépend pas explicitement du temps, le hamiltonien $H$ se conserve.
:::

::: formule Hamiltonien et équations de Hamilton
$$\begin{aligned}
H &= \sum_i p_i\,\dot{q}_i - \mathcal{L} \\
\dot{q}_i &= \dfrac{\partial H}{\partial p_i} \qquad \dot{p}_i = -\dfrac{\partial H}{\partial q_i}
\end{aligned}$$
:::

Pour un système dont les liaisons ne dépendent pas du temps, $H = T + V$ est l’énergie mécanique. L’évolution d’une grandeur $f(q, p, t)$ s’écrit avec le crochet de Poisson : $\dfrac{\mathrm{d}f}{\mathrm{d}t} = \{f, H\} + \dfrac{\partial f}{\partial t}$.

::: exemple Le pendule simple
$\mathcal{L} = \dfrac{1}{2}\,m\,\ell^2\,\dot{\theta}^2 + m\,g\,\ell\cos\theta$. L’équation de Lagrange donne $m\,\ell^2\,\ddot{\theta} + m\,g\,\ell\sin\theta = 0$, c’est-à-dire $\ddot{\theta} + \dfrac{g}{\ell}\sin\theta = 0$. Le moment conjugué vaut $p_\theta = m\,\ell^2\,\dot{\theta}$, et $H = \dfrac{p_\theta^2}{2\,m\,\ell^2} - m\,g\,\ell\cos\theta$.
:::

::: exemple Force centrale et loi des aires
En polaires, $\mathcal{L} = \dfrac{1}{2}\,m\,(\dot{r}^2 + r^2\dot{\theta}^2) - E_p(r)$ ne dépend pas de $\theta$ : $p_\theta = m\,r^2\,\dot{\theta}$ se conserve. C’est le moment cinétique, et l’on retrouve la loi des aires de la partie VII.
:::
