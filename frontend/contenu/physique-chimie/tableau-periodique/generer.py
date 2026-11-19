# -*- coding: utf-8 -*-
"""Page « Tableau périodique des éléments » : texte, PDF à imprimer et aperçu.

    python -I -X utf8 generer.py

Lit elements.json (construit et vérifié par construire_elements.py) et écrit :
- formulaire.md (ne pas le modifier à la main : modifier ce script et le relancer) ;
- le PDF A4 paysage public/ressources-gratuites/physique-chimie/tableau-periodique/
  tableau-periodique-des-elements.pdf (LuaLaTeX + TikZ) ;
- son aperçu figures/images/apercu_tableau_periodique.png (1 100 px de large).
La figure « case_element » est dans figures/figures.py (outil figures_livre.py).
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
FRONT = ICI.parents[2]
PDF_URL = "/ressources-gratuites/physique-chimie/tableau-periodique/tableau-periodique-des-elements.pdf"
PDF = FRONT / "public" / PDF_URL.lstrip("/")
APERCU = ICI / "figures" / "images" / "apercu_tableau_periodique.png"
NBSP, NNBSP = chr(0xA0), chr(0x202F)

E = json.loads((ICI / "elements.json").read_text(encoding="utf-8"))
assert len(E) == 118

COULEURS = {  # mêmes teintes que la page (formulaires.css, .tp--…)
    "alcalin": "FFDCD8", "alcalino-terreux": "FFE7C9", "transition": "FFF2B8", "metal-pauvre": "E3E8EF",
    "lanthanide": "E2F3C8", "actinide": "CFEEDD", "metalloide": "D2EDF2", "non-metal": "D9E7FF",
    "halogene": "E8DCFF", "gaz-noble": "FFDCEE",
}
FAMILLES = [("alcalin", "Métaux alcalins"), ("alcalino-terreux", "Métaux alcalino-terreux"),
            ("transition", "Métaux de transition"), ("metal-pauvre", "Métaux pauvres"),
            ("lanthanide", "Lanthanides"), ("actinide", "Actinides"), ("metalloide", "Métalloïdes"),
            ("non-metal", "Non-métaux"), ("halogene", "Halogènes"), ("gaz-noble", "Gaz nobles")]


def config_latex(conf):
    """« 1s2 2s2 2p5 » → « $\\mathrm{1s^{2}\\,2s^{2}\\,2p^{5}}$ »."""
    morceaux = [f"{m[:2]}^{{{m[2:]}}}" for m in conf.split()]
    return "$\\mathrm{" + "\\,".join(morceaux) + "}$"


def masse_texte(el):
    return el["m"] if el["m"].startswith("[") else f"{el['m']}"


# ---------------------------------------------------------------- formulaire.md
def tableau_configurations():
    lignes = ["| Élément | Configuration électronique | Électrons de valence |", "|---|---|---|"]
    for el in E[:18]:
        lignes.append(f"| {el['nom']} {el['s']} ($Z = {el['z']}$) | {config_latex(el['config'])} | {el['valence']} |")
    return "\n".join(lignes)


def liste_elements():
    lignes = ["| $Z$ | Élément | Masse molaire (g/mol) |", "|---|---|---|"]
    for el in E:
        lignes.append(f"| {el['z']} | {el['nom']} ({el['s']}) | {masse_texte(el)} |")
    return "\n".join(lignes)


INFOS = {
    "slug": "tableau-periodique",
    "titre": "Tableau périodique des éléments",
    "titreCourt": "Tableau périodique",
    "titreSeo": "Tableau périodique des éléments : interactif et à imprimer",
    "description": "Le tableau périodique des 118 éléments, interactif et à imprimer en PDF : numéro atomique, masse molaire, familles, configuration électronique.",
    "chapo": "Les 118 éléments chimiques en un coup d’œil : touchez un élément pour afficher sa fiche, retrouvez la masse molaire de chacun dans la liste complète et téléchargez le tableau à imprimer.",
    "resume": "Les 118 éléments : tableau interactif, masses molaires et PDF à imprimer",
    "vignette": "apercu_tableau_periodique",
    "theme": "Chimie",
    "niveaux": ["Collège", "Lycée"],
    "ordre": 0,
    "publie": "2026-11-19",
    "modifie": "2026-11-19",
    "outil": "tableau-periodique",
    "telechargements": [
        {"titre": "Tableau périodique des éléments, A4 paysage en couleur", "libelle": "Tableau", "pdf": PDF_URL}
    ],
    "motsCles": ["tableau périodique", "tableau périodique des éléments", "classification périodique des éléments",
                 "tableau de Mendeleïev", "tableau périodique à imprimer", "tableau périodique interactif",
                 "liste des éléments chimiques", "masse molaire des éléments", "numéro atomique",
                 "familles chimiques", "métaux alcalins", "halogènes", "gaz nobles", "configuration électronique",
                 "électrons de valence", "électronégativité", "bloc s", "bloc p"],
    "figures": [
        {"nom": "case_element", "alt": "Une case du tableau périodique, celle du carbone : en haut à gauche le numéro atomique Z = 6, au centre le symbole C, puis le nom carbone et la masse molaire atomique 12,0 g/mol."},
        {"nom": "apercu_tableau_periodique", "alt": "Aperçu du tableau périodique à imprimer : les 118 éléments rangés en 7 périodes et 18 groupes, avec les lanthanides et les actinides en dessous, chaque case colorée selon sa famille, avec numéro atomique, symbole, nom et masse molaire."}
    ],
    "liees": [
        "physique-chimie/ions-courants",
        "physique-chimie/quantite-de-matiere-concentration",
        "physique-chimie/formules-physique-chimie-brevet",
        "tables/puissances-de-10-prefixes"
    ],
    "faq": [
        ["Combien y a-t-il d’éléments dans le tableau périodique ?", "118 éléments sont connus et nommés, de l’hydrogène (Z = 1) à l’oganesson (Z = 118). Les quatre derniers, le nihonium, le moscovium, le tennesse et l’oganesson, ont reçu leur nom en 2016."],
        ["Qui a inventé le tableau périodique ?", "Le chimiste russe Dmitri Mendeleïev a publié en 1869 une classification des éléments connus, rangés par masse croissante et selon leurs propriétés. Il y avait laissé des cases vides pour des éléments découverts ensuite, comme le gallium et le germanium."],
        ["Comment calculer la masse molaire d’une molécule ?", "On additionne les masses molaires atomiques de tous ses atomes, lues dans le tableau périodique. Pour l’eau H2O : 2 × 1,0 + 16,0 = 18,0 g/mol. Pour le dioxyde de carbone CO2 : 12,0 + 2 × 16,0 = 44,0 g/mol."],
        ["Que donne le numéro atomique Z ?", "Le nombre de protons du noyau. Un atome étant électriquement neutre, c’est aussi son nombre d’électrons. Il identifie l’élément : tout atome qui a 26 protons est un atome de fer."],
        ["Pourquoi les éléments d’une même colonne se ressemblent-ils ?", "Dans les colonnes 1, 2 et 13 à 18, ils ont le même nombre d’électrons de valence. Ce sont ces électrons qui interviennent dans les réactions : les éléments d’une même colonne réagissent donc de façon semblable et forment une famille."],
        ["Quels sont les gaz nobles ?", "L’hélium, le néon, l’argon, le krypton, le xénon, le radon et l’oganesson, dans la dernière colonne. Leur couche externe est complète, ce qui les rend très peu réactifs."]
    ]
}

TEXTE = r"""<!-- optitab:1 -->
[OUTIL]

