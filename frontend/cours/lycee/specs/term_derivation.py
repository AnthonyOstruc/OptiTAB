# -*- coding: utf-8 -*-
"""Terminale — Dérivation : composée, dérivée seconde, convexité (notion 87)."""
NIVEAU = "Terminale"
COURS_ID = 88
FICHE_ID = 32

ENTETE = r"""
<div style="background:#e8f4fd; border:2px solid #3498db; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🎯 Objectifs du chapitre :</strong> dériver une fonction composée, calculer et interpréter une dérivée seconde, étudier la convexité d’une fonction et déterminer ses points d’inflexion, puis utiliser ces outils pour esquisser une courbe ou démontrer une inégalité.</p>
</div>
<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0;"><strong>📚 Au programme de Terminale :</strong> les sections <strong>I à IV</strong> (dérivée d’une composée, dérivée seconde, convexité, points d’inflexion) forment le cœur du programme. La section <strong>0</strong> rappelle les dérivées de Première, à maîtriser avant de commencer.</p>
<p style="margin:8px 0 0 0;">🌟 <strong>Approfondissements :</strong> les parties marquées « 🌟 Bonus » et la section VI sont utiles mais ne sont pas strictement exigibles au Bac.</p>
</div>
"""

ROLES = {"inégalité arithmético": "def"}

FIGURES = [
    dict(fichier="term_derivation_tangente.png", ancre="<strong>Rappel - Tangente à une courbe</strong>"),
    dict(fichier="term_derivation_composee.png", ancre="<strong>Théorème - Dérivée d'une fonction composée</strong>"),
    dict(fichier="term_derivation_convexite.png", ancre="<strong>Théorème - Caractérisation de la concavité</strong>"),
    dict(fichier="term_derivation_inflexion.png", ancre="<strong>Théorème - Condition pour un point d'inflexion</strong>"),
    dict(fichier="term_derivation_exemple.png", ancre=r"$\displaystyle I_1(-1, -1)$ et $\displaystyle I_2(1, -1)$"),
    dict(fichier="term_derivation_lorenz.png", ancre="🌟 Bonus - Courbe de Lorenz</h3>", mode="fin_carte"),
]

AJOUTS = [
    dict(ancre="<strong>Théorème - Condition pour un point d'inflexion</strong>", html=r"""
<div style="background:#fff8dc; border-left:6px solid #ffa500; border-radius:6px; padding:15px; margin:12px 0;">
<p style="margin:0;"><strong>⚠️ Attention :</strong> $\displaystyle f''(a)=0$ ne suffit pas ! Pour $\displaystyle f(x)=x^4$, on a $\displaystyle f''(0)=0$ mais $\displaystyle f''(x)=12x^2\ge 0$ ne change pas de signe : la courbe reste convexe et l’origine n’est <strong>pas</strong> un point d’inflexion. Il faut que $\displaystyle f''$ <strong>s’annule en changeant de signe</strong>.</p>
</div>"""),
]

ESSENTIEL = r"""
<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin:20px 0 0 0;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🏆 L’essentiel :</strong> $\displaystyle (v\circ u)'=(v'\circ u)\times u'$, donc $\displaystyle (e^u)'=u'e^u$, $\displaystyle (\ln u)'=\frac{u'}{u}$, $\displaystyle (u^n)'=nu'u^{n-1}$, $\displaystyle (\sqrt{u})'=\frac{u'}{2\sqrt{u}}$ ; $\displaystyle f''=(f')'$ ; $\displaystyle f''\ge 0$ sur $\displaystyle I$ $\displaystyle \iff$ $\displaystyle f'$ croissante $\displaystyle \iff$ $\displaystyle f$ convexe (courbe au-dessus de ses tangentes) ; $\displaystyle f''\le 0$ : concave ; point d’inflexion là où $\displaystyle f''$ s’annule <strong>en changeant de signe</strong> (la courbe traverse sa tangente). Fiche de synthèse dans l’onglet Fiches !</p>
</div>
"""

