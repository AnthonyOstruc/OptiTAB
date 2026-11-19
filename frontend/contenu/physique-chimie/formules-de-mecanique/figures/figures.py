# -*- coding: utf-8 -*-
"""Figures de la page « Formules de mécanique » (physique-chimie, lycée).

    PYTHONUTF8=1 python cours/format_v1/outils/figures_livre.py contenu/physique-chimie/formules-de-mecanique --planche --jobs 1

Toutes les positions sont CALCULÉES à partir des valeurs physiques (mêmes valeurs
que l'exemple de la page pour le tir : v0 = 10,0 m/s, α = 45°, g = 9,81 m/s²).
Conventions (consigne du propriétaire, rigueur des schémas) : vitesses en bleu
marine, forces et accélérations en orange, une couleur par force, chaque force
part de son point d'application (le centre de l'objet), texte jamais posé sur un trait.
"""
from math import atan2, cos, degrees, pi, radians, sin, sqrt

PREAMBULE_EXTRA = r"""
\tikzset{
  leg/.style={font=\otRegular\fontsize{9.5}{11.5}\selectfont,text=otInk,inner sep=1.4pt,align=center},
  legG/.style={leg,text=otMuted},
  legN/.style={leg,text=otNavy},
  legO/.style={leg,text=otOrange!80!black},
  legV/.style={leg,text=otGreenDark},
  pt/.style={circle,fill=otInk,inner sep=0pt,minimum size=4pt},
  vecN/.style={otNavy,line width=1.2pt,-{Stealth[length=2.6mm]}},
  vecO/.style={otOrange!85!black,line width=1.2pt,-{Stealth[length=2.6mm]}},
  vecV/.style={otGreenDark,line width=1.2pt,-{Stealth[length=2.6mm]}},
  vecG/.style={otMuted,line width=0.9pt,-{Stealth[length=2.3mm]}},
  axe/.style={otMuted,line width=0.6pt,-{Stealth[length=2.2mm]}},
  trajet/.style={otMuted!80,line width=0.6pt,dash pattern=on 2.5pt off 1.5pt},
  guide/.style={otMuted!70,line width=0.45pt,dash pattern=on 1.5pt off 1.5pt},
  cote/.style={otMuted,line width=0.55pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}},
}
"""

DEBUT, FIN = "\\begin{tikzpicture}\n", "\\end{tikzpicture}"
FIGURES = {}


def f(x):
    return f"{x:.3f}"


def P(x, y):
    return f"({f(x)},{f(y)})"


# ====================================================================== 1. chronophotographie
# Balle lancée avec v0 = (2,0 ; 3,0) m/s, une image toutes les τ = 0,10 s, g = 9,8 m/s².
# Échelles : 1 m → 5 cm ; 1 m/s → 0,6 cm.
def chronophotographie():
    tau, ech, ev, g = 0.1, 5.0, 0.36, 9.8   # flèches plus courtes que l'écart entre deux images
    vx, vz = 2.0, 3.0
    M = [(vx * k * tau * ech, (vz * k * tau - g / 2 * (k * tau) ** 2) * ech) for k in range(7)]
    s = DEBUT
    s += f"\\draw[trajet] plot[smooth] coordinates {{{' '.join(P(x, y) for x, y in M)}}};\n"
    places = {0: ("north west", 0.02, -0.12), 1: ("north west", 0.06, -0.12), 2: ("south east", -0.08, 0.06),
              3: ("south west", 0.08, 0.07), 4: ("south west", 0.08, 0.06), 5: ("north east", -0.06, -0.12), 6: ("north east", -0.06, -0.12)}
    for k, (x, y) in enumerate(M):
        s += f"\\node[pt] at {P(x, y)} {{}};\n"
        ancre, dx, dy = places[k]
        s += f"\\node[legG,anchor={ancre}] at {P(x + dx, y + dy)} {{$M_{k}$}};\n"
    v2 = (vx, vz - g * 2 * tau)
    v4 = (vx, vz - g * 4 * tau)
    (x2, y2), (x3, y3), (x4, y4) = M[2], M[3], M[4]
    s += f"\\draw[vecN] {P(x2, y2)} -- ++{P(v2[0] * ev, v2[1] * ev)} node[legN,anchor=south east] {{$\\vec{{v}}_2$}};\n"
    s += f"\\draw[vecN] {P(x4, y4)} -- ++{P(v4[0] * ev, v4[1] * ev)} node[legN,anchor=west] {{$\\vec{{v}}_4$}};\n"
    dv = (v4[0] - v2[0], v4[1] - v2[1])
    assert abs(dv[0]) < 1e-12 and dv[1] < 0          # Δv vertical, vers le bas, comme le poids
    s += f"\\draw[vecO] {P(x3, y3)} -- ++{P(dv[0] * ev, dv[1] * ev)} node[legO,anchor=north] {{$\\Delta\\vec{{v}} = \\vec{{v}}_4 - \\vec{{v}}_2$}};\n"
    return s + FIN