::: conseil Par où commencer ?
- **Au collège** : parties I et V, puis la liste des masses molaires (partie VII).
- **En Seconde** : parties II à IV (familles, blocs, configuration électronique, ions).
- **En Première** : partie VI (électronégativité) et les masses molaires de la partie VII.
- **Pour l’imprimer** : partie VIII.
:::

## I. Lire une case du tableau {Collège}

Chaque case correspond à un **élément chimique**. Les éléments sont rangés par numéro atomique croissant, de l’hydrogène ($Z = 1$) à l’oganesson ($Z = 118$).

[IMAGE_1]

| Information | Pour le carbone |
|---|---|
| Numéro atomique $Z$ : nombre de protons du noyau | 6 |
| Symbole | C |
| Nom | carbone |
| Masse molaire atomique | 12,0 g/mol |

::: attention Majuscule et minuscule
Un symbole commence toujours par une majuscule, suivie parfois d’une minuscule : Co est le cobalt, alors que CO est le monoxyde de carbone, une molécule formée d’un atome de carbone et d’un atome d’oxygène.
:::

## II. Périodes, groupes et familles {Lycée}

*Programme de Seconde.*

- Une **ligne** est une **période** : il y en a 7. Le numéro de la période est le numéro de la dernière couche électronique occupée.
- Une **colonne** est un **groupe** : il y en a 18. Dans les colonnes 1, 2 et 13 à 18, les éléments d’un même groupe ont le même nombre d’électrons de valence et des propriétés chimiques voisines : ils forment une **famille**.

