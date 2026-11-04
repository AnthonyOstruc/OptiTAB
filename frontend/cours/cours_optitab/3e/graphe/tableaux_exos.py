# -*- coding: utf-8 -*-
"""Tableaux bordés des énoncés et corrigés d'exercices de 3ème (style des cours OptiTAB)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import tableau, DIR_EXOS
import figures_ch17 as f17

M = "−"  # signe moins typographique


def out(nom):
    return os.path.join(DIR_EXOS, nom)


if __name__ == "__main__":
    tableau(out("fonctions_3e_tableau.png"),
            [["$x$", f"{M}2", "0", "1", "3"], ["$f(x)$", "5", "1", f"{M}1", "1"]], w0=1.2)
    tableau(out("affines_3e_tableau.png"), [["$x$", "0", "2", "5"], ["$y$", "3", "11", "23"]],
            w0=1.0)
    tableau(out("proportionnalite_3e_tableau.png"),
            [["Quantité (kg)", "2", "5", "8"], ["Prix (€)", "7", "17,5", "28"]])
    tableau(out("statistiques_3e_notes.png"),
            [["Note", "6", "8", "10", "12", "16"], ["Effectif", "2", "3", "6", "5", "4"]])
    tableau(out("statistiques_3e_notes_cumules.png"),
            [["Note", "6", "8", "10", "12", "16"], ["Effectif", "2", "3", "6", "5", "4"],
             ["Effectif cumulé", "2", "5", "11", "16", "20"]],
            vert={(2, c) for c in range(1, 6)})
    tableau(out("statistiques_3e_pluie.png"),
            [["Mois", "Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
             ["Pluie (mm)", "62", "55", "48", "51", "66", "38"],
             ["Mois", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"],
             ["Pluie (mm)", "22", "30", "54", "70", "78", "72"]], tete_rows=(0, 2))
    tableau(out("statistiques_3e_ecran.png"),
            [["Temps d'écran", "moins de 1 h", "1 h à 2 h", "2 h à 3 h", "3 h ou plus"],
             ["Effectif", "30", "70", "60", "?"]])
    tableau(out("statistiques_3e_ecran_sol.png"),
            [["Temps d'écran", "moins de 1 h", "1 h à 2 h", "2 h à 3 h", "3 h ou plus", "Total"],
             ["Effectif", "30", "70", "60", "40", "200"],
             ["Fréquence (%)", "15", "35", "30", "20", "100"],
             ["Angle (°)", "54", "126", "108", "72", "360"]],
            vert={(r, c) for r in (2, 3) for c in range(1, 6)} | {(1, 4)})
    f17.tableur(out("statistiques_3e_tableur.png"), 2, 4,
                {"A1": "Valeur", "B1": "Effectif", "A2": 4, "B2": 3, "A3": 7, "B3": 5,
                 "A4": 12, "B4": 2}, widths=[1.2, 1.2])
    print("Tableaux des exercices : OK")
