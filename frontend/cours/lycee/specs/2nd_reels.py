# -*- coding: utf-8 -*-
"""Seconde — Manipuler les nombres réels (notion 165)."""
NIVEAU = "Seconde"
COURS_ID = 160
FICHE_ID = 133

ENTETE = r"""
<div style="background:#e8f4fd; border:2px solid #3498db; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🎯 Objectifs du chapitre :</strong> situer un réel sur la droite numérique, lire et écrire des intervalles, utiliser la valeur absolue comme une distance, distinguer décimaux, rationnels et irrationnels, puis encadrer et arrondir un réel.</p>
<ul style="margin:10px 0 0 0; padding-left:20px; line-height:1.6;">
<li>Associer à chaque point de la droite graduée un <strong>unique</strong> nombre réel, et réciproquement.</li>
<li>Représenter un <strong>intervalle</strong> ; déterminer si un réel <strong>appartient</strong> à un intervalle.</li>
<li>Donner un <strong>encadrement</strong> (d’amplitude donnée) d’un réel par des décimaux.</li>
<li>Dans un problème, <strong>arrondir</strong> avec un nombre de chiffres significatifs adapté.</li>
</ul>
</div>
<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0;"><strong>📚 Au programme de Seconde :</strong> l’ensemble $\displaystyle \mathbb{R}$ et la droite numérique ; les intervalles (notations, inégalités, $\displaystyle +\infty$ et $\displaystyle -\infty$) ; la valeur absolue $\displaystyle |x|$ et la distance $\displaystyle |x-a|$ ; l’intervalle centré $\displaystyle [a-r\,;\,a+r]$ et la condition $\displaystyle |x-a|\le r$ ; les décimaux $\displaystyle \mathbb{D}$ et l’encadrement à $\displaystyle 10^{-n}$ près ; les rationnels $\displaystyle \mathbb{Q}$ et les irrationnels ($\displaystyle \sqrt{2}$, $\displaystyle \pi$).</p>
<p style="margin:8px 0 0 0;">🧠 <strong>Démonstrations à connaître</strong> (partie VII) : $\displaystyle \frac{1}{3}$ n’est pas décimal ; $\displaystyle \sqrt{2}$ est irrationnel.</p>
<p style="margin:8px 0 0 0;">🤖 <strong>Algorithme</strong> (partie VIII) : encadrer $\displaystyle \sqrt{2}$ par balayage, avec une amplitude $\displaystyle \le 10^{-n}$.</p>
<p style="margin:8px 0 0 0; color:#065f46;"><em>La valeur absolue est utilisée ici uniquement pour parler de <strong>distance</strong> (les autres usages sont hors programme).</em></p>
</div>
<p style="font-size:1em;">🌟 <strong>L’idée du chapitre :</strong> au cycle 4, tu as comparé des nombres avec des <strong>inégalités</strong>. En Seconde, on introduit la notion d’<strong>intervalle</strong> : c’est un ensemble de nombres qui vérifient une inégalité (par exemple « tous les réels entre 2 et 5 »). La valeur absolue sert à parler de <strong>distance</strong> sur la droite numérique.</p>
"""

ROLES = {"irrationnels": "def", "les ensembles à connaître": "def"}

FIGURES = [
    dict(fichier="2nd_reels_droite.png", ancre="<strong>Nombres réels</strong>"),
    dict(fichier="2nd_reels_ensembles.png", ancre="<strong>Les ensembles à connaître</strong>"),
    dict(fichier="2nd_reels_intervalles.png", ancre="<strong>Traductions à connaître</strong>"),
    dict(fichier="2nd_reels_distance.png", ancre="<strong>Distance entre deux réels</strong>"),
    dict(fichier="2nd_reels_centre.png", ancre=r"Centre $\displaystyle a=3$ et $\displaystyle r=2$ :"),
    dict(fichier="2nd_reels_encadrement.png", ancre=r"(car $\displaystyle 1{,}41^2\lt 2$"),
]

AJOUTS = [
    dict(ancre=r"Distance entre $\displaystyle -3$ et $\displaystyle 5$", html=r"""
<div style="background:#fff8dc; border-left:6px solid #ffa500; border-radius:6px; padding:15px; margin:12px 0;">
<p style="margin:0;"><strong>⚠️ Erreurs fréquentes :</strong></p>
<p style="margin:8px 0 0 0;">• Une valeur absolue n’est jamais négative : $\displaystyle |-7| = 7$, et non $\displaystyle -7$.</p>
<p style="margin:8px 0 0 0;">• L’ordre ne compte pas dans une distance : $\displaystyle |5-(-3)| = |-3-5| = 8$.</p>
<p style="margin:8px 0 0 0;">• En général $\displaystyle |a+b| \neq |a|+|b|$ : par exemple $\displaystyle |3+(-5)| = 2$ alors que $\displaystyle |3|+|-5| = 8$.</p>
</div>"""),
    dict(ancre="<strong>Irrationnels</strong>", html=r"""
<div style="background:#fff8dc; border-left:6px solid #ffa500; border-radius:6px; padding:15px; margin:12px 0;">
<p style="margin:0;"><strong>⚠️ Attention :</strong> une racine carrée n’est pas toujours irrationnelle ($\displaystyle \sqrt{4} = 2$, $\displaystyle \sqrt{0{,}25} = 0{,}5$), et une calculatrice qui affiche beaucoup de décimales ne prouve rien : $\displaystyle \frac{1}{7} = 0{,}142857142857\ldots$ est rationnel (période $\displaystyle 142857$).</p>
</div>"""),
]

