# -*- coding: utf-8 -*-
"""Met en ligne un cours et une fiche de lycée remis en forme (base de PRODUCTION).

Exécution : manage.py shell -c "import sys; sys.argv=['x','<slug>', ...]; exec(open(r'.../integrer_lycee.py', encoding='utf-8').read())"
Sécurités : refuse si le cours ou la fiche ont changé en base depuis l'extraction (source/) ;
            ne touche ni aux titres, ni aux identifiants, ni aux exercices ; garde les images existantes du cours.
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
RACINE = Path(r"C:/Users/SWEELCO-AT/Desktop/SWINDER/OptiTABV2/frontend/cours/lycee")
M = {m.__name__: m for m in apps.get_models()}
Cours, Fiche, CI, SI = M["Cours"], M["SynthesisSheet"], M["CoursImage"], M["SynthesisImage"]
FK_SI = [f.name for f in SI._meta.fields if f.is_relation][0]


def spec(slug):
    sp = importlib.util.spec_from_file_location(slug, RACINE / "specs" / f"{slug}.py")
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


def alt(fichier, quoi):
    base = re.sub(r"\.png$", "", fichier).split("_", 1)[-1].replace("_", " ")
    return f"Schéma {quoi} : {base}"[:255]


def attacher(model, fk, owner, pos, chemin, texte):
    assert chemin.exists(), chemin
    ex = model.objects.filter(**{fk: owner, "position": pos}).first()
    if ex:
        if os.path.basename(ex.image.name).startswith(chemin.stem):
            return "="
        ex.delete()
    obj = model(**{fk: owner}, position=pos, alt_text=texte)
    with open(chemin, "rb") as fh:
        obj.image.save(chemin.name, File(fh), save=True)
    return "+"


def integrer(slug):
    sp = spec(slug)
    cours = Cours.objects.get(id=sp.COURS_ID)
    fiche = Fiche.objects.get(id=sp.FICHE_ID)
    assert fiche.notion_id == cours.notion_id, "la fiche n'appartient pas à la même notion"
    nouveau_c = (RACINE / "sortie" / f"{slug}_cours.html").read_text(encoding="utf-8")
    nouveau_f = (RACINE / "sortie" / f"{slug}_fiche.html").read_text(encoding="utf-8")
    src_c = (RACINE / "source" / f"cours_{cours.id}.html").read_text(encoding="utf-8")
    src_f = (RACINE / "source" / f"fiche_{fiche.id}.html").read_text(encoding="utf-8")
    deja = cours.contenu == nouveau_c
    assert deja or cours.contenu == src_c, f"cours {cours.id} modifié en base depuis l'extraction : arrêt"
    assert fiche.summary == nouveau_f or (fiche.summary or "") == src_f, f"fiche {fiche.id} modifiée : arrêt"
    n0 = max([int(n) for n in re.findall(r"\[IMAGE_(\d+)\]", src_c)] or [0])
    occupees = set(CI.objects.filter(cours=cours, position__gt=n0).values_list("position", flat=True))
    stats = {"+": 0, "=": 0}
    with transaction.atomic():
        for k, fig in enumerate(sp.FIGURES, n0 + 1):
            assert deja or k not in occupees, f"position {k} déjà occupée par une autre image du cours"
            stats[attacher(CI, "cours", cours, k, RACINE / "images" / fig["fichier"], alt(fig["fichier"], "du cours"))] += 1
        cours.contenu = nouveau_c
        cours.save(update_fields=["contenu"])
        for k, f in enumerate(sp.FICHE_IMAGES, 1):
            stats[attacher(SI, FK_SI, fiche, k, RACINE / "images" / f, alt(f, "de la fiche"))] += 1
        SI.objects.filter(**{FK_SI: fiche, "position__gt": len(sp.FICHE_IMAGES)}).delete()
        fiche.summary = nouveau_f
        fiche.save(update_fields=["summary"])
    marq_c = sorted(int(n) for n in re.findall(r"\[IMAGE_(\d+)\]", nouveau_c))
    pos_c = sorted(CI.objects.filter(cours=cours).values_list("position", flat=True))
    assert set(marq_c) <= set(pos_c), f"marqueurs sans image : {set(marq_c) - set(pos_c)}"
    print(f"[{slug}] cours {cours.id} « {cours.titre} » et fiche {fiche.id} mis à jour ; "
          f"images +{stats['+']}/={stats['=']} ; marqueurs cours {marq_c}")


for s in sys.argv[1:]:
    integrer(s)