FICHE_IMAGES = ["term_derivation_composee.png", "term_derivation_convexite.png"]

FICHE = r"""
<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">

<div style="background:#e8f4fd; border:2px solid #3498db; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>📚 Objectif pédagogique :</strong> retenir l’essentiel : la dérivée d’une composée, la dérivée seconde, la convexité et les points d’inflexion. Programme de Terminale.</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Dériver une composée</h2>

<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
<div style="background:#e8f4fd; border:3px solid #3498db; border-radius:8px; padding:12px; margin:12px auto; text-align:center; max-width:460px;">
<p style="margin:0; font-weight:bold;">$\displaystyle \big(v(u(x))\big)'=v'(u(x))\times u'(x)$</p>
</div>
[IMAGE_1]
<p style="margin:0;">• $\displaystyle (e^{u})'=u'e^{u}$ ; $\displaystyle (\ln u)'=\frac{u'}{u}$ ($\displaystyle u>0$) ; $\displaystyle (\sqrt{u})'=\frac{u'}{2\sqrt{u}}$ ($\displaystyle u>0$).</p>
<p style="margin:6px 0 0 0;">• $\displaystyle (u^n)'=n\,u'\,u^{n-1}$ ; $\displaystyle \big(\sin u\big)'=u'\cos u$ ; $\displaystyle \big(\cos u\big)'=-u'\sin u$.</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Convexité et points d’inflexion</h2>

<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
[IMAGE_2]
<p style="margin:0;">1️⃣ $\displaystyle f''\ge 0$ sur $\displaystyle I$ $\displaystyle \iff$ $\displaystyle f'$ croissante $\displaystyle \iff$ $\displaystyle f$ <strong>convexe</strong> : courbe au-dessus de ses tangentes (forme ∪).</p>
<p style="margin:6px 0 0 0;">2️⃣ $\displaystyle f''\le 0$ sur $\displaystyle I$ $\displaystyle \iff$ $\displaystyle f'$ décroissante $\displaystyle \iff$ $\displaystyle f$ <strong>concave</strong> : courbe en dessous de ses tangentes (forme ∩).</p>
<p style="margin:6px 0 0 0;">3️⃣ <strong>Point d’inflexion</strong> en $\displaystyle a$ : $\displaystyle f''$ s’annule <strong>et change de signe</strong> ; la courbe traverse sa tangente.</p>
<p style="margin:6px 0 0 0;">4️⃣ Méthode : calculer $\displaystyle f''$, résoudre $\displaystyle f''(x)=0$, dresser le tableau de signe de $\displaystyle f''$.</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Les pièges à éviter</h2>

<div style="background:#fff8dc; border-radius:6px; border-left:6px solid #ffa500; padding:15px; margin:12px 0;">
<p style="margin:0;"><strong>⚠️ Les 4 erreurs classiques :</strong></p>
<p style="margin:6px 0 0 0;">1️⃣ Oublier de multiplier par $\displaystyle u'$ : $\displaystyle (e^{3x})'=3e^{3x}$, pas $\displaystyle e^{3x}$.</p>
<p style="margin:6px 0 0 0;">2️⃣ Écrire $\displaystyle (uv)'=u'v'$ : c’est $\displaystyle u'v+uv'$.</p>
<p style="margin:6px 0 0 0;">3️⃣ Conclure à un point d’inflexion dès que $\displaystyle f''(a)=0$ ($\displaystyle x^4$ en $\displaystyle 0$ est un contre-exemple).</p>
<p style="margin:6px 0 0 0;">4️⃣ Confondre convexe et croissante : $\displaystyle x\mapsto e^{-x}$ est convexe et décroissante.</p>
</div>

<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin:20px 0 0 0;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🏆 Réflexe :</strong> composée → « dérivée de l’extérieur (en gardant l’intérieur) × dérivée de l’intérieur » ; convexité → signe de $\displaystyle f''$ ; inflexion → $\displaystyle f''$ s’annule en changeant de signe.</p>
</div>

</div>
"""
