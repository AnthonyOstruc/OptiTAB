"""Correspondance explicite entre les chapitres et les situations du site."""
from config import GRADE
import nombres as N
import mesures_geometrie as G
import donnees_problemes as D

def choisir(ch,i,l):
    if GRADE.startswith('cm'):
        slug=ch.slug
        mapping={
            'grands-nombres':N.numeration,'operations-entiers':lambda i,l:N.addition(i,l) if i%2==0 else N.multiplication(i,l),
            'addition-soustraction':lambda i,l:N.addition(i,l,subtract=i%2==1),
            'multiplication':N.multiplication,'multiples-diviseurs':N.multiples,
            'division':lambda i,l:N.division_decimale(i,l) if GRADE=='cm2' and i>=4 else N.division(i,l),
            'regularites':N.regularites,
            'fractions':lambda i,l:N.fraction_nombre(i,l) if i>=4 else N.fractions(i,l),
            'decouvrir-fractions':lambda i,l:N.fraction_nombre(i,l) if i>=4 else N.fractions(i,l),
            'utiliser-fractions':lambda i,l:N.fractions(i,l,'compare') if i<4 else N.fraction_nombre(i,l),
            'comparer-fractions':lambda i,l:N.fractions(i,l,'compare' if i<4 else 'read'),
            'fraction-quantite':N.fraction_quantite,
            'decimaux':N.decimaux,'fractions-decimales':N.decimaux,'comparer-decimaux':N.comparer_decimaux,
            'calculs-decimaux':N.calculs_decimaux,'calculer-decimaux':N.calculs_decimaux,
            'mesures':lambda i,l:G.mesures(i,l,['length','mass','capacity'][i%3]),
            'longueurs':lambda i,l:G.mesures(i,l) if i<4 else G.perimetre(i,l),
            'masses-contenances':lambda i,l:G.mesures(i,l,'mass' if i%2==0 else 'capacity'),
            'aires':lambda i,l:G.perimetre(i,l,True),'aires-angles':G.aires_angles,
            'angles':G.angles,'durees':G.durees,
            'constructions':G.construction,'droites-cercles':G.construction,
            'polygones':G.polygones,'triangles-quadrilateres':G.polygones,
            'symetrie':G.symetrie,'solides':G.solides,
            'proportionnalite':D.proportionnalite,'donnees':D.donnees,
            'probabilites':D.hasard,'hasard':D.hasard}
        return mapping[slug](i,l)
    if GRADE=='ce2':
        mapping={1:N.numeration,2:N.numeration,3:N.comparer_nombres,
            4:N.addition,5:lambda i,l:N.addition(i,l,True),6:lambda i,l:N.addition(i,l,subtract=l==2,compensation=True),
            7:lambda i,l:N.multiplication(i,l,'tables'),8:N.doubles,
            9:lambda i,l:N.multiplication(i,l,'ten'),10:lambda i,l:N.multiplication(i,l,'decompose'),
            11:lambda i,l:N.multiplication(i,l,'double'),12:N.multiplication,13:lambda i,l:N.multiplication(i,l,'two'),
            14:N.division,15:D.parties_tout,16:D.parties_tout,17:D.parties_tout,18:D.parties_tout,19:D.choix,
            20:N.fractions_egales,21:lambda i,l:N.fractions(i,l,'compare'),22:D.fraction_unite,23:N.fractions,
            24:G.mesures,25:G.perimetre,26:lambda i,l:G.mesures(i,l,'mass'),27:lambda i,l:G.mesures(i,l,'capacity'),
            28:D.monnaie,29:D.monnaie,30:lambda i,l:G.durees(i,l,True),31:G.durees,
            32:G.polygones,33:G.construction,34:G.solides,35:G.symetrie,36:D.donnees}
    else:
        mapping={1:N.numeration,2:N.numeration,3:N.comparer_nombres,4:D.rangs,
            5:N.addition,6:N.addition,7:lambda i,l:N.addition(i,l,True,True),8:lambda i,l:N.addition(i,l,True),
            9:lambda i,l:N.multiplication(i,l,'tables'),10:lambda i,l:N.multiplication(i,l,'tables'),11:lambda i,l:N.multiplication(i,l,'tables'),
            12:lambda i,l:N.multiplication(i,l,'ten' if i<3 else 'decompose'),13:N.doubles,
            14:D.parties_tout,15:D.parties_tout,16:D.parties_tout,17:N.division,
            18:N.fractions,19:lambda i,l:N.fractions(i,l,'compare'),20:N.fractions,
            21:G.mesures,22:lambda i,l:G.mesures(i,l,'mass'),23:D.monnaie,
            24:lambda i,l:G.durees(i,l,True),25:G.durees,26:G.polygones,27:G.construction,28:G.construction,
            29:G.solides,30:G.plan,31:D.donnees,32:D.donnees}
    return mapping[ch.numero](i,l)

def theme(ch):
    if GRADE.startswith('cm'):
        return 'nombres' if ch.numero<=10 else 'mesures' if ch.numero<=14 else 'geometrie' if ch.numero<=18 else 'donnees'
    d=ch.domaine.lower()
    return 'geometrie' if 'géométrie' in d else 'donnees' if 'données' in d else 'mesures' if any(x in d for x in ['mesur','monnaie','temps','durée']) else 'nombres'
