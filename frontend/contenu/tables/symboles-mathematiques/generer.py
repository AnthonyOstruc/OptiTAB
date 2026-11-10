# -*- coding: utf-8 -*-
"""Génère formulaire.md « Symboles mathématiques » (tableaux symbole | lecture et exemple).

    python frontend/contenu/tables/symboles-mathematiques/generer.py
"""
import json
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent

INFO = {
    "slug": "symboles-mathematiques",
    "titre": "Symboles mathématiques",
    "titreCourt": "Symboles mathématiques",
    "titreSeo": "Symboles mathématiques : liste, signification et exemples",
    "description": "La liste des symboles mathématiques avec leur lecture et un exemple : logique (∀, ∃, ⇒, ⇔), ensembles (∈, ⊂, ∪, ∩), relations, opérations, analyse, géométrie.",
    "chapo": "Tous les symboles rencontrés du collège au supérieur, rangés par thème : comment ils se lisent, ce qu’ils signifient et un exemple d’emploi pour chacun.",
    "resume": "∀, ∃, ∈, ⊂, ⇒, ⇔, Σ, ∫ : lecture et exemples",
    "vignette": "symboles",
    "theme": "Notations",
    "niveaux": ["Collège", "Lycée", "Supérieur"],
    "ordre": 13,
    "publie": "2026-11-10",
    "modifie": "2026-11-10",
    "motsCles": ["symboles mathématiques", "liste des symboles mathématiques", "signification symbole math", "symbole appartient", "symbole pour tout il existe", "symbole implique équivaut", "symbole inclus", "notations mathématiques"],
    "figures": [
        {"nom": "symboles", "alt": "Douze symboles mathématiques courants avec leur lecture : pour tout, il existe, appartient à, est inclus dans, implique, équivaut à, somme, intégrale, infini, environ égal, différent de, racine carrée."},
    ],
    "chapitresLies": ["seconde/manipuler-les-nombres-reels", "3e/raisonner-et-demontrer", "terminale/combinatoire-et-denombrement"],
    "faq": [
        ["Que signifie le symbole ∈ ?", "∈ se lit « appartient à » : x ∈ ℝ signifie que x est un nombre réel. Son contraire ∉ se lit « n’appartient pas à »."],
        ["Quelle est la différence entre ⇒ et ⇔ ?", "A ⇒ B se lit « A implique B » : si A est vraie, B l’est aussi. A ⇔ B se lit « A équivaut à B » : A et B sont vraies en même temps, l’implication marche dans les deux sens."],
        ["Que veulent dire ∀ et ∃ ?", "∀ se lit « pour tout » et ∃ se lit « il existe ». Par exemple, ∀x ∈ ℝ, x² ≥ 0 signifie que tout réel a un carré positif."],
        ["Quelle est la différence entre ∈ et ⊂ ?", "∈ relie un élément à un ensemble (2 ∈ ℕ), alors que ⊂ relie deux ensembles (ℕ ⊂ ℤ : tout entier naturel est un entier relatif)."],
        ["Que signifie le symbole ≈ ?", "≈ se lit « environ égal à » : il indique une valeur approchée, comme π ≈ 3,14."],
    ],
}

