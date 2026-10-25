"""Modèle des données du livre de Quatrième, édition 2027-2028 (programme 2026)."""
from dataclasses import dataclass, field

def Q(*items):
    return '\\begin{questions}\n'+'\n'.join('\\item '+x for x in items)+'\n\\end{questions}'

@dataclass
class Exercice:
    titre: str
    enonce: str
    corrige: str
    methode: str
    controle: str
    figure: str = ''
    conseil: str = ''
    difficulte: int = 0

def E(titre, enonce, corrige, methode, controle, figure='', conseil=''):
    return Exercice(titre,enonce,corrige,methode,controle,figure,conseil)

@dataclass
class Chapitre:
    numero: int
    slug: str
    titre: str
    partie: str
    sous_titre: str
    objectifs: list
    prerequis: list
    cours: list
    exercices: list
    reperes: list = field(default_factory=list)
    deco: str = 'courbe'

CHAPITRES=[]
FIGURES={}

def chapitre(*args,**kwargs):
    c=Chapitre(*args,**kwargs)
    assert len(c.exercices)==15, (c.numero,len(c.exercices))
    assert len(c.cours)==2 and len(c.reperes)==4
    for i,e in enumerate(c.exercices,1): e.difficulte=1 if i<=5 else 2 if i<=10 else 3
    CHAPITRES.append(c)
    return c

def figure(nom,tex,legende):
    assert nom not in FIGURES,nom
    FIGURES[nom]={'tex':tex,'legende':legende}
    return nom

def tableau(entetes,lignes):
    return (r'\begin{center}\renewcommand{\arraystretch}{1.35}\begin{tabular}{c|'+
            'c'*(len(entetes)-1)+r'}\toprule'+'\n'+' & '.join(entetes)+r'\\\midrule'+'\n'+
            '\n'.join(' & '.join(row)+r'\\' for row in lignes)+
            '\n'+r'\bottomrule\end{tabular}\end{center}')
