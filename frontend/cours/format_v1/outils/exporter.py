# -*- coding: utf-8 -*-
"""Export en LECTURE SEULE du contenu en ligne d'une ou plusieurs notions.

Depuis backend/ :
  venv/Scripts/python.exe manage.py shell -c "import sys; sys.argv=['x','84','204']; exec(open(r'<chemin>/exporter.py', encoding='utf-8').read())"
  sys.argv=['x','--contexte','43']   # toutes les notions d'un niveau
  sys.argv=['x','--tout']            # tout le site

Pour chaque notion : frontend/cours/format_v1/chantier/<niveau>/<id>_<slug>/source_en_ligne/
  cours_<id>.txt, fiche_<id>.txt   (« Titre: … » puis le contenu tel qu'en base)
  exercices.txt                    (format historique, avec « Id: » par exercice)
  meta.json                        (identifiants, titres, images et leurs positions)
Les images en ligne ne sont pas téléchargées ici (voir telecharger_images.py).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

from cours.models import Cours, CoursImage
from curriculum.models import Exercice, ExerciceImage, Notion
from synthesis.models import SynthesisImage, SynthesisSheet

CHANTIER = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\chantier")

NIVEAUX = {  # contexte -> dossier
    43: "6e", 49: "5e", 48: "4e", 47: "3e", 45: "2nde", 44: "1ere", 25: "terminale",
    41: "bases-terminale", 46: "bases-methodes", 42: "mpsi",
    55: "terminale-pc",  # Physique-Chimie de Terminale (créée le 2026-11-03, creer_pc_terminale.py)
}


def slug(texte):
    t = unicodedata.normalize("NFD", texte or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:50] or "notion"


def images(qs):
    out = []
    for im in qs.order_by("position", "id"):
        out.append({"id": im.id, "position": im.position, "nom": im.image.name, "url": im.image.url,
                    "width": im.width, "height": im.height, "alt": getattr(im, "alt_text", "")})
    return out


def exporter_notion(n):
    ctx = n.theme.contexte_id if n.theme else None
    niveau = CHANTIER / NIVEAUX.get(ctx, f"contexte-{ctx}")
    # une notion renommée garde son dossier existant (le slug suit l'ancien titre)
    existants = sorted(niveau.glob(f"{n.id}_*")) if niveau.exists() else []
    dossier = (existants[0] if existants else niveau / f"{n.id}_{slug(n.titre)}") / "source_en_ligne"
    dossier.mkdir(parents=True, exist_ok=True)
    meta = {"notion": n.id, "titre": n.titre, "theme": n.theme_id, "contexte": ctx,
            "cours": [], "fiches": [], "exercices": []}
    for c in Cours.objects.filter(notion=n).order_by("id"):
        (dossier / f"cours_{c.id}.txt").write_bytes(
            (f"Titre: {c.titre}\n\n" + (c.contenu or "").replace("\r\n", "\n")).encode("utf-8"))
        meta["cours"].append({"id": c.id, "titre": c.titre, "images": images(CoursImage.objects.filter(cours=c))})
    for f in SynthesisSheet.objects.filter(notion=n).order_by("id"):
        (dossier / f"fiche_{f.id}.txt").write_bytes(
            (f"Titre: {f.titre}\n\n" + (f.summary or "").replace("\r\n", "\n")).encode("utf-8"))
        meta["fiches"].append({"id": f.id, "titre": f.titre, "images": images(SynthesisImage.objects.filter(sheet=f))})
    blocs = []
    for e in Exercice.objects.filter(notion=n).order_by("titre", "id"):
        ims = images(ExerciceImage.objects.filter(exercice=e))
        noms = ",".join(Path(i["nom"]).name for i in ims)
        tete = f"=== {e.titre}\nId: {e.id}\nDifficulté: {e.difficulty}\n" + (f"Image: {noms}\n" if noms else "")
        blocs.append(tete + "\nÉnoncé: " + (e.question or "").replace("\r\n", "\n").strip()
                     + "\n\nÉtapes:\n\n" + (e.etapes or "").replace("\r\n", "\n").strip()
                     + "\n\nSolution:\n" + (e.reponse_correcte or "").replace("\r\n", "\n").strip() + "\n")
        meta["exercices"].append({"id": e.id, "titre": e.titre, "images": ims})
    (dossier / "exercices.txt").write_bytes(("\n===\n\n".join(blocs) + ("\n===\n" if blocs else "")).encode("utf-8"))
    (dossier / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return dossier.parent, len(meta["exercices"])


args = sys.argv[1:]
if "--tout" in args:
    notions = Notion.objects.select_related("theme").all()
elif "--contexte" in args:
    ctx = int(args[args.index("--contexte") + 1])
    notions = Notion.objects.select_related("theme").filter(theme__contexte_id=ctx)
else:
    notions = Notion.objects.select_related("theme").filter(id__in=[int(a) for a in args])
total = 0
for n in notions.order_by("id"):
    d, k = exporter_notion(n)
    total += k
print(f"{notions.count()} notions exportées ({total} exercices) dans {CHANTIER}")
