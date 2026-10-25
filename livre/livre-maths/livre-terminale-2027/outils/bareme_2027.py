"""Édition 2027-2028 : passage des sujets type bac au barème « 18 points d'exercices + 2 points de maîtrise de la langue ».

Note de service du 11 septembre 2026 (NOR MENE2622642N) : chaque exercice est noté de 4 à 8 points et la maîtrise
de la langue compte pour deux points sur vingt. Ce script, exécuté une seule fois sur les sources copiées de l'édition
2019, réduit d'un point deux exercices par sujet en modifiant des barèmes de questions désignés explicitement, et vérifie
chaque valeur d'origine avant de la remplacer. Usage : python -I -X utf8 outils/bareme_2027.py (depuis livre-terminale-2027).
"""
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# sujet -> {exercice: (ancien total, nouveau total, {indice de question (1-based): (ancien, nouveau)})}
PLAN = {
    1: {2: (5, 4, {2: ("0,75", "0,5"), 4: ("1,5", "1"), 5: ("0,75", "0,5")}),
        3: (6, 5, {2: ("1,25", "1"), 4: ("1", "0,75"), 6: ("0,75", "0,5"), 7: ("1", "0,75")})},
    2: {1: (5, 4, {2: ("1", "0,75"), 3: ("1", "0,75"), 4: ("1", "0,75"), 5: ("1", "0,75")}),
        3: (5, 4, {2: ("1", "0,75"), 4: ("0,75", "0,5"), 5: ("0,75", "0,5"), 6: ("0,75", "0,5")})},
    3: {1: (5, 4, {2: ("0,75", "0,5"), 3: ("0,75", "0,5"), 7: ("0,75", "0,5"), 8: ("0,75", "0,5")}),
        4: (6, 5, {2: ("1,5", "1"), 4: ("1,5", "1")})},
    4: {2: (6, 5, {4: ("1,5", "1"), 5: ("1,25", "0,75")}),
        3: (5, 4, {2: ("1", "0,75"), 3: ("1", "0,75"), 5: ("1,25", "0,75")})},
    5: {2: (5, 4, {2: ("1,5", "1"), 4: ("1,25", "1"), 5: ("0,75", "0,5")}),
        4: (6, 5, {2: ("1,5", "1"), 5: ("1,25", "1"), 6: ("0,75", "0,5")})},
    6: {1: (5, 4, {2: ("1", "0,75"), 3: ("1", "0,75"), 4: ("1", "0,75"), 5: ("1", "0,75")}),
        3: (5, 4, {2: ("1,25", "1"), 3: ("1", "0,75"), 4: ("1", "0,75"), 5: ("0,75", "0,5")})},
    7: {2: (6, 5, {2: ("1", "0,75"), 5: ("1,5", "1"), 7: ("1", "0,75")}),
        4: (5, 4, {2: ("1", "0,75"), 3: ("1", "0,75"), 4: ("1,25", "1"), 5: ("0,75", "0,5")})},
    8: {2: (5, 4, {2: ("1,5", "1"), 3: ("1,25", "1"), 5: ("0,75", "0,5")}),
        3: (6, 5, {2: ("1,5", "1"), 6: ("1,25", "0,75")})},
    9: {1: (5, 4, {1: ("1,25", "1"), 3: ("0,75", "0,5"), 4: ("0,75", "0,5"), 5: ("0,75", "0,5")}),
        4: (6, 5, {2: ("1,25", "1"), 3: ("1", "0,75"), 6: ("1,25", "0,75")})},
    10: {2: (5, 4, {2: ("1,25", "1"), 3: ("1", "0,75"), 4: ("1,25", "1"), 5: ("0,75", "0,5")}),
         4: (5, 4, {1: ("0,75", "0,5"), 2: ("0,75", "0,5"), 5: ("1", "0,75"), 6: ("1,25", "1")})},
}

PTS = re.compile(r"\\pts\{([0-9]+(?:,[0-9]+)?) pts?\}")


def unite(v):
    return "pt"  # convention des corrigés : « 0,5 pt », « 1,5 pt »


def traiter_corrige(num, plan):
    path = RACINE / "bac" / f"corrige-{num:02d}.tex"
    txt = path.read_text(encoding="utf-8")
    env = re.compile(r"\\begin\{corrigeBac\}\{(\d+)\}")
    debuts = [m for m in env.finditer(txt)]
    morceaux, pos = [], 0
    for k, m in enumerate(debuts):
        fin = debuts[k + 1].start() if k + 1 < len(debuts) else len(txt)
        morceaux.append((k + 1, m.start(), fin))
    nouveau = txt
    for ex, deb, fin in reversed(morceaux):
        if ex not in plan:
            continue
        ancien_total, nouveau_total, questions = plan[ex]
        bloc = txt[deb:fin]
        assert bloc.startswith("\\begin{corrigeBac}{%d}" % ancien_total), (num, ex, bloc[:40])
        bloc = bloc.replace("\\begin{corrigeBac}{%d}" % ancien_total, "\\begin{corrigeBac}{%d}" % nouveau_total, 1)
        liste = list(PTS.finditer(bloc))
        for q in sorted(questions, reverse=True):
            a, n = questions[q]
            m = liste[q - 1]
            assert m.group(1) == a, (num, ex, q, m.group(1), a)
            bloc = bloc[:m.start()] + "\\pts{%s %s}" % (n, unite(n)) + bloc[m.end():]
        nouveau = nouveau[:deb] + bloc + nouveau[fin:]
    path.write_text(nouveau, encoding="utf-8", newline="")


def traiter_sujet(num, plan):
    path = RACINE / "bac" / f"sujet-{num:02d}.tex"
    txt = path.read_text(encoding="utf-8")
    # en-tête \sujetBac{n}{Thème/points,...}
    m = re.search(r"\\sujetBac\{%d\}\{([^\n]*)\}\n" % num, txt)
    items = m.group(1).split(",")
    for ex, (a, n, _) in plan.items():
        theme, pts = items[ex - 1].rsplit("/", 1)
        assert int(pts) == a, (num, ex, pts)
        items[ex - 1] = "%s/%d" % (theme, n)
    txt = txt[:m.start(1)] + ",".join(items) + txt[m.end(1):]
    env = list(re.finditer(r"\\begin\{exoBac\}\{(\d+)\}", txt))
    for ex in sorted(plan, reverse=True):
        a, n, _ = plan[ex]
        e = env[ex - 1]
        assert int(e.group(1)) == a, (num, ex, e.group(1))
        txt = txt[:e.start(1)] + str(n) + txt[e.end(1):]
    path.write_text(txt, encoding="utf-8", newline="")


if __name__ == "__main__":
    for num, plan in PLAN.items():
        traiter_corrige(num, plan)
        traiter_sujet(num, plan)
    print("Barèmes 2027 appliqués aux sujets 1 à 10.")
