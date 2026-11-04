# -*- coding: utf-8 -*-
"""Rend les corrigés plus pédagogiques : ajoute une puce « Méthode » aux questions
dont la correction ne contient qu'un « Résultat ».

  python outils/enrichir_3e.py lister <slug>      -> questions concernées (ex, q, énoncé, résultat)
  python outils/enrichir_3e.py appliquer <slug>   -> insère les méthodes de methodes/<slug>.py

methodes/<slug>.py définit METHODES = {(n_exercice, n_question): "texte"} ;
notation §...§ = formule ($\\displaystyle ...$). Idempotent : une question qui a déjà une
puce Méthode/Étape n'est pas modifiée.
"""
import importlib.util
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
FRONT = ICI.parents[3]
BR = "$\\\\$"


def math(t):
    return re.sub(r"§(.+?)§", lambda m: "$\\displaystyle " + m.group(1) + "$", t)


def blocs(raw):
    return re.split(r"(^===\s*$)", raw, flags=re.M)


def questions_enonce(b):
    en = b[b.index("Énoncé:"):b.index("Étapes:")]
    return dict(re.findall(r"^\*\*Question (\d+) : (.*?)\*\*\s*$", en, re.M))


def decouper_etapes(et):
    """liste de (entête, corps) pour chaque question de la section Étapes."""
    parts = re.split(r"(^\*\*Question (\d+) : [^\n]*\*\*[ \t]*$)", et, flags=re.M)
    out = []
    for i in range(1, len(parts), 3):
        out.append((int(parts[i + 1]), parts[i], parts[i + 2]))
    return parts[0], out


def nu(corps):
    puces = re.findall(r"●\s+\*\*([^*:]+?)\s*:\*\*", corps)
    return [p for p in puces if not p.startswith(("💡", "⚠"))] == ["Résultat"]


def parcourir(slug):
    path = FRONT / f"exercices/3e/exercice_{slug}_3e.txt"
    raw = path.read_text(encoding="utf-8")
    morceaux = blocs(raw)
    n_ex = 0
    for idx, b in enumerate(morceaux):
        if not b.strip() or re.match(r"^===\s*$", b):
            continue
        n_ex += 1
        yield path, morceaux, idx, n_ex, b


def lister(slug):
    for _, _, _, n_ex, b in parcourir(slug):
        titre = b.strip().splitlines()[0].replace("===", "").strip()
        qs = questions_enonce(b)
        et = b[b.index("Étapes:"):b.index("Solution:")]
        _, items = decouper_etapes(et)
        for q, _, corps in items:
            if nu(corps):
                res = re.search(r"\*\*Résultat :\*\*(.*)", corps).group(1).strip()
                print(f"[{n_ex}.{q}] {titre[-38:]} | Q: {qs.get(str(q), '?')[:150]} | R: {res[:160]}")


def appliquer(slug):
    spec = importlib.util.spec_from_file_location("m", ICI / "methodes" / f"{slug}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    M = mod.METHODES
    path = None
    morceaux = None
    faits = set()
    for path, morceaux, idx, n_ex, b in parcourir(slug):
        i0, i1 = b.index("Étapes:"), b.index("Solution:")
        tete, items = decouper_etapes(b[i0:i1])
        nouveau = tete
        for q, entete, corps in items:
            cle = (n_ex, q)
            if cle in M and nu(corps):
                puce = f"    ● **Méthode :** {math(M[cle])}\n    {BR}\n    \n"
                corps = re.sub(r"(\n)([ \t]*● \*\*Résultat :\*\*)", lambda m: m.group(1) + puce + m.group(2),
                               corps, count=1)
                faits.add(cle)
            elif cle in M:
                faits.add(cle)
            nouveau += entete + corps
        morceaux[idx] = b[:i0] + nouveau + b[i1:]
    inconnus = set(M) - faits
    assert not inconnus, f"clés sans question correspondante : {sorted(inconnus)}"
    path.write_text("".join(morceaux), encoding="utf-8")
    print(f"[{slug}] {len(M)} méthode(s) appliquée(s)")


if __name__ == "__main__":
    {"lister": lister, "appliquer": appliquer}[sys.argv[1]](sys.argv[2])
