---
{
  "slug": "electrocinetique",
  "titre": "Électrocinétique : le formulaire de prépa",
  "titreCourt": "Électrocinétique",
  "titreSeo": "Formulaire d’électrocinétique : prépa et école d’ingénieur",
  "description": "Formulaire d’électrocinétique de prépa : Kirchhoff, ponts diviseurs, Thévenin, Norton, Millman, RC, RL, RLC, impédances complexes, résonance, filtres et Bode.",
  "chapo": "Toutes les formules d’électrocinétique de prépa et de première année d’école d’ingénieur, classées dans l’ordre du cours : lois de Kirchhoff, dipôles, théorèmes, régimes transitoires, régime sinusoïdal, résonance et filtres. Avec les schémas, les conditions d’application et les erreurs à éviter.",
  "resume": "Kirchhoff, Thévenin, RLC, impédances, résonance, filtres, Bode",
  "vignette": "bode_passe_bas",
  "theme": "Électricité",
  "niveaux": ["Supérieur"],
  "ordre": 11,
  "publie": "2026-11-18",
  "modifie": "2026-11-18",
  "motsCles": ["formulaire électrocinétique", "électrocinétique prépa", "pont diviseur de tension", "pont diviseur de courant", "théorème de Thévenin", "modèle de Norton", "théorème de Millman", "impédance complexe", "impédance d'une bobine", "impédance d'un condensateur", "circuit RLC", "facteur de qualité", "résonance", "filtre passe-bas", "diagramme de Bode", "fréquence de coupure"],
  "figures": [
    { "nom": "ponts_diviseurs", "alt": "À gauche, un diviseur de tension : deux résistances R1 et R2 en série soumises à la tension u, la tension de sortie u2 est prise aux bornes de R2. À droite, un diviseur de courant : le courant i se partage entre R1 (courant i1) et R2 (courant i2) en parallèle." },
    { "nom": "thevenin_norton", "alt": "À gauche, le modèle de Thévenin : une source idéale de tension Eth en série avec une résistance Rth, entre les bornes A et B. À droite, le modèle de Norton : une source idéale de courant IN en parallèle avec une résistance RN." },
    { "nom": "rlc_regimes", "alt": "Réponse d’un circuit RLC série à un échelon de tension : pour Q = 5, la tension uC/E oscille autour de 1 en s’amortissant ; pour Q = 1/2, elle rejoint 1 le plus vite sans dépasser ; pour Q = 0,2, elle rejoint 1 lentement sans osciller." },
    { "nom": "bode_passe_bas", "alt": "Diagramme de Bode en gain d’un filtre passe-bas du premier ordre : le gain vaut 0 dB à basse fréquence, −3 dB à la pulsation de coupure, puis décroît de 20 dB par décade. Les asymptotes sont tracées en pointillés." }
  ],
  "liees": [
    "physique-chimie/lois-de-l-electricite",
    "formulaires/nombres-complexes",
    "formulaires/equations-differentielles"
  ],
  "faq": [
    ["Quelle est l’impédance d’une bobine et d’un condensateur ?", "En régime sinusoïdal de pulsation ω, l’impédance d’une bobine d’inductance L vaut ZL = jLω et celle d’un condensateur de capacité C vaut ZC = 1/(jCω). À basse fréquence, la bobine se comporte comme un fil et le condensateur comme un interrupteur ouvert ; à haute fréquence, c’est l’inverse."],
    ["Comment calculer la fréquence de coupure d’un filtre RC ?", "Pour un filtre RC du premier ordre, la pulsation de coupure vaut ωc = 1/(RC) et la fréquence de coupure fc = 1/(2πRC). Avec R = 1 kΩ et C = 100 nF, ωc = 10⁴ rad/s et fc ≈ 1,6 kHz. À cette fréquence, le gain vaut −3 dB."],
    ["Que vaut le facteur de qualité d’un circuit RLC série ?", "Q = (1/R)√(L/C) = Lω0/R, avec ω0 = 1/√(LC). Si Q > 1/2, le régime libre est pseudo-périodique ; si Q = 1/2, il est critique ; si Q < 1/2, il est apériodique. En régime forcé, la bande passante de la résonance en intensité vaut Δω = ω0/Q."],
    ["Comment trouver le modèle de Thévenin d’un circuit ?", "La force électromotrice Eth est la tension entre les deux bornes à vide (aucun courant débité). La résistance Rth est la résistance vue entre les bornes quand on éteint les sources : une source de tension devient un fil, une source de courant un interrupteur ouvert. Le modèle de Norton équivalent a pour courant IN = Eth/Rth et pour résistance RN = Rth."],
    ["Qu’est-ce que le théorème de Millman ?", "C’est la loi des nœuds écrite avec les potentiels. Pour un nœud A relié par des résistances Rk à des points de potentiels Vk : VA = (Σ Vk/Rk) / (Σ 1/Rk). Il donne directement le potentiel d’un nœud sans écrire toutes les équations."],
    ["Quand peut-on utiliser un pont diviseur de tension ?", "Seulement si les deux résistances sont parcourues par le même courant, c’est-à-dire si l’on ne prélève aucun courant à la sortie (sortie à vide). Alors u2 = R2/(R1 + R2) × u. Si une charge est branchée en sortie, il faut l’inclure dans R2."]
  ]
}
---
<!-- optitab:1 -->
::: conseil Comment lire ce formulaire
Les grandeurs variables sont en minuscules ($u$, $i$), les grandeurs constantes en majuscules ($E$, $R$). Toutes les relations sont écrites en **convention récepteur**, sauf mention contraire. Pour les bases (loi d’Ohm, série, dérivation, puissance), voir la page sur les lois de l’électricité, en lien en bas de page.
:::

