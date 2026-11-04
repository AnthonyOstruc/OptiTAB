# -*- coding: utf-8 -*-
"""Moteur commun aux scripts de vérification de la notion (programmes EXÉCUTÉS).

Chaque fichier final (cours, fiche, exercices) est lu ligne à ligne :
- un « document » = le cours, la fiche, ou un exercice (bloc === … ===) ;
  ses blocs ```python sont exécutés dans l'ordre, dans un même espace de noms
  (une fonction définie plus haut reste utilisable plus bas) ;
- chaque bloc ```console doit être EXACTEMENT l'affichage du dernier programme
  exécuté qui le précède ; --remplir réécrit ces blocs avec l'affichage réel ;
- un programme contenant « … » est un programme à compléter : non exécuté ;
- un programme qui consomme du hasard sans appeler seed(…) est refusé
  (les simulations doivent être reproductibles) ;
- largeur sur téléphone : ≤ 35 caractères au premier niveau, ≤ 31 dans un
  encadré, ≤ 29 dans une étape (mesures des notions 99 et 164) ;
- une boucle qui dépasse 5 000 000 de lignes exécutées est signalée.
"""
import contextlib
import io
import random
import re
import sys
from pathlib import Path

LARGEUR = {"haut": 35, "encadre": 31, "etape": 29}
FENCE = re.compile(r"^([ \t]*)```(python|console)[ \t]*$")
FIN = re.compile(r"^[ \t]*```[ \t]*$")


class TropLong(Exception):
    pass


def executer(code, ns, limite=5_000_000):
    compteur = [0]

    def trace(frame, event, arg):
        if event == "line":
            compteur[0] += 1
            if compteur[0] > limite:
                raise TropLong
        return trace

    tampon = io.StringIO()
    sys.settrace(trace)
    try:
        with contextlib.redirect_stdout(tampon):
            exec(compile(code, "<bloc>", "exec"), ns)
    finally:
        sys.settrace(None)
    return tampon.getvalue()


def normal(t):
    return "\n".join(l.rstrip() for l in t.strip("\n").splitlines())


def analyser(path, remplir=False, montrer=False):
    """Renvoie (erreurs, stats) ; avec remplir=True, réécrit les blocs console."""
    lignes = path.read_text(encoding="utf-8").split("\n")
    erreurs = []
    stats = {"programmes": 0, "affichages": 0, "trous": 0}
    sortie_lignes = []
    ns = {"__name__": "__main__"}
    nom = path.stem
    pile = []
    derniere = None
    i = 0
    while i < len(lignes):
        l = lignes[i]
        s = l.strip()
        if s.startswith("==="):
            ns = {"__name__": "__main__"}
            derniere = None
            pile = []
            nom = path.stem + " / " + s[3:].strip()[:40]
        m_id = re.match(r"^Id:\s*(\S+)", l)
        if m_id:
            nom = "exercice " + m_id.group(1)
        if re.match(r"^(Énoncé|Étapes|Solution):", s):
            pile = []
        m = FENCE.match(l)
        if m:
            base = len(m.group(1))
            genre = m.group(2)
            j = i + 1
            corps = []
            while j < len(lignes) and not FIN.match(lignes[j]):
                x = lignes[j]
                corps.append(x[base:] if x[:base].strip() == "" else x.lstrip())
                j += 1
            ctx = "haut" if not pile else ("etape" if pile[-1] in ("etape", "point") else "encadre")
            code = "\n".join(corps)
            for x in corps:
                if len(x) > LARGEUR[ctx]:
                    erreurs.append(f"{nom} l.{i + 1} : ligne trop longue pour un téléphone "
                                   f"({len(x)} > {LARGEUR[ctx]}, {ctx}) : {x}")
            nouvelles = None
            if genre == "python":
                if "…" in code:
                    stats["trous"] += 1
                    derniere = None
                else:
                    stats["programmes"] += 1
                    etat = random.getstate()
                    try:
                        derniere = executer(code, ns)
                    except TropLong:
                        erreurs.append(f"{nom} l.{i + 1} : le programme ne s'arrête pas")
                        derniere = None
                    except Exception as e:  # noqa: BLE001
                        erreurs.append(f"{nom} l.{i + 1} : le programme échoue ({type(e).__name__} : {e})")
                        derniere = None
                    if random.getstate() != etat and "seed(" not in code:
                        erreurs.append(f"{nom} l.{i + 1} : simulation sans graine (seed) dans le programme")
                    if montrer and derniere is not None:
                        print(f"--- {nom} l.{i + 1}\n{derniere}", end="" if derniere.endswith("\n") else "\n")
            else:
                stats["affichages"] += 1
                if derniere is None:
                    erreurs.append(f"{nom} l.{i + 1} : affichage sans programme exécuté juste avant")
                elif normal(derniere) != normal(code):
                    if remplir:
                        nouvelles = [" " * base + x for x in normal(derniere).split("\n")]
                    else:
                        erreurs.append(f"{nom} l.{i + 1} : affichage différent de l'exécution\n"
                                       f"      écrit  : {normal(code)!r}\n      obtenu : {normal(derniere)!r}")
                derniere = None if genre == "console" else derniere
            sortie_lignes.append(l)
            sortie_lignes.extend(nouvelles if nouvelles is not None else lignes[i + 1:j])
            if j < len(lignes):
                sortie_lignes.append(lignes[j])
            i = j + 1
            continue
        if re.match(r"^:::\s*\S", s):
            pile.append(s[3:].split()[0])
        elif s == ":::" and pile:
            pile.pop()
        sortie_lignes.append(l)
        i += 1
    if remplir:
        nouveau = "\n".join(sortie_lignes)
        if nouveau != "\n".join(lignes):
            path.write_text(nouveau, encoding="utf-8")
            print(f"{path.name} : affichages remplis avec l'exécution réelle")
    return erreurs, stats


def bloc_console_apres(texte, motif):
    """Contenu du premier bloc console qui suit la première occurrence de `motif`."""
    k = texte.index(motif)
    m = re.search(r"```console[ \t]*\n(.*?)\n[ \t]*```", texte[k:], re.S)
    return "\n".join(x.strip() for x in m.group(1).splitlines())