| Famille | Colonne | Éléments |
|---|---|---|
| Métaux alcalins | 1 (sauf H) | Li, Na, K, Rb, Cs, Fr |
| Métaux alcalino-terreux | 2 | Be, Mg, Ca, Sr, Ba, Ra |
| Halogènes | 17 | F, Cl, Br, I, At, Ts |
| Gaz nobles | 18 | He, Ne, Ar, Kr, Xe, Rn, Og |

::: remarque L’hydrogène, un cas à part
L’hydrogène est placé dans la colonne 1 parce qu’il a un seul électron de valence, mais ce n’est pas un métal alcalin : c’est un gaz, qui fait partie des non-métaux.
:::

## III. Les blocs s, p, d et f {Lycée}

*Programme de Seconde.*

Le tableau se découpe en **blocs**, selon la dernière sous-couche occupée par les électrons :

- **bloc s** : colonnes 1 et 2, et l’hélium ;
- **bloc p** : colonnes 13 à 18, sauf l’hélium ;
- **bloc d** : colonnes 3 à 12, les métaux de transition ;
- **bloc f** : les lanthanides et les actinides, placés sous le tableau pour qu’il reste lisible.

En Seconde, on utilise les blocs s et p, pour les éléments de numéro atomique inférieur ou égal à 18.

## IV. Configuration électronique et ions {Lycée}

*Programme de Seconde.*

Les électrons occupent les sous-couches dans l’ordre $\mathrm{1s}$, $\mathrm{2s}$, $\mathrm{2p}$, $\mathrm{3s}$, $\mathrm{3p}$. Une sous-couche s contient au plus 2 électrons, une sous-couche p au plus 6. Les **électrons de valence** sont ceux de la dernière couche occupée.

::: exemple
Le chlore ($Z = 17$) a pour configuration $\mathrm{1s^{2}\,2s^{2}\,2p^{6}\,3s^{2}\,3p^{5}}$. Sa dernière couche, la couche 3, porte $2 + 5 = 7$ électrons de valence : le chlore est dans la troisième période et dans la colonne 17.
:::

TABLEAU_CONFIGURATIONS

Les **gaz nobles** ont une couche externe complète : 2 électrons pour l’hélium, 8 pour les autres. C’est pourquoi ils sont très stables. Les autres atomes gagnent ou perdent des électrons pour obtenir la configuration du gaz noble le plus proche : ils forment des **ions monoatomiques**.

| Colonne | Ion formé | Exemples |
|---|---|---|
| 1 | perd 1 électron | $\mathrm{H^+}$, $\mathrm{Li^+}$, $\mathrm{Na^+}$, $\mathrm{K^+}$ |
| 2 | perd 2 électrons | $\mathrm{Mg^{2+}}$, $\mathrm{Ca^{2+}}$ |
| 13 | perd 3 électrons | $\mathrm{Al^{3+}}$ |
| 16 | gagne 2 électrons | $\mathrm{O^{2-}}$, $\mathrm{S^{2-}}$ |
| 17 | gagne 1 électron | $\mathrm{F^-}$, $\mathrm{Cl^-}$ |

::: retenir Le nombre de liaisons dans une molécule
Dans une molécule, un atome forme autant de liaisons qu’il lui manque d’électrons pour atteindre la configuration du gaz noble le plus proche : 1 liaison pour l’hydrogène, 2 pour l’oxygène, 3 pour l’azote et 4 pour le carbone.
:::

