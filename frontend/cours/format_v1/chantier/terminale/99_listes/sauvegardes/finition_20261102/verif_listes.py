# -*- coding: utf-8 -*-
"""Vérification de la notion « Listes » (Terminale) : chaque programme est exécuté.

    python verif_listes.py

1. Chaque bloc ```python des fichiers finaux (cours, fiche, exercices) est
   exécuté dans un espace de noms neuf ; s'il est suivi d'un bloc ```console,
   l'affichage obtenu doit être identique (une erreur attendue s'écrit
   « NomErreur: message » en dernière ligne). Un bloc sans affichage doit
   s'exécuter sans erreur.
2. Les résultats annoncés dans le texte (tableaux, valeurs en ligne) sont
   recalculés par les assertions de la partie 2.
3. Largeur : aucune ligne de code de plus de LARGEUR_MAX caractères (téléphone).
Code de sortie 0 seulement si tout est juste.
"""
import contextlib
import io
import re
import sys
import traceback
from pathlib import Path

ICI = Path(__file__).resolve().parent
FICHIERS = ["cours_105.txt", "fiche_37.txt", "exercices.txt"]
LARGEUR_MAX = 36

FENCE = re.compile(r"^(\s*)```\s*([A-Za-z0-9_+-]*)\s*$")


def blocs(texte):
    """Liste des blocs de code (langage, numéro de ligne, texte), dans l'ordre."""
    lignes = texte.split("\n")
    out, i = [], 0
    while i < len(lignes):
        m = FENCE.match(lignes[i])
        if m and m.group(2):
            base = len(m.group(1))
            corps, j = [], i + 1
            while j < len(lignes) and not re.match(r"^\s*```\s*$", lignes[j]):
                l = lignes[j]
                corps.append(l[base:] if l[:base].strip() == "" else l.lstrip())
                j += 1
            out.append((m.group(2), i + 1, "\n".join(corps).rstrip("\n"), j))
            i = j + 1
            continue
        i += 1
    return out, lignes


def executer(code):
    tampon = io.StringIO()
    ns = {"__name__": "__main__"}
    erreur = None
    with contextlib.redirect_stdout(tampon):
        try:
            exec(compile(code, "<bloc>", "exec"), ns)
        except Exception as e:  # noqa: BLE001
            erreur = f"{type(e).__name__}: {e}"
    sortie = tampon.getvalue().rstrip("\n")
    if erreur:
        sortie = (sortie + "\n" if sortie else "") + erreur
    return sortie, erreur


def verifier_fichier(nom, problemes):
    texte = (ICI / nom).read_text(encoding="utf-8")
    liste, lignes = blocs(texte)
    n_ok = 0
    for k, (lang, no, code, fin) in enumerate(liste):
        if lang == "python":
            for l in code.split("\n"):
                if len(l) > LARGEUR_MAX:
                    problemes.append(f"{nom} l.{no} : ligne de code trop longue ({len(l)} car.) : {l}")
            suivant = liste[k + 1] if k + 1 < len(liste) else None
            entre = lignes[fin + 1: suivant[1] - 1] if suivant else []
            attendu = None
            if suivant and suivant[0] == "console" and all(not x.strip() or x.strip().startswith(":::") for x in entre):
                attendu = suivant[2]
            sortie, erreur = executer(code)
            if attendu is None:
                if erreur:
                    problemes.append(f"{nom} l.{no} : erreur à l'exécution : {erreur}")
                else:
                    n_ok += 1
            elif sortie != attendu:
                problemes.append(f"{nom} l.{no} : affichage différent\n--- obtenu ---\n{sortie}\n--- annoncé ---\n{attendu}")
            else:
                n_ok += 1
        elif lang == "console":
            for l in code.split("\n"):
                if len(l) > LARGEUR_MAX:
                    problemes.append(f"{nom} l.{no} : ligne d'affichage trop longue ({len(l)} car.) : {l}")
    return n_ok, sum(1 for b in liste if b[0] == "python")


