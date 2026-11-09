# -*- coding: utf-8 -*-
"""Génère formulaire.md « Carrés, cubes et racines carrées » (valeurs calculées).

    python frontend/contenu/tables/carres-cubes-racines/generer.py
"""
import json
from math import isqrt, sqrt
from pathlib import Path

ICI = Path(__file__).resolve().parent
NB = " "


def millier(n):
    return f"{n:,}".replace(",", NB)


def racine(n):
    r = isqrt(n)
    return str(r) if r * r == n else f"{sqrt(n):.3f}".replace(".", ",")


assert racine(2) == "1,414" and racine(3) == "1,732" and racine(49) == "7"

INFO = {
    "slug": "carres-cubes-racines",
    "titre": "Carrés, cubes et racines carrées",
    "titreCourt": "Carrés, cubes et racines",
    "titreSeo": "Table des carrés, cubes et racines carrées de 1 à 50",
    "description": "La table des carrés, des cubes et des racines carrées de 1 à 50, les carrés parfaits, les racines à connaître et la méthode pour encadrer une racine.",
    "chapo": "Le carré, le cube et la racine carrée de chaque nombre de 1 à 50, les carrés et cubes parfaits à reconnaître et les valeurs approchées les plus utiles.",
    "resume": "De 1 à 50, carrés parfaits, √2, √3",
    "vignette": "carres_parfaits",
    "theme": "Calcul",
    "niveaux": ["Collège", "Lycée"],
    "ordre": 6,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["table des carrés", "carrés parfaits", "table des cubes", "racine carrée", "tableau racines carrées", "racine de 2", "liste des carrés", "carré d'un nombre"],
    "figures": [
        {"nom": "carres_parfaits", "alt": "Quatre carrés de côtés 1, 2, 3 et 4 quadrillés : ils contiennent 1, 4, 9 et 16 petits carrés, d’où 1² = 1, 2² = 4, 3² = 9 et 4² = 16."},
    ],
    "chapitresLies": ["5e/carres-et-cubes", "4e/carres-et-racines-carrees", "3e/puissances-racines-et-ecriture-scientifique", "4e/theoreme-de-pythagore"],
    "faq": [
        ["Qu’est-ce qu’un carré parfait ?", "C’est le carré d’un nombre entier : 1, 4, 9, 16, 25, 36, 49, 64, 81, 100… Sa racine carrée est un nombre entier."],
        ["Combien vaut la racine carrée de 2 ?", "√2 ≈ 1,414 (plus précisément 1,41421356…). C’est un nombre irrationnel : son écriture décimale ne s’arrête jamais et n’est pas périodique."],
        ["Comment encadrer une racine carrée sans calculatrice ?", "On cherche les deux carrés parfaits qui encadrent le nombre. Par exemple, 49 < 50 < 64, donc 7 < √50 < 8. Comme 50 est très proche de 49, √50 est à peine plus grand que 7 (√50 ≈ 7,07)."],
        ["Quelle est la différence entre le carré et la racine carrée ?", "Le carré de 5 est 5 × 5 = 25 ; la racine carrée de 25 est le nombre positif dont le carré vaut 25, c’est-à-dire 5. Ce sont deux opérations réciproques pour les nombres positifs."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Définitions {Collège}\n")
L.append("[IMAGE_1]\n")
L.append("| Notion | Définition |")
L.append("|---|---|")
L.append("| Carré de $n$ | $n^2 = n \\times n$ : l’aire d’un carré de côté $n$ |")
L.append("| Cube de $n$ | $n^3 = n \\times n \\times n$ : le volume d’un cube d’arête $n$ |")
L.append("| Racine carrée de $a$ ($a \\geqslant 0$) | le nombre positif $\\sqrt{a}$ dont le carré vaut $a$ |")
L.append("")

L.append("## II. Table de 1 à 50 {Collège}\n")
L.append("Les racines carrées sont arrondies au millième ; elles sont exactes pour les carrés parfaits.\n")
for debut in (1, 26):
    L.append("| $n$ | $n^2$ | $n^3$ | $\\sqrt{n}$ |")
    L.append("|---|---|---|---|")
    for n in range(debut, debut + 25):
        r = racine(n)
        r = f"**{r}**" if "," not in r else r
        L.append(f"| {n} | {millier(n * n)} | {millier(n ** 3)} | {r} |")
    L.append("")

L.append("## III. Carrés et cubes parfaits {Collège}\n")
L.append("| Liste | Valeurs |")
L.append("|---|---|")
L.append("| Carrés parfaits jusqu’à 400 | " + ", ".join(millier(k * k) for k in range(1, 21)) + " |")
L.append("| Cubes parfaits jusqu’à 1 000 | " + ", ".join(millier(k ** 3) for k in range(1, 11)) + " |")
L.append("| Puissances de 2 jusqu’à 1 024 | " + ", ".join(millier(2 ** k) for k in range(0, 11)) + " |")
L.append("")

L.append("## IV. Racines à connaître {Collège}\n")
L.append("| Racine | Valeur approchée |")
L.append("|---|---|")
for n in (2, 3, 5, 6, 7, 8, 10):
    L.append(f"| $\\sqrt{{{n}}}$ | $\\approx {sqrt(n):.4f}$ |".replace(".", "{,}"))
L.append("")
L.append("::: methode Encadrer une racine carrée")
L.append("On cherche les carrés parfaits qui entourent le nombre : $49 < 50 < 64$, donc $7 < \\sqrt{50} < 8$.")
L.append(":::\n")
L.append("::: attention")
L.append("$\\sqrt{a + b} \\neq \\sqrt{a} + \\sqrt{b}$, mais $\\sqrt{a \\times b} = \\sqrt{a} \\times \\sqrt{b}$ pour $a$ et $b$ positifs. Par exemple, $\\sqrt{50} = \\sqrt{25 \\times 2} = 5\\sqrt{2}$.")
L.append(":::\n")

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit ; √50 =", racine(50))