ESSENTIEL = r"""
<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin:20px 0 0 0;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🏆 L’essentiel :</strong> $\displaystyle \mathbb{N}\subset\mathbb{Z}\subset\mathbb{D}\subset\mathbb{Q}\subset\mathbb{R}$ ; $\displaystyle x\in[a;b] \iff a\le x\le b$ (crochet ouvert = borne exclue, toujours ouvert du côté de $\displaystyle \pm\infty$) ; $\displaystyle |x-a|$ est la distance entre $\displaystyle x$ et $\displaystyle a$, et $\displaystyle x\in[a-r;a+r] \iff |x-a|\le r$ ; décimal = écriture finie, rationnel = finie ou périodique, irrationnel sinon ($\displaystyle \sqrt{2}$, $\displaystyle \pi$) ; encadrer à $\displaystyle 10^{-n}$ près = amplitude $\displaystyle \le 10^{-n}$. Fiche de synthèse dans l’onglet Fiches !</p>
</div>
"""

FICHE_IMAGES = ["2nd_reels_ensembles.png", "2nd_reels_intervalles.png"]

FICHE = r"""
<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">

<div style="background:#e8f4fd; border:2px solid #3498db; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>📚 Objectif pédagogique :</strong> retenir l’essentiel : les ensembles de nombres, les intervalles, la valeur absolue comme distance et l’encadrement d’un réel. Programme de Seconde.</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Les ensembles de nombres</h2>

<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
<div style="background:#e8f4fd; border:3px solid #3498db; border-radius:8px; padding:12px; margin:12px auto; text-align:center; max-width:460px;">
<p style="margin:0; font-weight:bold;">$\displaystyle \mathbb{N}\subset\mathbb{Z}\subset\mathbb{D}\subset\mathbb{Q}\subset\mathbb{R}$</p>
</div>
[IMAGE_1]
<p style="margin:0;">• <strong>Décimal</strong> : écriture décimale finie, $\displaystyle x = \frac{k}{10^n}$ ($\displaystyle 0{,}125 = \frac{125}{1000}$).</p>
<p style="margin:6px 0 0 0;">• <strong>Rationnel</strong> : $\displaystyle x = \frac{p}{q}$ ; écriture finie ou périodique ($\displaystyle \frac{1}{3} = 0{,}333\ldots$ n’est pas décimal).</p>
<p style="margin:6px 0 0 0;">• <strong>Irrationnel</strong> : pas une fraction, écriture infinie non périodique ($\displaystyle \sqrt{2}$, $\displaystyle \pi$).</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Intervalles et distances</h2>

<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
[IMAGE_2]
<p style="margin:0;">1️⃣ $\displaystyle x\in[a;b] \iff a\le x\le b$ ; $\displaystyle x\in\,]a;b[\, \iff a\lt x\lt b$ ; $\displaystyle x\in[a;+\infty[ \iff x\ge a$.</p>
<p style="margin:6px 0 0 0;">2️⃣ $\displaystyle |x|$ = distance de $\displaystyle x$ à $\displaystyle 0$ ; distance entre $\displaystyle a$ et $\displaystyle b$ : $\displaystyle |b-a|$.</p>
<p style="margin:6px 0 0 0;">3️⃣ $\displaystyle x\in[a-r\,;\,a+r] \iff |x-a|\le r$ : par exemple $\displaystyle |x-3|\le 2 \iff x\in[1;5]$.</p>
<p style="margin:6px 0 0 0;">4️⃣ Encadrer à $\displaystyle 10^{-n}$ près : $\displaystyle a\le x\le b$ avec $\displaystyle b-a\le 10^{-n}$ ($\displaystyle 1{,}41\le\sqrt{2}\le 1{,}42$).</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Les pièges à éviter</h2>

<div style="background:#fff8dc; border-radius:6px; border-left:6px solid #ffa500; padding:15px; margin:12px 0;">
<p style="margin:0;"><strong>⚠️ Les 4 erreurs classiques :</strong></p>
<p style="margin:6px 0 0 0;">1️⃣ Mettre un crochet fermé du côté de $\displaystyle +\infty$ : on écrit $\displaystyle [2;+\infty[$, jamais $\displaystyle [2;+\infty]$.</p>
<p style="margin:6px 0 0 0;">2️⃣ Confondre $\displaystyle ]2;5[$ et $\displaystyle [2;5]$ : avec un crochet ouvert, la borne n’appartient pas à l’intervalle.</p>
<p style="margin:6px 0 0 0;">3️⃣ Croire qu’une valeur absolue peut être négative : $\displaystyle |-7| = 7$.</p>
<p style="margin:6px 0 0 0;">4️⃣ Croire qu’un nombre est irrationnel parce que la calculatrice affiche beaucoup de décimales ($\displaystyle \frac{1}{7}$ est rationnel).</p>
</div>

<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin:20px 0 0 0;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🏆 Réflexe :</strong> une inégalité → je la dessine sur la droite graduée et je l’écris en intervalle ; une condition « $\displaystyle |x-a|\le r$ » → je lis « distance de $\displaystyle x$ à $\displaystyle a$ au plus $\displaystyle r$ » et j’écris $\displaystyle [a-r\,;\,a+r]$.</p>
</div>

</div>
"""
