# -*- coding: utf-8 -*-
"""Construit le quiz d'une notion pour le site (onglet « Quiz » du chapitre).

    python construire_quiz.py <dossier_notion>

Lit <dossier_notion>/quiz/quiz.py (QUIZ = {...}, voir format_v1/QUIZ.md),
contrôle tout, puis écrit :
  - frontend/src/data/quiz/<notion>.json            (contenu du quiz)
  - frontend/public/quiz/<notion>/<figure>.png       (figures, depuis quiz/figures/images/)
Les figures se compilent avant avec : python figures_livre.py <dossier_notion>/quiz

Contrôles : schéma de chaque type, figures présentes, et pour chaque question
« saisie » les exemples `acceptees` (doivent être justes) et `refusees` (doivent
être fausses) passés au vrai correcteur du site (src/utils/quizMath.js, via node).
Rien n'est écrit si un contrôle échoue. N'écrit jamais en base.
"""
import importlib.util
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[4]          # OptiTABV2/
FRONT = RACINE / "frontend"
DATA = FRONT / "src" / "data" / "quiz"
PUBLIC = FRONT / "public" / "quiz"
QUIZMATH = FRONT / "src" / "utils" / "quizMath.js"

TYPES = {"qcm", "multi", "vf", "saisie", "associer", "ordre"}
NIVEAUX = {"Découverte", "Entraînement", "Approfondissement"}


def taille_png(chemin):
    with open(chemin, "rb") as f:
        tete = f.read(24)
    return struct.unpack(">II", tete[16:24])


