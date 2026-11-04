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
