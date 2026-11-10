# -*- coding: utf-8 -*-
"""Génère formulaire.md « Alphabet grec » à partir de lettres.py.

    python frontend/contenu/tables/alphabet-grec/generer.py
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from lettres import LETTRES  # noqa: E402

INFO = {
    "slug": "alphabet-grec",
    "titre": "Alphabet grec",
    "titreCourt": "Alphabet grec",
    "titreSeo": "Alphabet grec : les 24 lettres, prononciation et usage en maths",
    "description": "Les 24 lettres de l’alphabet grec en minuscule et en majuscule, leur nom, leur prononciation et leur usage en maths et en physique (α, β, Δ, π, Σ, σ, ω…).",
    "chapo": "Les 24 lettres grecques avec leur majuscule, leur nom et leur prononciation, ce qu’elles désignent en maths et en physique, les lettres à ne pas confondre et leur écriture en LaTeX.",
    "resume": "24 lettres, prononciation, usage en maths",
    "vignette": "lettres_grecques",
    "theme": "Notations",
    "niveaux": ["Collège", "Lycée", "Supérieur"],
    "ordre": 12,
    "publie": "2026-11-10",
    "modifie": "2026-11-10",
    "motsCles": ["alphabet grec", "lettres grecques", "alphabet grec majuscule minuscule", "lettre grecque maths", "prononciation alphabet grec", "lettre grecque sigma", "lettre grecque delta", "alphabet grec latex"],
    "figures": [
        {"nom": "lettres_grecques", "alt": "Les 24 lettres minuscules de l’alphabet grec dans l’ordre, de alpha à oméga, chacune avec son nom : α alpha, β bêta, γ gamma, δ delta… ψ psi, ω oméga."},
    ],
    "chapitresLies": ["3e/grandeurs-et-mesures", "premiere/equations-fonctions-polynomes-du-second-degre", "terminale/sommes-de-variables-aleatoires"],
    "faq": [
        ["Combien y a-t-il de lettres dans l’alphabet grec ?", "L’alphabet grec compte 24 lettres, d’alpha (α) à oméga (ω). Chacune existe en minuscule et en majuscule."],
        ["Comment s’appelle la lettre grecque Σ ?", "C’est sigma majuscule. En maths, Σ désigne une somme de plusieurs termes ; sa minuscule σ désigne souvent un écart type."],
        ["Que signifie Δ en maths ?", "Δ (delta majuscule) désigne le discriminant d’un trinôme du second degré, Δ = b² − 4ac, ou une variation, comme Δt pour une durée."],
        ["Comment écrire une lettre grecque en LaTeX ?", "On tape son nom précédé d’une barre oblique inverse : \\alpha donne α, \\pi donne π. Pour la majuscule, on met une capitale : \\Delta donne Δ."],
        ["Pourquoi utilise-t-on des lettres grecques en maths ?", "Pour avoir plus de symboles que l’alphabet latin et réserver certaines lettres à des usages précis : π pour le nombre pi, Σ pour une somme, Δ pour le discriminant."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Les 24 lettres {Collège}\n")
L.append("[IMAGE_1]\n")
L.append("| Lettres | Nom et usages en maths et en sciences |")
L.append("|---|---|")
for nom, prono, mini, maj, usage in LETTRES:
    n = f"**{nom}** (« {prono} »)" if prono and prono != nom else f"**{nom}**"
    L.append(f"| ${mini}$ $\\;{maj}$ | {n} : {usage} |")
L.append("")
L.append("Dans chaque case, la minuscule est écrite avant la majuscule. Plusieurs majuscules ($\\mathrm{A}$, $\\mathrm{B}$, $\\mathrm{E}$, $\\mathrm{H}$, $\\mathrm{P}$, $\\mathrm{X}$…) ont la même forme qu’une lettre latine.\n")

L.append("## II. Les plus utilisées selon le niveau {Collège}\n")
L.append("| Niveau | Lettres et sens |")
L.append("|---|---|")
L.append("| Collège | $\\pi$ : périmètre et aire du disque ; $\\alpha$, $\\beta$ : angles |")
L.append("| Lycée | $\\Delta$ : discriminant ; $\\Sigma$ : somme ; $\\theta$ : angle ; $\\mu$ et $\\sigma$ : moyenne et écart type ; $\\lambda$ : paramètre d’une loi |")
L.append("| Supérieur | $\\varepsilon$ et $\\delta$ : petites quantités ; $\\lambda$ : valeur propre ; $\\chi^2$ : test du khi-deux ; $\\Gamma$ : fonction gamma |")
L.append("| Physique | $\\lambda$ : longueur d’onde ; $\\rho$ : masse volumique ; $\\omega$ : pulsation ; $\\Omega$ : ohm ; $\\Delta$ : variation |")
L.append("")

L.append("## III. Lettres à ne pas confondre {Collège}\n")
L.append("| Lettre grecque | À ne pas confondre avec |")
L.append("|---|---|")
for g, nom, lat in [
    (r"\nu", "nu", "v"), (r"\rho", "rhô", "p"), (r"\omega", "oméga", "w"), (r"\eta", "êta", "n"),
    (r"\chi", "khi", "x"), (r"\kappa", "kappa", "k"), (r"\upsilon", "upsilon", "u"), (r"\iota", "iota", "i"),
]:
    L.append(f"| ${g}$ ({nom}) | la lettre latine ${lat}$ |")
L.append("")
L.append("::: retenir Variantes d’écriture")
L.append("Certaines lettres ont deux formes, qui désignent la même lettre : $\\varepsilon$ et $\\epsilon$, $\\theta$ et $\\vartheta$, $\\varphi$ et $\\phi$, $\\rho$ et $\\varrho$. Le sigma final, en fin de mot grec, s’écrit ς.")
L.append(":::\n")

L.append("## IV. Écrire les lettres grecques en LaTeX {Supérieur}\n")
L.append("On tape le nom de la lettre précédé d’une barre oblique inverse : `\\alpha` donne $\\alpha$, `\\pi` donne $\\pi$. Pour la majuscule, le nom commence par une capitale : `\\Delta` donne $\\Delta$, `\\Omega` donne $\\Omega$.\n")
L.append("| Cas particulier | Écriture |")
L.append("|---|---|")
L.append("| Majuscules identiques aux lettres latines | on tape la lettre latine : `A`, `B`, `E`… |")
L.append("| Omicron | on tape `o` |")
L.append("| Variantes | `\\varepsilon`, `\\vartheta`, `\\varphi`, `\\varrho` |")
L.append("")

noms = [l[0] for l in LETTRES]
assert noms[0] == "alpha" and noms[-1] == "oméga" and noms.index("pi") == 15 and noms.index("sigma") == 17

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit :", len(LETTRES), "lettres")