def charger(dossier):
    src = dossier / "quiz" / "quiz.py"
    spec = importlib.util.spec_from_file_location("quiz_notion", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QUIZ


def controler(quiz, images):
    err = []
    figures = set()

    def fig(nom, ou):
        if nom is None:
            return
        if not (images / f"{nom}.png").exists():
            err.append(f"{ou} : figure « {nom} » introuvable dans quiz/figures/images/")
        figures.add(nom)

    for cle in ("notion", "titre", "parties", "questions"):
        if cle not in quiz:
            err.append(f"clé « {cle} » manquante")
    for p in quiz.get("parties") or []:
        if not any(q.get("partie") == p for q in quiz.get("questions", [])):
            err.append(f"partie « {p} » : aucune question")
    ids = set()
    for i, q in enumerate(quiz.get("questions", []), 1):
        ou = f"question {i} ({q.get('id', '?')})"
        if q.get("id") in ids or not q.get("id"):
            err.append(f"{ou} : id manquant ou en double")
        ids.add(q.get("id"))
        t = q.get("type")
        if t not in TYPES:
            err.append(f"{ou} : type « {t} » inconnu")
            continue
        if q.get("partie") not in (quiz.get("parties") or []):
            err.append(f"{ou} : « partie » doit être l'une des « parties » du cours ({q.get('partie')!r})")
        if q.get("niveau") not in NIVEAUX:
            err.append(f"{ou} : niveau « {q.get('niveau')} » (attendu : {', '.join(sorted(NIVEAUX))})")
        for cle in ("enonce", "explication"):
            if not str(q.get(cle, "")).strip():
                err.append(f"{ou} : « {cle} » vide")
        fig(q.get("figure"), ou)
        fig(q.get("figure_corrige"), ou)
        if t in ("qcm", "multi"):
            n = len(q.get("choix") or q.get("choix_figures") or [])
            if n < 2:
                err.append(f"{ou} : au moins 2 choix")
            for nom in q.get("choix_figures") or []:
                fig(nom, ou)
            if t == "qcm" and not (isinstance(q.get("bonne"), int) and 0 <= q["bonne"] < n):
                err.append(f"{ou} : « bonne » doit être l'indice d'un choix")
            if t == "multi":
                b = q.get("bonnes") or []
                if not b or any(not (0 <= k < n) for k in b):
                    err.append(f"{ou} : « bonnes » = indices des bons choix")
        if t == "vf" and not isinstance(q.get("reponse"), bool):
            err.append(f"{ou} : « reponse » = True ou False")
        if t == "saisie":
            if q.get("nature") not in ("nombre", "expression"):
                err.append(f"{ou} : « nature » = nombre ou expression")
            if not q.get("reponses"):
                err.append(f"{ou} : « reponses » vide")
            if not q.get("acceptees") or not q.get("refusees"):
                err.append(f"{ou} : donner des exemples « acceptees » et « refusees »")
        if t == "associer":
            g, d = q.get("gauche") or [], q.get("droite") or q.get("droite_figures") or []
            if len(g) < 2 or len(g) != len(d):
                err.append(f"{ou} : « gauche » et « droite » de même longueur (≥ 2), gauche[i] ↔ droite[i]")
            for nom in q.get("droite_figures") or []:
                fig(nom, ou)
        if t == "ordre" and len(q.get("etapes") or []) < 3:
            err.append(f"{ou} : au moins 3 étapes")
    return err, figures


def controler_saisies(quiz):
    """Passe les exemples au correcteur du site (node + quizMath.js)."""
    cas = []
    for q in quiz["questions"]:
        if q.get("type") != "saisie":
            continue
        regle = {k: q.get(k) for k in ("reponses", "nature", "variable", "tolerance", "intervalle") if q.get(k) is not None}
        for s in q.get("acceptees", []):
            cas.append({"id": q["id"], "saisie": s, "regle": regle, "attendu": True})
        for s in q.get("refusees", []):
            cas.append({"id": q["id"], "saisie": s, "regle": regle, "attendu": False})
    if not cas:
        return []
    script = (
        f"import {{ comparer }} from '{QUIZMATH.as_uri()}';"
        "const cas = JSON.parse(process.argv[1]); const bad = [];"
        "for (const c of cas) { const r = comparer(c.saisie, c.regle); if (r.ok !== c.attendu) bad.push(c.id + ' : « ' + c.saisie + ' » ' + (c.attendu ? 'refusée à tort' : 'acceptée à tort') + (r.erreur ? ' (' + r.erreur + ')' : '')); }"
        "console.log(JSON.stringify(bad));"
    )
    out = subprocess.run(["node", "--input-type=module", "-e", script, json.dumps(cas, ensure_ascii=False)],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        return [f"node : {out.stderr.strip()[:300]}"]
    return json.loads(out.stdout.strip() or "[]")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    dossier = Path(sys.argv[1]).resolve()
    quiz = charger(dossier)
    images = dossier / "quiz" / "figures" / "images"
    err, figures = controler(quiz, images)
    if not err:
        err += controler_saisies(quiz)
    if err:
        print("✗ quiz refusé :")
        for e in err:
            print("  -", e)
        sys.exit(1)

    notion = quiz["notion"]
    cible = PUBLIC / str(notion)
    cible.mkdir(parents=True, exist_ok=True)
    tailles = {}
    for nom in sorted(figures):
        shutil.copyfile(images / f"{nom}.png", cible / f"{nom}.png")
        w, h = taille_png(images / f"{nom}.png")
        tailles[nom] = {"src": f"/quiz/{notion}/{nom}.png", "w": round(w / 2), "h": round(h / 2)}
    # figures retirées du quiz : supprimées du dossier public
    for vieux in cible.glob("*.png"):
        if vieux.stem not in figures:
            vieux.unlink()

    def resoudre(nom):
        return tailles.get(nom) if nom else None

    sortie = {k: v for k, v in quiz.items() if k != "questions"}
    sortie["questions"] = []
    for q in quiz["questions"]:
        q = {k: v for k, v in q.items() if k not in ("acceptees", "refusees")}
        for cle in ("figure", "figure_corrige"):
            if q.get(cle):
                q[cle] = resoudre(q[cle])
        for cle in ("choix_figures", "droite_figures"):
            if q.get(cle):
                q[cle] = [resoudre(n) for n in q[cle]]
        sortie["questions"].append(q)
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / f"{notion}.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")
    nb = len(quiz["questions"])
    types = sorted({q["type"] for q in quiz["questions"]})
    print(f"✓ quiz {notion} : {nb} questions ({', '.join(types)}), {len(figures)} figures → src/data/quiz/{notion}.json")


if __name__ == "__main__":
    main()