## I. Conventions et lois de Kirchhoff {Supérieur}

::: definition Approximation des régimes quasi stationnaires (ARQS)
Les lois de l’électrocinétique supposent que la taille du circuit est très petite devant la longueur d’onde $\lambda = \dfrac{c}{f}$ des signaux. L’intensité est alors la même en tout point d’une branche.
:::

| Convention | Flèches de $u$ et de $i$ | Le produit $p = u\,i$ est… |
|---|---|---|
| Récepteur | de sens opposés | la puissance reçue par le dipôle |
| Générateur | de même sens | la puissance fournie par le dipôle |

::: formule Loi des nœuds
$$\sum_k \varepsilon_k\, i_k = 0 \qquad (\varepsilon_k = +1 \text{ si le courant arrive}, -1 \text{ s'il part})$$
:::

::: formule Loi des mailles
$$\sum_k \varepsilon_k\, u_k = 0 \qquad (\varepsilon_k = \pm 1 \text{ selon le sens de parcours})$$
:::

## II. Les dipôles usuels {Supérieur}

| Dipôle | Relation $u$, $i$ | Énergie |
|---|---|---|
| Résistor $R$ | $u = R\,i$ | dissipe $R\,i^2$ |
| Condensateur $C$ | $i = C\,\dfrac{\mathrm{d}u}{\mathrm{d}t}$ | stocke $\dfrac{1}{2}\,C\,u^2$ |
| Bobine $L$ | $u = L\,\dfrac{\mathrm{d}i}{\mathrm{d}t}$ | stocke $\dfrac{1}{2}\,L\,i^2$ |

La tension aux bornes d’un condensateur et l’intensité qui traverse une bobine sont **continues** : elles ne peuvent pas sauter brusquement.

::: retenir En régime permanent continu
- Un condensateur se comporte comme un **interrupteur ouvert** ($i = 0$).
- Une bobine se comporte comme un **fil** ($u = 0$).
:::

## III. Les associations de dipôles {Supérieur}

| En série | Dipôle équivalent |
|---|---|
| Résistances | $R = R_1 + R_2$ |
| Bobines | $L = L_1 + L_2$ |
| Condensateurs | $\dfrac{1}{C} = \dfrac{1}{C_1} + \dfrac{1}{C_2}$ |
| Impédances | $\underline{Z} = \underline{Z}_1 + \underline{Z}_2$ |

| En parallèle | Dipôle équivalent |
|---|---|
| Résistances | $\dfrac{1}{R} = \dfrac{1}{R_1} + \dfrac{1}{R_2}$ |
| Bobines | $\dfrac{1}{L} = \dfrac{1}{L_1} + \dfrac{1}{L_2}$ |
| Condensateurs | $C = C_1 + C_2$ |
| Impédances | $\dfrac{1}{\underline{Z}} = \dfrac{1}{\underline{Z}_1} + \dfrac{1}{\underline{Z}_2}$ |

::: attention Les condensateurs font l’inverse
Les condensateurs s’associent à l’inverse des résistances : leurs capacités s’ajoutent en parallèle, et ce sont leurs inverses qui s’ajoutent en série.
:::

## IV. Les ponts diviseurs {Supérieur}

[IMAGE_1]

::: formule Diviseur de tension (même courant dans R₁ et R₂)
$$u_2 = \dfrac{R_2}{R_1 + R_2}\,u$$
:::

::: formule Diviseur de courant (deux branches en parallèle)
$$i_1 = \dfrac{R_2}{R_1 + R_2}\,i = \dfrac{G_1}{G_1 + G_2}\,i \qquad \left(G = \dfrac{1}{R}\right)$$
:::

::: exemple
- Tension : $u = 12$ V, $R_1 = 1$ kΩ, $R_2 = 2$ kΩ, d’où $u_2 = \dfrac{2}{3} \times 12 = 8$ V.
- Courant : $i = 30$ mA, $R_1 = 100$ Ω, $R_2 = 200$ Ω, d’où $i_1 = \dfrac{200}{300} \times 30 = 20$ mA. Le courant passe davantage par la plus petite résistance.
:::

::: attention Sortie à vide
Le diviseur de tension n’est valable que si l’on ne prélève aucun courant en sortie. Si une charge est branchée aux bornes de $R_2$, on remplace $R_2$ par l’association de $R_2$ et de la charge en parallèle.
:::

## V. Thévenin, Norton et Millman {Supérieur}

[IMAGE_2]

::: formule Modèle de Thévenin (convention générateur)
$$u = E_{\mathrm{th}} - R_{\mathrm{th}}\,i$$
:::

::: formule Modèle de Norton (convention générateur)
$$i = I_{\mathrm{N}} - \dfrac{u}{R_{\mathrm{N}}}$$
:::

| Équivalence | Thévenin vers Norton |
|---|---|
| Résistance | $R_{\mathrm{N}} = R_{\mathrm{th}}$ |
| Source | $I_{\mathrm{N}} = \dfrac{E_{\mathrm{th}}}{R_{\mathrm{th}}}$ |

::: methode Trouver le modèle équivalent
1. $E_{\mathrm{th}}$ est la tension entre les bornes à vide ($i = 0$) ; $I_{\mathrm{N}}$ est le courant de court-circuit.
2. $R_{\mathrm{th}}$ est la résistance vue entre les bornes, sources éteintes : une source de tension devient un fil, une source de courant un interrupteur ouvert.
:::

::: formule Théorème de Millman (loi des nœuds en potentiels)
$$V_A = \dfrac{\displaystyle\sum_k \dfrac{V_k}{R_k}}{\displaystyle\sum_k \dfrac{1}{R_k}}$$
:::

::: exemple
Un nœud A est relié à $V_1 = 10$ V par 1 kΩ, à la masse ($V_2 = 0$) par 1 kΩ et à $V_3 = 4$ V par 2 kΩ. Avec les résistances en kΩ :
$$V_A = \dfrac{10/1 + 0/1 + 4/2}{1/1 + 1/1 + 1/2} = \dfrac{12}{2{,}5} = 4{,}8\ \mathrm{V}$$
:::

## VI. Les circuits du premier ordre : RC et RL {Supérieur}

::: formule Circuit RC série soumis à un échelon E (τ = RC)
$$\tau\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t} + u_C = E$$
:::

::: formule Circuit RL série soumis à un échelon E (τ = L/R)
$$\tau\,\dfrac{\mathrm{d}i}{\mathrm{d}t} + i = \dfrac{E}{R}$$
:::

On écrit l’équation pour la grandeur continue : $u_C$ pour le circuit RC, $i$ pour le circuit RL.

::: formule Solution pour une grandeur $x$ (valeur initiale $x_0$, valeur finale $x_\infty$)
$$x(t) = x_\infty + \left(x_0 - x_\infty\right)\mathrm{e}^{-t/\tau}$$
:::

::: retenir
- Le temps de réponse à 5 % vaut $3\tau$ (car $\mathrm{e}^{-3} \approx 0{,}05$).
- À la charge d’un condensateur sous $E$ à travers $R$, le générateur fournit $C E^2$ : la moitié, $\dfrac{1}{2} C E^2$, est stockée dans le condensateur et l’autre moitié dissipée dans la résistance, quelle que soit la valeur de $R$.
:::

## VII. Le circuit RLC série en régime transitoire {Supérieur}

::: formule Forme canonique (réponse à un échelon $E$)
$$\dfrac{\mathrm{d}^2 u_C}{\mathrm{d}t^2} + \dfrac{\omega_0}{Q}\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t} + \omega_0^2\,u_C = \omega_0^2\,E$$
:::

