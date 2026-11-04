# -*- coding: utf-8 -*-
"""Met en ligne le chapitre pilote (Terminale, fonctions trigonométriques).

⚠️ backend/.env pointe sur la base de PRODUCTION : une écriture est
immédiatement visible des élèves.

Depuis backend/ :
  simulation (défaut, n'écrit rien) :
    venv/Scripts/python.exe manage.py shell -c "import sys; sys.argv=['x']; exec(open(r'<chemin>/importer.py', encoding='utf-8').read())"
  mise en ligne :
    … sys.argv=['x','--appliquer'] …
  retour arrière :
    … sys.argv=['x','--restaurer', r'<chemin>/sauvegarde_….json'] …

Protections : sauvegarde JSON de tous les champs avant écriture ;
refus d'écrire si le contenu en ligne a changé depuis l'export qui a servi
à la conversion (source_en_ligne/) ; transaction unique.
Périmètre : notion 84 (Mathématiques · France · Terminale) — cours 91,
fiche 29 et ses 10 exercices. La notion 204 (« Bases & Méthodes ») n'est pas
touchée.
"""
import datetime
import json
import re
import struct
import sys
from pathlib import Path

from django.core.files import File
from django.db import transaction

from cours.models import Cours, CoursImage
from curriculum.models import Exercice, ExerciceImage
from synthesis.models import SynthesisImage, SynthesisSheet

ICI = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\pilote_trigo_terminale")
NOTION = 84
COURS_ID = 91
FICHE_ID = 29


FIGURES = ICI / "figures"

# Texte alternatif de chaque figure (accessibilité, référencement)
ALT = {
    "cours_courbes": "Courbes des fonctions sinus et cosinus sur [−2π ; 2π] : deux sinusoïdes de période 2π",
    "cours_derivees": "Courbe de sinus avec ses tangentes en 0, π/2 et π, de pentes 1, 0 et −1, et courbe de cosinus",
    "cours_etude_sin2x": "Courbe de f(x) = sin(2x) : période π, maximum 1 en π/4, minimum −1 en 3π/4",
    "etude_f": "Courbe de f(x) = sin x + cos x sur [0 ; 2π] : maximum √2 en π/4, minimum −√2 en 5π/4",
    "etude_g": "Courbe de g(x) = −cos(2x) sur [0 ; 2π] : maximums en π/2 et 3π/2, minimums en 0, π et 2π",
    "etude_h": "Courbe de h(x) = sin x / (1 + cos x) sur [0 ; 2π[ avec l'asymptote verticale x = π",
    "etude_k": "Courbe de k(x) = sin x cos x sur [0 ; 2π] : maximums 1/2 et minimums −1/2",
    "etude_m": "Courbe de m(x) = tan x − x sur [0 ; π/2[ avec l'asymptote verticale x = π/2",
    "appli_sin3x": "Courbes de sin x et sin(3x) sur [0 ; 2π] et leurs sept points d'intersection",
    "appli_f": "Courbe de f(x) = sin x / (1 + sin x) sur [0 ; 2π] avec l'asymptote verticale x = 3π/2",
    "appli_cos2x": "Courbe de cos(2x) et droite y = 1/2 : solutions de cos(2x) ≥ 1/2 sur [0 ; 2π] en vert",
    "appli_tan2x": "Courbe de tan(2x) sur [0 ; π] et droite y = √3 : solutions π/6 et 2π/3",
    "lim_sinx_x": "Courbe de sin x / x : la limite en 0 vaut 1",
    "lim_1mcos": "Courbe de (1 − cos x) / x² : la limite en 0 vaut 1/2",
    "lim_tan": "Courbe de tan x / (x − π/2) sur [0 ; π] : limite −∞ en π/2",
    "lim_prolongement": "Courbe du prolongement par continuité de sin x / x, avec f(0) = 1",
    "lim_gendarmes": "Courbe de sin x / x encadrée par −1/x et 1/x : la limite en +∞ vaut 0",
    "ineq_sin": "Courbe de sin x et droite y = √3/2 : solution [π/3 ; 2π/3] en vert",
    "ineq_cos2x": "Courbe de cos(2x) et droite y = 1/2 sur [0 ; π] : solution ]π/6 ; 5π/6[ en vert",
    "optim_max": "Courbe de sin x + cos x sur [0 ; 2π] : maximum √2 en π/4",
    "ineq_tan": "Courbe de tan x sur [0 ; 2π[ et droite y = 1 : solutions de tan x ≤ 1 en vert",
    "ineq_sinpcos": "Courbe de sin x + cos x et droite y = 1 : solution [0 ; π/2] ∪ {2π} en vert",
}


