# -*- coding: utf-8 -*-
"""Construit les fichiers d'exercices de 4ème à partir des sources compactes.

Usage : python construire_4e.py <slug> [<slug> ...]   |   python construire_4e.py all
Source : 4e/sources/exos_<slug>_4e.src  ->  frontend/exercices/4e/exercice_<slug>_4e.txt

Format source (une instruction par ligne) :
  CHAPITRE: Relatifs                       nom court utilisé dans les titres
  %% commentaire                           ignoré
  @@ Découverte | 1. Titre | easy | a.png, b.png
  <lignes d'énoncé ; [IMAGE_1] seul sur sa ligne pour la figure>
  ?? texte de la question                  (une ligne par question, 6 au minimum)
  ## titre de la correction de la question 1
  M> méthode            E> étape (numérotée)     R> résultat
  V> vérification       A> à retenir             F> erreur fréquente
  P> rédaction modèle   [IMAGE_n] figure de correction (ligne seule)
  S> solution courte de la question (une par question)
Les formules s'écrivent $...$ : le constructeur ajoute \\displaystyle comme sur le site.
"""
import re
import sys
from pathlib import Path

FRONT = Path(__file__).resolve().parents[4]
DIR_SRC = FRONT / "cours/cours_optitab/4e/sources"
DIR_E = FRONT / "exercices/4e"
CATS = ["Découverte", "Entraînement", "Problème"]
DIFFS = {"easy", "medium", "hard"}
MIN_Q = 6
BR = "$\\\\$"

LABELS = {
    "M": "**Méthode :**",
    "R": "**Résultat :**",
    "V": "🔎 **Vérification :**",
    "A": "💡 **À retenir :**",
    "F": "⚠️ **Erreur fréquente :**",
    "P": "✍️ **Rédaction :**",
}


class SourceError(Exception):
    pass


def dmath(txt):
    """$x$ -> $\\displaystyle x$ (sans toucher aux formules déjà en displaystyle)."""
    def rep(m):
        inner = m.group(1).strip()
        if inner.startswith("\\displaystyle"):
            return f"${inner}$"
        return f"$\\displaystyle {inner}$"
    if txt.count("$") % 2:
        raise SourceError(f"nombre impair de $ : {txt}")
    return re.sub(r"\$([^$]+)\$", rep, txt)


