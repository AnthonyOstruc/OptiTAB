# -*- coding: utf-8 -*-
"""Première — Équations, fonctions polynômes du second degré (notion 154)."""
NIVEAU = "Première"
COURS_ID = 154
FICHE_ID = 71

ENTETE = r"""
<div style="background:#e8f4fd; border:2px solid #3498db; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🎯 Objectifs du chapitre :</strong> reconnaître une fonction polynôme du second degré et ses trois formes, utiliser le discriminant pour résoudre une équation du second degré, factoriser, étudier le signe d’un trinôme, choisir la forme la plus adaptée et résoudre des problèmes (optimisation, équation à paramètre).</p>
</div>
<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0;"><strong>📚 Au programme de Première :</strong> les sections <strong>I à VIII</strong> ainsi que la <strong>démonstration</strong> de la résolution de l’équation du second degré sont <strong>exigibles</strong> : ces connaissances sont nécessaires pour les évaluations.</p>
<p style="margin:8px 0 0 0;">🌟 <strong>Approfondissements et culture :</strong> la section IX (polynôme du troisième degré, factorisations particulières) est un <strong>bonus</strong> ; elle enrichit ta culture mathématique mais n’est pas strictement exigible.</p>
</div>
"""

ROLES = {"les trois formes": "def", "cas 1 :": "def", "cas 2 :": "def", "cas 3 :": "def"}

FIGURES = [
    dict(fichier="1er_second_degre_formes.png", ancre="<strong>Les trois formes d'un polynôme du second degré :</strong>"),
    dict(fichier="1er_second_degre_discriminant.png",
         ancre="<strong>Propriété - Nombre de racines selon le discriminant :</strong>"),
    dict(fichier="1er_second_degre_signe.png", ancre="<strong>Exemple 1 - Signe avec forme factorisée :</strong>"),
    dict(fichier="1er_second_degre_projectile.png", ancre=r"vaut $\displaystyle h(2) = 30$ m"),
]

AJOUTS = [
    dict(ancre="<strong>Exemple 1 - Signe avec forme factorisée :</strong>", mode="avant_bloc", html=r"""
<div style="background:#ecfdf5; border-left:6px solid #10b981; border-radius:6px; padding:15px; margin:12px 0;">
<p style="margin:0;"><strong>💡 Lecture graphique :</strong> le signe de $\displaystyle f(x)$ se lit sur la parabole : $\displaystyle f(x)>0$ quand la courbe est <strong>au-dessus</strong> de l’axe des abscisses, $\displaystyle f(x)<0$ quand elle est <strong>en dessous</strong>. Pour $\displaystyle a>0$, la parabole « sourit » : elle passe sous l’axe <strong>entre</strong> les racines.</p>
</div>"""),
]

ESSENTIEL = r"""
<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin:20px 0 0 0;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🏆 L’essentiel :</strong> $\displaystyle f(x)=ax^2+bx+c$ avec $\displaystyle a\neq 0$ ; $\displaystyle \Delta=b^2-4ac$ ; si $\displaystyle \Delta>0$, deux racines $\displaystyle x_{1,2}=\frac{-b\mp\sqrt{\Delta}}{2a}$ et $\displaystyle f(x)=a(x-x_1)(x-x_2)$ ; si $\displaystyle \Delta=0$, une racine double $\displaystyle -\frac{b}{2a}$ ; si $\displaystyle \Delta<0$, aucune racine réelle ; sommet $\displaystyle S(\alpha\,;\beta)$ avec $\displaystyle \alpha=-\frac{b}{2a}$ et $\displaystyle \beta=f(\alpha)$ ; $\displaystyle f(x)$ est du signe de $\displaystyle a$, sauf entre les racines ; forme développée pour calculer, canonique pour l’extremum, factorisée pour les équations et le signe. Fiche de synthèse dans l’onglet Fiches !</p>
</div>
"""

FICHE_IMAGES = ["1er_second_degre_formes.png", "1er_second_degre_discriminant.png"]

