# -*- coding: utf-8 -*-
"""Intègre un ou plusieurs chapitres de 4ème dans la base du site OptiTAB.

Usage (depuis backend/, via le shell Django) :
  manage.py shell -c "import sys; sys.argv=['x','relatifs']; exec(open(r'...integrer_4e.py', encoding='utf-8').read())"
  Argument spécial « activer » : active le niveau 4ème (filtres, chapitre démo).
Idempotent : update_or_create partout, images par position (remplacées si le fichier change).
Crée au besoin le contexte Mathématiques × 4ème et ses 5 thèmes (mêmes intitulés qu'en 3ème).
⚠️ backend/.env pointe sur la base et le stockage S3 de PRODUCTION : tout est en ligne aussitôt.
"""
import os
import re
import sys
from pathlib import Path

from django.core.files import File
from django.db import transaction

from curriculum.models import Theme, Notion, Exercice, ExerciceImage, MatiereContexte, Matiere
from cours.models import Cours, CoursImage
from synthesis.models import SynthesisSheet, SynthesisImage
from pays.models import Niveau

FRONT = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend")
DIR_C = FRONT / "cours/cours_optitab/4e"
DIR_R = FRONT / "cours/resume/4e"
DIR_E = FRONT / "exercices/4e"
NIVEAU_4E = 16       # Niveau « 4ème » (France)
MATIERE_MATHS = 1
DEMO = "relatifs"    # chapitre démo : cours, fiche et 2 premiers exercices en accès découverte

THEMES = [  # (clé, titre, ordre) — intitulés du programme, identiques à la 3ème
    ("nombres", "Nombres et calculs", 1),
    ("donnees", "Organisation et gestion de données, fonctions", 2),
    ("grandeurs", "Grandeurs et mesures", 3),
    ("geometrie", "Espace et géométrie", 4),
    ("algo", "Algorithmique et programmation", 5),
]

# slug : (numéro, titre de la notion, clé du thème, ordre dans le thème)
CHAPITRES = {
    "relatifs":         (1,  "Calculer avec les nombres relatifs",           "nombres", 1),
    "fractions":        (2,  "Fractions et nombres premiers",                "nombres", 2),
    "puissances":       (3,  "Puissances et notation scientifique",          "nombres", 3),
    "racines":          (4,  "Carrés et racines carrées",                    "nombres", 4),
    "calcul-litteral":  (5,  "Calcul littéral et distributivité",            "nombres", 5),
    "equations":        (6,  "Équations et résolution de problèmes",         "nombres", 6),
    "proportionnalite": (7,  "Proportionnalité et pourcentages",             "donnees", 1),
    "graphiques":       (9,  "Relier des grandeurs et lire des graphiques",  "donnees", 2),
    "statistiques":     (10, "Statistiques et diagrammes",                   "donnees", 3),
    "probabilites":     (11, "Probabilités",                                 "donnees", 4),
    "grandeurs":        (8,  "Grandeurs composées et unités",                "grandeurs", 1),
    "triangles":        (12, "Construire et comparer des triangles",         "geometrie", 1),
    "pythagore":        (13, "Théorème de Pythagore",                        "geometrie", 2),
    "thales":           (14, "Théorème de Thalès (triangles emboîtés)",      "geometrie", 3),
    "cosinus":          (15, "Cosinus dans le triangle rectangle",           "geometrie", 4),
    "translations":     (16, "Translations, agrandissements et réductions",  "geometrie", 5),
    "espace":           (17, "Pyramides, cônes et volumes",                  "geometrie", 6),
    "programmation":    (18, "Algorithmique et programmation",               "algo", 1),
}


def contexte_et_themes():
    niveau = Niveau.objects.get(id=NIVEAU_4E)
    assert niveau.nom.startswith("4"), niveau.nom
    ctx, _ = MatiereContexte.objects.get_or_create(
        matiere_id=MATIERE_MATHS, niveau=niveau,
        defaults=dict(titre="Mathématiques (France, 4ème)", ordre=0, couleur="#3b82f6",
                      est_actif=True))
    themes = {}
    for cle, titre, ordre in THEMES:
        t, _ = Theme.objects.update_or_create(
            contexte=ctx, titre=titre,
            defaults=dict(matiere_id=MATIERE_MATHS, ordre=ordre, description="",
                          couleur="#3b82f6", est_actif=True))
        themes[cle] = t
    return ctx, themes


def header_field(raw, name):
    m = re.search(rf"^{name}:\s*(.+)$", raw, re.M)
    return m.group(1).strip() if m else None


def auto_alt(fname, contexte):
    base = re.sub(r"\.png$", "", fname)
    base = re.sub(r"_4e", "", base).replace("_", " ").replace("-", " ")
    base = re.sub(r"\s+", " ", base).strip()
    return f"Schéma {contexte} : {base}"[:255]


def attach_image(model, fk_name, owner, pos, path, alt):
    assert path.exists(), f"Image introuvable : {path}"
    existing = model.objects.filter(**{fk_name: owner, "position": pos}).first()
    if existing:
        if os.path.basename(existing.image.name).startswith(path.stem):
            return "="
        existing.delete()
    obj = model(**{fk_name: owner}, position=pos, alt_text=alt[:255])
    with open(path, "rb") as fh:
        obj.image.save(path.name, File(fh), save=True)
    return "+"


