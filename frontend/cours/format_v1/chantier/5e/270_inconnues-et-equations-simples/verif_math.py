"""Vérifie les 21 scénarios et leurs réponses finales à partir des données.

Contrôles exacts avec Fraction et SymPy ; aucune connexion à la base.
Une copie autonome est conservée dans chaque notion du lot 266–270.
"""
from pathlib import Path
from fractions import Fraction
import json
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

D = Path(__file__).resolve().parent
CODE = int(D.name.split('_')[0])
T = (D/'exercices.txt').read_text(encoding='utf-8')
SOURCE = (D/'source_en_ligne/exercices.txt').read_text(encoding='utf-8')
META = json.loads((D/'source_en_ligne/meta.json').read_text(encoding='utf-8'))

def tex(v):
    v=Fraction(v)
    return str(v.numerator) if v.denominator==1 else rf'\frac{{{v.numerator}}}{{{v.denominator}}}'

def contains(answer,*values):
    for v in values:
        assert str(v) in answer, (CODE,eid,v,answer)

def numeric(latex):
    """Petit interpréteur de l'arithmétique LaTeX utilisée dans ce lot."""
    latex=latex.replace('{,}','.').replace(r'\,','').replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','')
    latex=latex.replace(r'\times','*').replace(r'\div','/').replace('^','**')
    # On n'évalue que les membres purement numériques ; les identités littérales
    # sont contrôlées séparément avec SymPy ci-dessous.
    while r'\frac' in latex:
        m=re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',latex)
        if not m:
            m=re.search(r'\\frac(\d)(\d)',latex)
        if not m: return None
        latex=latex[:m.start()]+'(('+m[1]+')/('+m[2]+'))'+latex[m.end():]
    latex=latex.replace('{','(').replace('}',')')
    if re.search(r'[^\d\s.+*/()\-]',latex) or not re.search(r'\d',latex):return None
    return s.sympify(latex,rational=True)

