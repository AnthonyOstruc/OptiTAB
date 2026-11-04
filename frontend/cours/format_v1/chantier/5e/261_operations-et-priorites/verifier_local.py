# -*- coding: utf-8 -*-
"""Vérification complète d'une notion du chantier avant import.

    python verifier_notion.py <dossier_notion> [--navigateur]

1. Syntaxe v1 (valider_v1) des fichiers finaux cours_<id>.txt, fiche_<id>.txt, exercices.txt.
2. Complétude : chaque cours, fiche et exercice de meta.json est présent une fois,
   avec le même Id et le même titre ; aucun Id inconnu.
3. Images : chaque [IMAGE_N] renvoie à une nouvelle figure (figures/correspondance.json,
   fichier présent, texte alternatif) ou à une image en ligne existante (meta.json) ;
   aucune nouvelle figure inutilisée ; largeur ≤ 1100 px.
   Les images en ligne CONSERVÉES sont listées : chacune doit avoir été jugée
   impeccable (sinon la refaire). Les images en ligne non appelées seront
   supprimées à l'import.
4. Aperçu <dossier>/apercu.html ; avec --navigateur, contrôle Chrome (téléphone
   390 px + ordinateur 1280 px) : débordements, formules en erreur, $ bruts.
Code de sortie 0 seulement si tout est bon.
"""
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parents[3] / 'outils'
sys.path.insert(0, str(ICI))
import valider_v1  # noqa: E402

IMG_RE = re.compile(r"\[\s*IMAGE\s*_?\s*(\d+)\s*\]", re.I)


def blocs_exercices(texte):
    out = []
    for b in re.split(r"^===[ \t]*$", texte, flags=re.M):
        b = b.strip()
        if not b:
            continue
        titre = b.splitlines()[0].replace("===", "", 1).strip()
        m = re.search(r"^Id:\s*(\S+)", b, re.M)
        eid = None if not m else (int(m.group(1)) if m.group(1).isdigit() else m.group(1))
        out.append((eid, titre, b))
    return out


def corps_doc(path):
    t = path.read_text(encoding="utf-8")
    k = t.find("<!-- optitab:1 -->")
    return t[k:] if k >= 0 else t


def largeur_png(p):
    with open(p, "rb") as fh:
        return struct.unpack(">II", fh.read(24)[16:24])[0]


