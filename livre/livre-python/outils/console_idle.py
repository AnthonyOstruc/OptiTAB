"""Simule une session du Shell d'IDLE (Python 3.13) et écrit la transcription.

Entrée (JSON sur stdin) : {"instructions": [[ligne, ...], ...], "saisies": [...]}
  - chaque instruction est la liste de ses lignes telles que tapées après « >>> »
    puis « ... » (une ligne vide finale = la touche Entrée qui termine un bloc) ;
  - saisies : réponses successives aux appels input().
Sortie (stdout) : la transcription exacte, comme IDLE l'affiche.

Fidèle à idlelib : numérotation <pyshell#N> (une par appui sur Entrée), erreurs
de syntaxe réduites à « SyntaxError: message », tracebacks sans « ^^^ »
(voir idle_commun.py).
"""
import builtins
import codeop
import io
import json
import sys

from idle_commun import SOURCES, imprimer_exception

donnees = json.load(sys.stdin)
saisies = list(donnees.get("saisies", []))
sortie = io.StringIO()


def entree(invite=""):
    sortie.write(str(invite))
    if not saisies:
        raise EOFError("EOF when reading a line")
    valeur = saisies.pop(0)
    sortie.write("«" + valeur + "»\n")
    return valeur


builtins.input = entree
espace = {"__name__": "__main__", "__builtins__": builtins}
gid = 0
compilateur = codeop.CommandCompiler()


def montrer(valeur):
    if valeur is not None:
        builtins._ = None
        sortie.write(repr(valeur) + "\n")
        builtins._ = valeur


for instruction in donnees["instructions"]:
    for k, ligne in enumerate(instruction):
        sortie.write((">>> " if k == 0 else "... ") + ligne + "\n")
    # IDLE consomme un numéro <pyshell#N> à chaque appui sur Entrée
    nom = "<pyshell#%d>" % (gid + len(instruction) - 1)
    gid += len(instruction)
    source = "\n".join(instruction).rstrip("\n")
    SOURCES[nom] = source.split("\n")
    try:
        code = compilateur(source, nom, "single")
        if code is None:
            code = compile(source + "\n", nom, "single")
    except (SyntaxError, OverflowError, ValueError) as e:
        msg = getattr(e, "msg", "") or e or "<no detail available>"
        sortie.write("SyntaxError: %s\n" % msg)
        continue
    ancien_stdout, ancien_hook = sys.stdout, sys.displayhook
    sys.stdout, sys.displayhook = sortie, montrer
    try:
        exec(code, espace)
    except SystemExit:
        pass
    except BaseException as e:  # noqa: BLE001 - on reproduit IDLE
        imprimer_exception(e, e.__traceback__.tb_next, sortie)
    finally:
        sys.stdout, sys.displayhook = ancien_stdout, ancien_hook

sys.stdout.write(sortie.getvalue())
