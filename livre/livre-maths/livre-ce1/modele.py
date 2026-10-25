"""Contenus originaux OptiTAB CE1 ; chaque chapitre contient neuf exercices."""
from dataclasses import dataclass
@dataclass
class Exercice:
    consigne:str
    reponse:str
    figure:tuple|None=None
    check:str=''
@dataclass
class Chapitre:
    titre:str
    domaine:str
    periode:str
    objectif:str
    materiel:str
    manipulation:str
    lecon:list[str]
    exemple:str
    figure:tuple
    guide:str
    guide_reponse:str
    exercices:list[Exercice]
    aide:str
    vigilance:str
    numero:int=0
CHAPITRES=[]
def E(consigne,reponse,figure=None,check=''):return Exercice(consigne,reponse,figure,check)
def C(titre,domaine,periode,objectif,materiel,manipulation,lecon,exemple,figure,guide,guide_reponse,exercices,aide,vigilance):
    assert len(exercices)==9,(titre,len(exercices))
    CHAPITRES.append(Chapitre(titre,domaine,periode,objectif,materiel,manipulation,lecon,exemple,figure,guide,guide_reponse,exercices,aide,vigilance,len(CHAPITRES)+1))
SOURCES=[
('Programme de mathématiques du cycle 2','BO du 31 octobre 2024, applicable depuis la rentrée 2025. Les rubriques CE1 ont été consultées.','https://www.education.gouv.fr/sites/default/files/ensel135_annexe4.pdf'),
('Livret d’accompagnement - Mathématiques CE1','Éduscol, 2025 : fractions, procédures mentales, table de 7, problèmes parties-tout.','https://eduscol.education.fr/document/67770/download'),
('Ressources d’accompagnement du cycle 2','Éduscol : programme en vigueur et livrets pédagogiques associés.','https://eduscol.education.gouv.fr/4746/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-2'),
('Repères CE1 - Cahier de l’élève 2026','DEPP. Consultation des familles de tâches de début d’année : numération, calculs, problèmes, graduation.','https://eduscol.education.gouv.fr/sites/default/files/document/26ce1e-128827.pdf'),
('Repères CE1 - Guide pour le professeur 2026','DEPP. Compétences et consignes associées aux tâches de début de CE1.','https://eduscol.education.gouv.fr/sites/default/files/document/26ce1p-128848.pdf'),
('Évaluations des acquis et besoins au CE1','Éduscol, septembre 2026 : objectifs des évaluations et ressources disponibles.','https://eduscol.education.gouv.fr/5289/evaluations-des-acquis-et-besoins-des-eleves-au-ce1'),
]
