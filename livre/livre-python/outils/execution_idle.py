"""Exécute un programme comme IDLE le fait avec Run > Run Module (F5).

Usage : python -X utf8 execution_idle.py programme.py   (dans le dossier du programme)
Variable OTPY_SAISIES : liste JSON des réponses aux input() ; chaque saisie est
recopiée dans la sortie sous la forme «texte» suivie d'un retour à la ligne,
comme elle apparaît à l'écran quand on la tape.

* erreur de syntaxe : IDLE l'annonce dans une boîte « SyntaxError » ; on écrit
  « SyntaxError: message » (code de sortie 1) ;
* autre erreur : traceback au format d'IDLE (sans « ^^^ »), code de sortie 1.
"""
import builtins
import json
import os
import sys

from idle_commun import imprimer_exception

saisies = json.loads(os.environ.get("OTPY_SAISIES", "[]"))


def entree(invite=""):
    sys.stdout.write(str(invite))
    if not saisies:
        raise EOFError("EOF when reading a line")
    valeur = saisies.pop(0)
    sys.stdout.write("«" + valeur + "»\n")
    return valeur


builtins.input = entree
nom = sys.argv[1]
sys.argv = [nom]
sys.path[0] = os.getcwd()
with open(nom, encoding="utf-8") as f:
    source = f.read()
try:
    code = compile(source, nom, "exec")
except (SyntaxError, OverflowError, ValueError) as e:
    msg = getattr(e, "msg", "") or e or "<no detail available>"
    sys.stdout.flush()
    sys.stderr.write("SyntaxError: %s\n" % msg)
    sys.exit(1)
espace = {"__name__": "__main__", "__file__": nom, "__builtins__": builtins}
try:
    exec(code, espace)
except SystemExit:
    raise
except BaseException as e:  # noqa: BLE001 - on reproduit IDLE
    sys.stdout.flush()
    imprimer_exception(e, e.__traceback__.tb_next, sys.stderr)
    sys.exit(1)
