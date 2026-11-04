# -*- coding: utf-8 -*-
"""Génère frontend/exercices/3e/exercice_brevet_3e.txt (sujets complets type brevet).

Le contenu est dans brevet_sujets_a.py (sujets 01 à 05) et brevet_sujets_b.py (06 à 10) ;
chaque sujet porte sa fonction de contrôle (assertions), exécutée avant l'écriture.
Notation : §...§ = formule ($\\displaystyle ...$) ; [IMG:nom] = figure brevet_3e_nom.png.

Usage : python outils/brevet_3e.py
"""
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
sys.path.insert(0, str(ICI.parent / "graphe"))
FRONT = ICI.parents[3]
SORTIE = FRONT / "exercices/3e/exercice_brevet_3e.txt"

BR = "$\\\\$"


def A(question, correction, court):
    return dict(q=question, c=correction, s=court)


def Q(label, enonce, etapes, court):
    return dict(label=label, q=enonce, steps=etapes, s=court)


def X(titre, texte, questions, retenir):
    return dict(titre=titre, texte=texte, questions=questions, retenir=retenir)


def S(num, titre, autos, exos, check):
    assert len(autos) == 10 and len(exos) == 4, num
    return dict(num=num, titre=titre, autos=autos, exos=exos, check=check)


def math(t):
    return re.sub(r"§(.+?)§", lambda m: "$\\displaystyle " + m.group(1) + "$", t)


def puce(kind, txt, n=None):
    nom = {"M": "Méthode", "R": "Résultat"}.get(kind) or f"Étape {n}"
    return f"    ● **{nom} :** {math(txt)}\n    {BR}\n"


def rendre(su):
    images = []

    def img(t):
        def rep(m):
            f = f"brevet_3e_{m.group(1)}.png"
            if f not in images:
                images.append(f)
            return f"[IMAGE_{images.index(f) + 1}]"
        return re.sub(r"\[IMG:(\w+)\]", rep, t)

    e = ["Sujet complet de type brevet (session 2027) : durée 2 heures, noté sur 20 points. "
         "La partie 1 se traite sans calculatrice ; la calculatrice est autorisée pour la "
         "partie 2.", BR,
         "**PARTIE 1 — AUTOMATISMES (20 minutes, sans calculatrice, 6 points)**", BR]
    for i, a in enumerate(su["autos"], 1):
        e += [f"**Question {i} : {math(a['q'])}**", BR]
    e += ["**PARTIE 2 — RAISONNEMENT ET RÉSOLUTION DE PROBLÈMES (1 h 40, calculatrice "
          "autorisée, 14 points)**", BR]
    for k, x in enumerate(su["exos"], 1):
        e += [f"**Exercice {k} — {x['titre']} (3,5 points)**", BR, img(math(x["texte"])), BR]
        for j, q in enumerate(x["questions"], 1):
            e += [f"**Question {k}.{j} : {img(math(q['q']))}**", BR]
    enonce = "\n".join(e[:-1])

    from methodes.brevet import AUTOS, METHODES
    et = []
    for i, a in enumerate(su["autos"], 1):
        et += [f"**Partie 1 — Question {i}**", ""]
        if (su["num"], i) in AUTOS:
            et.append(puce("M", AUTOS[(su["num"], i)]))
        et.append(puce("R", a["c"]))
    for k, x in enumerate(su["exos"], 1):
        for j, q in enumerate(x["questions"], 1):
            et += [f"**Exercice {k} — Question {k}.{j} : {math(q['label'])}**", ""]
            n = 0
            etapes_q = list(q["steps"])
            if [s[0] for s in etapes_q] == ["R"] and (su["num"], k, j) in METHODES:
                etapes_q.insert(0, "M: " + METHODES[(su["num"], k, j)])
            for st in etapes_q:
                kind, txt = st[0], st[2:].strip()
                if kind == "E":
                    n += 1
                et.append(puce(kind, img(txt), n))
            if j == len(x["questions"]):
                et.append(f"    ● 💡 **À retenir :** {math(x['retenir'])}\n")
    etapes = "\n".join(et).rstrip() + "\n"

    sol = ["Partie 1 : " + " ; ".join(f"{i}) {math(a['s'])}" for i, a in
                                      enumerate(su["autos"], 1)), BR]
    for k, x in enumerate(su["exos"], 1):
        sol += [f"Exercice {k} : " + " ; ".join(f"{k}.{j}) {math(q['s'])}" for j, q in
                                                enumerate(x["questions"], 1)), BR]
    solution = "\n".join(sol[:-1])

    titre = f"=== Type brevet - Sujet - {su['num']}. {su['titre']}"
    tete = [titre, "Difficulté: hard"]
    if images:
        tete.append("Images: " + ", ".join(images))
    return "\n".join(tete) + "\n\nÉnoncé: " + enonce + "\n\nÉtapes:\n\n" + etapes + \
        "\nSolution:\n" + solution + "\n\n===\n"


def main():
    from brevet_sujets_a import SUJETS as SA
    from brevet_sujets_b import SUJETS as SB
    sujets = SA + SB
    for su in sujets:
        su["check"]()
        brut = "".join(str(v) for v in [su["autos"], su["exos"]])
        assert "*" not in brut.replace("**", ""), f"astérisque isolé dans le sujet {su['num']}"
    texte = "\n".join(rendre(su) for su in sujets)
    SORTIE.write_text(texte, encoding="utf-8")
    print(f"{len(sujets)} sujets écrits dans {SORTIE.name} ; contrôles : OK")


if __name__ == "__main__":
    main()
