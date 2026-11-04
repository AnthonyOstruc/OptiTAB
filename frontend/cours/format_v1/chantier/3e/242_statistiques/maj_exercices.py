# -*- coding: utf-8 -*-
"""Mise à jour structurée de exercices.txt (titres, figures, encadrés « À retenir »)."""
import re
from pathlib import Path

p = Path(__file__).with_name("exercices.txt")
t = p.read_text(encoding="utf-8")

# 1. Titres « Type - Sujet » (sans le nom du chapitre ni numéro)
t = re.sub(r"^=== (Découverte|Entraînement|Problème) - Statistiques - \d+\. ", r"=== \1 - ", t, flags=re.M)

# 2. « **À retenir :** … » -> encadré retenir
t = re.sub(r"^\*\*À retenir :\*\* (.+)$", lambda m: "::: retenir\n" + m.group(1) + "\n:::", t, flags=re.M)


def bloc(t, id_):
    i = t.index("Id: %s\n" % id_)
    d = t.rfind("=== ", 0, i)
    f = t.index("\n===\n", i)
    return d, f


def remplace_dans(t, id_, ancien, nouveau):
    d, f = bloc(t, id_)
    b = t[d:f]
    assert ancien in b, (id_, ancien)
    return t[:d] + b.replace(ancien, nouveau, 1) + t[f:]


# 2322 : corrigé avec le diagramme complété
t = remplace_dans(t, 2322, "## Question 4 : Au moins 12\n", "## Question 4 : Au moins 12\n\n[IMAGE_2]\n")

# 2324 : le diagramme circulaire passe dans le corrigé (il donnait la réponse dans l'énoncé)
t = remplace_dans(t, 2324, "3. Vérifier que leur somme vaut 360°.\n   [IMAGE_1]\n", "3. Vérifier que leur somme vaut 360°.\n")
t = remplace_dans(t, 2324, "::: resultat\n$$90 + 162 + 108 = 360$$\n:::\n",
                  "::: resultat\n$$90 + 162 + 108 = 360$$\n:::\n\n[IMAGE_1]\n")

# 2334 : tableau de données en texte, série rangée en figure dans le corrigé
TAB = ("| Mois | janv. | févr. | mars | avr. | mai | juin |\n|---|---|---|---|---|---|---|\n"
       "| Pluie (mm) | $62$ | $55$ | $48$ | $51$ | $66$ | $38$ |\n\n"
       "| Mois | juil. | août | sept. | oct. | nov. | déc. |\n|---|---|---|---|---|---|---|\n"
       "| Pluie (mm) | $22$ | $30$ | $54$ | $70$ | $78$ | $72$ |\n")
t = remplace_dans(t, 2334, "d'une ville sur une année.\n\n[IMAGE_1]\n", "d'une ville sur une année.\n\n" + TAB)
t = remplace_dans(t, 2334, "## Question 3 :", "[IMAGE_1]\n\n## Question 3 :") if False else t

p.write_text(t, encoding="utf-8")
print("ok")