def taille_affichage(png):
    """Largeur et hauteur d'affichage : moitié des pixels (double résolution)."""
    with open(png, "rb") as fh:
        tete = fh.read(24)
    w, h = struct.unpack(">II", tete[16:24])
    return round(w / 2), round(h / 2)


def images_prevues():
    """(modèle, filtre, position, fichier) de toutes les figures à mettre en ligne."""
    corr = json.loads((FIGURES / "correspondance.json").read_text(encoding="utf-8"))
    prevues = []
    for pos, nom in corr["cours"].items():
        prevues.append((CoursImage, {"cours_id": COURS_ID}, int(pos), nom))
    for pos, nom in corr["fiche"].items():
        prevues.append((SynthesisImage, {"sheet_id": FICHE_ID}, int(pos), nom))
    ids = {e.titre: e.id for e in Exercice.objects.filter(notion_id=NOTION)}
    for titre, m in corr["exercices"].items():
        for pos, nom in m.items():
            prevues.append((ExerciceImage, {"exercice_id": ids[titre]}, int(pos), nom))
    return prevues


def norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("\r\n", "\n")).strip()


def corps(path):
    """Contenu d'un fichier cours/fiche sans ses lignes d'en-tête."""
    txt = path.read_text(encoding="utf-8")
    k = txt.find("<!--") if "<!-- optitab" in txt else txt.find("<")
    return txt[k:].strip()


def exercices(path):
    raw = path.read_text(encoding="utf-8")
    out = {}
    for b in re.split(r"^===[ \t]*$", raw, flags=re.M):
        b = b.strip()
        if not b:
            continue
        titre = b.splitlines()[0].replace("===", "", 1).strip()
        e = b.index("Énoncé:")
        t = b.index("Étapes:")
        s = b.index("Solution:")
        out[titre] = {
            "question": b[e + 7:t].strip(),
            "etapes": b[t + 7:s].strip(),
            "reponse_correcte": b[s + 9:].strip(),
        }
    return out


def etat_actuel():
    c = Cours.objects.get(id=COURS_ID)
    f = SynthesisSheet.objects.get(id=FICHE_ID)
    ex = {e.titre: {"id": e.id, "question": e.question, "etapes": e.etapes, "reponse_correcte": e.reponse_correcte}
          for e in Exercice.objects.filter(notion_id=NOTION)}
    return {"cours": {"id": c.id, "contenu": c.contenu}, "fiche": {"id": f.id, "summary": f.summary}, "exercices": ex}


def controler(actuel):
    """Le contenu en ligne doit être celui qui a été converti."""
    ecarts = []
    if norm(actuel["cours"]["contenu"]) != norm(corps(ICI / "source_en_ligne/cours.txt")):
        ecarts.append("cours 91 modifié en ligne depuis l'export")
    if norm(actuel["fiche"]["summary"]) != norm(corps(ICI / "source_en_ligne/fiche.txt")):
        ecarts.append("fiche 29 modifiée en ligne depuis l'export")
    source = exercices(ICI / "source_en_ligne/exercices.txt")
    for titre, champs in source.items():
        cur = actuel["exercices"].get(titre)
        if cur is None:
            ecarts.append(f"exercice absent en ligne : {titre}")
            continue
        for k in ("question", "etapes", "reponse_correcte"):
            if norm(cur[k]) != norm(champs[k]):
                ecarts.append(f"exercice « {titre} » ({k}) modifié en ligne depuis l'export")
    return ecarts


