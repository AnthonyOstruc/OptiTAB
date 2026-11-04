# -*- coding: utf-8 -*-
"""Met en ligne un cours et une fiche de lycée réécrits de zéro (base de PRODUCTION).

Exécution : manage.py shell -c "import sys; sys.argv=['x','<slug>', ...]; exec(open(r'.../v2/integrer_v2.py', encoding='utf-8').read())"
- remplace le titre et le contenu du cours, le titre et le résumé de la fiche (mêmes objets, mêmes identifiants) ;
- images : positions 1..n remplacées par les nouvelles figures, positions au-delà supprimées
  (les fichiers restent sur S3 ; l'ancien état est dans frontend/cours/sauvegardes_lycee/) ;
- ne touche ni aux notions, ni aux exercices.
"""
import importlib.util
import os
import re
import sys
from pathlib import Path

from django.apps import apps
from django.core.files import File
from django.db import transaction

sys.stdout.reconfigure(encoding="utf-8")
V2 = Path(r"C:/Users/SWEELCO-AT/Desktop/SWINDER/OptiTABV2/frontend/cours/lycee/v2")
IMAGES = V2.parent / "images"
M = {m.__name__: m for m in apps.get_models()}
Cours, Fiche, CI, SI = M["Cours"], M["SynthesisSheet"], M["CoursImage"], M["SynthesisImage"]
FK_SI = [f.name for f in SI._meta.fields if f.is_relation][0]
_s = importlib.util.spec_from_file_location("registre", V2 / "registre.py")
_r = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_r)
REG = _r.R


def entete(chemin):
    brut = chemin.read_text(encoding="utf-8")
    titre = re.search(r"^Titre:\s*(.+)$", brut, re.M).group(1).strip()
    imgs = re.search(r"^Images:\s*(.*)$", brut, re.M)
    images = [s.strip() for s in imgs.group(1).split(",") if s.strip()] if imgs else []
    return titre, images


def attacher(model, fk, owner, pos, chemin, alt):
    ex = model.objects.filter(**{fk: owner, "position": pos}).first()
    if ex:
        if os.path.basename(ex.image.name).startswith(chemin.stem):
            if ex.alt_text != alt:
                ex.alt_text = alt
                ex.save(update_fields=["alt_text"])
            return "="
        ex.delete()
    obj = model(**{fk: owner}, position=pos, alt_text=alt)
    with open(chemin, "rb") as fh:
        obj.image.save(chemin.name, File(fh), save=True)
    return "+"


def texte_alt(fichier, contexte):
    base = re.sub(r"\.png$", "", fichier)
    base = re.sub(r"^(2nd|1er|term|bases)_", "", base).replace("_", " ")
    return f"Figure {contexte} : {base}"[:255]


def integrer(slug):
    r = REG[slug]
    cours, fiche = Cours.objects.get(id=r["cours"]), Fiche.objects.get(id=r["fiche"])
    assert cours.notion_id == r["notion"] == fiche.notion_id, f"{slug} : notion incohérente"
    titre_c, img_c = entete(V2 / "cours" / f"{slug}.txt")
    titre_f, img_f = entete(V2 / "fiches" / f"{slug}.txt")
    html_c = (V2 / "sortie" / f"{slug}_cours.html").read_text(encoding="utf-8")
    html_f = (V2 / "sortie" / f"{slug}_fiche.html").read_text(encoding="utf-8")
    st = {"+": 0, "=": 0, "-": 0}
    with transaction.atomic():
        for k, f in enumerate(img_c, 1):
            st[attacher(CI, "cours", cours, k, IMAGES / f, texte_alt(f, "du cours"))] += 1
        st["-"] += CI.objects.filter(cours=cours, position__gt=len(img_c)).delete()[0]
        cours.titre, cours.contenu = titre_c, html_c
        cours.save(update_fields=["titre", "contenu"])
        for k, f in enumerate(img_f, 1):
            st[attacher(SI, FK_SI, fiche, k, IMAGES / f, texte_alt(f, "de la fiche"))] += 1
        st["-"] += SI.objects.filter(**{FK_SI: fiche, "position__gt": len(img_f)}).delete()[0]
        fiche.titre, fiche.summary = titre_f, html_f
        fiche.save(update_fields=["titre", "summary"])
    print(f"[{slug}] cours {cours.id} « {titre_c} » ({len(html_c)} car.) ; fiche {fiche.id} ({len(html_f)} car.) ; "
          f"images +{st['+']} ={st['=']} -{st['-']}")


for s in sys.argv[1:]:
    integrer(s)
