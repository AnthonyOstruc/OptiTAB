# -*- coding: utf-8 -*-
"""Génère formulaire.md de la table de la loi normale centrée réduite.

Les valeurs Φ(z) = P(Z ≤ z) sont calculées avec la fonction erf (précision
bien meilleure que les 4 décimales affichées).

    python frontend/contenu/tables/table-loi-normale/generer.py
"""
import json
from math import erf, sqrt
from pathlib import Path

ICI = Path(__file__).resolve().parent


def phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def f4(x):
    return f"{x:.4f}".replace(".", ",")


# Contrôles sur des valeurs de référence connues.
assert f4(phi(0)) == "0,5000" and f4(phi(1.96)) == "0,9750" and f4(phi(1)) == "0,8413"
assert f4(phi(2.33)) == "0,9901" and f4(phi(1.645)) == "0,9500"

INFO = {
    "slug": "table-loi-normale",
    "titre": "Table de la loi normale centrée réduite",
    "titreCourt": "Table de la loi normale",
    "titreSeo": "Table de la loi normale centrée réduite : valeurs de Φ(z)",
    "description": "La table de la loi normale centrée réduite N(0 ; 1) : valeurs de Φ(z) de 0 à 3,99, quantiles usuels (1,645 ; 1,96 ; 2,576) et méthode de lecture.",
    "chapo": "Toutes les valeurs de la fonction de répartition Φ(z) = P(Z ≤ z) de la loi normale centrée réduite, les quantiles à connaître et la méthode pour lire la table.",
    "resume": "Valeurs de Φ(z), quantiles, méthode de lecture",
    "vignette": "aire_phi",
    "theme": "Probabilités et statistiques",
    "niveaux": ["Lycée", "Supérieur"],
    "ordre": 4,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["table loi normale", "table de la loi normale centrée réduite", "table N(0,1)", "fonction de répartition loi normale", "table de Gauss", "quantile loi normale", "1,96 loi normale", "Φ(z)"],
    "figures": [
        {"nom": "aire_phi", "alt": "Courbe en cloche de la loi normale centrée réduite : l’aire colorée à gauche de z = 1,2 vaut Φ(1,2) ≈ 0,8849, et l’aire à droite vaut 1 − Φ(1,2)."},
        {"nom": "symetrie", "alt": "Courbe en cloche symétrique : l’aire à gauche de −z est égale à l’aire à droite de z."},
    ],
    "chapitresLies": ["terminale/concentration-loi-des-grands-nombres", "terminale/sommes-de-variables-aleatoires"],
    "faq": [
        ["Comment lire la table de la loi normale ?", "Pour z = 1,23, on cherche la ligne 1,2 et la colonne 0,03 : la case donne Φ(1,23) = P(Z ≤ 1,23) ≈ 0,8907. La table ne donne que des z positifs : pour un z négatif, on utilise Φ(−z) = 1 − Φ(z)."],
        ["Que vaut Φ(1,96) ?", "Φ(1,96) ≈ 0,9750. On en déduit P(−1,96 ≤ Z ≤ 1,96) = 2 × 0,975 − 1 = 0,95 : c’est l’origine du nombre 1,96 dans les intervalles à 95 %."],
        ["Comment utiliser la table pour une loi normale N(μ ; σ²) ?", "On centre et on réduit : si X suit N(μ ; σ²), alors Z = (X − μ)/σ suit N(0 ; 1). Par exemple, pour X de moyenne 100 et d’écart type 15, P(X ≤ 130) = P(Z ≤ 2) = Φ(2) ≈ 0,9772."],
        ["Pourquoi la table s’arrête-t-elle vers 4 ?", "Dès z = 3,9, Φ(z) dépasse 0,99995 : il vaut 1,0000 à quatre décimales près. Au-delà, la table n’apporte plus d’information."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Lire la table {Lycée}\n")
L.append("[IMAGE_1]\n")
L.append("La table donne $\\Phi(z) = P(Z \\leqslant z)$ pour $Z$ de loi normale $\\mathcal{N}(0\\,;1)$ : l’aire sous la courbe à gauche de $z$.\n")
L.append("::: methode Trouver $\\Phi(1{,}23)$")
L.append("On prend la ligne $1{,}2$ (unités et dixième) et la colonne $0{,}03$ (centième) : $\\Phi(1{,}23) \\approx " + f4(phi(1.23)).replace(",", "{,}") + "$.")
L.append(":::\n")

L.append("## II. Valeurs de Φ(z) pour z de 0 à 3,99 {Lycée}\n")
for debut in (0, 5):
    cols = range(debut, debut + 5)
    L.append(f"**Colonnes 0,0{debut} à 0,0{debut + 4}**\n")
    L.append("| z | " + " | ".join(f"0,0{c}" for c in cols) + " |")
    L.append("|" + "---|" * 6)
    for r in range(40):
        ligne = r / 10
        L.append(f"| {ligne:.1f}".replace(".", ",") + " | " + " | ".join(f4(phi(ligne + c / 100)) for c in cols) + " |")
    L.append("")

L.append("## III. Quantiles à connaître {Lycée}\n")
L.append("| Probabilité | Valeur de z | Utilisation |")
L.append("|---|---|---|")
for p, z, u in [
    ("$\\Phi(z) = 0{,}90$", "1,282", "risque unilatéral de 10 %"),
    ("$\\Phi(z) = 0{,}95$", "1,645", "risque unilatéral de 5 %"),
    ("$\\Phi(z) = 0{,}975$", "1,960", "intervalle à 95 %"),
    ("$\\Phi(z) = 0{,}99$", "2,326", "risque unilatéral de 1 %"),
    ("$\\Phi(z) = 0{,}995$", "2,576", "intervalle à 99 %"),
]:
    L.append(f"| {p} | {z} | {u} |")
L.append("")

L.append("## IV. Calculer toutes les probabilités {Lycée}\n")
L.append("[IMAGE_2]\n")
L.append("| Probabilité cherchée | Formule |")
L.append("|---|---|")
for t, fo in [
    ("À gauche de $z$", "$P(Z \\leqslant z) = \\Phi(z)$"),
    ("À droite de $z$", "$P(Z > z) = 1 - \\Phi(z)$"),
    ("À gauche d’un nombre négatif", "$P(Z \\leqslant -z) = 1 - \\Phi(z)$"),
    ("Entre deux valeurs", "$P(a \\leqslant Z \\leqslant b) = \\Phi(b) - \\Phi(a)$"),
    ("Intervalle centré", "$P(-z \\leqslant Z \\leqslant z) = 2\\,\\Phi(z) - 1$"),
]:
    L.append(f"| {t} | {fo} |")
L.append("")
L.append("::: exemple Avec une loi $\\mathcal{N}(100\\,;15^2)$")
L.append("$X$ suit la loi normale de moyenne $100$ et d’écart type $15$. On centre et on réduit :")
L.append("$$P(X \\leqslant 130) = P\\left(Z \\leqslant \\frac{130 - 100}{15}\\right) = \\Phi(2) \\approx " + f4(phi(2)).replace(",", "{,}") + "$$")
L.append(":::\n")

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit ; Φ(1,23) =", f4(phi(1.23)), "; Φ(2) =", f4(phi(2)))
