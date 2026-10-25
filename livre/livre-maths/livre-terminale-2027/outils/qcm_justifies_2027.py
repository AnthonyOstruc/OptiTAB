"""Édition 2027-2028 : les questionnaires à choix multiples des sujets type bac demandent désormais une justification.

Note de service du 11 septembre 2026 (NOR MENE2623195N) : « faire davantage rédiger les candidats en limitant le recours
à des exercices de type QCM ou à des consignes de type réponse courte ». Exécuté une seule fois ; chaque remplacement est
vérifié (une occurrence exactement). Usage : python -I -X utf8 outils/qcm_justifies_2027.py
"""
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CONSIGNE = ("Pour chacune des questions suivantes, une seule des quatre réponses proposées est exacte. Indiquer sur la copie le "
            "numéro de la\nquestion et la lettre de la réponse choisie, puis \\textbf{justifier ce choix} par un calcul ou un "
            "raisonnement rédigé. Une réponse\nnon justifiée ne rapporte aucun point.")

REMPLACEMENTS = {
    "bac/sujet-02.tex": [
        ("{QCM : analyse et probabilités/4,", "{QCM justifié : analyse et probabilités/4,"),
        ("\\begin{exoBac}{4}{Questionnaire à choix multiples}", "\\begin{exoBac}{4}{Questionnaire à choix multiples justifié}"),
        ("Pour chacune des questions suivantes, une seule des quatre réponses proposées est exacte. Indiquer sur la copie le numéro de la\n"
         "question et la lettre de la réponse choisie. Aucune justification n'est demandée. Une réponse fausse, une réponse multiple ou\n"
         "l'absence de réponse ne rapporte ni n'enlève aucun point.", CONSIGNE),
    ],
    "bac/sujet-05.tex": [
        (",QCM : géométrie dans l'espace/4,", ",QCM justifié : géométrie dans l'espace/4,"),
        ("\\begin{exoBac}{4}{Questionnaire à choix multiples}", "\\begin{exoBac}{4}{Questionnaire à choix multiples justifié}"),
        ("L'espace est muni d'un repère orthonormé. Pour chaque question, une seule des quatre réponses proposées est exacte. Aucune\n"
         "justification n'est demandée. Une réponse fausse, une réponse multiple ou l'absence de réponse ne rapporte ni n'enlève aucun point.",
         "L'espace est muni d'un repère orthonormé. Pour chaque question, une seule des quatre réponses proposées est exacte. Indiquer la\n"
         "réponse choisie, puis \\textbf{justifier ce choix} par un calcul ou un raisonnement rédigé. Une réponse non justifiée ne rapporte\n"
         "aucun point."),
    ],
    "bac/sujet-08.tex": [
        ("{QCM : probabilités et dénombrement/4,", "{QCM justifié : probabilités et dénombrement/4,"),
        ("\\begin{exoBac}{4}{Questionnaire à choix multiples}", "\\begin{exoBac}{4}{Questionnaire à choix multiples justifié}"),
        ("Pour chaque question, une seule des quatre réponses proposées est exacte. Aucune justification n'est demandée. Une réponse fausse, une\n"
         "réponse multiple ou l'absence de réponse ne rapporte ni n'enlève aucun point.",
         "Pour chaque question, une seule des quatre réponses proposées est exacte. Indiquer la réponse choisie, puis \\textbf{justifier ce\n"
         "choix} par un calcul ou un raisonnement rédigé. Une réponse non justifiée ne rapporte aucun point."),
    ],
    "bac/corrige-02.tex": [("{Questionnaire à choix multiples}", "{Questionnaire à choix multiples justifié}")],
    "bac/corrige-05.tex": [("{Questionnaire à choix multiples}", "{Questionnaire à choix multiples justifié}")],
    "bac/corrige-08.tex": [("{Questionnaire à choix multiples}", "{Questionnaire à choix multiples justifié}")],
}

for rel, paires in REMPLACEMENTS.items():
    p = RACINE / rel
    t = p.read_text(encoding="utf-8")
    for avant, apres in paires:
        assert t.count(avant) == 1, (rel, avant[:60], t.count(avant))
        t = t.replace(avant, apres)
    p.write_text(t, encoding="utf-8", newline="")
print("QCM justifiés : sujets 2, 5 et 8 mis à jour.")