| Grandeur | Expression |
|---|---|
| Pulsation propre | $\omega_0 = \dfrac{1}{\sqrt{LC}}$ |
| Facteur de qualité | $Q = \dfrac{1}{R}\sqrt{\dfrac{L}{C}} = \dfrac{L\,\omega_0}{R} = \dfrac{1}{R\,C\,\omega_0}$ |

[IMAGE_3]

| Facteur de qualité | Régime | Allure |
|---|---|---|
| $Q > \dfrac{1}{2}$ | pseudo-périodique | oscillations amorties, pseudo-pulsation $\omega = \omega_0\sqrt{1 - \dfrac{1}{4Q^2}}$ |
| $Q = \dfrac{1}{2}$ | critique | retour le plus rapide sans dépassement |
| $Q < \dfrac{1}{2}$ | apériodique | retour lent, sans oscillation |

::: remarque
En régime pseudo-périodique, on voit à peu près $Q$ oscillations avant l’amortissement. L’énergie $\dfrac{1}{2} L i^2 + \dfrac{1}{2} C u_C^2$ diminue au cours du temps : elle est dissipée dans la résistance, à la puissance $R\,i^2$.
:::

## VIII. Le régime sinusoïdal forcé {Supérieur}

::: definition Notation complexe
À $u(t) = U_m \cos(\omega t + \varphi)$, on associe $\underline{u} = U_m\,\mathrm{e}^{j(\omega t + \varphi)}$ et l’amplitude complexe $\underline{U}_m = U_m\,\mathrm{e}^{j\varphi}$. Dériver par rapport au temps revient à multiplier par $j\omega$.
:::