def appliquer():
    actuel = etat_actuel()
    ecarts = controler(actuel)
    nouveaux = exercices(ICI / "exercices.txt")
    print(f"Cours {COURS_ID}, fiche {FICHE_ID}, {len(nouveaux)} exercices (notion {NOTION})")
    if ecarts:
        print("ARRÊT : le contenu en ligne a changé, rien n'est écrit :")
        for e in ecarts:
            print("  -", e)
        print("Refaire l'export (source_en_ligne/), la conversion et les corrections.")
        return
    manquants = [t for t in nouveaux if t not in actuel["exercices"]]
    if manquants:
        print("ARRÊT : titres introuvables en ligne :", manquants)
        return
    figures = []
    for modele, filtre, pos, nom in images_prevues():
        obj = modele.objects.filter(**filtre, position=pos).first()
        png = FIGURES / "images" / nom
        if obj is None or not png.exists():
            print(f"ARRÊT : image introuvable ({modele.__name__} {filtre} position {pos} / {png.name})")
            return
        figures.append((obj, png))
    print(f"{len(figures)} figures à remplacer")
    if "--appliquer" not in sys.argv:
        print("Simulation : tout est prêt, aucune écriture. Relancer avec --appliquer.")
        return
    actuel["images"] = [
        {"modele": obj.__class__.__name__, "id": obj.id, "image": obj.image.name,
         "width": obj.width, "height": obj.height, "alt_text": obj.alt_text}
        for obj, _ in figures
    ]
    horodatage = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    sauvegarde = ICI / f"sauvegarde_avant_import_{horodatage}.json"
    sauvegarde.write_text(json.dumps(actuel, ensure_ascii=False, indent=1), encoding="utf-8")
    with transaction.atomic():
        Cours.objects.filter(id=COURS_ID).update(contenu=corps(ICI / "cours.txt"))
        SynthesisSheet.objects.filter(id=FICHE_ID).update(summary=corps(ICI / "fiche.txt"))
        for titre, champs in nouveaux.items():
            Exercice.objects.filter(id=actuel["exercices"][titre]["id"]).update(**champs)
        for obj, png in figures:
            w, h = taille_affichage(png)
            with open(png, "rb") as fh:
                obj.image.save(f"trigo_tle_{png.name}", File(fh), save=False)
            obj.width, obj.height = w, h
            obj.alt_text = ALT.get(png.stem, obj.alt_text)[:255]
            obj.save()
    print(f"Mis en ligne ({len(figures)} figures). Sauvegarde : {sauvegarde}")


def restaurer(chemin):
    data = json.loads(Path(chemin).read_text(encoding="utf-8"))
    with transaction.atomic():
        Cours.objects.filter(id=data["cours"]["id"]).update(contenu=data["cours"]["contenu"])
        SynthesisSheet.objects.filter(id=data["fiche"]["id"]).update(summary=data["fiche"]["summary"])
        for champs in data["exercices"].values():
            Exercice.objects.filter(id=champs["id"]).update(
                question=champs["question"], etapes=champs["etapes"], reponse_correcte=champs["reponse_correcte"])
        modeles = {"CoursImage": CoursImage, "SynthesisImage": SynthesisImage, "ExerciceImage": ExerciceImage}
        for im in data.get("images", []):
            # les anciens fichiers restent sur S3 : il suffit de les re-désigner
            modeles[im["modele"]].objects.filter(id=im["id"]).update(
                image=im["image"], width=im["width"], height=im["height"], alt_text=im["alt_text"])
    print("Contenu d'avant import restauré.")


if "--restaurer" in sys.argv:
    restaurer(sys.argv[sys.argv.index("--restaurer") + 1])
else:
    appliquer()