# (titre de partie, niveau, [(symbole LaTeX, texte de la ligne)])
PARTIES = [
    ("Logique", "Lycée", [
        (r"\forall", "se lit **« pour tout »**. Exemple : $\\forall x \\in \\mathbb{R},\\ x^2 \\geqslant 0$"),
        (r"\exists", "se lit **« il existe »**. Exemple : $\\exists x \\in \\mathbb{R},\\ x^2 = 2$"),
        (r"\exists!", "se lit **« il existe un unique »** : un seul élément convient"),
        (r"\Rightarrow", "se lit **« implique »**. Exemple : $x = 2 \\Rightarrow x^2 = 4$ (la réciproque est fausse)"),
        (r"\Leftrightarrow", "se lit **« équivaut à »** ou « si et seulement si ». Exemple : $2x = 6 \\Leftrightarrow x = 3$"),
        (r"\neg", "se lit **« non »** : négation d’une proposition (on écrit aussi « non »)"),
    ]),
    ("Ensembles", "Lycée", [
        (r"\in", "se lit **« appartient à »**. Exemple : $3 \\in \\mathbb{N}$"),
        (r"\notin", "se lit **« n’appartient pas à »**. Exemple : $-1 \\notin \\mathbb{N}$"),
        (r"\subset", "se lit **« est inclus dans »** : relie deux ensembles. Exemple : $\\mathbb{N} \\subset \\mathbb{Z}$"),
        (r"\cup", "**réunion** : les éléments de $A$ ou de $B$ (ou des deux)"),
        (r"\cap", "**intersection** : les éléments communs à $A$ et à $B$"),
        (r"\varnothing", "**ensemble vide** : l’ensemble qui ne contient aucun élément"),
        (r"A \setminus B", "se lit **« $A$ privé de $B$ »** : les éléments de $A$ qui ne sont pas dans $B$"),
        (r"\{\ \}", "**accolades** : liste les éléments d’un ensemble. Exemple : $\\{1\\,;2\\,;3\\}$"),
    ]),
    ("Ensembles de nombres", "Collège", [
        (r"\mathbb{N}", "les **entiers naturels** : $0$, $1$, $2$, $3$…"),
        (r"\mathbb{Z}", "les **entiers relatifs** : $\\dots$, $-2$, $-1$, $0$, $1$, $2$…"),
        (r"\mathbb{D}", "les **nombres décimaux** : écriture à virgule finie, comme $0{,}25$"),
        (r"\mathbb{Q}", "les **nombres rationnels** : quotients d’entiers, comme $\\dfrac{1}{3}$"),
        (r"\mathbb{R}", "les **nombres réels** : tous les nombres de la droite graduée, comme $\\sqrt{2}$ ou $\\pi$"),
        (r"\mathbb{C}", "les **nombres complexes** : de la forme $a + \\mathrm{i}b$, avec $\\mathrm{i}^2 = -1$"),
        (r"\mathbb{R}^*", "l’étoile signifie **« privé de $0$ »** ; $\\mathbb{R}^+$ désigne les réels positifs"),
    ]),
    ("Relations", "Collège", [
        (r"\neq", "se lit **« différent de »**. Exemple : $2 + 2 \\neq 5$"),
        (r"\approx", "se lit **« environ égal à »** : valeur approchée. Exemple : $\\pi \\approx 3{,}14$"),
        (r"\leqslant", "se lit **« inférieur ou égal à »** ; $\\geqslant$ se lit « supérieur ou égal à »"),
        (r"<", "se lit **« strictement inférieur à »** ; $>$ se lit « strictement supérieur à »"),
        (r"\equiv", "se lit **« congru à »** (arithmétique). Exemple : $17 \\equiv 2 \\pmod{5}$"),
        (r"\sim", "se lit **« équivalent à »** (analyse). Exemple : $\\sin x \\sim x$ en $0$"),
        (r"\propto", "se lit **« proportionnel à »**, surtout en physique"),
    ]),
    ("Opérations", "Collège", [
        (r"\pm", "se lit **« plus ou moins »**. Exemple : $x = \\pm 3$ signifie $x = 3$ ou $x = -3$"),
        (r"\sqrt{\ }", "**racine carrée** : $\\sqrt{9} = 3$ ; $\\sqrt[n]{\\ }$ désigne la racine $n$-ième"),
        (r"\lvert x \rvert", "**valeur absolue** : distance à $0$. Exemple : $\\lvert -5 \\rvert = 5$"),
        (r"n!", "se lit **« factorielle $n$ »** : $n! = 1 \\times 2 \\times \\dots \\times n$, et $4! = 24$"),
        (r"\sum", "**somme** de plusieurs termes. Exemple : $\\displaystyle\\sum_{k=1}^{3} k = 1 + 2 + 3$"),
        (r"\prod", "**produit** de plusieurs termes. Exemple : $\\displaystyle\\prod_{k=1}^{3} k = 1 \\times 2 \\times 3$"),
        (r"\binom{n}{k}", "se lit **« $k$ parmi $n$ »** : nombre de façons de choisir $k$ éléments parmi $n$"),
        (r"g \circ f", "se lit **« $g$ rond $f$ »** : composée, $(g \\circ f)(x) = g\\big(f(x)\\big)$"),
    ]),
    ("Analyse", "Lycée", [
        (r"\infty", "**l’infini** : $+\\infty$ et $-\\infty$ ne sont pas des nombres réels"),
        (r"\lim", "**limite**. Exemple : $\\lim\\limits_{x \\to +\\infty} \\dfrac{1}{x} = 0$"),
        (r"\mapsto", "se lit **« associe »**. Exemple : $f : x \\mapsto x^2$"),
        (r"f'", "se lit **« $f$ prime »** : dérivée de $f$, notée aussi $\\dfrac{\\mathrm{d}f}{\\mathrm{d}x}$"),
        (r"\int", "**intégrale**. Exemple : $\\displaystyle\\int_0^1 x\\,\\mathrm{d}x = \\dfrac{1}{2}$"),
        (r"\Delta", "**delta** : discriminant ou variation, comme $\\Delta t$ pour une durée"),
        (r"\partial", "**dérivée partielle** (supérieur) : dérivée par rapport à une seule variable"),
    ]),
    ("Géométrie", "Collège", [
        (r"(AB)", "la **droite** passant par $A$ et $B$"),
        (r"[AB]", "le **segment** d’extrémités $A$ et $B$ ; $AB$ désigne sa longueur"),
        (r"[AB)", "la **demi-droite** d’origine $A$ passant par $B$"),
        (r"\overrightarrow{AB}", "le **vecteur** allant de $A$ vers $B$ ; $\\lVert \\vec{u} \\rVert$ est la norme"),
        (r"\widehat{ABC}", "l’**angle** de sommet $B$ formé par les demi-droites $[BA)$ et $[BC)$"),
        (r"\parallel", "se lit **« est parallèle à »**. Exemple : $(AB) \\parallel (CD)$"),
        (r"\perp", "se lit **« est perpendiculaire à »**. Exemple : $(AB) \\perp (BC)$"),
    ]),
    ("Probabilités", "Lycée", [
        (r"P(A)", "**probabilité** de l’événement $A$, comprise entre $0$ et $1$"),
        (r"\overline{A}", "l’**événement contraire** de $A$ : $P(\\overline{A}) = 1 - P(A)$"),
        (r"P_A(B)", "probabilité **de $B$ sachant $A$** (probabilité conditionnelle)"),
        (r"E(X)", "**espérance** de la variable aléatoire $X$ : sa valeur moyenne"),
        (r"V(X)", "**variance** de $X$ ; $\\sigma(X) = \\sqrt{V(X)}$ est son écart type"),
    ]),
]

