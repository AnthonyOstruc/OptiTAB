# -*- coding: utf-8 -*-
"""Remise en forme des cours de lycée au format OptiTAB 4ème — fonctions communes.

Principe : le texte des cours n'est jamais réécrit automatiquement. On ne fait que
  1. recolorer les encadrés selon leur rôle (déduit de leur titre) ;
  2. remplacer l'en-tête (tout ce qui précède le premier <h2>) par un en-tête rédigé à la main ;
  3. insérer des figures [IMAGE_n] et des encadrés rédigés à la main à des ancres précises ;
  4. ajouter l'encadré final « 🏆 L'essentiel ».
"""
import importlib.util
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SOURCE, SORTIE, IMAGES, SPECS = (RACINE / d for d in ("source", "sortie", "images", "specs"))

ROLES = {
    "def": ("#e8f4fd", "#3498db"),
    "tip": ("#ecfdf5", "#10b981"),
    "warn": ("#fff8dc", "#ffa500"),
    "ex": ("#f8f9fa", "#6c757d"),
    "demo": ("#e0f2f1", "#00897b"),
    "bonus": ("#fef3c7", "#f59e0b"),
}
MOTS = [  # ordre important : le premier rôle reconnu l'emporte
    ("demo", ("démonstration", "justification", "preuve")),
    ("bonus", ("bonus", "approfondissement", "pour aller plus loin", "🌟", "culture")),
    ("warn", ("erreur", "piège", "attention", "important", "⚠", "❌", "à éviter", "ne pas confondre")),
    ("def", ("définition", "théorème", "propriété", "notation", "formule", "récapitulatif", "retenir",
             "idée clé", "syntaxe", "vocabulaire", "règle", "corollaire", "lemme", "conséquence", "rappel")),
    ("ex", ("exemple", "application", "solution", "résultat", "étape", "vérification", "données", "cas ",
            "sortie", "problème", "situation")),
    ("tip", ("méthode", "capacité", "conseil", "interprétation", "💡", "principe", "démarche", "astuce",
             "stratégie", "remarque", "explication", "idée", "motivation", "à suivre", "mini-formulaire",
             "algorithme", "nouveau")),
]
COULEUR_ROLE = {  # rôle par défaut selon la couleur d'origine (encadré sans titre reconnu)
    "#3498db": "def", "#9c27b0": "def", "#9333ea": "def", "#dc2626": "warn", "#ef4444": "warn",
    "#ffa500": "warn", "#ffc107": "warn", "#e11d48": "warn", "#10b981": "tip", "#f59e0b": "tip",
    "#4d6df3": "tip", "#4f46e5": "tip", "#00897b": "tip", "#6c757d": "ex",
}
TAG = re.compile(r"(<div\b[^>]*>|</div>)")


def style_de(tag):
    m = re.search(r'style="([^"]*)"', tag)
    return m.group(1) if m else ""


def proprietes(style):
    out = []
    for p in style.split(";"):
        if ":" in p:
            k, v = p.split(":", 1)
            out.append((k.strip().lower(), v.strip()))
    return out


def titre_de(texte):
    m = re.search(r"<strong>(.*?)</strong>", texte[:600], re.S)
    if not m:
        return ""
    t = re.sub(r"\$[^$]*\$", " ", re.sub(r"<[^>]+>", "", m.group(1)))
    return t.strip().lower()


def role_de(titre, couleur):
    if titre.startswith("théorème") or titre.startswith("propriété") or titre.startswith("définition"):
        return "def"
    if titre.startswith("💡") and not any(m in titre for m in ("propriété", "théorème", "définition")):
        return "tip"
    if "démonstration" not in titre and any(m in titre for m in ("méthode", "stratégie", "capacité", "conseil")):
        return "tip"
    for role, mots in MOTS:
        if any(m in titre for m in mots):
            return role
    return COULEUR_ROLE.get(couleur.lower(), "def")


def est_encadre(style):
    return re.search(r"border-left:\s*\d+px solid (#[0-9a-fA-F]{3,6})", style)


def est_formule(style):
    return re.search(r"border:\s*\d+px solid (#[0-9a-fA-F]{3,6})", style) and "text-align:center" in style.replace(" ", "")


def style_role(role, ancien):
    bg, bd = ROLES[role]
    garde = [f"{k}:{v}" for k, v in proprietes(ancien)
             if k not in ("background", "background-color", "border-left", "border", "border-radius", "padding",
                          "margin")]
    return "; ".join([f"background:{bg}", f"border-left:6px solid {bd}", "border-radius:6px", "padding:15px",
                      "margin:12px 0"] + garde) + ";"


