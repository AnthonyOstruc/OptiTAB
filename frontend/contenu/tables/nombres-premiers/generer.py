# -*- coding: utf-8 -*-
"""Génère formulaire.md des nombres premiers (listes et décompositions calculées).

    python frontend/contenu/tables/nombres-premiers/generer.py
"""
import json
from math import gcd
from pathlib import Path

ICI = Path(__file__).resolve().parent
NB = " "  # espace fine insécable (milliers)


def premier(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


PREMIERS = [n for n in range(2, 1001) if premier(n)]
assert len(PREMIERS) == 168 and len([p for p in PREMIERS if p < 100]) == 25


def facteurs(n):
    f, d = {}, 2
    while n > 1:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    return f


def ecrire_facteurs(n):
    return " \\times ".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in sorted(facteurs(n).items()))


def millier(n):
    return f"{n:,}".replace(",", NB)


INFO = {
    "slug": "nombres-premiers",
    "titre": "Nombres premiers et critères de divisibilité",
    "titreCourt": "Nombres premiers",
    "titreSeo": "Liste des nombres premiers jusqu’à 1 000 et critères de divisibilité",
    "description": "La liste des nombres premiers jusqu’à 1 000, le crible d’Ératosthène, les critères de divisibilité et la décomposition en facteurs premiers.",
    "chapo": "Les 168 nombres premiers inférieurs à 1 000, le crible de 1 à 100, les critères de divisibilité à connaître et la décomposition en facteurs premiers, avec le PGCD et le PPCM.",
    "resume": "Liste jusqu’à 1 000, critères de divisibilité",
    "vignette": "crible_100",
    "theme": "Nombres",
    "niveaux": ["Primaire", "Collège", "Lycée"],
    "ordre": 5,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["nombres premiers", "liste des nombres premiers", "nombres premiers jusqu'à 100", "nombres premiers jusqu'à 1000", "critères de divisibilité", "décomposition en facteurs premiers", "crible d'Ératosthène", "PGCD PPCM"],
    "figures": [
        {"nom": "crible_100", "alt": "Crible d’Ératosthène de 1 à 100 : les 25 nombres premiers 2, 3, 5, 7, 11, … 97 sont surlignés en vert."},
    ],
    "chapitresLies": [
        "cm2/multiples-et-diviseurs",
        "5e/multiples-diviseurs-et-partages",
        "4e/fractions-et-nombres-premiers",
        "3e/arithmetique-et-nombres-premiers",
        "seconde/utiliser-les-notions-de-multiple-diviseur-et-de-nombre-premier",
        "terminale/arithmetique",
    ],
    "faq": [
        ["Le nombre 1 est-il premier ?", "Non. Un nombre premier a exactement deux diviseurs distincts : 1 et lui-même. Le nombre 1 n’a qu’un seul diviseur, il n’est donc pas premier."],
        ["Combien y a-t-il de nombres premiers inférieurs à 100 ?", "Il y en a 25 : 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89 et 97. Il y en a 168 inférieurs à 1 000."],
        ["Comment savoir si un nombre est premier ?", "On essaie de le diviser par les nombres premiers 2, 3, 5, 7, 11… jusqu’à sa racine carrée. Si aucune division ne tombe juste, le nombre est premier. Par exemple, pour 97, il suffit de tester 2, 3, 5 et 7, car 11 × 11 = 121 > 97."],
        ["Existe-t-il un plus grand nombre premier ?", "Non : il y a une infinité de nombres premiers, comme l’a démontré Euclide il y a plus de 2 000 ans."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Définition {Primaire}\n")
L.append("::: definition Nombre premier")
L.append("Un nombre entier est **premier** s’il a exactement deux diviseurs : $1$ et lui-même. Par exemple, $7$ est premier (diviseurs $1$ et $7$), mais $9$ ne l’est pas ($9 = 3 \\times 3$).")
L.append(":::\n")
L.append("::: attention")
L.append("$1$ n’est **pas** un nombre premier : il n’a qu’un seul diviseur. Le nombre $2$ est le **seul** nombre premier pair.")
L.append(":::\n")

L.append("## II. Les nombres premiers de 1 à 100 {Primaire}\n")
L.append("[IMAGE_1]\n")
L.append("Il y a **25** nombres premiers inférieurs à $100$ : " + ", ".join(str(p) for p in PREMIERS if p < 100) + ".\n")
L.append("::: methode Le crible d’Ératosthène")
L.append("On barre $1$, puis on garde $2$ et on barre tous ses multiples ; on garde $3$ et on barre ses multiples ; et ainsi de suite avec $5$ et $7$. Les nombres qui restent sont les nombres premiers.")
L.append(":::\n")

L.append("## III. Liste des nombres premiers jusqu’à 1 000 {Collège}\n")
L.append("| Tranche | Nombres premiers |")
L.append("|---|---|")
for c in range(10):
    tranche = [p for p in PREMIERS if 100 * c < p <= 100 * (c + 1)]
    debut, fin = 100 * c + 1, 100 * (c + 1)
    L.append(f"| De {millier(debut)} à {millier(fin)} ({len(tranche)} nombres) | " + ", ".join(str(p) for p in tranche) + " |")
L.append("")
L.append(f"Au total, il y a **{len(PREMIERS)}** nombres premiers inférieurs à $1\\,000$.\n")

L.append("## IV. Critères de divisibilité {Primaire}\n")
L.append("| Divisible | Critère et exemple |")
L.append("|---|---|")
for d, regle, ex in [
    ("2", "le chiffre des unités est pair (0, 2, 4, 6, 8)", "$1\\,358$"),
    ("3", "la somme des chiffres est divisible par 3", "$231$ : $2 + 3 + 1 = 6$"),
    ("4", "le nombre formé par les deux derniers chiffres est divisible par 4", "$1\\,524$ : $24$"),
    ("5", "le chiffre des unités est 0 ou 5", "$745$"),
    ("6", "il est divisible par 2 et par 3", "$522$"),
    ("8", "le nombre formé par les trois derniers chiffres est divisible par 8", "$7\\,120$ : $120$"),
    ("9", "la somme des chiffres est divisible par 9", "$4\\,527$ : $4 + 5 + 2 + 7 = 18$"),
    ("10", "le chiffre des unités est 0", "$3\\,470$"),
    ("11", "la différence entre la somme des chiffres de rang impair et celle des chiffres de rang pair est divisible par 11", "$9\\,174$ : $(9 + 7) - (1 + 4) = 11$"),
    ("25", "le nombre formé par les deux derniers chiffres est 00, 25, 50 ou 75", "$1\\,275$"),
]:
    L.append(f"| Par {d} | si {regle}. Exemple : {ex} |")
L.append("")

# Vérification des exemples du tableau.
for d, n in [(2, 1358), (3, 231), (4, 1524), (5, 745), (6, 522), (8, 7120), (9, 4527), (10, 3470), (11, 9174), (25, 1275)]:
    assert n % d == 0, (d, n)

L.append("## V. Décomposition en facteurs premiers {Collège}\n")
L.append("Tout entier supérieur ou égal à $2$ s’écrit, de façon unique, comme un produit de nombres premiers.\n")
L.append("| Nombre | Décomposition |")
L.append("|---|---|")
for n in (12, 18, 36, 60, 84, 100, 360, 1001, 2026):
    nombre = millier(n).replace(NB, "\\,")
    deco = ecrire_facteurs(n).replace("1013", "1\\,013")
    L.append(f"| ${nombre}$ | ${deco}$ |")
L.append("")
L.append("::: methode Décomposer un nombre")
L.append("On divise successivement par le plus petit nombre premier possible : $360 \\div 2 = 180$, $180 \\div 2 = 90$, $90 \\div 2 = 45$, $45 \\div 3 = 15$, $15 \\div 3 = 5$. Donc $360 = 2^3 \\times 3^2 \\times 5$.")
L.append(":::\n")
assert ecrire_facteurs(360) == "2^{3} \\times 3^{2} \\times 5"

L.append("## VI. PGCD et PPCM {Collège}\n")
a, b = 60, 84
pgcd, ppcm = gcd(a, b), a * b // gcd(a, b)
L.append("| Notion | Méthode avec les décompositions |")
L.append("|---|---|")
L.append("| PGCD (plus grand commun diviseur) | produit des facteurs communs, avec le **plus petit** exposant |")
L.append("| PPCM (plus petit commun multiple) | produit de tous les facteurs, avec le **plus grand** exposant |")
L.append("| Relation | $\\mathrm{PGCD}(a, b) \\times \\mathrm{PPCM}(a, b) = a \\times b$ |")
L.append("")
L.append("::: exemple PGCD et PPCM de 60 et 84")
L.append(f"$60 = {ecrire_facteurs(60)}$ et $84 = {ecrire_facteurs(84)}$, donc $\\mathrm{{PGCD}} = 2^{{2}} \\times 3 = {pgcd}$ et $\\mathrm{{PPCM}} = 2^{{2}} \\times 3 \\times 5 \\times 7 = {ppcm}$.")
L.append(":::\n")
assert (pgcd, ppcm) == (12, 420)

# Milliers insécables dans les textes d'en-tête et la FAQ (« 1 000 » jamais coupé).
import re
def insecable(v):
    if isinstance(v, str):
        return re.sub(r"(\d) (\d{3})\b", "\\1" + NB + "\\2", v)
    if isinstance(v, list):
        return [insecable(x) for x in v]
    return v
INFO = {k: (insecable(v) if k not in ("slug", "figures", "chapitresLies") else v) for k, v in INFO.items()}

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit :", len(PREMIERS), "nombres premiers ; 2026 =", ecrire_facteurs(2026))
