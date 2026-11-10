# -*- coding: utf-8 -*-
"""Les 24 lettres grecques, partagées par generer.py et figures/figures.py.

(nom, prononciation si elle diffère de l'écriture, minuscule LaTeX, majuscule LaTeX, usages)
"""

LETTRES = [
    ("alpha", "", r"\alpha", r"\mathrm{A}", "angles ; coefficients ; racines d’un trinôme ; rayonnement α"),
    ("bêta", "", r"\beta", r"\mathrm{B}", "angles ; racines d’un trinôme ; rayonnement β"),
    ("gamma", "", r"\gamma", r"\Gamma", "angles ; rayonnement γ ; Γ : fonction gamma"),
    ("delta", "", r"\delta", r"\Delta", "Δ : discriminant, variation (Δt, Δx) ; δ : petite quantité"),
    ("epsilon", "epsilonne", r"\varepsilon", r"\mathrm{E}", "quantité aussi petite qu’on veut (limites) ; permittivité"),
    ("zêta", "dzêta", r"\zeta", r"\mathrm{Z}", "fonction zêta de Riemann"),
    ("êta", "", r"\eta", r"\mathrm{H}", "rendement ; viscosité"),
    ("thêta", "têta", r"\theta", r"\Theta", "angle ; température"),
    ("iota", "", r"\iota", r"\mathrm{I}", "très peu utilisée"),
    ("kappa", "", r"\kappa", r"\mathrm{K}", "courbure ; conductivité thermique"),
    ("lambda", "", r"\lambda", r"\Lambda", "longueur d’onde ; valeur propre ; paramètre d’une loi"),
    ("mu", "mu", r"\mu", r"\mathrm{M}", "préfixe micro (µm) ; moyenne ; coefficient de frottement"),
    ("nu", "nu", r"\nu", r"\mathrm{N}", "fréquence"),
    ("xi", "ksi", r"\xi", r"\Xi", "variable auxiliaire"),
    ("omicron", "omicronne", r"o", r"\mathrm{O}", "presque jamais utilisée (confusion avec o)"),
    ("pi", "", r"\pi", r"\Pi", "π ≈ 3,14159 ; Π : produit de plusieurs termes"),
    ("rhô", "rô", r"\rho", r"\mathrm{P}", "masse volumique ; coefficient de corrélation"),
    ("sigma", "", r"\sigma", r"\Sigma", "σ : écart type ; Σ : somme de plusieurs termes"),
    ("tau", "tô", r"\tau", r"\mathrm{T}", "constante de temps ; taux"),
    ("upsilon", "upsilonne", r"\upsilon", r"\Upsilon", "très peu utilisée"),
    ("phi", "fi", r"\varphi", r"\Phi", "angle, déphasage ; nombre d’or ; Φ : flux, loi normale"),
    ("khi", "ki", r"\chi", r"\mathrm{X}", "loi du khi-deux (χ²)"),
    ("psi", "psi", r"\psi", r"\Psi", "fonction d’onde (physique quantique)"),
    ("oméga", "", r"\omega", r"\Omega", "ω : vitesse angulaire, pulsation ; Ω : ohm, univers des possibles"),
]

assert len(LETTRES) == 24
