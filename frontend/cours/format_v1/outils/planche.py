# -*- coding: utf-8 -*-
"""Planches-contacts des images en ligne d'une notion, pour les relire d'un coup d'œil.

    python planche.py <dossier_notion> [--par 12] [--seulement-appelees]

Télécharge (une fois) les images listées dans source_en_ligne/meta.json vers
<dossier>/images_en_ligne/, puis compose <dossier>/planches/planche_NN.png :
vignettes numérotées « cours 279 · 2 », « ex 3251 · 1 »… (modèle, id, position),
sur fond gris clair pour voir les bords blancs. Lire ensuite les planches avec
l'outil Read (une planche = 12 images par défaut).
"""
import json
import re
import sys
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

LARGEUR_VIGNETTE = 420
HAUTEUR_VIGNETTE = 300
COLONNES = 3


def police(taille):
    for nom in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(nom, taille)
        except OSError:
            continue
    return ImageFont.load_default()


def appels(dossier):
    """Positions [IMAGE_N] appelées dans les textes convertis, par (genre, id)."""
    out = set()
    for f in dossier.glob("cours_*.txt"):
        cid = int(re.search(r"\d+", f.stem).group())
        out |= {("cours", cid, int(n)) for n in re.findall(r"\[IMAGE_(\d+)\]", f.read_text(encoding="utf-8"))}
    for f in dossier.glob("fiche_*.txt"):
        fid = int(re.search(r"\d+", f.stem).group())
        out |= {("fiche", fid, int(n)) for n in re.findall(r"\[IMAGE_(\d+)\]", f.read_text(encoding="utf-8"))}
    ex = dossier / "exercices.txt"
    if ex.exists():
        for bloc in re.split(r"^===[ \t]*$", ex.read_text(encoding="utf-8"), flags=re.M):
            m = re.search(r"^Id:\s*(\d+)", bloc, re.M)
            if m:
                out |= {("ex", int(m.group(1)), int(n)) for n in re.findall(r"\[IMAGE_(\d+)\]", bloc)}
    return out


def images(dossier):
    meta = json.loads((dossier / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
    for genre, cle in (("cours", "cours"), ("fiche", "fiches"), ("ex", "exercices")):
        for it in meta[cle]:
            for im in it["images"]:
                yield genre, it["id"], im


def telecharger(dossier, im):
    cache = dossier / "images_en_ligne"
    cache.mkdir(exist_ok=True)
    cible = cache / Path(im["nom"]).name
    if not cible.exists():
        r = requests.get(im["url"], timeout=60)
        r.raise_for_status()
        cible.write_bytes(r.content)
    return cible


def composer(liste, sortie):
    lignes = (len(liste) + COLONNES - 1) // COLONNES
    planche = Image.new("RGB", (COLONNES * (LARGEUR_VIGNETTE + 16) + 16, lignes * (HAUTEUR_VIGNETTE + 44) + 16), (226, 230, 238))
    dessin = ImageDraw.Draw(planche)
    f = police(17)
    for k, (etiquette, chemin) in enumerate(liste):
        x = 16 + (k % COLONNES) * (LARGEUR_VIGNETTE + 16)
        y = 16 + (k // COLONNES) * (HAUTEUR_VIGNETTE + 44)
        dessin.text((x, y), etiquette, fill=(27, 60, 142), font=f)
        try:
            img = Image.open(chemin).convert("RGB")
        except Exception as exc:  # noqa: BLE001
            dessin.text((x, y + 40), f"illisible : {exc}"[:50], fill=(200, 0, 0), font=f)
            continue
        w, h = img.size
        img.thumbnail((LARGEUR_VIGNETTE, HAUTEUR_VIGNETTE), Image.LANCZOS)
        planche.paste(img, (x, y + 26))
        dessin.text((x + LARGEUR_VIGNETTE - 110, y), f"{w}×{h}", fill=(107, 115, 133), font=police(14))
    planche.save(sortie)


def main():
    args = sys.argv[1:]
    dossier = Path(args[0])
    par = int(args[args.index("--par") + 1]) if "--par" in args else 12
    seulement = "--seulement-appelees" in args
    utiles = appels(dossier)
    liste = []
    for genre, oid, im in images(dossier):
        if seulement and (genre, oid, im["position"]) not in utiles:
            continue
        etiquette = f"{genre} {oid} · {im['position']}" + ("" if (genre, oid, im["position"]) in utiles else "  (non appelée)")
        liste.append((etiquette, telecharger(dossier, im)))
    sortie = dossier / "planches"
    sortie.mkdir(exist_ok=True)
    for vieux in sortie.glob("planche_*.png"):
        vieux.unlink()
    for k in range(0, len(liste), par):
        composer(liste[k:k + par], sortie / f"planche_{k // par + 1:02d}.png")
    print(f"{len(liste)} image(s), {(len(liste) + par - 1) // par} planche(s) dans {sortie}")


if __name__ == "__main__":
    main()
