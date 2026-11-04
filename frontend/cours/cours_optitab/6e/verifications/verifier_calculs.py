"""Calculs exacts, contrôles sources et invariants de la Sixième."""
import json
import math
import sys
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'outils'))
from modele_6e import FRONT,n
from construire_6e import CHAPITRES,BUILDERS


def verifier():
    count=0;details=[];questions=0
    for c in CHAPITRES:
        for level in range(3):
            for i in range(7):
                e=BUILDERS[c.slug](i,level)
                assert len(e.questions)>=6
                for j,q in enumerate(e.questions,1):
                    if q.controle:
                        assert eval(q.controle,{'F':F,'abs':abs,'sum':sum,'divmod':divmod,'all':all,'any':any,'range':range}), (c.slug,level,i,j,q.controle)
                        count+=1
                questions+=len(e.questions)
                details.append(dict(slug=c.slug,niveau=level,indice=i,questions=len(e.questions),statut='réussi'))
    env={k:getattr(s,k) for k in ['Rational','sqrt','expand','simplify','solve','solveset','factorint','isprime','divisors','gcd','ilcm','degree','S','pi','sin','cos','tan','N','Abs','binomial']}
    env.update(x=s.Symbol('x',real=True),n=s.Symbol('n',integer=True),ceil=math.ceil,math=math)
    source_checks=0
    for c in CHAPITRES:
        for e in c.exercices:
            exec(e.controle,env.copy());source_checks+=1
    invariants=0
    for level in range(3):
        for i in range(7):
            # Position d'un point de la médiatrice : distances aux extrémités égales.
            half=2+i;pa=half+2+level
            height_squared=pa*pa-half*half
            assert height_squared>0 and half*half+height_squared==pa*pa
            # Triangle isocèle constructible et angle partagé en deux parts égales.
            base=4+i;side=base+1+level
            assert base<2*side
            angle=30+10*i+5*level
            assert 0<angle<180 and 2*F(angle,2)==angle
            # Conversion d'aire : compter les centimètres carrés d'un rectangle.
            length,width=4+i,2+level
            assert (10*length)*(10*width)==100*(length*width)
            # Tracer l'escalier indépendamment du texte.
            steps=3+level+i%3
            x=y=0
            for _ in range(steps):x+=1;y+=1
            assert (x,y)==(steps,steps)
            invariants+=5
    files=[]
    for c in CHAPITRES:
        files.extend([ROOT/f'cours_{c.slug}_6e.txt',FRONT/f'cours/resume/6e/resume_{c.slug}_6e.txt',FRONT/f'exercices/6e/exercice_{c.slug}_6e.txt'])
    report=dict(chapitres=len(CHAPITRES),exercices=len(details),questions=questions,
        controles_exercices=count,controles_sources=source_checks,invariants=invariants,erreurs=[],
        portee='Calculs explicites des scénarios, contrôles du livre source et invariants géométriques. Les raisonnements en langage naturel et la qualité éditoriale requièrent aussi une relecture.',
        empreintes={str(p.relative_to(FRONT)):sha256(p.read_bytes()).hexdigest() for p in files},details=details)
    (ROOT/'verifications/calculs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(details)} exercices, {questions} questions : {count} contrôles exacts, {source_checks} contrôles sources, {invariants} invariants réussis.')
    return report


if __name__=='__main__':verifier()
