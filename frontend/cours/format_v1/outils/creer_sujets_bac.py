# -*- coding: utf-8 -*-
"""Crée le squelette (INACTIF) du thème « Préparation au bac » de Terminale.

Depuis backend/ :
  manage.py shell -c "import sys; sys.argv=['x']; exec(open(r'<chemin>', encoding='utf-8').read())"
  (ajouter '--appliquer' pour écrire)

Thème + notion « Sujets type bac » (est_actif=False tant que le contenu n'est
pas importé), un cours de méthode et une fiche vides au format v1. Les sujets
sont ensuite ajoutés par importer_v1.py (blocs « Id: nouveau-N »).
"""
import sys

from django.db import transaction
from django.db.models import Max

from cours.models import Cours
from curriculum.models import Matiere, Notion, Theme
from synthesis.models import SynthesisSheet

CTX_TLE = 25
VIDE = "<!-- optitab:1 -->\n\nEn préparation."

themes = Theme.objects.filter(contexte_id=CTX_TLE)
print([(t.id, t.ordre, t.titre) for t in themes.order_by("ordre")])
ref = Cours.objects.filter(notion__theme__contexte_id=CTX_TLE).first()
print("accès cours de référence :", ref.access_scope, "| ordre max :", Cours.objects.aggregate(Max("ordre")))
if "--appliquer" not in sys.argv:
    print("Simulation : rien n'a été écrit.")
else:
    with transaction.atomic():
        theme, _ = Theme.objects.get_or_create(
            contexte_id=CTX_TLE, titre="Préparation au bac",
            defaults=dict(matiere=themes.first().matiere, ordre=themes.aggregate(Max("ordre"))["ordre__max"] + 1,
                          description=""))
        notion, _ = Notion.objects.get_or_create(
            theme=theme, titre="Sujets type bac",
            defaults=dict(ordre=1, description="", est_actif=False))
        Cours.objects.get_or_create(
            notion=notion,
            defaults=dict(titre="Méthode : réussir l'épreuve de mathématiques du bac", contenu=VIDE,
                          difficulty="medium", ordre=ref.ordre, access_scope="paid"))
        SynthesisSheet.objects.get_or_create(
            notion=notion, sheet_type="summary",
            defaults=dict(titre="Résumé : l'essentiel pour le bac", summary=VIDE,
                          difficulty="medium", reading_time_minutes=10, access_scope="paid"))
    print(f"Créé : thème {theme.id}, notion {notion.id} (inactive)")
