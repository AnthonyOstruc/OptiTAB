# -*- coding: utf-8 -*-
"""Contrôle en base de PRODUCTION des chapitres réécrits (lecture seule).

Exécution : manage.py shell -c "exec(open(r'.../v2/verifier_prod.py', encoding='utf-8').read())"
Pour chaque slug ayant ses fichiers v2 : contenu en base == sortie générée, images 1..n présentes
avec le bon nom de fichier, aucune image en trop, marqueurs [IMAGE_k] cohérents.
"""
import importlib.util
import os
import re
import sys
from pathlib import Path

from django.apps import apps

sys.stdout.reconfigure(encoding="utf-8")
V2 = Path(r"C:/Users/SWEELCO-AT/Desktop/SWINDER/OptiTABV2/frontend/cours/lycee/v2")
M = {m.__name__: m for m in apps.get_models()}
Cours, Fiche, CI, SI = M["Cours"], M["SynthesisSheet"], M["CoursImage"], M["SynthesisImage"]
FK_SI = [f.name for f in SI._meta.fields if f.is_relation][0]
_s = importlib.util.spec_from_file_location("registre", V2 / "registre.py")
_r = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_r)


def images_attendues(chemin):
    m = re.search(r"^Images:\s*(.*)$", chemin.read_text(encoding="utf-8"), re.M)
    return [s.strip() for s in m.group(1).split(",") if s.strip()] if m else []


def controle(objet, contenu, sortie, model, fk, attendues):
    pb = []
    if contenu != sortie.read_text(encoding="utf-8"):
        pb.append("contenu différent de la sortie")
    imgs = list(model.objects.filter(**{fk: objet}).order_by("position"))
    if [i.position for i in imgs] != list(range(1, len(attendues) + 1)):
        pb.append(f"positions {[i.position for i in imgs]}")
    for i, f in zip(imgs, attendues):
        if not os.path.basename(i.image.name).startswith(Path(f).stem):
            pb.append(f"image {i.position} = {os.path.basename(i.image.name)} (attendu {f})")
    marq = sorted({int(k) for k in re.findall(r"\[IMAGE_(\d+)\]", contenu)})
    if marq != list(range(1, len(attendues) + 1)):
        pb.append(f"marqueurs {marq}")
    if "🏆" not in contenu:
        pb.append("encadré final absent")
    return pb


ok = 0
for slug, r in _r.R.items():
    fc, ff = V2 / "cours" / f"{slug}.txt", V2 / "fiches" / f"{slug}.txt"
    if not (fc.exists() and ff.exists()):
        continue
    c, f = Cours.objects.get(id=r["cours"]), Fiche.objects.get(id=r["fiche"])
    pb = controle(c, c.contenu, V2 / "sortie" / f"{slug}_cours.html", CI, "cours", images_attendues(fc))
    pb += ["fiche : " + p for p in controle(f, f.summary, V2 / "sortie" / f"{slug}_fiche.html", SI, FK_SI,
                                           images_attendues(ff))]
    print(f"{'OK ' if not pb else 'ERR'} {slug:30s} cours {c.id} « {c.titre} »" + ("" if not pb else " → " + " ; ".join(pb)))
    ok += not pb
print(f"{ok} chapitre(s) conformes")
