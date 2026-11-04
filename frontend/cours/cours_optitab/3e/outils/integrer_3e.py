# -*- coding: utf-8 -*-
"""Intègre un ou plusieurs chapitres de 3ème dans la base du site OptiTAB.

Usage (depuis backend/, via le shell Django) :
  manage.py shell -c "import sys; sys.argv=['x','fractions']; exec(open(r'...integrer_3e.py', encoding='utf-8').read())"
Idempotent : update_or_create partout, images par position (remplacées si le fichier change).
Pas de description sur les notions (demande du 2026-10-27 : titre seul sur les cartes).
"""
import os
import re
import sys
from pathlib import Path

from django.core.files import File
from django.db import transaction

from curriculum.models import Theme, Notion, Exercice, ExerciceImage
from cours.models import Cours, CoursImage
from synthesis.models import SynthesisSheet, SynthesisImage

FRONT = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend")
DIR_C = FRONT / "cours/cours_optitab/3e"
DIR_R = FRONT / "cours/resume/3e"
DIR_E = FRONT / "exercices/3e"
CTX_3E = 47          # MatiereContexte Mathématiques × 3ème (France)
THEME_BREVET_TITRE = "Préparation au brevet"

# num, slug, titre de la notion, id du thème, ordre dans le thème
CHAPITRES = {
    "fractions":        (1,  "Nombres rationnels et fractions",        85, 1),
    "puissances":       (2,  "Puissances, racines et écriture scientifique", 85, 2),
    "arithmetique":     (3,  "Arithmétique et nombres premiers",       85, 3),
    "calcul-litteral":  (4,  "Calcul littéral",                        85, 4),
    "equations":        (5,  "Équations",                              85, 5),
    "proportionnalite": (6,  "Proportionnalité et pourcentages",       86, 1),
    "grandeurs":        (7,  "Grandeurs et mesures",                   87, 1),
    "fonctions":        (8,  "Notion de fonction",                     86, 2),
    "affines":          (9,  "Fonctions linéaires et affines",         86, 3),
    "statistiques":     (10, "Statistiques",                           86, 4),
    "probabilites":     (11, "Probabilités",                           86, 5),
    "pythagore":        (12, "Théorème de Pythagore",                  88, 1),
    "thales":           (13, "Théorème de Thalès et triangles semblables", 88, 2),
    "trigonometrie":    (14, "Trigonométrie du triangle rectangle",    88, 3),
    "transformations":  (15, "Transformations du plan",                88, 4),
    "espace":           (16, "Géométrie dans l'espace",                88, 5),
    "algorithmique":    (17, "Algorithmique et programmation",         89, 1),
    "raisonner":        (18, "Raisonner et démontrer",                 89, 2),
}


def header_field(raw, name):
    m = re.search(rf"^{name}:\s*(.+)$", raw, re.M)
    return m.group(1).strip() if m else None


def auto_alt(fname, contexte):
    base = re.sub(r"\.png$", "", fname)
    base = re.sub(r"_3e", "", base).replace("_", " ").replace("-", " ")
    base = re.sub(r"\s+", " ", base).strip()
    return f"Schéma {contexte} : {base}"[:255]


def attach_image(model, fk_name, owner, pos, path, alt):
    assert path.exists(), f"Image introuvable : {path}"
    existing = model.objects.filter(**{fk_name: owner, "position": pos}).first()
    if existing:
        if os.path.basename(existing.image.name).startswith(path.stem):
            try:
                meme = existing.image.size == path.stat().st_size
            except Exception:
                meme = True
            if meme:
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


def integrer_chapitre(slug):
    num, notion_titre, theme_id, ordre = CHAPITRES[slug]
    theme = Theme.objects.get(id=theme_id, contexte_id=CTX_3E)
    raw_c = (DIR_C / f"cours_{slug}_3e.txt").read_text(encoding="utf-8")
    raw_f = (DIR_R / f"resume_{slug}_3e.txt").read_text(encoding="utf-8")
    exos = parse_exos(DIR_E / f"exercice_{slug}_3e.txt")
    assert len(exos) >= 20, f"{slug} : {len(exos)} exercices (< 20)"

    # thales = chapitre démo du niveau : cours/fiche + 2 premiers exercices en accès découverte
    demo = (slug == "thales")
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
        # purge : supprime les exercices dont le titre n'est plus dans le fichier
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
          f"(total exos : {n_im})")


def integrer_brevet():
    """Thème « Préparation au brevet » + notion « Sujets type brevet » (10 sujets)."""
    from curriculum.models import Matiere
    theme, _ = Theme.objects.update_or_create(
        contexte_id=CTX_3E, titre=THEME_BREVET_TITRE,
        defaults=dict(matiere=Matiere.objects.get(id=1), ordre=6, description=""))
    exos = parse_exos(DIR_E / "exercice_brevet_3e.txt")
    assert len(exos) >= 10, f"brevet : {len(exos)} sujets (< 10)"
    with transaction.atomic():
        notion, _ = Notion.objects.update_or_create(
            theme=theme, titre="Sujets type brevet",
            defaults=dict(ordre=1, description=""))
        for ex in exos:
            obj, _ = Exercice.objects.update_or_create(
                notion=notion, titre=ex["titre"],
                defaults=dict(question=ex["question"], contenu=ex["question"],
                              etapes=ex["etapes"], reponse_correcte=ex["solution"],
                              difficulty=ex["difficulty"], access_scope="paid"))
            for i, f in enumerate(ex["images"], 1):
                attach_image(ExerciceImage, "exercice", obj, i, DIR_E / "images" / f,
                             auto_alt(f, f"du sujet « {ex['titre']} »"))
        obsoletes = Exercice.objects.filter(notion=notion).exclude(
            titre__in=[e["titre"] for e in exos])
        if obsoletes.exists():
            print(f"  purge de {obsoletes.count()} sujet(s) obsolète(s)")
            obsoletes.delete()
        # cours de méthode et fiche d'automatismes de l'onglet brevet
        fc, ff = DIR_C / "cours_brevet_3e.txt", DIR_R / "resume_brevet_3e.txt"
        if fc.exists():
            raw_c = fc.read_text(encoding="utf-8")
            cours, _ = Cours.objects.update_or_create(
                notion=notion,
                defaults=dict(titre=header_field(raw_c, "Titre"),
                              contenu=raw_c[raw_c.index("<div"):].strip(),
                              difficulty="medium", ordre=19, access_scope="paid"))
            imgs_c = header_field(raw_c, "Images")
            for i, f in enumerate([s.strip() for s in imgs_c.split(",")] if imgs_c else [], 1):
                attach_image(CoursImage, "cours", cours, i, DIR_C / "images" / f,
                             auto_alt(f, "du cours de méthode du brevet"))
        if ff.exists():
            raw_f = ff.read_text(encoding="utf-8")
            SynthesisSheet.objects.update_or_create(
                notion=notion, titre=header_field(raw_f, "Titre"), sheet_type="summary",
                defaults=dict(summary=raw_f[raw_f.index("<div"):].strip(),
                              difficulty="medium", reading_time_minutes=10,
                              access_scope="paid"))
    print(f"[brevet] thème {theme.id}, notion {notion.id} : "
          f"{Exercice.objects.filter(notion=notion).count()} sujets, "
          f"cours {'oui' if fc.exists() else 'non'}, fiche {'oui' if ff.exists() else 'non'}")


if __name__ == "__main__" or True:
    cibles = [a for a in sys.argv[1:] if not a.endswith(".py") and a != "x"]
    for slug in cibles:
        if slug == "brevet":
            integrer_brevet()
        else:
            integrer_chapitre(slug)
