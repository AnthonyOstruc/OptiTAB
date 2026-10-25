"""Affichage des exceptions exactement comme IDLE (idlelib/run.py, Python 3.13).

IDLE transforme chaque étape du traceback en tuple (fichier, ligne, fonction,
texte) avant de l'afficher : il n'y a donc jamais de lignes « ^^^^ » sous le
code fautif, contrairement à Python lancé dans un terminal. Le message final
des NameError et AttributeError est celui de sys.__excepthook__, avec ses
suggestions « Did you mean… ».
"""
import contextlib
import io
import sys
import traceback

# sources des instructions tapées dans le Shell : {"<pyshell#3>": [lignes]}
SOURCES = {}


def lignes_message(typ, exc, tb):
    if typ in (AttributeError, NameError):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            sys.__excepthook__(typ, exc, tb)
        return [err.getvalue().split("\n")[-2] + "\n"]
    return traceback.format_exception_only(typ, exc)


def imprimer_exception(exc, tb, flux):
    vus = set()

    def imprimer(exc, tb):
        vus.add(id(exc))
        contexte, cause = exc.__context__, exc.__cause__
        if cause is not None and id(cause) not in vus:
            imprimer(cause, cause.__traceback__)
            flux.write("\nThe above exception was the direct cause of the following exception:\n\n")
        elif contexte is not None and not exc.__suppress_context__ and id(contexte) not in vus:
            imprimer(contexte, contexte.__traceback__)
            flux.write("\nDuring handling of the above exception, another exception occurred:\n\n")
        if tb:
            pile = []
            for fs in traceback.extract_tb(tb):
                fn, ln, nm, ligne = fs.filename, fs.lineno, fs.name, fs.line
                if nm == "?":
                    nm = "-toplevel-"
                if not ligne and fn in SOURCES:
                    ligne = SOURCES[fn][ln - 1]
                pile.append((fn, ln, nm, ligne))
            flux.write("Traceback (most recent call last):\n")
            flux.write("".join(traceback.format_list(pile)))
        flux.write("".join(lignes_message(type(exc), exc, tb)))

    imprimer(exc, tb)
