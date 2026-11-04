# -*- coding: utf-8 -*-
"""Validation de format des contenus 4ème avant intégration au site.

Usage : python valider_4e.py <slug> [<slug> ...]   (ex. : python valider_4e.py relatifs)
        python valider_4e.py all
Contrôles : structure des fichiers, catégories et numérotation des exercices
(l'ordre alphabétique des titres doit refléter la progression), difficultés,
présence des images référencées, marqueurs [IMAGE_n], parité des $, équilibre des <div>,
et règles de la 4ème : 6 questions minimum par exercice, chaque question corrigée
(titre, résultat), au moins une note « À retenir » ou « Erreur fréquente » par exercice,
aucun astérisque isolé (le site le transformerait en italique), aucune formule sur deux lignes.
Les formules elles-mêmes sont vérifiées par outils/verifier_mathjax.cjs.
"""
import re
import sys
from pathlib import Path

FRONT = Path(__file__).resolve().parents[4]
DIR_C = FRONT / "cours/cours_optitab/4e"
DIR_R = FRONT / "cours/resume/4e"
DIR_E = FRONT / "exercices/4e"
CATS = ["Découverte", "Entraînement", "Problème"]
MIN_Q = 6
ERREURS = []


def err(msg):
    ERREURS.append(msg)
    print("  [ERREUR]", msg)


def check_dollars(txt, ctx):
    if txt.count("$") % 2 != 0:
        err(f"{ctx} : nombre impair de '$' ({txt.count('$')})")
    for i, line in enumerate(txt.splitlines(), 1):
        if line.count("$") % 2:
            err(f"{ctx} : formule coupée sur deux lignes (ligne {i} du bloc)")
            break


def check_divs(txt, ctx):
    if txt.count("<div") != txt.count("</div>"):
        err(f"{ctx} : <div> non équilibrés ({txt.count('<div')} ouvrants / {txt.count('</div>')} fermants)")


def check_stars(txt, ctx):
    for i, line in enumerate(txt.splitlines(), 1):
        if line.count("**") % 2:
            err(f"{ctx} : gras '**' non refermé (ligne {i} du bloc)")
            break
        if "*" in line.replace("**", ""):
            err(f"{ctx} : astérisque isolé (ligne {i} du bloc) — le site le met en italique")
            break


def check_images(images, markers_src, img_dir, ctx):
    for f in images:
        if not (img_dir / f).exists():
            err(f"{ctx} : image absente du disque : {f}")
    marks = sorted({int(m) for m in re.findall(r"\[IMAGE_(\d+)\]", markers_src)})
    for m in marks:
        if m > len(images):
            err(f"{ctx} : marqueur [IMAGE_{m}] mais seulement {len(images)} image(s) déclarée(s)")
    for k in range(1, len(images) + 1):
        if k not in marks:
            err(f"{ctx} : image {k} déclarée mais aucun marqueur [IMAGE_{k}]")


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
    check_images(images, body, img_dir, ctx)
    if "4ème" not in raw[:raw.index("<div")]:
        err(f"{ctx} : l'en-tête ne mentionne pas la 4ème")
    return len(images)


def valider_exos(path, img_dir, ctx, minimum=21):
    raw = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"^===\s*$", raw, flags=re.M) if b.strip()]
    if len(blocks) < minimum:
        err(f"{ctx} : {len(blocks)} exercices (minimum {minimum})")
    titres = []
    nq_tot = 0
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
        if not all(p in b for p in ("Énoncé:", "Étapes:", "Solution:")):
            err(f"{bctx} : section manquante")
            continue
        im = re.search(r"^Images?:\s*(.+)$", b, re.M)
        images = [s.strip() for s in im.group(1).split(",")] if im else []
        check_images(images, b, img_dir, bctx)
        check_dollars(b, bctx)
        check_stars(b, bctx)
        enonce = b[b.index("Énoncé:"):b.index("Étapes:")]
        etapes = b[b.index("Étapes:"):b.index("Solution:")]
        solution = b[b.index("Solution:"):]
        nq = len(re.findall(r"\*\*Question\s+\d+ :", enonce))
        nq_tot += nq
        if nq < MIN_Q:
            err(f"{bctx} : seulement {nq} question(s) dans l'énoncé (minimum {MIN_Q})")
        parts = re.split(r"^\*\*Question\s+\d+ :.*\*\*$", etapes, flags=re.M)[1:]
        if len(parts) != nq:
            err(f"{bctx} : {nq} questions mais {len(parts)} corrections dans les étapes")
        for k, p in enumerate(parts, 1):
            if "**Résultat :**" not in p:
                err(f"{bctx} Q{k} : correction sans « Résultat »")
        if "💡 **À retenir :**" not in etapes and "⚠️ **Erreur fréquente :**" not in etapes:
            err(f"{bctx} : aucune note pédagogique (À retenir / Erreur fréquente)")
        nsol = len(re.findall(r"^\d+\. ", solution, flags=re.M))
        if nsol != nq:
            err(f"{bctx} : {nsol} lignes de solution pour {nq} questions")
    tri = sorted(titres, key=lambda t: t.casefold())
    if tri != titres:
        for a, b2 in zip(tri, titres):
            if a != b2:
                err(f"{ctx} : ordre alphabétique ≠ ordre pédagogique, premier écart : « {b2} » devrait venir après « {a} »")
                break
    if len(set(titres)) != len(titres):
        err(f"{ctx} : titres en double")
    return len(blocks), nq_tot


def valider(slug):
    print(f"--- {slug} ---")
    n0 = len(ERREURS)
    cours = DIR_C / f"cours_{slug}_4e.txt"
    fiche = DIR_R / f"resume_{slug}_4e.txt"
    exos = DIR_E / f"exercice_{slug}_4e.txt"
    nb, nq = "?", "?"
    for p, ctx, d in [(cours, "cours", DIR_C / "images"), (fiche, "fiche", DIR_C / "images")]:
        if p.exists():
            valider_page(p, d, f"{slug} {ctx}")
        else:
            err(f"{slug} : fichier manquant {p.name}")
    if exos.exists():
        nb, nq = valider_exos(exos, DIR_E / "images", f"{slug} exercices")
    else:
        err(f"{slug} : fichier manquant {exos.name}")
    print(f"    => {nb} exercices, {nq} questions, {'OK' if len(ERREURS) == n0 else 'ERREURS'}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["all"]:
        args = sorted({re.match(r"exercice_(.+)_4e", p.stem).group(1)
                       for p in DIR_E.glob("exercice_*_4e.txt")})
    for slug in args:
        valider(slug)
    print(f"\n{len(ERREURS)} erreur(s) au total.")
    sys.exit(1 if ERREURS else 0)
