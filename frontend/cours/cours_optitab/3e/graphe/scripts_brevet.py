# -*- coding: utf-8 -*-
"""Scripts Scratch des sujets type brevet (dessinés et exécutés pour contrôle)."""
from scratch3e import V, ANS, P, op, cmp

FLAG = ("flag",)

SCRIPTS = {
    "s02": [[("define", "carré", ["côté"]),
             ("repeat", 4, [("move", P("côté")), ("left", 90)])],
            [FLAG, ("clear",), ("goto", 0, 0), ("point", 90), ("pendown",), ("set", "c", 10),
             ("repeat", 4, [("call", "carré", [V("c")]), ("penup",),
                            ("move", op("+", V("c"), 5)), ("pendown",), ("change", "c", 5)])]],
    "s04": [[FLAG, ("ask", "Choisis un nombre"), ("set", "x", ANS),
             ("set", "a", op("-", V("x"), 3)), ("set", "b", op("+", V("x"), 3)),
             ("set", "r", op("*", V("a"), V("b"))), ("say", V("r"))]],
    "s06": [[FLAG, ("set", "n", 5000), ("set", "t", 0),
             ("until", cmp(">", V("n"), 1000000),
              [("set", "n", op("*", V("n"), 2)), ("change", "t", 20)]),
             ("say", V("t"))]],
    "s08": [[FLAG, ("ask", "Durée de la course en minutes ?"), ("set", "t", ANS),
             ("set", "v", op("/", op("*", 10.8, 60), V("t"))), ("saysec", V("v"), 2),
             ("ifelse", cmp(">", V("v"), 12), [("say", "Objectif atteint !")],
              [("say", "Objectif manqué")])]],
}
TITRES = {"s02": ["Bloc personnalisé", "Script principal"]}