FIGURES["chronophotographie"] = chronophotographie()


# ====================================================================== 2. actions réciproques (gravitation)
def actions_reciproques():
    ra, rb, d, L = 0.85, 0.42, 4.4, 1.35
    s = DEBUT
    s += f"\\draw[otNavy!60,line width=0.9pt] (0,0) circle ({ra});\n"
    s += f"\\draw[otNavy!60,line width=0.9pt] ({d},0) circle ({rb});\n"
    s += f"\\node[legN,anchor=south east] at {P(-ra * 0.72, ra * 0.72)} {{$A$ ($m_A$)}};\n"
    s += f"\\node[legN,anchor=south west] at {P(d + rb * 0.72, rb * 0.72)} {{$B$ ($m_B$)}};\n"
    # forces : chacune part du centre de l'objet qui la subit, même longueur, sens opposés
    s += f"\\draw[vecV] (0,0) -- ({L},0);\n"
    s += f"\\node[legV,anchor=south] at {P(ra + (L - ra) / 2 + 0.05, 0.1)} {{$\\vec{{F}}_{{B/A}}$}};\n"
    s += f"\\draw[vecO] ({d},0) -- ({d - L},0);\n"
    s += f"\\node[legO,anchor=south] at {P(d - L + (L - rb) / 2 - 0.05, 0.1)} {{$\\vec{{F}}_{{A/B}}$}};\n"
    s += "\\node[pt] at (0,0) {};\n" + f"\\node[pt] at ({d},0) {{}};\n"
    # distance entre les centres
    yc = -1.35
    s += f"\\draw[guide] (0,{-ra - 0.08}) -- (0,{yc - 0.15});\n"
    s += f"\\draw[guide] ({d},{-rb - 0.08}) -- ({d},{yc - 0.15});\n"
    s += f"\\draw[cote] (0,{yc}) -- ({d},{yc});\n"
    s += f"\\node[legG,anchor=north] at ({d / 2},{yc - 0.08}) {{distance $d$ entre les centres}};\n"
    return s + FIN


FIGURES["actions_reciproques"] = actions_reciproques()


