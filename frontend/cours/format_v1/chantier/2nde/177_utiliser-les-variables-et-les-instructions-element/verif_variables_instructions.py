# -*- coding: utf-8 -*-
"""Vérification de la notion 177 (variables et instructions, Python).

- extrait chaque bloc ```python du cours, de la fiche et des exercices ;
- contrôle : lignes <= 30 caractères (<= 29 dans un encadré « etape »),
  pas de guillemets « », pas de $\\ast$ ;
- compile et exécute chaque bloc (délai 3 s) ; compare la sortie au bloc
  ```console qui suit, s'il existe ;
- les erreurs attendues (programmes à trous, erreurs volontaires, boucle
  infinie de l'énoncé) sont listées dans ATTENDU ;
- vérifie les valeurs numériques citées dans les textes.
"""
import math
import os
import subprocess
import sys
import textwrap
from pathlib import Path

ICI = Path(__file__).resolve().parent
FICHIERS = ["cours_221.txt", "fiche_137.txt", "exercices.txt"]

# premier fragment du bloc -> erreur attendue
ATTENDU = {
    "p = ...": "TypeError",                # 1972 Q3 : programme à trous
    "if ...:": "",                         # 1974 Q5 : à trous (Ellipsis, s'exécute)
    "if n % 2 = 0:": "SyntaxError",        # nouveau-1 Q1 : erreur volontaire
    'age = "15"\nprint(age + 1)': "TypeError",  # nouveau-1 Q5
    "n > 0:\n    print(n)\n": "TIMEOUT",   # 1973 Q3 : boucle infinie (fin du bloc)
    "instructions_1": "NameError",         # cours : syntaxe générale
    "    instructions\n": "NameError",     # cours : syntaxe générale
}

problemes = []


def blocs(fichier):
    lignes = (ICI / fichier).read_text(encoding="utf-8").splitlines()
    pile = []
    i = 0
    while i < len(lignes):
        brut = lignes[i]
        l = brut.strip()
        if l.startswith(":::") and l != ":::":
            pile.append(l.split()[1])
        elif l == ":::":
            if pile:
                pile.pop()
        elif l.startswith("```python") or l.startswith("```console"):
            lang = l[3:]
            indent = len(brut) - len(brut.lstrip())
            j = i + 1
            corps = []
            while lignes[j].strip() != "```":
                corps.append(lignes[j][indent:])
                j += 1
            yield lang, "\n".join(corps) + "\n", "etape" in pile, i + 1
            i = j
        i += 1


def executer(code):
    try:
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-c", code],
                           capture_output=True, text=True, timeout=3,
                           encoding="utf-8",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT"
    err = r.stderr.strip().splitlines()[-1] if r.returncode else ""
    return r.stdout, err


n_blocs = 0
for f in FICHIERS:
    liste = list(blocs(f))
    for k, (lang, code, dans_etape, num) in enumerate(liste):
        for ligne in code.splitlines():
            lim = 29 if dans_etape else 30
            if len(ligne) > lim:
                problemes.append(f"{f}:{num} ligne > {lim} : {ligne!r}")
            if "«" in ligne or "»" in ligne or "ast" in ligne and "$" in ligne:
                problemes.append(f"{f}:{num} caractère interdit : {ligne!r}")
        if lang != "python":
            continue
        n_blocs += 1
        sortie, err = executer(code)
        attendu = next((v for c, v in ATTENDU.items()
                        if (code.endswith(c) if v == "TIMEOUT" else c in code)), None)
        if attendu == "":
            continue
        if attendu:
            if not err.startswith(attendu):
                problemes.append(f"{f}:{num} erreur attendue {attendu}, obtenu {err!r}")
            continue
        if err:
            problemes.append(f"{f}:{num} erreur : {err}")
            continue
        if k + 1 < len(liste) and liste[k + 1][0] == "console" \
                and liste[k + 1][3] - num <= len(code.splitlines()) + 4:
            if sortie.strip() != liste[k + 1][1].strip():
                problemes.append(f"{f}:{num} sortie {sortie!r} != console {liste[k + 1][1]!r}")
        print(f"--- {f}:{num}\n{sortie.rstrip()}")