## V. Métaux, non-métaux et métalloïdes {Collège}

- Les **métaux**, à gauche et au centre, représentent environ quatre éléments sur cinq. Ils sont brillants et conduisent bien l’électricité et la chaleur.
- Les **non-métaux** sont à droite, avec l’hydrogène : carbone, azote, oxygène, soufre, halogènes et gaz nobles.
- Les **métalloïdes** (bore, silicium, germanium, arsenic, antimoine, tellure) forment une diagonale entre les deux. Le silicium sert à fabriquer les puces électroniques et les panneaux solaires.

## VI. L’électronégativité {Lycée}

*Programme de Première.*

L’**électronégativité** mesure la tendance d’un atome à attirer vers lui les électrons d’une liaison. Dans le tableau, elle augmente de gauche à droite et de bas en haut : le fluor, avec 3,98, est l’élément le plus électronégatif. Touchez un élément dans le tableau interactif pour lire sa valeur (échelle de Pauling).

::: exemple Une liaison polarisée
Dans la liaison O–H, l’oxygène (3,44) est plus électronégatif que l’hydrogène (2,20). Il attire davantage les électrons de la liaison et porte une charge partielle négative, notée $\delta^-$ ; l’hydrogène porte une charge partielle positive $\delta^+$.
:::

En pratique, on considère qu’une liaison est polarisée quand la différence d’électronégativité entre ses deux atomes dépasse environ 0,4.

## VII. La liste des 118 éléments et leurs masses molaires {Collège}

La masse molaire atomique est arrondie au dixième, en g/mol. Entre crochets : élément radioactif sans masse molaire de référence ; on donne alors le nombre de masse de son isotope le plus stable.

LISTE_ELEMENTS

## VIII. Le tableau périodique à imprimer {Collège}

Le tableau complet en couleur, au format A4 paysage : numéro atomique, symbole, nom et masse molaire de chaque élément, avec la légende des familles.

[TELECHARGEMENTS]

[IMAGE_2]
"""


UNITE = r"(?:g/mol|mol|mm|cm|nm|g|°C|%)"
NOMBRE_UNITE = re.compile(r"(\d) (?=" + UNITE + r"(?![A-Za-zÀ-ÿ0-9]))")
MILLIERS = re.compile(r"(\d) (?=\d{3}(?![\d,]))")
MATHS = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)")


def insecables(texte):
    """Espace insécable entre un nombre et son unité, espace fine des milliers (hors formules)."""
    morceaux = MATHS.split(texte)
    for i in range(0, len(morceaux), 2):
        m = MILLIERS.sub(lambda x: x.group(1) + NNBSP, morceaux[i])
        morceaux[i] = NOMBRE_UNITE.sub(lambda x: x.group(1) + NBSP, m)
    return "".join(morceaux)


def ecrire_formulaire():
    texte = TEXTE.replace("TABLEAU_CONFIGURATIONS", tableau_configurations()).replace("LISTE_ELEMENTS", liste_elements())
    entete = json.dumps(INFOS, ensure_ascii=False, indent=2)
    contenu = insecables(f"---\n{entete}\n---\n{texte}")
    (ICI / "formulaire.md").write_text(contenu, encoding="utf-8", newline="\n")
    print("formulaire.md écrit")


# ---------------------------------------------------------------- PDF A4 paysage
L, H, PAS_X, PAS_Y = 14.4, 15.0, 15.05, 15.6   # case (mm) et pas de la grille
X0, Y0 = 9.0, 21.0                              # coin de la case (groupe 1, période 1)


def place(el):
    if el["groupe"]:
        return el["groupe"], el["periode"]
    debut = 57 if el["periode"] == 6 else 89
    return 3 + el["z"] - debut, 8.35 if el["periode"] == 6 else 9.35


def coin(col, lig):
    return X0 + (col - 1) * PAS_X, Y0 + (lig - 1) * PAS_Y


def latex():
    S = []
    a = S.append
    a(r"""\documentclass{article}