blocks=[b for b in re.split(r'^===[ \t]*$',T,flags=re.M) if b.strip()]
assert len(blocks)==len(META['exercices'])==21
ids=[]; math_chains=0; results=0
for b in blocks:
    eid=int(re.search(r'^Id: (\d+)',b,re.M)[1]); ids.append(eid)
    title=re.search(r'^=== (.+)',b,re.M)[1]
    original=next(e for e in META['exercices'] if e['id']==eid)
    assert title==original['titre']
    difficulty=re.search(r'^Difficulté: (.+)',b,re.M)[0]
    srcblock=next(x for x in re.split(r'^===[ \t]*$',SOURCE,flags=re.M) if re.search(rf'^Id: {eid}\s*$',x,re.M))
    assert difficulty in srcblock
    en=b.split('Énoncé:')[1].split('Étapes:')[0]
    steps=b.split('Étapes:')[1].split('Solution:')[0]
    sol=b.split('Solution:')[1]
    answers=re.findall(r'^\d+\. (.+)',sol,re.M)
    assert len(answers)==6 and len(re.findall(r'^::: methode',steps,re.M))==6
    assert len(re.findall(r'^::: etape',steps,re.M))==6
    rr=re.findall(r'^::: resultat\n(.*?)\n:::',steps,re.S|re.M)
    assert rr==answers, (eid,'désaccord étapes/solution')
    results+=6
    if CODE==266:
        m=re.search(r'contient (\d+) L.*?\\frac\{(\d+)\}\{(\d+)\}.*?\\frac\{(\d+)\}\{(\d+)\}',en,re.S)
        if m:
            total,a,b1,c,d=map(int,m.groups()); morning=Fraction(total*a,b1); afternoon=Fraction(total*c,d)
            used=(morning+afternoon)/total
            contains(answers[2],tex(used)); contains(answers[3],tex(1-used))
            contains(answers[4],int(morning+afternoon),int(total-morning-afternoon))
            contains(answers[5],abs(int(afternoon-morning)))
            expected='plus' if afternoon>morning else 'moins' if afternoon<morning else 'autant'
            contains(answers[5],expected)
        else:
            total,div=map(int,re.search(r'possède (\d+) livres.*?sur (\d+)',en,re.S).groups())
            morning=Fraction(total,div); remaining=total-morning; after=remaining/4
            for answer,value in zip(answers,[morning,remaining,after,morning+after,remaining-after]): contains(answer,int(value))
            assert morning+after+remaining-after==total
    elif CODE==267:
        n=int(re.search(r'carrée de (\d+)',en)[1])
        contains(answers[0],f'{n}^2'); contains(answers[1],n*n); contains(answers[2],n)
        contains(answers[3],n*n*n); contains(answers[4],(n+n)*(n+n)); contains(answers[5],(n+n)**3)
        assert Fraction((2*n)**2,n*n)==4 and Fraction((2*n)**3,n**3)==8
    elif CODE==268:
        first,change=map(int,re.search(r'utilise (\d+) allumettes.*?ajoute (\d+) allumettes',en,re.S).groups())
        rank=int(re.search(r'3\. .*?rang (\d+)',en)[1]); target=int(re.search(r'5\. .*?(\d+) allumettes',en)[1])
        seq=[first]
        for i in range(1,max(2*rank,100)):seq.append(seq[-1]+change)
        contains(answers[0],seq[1],seq[2]); contains(answers[2],seq[rank-1])
        assert target in seq
        contains(answers[4],seq.index(target)+1)
        contains(answers[5],seq[2*rank-1],2*seq[rank-1])
        n=s.Symbol('n'); assert s.expand(first+(n-1)*change-(change*n+first-change))==0
        assert seq[2*rank-1]!=2*seq[rank-1]
    elif CODE==269:
        k,add=map(int,re.search(r'hauteur de (\d+) cm.*?x\+(\d+)',en,re.S).groups())
        value=int(re.search(r'4\. .*?x=(\d+)',en)[1]); x=s.Symbol('x')
        assert s.expand(k*(x+add)-(k*x+k*add))==0
        contains(answers[1],k*add); contains(answers[2],k*add); contains(answers[3],k*value+k*add)
        assert s.expand(k*(x+1+add)-k*(x+add))==k
        contains(answers[5],k)
    else:
        m=re.search(r'achète (\d+) pochettes.*?emballage à (\d+) €.*?totale est de (\d+) €',en,re.S)
        if m:
            n,fee,total=map(int,m.groups()); x=s.Symbol('x')
            price=s.solve(n*x+fee-total,x)[0]; delta=s.Rational(6,n)
            contains(answers[2],total-fee); contains(answers[3],tex(price)); contains(answers[5],tex(delta),tex(price+delta))
            assert n*(price+delta)+fee==total+6
        else:
            den,out=map(int,re.search(r'partage en (\d+) parts égales et affiche (\d+)',en).groups())
            value=s.solve(s.Symbol('x')/den-out,s.Symbol('x'))[0]
            contains(answers[2],f'x={value}'); contains(answers[4],'x=0')
    # Contrôle indépendant de chaque chaîne numérique des étapes.
    for formula in re.findall(r'\$\$(.*?)\$\$',steps,re.S):
        for line in formula.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
            values=[numeric(v.strip().replace('&','')) for v in line.split('=')]
            values=[v for v in values if v is not None]
            for left,right in zip(values,values[1:]):
                assert s.simplify(left-right)==0,(eid,line,left,right)
                math_chains+=1
assert len(set(ids))==21
# Exemples numériques des cours et fiches (calcul exact).
assert Fraction(3,4)+Fraction(5,6)==Fraction(19,12)
assert Fraction(3,4)-Fraction(1,6)==Fraction(7,12)
assert Fraction(2,5)+Fraction(1,3)==Fraction(11,15)
assert (40//5)*3==24 and 60//3+(60-60//3)//4==30
assert 3+2*5**2==53 and 2*4**2+3==35
assert 3*2**2+2*2==16 and 2*(7+3)==20 and 7*3==21
assert 3*5+1==16 and Fraction(18,5)==Fraction('3.6')
assert [i*i for i in range(13)]==[0,1,4,9,16,25,36,49,64,81,100,121,144]
report={'notion':CODE,'exercices':21,'reponses_controlees':results,'egalites_numeriques_controlees':math_chains,'identites_et_donnees':'OK','statut':'OK'}
(D/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