# ====================================================================== 3. mouvement circulaire uniforme
def mouvement_circulaire():
    R = 2.0
    s = DEBUT
    s += f"\\draw[otInk!55,line width=0.7pt] (0,0) circle ({R});\n"
    s += "\\node[pt] at (0,0) {};\n\\node[legG,anchor=north east] at (-0.06,-0.06) {$O$};\n"
    # rayon tracé vers le bas, à l'écart des vecteurs
    s += f"\\draw[guide] (0,0) -- (0,{-R});\n"
    s += f"\\node[legG,anchor=west] at (0.08,{-R / 2}) {{$R$}};\n"

    def base(th):
        th = radians(th)
        m = (R * cos(th), R * sin(th))
        ut = (-sin(th), cos(th))                 # sens du mouvement (trigonométrique)
        un = (-cos(th), -sin(th))                # vers le centre
        return m, ut, un

    # M1 : vitesse et accélération (mouvement circulaire uniforme)
    m, ut, un = base(30)
    lv, la = 1.5, 1.05
    s += f"\\node[pt] at {P(*m)} {{}};\n"
    s += f"\\node[leg,anchor=west] at {P(m[0] + 0.12, m[1] - 0.12)} {{$M_1$}};\n"
    s += f"\\draw[vecN] {P(*m)} -- {P(m[0] + lv * ut[0], m[1] + lv * ut[1])};\n"
    s += f"\\node[legN,anchor=south west] at {P(m[0] + lv * ut[0] + 0.02, m[1] + lv * ut[1])} {{$\\vec{{v}}$}};\n"
    s += f"\\draw[vecO] {P(*m)} -- {P(m[0] + la * un[0], m[1] + la * un[1])};\n"
    s += f"\\node[legO,anchor=north] at {P(m[0] + la * un[0] + 0.05, m[1] + la * un[1] - 0.1)} {{$\\vec{{a}}$}};\n"
    # M2 : le repère de Frenet
    m, ut, un = base(150)
    lu = 0.75
    s += f"\\node[pt] at {P(*m)} {{}};\n"
    s += f"\\node[leg,anchor=south east] at {P(m[0] - 0.08, m[1] + 0.06)} {{$M_2$}};\n"
    s += f"\\draw[vecG] {P(*m)} -- {P(m[0] + lu * ut[0], m[1] + lu * ut[1])};\n"
    s += f"\\node[legG,anchor=east] at {P(m[0] + lu * ut[0] - 0.08, m[1] + lu * ut[1])} {{$\\vec{{u}}_t$}};\n"
    s += f"\\draw[vecG] {P(*m)} -- {P(m[0] + lu * un[0], m[1] + lu * un[1])};\n"
    s += f"\\node[legG,anchor=north] at {P(m[0] + lu * un[0], m[1] + lu * un[1] - 0.08)} {{$\\vec{{u}}_n$}};\n"
    # sens de parcours
    s += f"\\draw[otMuted,line width=0.6pt,-{{Stealth[length=2mm]}}] (-60:{R + 0.28}) arc[start angle=-60,end angle=-25,radius={R + 0.28}];\n"
    return s + FIN


FIGURES["mouvement_circulaire"] = mouvement_circulaire()


# ====================================================================== 4. tir dans le champ de pesanteur
V0, ALPHA, G = 10.0, 45.0, 9.81
TS = V0 * sin(radians(ALPHA)) / G
H = (V0 * sin(radians(ALPHA))) ** 2 / (2 * G)
D = V0 ** 2 * sin(radians(2 * ALPHA)) / G


def tir_parabolique():
    e = 0.58                                   # 1 m → 0,58 cm
    a = radians(ALPHA)
    pts = []
    n = 40
    for i in range(n + 1):
        t = 2 * TS * i / n
        pts.append((V0 * cos(a) * t * e, (V0 * sin(a) * t - G / 2 * t * t) * e))
    xS, zS = V0 * cos(a) * TS * e, H * e
    xD = D * e
    s = DEBUT
    s += f"\\draw[axe] (0,0) -- ({f(xD + 0.9)},0) node[legG,anchor=north] {{$x$}};\n"
    s += f"\\draw[axe] (0,0) -- (0,{f(zS + 1.25)}) node[legG,anchor=east] {{$z$}};\n"
    s += "\\node[legG,anchor=north east] at (-0.07,-0.07) {$O$};\n"
    s += f"\\draw[trajet] plot[smooth] coordinates {{{' '.join(P(x, z) for x, z in pts)}}};\n"
    # vitesse initiale et angle de tir
    lv = 1.6
    s += f"\\draw[otMuted,line width=0.6pt] (0.75,0) arc[start angle=0,end angle={ALPHA},radius=0.75];\n"
    s += f"\\node[legG] at ({f(1.0 * cos(a / 2))},{f(1.0 * sin(a / 2))}) {{$\\alpha$}};\n"
    s += f"\\draw[vecN] (0,0) -- {P(lv * cos(a), lv * sin(a))};\n"
    s += f"\\node[legN,anchor=south east] at {P(lv * cos(a) - 0.05, lv * sin(a))} {{$\\vec{{v}}_0$}};\n"
    # au sommet S : vitesse horizontale (v0 cos α, même échelle) et poids
    s += f"\\fill[otInk] {P(xS, zS)} circle (2.6pt);\n"
    s += f"\\node[leg,anchor=south east] at {P(xS - 0.06, zS + 0.06)} {{$S$}};\n"
    s += f"\\draw[vecN] {P(xS, zS)} -- {P(xS + lv * cos(a), zS)};\n"
    s += f"\\node[legN,anchor=south] at {P(xS + lv * cos(a) / 2 + 0.25, zS + 0.05)} {{$\\vec{{v}}_S$}};\n"
    s += f"\\draw[vecO] {P(xS, zS)} -- {P(xS, zS - 0.95)};\n"
    s += f"\\node[legO,anchor=west] at {P(xS + 0.08, zS - 0.62)} {{$\\vec{{P}}$}};\n"
    # hauteur maximale (à gauche) et portée (en dessous)
    xh = -0.75
    s += f"\\draw[guide] {P(xS - 0.1, zS)} -- {P(xh - 0.15, zS)};\n"
    s += f"\\draw[cote] ({xh},0) -- {P(xh, zS)};\n"
    s += f"\\draw[guide] (-0.05,0) -- ({xh - 0.15},0);\n"
    s += f"\\node[legG,anchor=east] at {P(xh - 0.08, zS / 2)} {{$h$}};\n"
    zc = -0.62
    s += f"\\draw[guide] ({f(xD)},-0.05) -- ({f(xD)},{zc - 0.15});\n"
    s += f"\\draw[guide] (0,-0.05) -- (0,{zc - 0.15});\n"
    s += f"\\draw[cote] (0,{zc}) -- ({f(xD)},{zc});\n"
    s += f"\\node[legG,anchor=north] at ({f(xD / 2)},{zc - 0.08}) {{portée $D$}};\n"
    return s + FIN


