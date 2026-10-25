"""Petites fonctions de composition ; les contenus restent propres à chaque chapitre."""
from modele import E
def page(n,titre,*blocs):
    return r'\essSection{'+str(n)+'}{'+titre+'}\n'+'\n'.join(blocs)
def sec(n,titre):
    return r'\essSection{'+str(n)+'}{'+titre+'}'
def bloc(kind,texte,titre=''):
    return r'\begin{'+kind+'}'+('['+titre+']' if titre else '')+texte+r'\end{'+kind+'}'
def direct(titre,question,etapes,methode,test,fig=''):
    return E(titre,question,etapes,methode,test,figure=fig)
