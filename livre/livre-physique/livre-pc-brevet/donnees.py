"""Cours et entraînements de Troisième et révisions du cycle 4."""
from dataclasses import dataclass,field
from pathlib import Path
import json
THEMES=[(1,7,'Organisation et transformations de la matière'),(8,10,'Mouvements et interactions'),(11,15,'L’énergie, ses transferts et ses conversions'),(16,18,'Des signaux pour observer et communiquer')]
@dataclass
class Exercice:
    titre:str
    questions:list
    reponses:list
    document:str=''
    figure:str=''
    calculs:list=field(default_factory=list)
    figure_correction:str=''
    legende_figure:str=''
    legende_correction:str=''
    figure_exacte:bool=False
    correction_exacte:bool=False
    methode:str=''
def E(titre,questions,reponses,document='',figure='',calculs=None):
    q,a=questions.split('@@'),reponses.split('@@')
    assert len(q)==len(a),(titre,len(q),len(a))
    return Exercice(titre,q,a,document,figure,calculs or [])
@dataclass
class Chapitre:
    numero:int
    titre:str
    question:str
    objectifs:list
    prerequis:list
    lecons:list
    exemple:str
    activite:str
    bilan:list
    erreur:str
    exercices:list
    defi:Exercice
    theme:int=0
def C(n,titre,question,objectifs,prerequis,lecons,exemple,activite,bilan,erreur,exercices,defi):
    assert len(lecons)==4 and len(exercices)==15,(n,len(lecons),len(exercices))
    theme=next(i for i,(a,b,_) in enumerate(THEMES,1) if a<=n<=b)
    return Chapitre(n,titre,question,objectifs,prerequis,lecons,exemple,activite,bilan,erreur,exercices,defi,theme)
SOURCES=[
('Programme en application','Éduscol, programmes du cycle 4 pour 2026-2027 ; physique-chimie : BO du 30 juillet 2020.','https://eduscol.education.gouv.fr/4362/enseigner-au-cycle-4'),
('Texte de référence','Programme de physique-chimie du cycle 4, pages 96 à 106 ; découpage annuel éditorial.','https://eduscol.education.fr/document/621/download'),
('Épreuves du DNB 2027','Note de service du 11 septembre 2026, NOR MENE2623228N, partie I.4 : sciences.','https://www.education.gouv.fr/bo/2026/Hebdo4/MENE2623228N'),
('Présentation des épreuves','Éduscol : durée, notation et compétences ; page actualisée en octobre 2026.','https://eduscol.education.gouv.fr/5607/les-epreuves-du-dnb'),
('Sujet de référence','Éduscol, physique-chimie, série générale, n° 01 : repérage des attendus et de la rédaction.','https://eduscol.education.gouv.fr/sites/default/files/document/dnb-sujet-de-reference-physique-chimie-serie-generale-n01-129673.pdf'),
('Annale officielle 2026','Ministère, sciences, série générale : lecture critique du format et des démarches attendues. Les énoncés ne sont pas reproduits.','https://www.education.gouv.fr/sites/default/files/document/diplome-national-du-brevet-2026-sciences-serie-generale-517070.pdf'),
('Atome et noyau','CEA : protons, neutrons, électrons et numéro atomique.','https://www.cea.fr/comprendre/enseignants/pages/ressources-pedagogiques/essentiel-sur/physique-chimie/essentiel-sur-noyaux-des-atomes.aspx'),
('Unités','BIPM, Brochure sur le SI : unités, symboles et préfixes.','https://www.bipm.org/fr/publications/si-brochure'),
('Chronologie cosmique','NASA Science : âges approximatifs de l’Univers et du Système solaire.','https://science.nasa.gov/exoplanets/what-is-the-universe/'),
]
def charger():
    from chimie import CHAPITRES as m
    from physique import CHAPITRES as p
    ds=json.loads((Path(__file__).parent/'revisions.json').read_text(encoding='utf8'))
    revisions=[]
    for d in ds:
        d['exercices']=[Exercice(**e) for e in d['exercices']];d['defi']=Exercice(**d['defi'])
        revisions.append(Chapitre(**d))
    chs=sorted(m+p+revisions,key=lambda c:c.numero)
    assert [c.numero for c in chs]==list(range(1,19))
    from revision_exercices import enrichir
    enrichir(chs)
    return chs
