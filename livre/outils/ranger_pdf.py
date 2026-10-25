"""Range tous les PDF livrés dans livre/output, directement dans le dossier de leur matière.

  python -X utf8 outils/ranger_pdf.py          (depuis le dossier livre/)

  output/Mathématiques/05 - CE1.pdf                     numéroté dans l'ordre des classes
  output/Physique-chimie/16 - MPSI - Chapitre 01 - ….pdf
  output/Anglais/Tome 1 - Premiers pas (A1)/Tome 1 - Premiers pas (A1).pdf  (+ dossier Audios)
  output/Python/Volume 1 - First Steps/Volume 1 - First Steps (….pdf
  (collections en plusieurs tomes : un dossier par tome)
  output/README.md                                      catalogue (liens, nombre de pages)

À lancer après chaque livraison : les scripts « livrer.py » déposent leurs PDF sous leur nom
complet « OptiTAB - Matière - Niveau - Type.pdf », souvent selon l'ancien rangement
(…/output/pdf/France/…, livre-maths/output, livre-physique/output) et leurs rapports dans
output/verification|sources|archives. Ce script les renomme et les range, déplace les rapports
dans archives/verification, efface les sauvegardes zippées et les anciennes versions, et ne
modifie jamais le contenu d'un PDF.
"""
import hashlib
import json
import re
import shutil
from pathlib import Path

import fitz

LIVRES = Path(__file__).resolve().parents[1]
OUTPUT = LIVRES / "output"
ARCHIVES = LIVRES / "archives"

MATIERES = ["Mathématiques", "Physique-chimie", "Anglais", "Python"]
COLLECTIONS = ("Anglais", "Python")  # plusieurs tomes : un dossier par tome
NIVEAUX = [("Petite section", 1), ("Moyenne section", 2), ("Grande section", 3), ("CP", 4), ("CE1", 5),
           ("CE2", 6), ("CM1", 7), ("CM2", 8), ("Sixième", 9), ("Cinquième", 10), ("Quatrième", 11),
           ("Troisième", 12), ("Seconde", 13), ("Première", 14), ("Terminale", 15), ("MPSI", 16)]
LIVRE_PRINCIPAL = ("Manuel complet", "Cahier d’activités", "Cahier d'activités")
VOLUMES_PYTHON = {"Volume 1": "Volume 1 - First Steps"}
# Certains noms de livraison ont perdu leurs accents
ACCENTS = {"Signaux electriques dans l ARQS": "Signaux électriques dans l'ARQS",
           "Circuits lineaires": "Circuits linéaires"}
# Dossiers de travail que les anciens scripts créent dans output/ : on les range dans archives/
# (None : sauvegardes zippées et anciennes versions, inutiles depuis que tout est sur GitHub → effacées)
BALAYAGE = {"verification": "verification", "sources": None, "archives": None}