| Dipôle | Impédance $\underline{Z}$ | Avance de $u$ sur $i$ |
|---|---|---|
| Résistor | $R$ | $0$ |
| Bobine | $jL\omega$ | $+\dfrac{\pi}{2}$ |
| Condensateur | $\dfrac{1}{jC\omega}$ | $-\dfrac{\pi}{2}$ |

| Dipôle | Basse fréquence | Haute fréquence |
|---|---|---|
| Bobine | fil | interrupteur ouvert |
| Condensateur | interrupteur ouvert | fil |

::: formule Loi d’Ohm complexe
$$\underline{U} = \underline{Z}\,\underline{I} \qquad |\underline{Z}| = \dfrac{U_m}{I_m} \qquad \arg \underline{Z} = \varphi_u - \varphi_i$$
:::

::: formule Puissance moyenne reçue
$$P = U_{\mathrm{eff}}\,I_{\mathrm{eff}} \cos\varphi \qquad U_{\mathrm{eff}} = \dfrac{U_m}{\sqrt{2}}$$
:::

Une résistance reçoit $P = R\,I_{\mathrm{eff}}^2$ ; une bobine ou un condensateur idéal reçoit une puissance moyenne nulle. Le secteur délivre 230 V efficaces à 50 Hz, soit une amplitude $U_m = 230\sqrt{2} \approx 325$ V.

