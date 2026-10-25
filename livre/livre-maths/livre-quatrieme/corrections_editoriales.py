"""Corrections ciblées de la première relecture, avant génération."""
from pathlib import Path
R=Path(__file__).resolve().parent
def change(name,old,new):
    p=R/name;s=p.read_text(encoding='utf8')
    assert old in s,(name,old)
    p.write_text(s.replace(old,new),encoding='utf8')
change('contenu_16_18.py','simplify(pi*(8/2)**2*9/3)==48*pi','simplify(pi*Rational(8,2)**2*Rational(9,3))==48*pi')
change('approfondissements.py','sqrt((180-116)/4)==4','sqrt(Rational(180-116,4))==4')
change('approfondissements.py',"'Son aire est la somme","r'Son aire est la somme")
change('approfondissements.py',"'Après la baisse, il reste","r'Après la baisse, il reste")
change('approfondissements.py',"'Le quotient se simplifie","r'Le quotient se simplifie")
change('contenu_07_09.py',r'On remplace $t$ dans la formule : $P(0)$ se lit ici « prix pour 0 heure » et vaut 5 ; les deux autres prix valent',r'On remplace $t$ dans la formule : pour 0 heure, le prix vaut 5 euros ; les deux autres prix valent')
change('contenu_07_09.py','180-12*10==60','160-10*10==60')
change('contenu_13_15.py','l’aire du quadrilatère MNPQ, délimité dans l’ordre M, N, Q, P','l’aire du quadrilatère MNQP, délimité dans l’ordre M, N, Q, P')
change('contenu_01_03.py',"and Rational(180,252)==Rational(5,7)\"),","and Rational(180,252)==Rational(5,7)\",figure='facteurs-180'),")
change('generer_figures.py',r'\coordinate(A)at(3,3);\coordinate(B)at(0,0);\coordinate(C)at(6,0);',r'\coordinate(A)at(3,4);\coordinate(B)at(0,0);\coordinate(C)at(6,0);')
change('generer_figures.py',"cone('sol-04','4 cm','9 cm')","cone('sol-04',reponse('4 cm'),'9 cm')")
