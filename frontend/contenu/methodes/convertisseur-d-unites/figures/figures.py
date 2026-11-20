# -*- coding: utf-8 -*-
"""Figures de la page « Convertisseur d'unités ».

    PYTHONUTF8=1 python cours/format_v1/outils/figures_livre.py contenu/methodes/convertisseur-d-unites --planche --jobs 1

1. conversions_essentielles : six équivalences à connaître (image de partage).
2. echelles_temperature : les échelles Celsius, Kelvin et Fahrenheit côte à côte
   (valeurs calculées : T = θ + 273,15 ; θF = 1,8 θ + 32).
Texte jamais posé sur un trait, cadres non remplis.
"""

BS = chr(92)
DEBUT, FIN = BS + "begin{tikzpicture}\n", BS + "end{tikzpicture}"
CAT = BS + "otMedium" + BS + "fontsize{8.5}{10}" + BS + "selectfont"
GROS = BS + "otMedium" + BS + "bfseries" + BS + "fontsize{14}{16}" + BS + "selectfont"
EGAL = BS + "otMedium" + BS + "fontsize{11.5}{13.5}" + BS + "selectfont"
NOTE = BS + "otRegular" + BS + "fontsize{9}{11}" + BS + "selectfont"

CARTES = [
    ("FORCE", "1 kN", "= 1 000 N"),
    ("PRESSION", "1 bar", "= 100 000 Pa"),
    ("ÉNERGIE", "1 kWh", "= 3,6 MJ"),
    ("VITESSE", "1 m/s", "= 3,6 km/h"),
    ("LONGUEUR", "1 pouce", "= 2,54 cm"),
    ("TEMPÉRATURE", "0 °C", "= 32 °F"),
]
NB = chr(0xA0)


def conversions_essentielles():
    L, H, gx, gy = 2.9, 1.55, 0.25, 0.25          # 2 colonnes : lisible sur téléphone
    s = DEBUT
    for i, (cat, gros, egal) in enumerate(CARTES):
        c, r = i % 2, i // 2
        x0, y0 = c * (L + gx), -r * (H + gy)
        s += f"{BS}draw[otNavy!35,line width=0.8pt,rounded corners=6pt] ({x0:.3f},{y0:.3f}) rectangle ({x0 + L:.3f},{y0 - H:.3f});\n"
        xm = x0 + L / 2
        s += f"{BS}node[text=otGreenDark,font={CAT}] at ({xm:.3f},{y0 - 0.3:.3f}) {{{cat}}};\n"
        s += f"{BS}node[text=otNavy,font={GROS}] at ({xm:.3f},{y0 - 0.75:.3f}) {{{gros.replace(' ', NB)}}};\n"
        s += f"{BS}node[text=otInk,font={EGAL}] at ({xm:.3f},{y0 - 1.18:.3f}) {{{egal.replace(' 000', BS + ',000')}}};\n"
    return s + FIN


# ---------------------------------------------------------------- échelles de température
REPERES = [  # (événement, θ en °C)
    ("zéro absolu", -273.15),
    ("la glace fond", 0.0),
    ("corps humain", 37.0),
    ("l’eau bout", 100.0),
]


def y_de(theta):
    """Position verticale : échelle linéaire de 0 à 100 °C, le zéro absolu est en dessous d'une coupure."""
    return 0.0 if theta < -200 else 1.5 + theta * 0.035


def fr(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",").replace("-", "−")
    return s


def echelles_temperature():
    cols = [("Celsius", "°C", lambda t: t), ("Kelvin", "K", lambda t: t + 273.15), ("Fahrenheit", "°F", lambda t: 1.8 * t + 32)]
    assert fr(1.8 * -273.15 + 32) == "−459,67" and fr(1.8 * 37 + 32) == "98,6"
    xs = [2.85, 4.95, 7.05]
    s = DEBUT
    for (nom, u, f), x in zip(cols, xs):
        s += f"{BS}node[text=otNavy,font={EGAL},anchor=south] at ({x:.2f},5.55) {{{nom}}};\n"
        s += f"{BS}draw[otNavy!55,line width=1pt] ({x:.2f},-0.15) -- ({x:.2f},0.42);\n"
        s += f"{BS}draw[otNavy!55,line width=1pt] ({x:.2f},1.08) -- ({x:.2f},5.4);\n"
        # coupure de l'axe
        s += f"{BS}draw[otNavy!55,line width=0.8pt] ({x - 0.12:.2f},0.38) -- ({x + 0.12:.2f},0.5);\n"
        s += f"{BS}draw[otNavy!55,line width=0.8pt] ({x - 0.12:.2f},1.0) -- ({x + 0.12:.2f},1.12);\n"
        for _, t in REPERES:
            y = y_de(t)
            s += f"{BS}draw[otNavy,line width=1pt] ({x - 0.09:.2f},{y:.3f}) -- ({x + 0.09:.2f},{y:.3f});\n"
            s += f"{BS}node[text=otInk,font={NOTE},anchor=west] at ({x + 0.14:.2f},{y:.3f}) {{{fr(f(t))}{NB}{u}}};\n"
    for nom, t in REPERES:
        s += f"{BS}node[text=otMuted,font={NOTE},anchor=east] at (2.47,{y_de(t):.3f}) {{{nom}}};\n"
    return s + FIN


FIGURES = {"conversions_essentielles": conversions_essentielles(), "echelles_temperature": echelles_temperature()}
