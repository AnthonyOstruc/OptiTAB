# -*- coding: utf-8 -*-
"""Copie depuis la base (lecture seule) les cours et fiches de lycée vers source/, et l'adresse des images existantes.

Exécution : manage.py shell -c "exec(open(r'.../lycee/outils/extraire.py', encoding='utf-8').read())"
"""
import json
import sys
from pathlib import Path

from django.apps import apps

sys.stdout.reconfigure(encoding="utf-8")
RACINE = Path(r"C:/Users/SWEELCO-AT/Desktop/SWINDER/OptiTABV2/frontend/cours/lycee")
M = {m.__name__: m for m in apps.get_models()}
Cours, Fiche, CI, SI = M["Cours"], M["SynthesisSheet"], M["CoursImage"], M["SynthesisImage"]
fk_si = [f.name for f in SI._meta.fields if f.is_relation][0]
inventaire, images = [], {}
for c in Cours.objects.filter(notion__theme__contexte__niveau_id__in=[18, 19, 20]).select_related("notion__theme"):
    (RACINE / "source" / f"cours_{c.id}.html").write_text(c.contenu, encoding="utf-8")
    images[f"cours_{c.id}"] = {str(i.position): i.image.url for i in CI.objects.filter(cours=c)}
    fiches = list(Fiche.objects.filter(notion=c.notion))
    for f in fiches:
        (RACINE / "source" / f"fiche_{f.id}.html").write_text(f.summary or "", encoding="utf-8")
        images[f"fiche_{f.id}"] = {str(i.position): i.image.url for i in SI.objects.filter(**{fk_si: f})}
    inventaire.append(dict(niveau=c.notion.theme.contexte.niveau_id, contexte=c.notion.theme.contexte_id,
                           theme=c.notion.theme.titre, notion=c.notion_id, titre_notion=c.notion.titre, cours=c.id,
                           titre_cours=c.titre, fiches=[f.id for f in fiches], longueur=len(c.contenu)))
(RACINE / "images" / "existantes.json").write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
(RACINE / "source" / "inventaire.json").write_text(json.dumps(inventaire, ensure_ascii=False, indent=1),
                                                    encoding="utf-8")
print(len(inventaire), "cours extraits ;", sum(len(i["fiches"]) for i in inventaire), "fiches")