def verifier(dossier, navigateur=False):
    dossier = Path(dossier)
    meta = json.loads((dossier / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
    corr_path = dossier / "figures" / "correspondance.json"
    corr = json.loads(corr_path.read_text(encoding="utf-8")) if corr_path.exists() else {}
    problemes, notes = [], []

    # 1. syntaxe
    fichiers = [dossier / f"cours_{c['id']}.txt" for c in meta["cours"]] + \
               [dossier / f"fiche_{f['id']}.txt" for f in meta["fiches"]]
    if meta["exercices"]:
        fichiers.append(dossier / "exercices.txt")
    for f in fichiers:
        if not f.exists():
            problemes.append(f"fichier manquant : {f.name}")
            continue
        p = []
        valider_v1.check_file(f, p)
        problemes += [x for x in p if "utilisée mais" not in x]

    # 2. complétude + collecte des appels d'images
    appels = {}  # (genre, id) -> {positions}
    for c in meta["cours"]:
        f = dossier / f"cours_{c['id']}.txt"
        if f.exists():
            appels[("cours", c["id"])] = {int(n) for n in IMG_RE.findall(corps_doc(f))}
    for s in meta["fiches"]:
        f = dossier / f"fiche_{s['id']}.txt"
        if f.exists():
            appels[("fiches", s["id"])] = {int(n) for n in IMG_RE.findall(corps_doc(f))}
    if meta["exercices"] and (dossier / "exercices.txt").exists():
        blocs = blocs_exercices((dossier / "exercices.txt").read_text(encoding="utf-8"))
        attendus = {e["id"]: e["titre"] for e in meta["exercices"]}
        vus = {}
        for eid, titre, b in blocs:
            if eid is None:
                problemes.append(f"exercice sans ligne « Id: » : {titre[:60]}")
                continue
            if eid in vus:
                problemes.append(f"exercice Id {eid} présent deux fois")
            vus[eid] = titre
            if isinstance(eid, str):
                if not re.fullmatch(r"nouveau-\d+", eid):
                    problemes.append(f"Id invalide « {eid} » (nombre en ligne ou nouveau-N)")
                else:
                    notes.append(f"exercice à créer : {eid} « {titre} »")
            elif eid not in attendus:
                problemes.append(f"Id d'exercice inconnu en ligne : {eid}")
            elif titre != attendus[eid]:
                notes.append(f"titre changé pour l'Id {eid} : « {titre} »")
            for champ in ("Énoncé:", "Étapes:", "Solution:"):
                if champ not in b:
                    problemes.append(f"Id {eid} : rubrique {champ} absente")
            s = b.find("Énoncé:")
            appels[("exercices", eid)] = {int(n) for n in IMG_RE.findall(b[s:])} if s >= 0 else set()
        for eid in attendus:
            if eid not in vus:
                problemes.append(f"exercice Id {eid} absent du fichier final")

    # 3. images
    en_ligne = {}
    for genre, cle in (("cours", "cours"), ("fiches", "fiches"), ("exercices", "exercices")):
        for it in meta[cle]:
            en_ligne[(genre, it["id"])] = {im["position"]: im for im in it["images"]}
    nouvelles = {}
    for genre in ("cours", "fiches", "exercices"):
        for oid, m in (corr.get(genre) or {}).items():
            for pos, v in m.items():
                nouvelles[(genre, int(oid) if oid.isdigit() else oid, int(pos))] = v
    conservees = []
    for (genre, oid), positions in sorted(appels.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        for pos in sorted(positions):
            v = nouvelles.get((genre, oid, pos))
            if v is not None:
                fichier = v if isinstance(v, str) else v.get("fichier")
                alt = "" if isinstance(v, str) else (v.get("alt") or "")
                png = dossier / "figures" / "images" / (fichier or "")
                if not fichier or not png.exists():
                    problemes.append(f"{genre} {oid} [IMAGE_{pos}] : figure introuvable ({fichier})")
                    continue
                if len(alt.strip()) < 15:
                    problemes.append(f"{genre} {oid} [IMAGE_{pos}] : texte alternatif absent ou trop court")
                if largeur_png(png) > 1100:
                    problemes.append(f"{genre} {oid} [IMAGE_{pos}] : {fichier} trop large ({largeur_png(png)} px > 1100)")
            elif pos in en_ligne.get((genre, oid), {}):
                conservees.append(f"{genre} {oid} [IMAGE_{pos}] = {Path(en_ligne[(genre, oid)][pos]['nom']).name}")
            else:
                problemes.append(f"{genre} {oid} [IMAGE_{pos}] : aucune image (ni nouvelle figure ni image en ligne)")
    for (genre, oid, pos), v in sorted(nouvelles.items(), key=lambda kv: (kv[0][0], str(kv[0][1]), kv[0][2])):
        if pos not in appels.get((genre, oid), set()):
            problemes.append(f"{genre} {oid} : nouvelle figure en position {pos} jamais appelée par [IMAGE_{pos}]")
    a_supprimer = sum(1 for (g, oid), ims in en_ligne.items() for pos in ims
                      if pos not in appels.get((g, oid), set()) and (g, oid, pos) not in nouvelles)

    etat = dossier / "etat.json"
    if not etat.exists():
        notes.append("etat.json absent (statut a_faire)")

    # 4. aperçu (+ navigateur)
    r = subprocess.run(["node", str(ICI / "apercu_notion.mjs"), str(dossier)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        problemes.append("aperçu impossible : " + (r.stderr or r.stdout)[-400:])
    elif "⚠" in r.stderr:
        problemes += [l for l in r.stderr.splitlines() if "⚠" in l]
    if navigateur and r.returncode == 0:
        c = subprocess.run(["node", str(Path(__file__).with_name("controle_apercu_local.mjs")), str(dossier / "apercu.html"), str(dossier / "captures_revision_2026-10-30")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           stdin=subprocess.DEVNULL, timeout=1800)
        mauvais = [l for l in c.stdout.splitlines() if l.startswith("[") and not re.search(
            r"débordement 0px · erreurs formule 0 · \$ bruts 0 · images manquantes 0 · blocs en erreur 0 · éléments trop larges 0", l)]
        details = [l for l in c.stdout.splitlines() if l.startswith("    ")]
        problemes += [f"navigateur : {l}" for l in mauvais] + [f"navigateur   {l.strip()}" for l in details]
        if c.returncode not in (0, 2):
            problemes.append("contrôle navigateur en échec : " + (c.stderr or c.stdout)[-400:])

    print(f"== {dossier.parent.name}/{dossier.name}")
    print(f"   {len(meta['cours'])} cours, {len(meta['fiches'])} fiche(s), {len(meta['exercices'])} exercice(s) ; "
          f"{len(nouvelles)} nouvelle(s) figure(s), {len(conservees)} image(s) en ligne conservée(s), "
          f"{a_supprimer} image(s) en ligne non appelée(s) → supprimée(s) à l'import")
    for c in conservees:
        print("   · conservée :", c)
    for n in notes:
        print("   ·", n)
    for p in problemes:
        print("   ✗", p)
    print(f"   {'OK' if not problemes else str(len(problemes)) + ' problème(s)'}")
    return problemes


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    total = 0
    for d in args:
        total += len(verifier(d, "--navigateur" in sys.argv))
    sys.exit(1 if total else 0)