def parse_exos(path):
    raw = path.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"^===\s*$", raw, flags=re.M) if b.strip()]
    out = []
    for b in blocks:
        titre = b.splitlines()[0].replace("===", "", 1).strip()
        diff = re.search(r"^Difficulté:\s*(\w+)", b, re.M).group(1)
        im = re.search(r"^Images?:\s*(.+)$", b, re.M)
        imgs = [s.strip() for s in im.group(1).split(",")] if im else []
        enonce = b[b.index("Énoncé:") + len("Énoncé:"): b.index("Étapes:")].strip()
        etapes = b[b.index("Étapes:") + len("Étapes:"): b.index("Solution:")].strip()
        solution = b[b.index("Solution:") + len("Solution:"):].strip()
        assert diff in ("easy", "medium", "hard") and enonce and etapes and solution, titre
        out.append(dict(titre=titre, difficulty=diff, images=imgs,
                        question=enonce, etapes=etapes, solution=solution))
    return out


def integrer_chapitre(slug, themes):
    num, notion_titre, theme_cle, ordre = CHAPITRES[slug]
    theme = themes[theme_cle]
    raw_c = (DIR_C / f"cours_{slug}_4e.txt").read_text(encoding="utf-8")
    raw_f = (DIR_R / f"resume_{slug}_4e.txt").read_text(encoding="utf-8")
    exos = parse_exos(DIR_E / f"exercice_{slug}_4e.txt")
    assert len(exos) >= 21, f"{slug} : {len(exos)} exercices (< 21)"

    demo = (slug == DEMO)
    scope_libre = "both" if demo else "paid"
    with transaction.atomic():
        notion, _ = Notion.objects.update_or_create(
            theme=theme, titre=notion_titre,
            defaults=dict(ordre=ordre, description=""))
        cours, _ = Cours.objects.update_or_create(
            notion=notion,
            defaults=dict(titre=header_field(raw_c, "Titre"),
                          contenu=raw_c[raw_c.index("<div"):].strip(),
                          difficulty="medium", ordre=num, access_scope=scope_libre))
        stats = {"+": 0, "=": 0}
        imgs_c = header_field(raw_c, "Images")
        for i, f in enumerate([s.strip() for s in imgs_c.split(",")] if imgs_c else [], 1):
            stats[attach_image(CoursImage, "cours", cours, i, DIR_C / "images" / f,
                               auto_alt(f, f"du cours {notion_titre}"))] += 1
        for idx, ex in enumerate(exos):
            scope_ex = "both" if (demo and idx < 2) else "paid"
            obj, _ = Exercice.objects.update_or_create(
                notion=notion, titre=ex["titre"],
                defaults=dict(question=ex["question"], contenu=ex["question"],
                              etapes=ex["etapes"], reponse_correcte=ex["solution"],
                              difficulty=ex["difficulty"], access_scope=scope_ex))
            for i, f in enumerate(ex["images"], 1):
                stats[attach_image(ExerciceImage, "exercice", obj, i,
                                   DIR_E / "images" / f,
                                   auto_alt(f, f"de l'exercice « {ex['titre']} »"))] += 1
        obsoletes = Exercice.objects.filter(notion=notion).exclude(
            titre__in=[e["titre"] for e in exos])
        if obsoletes.exists():
            print(f"  purge de {obsoletes.count()} exercice(s) obsolète(s) : "
                  f"{[o.titre for o in obsoletes]}")
            obsoletes.delete()
        fiche, _ = SynthesisSheet.objects.update_or_create(
            notion=notion, titre=header_field(raw_f, "Titre"), sheet_type="summary",
            defaults=dict(summary=raw_f[raw_f.index("<div"):].strip(),
                          difficulty="medium", reading_time_minutes=8,
                          access_scope=scope_libre))
        imgs_f = header_field(raw_f, "Images")
        for i, f in enumerate([s.strip() for s in imgs_f.split(",")] if imgs_f else [], 1):
            stats[attach_image(SynthesisImage, "sheet", fiche, i, DIR_C / "images" / f,
                               auto_alt(f, f"de la fiche {notion_titre}"))] += 1
    n_ex = Exercice.objects.filter(notion=notion).count()
    n_im = ExerciceImage.objects.filter(exercice__notion=notion).count()
    print(f"[{slug}] notion {notion.id} « {notion_titre} » : cours {cours.id}, "
          f"{n_ex} exercices, fiche {fiche.id}, images +{stats['+']}/={stats['=']} "
          f"(images d'exercices en base : {n_im})")
    return notion


def activer(themes):
    """Active le niveau 4ème avec les filtres d'exercices et le chapitre démo."""
    niveau = Niveau.objects.get(id=NIVEAU_4E)
    notion_demo = Notion.objects.get(theme=themes[CHAPITRES[DEMO][2]],
                                     titre=CHAPITRES[DEMO][1])
    demo_ex = list(Exercice.objects.filter(notion=notion_demo).order_by("titre")[:2])
    niveau.est_actif = True
    niveau.exercice_filter_options = ["Découverte", "Entraînement", "Problème"]
    niveau.exercice_filter_default = "Tous"
    niveau.demo_notion = notion_demo
    niveau.save()
    niveau.demo_exercices.set(demo_ex)
    print(f"[activer] niveau {niveau.id} « {niveau.nom} » actif ; démo : notion "
          f"{notion_demo.id}, exercices {[e.id for e in demo_ex]}")


if __name__ == "__main__" or True:
    cibles = [a for a in sys.argv[1:] if not a.endswith(".py") and a != "x"]
    ctx, themes = contexte_et_themes()
    print(f"contexte {ctx.id} ; thèmes {[t.id for t in themes.values()]}")
    for slug in cibles:
        if slug == "activer":
            activer(themes)
        else:
            integrer_chapitre(slug, themes)
