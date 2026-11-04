# -*- coding: utf-8 -*-
"""Validation de format des contenus 3ème avant intégration au site.

Usage : python valider_3e.py <slug> [<slug> ...]   (ex. : python valider_3e.py fractions)
        python valider_3e.py all
Contrôles : structure des fichiers, catégories et numérotation des exercices
(l'ordre alphabétique des titres doit refléter la progression), difficultés,
présence des images référencées, marqueurs [IMAGE_n], parité des $, équilibre des <div>.
"""
import re
import sys
from pathlib import Path

FRONT = Path(__file__).resolve().parents[4]
DIR_C = FRONT / "cours/cours_optitab/3e"
DIR_R = FRONT / "cours/resume/3e"
DIR_E = FRONT / "exercices/3e"
CATS = ["Découverte", "Entraînement", "Problème", "Type brevet"]
ERREURS = []


def err(msg):
    ERREURS.append(msg)
    print("  [ERREUR]", msg)


def check_dollars(txt, ctx):
    # parité des $ délimiteurs (les formules sont $...$ ; $\\$ compte 2 $) ;
    # un \$ (dollar littéral, ex. référence de tableur \$D\$2) n'est pas un délimiteur
    n = sum(1 for m in re.finditer(r"(\\*)\$", txt) if len(m.group(1)) % 2 == 0)
    if n % 2 != 0:
        err(f"{ctx} : nombre impair de '$' délimiteurs ({n})")
    # le moteur du site transforme *texte* en italique : un astérisque isolé est interdit
    if re.sub(r"\*\*", "", txt).count("*"):
        err(f"{ctx} : astérisque isolé (écrire &#42; ou ×)")


def check_tables(txt, ctx):
    """Tableaux HTML : gabarit OptiTAB bordé (cf. outils/tableaux_3e.py)."""
    for m in re.finditer(r"<table\b.*?</table>", txt, re.S):
        tab = m.group(0)
        ouv = re.match(r"<table[^>]*>", tab).group(0)
        if "border:2px solid #3498db" not in ouv or "border-collapse:collapse" not in ouv:
            err(f"{ctx} : tableau sans bordure extérieure / border-collapse (lancer outils/tableaux_3e.py)")
        if any("border:" not in c for c in re.findall(r"<t[dh]\b[^>]*>", tab)):
            err(f"{ctx} : cellule de tableau sans bordure")
        if "overflow-x:auto" not in txt[max(0, m.start() - 80):m.start()]:
            err(f"{ctx} : tableau sans conteneur défilant (mobile)")


def check_corriges(etapes, ctx):
    """Chaque question corrigée doit expliquer la démarche (Méthode ou Étape), pas seulement un résultat."""
    morceaux = re.split(r"^\*\*[^\n]*\*\*[ \t]*$", etapes, flags=re.M)[1:]
    titres = re.findall(r"^\*\*([^\n]*)\*\*[ \t]*$", etapes, flags=re.M)
    for titre, corps in zip(titres, morceaux):
        puces = [p for p in re.findall(r"●\s+\*\*([^*:]+?)\s*:\*\*", corps)
                 if not p.startswith(("💡", "⚠"))]
        if puces == ["Résultat"]:
            err(f"{ctx} : corrigé sans explication (« {titre[:50]} ») — ajouter une Méthode")


def check_divs(txt, ctx):
    if txt.count("<div") != txt.count("</div>"):
        err(f"{ctx} : <div> non équilibrés ({txt.count('<div')} ouvrants / {txt.count('</div>')} fermants)")


def check_images(images, markers_src, img_dir, ctx):
    for f in images:
        if not (img_dir / f).exists():
            err(f"{ctx} : image absente du disque : {f}")
    marks = sorted({int(m) for m in re.findall(r"\[IMAGE_(\d+)\]", markers_src)})
    for m in marks:
        if m > len(images):
            err(f"{ctx} : marqueur [IMAGE_{m}] mais seulement {len(images)} image(s) déclarée(s)")
    if images and not marks:
        err(f"{ctx} : images déclarées mais aucun marqueur [IMAGE_n]")


def header_field(raw, name):
    m = re.search(rf"^{name}:\s*(.+)$", raw, re.M)
    return m.group(1).strip() if m else None


def valider_page(path, img_dir, ctx):
    raw = path.read_text(encoding="utf-8")
    if not header_field(raw, "Titre"):
        err(f"{ctx} : champ Titre manquant")
    imgs_f = header_field(raw, "Images")
    images = [s.strip() for s in imgs_f.split(",")] if imgs_f else []
    body = raw[raw.index("<div"):]
    check_dollars(body, ctx)
    check_divs(body, ctx)
    check_tables(body, ctx)
    check_images(images, body, img_dir, ctx)
    return len(images)


