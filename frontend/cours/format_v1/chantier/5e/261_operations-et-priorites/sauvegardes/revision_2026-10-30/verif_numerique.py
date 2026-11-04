"""Audit exact des 105 exercices (ou du dossier passé en argument).

Recalcule les réponses depuis les données de chaque énoncé ; vérifie aussi
les égalités numériques des cours, fiches et corrigés avec SymPy rationnel.
Aucun accès à la base, aucun réseau, aucune modification de contenu.
"""
from pathlib import Path
from fractions import Fraction
import json
import math
import re
import sys
import sympy as sp

BASE=Path(__file__).resolve().parent.parent
checked=0
failures=[]

def val(s):
    s=s.replace('{,}','.').replace(r'\,','').replace(r'\displaystyle','').strip()
    while re.search(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',s):
        s=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
    s=s.replace(r'\frac34','(3/4)').replace(r'\frac54','(5/4)').replace(r'\frac14','(1/4)').replace(r'\frac13','(1/3)').replace(r'\frac74','(7/4)')
    s=s.replace(r'\frac58','(5/8)').replace(r'\frac38','(3/8)').replace(r'\frac25','(2/5)').replace(r'\frac23','(2/3)')
    s=re.sub(r'\\frac\{(\d+)\}(\d)',r'((\1)/(\2))',s)
    s=s.replace(r'\times','*').replace(r'\div','/').replace(':','/').replace('{','(').replace('}',')').rstrip('.')
    if not re.fullmatch(r'[\d\s.()+*/-]+',s): raise ValueError(s)
    return sp.sympify(s,rational=True)

def numeric(s):
    return [val(x) for x in re.findall(r'\$(.*?)\$',s) if re.fullmatch(r'[\d{}.,+*/()\\a-z-]+',x)]

def check(ok, message):
    global checked
    checked+=1
    if not ok: failures.append(message)

def equalities(text, label):
    for block in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^\n$]+)\$(?!\$)',text,re.S):
        formula=next((s for s in block if s),'')
        formula=formula.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
        formula=formula.replace('\\\\=', '=')
        for f in re.split(r'\\quad|;|\\\\',formula):
            f=f.strip().strip(',')
            if '=' not in f or any(t in f for t in ('<','>',r'\le',r'\ge',r'\ne',r'\text')): continue
            terms=f.split('=')
            try: values=[val(t) for t in terms]
            except (ValueError,TypeError,sp.SympifyError): continue
            check(all(v==values[0] for v in values),f'{label}: égalité fausse {f}')

