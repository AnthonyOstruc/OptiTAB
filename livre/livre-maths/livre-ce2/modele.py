"""Contenus originaux OptiTAB CE2, neuf exercices progressifs par chapitre."""
from dataclasses import dataclass

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

CHAPITRES = []
def E(consigne, reponse, figure=None, check=''):
    return Exercice(consigne, reponse, figure, check)
def C(titre,domaine,periode,objectif,materiel,manipulation,lecon,exemple,figure,guide,guide_reponse,exercices,aide,vigilance):
    assert len(exercices)==9, (titre,len(exercices))
    assert len(lecon)==3, titre
    CHAPITRES.append(Chapitre(titre,domaine,periode,objectif,materiel,manipulation,lecon,exemple,figure,guide,guide_reponse,exercices,aide,vigilance,len(CHAPITRES)+1))

SOURCES=[
('Programme de mathématiques du cycle 2','BO du 31 octobre 2024, applicable depuis septembre 2025. Rubriques CE2 : progression, contenus et repères de réussite.','https://www.education.gouv.fr/sites/default/files/ensel135_annexe4.pdf'),
('Livret d’accompagnement - Mathématiques CE2','Éduscol, 2025. Consulté pour la mesure en fractions d’unité, le calcul par doubles successifs et les problèmes de comparaison en deux étapes.','https://eduscol.education.gouv.fr/sites/default/files/document/2025livretaccompagnementmathce2pdf-122974.pdf'),
('Ressources d’accompagnement du cycle 2','Éduscol, page actualisée en février 2026 : programme en vigueur, livrets et annexes.','https://eduscol.education.gouv.fr/4746/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-2'),
('Repères CE2 - Cahier de l’élève 2026','DEPP. Familles de tâches de rentrée : numération, graduation, opérations, fractions et problèmes. Ces évaluations portent sur les acquis antérieurs.','https://eduscol.education.gouv.fr/sites/default/files/document/26ce2e-128860.pdf'),
('Repères CE2 - Guide pour le professeur 2026','DEPP. Consignes, compétences évaluées et modalités de passation ; ressource pour observer les besoins à l’entrée en CE2.','https://eduscol.education.gouv.fr/sites/default/files/document/26ce2p-128881.pdf'),
('Évaluations des acquis et besoins au CE2','Éduscol, septembre 2026 : objectifs, supports et ressources d’accompagnement des évaluations de début d’année.','https://eduscol.education.gouv.fr/5283/evaluations-des-acquis-et-besoins-des-eleves-au-ce2'),
]