def valider_exos(path, img_dir, ctx, minimum=20):
    raw = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"^===\s*$", raw, flags=re.M) if b.strip()]
    if len(blocks) < minimum:
        err(f"{ctx} : {len(blocks)} exercices (minimum {minimum})")
    titres = []
    for i, b in enumerate(blocks, 1):
        bctx = f"{ctx} exo {i}"
        first = b.splitlines()[0]
        if not first.startswith("=== "):
            err(f"{bctx} : première ligne sans '=== '")
            continue
        titre = first[4:].strip()
        titres.append(titre)
        cat = titre.split(" - ")[0]
        if cat not in CATS:
            err(f"{bctx} : catégorie inconnue « {cat} »")
        m = re.search(r"^Difficulté:\s*(\w+)$", b, re.M)
        if not m or m.group(1) not in ("easy", "medium", "hard"):
            err(f"{bctx} : difficulté absente ou invalide")
        for part in ("Énoncé:", "Étapes:", "Solution:"):
            if part not in b:
                err(f"{bctx} : section manquante {part}")
        im = re.search(r"^Images?:\s*(.+)$", b, re.M)
        images = [s.strip() for s in im.group(1).split(",")] if im else []
        check_images(images, b, img_dir, bctx)
        check_dollars(b, bctx)
        check_tables(b, bctx)
        if re.search(r"\\quad.*\\quad.*\\quad", b):
            err(f"{bctx} : pseudo-tableau aligné avec des espaces (utiliser fig3e.tableau)")
        if "Étapes:" in b and "Solution:" in b:
            check_corriges(b[b.index("Étapes:"):b.index("Solution:")], bctx)
        if "Étapes:" in b and not re.search(r"💡|⚠️", b[b.index("Étapes:"):]):
            err(f"{bctx} : aucune note pédagogique (💡 À retenir / ⚠️ Erreur fréquente)")
        # règle utilisateur (2026-10-27) : exercices complets — jamais une seule
        # question ; au moins 4 questions (5 si questions indépendantes)
        enonce_part = b[b.index("Énoncé:"):b.index("Étapes:")] if "Énoncé:" in b and "Étapes:" in b else b
        nq = len(re.findall(r"\*\*Question\s+\d+", enonce_part))
        if nq < 4:
            err(f"{bctx} : seulement {nq} question(s) dans l'énoncé (minimum 4, ou 5 si indépendantes)")
    # l'ordre alphabétique (tri du site) doit être l'ordre des blocs du fichier
    tri = sorted(titres, key=lambda t: t.casefold())
    if tri != titres:
        for a, b2 in zip(tri, titres):
            if a != b2:
                err(f"{ctx} : ordre alphabétique ≠ ordre pédagogique, premier écart : « {b2} » devrait venir après « {a} »")
                break
    if len(set(titres)) != len(titres):
        err(f"{ctx} : titres en double")
    return len(blocks)


def valider(slug):
    print(f"--- {slug} ---")
    n0 = len(ERREURS)
    cours = DIR_C / f"cours_{slug}_3e.txt"
    fiche = DIR_R / f"resume_{slug}_3e.txt"
    exos = DIR_E / f"exercice_{slug}_3e.txt"
    nb = "?"
    if slug == "brevet":
        exos = DIR_E / "exercice_brevet_3e.txt"
        if exos.exists():
            nb = valider_exos(exos, DIR_E / "images", "sujets brevet", minimum=10)
        else:
            err("fichier sujets brevet manquant")
        for p, ctx in [(cours, "brevet cours"), (fiche, "brevet fiche")]:
            if p.exists():
                valider_page(p, DIR_C / "images", ctx)
        print(f"    => {nb} sujets, {'OK' if len(ERREURS) == n0 else 'ERREURS'}")
        return
    for p, ctx, d in [(cours, "cours", DIR_C / "images"), (fiche, "fiche", DIR_C / "images")]:
        if p.exists():
            valider_page(p, d, f"{slug} {ctx}")
        else:
            err(f"{slug} : fichier manquant {p.name}")
    if exos.exists():
        nb = valider_exos(exos, DIR_E / "images", f"{slug} exercices")
    else:
        err(f"{slug} : fichier manquant {exos.name}")
    print(f"    => {nb} exercices, {'OK' if len(ERREURS) == n0 else 'ERREURS'}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["all"]:
        args = sorted({re.match(r"exercice_(.+)_3e", p.stem).group(1)
                       for p in DIR_E.glob("exercice_*_3e.txt")})
    for slug in args:
        valider(slug)
    print(f"\n{len(ERREURS)} erreur(s) au total.")
    sys.exit(1 if ERREURS else 0)