FIGURES["tir_parabolique"] = tir_parabolique()


# ====================================================================== 5. satellite en orbite circulaire
def satellite():
    RT, r = 1.25, 2.7
    th = radians(40)
    S = (r * cos(th), r * sin(th))
    ut = (-sin(th), cos(th))
    un = (-cos(th), -sin(th))
    s = DEBUT
    s += f"\\draw[otNavy!60,line width=0.9pt] (0,0) circle ({RT});\n"
    s += f"\\draw[trajet] (0,0) circle ({r});\n"
    s += "\\node[legN] at (0,0.55) {Terre};\n"
    s += "\\node[pt] at (0,0) {};\n\\node[legG,anchor=east] at (-0.12,-0.02) {$O$};\n"
    # rayon de la Terre puis altitude, le long d'un rayon à l'écart des vecteurs
    phi = radians(-35)
    u = (cos(phi), sin(phi))
    n = (-sin(phi), cos(phi))
    s += f"\\draw[cote] (0,0) -- {P(RT * u[0], RT * u[1])};\n"
    s += f"\\draw[cote] {P(RT * u[0], RT * u[1])} -- {P(r * u[0], r * u[1])};\n"
    s += f"\\node[legG] at {P(RT / 2 * u[0] - 0.24 * n[0], RT / 2 * u[1] - 0.24 * n[1])} {{$R_T$}};\n"
    s += f"\\node[legG] at {P((RT + r) / 2 * u[0] - 0.24 * n[0], (RT + r) / 2 * u[1] - 0.24 * n[1])} {{$h$}};\n"
    # satellite : force de gravitation vers le centre de la Terre, vitesse tangente
    s += f"\\fill[otInk] {P(*S)} circle (2.8pt);\n"
    s += f"\\node[leg,anchor=west] at {P(S[0] + 0.14, S[1] - 0.06)} {{satellite}};\n"
    lf, lv = 0.95, 1.35
    s += f"\\draw[vecO] {P(*S)} -- {P(S[0] + lf * un[0], S[1] + lf * un[1])};\n"
    s += f"\\node[legO,anchor=north west] at {P(S[0] + lf * un[0] + 0.06, S[1] + lf * un[1] - 0.02)} {{$\\vec{{F}}$}};\n"
    s += f"\\draw[vecN] {P(*S)} -- {P(S[0] + lv * ut[0], S[1] + lv * ut[1])};\n"
    s += f"\\node[legN,anchor=south] at {P(S[0] + lv * ut[0], S[1] + lv * ut[1] + 0.05)} {{$\\vec{{v}}$}};\n"
    s += f"\\node[legG,anchor=north] at (0,{-r - 0.08}) {{orbite de rayon $r = R_T + h$}};\n"
    return s + FIN


FIGURES["satellite"] = satellite()