# ---------------------------------------------------------------- finition 2026-11-02
# Programmes des ÉNONCÉS : exécutés tels quels, la sortie (ou l'état final des
# variables) est comparée à la réponse donnée dans le corrigé.
import re

EXO = (ICI / "exercices.txt").read_text(encoding="utf-8")


def enonce(eid, k, remplace=None):
    """k-ième bloc python de l'énoncé de l'exercice eid (désindenté)."""
    b = re.search(r"^Id: %s\n(.*?)(?=^Étapes:)" % re.escape(str(eid)), EXO, re.S | re.M).group(1)
    code = textwrap.dedent(re.findall(r"```python\n(.*?)```", b, re.S)[k])
    if remplace:
        for a, c in remplace:
            assert a in code, (eid, k, a)
            code = code.replace(a, c)
    return code


ATTENDUS = [
    # (Id, n° du bloc dans l'énoncé, remplacements, instructions ajoutées, sortie attendue)
    (1974, 0, None, "", "4"),
    (1974, 1, None, "", "7 est premier"),
    (1974, 2, [("if ...:", "if c == 2:")], "", "2\n3\n5\n7\n11\n13\n17\n19"),
    (1969, 0, None, "print(x)", "20"),
    (1969, 1, None, "print(a, b)", "6 8"),
    (1969, 2, None, "print(a, b)", "9 9"),
    (1969, 3, None, "print(s)", "14"),
    (1970, 0, None, "", "52"),
    (1968, 0, None, "print(a, b, c, d, type(a).__name__, type(b).__name__, type(c).__name__, type(d).__name__)",
     "7 2.0 False maths int float bool str"),
    (1972, 0, None, "", "0\n1\n2\n3\n4"),
    (1972, 1, None, "", "10"),
    (1972, 3, None, "", "12"),
    (1973, 0, None, "", "27"),
    (1973, 1, None, "", "6"),
    (1971, 0, None, "", "Bien"),
    (1971, 0, [("note = 14", "note = 16")], "", "Très bien"),
    (1971, 0, [("note = 14", "note = 8")], "", "Insuffisant"),
    (1971, 1, None, "", "7"),
    (3756, 1, None, "", "5"),            # « Il affiche 5 »
    (3756, 2, None, "", "45"),           # « Il affiche 45 »
    (3756, 3, None, "", "0"),            # « Il affiche 0 »
    ("nouveau-3", 0, None, "", "32.5 True"),
    ("nouveau-4", 0, None, "", "5"),
    ("nouveau-5", 0, None, "", "8"),
    ("nouveau-5", 0, [("u = 6", "u = 7")], "", "16"),
]
for eid, k, remp, ajout, attendu in ATTENDUS:
    code = enonce(eid, k, remp) + (ajout + "\n" if ajout else "")
    sortie, err = executer(code)
    if err or sortie.strip() != attendu:
        problemes.append(f"énoncé {eid} bloc {k} : sortie {sortie.strip()!r} (erreur {err!r}), attendu {attendu!r}")
    else:
        print(f"--- énoncé {eid} bloc {k} : {attendu!r} vérifié par exécution")
