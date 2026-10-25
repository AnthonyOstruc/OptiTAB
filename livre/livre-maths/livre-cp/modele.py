"""Données éditoriales originales du livre OptiTAB CP."""
from dataclasses import dataclass, field

@dataclass
class Exercice:
    consigne: str
    reponse: str
    figure: tuple | None = None
    check: str = ''

@dataclass
class Chapitre:
    titre: str
    domaine: str
    periode: str
    objectif: str
    materiel: str
    manipulation: str
    lecon: list[str]
    exemple: str
    figure: tuple
    guide: str
    guide_reponse: str
    exercices: list[Exercice]
    aide: str
    vigilance: str
    numero: int = 0

CHAPITRES=[]
def E(consigne,reponse,figure=None,check=''):
    return Exercice(consigne,reponse,figure,check)
def C(titre,domaine,periode,objectif,materiel,manipulation,lecon,exemple,figure,guide,guide_reponse,exercices,aide,vigilance):
    assert len(exercices)==9, (titre,len(exercices))
    c=Chapitre(titre,domaine,periode,objectif,materiel,manipulation,lecon,exemple,figure,guide,guide_reponse,exercices,aide,vigilance,len(CHAPITRES)+1)
    CHAPITRES.append(c)

SOURCES=[
('Programme de mathématiques du cycle 2', 'BO du 31 octobre 2024, applicable depuis septembre 2025. Rubriques CP : nombres et calculs, mesures, géométrie, données.', 'https://www.education.gouv.fr/sites/default/files/ensel135_annexe4.pdf'),
('Livret d’accompagnement - Mathématiques CP', 'Éduscol, 2025. Séquences de numération, calcul mental et problèmes parties-tout.', 'https://eduscol.education.fr/document/65383/download'),
('Repères CP - Cahier de l’élève 2026', 'DEPP. Consultation des tâches de reconnaissance, dénombrement, comparaison, ligne numérique et problèmes.', 'https://eduscol.education.gouv.fr/sites/default/files/document/26cpe-128779.pdf'),
('Repères CP - Guide pour le professeur 2026', 'DEPP. Consignes et compétences associées aux tâches de début de CP.', 'https://eduscol.education.gouv.fr/sites/default/files/document/26cpp-128800.pdf'),
('Point d’étape CP', 'Éduscol, page actualisée en juillet 2026. Ressources pour accompagner les apprentissages en milieu d’année.', 'https://eduscol.education.gouv.fr/5268/evaluer-en-milieu-d-annee-au-cp-un-point-d-etape-vers-la-reussite'),
('Calculer en ligne avec des nombres entiers', 'Éduscol. Fiche d’accompagnement : représentations, procédures et difficultés.', 'https://eduscol.education.gouv.fr/sites/default/files/document/ev23-mi-cp-maths-nombres-calculs-calculer-lignepdf-97755.pdf'),
('Résoudre des problèmes avec des nombres entiers', 'Éduscol. Fiche d’accompagnement des structures additives.', 'https://eduscol.education.gouv.fr/sites/default/files/document/ev23-mi-cp-maths-nombres-calculs-problemespdf-97761.pdf'),
]