CHIFFRES = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
L = ["<!-- optitab:1 -->"]
L.append("## I. Logique {Lycée}\n")
L.append("[IMAGE_1]\n")
for k, (titre, niveau, lignes) in enumerate(PARTIES):
    if k:
        L.append(f"## {CHIFFRES[k]}. {titre} {{{niveau}}}\n")
    L.append("| Symbole | Lecture et exemple |")
    L.append("|---|---|")
    textes = []
    for sym, texte in lignes:
        L.append(f"| ${sym}$ | {texte} |")
        textes.append(re.sub(r"\$[^$]*\$", "", texte).replace("**", "").strip())
    # chaque tableau doit passer en « symbole | texte aligné à gauche » (moyenne > 40 caractères)
    moyenne = sum(len(t) for t in textes) / len(textes)
    assert moyenne > 40, (titre, moyenne)
    L.append("")
    if titre == "Logique":
        L.append("::: attention Ne pas confondre")
        L.append("$\\Rightarrow$ ne marche que dans un sens : $x = 2 \\Rightarrow x^2 = 4$ est vrai, mais $x^2 = 4$ n’implique pas $x = 2$ (on peut avoir $x = -2$).")
        L.append(":::\n")
    if titre == "Ensembles":
        L.append("::: retenir $\\in$ ou $\\subset$ ?")
        L.append("$\\in$ relie un **élément** à un ensemble ($2 \\in \\mathbb{N}$) ; $\\subset$ relie deux **ensembles** ($\\mathbb{N} \\subset \\mathbb{Z}$).")
        L.append(":::\n")
    if titre == "Ensembles de nombres":
        L.append("::: retenir Inclusions")
        L.append("$$\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{D} \\subset \\mathbb{Q} \\subset \\mathbb{R} \\subset \\mathbb{C}$$")
        L.append(":::\n")

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit :", sum(len(p[2]) for p in PARTIES), "symboles,", len(PARTIES), "parties")
