# -*- coding: utf-8 -*-
"""Audit indépendant des notions importées (lecture seule, ne modifie rien).

    python audit_niveau.py terminale 2nde …

Pour chaque notion au statut « importe » :
  1. relance son ou ses scripts verif_*.py (tous les calculs doivent passer) ;
  2. contrôle la rédaction de chaque exercice : énoncé numéroté, étapes avec
     « ## Question », méthode, étape détaillée et résultat pour chaque question,
     solution non vide ;
  3. traque les restes : \\displaystyle, « à compléter », TODO, texte anglais,
     encadrés vides, questions sans corrigé, doublons d'énoncés ;
  4. mesure le cours et la fiche (trop courts = suspect).
"""
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
CHANTIER = ICI.parent / "chantier"

RESTES = [
    (r"\\displaystyle", "\\displaystyle"),
    (r"(?i)\bà compléter\b|\bTODO\b|\bFIXME\b|XXX", "texte provisoire"),
    (r"(?i)\b(the|and|with|which|step|answer)\b", "mot anglais"),
    (r"::: ?\w+[^\n]*\n:::", "encadré vide"),
    (r"(?<!\$)\$[ 	]+\$(?!\$)", "formule vide"),
    (r"\?\?|!!", "ponctuation douteuse"),
]


def blocs(path):
    out = []
    for b in re.split(r"^===[ \t]*$", path.read_text(encoding="utf-8"), flags=re.M):
        b = b.strip()
        if not b:
            continue
        pos = {m.group(1): m for m in re.finditer(r"^(Énoncé|Étapes|Solution):[ \t]*$", b, re.M)}
        if set(pos) != {"Énoncé", "Étapes", "Solution"}:
            out.append((b.splitlines()[0], None, None, None))
            continue
        out.append((b.splitlines()[0].replace("===", "").strip(),
                    b[pos["Énoncé"].end():pos["Étapes"].start()],
                    b[pos["Étapes"].end():pos["Solution"].start()],
                    b[pos["Solution"].end():]))
    return out


def audit(dossier):
    pb = []
    # 1. calculs
    for v in sorted(dossier.glob("verif*.py")):
        r = subprocess.run([sys.executable, v.name], cwd=dossier, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=900,
                           env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"})
        if r.returncode != 0:
            pb.append(f"calculs : {v.name} échoue → {(r.stdout + r.stderr).strip().splitlines()[-1][:120] if (r.stdout + r.stderr).strip() else 'code ' + str(r.returncode)}")
    if not list(dossier.glob("verif*.py")):
        pb.append("calculs : aucun script de vérification")
    # 2. exercices
    ex = dossier / "exercices.txt"
    enonces = {}
    if ex.exists():
        for titre, en, et, so in blocs(ex):
            court = titre[:50]
            if en is None:
                pb.append(f"« {court} » : rubriques manquantes")
                continue
            q_en = len(re.findall(r"^\s*\d+[.)]\s", en, re.M))
            q_et = len(re.findall(r"^## Question", et, re.M))
            if q_et == 0:
                pb.append(f"« {court} » : étapes sans « ## Question »")
            elif q_en and q_et < q_en:
                pb.append(f"« {court} » : {q_en} questions dans l'énoncé, {q_et} corrigées dans les étapes")
            for k, part in enumerate(re.split(r"^## Question", et, flags=re.M)[1:], start=1):
                if "::: resultat" not in part and "::: retenir" not in part:
                    pb.append(f"« {court} » Q{k} : pas d'encadré résultat")
                if "::: etape" not in part and "::: point" not in part and "::: methode" not in part:
                    pb.append(f"« {court} » Q{k} : pas d'étape détaillée")
            if len(so.strip()) < 40:
                pb.append(f"« {court} » : solution quasi vide")
            cle = re.sub(r"\s+", " ", en).strip()
            if cle in enonces:
                pb.append(f"« {court} » : même énoncé que « {enonces[cle][:40]} »")
            enonces[cle] = titre
    # 3. restes
    for f in list(dossier.glob("cours_*.txt")) + list(dossier.glob("fiche_*.txt")) + ([ex] if ex.exists() else []):
        t = f.read_text(encoding="utf-8")
        t_sans_code = re.sub(r"```.*?```", "", t, flags=re.S)
        for motif, nom in RESTES:
            n = len(re.findall(motif, t_sans_code))
            if n:
                pb.append(f"{f.name} : {nom} ×{n}")
    # 4. taille
    for f in dossier.glob("cours_*.txt"):
        n = len(f.read_text(encoding="utf-8"))
        if n < 6000:
            pb.append(f"{f.name} : cours court ({n} caractères)")
    for f in dossier.glob("fiche_*.txt"):
        n = len(f.read_text(encoding="utf-8"))
        if n < 1200:
            pb.append(f"{f.name} : fiche courte ({n} caractères)")
    return pb


def main():
    total = 0
    for niveau in sys.argv[1:]:
        for d in sorted(p.parent for p in (CHANTIER / niveau).glob("*/source_en_ligne")):
            etat = d / "etat.json"
            if not etat.exists() or '"importe"' not in etat.read_text(encoding="utf-8"):
                continue
            pb = audit(d)
            total += len(pb)
            print(f"{'✓' if not pb else '✗'} {niveau}/{d.name[:55]} : {len(pb)} point(s)")
            for p in pb[:12]:
                print("     -", p)
            if len(pb) > 12:
                print(f"     … et {len(pb) - 12} autre(s)")
    print(f"\nTOTAL : {total} point(s) à examiner")


if __name__ == "__main__":
    main()