FICHE = r"""
<div style="background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;">

<div style="background:#e8f4fd; border:2px solid #3498db; border-radius:8px; padding:15px; margin-bottom:20px;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>📚 Objectif pédagogique :</strong> retenir l’essentiel : les trois formes d’un trinôme, le discriminant, les racines et le signe. Programme de Première.</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">I. Les trois formes d’un trinôme</h2>

<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
<div style="background:#e8f4fd; border:3px solid #3498db; border-radius:8px; padding:12px; margin:12px auto; text-align:center; max-width:520px;">
<p style="margin:0; font-weight:bold;">$\displaystyle ax^2+bx+c \;=\; a(x-\alpha)^2+\beta \;=\; a(x-x_1)(x-x_2)$</p>
</div>
[IMAGE_1]
<p style="margin:0;">• <strong>Développée</strong> : calculer une image ; $\displaystyle f(0)=c$.</p>
<p style="margin:6px 0 0 0;">• <strong>Canonique</strong> : sommet $\displaystyle S(\alpha\,;\beta)$ avec $\displaystyle \alpha=-\frac{b}{2a}$, $\displaystyle \beta=f(\alpha)$ → extremum et variations.</p>
<p style="margin:6px 0 0 0;">• <strong>Factorisée</strong> : racines $\displaystyle x_1$ et $\displaystyle x_2$ → équations et signe.</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">II. Discriminant, racines et signe</h2>

<div style="background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;">
<div style="background:#e8f4fd; border:3px solid #3498db; border-radius:8px; padding:12px; margin:12px auto; text-align:center; max-width:460px;">
<p style="margin:0; font-weight:bold;">$\displaystyle \Delta=b^2-4ac$</p>
</div>
[IMAGE_2]
<p style="margin:0;">1️⃣ $\displaystyle \Delta>0$ : $\displaystyle x_1=\frac{-b-\sqrt{\Delta}}{2a}$ et $\displaystyle x_2=\frac{-b+\sqrt{\Delta}}{2a}$.</p>
<p style="margin:6px 0 0 0;">2️⃣ $\displaystyle \Delta=0$ : une racine double $\displaystyle x_0=-\frac{b}{2a}$ ; $\displaystyle \Delta<0$ : aucune racine réelle.</p>
<p style="margin:6px 0 0 0;">3️⃣ Signe : $\displaystyle f(x)$ a le signe de $\displaystyle a$ partout, sauf <strong>entre</strong> les racines.</p>
<p style="margin:6px 0 0 0;">4️⃣ Contrôle : $\displaystyle x_1+x_2=-\frac{b}{a}$ et $\displaystyle x_1x_2=\frac{c}{a}$.</p>
</div>

<h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">III. Les pièges à éviter</h2>

<div style="background:#fff8dc; border-radius:6px; border-left:6px solid #ffa500; padding:15px; margin:12px 0;">
<p style="margin:0;"><strong>⚠️ Les 4 erreurs classiques :</strong></p>
<p style="margin:6px 0 0 0;">1️⃣ Oublier le coefficient $\displaystyle a$ dans la forme factorisée : $\displaystyle 2x^2+4x-6=2(x-1)(x+3)$, pas $\displaystyle (x-1)(x+3)$.</p>
<p style="margin:6px 0 0 0;">2️⃣ Mal calculer $\displaystyle b^2$ quand $\displaystyle b<0$ : $\displaystyle (-5)^2=25$, pas $\displaystyle -25$.</p>
<p style="margin:6px 0 0 0;">3️⃣ Conclure « aucune racine » quand $\displaystyle \Delta=0$ : il y a une racine double.</p>
<p style="margin:6px 0 0 0;">4️⃣ Se tromper de signe : pour $\displaystyle a>0$, le trinôme est <strong>négatif entre</strong> les racines.</p>
</div>

<div style="background:#ecfdf5; border:2px solid #10b981; border-radius:8px; padding:15px; margin:20px 0 0 0;">
<p style="margin:0; font-size:1.05em; color:#2c3e50;"><strong>🏆 Réflexe :</strong> équation $\displaystyle ax^2+bx+c=0$ → racine évidente ou $\displaystyle \Delta$ ; inéquation → forme factorisée et signe de $\displaystyle a$ ; maximum ou minimum → forme canonique (sommet).</p>
</div>

</div>
"""