def classer(nom):
    """(matière, nom dans la bibliothèque) d'après le nom de livraison « OptiTAB - … » ; None sinon."""
    m = re.match(r"OptiTAB - Physique - MPSI - (.+)\.pdf$", nom)
    if m:
        reste = m.group(1).replace(" - Sommaire revise", " (sommaire révisé)")
        for sans, avec in ACCENTS.items():
            reste = reste.replace(sans, avec)
        return "Physique-chimie", f"16 - MPSI - {reste}.pdf"
    m = re.match(r"OptiTAB - Physique MPSI - Chapitres (\d+) a (\d+)\.zip$", nom)
    if m:
        return "Physique-chimie", f"16 - MPSI - Chapitres {m.group(1)} à {m.group(2)}.zip"
    m = re.match(r"OptiTAB - L'essentiel - Mathématiques Terminale(.*)\.pdf$", nom)
    if m:
        return "Mathématiques", f"15 - Terminale spécialité - Fiches L'essentiel{m.group(1)}.pdf"
    # Collections en plusieurs tomes : un dossier par tome (le PDF, et les audios pour l'anglais)
    m = re.match(r"OptiTAB - Anglais - (Tome \d+ - .+)\.pdf$", nom)
    if m:
        return "Anglais", f"{m.group(1)}/{m.group(1)}.pdf"
    m = re.match(r"OptiTAB - Python - (Volume \d+)(.*)\.pdf$", nom)
    if m:
        volume = VOLUMES_PYTHON.get(m.group(1), m.group(1))
        return "Python", f"{volume}/{volume}{m.group(2)}.pdf"
    m = re.match(r"OptiTAB - (Mathématiques|Physique-chimie) - (.+) - ([^-]+)\.pdf$", nom)
    if m:
        niveau, type_ = m.group(2), m.group(3).strip()
        for cle, num in NIVEAUX:
            if niveau.startswith(cle):
                suffixe = "" if type_ in LIVRE_PRINCIPAL else f" - {type_}"
                return m.group(1), f"{num:02d} - {niveau}{suffixe}.pdf"
    return None


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def deplacer(src, dst):
    """Déplace src vers dst ; si dst existe déjà, garde le plus récent et efface l'autre
    (le propriétaire ne garde pas les anciennes versions : l'historique Git suffit)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.move(str(src), str(dst))
        return
    if src.stat().st_mtime >= dst.stat().st_mtime:
        dst.unlink()
        shutil.move(str(src), str(dst))
    else:
        src.unlink()


def deja_range(f):
    if classer(f.name) is not None:
        return False
    if f.parent.parent == OUTPUT and f.parent.name in MATIERES:
        return True  # maths, physique : directement dans le dossier de la matière
    return f.parent.parent.parent == OUTPUT and f.parent.parent.name in COLLECTIONS  # un dossier par tome


def ranger():
    deplaces, inconnus = [], []
    # 0. les anciens scripts écrivent dans « ../output » : livre-maths/output, livre-physique/output…
    for perdu in sorted(LIVRES.glob("livre-*/output")):
        for f in sorted(p for p in perdu.rglob("*") if p.is_file()):
            deplacer(f, OUTPUT / f.relative_to(perdu))
        shutil.rmtree(perdu, ignore_errors=True)
    # 1. dossiers de travail : les rapports vont dans archives/, le reste est effacé
    for nom, cible in BALAYAGE.items():
        d = OUTPUT / nom
        if d.is_dir():
            if cible is None:
                shutil.rmtree(d, ignore_errors=True)
                continue
            for f in sorted(p for p in d.rglob("*") if p.is_file()):
                deplacer(f, ARCHIVES / cible / f.relative_to(d))
    # 2. PDF et zip livrés : renommés et posés directement dans le dossier de leur matière
    for f in sorted(p for p in OUTPUT.rglob("*") if p.is_file() and p.suffix in (".pdf", ".zip")):
        if deja_range(f):
            continue
        c = classer(f.name)
        if c is None:
            inconnus.append(f)
            continue
        cible = OUTPUT / c[0] / c[1]
        if f != cible:
            deplacer(f, cible)
            deplaces.append(cible)
    # 3. ancien index et dossiers vides
    ancien_index = OUTPUT / "pdf" / "README.md"
    if ancien_index.exists():
        ancien_index.unlink()
    for d in sorted((p for p in OUTPUT.rglob("*") if p.is_dir()), key=lambda p: -len(p.parts)):
        if not any(d.iterdir()):
            d.rmdir()
    return deplaces, inconnus


def catalogue():
    lignes = ["# Bibliothèque OptiTAB — tous les PDF", "",
              "Un dossier par matière ; les livres y sont rangés dans l'ordre des classes. "
              "Ce fichier est refait par `outils/ranger_pdf.py` ; ne pas le modifier à la main.", ""]
    rapport = []
    total_pdf = total_pages = 0
    for matiere in MATIERES:
        dm = OUTPUT / matiere
        if not dm.is_dir():
            continue
        lignes += [f"## {matiere}", "", "| Livre | Pages |", "| --- | ---: |"]
        elements = sorted(dm.iterdir(), key=lambda p: (p.is_dir(), p.name))
        if matiere in COLLECTIONS:  # un dossier par tome
            elements = [f for tome in sorted(p for p in dm.iterdir() if p.is_dir())
                        for f in sorted(tome.iterdir(), key=lambda p: (p.is_dir(), p.name))]
        for f in elements:
            chemin = f.relative_to(dm).as_posix()
            titre = re.sub(r"^\d+ - ", "", f.stem if f.is_file() else f"{f.parent.name} — {f.name}")
            if f.suffix == ".pdf":
                with fitz.open(f) as doc:
                    pages = len(doc)
                total_pdf += 1
                total_pages += pages
                lignes.append(f"| [{titre}](<{matiere}/{chemin}>) | {pages} |")
                rapport.append(dict(matiere=matiere, fichier=chemin, pages=pages, sha256=sha(f)))
            elif f.suffix == ".zip":
                lignes.append(f"| [{titre} (archive zip)](<{matiere}/{chemin}>) | — |")
            elif f.is_dir():
                n = sum(1 for _ in f.rglob("*.mp3"))
                lignes.append(f"| [{titre}](<{matiere}/{chemin}/index.html>) — {n} pistes audio | — |")
        lignes.append("")
    lignes.append(f"**{total_pdf} PDF · {total_pages} pages.**")
    (OUTPUT / "README.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    r = ARCHIVES / "verification" / "classement-pdf.json"
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text(json.dumps(dict(pdf=total_pdf, pages=total_pages, livres=rapport), ensure_ascii=False,
                            indent=1), encoding="utf-8")
    return total_pdf, total_pages


if __name__ == "__main__":
    deplaces, inconnus = ranger()
    n, pages = catalogue()
    print(f"{len(deplaces)} fichier(s) rangé(s) · catalogue : {n} PDF, {pages} pages")
    for f in inconnus:
        print("  À RANGER À LA MAIN (nom non standard) :", f.relative_to(LIVRES))