# ---------------------------------------------------------------- partie 2
def assertions():
    pb = []

    def egal(desc, obtenu, attendu):
        if obtenu != attendu:
            pb.append(f"{desc} : obtenu {obtenu!r}, annoncé {attendu!r}")

    # Cours II : erreur d'indice, tranche
    notes = [12, 15, 18, 10, 14]
    try:
        notes[5]
        pb.append("notes[5] aurait dû provoquer IndexError")
    except IndexError as e:
        egal("message IndexError", f"IndexError: {e}", "IndexError: list index out of range")
    egal("notes[1:3]", notes[1:3], [15, 18])
    egal("notes[-k] == notes[n-k]", all(notes[-k] == notes[5 - k] for k in range(1, 6)), True)

    # Cours III : méthodes appliquées successivement à [3, 1, 2]
    L = [3, 1, 2]
    L.append(5); egal("append(5)", L, [3, 1, 2, 5])
    L.insert(0, 7); egal("insert(0, 7)", L, [7, 3, 1, 2, 5])
    L.remove(1); egal("remove(1)", L, [7, 3, 2, 5])
    x = L.pop(); egal("pop() valeur", x, 5); egal("pop() liste", L, [7, 3, 2])
    L = [1, 2, 3]; L.append([4, 5]); egal("append([4, 5])", L, [1, 2, 3, [4, 5]])
    L = [1, 2, 3]; L = L + [4, 5]; egal("L + [4, 5]", L, [1, 2, 3, 4, 5])
    try:
        [1, 2].remove(3)
        pb.append("remove d'une valeur absente aurait dû échouer")
    except ValueError:
        pass
    # insertion (figure) : [5, 10, 15] -> insert(1, 8)
    L = [5, 10, 15]; L.insert(1, 8); egal("insert(1, 8)", L, [5, 8, 10, 15])

    # Cours IV : tableau d'information sur [5, 2, 8, 2, 1]
    L = [5, 2, 8, 2, 1]
    egal("len", len(L), 5); egal("sum", sum(L), 18); egal("min", min(L), 1); egal("max", max(L), 8)
    egal("8 in L", 8 in L, True); egal("index(2)", L.index(2), 1); egal("count(2)", L.count(2), 2)
    egal("sorted prénoms", sorted(["Chloé", "Alice", "Bob"]), ["Alice", "Bob", "Chloé"])
    egal("majuscules avant minuscules", sorted(["abricot", "Zèbre"]), ["Zèbre", "abricot"])
    egal("sort(reverse=True)", sorted([15, 8, 20, 12], reverse=True), [20, 15, 12, 8])
    egal("L = L.sort()", [3, 1].sort(), None)

    # Cours V : moyenne 85/6
    egal("85/6 arrondi 2", round(85 / 6, 2), 14.17)
    egal("85/6 arrondi 1", round(85 / 6, 1), 14.2)

    # Cours VI : constructions
    egal("list(range(5))", list(range(5)), [0, 1, 2, 3, 4])
    egal("[0] * 4", [0] * 4, [0, 0, 0, 0])
    egal("concaténation", [1, 2] + [3, 4], [1, 2, 3, 4])
    u = [3]
    for _ in range(5):
        u.append(2 * u[-1] - 1)
    egal("suite u", u, [3, 5, 9, 17, 33, 65])
    egal("filtre impairs", [x for x in [2, 4, 5, 6] if x % 2 != 0], [5])

    # Copie
    L = [1, 2, 3]; M = L; M.append(4); N = L.copy(); N.append(5)
    egal("alias", L, [1, 2, 3, 4]); egal("copie", N, [1, 2, 3, 4, 5])

    # Exercices
    egal("838 index 13", _erreur(lambda: [15, 12, 18, 12, 10].index(13)), "ValueError: 13 is not in list")
    egal("838 x = 18", [15, 12, 18, 12, 10].index(18), 2)
    egal("836 fruits[4]", _erreur(lambda: ["pomme", "banane", "orange", "kiwi"][4]),
         "IndexError: list index out of range")
    egal("839 accents après", sorted(["éa", "z", "Z"]), ["Z", "z", "éa"])
    s, trace = 0, []
    for note in [14, 12, 16, 10, 18]:
        s += note
        trace.append(s)
    egal("840 trace somme", trace, [14, 26, 42, 52, 70])
    return pb


def _erreur(f):
    try:
        f()
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"
    return None


def main():
    problemes = []
    total_ok = total = 0
    for nom in FICHIERS:
        if (ICI / nom).exists():
            ok, n = verifier_fichier(nom, problemes)
            total_ok += ok
            total += n
            print(f"{nom} : {ok}/{n} programme(s) exécuté(s) avec l'affichage annoncé")
    problemes += assertions()
    for p in problemes:
        print("✗", p)
    print("OK" if not problemes else f"{len(problemes)} problème(s)")
    return 1 if problemes else 0


if __name__ == "__main__":
    sys.path.insert(0, str(ICI))
    sys.exit(main())
