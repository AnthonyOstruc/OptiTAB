# -*- coding: utf-8 -*-
"""Génère formulaire.md de la table de multiplication (calculs faits par le script).

    python frontend/contenu/tables/table-de-multiplication/generer.py
"""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent

INFO = {
    "slug": "table-de-multiplication",
    "titre": "Table de multiplication",
    "titreCourt": "Table de multiplication",
    "titreSeo": "Table de multiplication de 1 à 20 : à imprimer, avec astuces",
    "description": "La table de multiplication de 1 à 10 et de 11 à 20, chaque table une par une, les astuces pour les retenir et une version à imprimer. Gratuit.",
    "chapo": "Toutes les tables de multiplication de 1 à 20, la table de Pythagore à imprimer et les astuces pour retenir les résultats les plus difficiles.",
    "resume": "Tables de 1 à 20, à imprimer, astuces",
    "vignette": "table_pythagore",
    "theme": "Calcul",
    "niveaux": ["Primaire", "Collège"],
    "ordre": 1,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["table de multiplication", "tables de multiplication", "table de multiplication à imprimer", "table de Pythagore", "table de 7", "table de 8", "table de 9", "apprendre les tables de multiplication"],
    "figures": [
        {"nom": "table_pythagore", "alt": "Table de Pythagore de 1 à 10 à imprimer : en-têtes bleus, produits dans les cases, carrés 1, 4, 9 … 100 en vert sur la diagonale."},
        {"nom": "rangees_7x8", "alt": "Quadrillage de 7 rangées de 8 points pour comprendre que 7 × 8 = 56."},
    ],
    "chapitresLies": [
        "ce1/construire-les-premieres-tables",
        "ce1/construire-les-autres-tables",
        "ce2/tables-facteurs-et-multiples",
        "ce2/multiplier-par-4-et-par-8",
        "cm1/multiplier-des-entiers",
    ],
    "faq": [
        ["Comment apprendre les tables de multiplication facilement ?", "Apprenez une table à la fois, à voix haute, puis récitez-la dans le désordre. Utilisez les astuces (table de 9, de 5, de 10), le fait que 7 × 8 = 8 × 7, et révisez quelques minutes chaque jour plutôt qu’une longue séance."],
        ["Combien font 7 × 8 ?", "7 × 8 = 56. Astuce : « 5, 6, 7, 8 », car 56 = 7 × 8. C’est l’un des résultats les plus souvent oubliés, avec 6 × 7 = 42, 6 × 8 = 48 et 7 × 9 = 63."],
        ["Quelle est la table de multiplication la plus difficile ?", "Pour la plupart des élèves, ce sont les tables de 7 et de 8, et en particulier 6 × 7, 6 × 8, 7 × 8 et 8 × 9. Les tables de 1, 2, 5 et 10 sont les plus faciles."],
        ["À quel âge apprend-on les tables de multiplication ?", "Les premières tables se construisent au CE1. Toutes les tables de 1 à 9 doivent être mémorisées à la fin du CE2, puis entretenues au CM1 et au CM2."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Table de Pythagore de 1 à 10 {Primaire}\n")
L.append("Le résultat de $7 \\times 8$ se lit au croisement de la ligne $7$ et de la colonne $8$. Les **carrés** ($1 \\times 1$, $2 \\times 2$…) sont en gras, sur la diagonale.\n")
L.append("| × | " + " | ".join(str(j) for j in range(1, 11)) + " |")
L.append("|" + "---|" * 11)
for i in range(1, 11):
    L.append(f"| {i} | " + " | ".join(f"**{i * j}**" if i == j else str(i * j) for j in range(1, 11)) + " |")
L.append("")

L.append("## II. Les tables de 1 à 10, une par une {Primaire}\n")
for n in range(1, 11):
    L.append(f"### Table de {n}\n")
    L.append("| De 1 à 5 | De 6 à 10 |")
    L.append("|---|---|")
    for k in range(1, 6):
        L.append(f"| ${n} \\times {k} = {n * k}$ | ${n} \\times {k + 5} = {n * (k + 5)}$ |")
    L.append("")

L.append("## III. Tables de 11 à 20 {Collège}\n")
L.append("| × | " + " | ".join(str(j) for j in range(1, 11)) + " |")
L.append("|" + "---|" * 11)
for i in range(11, 21):
    L.append(f"| {i} | " + " | ".join(str(i * j) for j in range(1, 11)) + " |")
L.append("")

L.append("## IV. Astuces pour les retenir {Primaire}\n")
L.append("[IMAGE_2]\n")
L.append("Multiplier, c’est compter des rangées : $7$ rangées de $8$ points, c’est $7 \\times 8 = 56$ points.\n")
L.append("| Table | Astuce |")
L.append("|---|---|")
for t, a in [
    ("Table de 1", "le nombre ne change pas : $1 \\times 7 = 7$"),
    ("Table de 2", "on double : $2 \\times 8 = 8 + 8 = 16$"),
    ("Table de 4", "on double deux fois : $4 \\times 7 = 14 \\times 2 = 28$"),
    ("Table de 5", "la moitié de la table de 10 ; le résultat finit par $0$ ou $5$"),
    ("Table de 8", "on double trois fois : $8 \\times 6 = 12 \\to 24 \\to 48$"),
    ("Table de 9", "pour $9 \\times n$, le chiffre des dizaines est $n - 1$ et les deux chiffres ont pour somme $9$ : $9 \\times 7 = 63$"),
    ("Table de 10", "on écrit un $0$ à droite : $10 \\times 7 = 70$"),
    ("Table de 11 (jusqu’à 9)", "on répète le chiffre : $11 \\times 7 = 77$"),
]:
    L.append(f"| {t} | {a} |")
L.append("")
L.append("::: retenir L’ordre ne compte pas")
L.append("$7 \\times 8 = 8 \\times 7$ : quand on connaît une table, on connaît déjà une partie des autres. Il suffit d’apprendre la moitié de la table de Pythagore.")
L.append(":::\n")
L.append("::: attention Les résultats les plus souvent oubliés")
L.append("$6 \\times 7 = 42$, $\\quad 6 \\times 8 = 48$, $\\quad 7 \\times 7 = 49$, $\\quad 7 \\times 8 = 56$, $\\quad 7 \\times 9 = 63$, $\\quad 8 \\times 8 = 64$, $\\quad 8 \\times 9 = 72$.")
L.append("")
L.append("Moyen mnémotechnique : « 5, 6, 7, 8 » donne $56 = 7 \\times 8$.")
L.append(":::\n")

L.append("## V. Table de multiplication à imprimer {Primaire}\n")
L.append("[IMAGE_1]\n")
L.append("Enregistrez l’image ou utilisez le bouton « Imprimer la table » en haut de la page : seule la table s’imprime, sans menus.\n")

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit :", len(L), "lignes")
