"""Structure des chapitres 3 à 20, sans dépendance au moteur de mise en page."""
from dataclasses import dataclass, field
from contenu import Exo, PLAN, SOURCES

TITRES={n:title for n,(title,_) in enumerate([c for _,_,chapters in PLAN for c in chapters],1)}
THEMES={n:theme for start,end,theme in [(1,8,PLAN[0][1]),(9,11,PLAN[1][1]),(12,16,PLAN[2][1]),(17,20,PLAN[3][1])] for n in range(start,end+1)}

@dataclass
class Lecon:
    titre: str
    texte: str
    schema: tuple
    legende: str
    retenir: str
    methode: str

@dataclass
class Activite:
    titre: str
    mission: str
    etapes: list[str]
    schema: tuple
    legende: str
    questions: list[str]
    correction: str

@dataclass
class Defi:
    titre: str
    situation: str
    schema: tuple
    questions: list[str]
    aide: str
    correction: str

@dataclass
class Chapitre:
    n: int
    question: str
    objectifs: list[str]
    lecons: list[Lecon]
    activite: Activite
    bilan: list[str]
    erreur: str
    exercices: list[Exo]
    defi: Defi

def E(n,titre,questions,reponse,document='',figure=None,check=''):
    if isinstance(questions,str):questions=[questions]
    return Exo(n,titre,questions,reponse,document,figure,65 if figure else 0,check=check)

SOURCES_COMPLEMENTAIRES=[
('Explorer le Système solaire','CNES : organisation du Système solaire et diversité des huit planètes.','https://cnes.fr/dossiers/systeme-solaire'),
('Se repérer dans l’espace','CNES, glossaire spatial : unités et vocabulaire astronomiques.','https://cnes.fr/dossiers/glossaire-spatial'),
('Comprendre le risque électrique','INRS : risque de contact, court-circuit et prévention. Les montages du livre utilisent uniquement le matériel scolaire de très basse tension.','https://www.inrs.fr/risques/electriques/ce-qu-il-faut-retenir.html'),
('Préserver son audition','Assurance Maladie : effets des bruits intenses et des expositions prolongées.','https://www.ameli.fr/assure/sante/themes/bruit-sante/effets-du-bruit-sur-la-sante'),
('Identifier un gaz','Éduscol : exemple d’exploitation du test du dioxyde de carbone à l’eau de chaux.','https://eduscol.education.fr/document/29578/download'),
('Ressources renouvelables','Ministère de la Transition écologique : familles de ressources et conversions énergétiques.','https://www.ecologie.gouv.fr/politiques-publiques/energies-renouvelables'),
('Sons et effets du bruit','Ressource Éduscol sur le son, les milieux de propagation et la santé auditive.','https://eduscol.education.fr/document/30202/download')]
