# -*- coding: utf-8 -*-
"""Assertions de la notion « Conditions / Logique » : résultats annoncés dans le texte."""
from itertools import product


def assertions():
    pb = []

    def egal(desc, obtenu, attendu):
        if obtenu != attendu:
            pb.append(f"{desc} : obtenu {obtenu!r}, annoncé {attendu!r}")

    # Tables de vérité et lois de De Morgan
    for A, B in product([True, False], repeat=2):
        egal(f"De Morgan and {A},{B}", not (A and B), (not A) or (not B))
        egal(f"De Morgan or {A},{B}", not (A or B), (not A) and (not B))
    for age in range(0, 120):
        egal(f"négation encadrement {age}", not (18 <= age <= 65), age < 18 or age > 65)
        egal(f"and impossible {age}", age < 18 and age > 65, False)
    egal("priorité and/or", all((p or (a and b)) == (p or a and b) for p, a, b in product([True, False], repeat=3)), True)
    egal("x == 1 or 2 toujours vrai", all(bool(x == 1 or 2) for x in range(-5, 6)), True)
    egal("Lundi/lundi", "Lundi" == "lundi", False)
    egal("120 * 0.9", 120 * 0.9, 108.0)

    # Tarifs de transport (cours VII) : toutes les frontières
    def tarif(age):
        return 0 if age < 4 else 5 if age < 12 else 8 if age < 18 else 12 if age < 65 else 6
    egal("tarifs cours", [tarif(a) for a in (3, 4, 11, 12, 17, 18, 64, 65)], [0, 5, 5, 8, 8, 12, 12, 6])

    # 829 : cinéma, VIP
    def cinema(age, jour):
        return 7 if age < 18 else (9 if jour == "Lundi" else 12) if age < 65 else 8
    egal("cinéma 25 lundi", cinema(25, "Lundi"), 9)
    egal("cinéma 25 lundi minuscule", cinema(25, "lundi"), 12)
    vip = lambda p, pts, e: p or (pts > 1000 and e)  # noqa: E731
    egal("VIP 1200", vip(False, 1200, True), True)
    egal("VIP 800", vip(False, 800, True), False)

    # 830 : prix des billets
    def billet(dest, jours, classe, club):
        prix = {"Paris": 100, "Londres": 150, "New York": 500}[dest]
        if jours > 30:
            prix = prix * 0.8
        if classe == "Affaires":
            prix = prix + 50
        if club:
            prix = prix * 0.9
        return round(prix, 2)
    egal("Londres", billet("Londres", 45, "Économique", True), 108.0)
    egal("New York", billet("New York", 10, "Affaires", False), 550)
    # version erronée avec elif : seule la réduction de 20 %
    egal("Londres avec elif", 150 * 0.8, 120.0)

    # 828 : tarif train, programme mal ordonné
    def train(age):
        return 0 if age < 4 else 8 if age < 18 else 15 if age < 65 else 10
    egal("train", [train(a) for a in (67, 4, 18, 65)], [10, 8, 15, 10])
    egal("ordre faux 30 ans", 8 if 30 >= 4 else None, 8)
    egal("ordre juste", [train(a) for a in (30, 3, 70)], [15, 0, 10])

    # 826
    egal("15 % 2", 15 % 2, 1)
    egal("18 >= 18", 18 >= 18, True)

    # bissextile (cours VI) contre la définition
    def bis(a):
        return (a % 4 == 0 and a % 100 != 0) or a % 400 == 0

    def bis_cours(a):
        if a % 400 == 0:
            return True
        elif a % 100 == 0:
            return False
        else:
            return a % 4 == 0
    egal("bissextile", all(bis(a) == bis_cours(a) for a in range(1, 3001)), True)
    return pb