\usepackage[a4paper,landscape,margin=0mm]{geometry}
\usepackage{fontspec}
\setmainfont{Montserrat}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-SemiBold]
\newfontfamily\moyen{Montserrat}[Extension=.otf, UprightFont=*-Medium, BoldFont=*-SemiBold]
\usepackage{xcolor}
\usepackage{tikz}
\definecolor{encre}{HTML}{121A33}
\definecolor{doux}{HTML}{5D667D}
\definecolor{marine}{HTML}{1B3C8E}
\definecolor{vert}{HTML}{2F7A3A}
""")
    for cle, hexa in COULEURS.items():
        a(rf"\definecolor{{f-{cle}}}{{HTML}}{{{hexa}}}" + "\n")
    a(r"""\pagestyle{empty}
\begin{document}
\noindent\begin{tikzpicture}[x=1mm,y=-1mm,remember picture,overlay,shift={(current page.north west)}]
""")
    # Titre et mentions
    a(r"  \node[anchor=north west,text=marine,font=\fontsize{20}{24}\selectfont\bfseries] at (9,7) {Tableau périodique des éléments};" + "\n")
    a(r"  \node[anchor=north east,align=right,text=doux,font=\fontsize{7.5}{9.5}\selectfont] at (288,7.6) {Masse molaire atomique en g/mol, arrondie au dixième\\[0.5mm] Entre crochets : élément radioactif, nombre de masse de l’isotope le plus stable};" + "\n")
    # Numéros de groupe (au-dessus du premier élément de chaque colonne) et de période
    haut = {1: 1, 2: 2, 13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 1}
    for g in range(1, 19):
        x, y = coin(g, haut.get(g, 4))
        a(rf"  \node[anchor=south,text=doux,font=\fontsize{{7}}{{8}}\selectfont] at ({x + L / 2:.2f},{y - 0.6:.2f}) {{{g}}};" + "\n")
    for p in range(1, 8):
        x, y = coin(1, p)
        a(rf"  \node[anchor=east,text=doux,font=\fontsize{{7}}{{8}}\selectfont] at ({x - 0.8:.2f},{y + H / 2:.2f}) {{{p}}};" + "\n")
    # Cases
    for el in E:
        col, lig = place(el)
        x, y = coin(col, lig)
        nom = el["nom"]
        taille_nom = 4.7 if len(nom) <= 10 else 4.1
        a(rf"  \filldraw[fill=f-{el['famille']},draw=encre!22,line width=0.25pt,rounded corners=0.7mm] ({x:.2f},{y:.2f}) rectangle ++({L},{H});" + "\n")
        a(rf"  \node[anchor=north west,inner sep=0pt,text=encre!80,font=\fontsize{{5.6}}{{6}}\selectfont] at ({x + 1.0:.2f},{y + 1.0:.2f}) {{{el['z']}}};" + "\n")
        a(rf"  \node[inner sep=0pt,text=encre,font=\fontsize{{12.5}}{{13}}\selectfont\bfseries] at ({x + L / 2:.2f},{y + 6.4:.2f}) {{{el['s']}}};" + "\n")
        a(rf"  \node[inner sep=0pt,text=encre,font=\moyen\fontsize{{{taille_nom}}}{{5}}\selectfont] at ({x + L / 2:.2f},{y + 10.3:.2f}) {{{nom}}};" + "\n")
        a(rf"  \node[inner sep=0pt,text=encre!85,font=\fontsize{{5}}{{6}}\selectfont] at ({x + L / 2:.2f},{y + 12.9:.2f}) {{{el['m']}}};" + "\n")
    # Renvois vers les lanthanides et actinides
    for lig, texte, cle in [(6, "57-71", "lanthanide"), (7, "89-103", "actinide")]:
        x, y = coin(3, lig)
        a(rf"  \filldraw[fill=f-{cle},draw=encre!22,line width=0.25pt,rounded corners=0.7mm] ({x:.2f},{y:.2f}) rectangle ++({L},{H});" + "\n")
        a(rf"  \node[inner sep=0pt,text=encre!80,font=\moyen\fontsize{{6}}{{7}}\selectfont] at ({x + L / 2:.2f},{y + H / 2:.2f}) {{{texte}}};" + "\n")
    for lig, texte in [(8.35, "Lanthanides"), (9.35, "Actinides")]:
        x, y = coin(3, lig)
        a(rf"  \node[anchor=east,text=doux,font=\moyen\fontsize{{6.5}}{{8}}\selectfont] at ({x - 1.5:.2f},{y + H / 2:.2f}) {{{texte}}};" + "\n")
    # Case expliquée (dans l'espace au-dessus des métaux de transition)
    cx, cy = coin(4, 1)
    cx += 2
    a(rf"  \filldraw[fill=f-non-metal,draw=encre!40,line width=0.4pt,rounded corners=1mm] ({cx:.2f},{cy:.2f}) rectangle ++(24,26);" + "\n")
    a(rf"  \node[anchor=north west,inner sep=0pt,text=encre,font=\fontsize{{9}}{{10}}\selectfont] at ({cx + 1.8:.2f},{cy + 1.8:.2f}) {{6}};" + "\n")
    a(rf"  \node[inner sep=0pt,text=encre,font=\fontsize{{24}}{{26}}\selectfont\bfseries] at ({cx + 12:.2f},{cy + 11:.2f}) {{C}};" + "\n")
    a(rf"  \node[inner sep=0pt,text=encre,font=\moyen\fontsize{{8}}{{9}}\selectfont] at ({cx + 12:.2f},{cy + 18.2:.2f}) {{Carbone}};" + "\n")
    a(rf"  \node[inner sep=0pt,text=encre,font=\fontsize{{8}}{{9}}\selectfont] at ({cx + 12:.2f},{cy + 22.4:.2f}) {{12,0}};" + "\n")
    for dy, texte, depart in [(3.0, "numéro atomique $Z$", 5.5), (11.0, "symbole", 18.0), (18.2, "nom", 19.5), (22.4, "masse molaire (g/mol)", 16.5)]:
        a(rf"  \draw[doux,line width=0.3pt] ({cx + depart:.2f},{cy + dy:.2f}) -- ({cx + 30:.2f},{cy + dy:.2f});" + "\n")
        a(rf"  \node[anchor=west,inner sep=0.6pt,text=encre,font=\fontsize{{7.5}}{{9}}\selectfont] at ({cx + 30.6:.2f},{cy + dy:.2f}) {{{texte}}};" + "\n")
    # Légende des familles
    lx, ly = 9.0, Y0 + 9.35 * PAS_Y + 5.5
    for i, (cle, nom) in enumerate(FAMILLES):
        x = lx + (i % 5) * 56
        y = ly + (i // 5) * 5.6
        a(rf"  \filldraw[fill=f-{cle},draw=encre!25,line width=0.25pt,rounded corners=0.4mm] ({x:.2f},{y:.2f}) rectangle ++(4,4);" + "\n")
        a(rf"  \node[anchor=west,inner sep=0pt,text=encre,font=\fontsize{{7.5}}{{9}}\selectfont] at ({x + 5.5:.2f},{y + 2:.2f}) {{{nom}}};" + "\n")
    a(r"  \node[anchor=south east,text=doux,font=\fontsize{7}{8}\selectfont] at (288,206) {OptiTAB · ressources gratuites · www.optitab.net/ressources-gratuites/physique-chimie/tableau-periodique/};" + "\n")
    a(r"""\end{tikzpicture}
\end{document}
""")
    return "".join(S)


def ecrire_pdf():
    PDF.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as dossier:
        tex = Path(dossier) / "tableau.tex"
        tex.write_text(latex(), encoding="utf-8")
        for _ in range(2):  # « remember picture » : deux passes
            r = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                               cwd=dossier, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode:
                raise SystemExit("LuaLaTeX a échoué :\n" + r.stdout[-2500:])
        PDF.write_bytes((Path(dossier) / "tableau.pdf").read_bytes())
        APERCU.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-png", "-singlefile", "-scale-to-x", "1100", "-scale-to-y", "-1",
                        str(PDF), str(APERCU.with_suffix(""))], check=True)
    print(f"PDF : {PDF} ({PDF.stat().st_size // 1024} Ko) ; aperçu : {APERCU}")


if __name__ == "__main__":
    ecrire_formulaire()
    ecrire_pdf()