def parse(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    chap = None
    exos = []
    cur = None
    for no, raw in enumerate(lines, 1):
        line = raw.rstrip()
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        where = f"{path.name}:{no}"
        if s.startswith("CHAPITRE:"):
            chap = s.split(":", 1)[1].strip()
            continue
        if s.startswith("@@"):
            parts = [p.strip() for p in s[2:].split("|")]
            if len(parts) not in (3, 4):
                raise SourceError(f"{where} : en-tête d'exercice invalide")
            cat, titre, diff = parts[:3]
            imgs = [x.strip() for x in parts[3].split(",")] if len(parts) == 4 and parts[3] else []
            if cat not in CATS or diff not in DIFFS:
                raise SourceError(f"{where} : catégorie ou difficulté invalide")
            cur = dict(cat=cat, titre=titre, diff=diff, imgs=imgs, intro=[],
                       questions=[], corr=[], where=where)
            exos.append(cur)
            continue
        if cur is None:
            raise SourceError(f"{where} : texte hors exercice")
        if s.startswith("??"):
            if cur["corr"]:
                raise SourceError(f"{where} : question après le début du corrigé")
            cur["questions"].append(s[2:].strip())
        elif s.startswith("##"):
            cur["corr"].append(dict(titre=s[2:].strip(), items=[], sol=None))
        elif cur["corr"]:
            c = cur["corr"][-1]
            m = re.match(r"^([MERVAFPS])>\s*(.*)$", s)
            if m:
                k, t = m.groups()
                if not t:
                    raise SourceError(f"{where} : élément vide")
                if k == "S":
                    if c["sol"] is not None:
                        raise SourceError(f"{where} : deux solutions courtes")
                    c["sol"] = t
                else:
                    c["items"].append((k, t))
            elif re.fullmatch(r"\[IMAGE_\d+\]", s):
                c["items"].append(("IMG", s))
            else:
                raise SourceError(f"{where} : ligne de corrigé non reconnue : {s[:60]}")
        else:
            if cur["questions"]:
                raise SourceError(f"{where} : texte d'énoncé après les questions")
            cur["intro"].append(s)
    if not chap:
        raise SourceError(f"{path.name} : ligne CHAPITRE manquante")
    return chap, exos


def check(chap, exos, name):
    errs = []
    counts = {c: 0 for c in CATS}
    last = -1
    for ex in exos:
        w = f"{name} « {ex['titre']} »"
        ci = CATS.index(ex["cat"])
        if ci < last:
            errs.append(f"{w} : catégories dans le désordre")
        last = ci
        counts[ex["cat"]] += 1
        m = re.match(r"^(\d)\. ", ex["titre"])
        if not m or int(m.group(1)) != counts[ex["cat"]]:
            errs.append(f"{w} : numéro attendu {counts[ex['cat']]} (un seul chiffre)")
        nq = len(ex["questions"])
        if nq < MIN_Q:
            errs.append(f"{w} : {nq} questions (minimum {MIN_Q})")
        if len(ex["corr"]) != nq:
            errs.append(f"{w} : {nq} questions mais {len(ex['corr'])} corrections")
        peda = 0
        for i, c in enumerate(ex["corr"], 1):
            kinds = [k for k, _ in c["items"]]
            if "R" not in kinds:
                errs.append(f"{w} Q{i} : pas de Résultat")
            if c["sol"] is None:
                errs.append(f"{w} Q{i} : pas de solution courte S>")
            if not ({"M", "E"} & set(kinds)):
                errs.append(f"{w} Q{i} : correction sans méthode ni étape (trop sèche)")
            peda += sum(k in "AF" for k in kinds)
        if peda < 1:
            errs.append(f"{w} : aucun « À retenir » ni « Erreur fréquente »")
        intro = "\n".join(ex["intro"])
        if ex["imgs"]:
            used = set(re.findall(r"\[IMAGE_(\d+)\]", intro + str(ex["corr"])))
            for k in range(1, len(ex["imgs"]) + 1):
                if str(k) not in used:
                    errs.append(f"{w} : image {k} déclarée mais jamais placée")
            for k in used:
                if int(k) > len(ex["imgs"]):
                    errs.append(f"{w} : [IMAGE_{k}] sans image déclarée")
        elif "[IMAGE_" in intro + str(ex["corr"]):
            errs.append(f"{w} : marqueur [IMAGE_n] sans image déclarée")
    for c in CATS:
        if counts[c] != 7:
            errs.append(f"{name} : {counts[c]} exercices « {c} » (7 attendus)")
    return errs


def render(chap, ex):
    out = [f"=== {ex['cat']} - {chap} - {ex['titre']}", f"Difficulté: {ex['diff']}"]
    if ex["imgs"]:
        out.append("Images: " + ", ".join(ex["imgs"]))
    out.append("")
    intro_lines = []
    for i, l in enumerate(ex["intro"]):
        if i and not l.startswith("[IMAGE_") and not intro_lines[-1].startswith("[IMAGE_"):
            intro_lines.append(BR)
        intro_lines.append(dmath(l))
    enonce = []
    if intro_lines:
        intro_lines[0] = "Énoncé: " + intro_lines[0]
        enonce += intro_lines
        enonce.append(BR)
    for i, q in enumerate(ex["questions"], 1):
        line = f"**Question {i} : {dmath(q)}**"
        if not enonce:
            line = "Énoncé: " + line
        enonce.append(line)
        if i < len(ex["questions"]):
            enonce.append(BR)
    out += enonce
    out += ["", "Étapes:", ""]
    for i, c in enumerate(ex["corr"], 1):
        out += [f"**Question {i} : {dmath(c['titre'])}**", ""]
        n_e = 0
        # ordre pédagogique imposé (tri stable) : méthode, étapes, résultat/figure,
        # vérification et rédaction, puis notes « À retenir » / « Erreur fréquente »
        rang = {"M": 0, "E": 1, "R": 2, "IMG": 2, "V": 3, "P": 3, "A": 4, "F": 4}
        for k, t in sorted(c["items"], key=lambda it: rang[it[0]]):
            if k == "IMG":
                out.append(t)
                out.append("")
                continue
            if k == "E":
                n_e += 1
                lab = f"**Étape {n_e} :**"
            else:
                lab = LABELS[k]
            out.append(f"    ● {lab} {dmath(t)}")
            out.append(f"    {BR}")
            out.append("")
    while out and out[-1] == "":
        out.pop()
    if out[-1].strip() == BR:
        out.pop()
    out += ["", "Solution:"]
    for i, c in enumerate(ex["corr"], 1):
        out.append(f"{i}. {dmath(c['sol'])}")
        if i < len(ex["corr"]):
            out.append(BR)
    out += ["", "==="]
    return "\n".join(out)


def construire(slug):
    src = DIR_SRC / f"exos_{slug}_4e.src"
    chap, exos = parse(src)
    errs = check(chap, exos, slug)
    if errs:
        for e in errs:
            print("  [ERREUR]", e)
        return False
    DIR_E.mkdir(parents=True, exist_ok=True)
    txt = "\n\n".join(render(chap, ex) for ex in exos) + "\n"
    (DIR_E / f"exercice_{slug}_4e.txt").write_text(txt, encoding="utf-8")
    nq = sum(len(e["questions"]) for e in exos)
    print(f"[{slug}] {len(exos)} exercices, {nq} questions -> exercice_{slug}_4e.txt")
    return True


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["all"]:
        args = sorted(p.stem[5:-3] for p in DIR_SRC.glob("exos_*_4e.src"))
    ok = True
    for slug in args:
        try:
            ok &= construire(slug)
        except SourceError as e:
            print("  [ERREUR]", e)
            ok = False
    sys.exit(0 if ok else 1)
