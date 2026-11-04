# -*- coding: utf-8 -*-
"""Mise en ligne de notions du chantier au format OptiTAB v1.

⚠️ backend/.env pointe sur la base de PRODUCTION et le S3 de production :
une écriture est immédiatement visible des élèves. Le moteur v1 doit être
déployé sur le site AVANT toute mise en ligne de contenu v1.

Depuis backend/ :
  simulation (défaut, n'écrit rien) :
    venv/Scripts/python.exe manage.py shell -c "import sys; sys.argv=['x', r'<dossier_notion>']; exec(open(r'<chemin>/importer_v1.py', encoding='utf-8').read())"
  plusieurs notions / un niveau entier (notions au statut « pret ») :
    sys.argv=['x', r'<dossier1>', r'<dossier2>']    sys.argv=['x', '--niveau', 'terminale']
  mise en ligne : ajouter '--appliquer'
  retour arrière : sys.argv=['x', '--restaurer', r'<dossier>/sauvegardes/avant_import_….json']

Pour chaque notion, dans une transaction :
  - contrôle complet (verifier_notion, sans navigateur) : refus au moindre problème ;
  - contrôle de concurrence : le contenu en ligne (textes ET images) doit être
    exactement celui de l'export source_en_ligne/ ; sinon refus ;
  - sauvegarde JSON de tout ce qui sera modifié (textes, lignes d'images) ;
  - textes : cours, fiche, énoncé / étapes / solution de chaque exercice ;
  - images : figures de correspondance.json (remplacement à la même position
    ou création), largeur/hauteur = moitié des pixels, texte alternatif ;
    lignes d'images en ligne qui ne sont plus appelées par [IMAGE_N] : supprimées
    (le fichier S3 reste : la restauration les recrée) ;
  - relecture de la base après écriture ; etat.json → « importe ».
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

OUTILS = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\outils")
CHANTIER = OUTILS.parent / "chantier"
sys.path.insert(0, str(OUTILS))
import verifier_notion  # noqa: E402

IMG_RE = re.compile(r"\[\s*IMAGE\s*_?\s*(\d+)\s*\]", re.I)
MODELES = {
    "cours": (CoursImage, "cours_id", "legende"),
    "fiches": (SynthesisImage, "sheet_id", "caption"),
    "exercices": (ExerciceImage, "exercice_id", "legende"),
}
MODELE_PAR_NOM = {"CoursImage": "cours", "SynthesisImage": "fiches", "ExerciceImage": "exercices"}


# --------------------------------------------------------------------- lecture
def taille_affichage(png):
    with open(png, "rb") as fh:
        w, h = struct.unpack(">II", fh.read(24)[16:24])
    return round(w / 2), round(h / 2)


def corps_doc(path):
    t = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    k = t.find("<!-- optitab:1 -->")
    if k < 0:
        raise ValueError(f"{path.name} : marqueur v1 absent")
    return t[k:].strip()


def exercices_finaux(path):
    out = {}
    for b in re.split(r"^===[ \t]*$", path.read_text(encoding="utf-8").replace("\r\n", "\n"), flags=re.M):
        b = b.strip()
        if not b:
            continue
        brut = re.search(r"^Id:\s*(\S+)", b, re.M).group(1)
        eid = int(brut) if brut.isdigit() else brut  # « nouveau-N » : exercice à créer
        pos = {m.group(1): (m.start(), m.end()) for m in re.finditer(r"^(Énoncé|Étapes|Solution):[ \t]*$", b, re.M)}
        if set(pos) != {"Énoncé", "Étapes", "Solution"}:
            raise ValueError(f"exercice {eid} : rubriques incomplètes")
        diff = re.search(r"^Difficulté:\s*(\w+)", b, re.M)
        out[eid] = {
            "titre": b.splitlines()[0].replace("===", "", 1).strip(),
            "difficulty": diff.group(1) if diff else "medium",
            "champs": {
                "question": b[pos["Énoncé"][1]:pos["Étapes"][0]].strip(),
                "etapes": b[pos["Étapes"][1]:pos["Solution"][0]].strip(),
                "reponse_correcte": b[pos["Solution"][1]:].strip(),
            },
        }
    return out


def blocs_source(path):
    """Blocs de l'export par Id, tels qu'écrits par exporter.py."""
    out = {}
    if not path.exists():
        return out
    for b in path.read_bytes().decode("utf-8").split("\n===\n\n"):
        m = re.search(r"^Id: (\d+)$", b, re.M)
        if m:
            out[int(m.group(1))] = b.rstrip("\n").removesuffix("\n===").rstrip("\n")
    return out


def bloc_export(e, noms_images):
    """Même mise en forme que exporter.py (contrôle de concurrence exact)."""
    noms = ",".join(noms_images)
    tete = f"=== {e.titre}\nId: {e.id}\nDifficulté: {e.difficulty}\n" + (f"Image: {noms}\n" if noms else "")
    return (tete + "\nÉnoncé: " + (e.question or "").replace("\r\n", "\n").strip()
            + "\n\nÉtapes:\n\n" + (e.etapes or "").replace("\r\n", "\n").strip()
            + "\n\nSolution:\n" + (e.reponse_correcte or "").replace("\r\n", "\n").strip()).rstrip("\n")


def images_en_base(genre, oid):
    modele, champ, _ = MODELES[genre]
    return list(modele.objects.filter(**{champ: oid}).order_by("position", "id"))


def ligne_image(genre, im):
    _, champ, leg = MODELES[genre]
    return {"modele": type(im).__name__, "id": im.id, "proprietaire": getattr(im, champ), "position": im.position,
            "image": im.image.name, "legende": getattr(im, leg), "alt_text": im.alt_text,
            "title_text": im.title_text, "width": im.width, "height": im.height}


# ------------------------------------------------------------------- un import
def preparer(dossier):
    """Contrôles et plan d'écriture d'une notion (aucune écriture)."""
    dossier = Path(dossier)
    meta = json.loads((dossier / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
    # Exercices retirés volontairement (exercices_retires.txt) : ignorés ici, supprimés
    # ensuite en base par retirer_exercices.py (avec sauvegarde).
    retires_txt = dossier / "exercices_retires.txt"
    if retires_txt.exists():
        retires = {int(m.group(1)) for m in re.finditer(r"^\s*(\d+)", retires_txt.read_text(encoding="utf-8"), re.M)}
        meta["exercices"] = [e for e in meta["exercices"] if e["id"] not in retires]
    problemes = verifier_notion.verifier(dossier, navigateur=False)
    if problemes:
        return None, [f"verifier_notion : {len(problemes)} problème(s)"]
    ecarts = []

    # concurrence : textes
    src = dossier / "source_en_ligne"
    textes = {"cours": {}, "fiches": {}, "exercices": {}}
    for c in meta["cours"]:
        obj = Cours.objects.get(id=c["id"])
        attendu = (src / f"cours_{c['id']}.txt").read_bytes().decode("utf-8")
        if f"Titre: {obj.titre}\n\n" + (obj.contenu or "").replace("\r\n", "\n") != attendu:
            ecarts.append(f"cours {c['id']} modifié en ligne depuis l'export")
        textes["cours"][c["id"]] = corps_doc(dossier / f"cours_{c['id']}.txt")
    for f in meta["fiches"]:
        obj = SynthesisSheet.objects.get(id=f["id"])
        attendu = (src / f"fiche_{f['id']}.txt").read_bytes().decode("utf-8")
        if f"Titre: {obj.titre}\n\n" + (obj.summary or "").replace("\r\n", "\n") != attendu:
            ecarts.append(f"fiche {f['id']} modifiée en ligne depuis l'export")
        textes["fiches"][f["id"]] = corps_doc(dossier / f"fiche_{f['id']}.txt")
    renommer, nouveaux = {}, {}
    finaux = exercices_finaux(dossier / "exercices.txt") if (dossier / "exercices.txt").exists() else {}
    if meta["exercices"]:
        source = blocs_source(src / "exercices.txt")
        for e in meta["exercices"]:
            obj = Exercice.objects.get(id=e["id"])
            noms = [Path(im.image.name).name for im in images_en_base("exercices", e["id"])]
            if bloc_export(obj, noms) != source.get(e["id"]):
                ecarts.append(f"exercice {e['id']} modifié en ligne depuis l'export")
            f = finaux[e["id"]]
            textes["exercices"][e["id"]] = f["champs"]
            if (f["titre"], f["difficulty"]) != (obj.titre, obj.difficulty):
                renommer[e["id"]] = {"titre": f["titre"], "difficulty": f["difficulty"]}
    nouveaux = {k: v for k, v in finaux.items() if isinstance(k, str)}
    titres = [v["titre"] for v in finaux.values()]
    if len(set(titres)) != len(titres):
        ecarts.append("deux exercices portent le même titre")
    autres = set(Exercice.objects.filter(notion_id=meta["notion"]).exclude(
        id__in=[e["id"] for e in meta["exercices"]]).values_list("titre", flat=True))
    if autres & set(titres):
        ecarts.append(f"titre déjà utilisé dans la notion : {sorted(autres & set(titres))}")

    # concurrence : images
    for genre, cle in (("cours", "cours"), ("fiches", "fiches"), ("exercices", "exercices")):
        for it in meta[cle]:
            en_base = {(im.position, im.image.name) for im in images_en_base(genre, it["id"])}
            exportees = {(im["position"], im["nom"]) for im in it["images"]}
            if en_base != exportees:
                ecarts.append(f"images de {genre} {it['id']} modifiées en ligne depuis l'export")
    if ecarts:
        return None, ecarts

    # plan des images
    corr_path = dossier / "figures" / "correspondance.json"
    corr = json.loads(corr_path.read_text(encoding="utf-8")) if corr_path.exists() else {}
    plan = {"remplacer": [], "creer": [], "supprimer": []}
    for genre in ("cours", "fiches", "exercices"):
        for oid, txt in textes[genre].items():
            appels = {int(n) for n in IMG_RE.findall(txt if isinstance(txt, str) else " ".join(txt.values()))}
            nouvelles = {int(p): v for p, v in (corr.get(genre) or {}).get(str(oid), {}).items()}
            existantes = {im.position: im for im in images_en_base(genre, oid)}
            for pos, v in sorted(nouvelles.items()):
                png = dossier / "figures" / "images" / v["fichier"]
                action = "remplacer" if pos in existantes else "creer"
                plan[action].append((genre, oid, pos, png, v["alt"], existantes.get(pos)))
            for pos, im in sorted(existantes.items()):
                if pos not in appels and pos not in nouvelles:
                    plan["supprimer"].append((genre, oid, pos, im))
    # figures des exercices à créer (clé « nouveau-N » dans correspondance.json)
    figures_nouveaux = {}
    for cle in nouveaux:
        m = (corr.get("exercices") or {}).get(cle, {})
        figures_nouveaux[cle] = [(int(p), dossier / "figures" / "images" / v["fichier"], v["alt"]) for p, v in m.items()]
    return {"dossier": dossier, "meta": meta, "textes": textes, "plan": plan, "renommer": renommer,
            "nouveaux": nouveaux, "figures_nouveaux": figures_nouveaux}, []


def sauvegarder(prep):
    meta, dossier = prep["meta"], prep["dossier"]
    sauve = {"notion": meta["notion"], "dossier": str(dossier), "date": datetime.datetime.now().isoformat(timespec="seconds"),
             "cours": [], "fiches": [], "exercices": [], "images": [], "images_creees": [], "exercices_crees": []}
    for c in meta["cours"]:
        o = Cours.objects.get(id=c["id"])
        sauve["cours"].append({"id": o.id, "contenu": o.contenu})
    for f in meta["fiches"]:
        o = SynthesisSheet.objects.get(id=f["id"])
        sauve["fiches"].append({"id": o.id, "summary": o.summary})
    for e in meta["exercices"]:
        o = Exercice.objects.get(id=e["id"])
        sauve["exercices"].append({"id": o.id, "question": o.question, "etapes": o.etapes, "reponse_correcte": o.reponse_correcte,
                                   "titre": o.titre, "difficulty": o.difficulty, "contenu": o.contenu})
    for genre, cle in (("cours", "cours"), ("fiches", "fiches"), ("exercices", "exercices")):
        for it in meta[cle]:
            sauve["images"] += [ligne_image(genre, im) for im in images_en_base(genre, it["id"])]
    (dossier / "sauvegardes").mkdir(exist_ok=True)
    chemin = dossier / "sauvegardes" / f"avant_import_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
    chemin.write_text(json.dumps(sauve, ensure_ascii=False, indent=1), encoding="utf-8")
    return chemin, sauve


def appliquer(prep):
    meta, dossier, textes, plan = prep["meta"], prep["dossier"], prep["textes"], prep["plan"]
    chemin, sauve = sauvegarder(prep)
    with transaction.atomic():
        for cid, txt in textes["cours"].items():
            Cours.objects.filter(id=cid).update(contenu=txt)
        for fid, txt in textes["fiches"].items():
            SynthesisSheet.objects.filter(id=fid).update(summary=txt)
        for eid, champs in textes["exercices"].items():
            Exercice.objects.filter(id=eid).update(**champs, contenu=champs["question"], **prep["renommer"].get(eid, {}))
        for cle, v in prep["nouveaux"].items():
            ex = Exercice.objects.create(notion_id=meta["notion"], titre=v["titre"], difficulty=v["difficulty"],
                                         contenu=v["champs"]["question"], access_scope=Exercice.ACCESS_SCOPE_PAID,
                                         **v["champs"])
            sauve["exercices_crees"].append({"cle": cle, "id": ex.id, "titre": ex.titre})
            for pos, png, alt in prep["figures_nouveaux"].get(cle, []):
                im = ExerciceImage(exercice=ex, position=pos)
                w, h = taille_affichage(png)
                with open(png, "rb") as fh:
                    im.image.save(f"v1_n{meta['notion']}_ex{ex.id}_{pos}_{png.name}", File(fh), save=False)
                im.width, im.height, im.alt_text = w, h, alt[:255]
                im.save()
        for genre, oid, pos, im in plan["supprimer"]:
            im.delete()  # le fichier S3 n'est pas supprimé (FileField) : restauration possible
        for action in ("remplacer", "creer"):
            for genre, oid, pos, png, alt, im in plan[action]:
                modele, champ, leg = MODELES[genre]
                if im is None:
                    im = modele(**{champ: oid, "position": pos})
                w, h = taille_affichage(png)
                with open(png, "rb") as fh:
                    im.image.save(f"v1_n{meta['notion']}_{genre[:2]}{oid}_{pos}_{png.name}", File(fh), save=False)
                im.width, im.height = w, h
                im.alt_text = alt[:255]
                im.title_text = ""
                setattr(im, leg, None)
                im.save()
                if action == "creer":
                    sauve["images_creees"].append({"modele": modele.__name__, "id": im.id})
    chemin.write_text(json.dumps(sauve, ensure_ascii=False, indent=1), encoding="utf-8")
    # relecture
    erreurs = []
    for cid, txt in textes["cours"].items():
        if Cours.objects.get(id=cid).contenu != txt:
            erreurs.append(f"cours {cid} relu différent")
    for fid, txt in textes["fiches"].items():
        if SynthesisSheet.objects.get(id=fid).summary != txt:
            erreurs.append(f"fiche {fid} relue différente")
    for eid, champs in textes["exercices"].items():
        o = Exercice.objects.get(id=eid)
        if any(getattr(o, k) != v for k, v in champs.items()):
            erreurs.append(f"exercice {eid} relu différent")
    etat = dossier / "etat.json"
    e = json.loads(etat.read_text(encoding="utf-8")) if etat.exists() else {}
    e.update({"statut": "importe", "import": datetime.datetime.now().isoformat(timespec="seconds"), "sauvegarde": str(chemin)})
    etat.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    # les « nouveau-N » créés prennent leur vrai Id dans les fichiers (pas de doublon au réimport)
    import relier_nouveaux
    relier_nouveaux.relier(dossier)
    return chemin, erreurs


def restaurer(chemin):
    data = json.loads(Path(chemin).read_text(encoding="utf-8"))
    modeles = {"CoursImage": CoursImage, "SynthesisImage": SynthesisImage, "ExerciceImage": ExerciceImage}
    with transaction.atomic():
        for c in data["cours"]:
            Cours.objects.filter(id=c["id"]).update(contenu=c["contenu"])
        for f in data["fiches"]:
            SynthesisSheet.objects.filter(id=f["id"]).update(summary=f["summary"])
        for e in data["exercices"]:
            extra = {k: e[k] for k in ("titre", "difficulty", "contenu") if k in e}
            Exercice.objects.filter(id=e["id"]).update(question=e["question"], etapes=e["etapes"],
                                                        reponse_correcte=e["reponse_correcte"], **extra)
        for e in data.get("exercices_crees", []):
            Exercice.objects.filter(id=e["id"]).delete()
        for im in data.get("images_creees", []):
            modeles[im["modele"]].objects.filter(id=im["id"]).delete()
        for im in data["images"]:
            genre = MODELE_PAR_NOM[im["modele"]]
            modele, champ, leg = MODELES[genre]
            champs = {"image": im["image"], "position": im["position"], leg: im["legende"], "alt_text": im["alt_text"],
                      "title_text": im["title_text"], "width": im["width"], "height": im["height"]}
            if modele.objects.filter(id=im["id"]).exists():
                modele.objects.filter(id=im["id"]).update(**champs)
            else:
                modele.objects.filter(**{champ: im["proprietaire"], "position": im["position"]}).delete()
                modele.objects.create(id=im["id"], **{champ: im["proprietaire"]}, **champs)
    dossier = Path(data["dossier"])
    etat = dossier / "etat.json"
    if etat.exists():
        e = json.loads(etat.read_text(encoding="utf-8"))
        e.update({"statut": "pret", "restaure": datetime.datetime.now().isoformat(timespec="seconds")})
        etat.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Notion {data['notion']} restaurée telle qu'avant l'import du {data['date']}.")


# ---------------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    if "--restaurer" in args:
        restaurer(args[args.index("--restaurer") + 1])
        return
    ecrire = "--appliquer" in args
    if "--niveau" in args:
        niveau = args[args.index("--niveau") + 1]
        dossiers = []
        for d in sorted(p.parent for p in (CHANTIER / niveau).glob("*/source_en_ligne")):
            etat = d / "etat.json"
            statut = json.loads(etat.read_text(encoding="utf-8")).get("statut") if etat.exists() else "a_faire"
            if statut == "pret":
                dossiers.append(d)
            else:
                print(f"   (ignorée, statut {statut}) {d.name}")
    else:
        dossiers = [Path(a) for a in args if not a.startswith("--")]
    bilan = []
    for d in dossiers:
        prep, refus = preparer(d)
        if refus:
            print(f"✗ {d.name} : REFUSÉE")
            for r in refus:
                print("    -", r)
            bilan.append((d.name, "refusée"))
            continue
        p = prep["plan"]
        n_ex = len(prep["textes"]["exercices"])
        resume = (f"{len(prep['textes']['cours'])} cours, {len(prep['textes']['fiches'])} fiche(s), {n_ex} exercice(s) ; "
                  f"images : {len(p['remplacer'])} remplacée(s), {len(p['creer'])} créée(s), {len(p['supprimer'])} supprimée(s)")
        if not ecrire:
            print(f"✓ {d.name} : prête — {resume}")
            bilan.append((d.name, "prête"))
            continue
        chemin, erreurs = appliquer(prep)
        print(f"{'✓' if not erreurs else '✗'} {d.name} : MISE EN LIGNE — {resume} ; sauvegarde {chemin.name}")
        for e in erreurs:
            print("    -", e)
        bilan.append((d.name, "en ligne" if not erreurs else "à vérifier"))
    print(f"\n{len(bilan)} notion(s) : " + ", ".join(f"{n} {s}" for n, s in bilan))
    if not ecrire:
        print("Simulation : rien n'a été écrit. Ajouter '--appliquer' pour mettre en ligne.")


main()
