# -*- coding: utf-8 -*-
"""Vérification de la notion « Conditions / Logique » (Terminale) : chaque programme est exécuté.

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
FICHIERS = ["cours_103.txt", "fiche_35.txt", "exercices.txt"]
LARGEUR_MAX = 30

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
            if "bloc1" in code:  # gabarit de syntaxe, non exécutable
                n_ok += 1
                continue
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
from verif_conditions_assertions import assertions  # noqa: E402


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
