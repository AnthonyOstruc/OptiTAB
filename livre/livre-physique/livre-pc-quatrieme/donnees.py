"""Données pédagogiques originales du manuel, indépendantes de la mise en page."""
from dataclasses import dataclass, field

THEMES = [
    (1, 8, 'Organisation et transformations de la matière'),
    (9, 11, 'Mouvements et interactions'),
    (12, 17, 'L’énergie, ses transferts et ses conversions'),
    (18, 20, 'Des signaux pour observer et communiquer'),
]

@dataclass
class Exercice:
    titre: str
    questions: list
    reponses: list
    document: str = ''
    figure: str = ''
    calculs: list = field(default_factory=list)
    figure_correction: str = ''
    legende_figure: str = ''
    legende_correction: str = ''
    figure_exacte: bool = False
    correction_exacte: bool = False
    methode: str = ''

def E(titre, questions, reponses, document='', figure='', calculs=None):
    q, a = questions.split('@@'), reponses.split('@@')
    assert len(q) == len(a), (titre, len(q), len(a))
    return Exercice(titre, q, a, document, figure, calculs or [])

@dataclass
class Chapitre:
    numero: int
    titre: str
    question: str
    objectifs: list
    prerequis: list
    lecons: list
    exemple: str
    activite: str
    bilan: list
    erreur: str
    exercices: list
    defi: Exercice
    theme: int = 0

def C(n, titre, question, objectifs, prerequis, lecons, exemple, activite, bilan, erreur, exercices, defi):
    assert len(lecons) == 4 and len(exercices) == 15
    theme = next(i for i, (a,b,_) in enumerate(THEMES,1) if a <= n <= b)
    return Chapitre(n,titre,question,objectifs,prerequis,lecons,exemple,activite,bilan,erreur,exercices,defi,theme)

SOURCES = [
 ('Programme en vigueur et ressources', 'Éduscol, cycle 4, page consultée le 24 octobre 2026. BO du 30 juillet 2020.', 'https://eduscol.education.gouv.fr/5739/ressources-d-accompagnement-du-programme-de-physique-chimie-au-cycle-4'),
 ('Programmes appliqués en 2026-2027', 'Éduscol, tableau des programmes du cycle 4.', 'https://eduscol.education.gouv.fr/4362/enseigner-au-cycle-4'),
 ('Texte du programme', 'Programme du cycle 4, version 2020, physique-chimie : pages 96 à 106.', 'https://eduscol.education.fr/document/621/download'),
 ('Construire une progression', 'Éduscol, ressource d’accompagnement : aide à la construction d’une progression en physique-chimie au cycle 4.', 'https://eduscol.education.gouv.fr/sites/default/files/document/ra16c4phchaideconstructionprogression594860pdf-78099.pdf'),
]

def charger():
    from matiere import CHAPITRES as m
    from mouvement import CHAPITRES as v
    from energie import CHAPITRES as e
    from signaux import CHAPITRES as s
    ch = m+v+e+s
    assert [c.numero for c in ch] == list(range(1,21))
    from revision_exercices import enrichir
    enrichir(ch)
    return ch
