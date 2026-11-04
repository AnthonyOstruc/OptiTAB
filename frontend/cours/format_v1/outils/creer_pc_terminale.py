# -*- coding: utf-8 -*-
"""Crée le squelette (INVISIBLE) de la Physique-Chimie de Terminale sur le site.

Depuis backend/ :
  manage.py shell -c "import sys; sys.argv=['x']; exec(open(r'<chemin>', encoding='utf-8').read())"
  (ajouter '--appliquer' pour écrire)

Matière « Physique-Chimie » + contexte Terminale + 5 thèmes (parties du programme
officiel de spécialité) + 27 notions (chapitres du livre OptiTAB livre-pc-terminale),
chacune avec un cours et une fiche vides au format v1. TOUT est créé INACTIF
(matière, contexte, thèmes, notions) : rien n'apparaît aux élèves tant que le
propriétaire n'a pas validé. Les exercices viennent ensuite par importer_v1.py
(blocs « Id: nouveau-N »). Relançable sans doublon (get_or_create).
"""
import sys

from django.db import transaction

from cours.models import Cours
from curriculum.models import Matiere, MatiereContexte, Notion, Theme
from synthesis.models import SynthesisSheet

NIVEAU_TLE = 20
CTX_MATHS_TLE = 25
VIDE = "<!-- optitab:1 -->\n\nEn préparation."

PROGRAMME = [
    ("Constitution et transformations de la matière", [
        "Transformations acide-base",
        "Méthodes physiques d'analyse",
        "Titrages pH-métriques et conductimétriques",
        "Cinétique chimique",
        "Mécanismes réactionnels",
        "Décroissance radioactive",
        "Équilibre chimique et sens d'évolution",
        "Piles et oxydoréduction",
        "Force des acides et des bases",
        "Électrolyse et stockage de l'énergie",
        "Structure des molécules organiques",
        "Stratégies de synthèse organique",
    ]),
    ("Mouvement et interactions", [
        "Décrire un mouvement",
        "Deuxième loi de Newton",
        "Mouvement dans un champ uniforme",
        "Mouvement dans un champ de gravitation",
        "Écoulement des fluides",
    ]),
    ("L'énergie : conversions et transferts", [
        "Modèle du gaz parfait",
        "Premier principe de la thermodynamique",
        "Transferts thermiques et bilans",
    ]),
    ("Ondes et signaux", [
        "Intensité sonore et atténuation",
        "Diffraction et interférences",
        "Effet Doppler",
        "Lunette astronomique",
        "Photons et effet photoélectrique",
        "Circuit RC et capteurs capacitifs",
    ]),
    ("Mesure et incertitudes", [
        "Mesures et incertitudes",
    ]),
]

ref = Cours.objects.filter(notion__theme__contexte_id=CTX_MATHS_TLE).first()
print(f"{sum(len(c) for _, c in PROGRAMME)} chapitres en {len(PROGRAMME)} thèmes ; "
      f"accès des cours de maths Tle : {ref.access_scope}")
existe = Matiere.objects.filter(titre="Physique-Chimie").first()
print("Matière « Physique-Chimie » déjà présente :", existe.id if existe else "non")

if "--appliquer" not in sys.argv:
    print("Simulation : rien n'a été écrit.")
else:
    with transaction.atomic():
        matiere, _ = Matiere.objects.get_or_create(
            titre="Physique-Chimie",
            defaults=dict(ordre=4, couleur="#E8912D", description="", est_actif=False, show_on_home=False))
        ctx, _ = MatiereContexte.objects.get_or_create(
            matiere=matiere, niveau_id=NIVEAU_TLE,
            defaults=dict(titre="Physique-Chimie Terminale", ordre=2, est_actif=False))
        n_notions = 0
        for i, (titre_theme, chapitres) in enumerate(PROGRAMME, 1):
            theme, _ = Theme.objects.get_or_create(
                contexte=ctx, titre=titre_theme,
                defaults=dict(matiere=matiere, ordre=i, description="", est_actif=False))
            for j, titre in enumerate(chapitres, 1):
                notion, _ = Notion.objects.get_or_create(
                    theme=theme, titre=titre, defaults=dict(ordre=j, description="", est_actif=False))
                Cours.objects.get_or_create(
                    notion=notion,
                    defaults=dict(titre=titre, contenu=VIDE, difficulty="medium", ordre=ref.ordre,
                                  access_scope="paid"))
                SynthesisSheet.objects.get_or_create(
                    notion=notion, sheet_type="summary",
                    defaults=dict(titre=titre, summary=VIDE, difficulty="medium",
                                  reading_time_minutes=10, access_scope="paid"))
                n_notions += 1
    print(f"Créé (INACTIF) : matière {matiere.id}, contexte {ctx.id}, {len(PROGRAMME)} thèmes, {n_notions} notions")
    for t in Theme.objects.filter(contexte=ctx).order_by("ordre"):
        print(f"  thème {t.id} {t.titre}")
        for n in t.notions.order_by("ordre"):
            print(f"    notion {n.id} {n.titre}")