def audit(p):
    n=int(p.name[:3]); meta=json.loads((p/'source_en_ligne/meta.json').read_text(encoding='utf8'))
    ex=(p/'exercices.txt').read_text(encoding='utf8')
    blocks=[b for b in re.split(r'^===[ \t]*$',ex,flags=re.M) if re.search(r'^Id:',b,re.M)]
    check(len(blocks)==21,f'{n}: 21 exercices attendus')
    for b in blocks:
        eid=int(re.search(r'^Id: (\d+)',b,re.M)[1]); title=b.strip().splitlines()[0].replace('===','',1).strip(); m=next(x for x in meta['exercices'] if x['id']==eid)
        check(title==m['titre'],f'{eid}: titre modifié')
        original=(p/'source_en_ligne/exercices.txt').read_text(encoding='utf8')
        original_block=next(x for x in re.split(r'^===[ \t]*$',original,flags=re.M) if re.search(rf'^Id:\s*{eid}\s*$',x,re.M))
        check(re.search(r'^Difficulté:.*',b,re.M)[0]==re.search(r'^Difficulté:.*',original_block,re.M)[0],f'{eid}: difficulté modifiée')
        statement=b.split('Énoncé:')[1].split('Étapes:')[0]
        steps=b.split('Étapes:')[1].split('Solution:')[0]
        answers=re.findall(r'^\d+\. (.*)$',b.split('Solution:')[1],re.M)
        check(len(answers)==6 and steps.count('::: methode')==6 and steps.count('::: etape')==6 and steps.count('::: resultat')==6,f'{eid}: structure incomplète')
        if n==261 and 'Un club prépare' in statement:
            data=re.search(r'prépare (\d+) ateliers.*?reçoit (\d+) carnets.*?et (\d+) carnets.*?coûte \$(.*?)\$.*?dispose de \$(.*?)\$',statement,re.S)
            k,a,c=map(int,data.group(1,2,3)); price,budget=[val(v) for v in data.group(4,5)]; qty=k*(a+c); cost=qty*price
            expected=[a+c,qty,cost,cost+6,budget-cost-6,6*(k-1)]
            for i,(answer,want) in enumerate(zip(answers,expected)):
                if i in (0,1,5): actual=int(re.search(r'\d+',answer)[0])
                else: actual=val(re.findall(r'\$(.*?)\$',answer)[0].split('=')[-1])
                check(actual==want,f'{eid} Q{i+1}: {actual} au lieu de {want}')
        elif n==261:
            v,c=[val(x) for x in re.findall(r'\$(.*?)\$',statement)[:2]]; full=int(sp.floor(v/c)); rem=v-full*c
            for i,want in [(2,full),(3,rem),(4,full+1),(5,c-rem)]:
                actual=int(re.search(r'\d+',answers[i])[0]) if i in (2,4) else val(re.findall(r'\$(.*?)\$',answers[i])[0])
                check(actual==want,f'{eid} Q{i+1}')
            quotient=val(re.findall(r'\$(.*?)\$',answers[0])[0]); shifted=val(re.findall(r'\$(.*?)\$',answers[1])[0]); check(quotient==shifted==v/c,f'{eid}: conservation quotient')
        elif n==262 and 'association' in statement:
            a,c=map(int,re.search(r'ranger (\d+) objets.*?maximum (\d+) objets',statement,re.S).groups()); q,r=divmod(a,c)
            check(list(map(int,re.findall(r'\d+',answers[1])))==[q,r],f'{eid}: quotient reste')
            check(int(re.search(r'\d+',answers[3])[0])==math.ceil(a/c),f'{eid}: boîtes')
            check(int(re.search(r'\d+',answers[4])[0])==(-a)%c,f'{eid}: places vides')
        elif n==262 and 'cartes rouges' in statement:
            a,c=map(int,re.search(r'possède (\d+) cartes rouges et (\d+) cartes bleues',statement).groups()); divs=[k for k in range(1,min(a,c)+1) if a%k==c%k==0]
            check(list(map(int,re.findall(r'\d+',answers[2])))==divs,f'{eid}: diviseurs communs')
            check(int(re.search(r'\d+',answers[3])[0])==max(divs),f'{eid}: maximum lots')
            check(list(map(int,re.findall(r'\d+',answers[4])))==[a//max(divs),c//max(divs)],f'{eid}: composition lots')
        elif n==262:
            a,c=map(int,re.search(r'toutes les (\d+) secondes.*?toutes les (\d+) secondes',statement).groups()); t=next(k for k in range(1,a*c+1) if k%a==k%c==0)
            for i,expected in [(0,[a*k for k in range(1,6)]),(1,[c*k for k in range(1,6)]),(2,[t]),(3,[t//a,t//c]),(4,[2*t,3*t])]:
                check(list(map(int,re.findall(r'\d+',answers[i])))==expected,f'{eid} Q{i+1}')
        elif n==263:
            a,c,d=map(int,re.search(r'abscisses (-?\d+), (-?\d+) et (-?\d+)',statement).groups()); order=[a,d,0,c]
            check(list(map(int,re.findall(r'-?\d+',answers[1])))==sorted(order),f'{eid}: ordre')
            check(int(re.search(r'\d+',answers[2])[0])==abs(a),f'{eid}: distance origine')
            check(int(re.findall(r'\$(.*?)\$',answers[3])[-1])==-a,f'{eid}: opposé')
            check(int(re.search(r'\d+',answers[4])[0])==abs(c-a),f'{eid}: distance AB')
            tied=len(set(map(abs,order)))<len(order)
            check(('À égalité' in answers[5])==tied,f'{eid}: égalité des distances')
        elif n==264:
            start,up,down=map(int,re.search(r'de (-?\d+) °C.*?de (\d+) °C.*?de (\d+) °C',statement).groups()); temperatures=[start,start+up,start+up-down]; expected=[up,temperatures[1],-down,temperatures[2],up-down,down-up]
            check([int(re.findall(r'\$(.*?)\$',s)[0]) for s in answers]==expected,f'{eid}: températures/variations')
        elif n==265 and 'Un atelier possède' in statement:
            total,a,c=map(int,re.search(r'possède (\d+) L.*?\\frac\{(\d+)\}\{(\d+)\}',statement).groups())
            for i,want in [(1,sp.Rational(a,c)),(2,sp.Rational(total,c)),(3,sp.Rational(total*a,c)),(4,sp.Rational(c-a,c))]:
                actual=val(re.findall(r'\$(.*?)\$',answers[i])[0]); check(actual==want,f'{eid} Q{i+1}')
            check(answers[5].startswith('Oui')==(2*a>c),f'{eid}: dépasse moitié')
        else:
            (a,c),(d,e)=[tuple(map(int,v)) for v in re.findall(r'\\frac\{(\d+)\}\{(\d+)\}',statement)]; length=int(re.search(r'mesurait (\d+) cm',statement)[1])
            expr=re.findall(r'\$(.*?)\$',answers[3])[0].split('=')
            check(all(val(x)==sp.Rational(a,c)-sp.Rational(d,e) for x in expr),f'{eid}: écart fractions')
            check([val(x) for x in re.findall(r'\$(.*?)\$',answers[4])]==[sp.Rational(length*a,c),sp.Rational(length*d,e)],f'{eid}: longueurs')
        equalities(steps,f'exercice {eid}')
        check(r'\n' not in b,f'{eid}: retour littéral')
    for pat in ('cours_*.txt','fiche_*.txt'):
        for file in p.glob(pat): equalities(file.read_text(encoding='utf8'),file.name)
    print(p.name,': 21 exercices et documents vérifiés')

if __name__=='__main__':
    targets=[Path(sys.argv[1])] if len(sys.argv)>1 else [p for p in sorted(BASE.iterdir()) if p.name[:3] in {'261','262','263','264','265'}]
    for p in targets: audit(p)
    print(checked,'contrôles exacts ;',len(failures),'échec(s)')
    for failure in failures: print('ERREUR',failure)
    sys.exit(bool(failures))