# les réponses ci-dessus sont bien celles écrites dans les corrigés
for eid, morceau in ((1974, "Le programme affiche `4`"), (1974, "Il affiche `7 est premier`"), (1969, "$x = 20$"),
                     (1969, "$a = 6$ et $b = 8$"), (1969, "$s = 14$"), (1970, "2. `52`."), (1972, "affichage `12`"),
                     (1973, "1. `27`."), (1973, "affichage `6`"), (1971, "1. `Bien`."), (1971, "`note = 16` : `Très bien`"),
                     (1971, "`note = 8` : `Insuffisant`"), (1971, "4. `7`"), ("nouveau-3", "3. `32.5 True`."),
                     ("nouveau-4", "3. `5`"), ("nouveau-5", "affichage `8`"), ("nouveau-5", "3. `16`.")):
    b = re.search(r"^Id: %s\n(.*?)(?=^===|\Z)" % re.escape(str(eid)), EXO, re.S | re.M).group(1)
    if morceau not in b.split("Solution:")[1]:
        problemes.append(f"{eid} : réponse « {morceau} » absente de la solution")
for eid, morceau in ((3756, "Il affiche $5$"), (3756, "Il affiche $45$"), (3756, "Il affiche $0$")):
    if morceau not in re.search(r"^Id: %s\n(.*?)(?=^Étapes:)" % eid, EXO, re.S | re.M).group(1):
        problemes.append(f"{eid} : « {morceau} » absent de l'énoncé")

# figures de la finition : données = programmes
h, n, hs = 160, 0, []
while h >= 10:
    h = h / 2
    n += 1
    hs.append(h)
if hs != [80, 40, 20, 10, 5] or n != 5:
    problemes.append("figure n2_rebonds : hauteurs")
u, vol = 6, [6]
while u != 1:
    u = u // 2 if u % 2 == 0 else 3 * u + 1
    vol.append(u)
if vol != [6, 3, 10, 5, 16, 8, 4, 2, 1]:
    problemes.append("figure n3_syracuse : vol de 6")
if [500 * 1.03 ** k > 1000 for k in (23, 24)] != [False, True]:
    problemes.append("figure e1973_capital : année 24")
if not (8 * 10 == 50 + 3 * 10 and 8 * 11 > 50 + 3 * 11):
    problemes.append("figure e3757_tarifs : égalité en 10, B moins cher en 11")
if (200 // 60, 200 % 60) != (3, 20) or list(range(2, 8, 2)) != [2, 4, 6]:
    problemes.append("figures e1970 / e1972")


# Valeurs citées dans les textes
def egal(nom, a, b, tol=0.005):
    if abs(a - b) > tol:
        problemes.append(f"valeur {nom} : {a} != {b}")

egal("25 pi", 25 * math.pi, 78.54)
egal("36 pi", 36 * math.pi, 113.10)
egal("4/3 pi 27", 4 / 3 * math.pi * 27, 36 * math.pi, 1e-9)
egal("500*1.03^23", 500 * 1.03 ** 23, 986.79)
egal("500*1.03^24", 500 * 1.03 ** 24, 1016.40)
egal("2^19", 2 ** 19, 524288, 0)
egal("2^20", 2 ** 20, 1048576, 0)
egal("2^9", 2 ** 9, 512, 0)
egal("3^5", 3 ** 5, 243, 0)
egal("3^6", 3 ** 6, 729, 0)
egal("somme 11 impairs", sum(range(1, 22, 2)), 121, 0)
egal("somme 10 impairs", sum(range(1, 20, 2)), 100, 0)
egal("diviseurs 15", len([d for d in range(1, 16) if 15 % d == 0]), 4, 0)
for n, a, b in [(6, 48, 68), (15, 120, 95), (10, 80, 80), (9, 72, 77), (11, 88, 83)]:
    egal(f"tarifs {n}", 8 * n, a, 0)
    egal(f"tarifs {n}", 50 + 3 * n, b, 0)
egal("7 % i", sum(abs(7 % i - v) for i, v in zip(range(1, 8), [0, 1, 1, 3, 2, 1, 0])), 0, 0)
egal("200 min", 200 // 60 * 100 + 200 % 60, 320, 0)

print(f"\n{n_blocs} blocs Python exécutés.")
if problemes:
    print("PROBLÈMES :")
    for p in problemes:
        print(" -", p)
    sys.exit(1)
print("Tout est correct.")
