# -*- coding: utf-8 -*-
"""Figure de la page « Simulateur du brevet » : ce que pèse chaque note.

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/methodes/simulateur-brevet --planche --jobs 1

Part de chaque note dans la note finale (arrêté du 10 avril 2025) : contrôle
continu 40 % ; épreuves 60 % réparties selon les coefficients (total 10) :
français 2, mathématiques 2, sciences 2, oral 2 → 12 % chacun ;
histoire-géographie 1,5 → 9 % ; EMC 0,5 → 3 %.
"""
BS = chr(92)
NOTE = BS + "otMedium" + BS + "fontsize{10.5}{12}" + BS + "selectfont"

PARTS = [("Contrôle continu", 40, "otGreen"), ("Français", 12, "otNavy!75"), ("Mathématiques", 12, "otNavy!75"),
         ("Sciences", 12, "otNavy!75"), ("Oral", 12, "otNavy!75"), ("Histoire-géo.", 9, "otNavy!75"),
         ("EMC", 3, "otNavy!75")]
assert sum(p for _, p, _ in PARTS) == 100
assert [p for _, p, _ in PARTS[1:]] == [round(60 * c / 10) for c in (2, 2, 2, 2, 1.5, 0.5)]

ECHELLE = 0.11   # cm par point de pourcentage (40 % → 4,4 cm)
X0 = 0.0


def barres():
    L = [BS + "begin{tikzpicture}"]
    for i, (nom, part, couleur) in enumerate(PARTS):
        y = -0.72 * i - (0.35 if i else 0)
        L.append(rf"{BS}node[anchor=east,inner sep=0pt,font={NOTE},text=otInk] at ({X0 - 0.25},{y}) {{{nom}}};")
        L.append(rf"{BS}fill[{couleur},rounded corners=2pt] ({X0},{y - 0.24}) rectangle ({X0 + part * ECHELLE:.2f},{y + 0.24});")
        L.append(rf"{BS}node[anchor=west,inner sep=0pt,font={NOTE}{BS}bfseries,text=otInk] at ({X0 + part * ECHELLE + 0.15:.2f},{y}) {{{part}{BS},{BS}%}};")
    # séparation entre le contrôle continu (40 %) et les épreuves (60 %)
    L.append(rf"{BS}draw[otMuted!60,line width=0.5pt,dash pattern=on 2pt off 1.5pt] ({X0 - 3.3},-0.53) -- ({X0 + 5.3},-0.53);")
    L.append(BS + "end{tikzpicture}")
    return "\n".join(L)


FIGURES = {"poids_notes_brevet": barres()}
