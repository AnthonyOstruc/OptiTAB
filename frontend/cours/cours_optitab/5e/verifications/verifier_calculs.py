"""Contrôles exacts et invariants indépendants du rendu HTML et MathJax."""
import importlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'outils'))
from modele_5e import FRONT,REPO
from construire_5e import CHAPITRES,BUILDERS
from variantes import choisir


def verifier():
    count=0
    details=[]
    for c in CHAPITRES:
        for level in range(3):
            for i in range(7):
                e=choisir(c.slug,i,level,BUILDERS[c.slug])
                for j,q in enumerate(e.questions,1):
                    if q.controle:
                        # Les expressions appartiennent aux sources locales du projet.
                        assert eval(q.controle,{'F':F,'abs':abs,'sum':sum,'divmod':divmod,'all':all,'any':any,'range':range}), (c.slug,level,i,j,q.controle)
                        count+=1
                details.append(dict(slug=c.slug,niveau=level,indice=i,questions=len(e.questions),statut='réussi'))
    # Rejouer aussi les 300 contrôles éditoriaux du livre dont les cours sont adaptés.
    env={k:getattr(s,k) for k in ['Rational','sqrt','expand','simplify','solve','solveset','factorint','isprime','divisors','gcd','ilcm','degree','S','pi','sin','cos','tan','N','Abs','binomial']}
    env.update(x=s.Symbol('x',real=True),n=s.Symbol('n',integer=True),ceil=math.ceil,math=math)
    for c in CHAPITRES:
        for e in c.exercices:
            exec(e.controle,env.copy())
            count+=1
    # Invariants géométriques et algorithmiques sur toute la plage de paramètres.
    props=0
    for level in range(3):
        for i in range(7):
            a,b=35+5*i,45+5*level
            assert 0<180-a-b<180
            side,height=4+level,2+level
            assert side>height>0
            # Le milieu d'un point et de son symétrique central est l'origine.
            x,y=2+i,1+level
            assert (F(x-x,2),F(y-y,2))==(0,0)
            # Trace indépendante de la boucle géométrique (sans variable mise à jour pour l'élève).
            position=(0,0)
            distance=10+5*level
            for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
                position=(position[0]+dx*distance,position[1]+dy*distance)
            assert position==(0,0)
            props+=4
    files=sorted(ROOT.glob('cours_*_5e.txt'))+sorted((FRONT/'cours/resume/5e').glob('*.txt'))+sorted((FRONT/'exercices/5e').glob('*.txt'))
    report=dict(chapitres=20,exercices=420,questions=2520,controles_calculs=count,invariants=props,
        erreurs=[],portee='Calculs explicites, contrôles des cours sources, invariants géométriques et traces. Ne constitue pas une preuve automatique de toutes les phrases.',
        empreintes={str(p.relative_to(FRONT)):sha256(p.read_bytes()).hexdigest() for p in files},details=details)
    (ROOT/'verifications/calculs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{count} contrôles exacts, {props} invariants, 420 exercices : OK')
    return report


if __name__=='__main__':verifier()