## IX. La résonance du circuit RLC série {Supérieur}

Le circuit est alimenté par $e(t) = E_m \cos(\omega t)$ :

$$\underline{I} = \dfrac{\underline{E}}{R + j\left(L\omega - \dfrac{1}{C\omega}\right)}$$

::: retenir Résonance en intensité
Elle a **toujours** lieu, à $\omega = \omega_0$. L’amplitude maximale vaut $I_{m,\max} = \dfrac{E_m}{R}$ et la bande passante à $-3$ dB vaut $\Delta\omega = \dfrac{\omega_0}{Q}$ : plus $Q$ est grand, plus la résonance est aiguë.
:::

::: retenir Résonance en tension aux bornes du condensateur
Elle n’a lieu que si $Q > 1/\sqrt{2}$, à la pulsation
$$\omega_r = \omega_0\sqrt{1 - \dfrac{1}{2Q^2}}$$
légèrement inférieure à $\omega_0$. À $\omega_0$, l’amplitude vaut $U_{C,m} = Q\,E_m$.
:::

::: attention Surtension
À la résonance, la tension aux bornes du condensateur vaut environ $Q$ fois celle du générateur : avec $Q = 10$ et 5 V en entrée, on mesure environ 50 V aux bornes de $C$.
:::

## X. Les filtres et le diagramme de Bode {Supérieur}

::: definition Fonction de transfert
$\underline{H}(j\omega) = \underline{U}_s / \underline{U}_e$ (sortie à vide). Gain $G = |\underline{H}|$, gain en décibels $G_{\mathrm{dB}} = 20 \log G$, phase $\varphi = \arg \underline{H}$. La pulsation de coupure est celle où $G = G_{\max}/\sqrt{2}$, soit 3 dB sous le maximum.
:::

::: formule Passe-bas RC (sortie aux bornes de C)
$$\underline{H} = \dfrac{1}{1 + j\,\dfrac{\omega}{\omega_c}}$$
:::

::: formule Passe-haut RC (sortie aux bornes de R)
$$\underline{H} = \dfrac{j\,\dfrac{\omega}{\omega_c}}{1 + j\,\dfrac{\omega}{\omega_c}}$$
:::

::: formule Passe-bas du second ordre (RLC, sortie aux bornes de C)
$$\underline{H} = \dfrac{1}{1 - \left(\dfrac{\omega}{\omega_0}\right)^2 + j\,\dfrac{\omega}{Q\,\omega_0}}$$
:::

| Filtre | Gain : asymptotes | Phase |
|---|---|---|
| Passe-bas RC | 0 dB puis −20 dB/décade | de 0 à −π/2 |
| Passe-haut RC | +20 dB/décade puis 0 dB | de π/2 à 0 |
| Passe-bas RLC | 0 dB puis −40 dB/décade | de 0 à −π |

Pour les filtres RC : $\omega_c = \dfrac{1}{RC}$ et $f_c = \dfrac{\omega_c}{2\pi} = \dfrac{1}{2\pi RC}$.

[IMAGE_4]

::: exemple
Avec $R = 1$ kΩ et $C = 100$ nF : $\omega_c = 1/(10^{3} \times 10^{-7}) = 10^{4}$ rad/s, soit $f_c = 10^{4}/(2\pi) \approx 1{,}6$ kHz. À $f_c$, la phase du passe-bas vaut $-\dfrac{\pi}{4}$.
:::

::: retenir Intégrateur et dérivateur
- Bien au-dessus de sa coupure, le passe-bas du premier ordre se comporte en **intégrateur** : $\underline{H} \approx \dfrac{\omega_c}{j\omega}$.
- Bien en dessous de sa coupure, le passe-haut se comporte en **dérivateur** : $\underline{H} \approx \dfrac{j\omega}{\omega_c}$.
:::