def style_formule(role, ancien):
    bg, bd = ROLES[role]
    s = re.sub(r"background:\s*#[0-9a-fA-F]{3,6}", f"background:{bg}", ancien)
    return re.sub(r"border:\s*(\d+)px solid #[0-9a-fA-F]{3,6}", rf"border:\1px solid {bd}", s)


def harmoniser(html, journal=None, forces=None):
    """Recolore chaque encadré selon son rôle ; renvoie le HTML (texte inchangé).
    forces = {début de titre (minuscules): rôle} pour corriger un classement automatique."""
    toks = TAG.split(html)
    pile = []
    section = ""
    for i, tok in enumerate(toks):
        h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", tok, re.S)
        if h2:
            section = re.sub(r"<[^>]+>", "", h2[-1]).lower()
        if tok.startswith("<div"):
            st = style_de(tok)
            enc = est_encadre(st)
            if enc:
                titre = titre_de(toks[i + 1] if i + 1 < len(toks) else "")
                role = role_de(titre, enc.group(1))
                if "démonstration" in section and role not in ("warn", "bonus"):
                    role = "demo"
                for debut, r in (forces or {}).items():
                    if titre.startswith(debut):
                        role = r
                toks[i] = tok.replace(st, style_role(role, st))
                pile.append(role)
                if journal is not None:
                    journal.append((role, titre[:50]))
            elif est_formule(st) and any(pile):
                role = [r for r in pile if r][-1]
                toks[i] = tok.replace(st, style_formule(role, st))
                pile.append(None)
            else:
                pile.append(None)
        elif tok == "</div>":
            pile.pop()
    assert not pile, "balises <div> non équilibrées"
    return "".join(toks)


def blocs(html):
    """Liste des <div> : (début, fin après </div>, style)."""
    out, pile = [], []
    for m in TAG.finditer(html):
        if m.group(0).startswith("<div"):
            pile.append((m.start(), style_de(m.group(0))))
        else:
            d, st = pile.pop()
            out.append((d, m.end(), st))
    return out


def position(html, ancre, mode):
    i = html.find(ancre)
    assert i >= 0, f"ancre introuvable : {ancre[:60]}"
    assert html.find(ancre, i + 1) < 0, f"ancre ambiguë : {ancre[:60]}"
    if mode == "apres_texte":
        return i + len(ancre)
    contenants = [(d, f, st) for d, f, st in blocs(html) if d <= i < f]
    if mode in ("apres_bloc", "avant_bloc"):
        cand = [b for b in contenants if est_encadre(b[2])] or contenants
        d, f, _ = max(cand, key=lambda b: b[0])
        return f if mode == "apres_bloc" else d
    if mode == "fin_carte":
        cand = [b for b in contenants if "#e1e8ed" in b[2]]
        d, f, _ = max(cand, key=lambda b: b[0])
        return f - len("</div>")
    raise ValueError(mode)


def inserer(html, ajouts):
    """ajouts = [(ancre, mode, fragment)] ; insertion de la fin vers le début pour garder les positions."""
    pos = [(position(html, a, m), frag) for a, m, frag in ajouts]
    for p, frag in sorted(pos, key=lambda x: -x[0]):
        html = html[:p] + "\n" + frag + "\n" + html[p:]
    return html


def charger_spec(slug):
    sp = importlib.util.spec_from_file_location(slug, SPECS / f"{slug}.py")
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


def remplacer_entete(html, entete):
    d = html.find(">", html.find("<div")) + 1
    h2 = html.find("<h2")
    assert 0 < d < h2
    return html[:d] + "\n" + entete.strip() + "\n" + html[h2:]


def ajouter_fin(html, fragment):
    k = html.rstrip().rfind("</div>")
    return html[:k] + fragment.strip() + "\n" + html[k:]


def max_image(html):
    return max([int(n) for n in re.findall(r"\[IMAGE_(\d+)\]", html)] or [0])


def verifier(html, nom):
    err = []
    if len(re.findall(r"<div\b", html)) != html.count("</div>"):
        err.append("div non équilibrés")
    for k, ligne in enumerate(html.splitlines(), 1):
        if ligne.count("$") % 2:
            err.append(f"ligne {k} : nombre impair de $")
    nums = [int(n) for n in re.findall(r"\[IMAGE_(\d+)\]", html)]
    if len(nums) != len(set(nums)):
        err.append("marqueur [IMAGE_n] en double")
    for e in err:
        print(f"  [ERREUR] {nom} : {e}")
    return not err
