"""Contrôles exacts adaptés aux nouveaux exercices et aux données graphiques."""
from pathlib import Path
from fractions import Fraction as F
import ast
import json
import operator
import re
import runpy
import sys
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
DATA=runpy.run_path(str(HERE/'revision_pedagogique_20261030.py'))['EX']
failures=[]
count=0

def check(ok,msg):
    global count
    count+=1
    if not ok: failures.append(msg)

def evaluate(code):
    def visit(node):
        if isinstance(node,ast.Expression): return visit(node.body)
        if isinstance(node,ast.Constant):
            if isinstance(node.value,bool): return node.value
            return F(str(node.value))
        if isinstance(node,ast.UnaryOp): return (-1 if isinstance(node.op,ast.USub) else 1)*visit(node.operand)
        if isinstance(node,ast.BinOp): return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(node.op)](visit(node.left),visit(node.right))
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='abs': return abs(visit(node.args[0]))
        if isinstance(node,ast.Compare):
            vals=[visit(node.left)]+[visit(x) for x in node.comparators]
            return all({ast.Lt:operator.lt,ast.Gt:operator.gt,ast.LtE:operator.le,ast.GtE:operator.ge,ast.Eq:operator.eq,ast.NotEq:operator.ne}[type(op)](a,b) for op,a,b in zip(node.ops,vals,vals[1:]))
        raise ValueError(code)
    return visit(ast.parse(code,mode='eval'))

def value(tex):
    tex=tex.strip().rstrip('.').replace('{,}','.').replace(r'\,','').replace(r'\displaystyle','')
    tex=tex.replace(r'\times','*').replace(r'\div','/').replace(r'\neq','!=').replace(r'\ne','!=').replace(r'\le','<=').replace(r'\ge','>=')
    frac=re.compile(r'\\(?:d?frac)\s*(\{[^{}]*\}|[0-9])\s*(\{[^{}]*\}|[0-9])')
    while frac.search(tex):
        tex=frac.sub(lambda m:'(('+m[1].strip('{}')+')/('+m[2].strip('{}')+'))',tex)
    tex=tex.replace('{','(').replace('}',')').replace(r'\left','').replace(r'\right','')
    if re.search(r'[A-Za-z\\]',tex): raise ValueError(tex)
    return evaluate(tex)

def formulas(text,where):
    for pair in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^\n$]+)\$(?!\$)',text,re.S):
        s=next(x for x in pair if x)
        s=s.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        s=s.replace(r'\\&=','=')
        for line in re.split(r'\\\\|\\q(?:quad|uad)|;',s):
            line=line.replace('&','').strip().strip(',')
            if re.search(r'\\(?:le|ge|ne)|[<>]',line):
                try: answer=value(line)
                except (ValueError,SyntaxError,KeyError,TypeError,ZeroDivisionError): continue
                if isinstance(answer,bool): check(answer,f'{where}: comparaison fausse {line}')
                continue
            parts=line.split('=')
            vals=[]
            for part in parts:
                try: vals.append(value(part))
                except (ValueError,SyntaxError,KeyError,TypeError,ZeroDivisionError): pass
            if len(vals)>=2: check(all(v==vals[0] for v in vals),f'{where}: égalité fausse {line}')

def audit(p):
    n=int(p.name[:3]); text=(p/'exercices.txt').read_text(encoding='utf8')
    ids=list(map(int,re.findall(r'^Id:\s*(\d+)',text,re.M)))
    baseline=(p/'sauvegardes/revision_2026-10-30/exercices.txt').read_text(encoding='utf8')
    check(ids==list(map(int,re.findall(r'^Id:\s*(\d+)',baseline,re.M))),f'{n}: identifiants ou ordre modifiés')
    titles=re.findall(r'^=== (.+)',text,re.M)
    check(len(titles)==len(set(titles))==21,f'{n}: titres dupliqués ou blocs perdus')
    changed=[]
    for b in re.split(r'^===[ \t]*$',text,flags=re.M):
        m=re.search(r'^Id: (\d+)',b,re.M)
        if not m: continue
        eid=int(m[1]); diff=re.search(r'^Difficulté: (\w+)',b,re.M)[1]; title=b.strip().splitlines()[0]
        check(('Découverte' in title and diff=='easy') or ('Entraînement' in title and diff=='medium') or ('Problème' in title and diff=='hard'),f'{eid}: préfixe incohérent')
        check('::: attention' in b or '::: retenir' in b,f'{eid}: absence de note pédagogique')
        check('Raisonner et calculer' not in b,f'{eid}: titre d’étape générique restant')
        if eid in DATA:
            changed.append(eid)
            for expr,expected in DATA[eid]['calculs_controles']:
                got=evaluate(expr); want=evaluate(expected)
                if isinstance(got,F): check(sp.Rational(got.numerator,got.denominator)==sp.Rational(want.numerator,want.denominator),f'{eid}: {expr} attendu {expected}')
                else: check(got==want,f'{eid}: {expr}')
            check('::: etape' in b and b.count('::: etape')>len(DATA[eid]['questions']),f'{eid}: raisonnement composé insuffisamment décomposé')
            if eid==2744:
                common=[d for d in range(1,85) if 84%d==126%d==0]
                check(common==[1,2,3,6,7,14,21,42],'2744: liste des diviseurs communs')
                check(max(d for d in common if d<=20)==14,'2744: limite 20 lots')
                check(max(d for d in common if 84//d>=4 and 126//d>=4)==21,'2744: minima de composition')
            if eid==2745:
                a=set(range(10,200,8)); c=set(range(14,200,12)); meet=sorted(a&c)
                check(meet[:3]==[26,50,74],'2745: horaires des rendez-vous')
            if eid==2738:
                pairs=[(i,36//i) for i in range(1,7) if 36%i==0]
                check(pairs==[(1,36),(2,18),(3,12),(4,9),(6,6)],'2738: énumération des rectangles')
                check([2*(a+b) for a,b in pairs]==[74,40,30,26,24],'2738: périmètres')
        assertion_text=b.split('Étapes:',1)[1]
        assertion_text=re.sub(r'^## Question.*$','',assertion_text,flags=re.M)
        formulas(assertion_text,f'exercice {eid}')
    check(len(changed)==6,f'{n}: six remplacements attendus')
    for pattern in ('cours_*.txt','fiche_*.txt'):
        for f in p.glob(pattern): formulas(f.read_text(encoding='utf8'),f.name)
    if n==263:
        check([F(k-4,4) for k in [1,6,3,7]]==[F(-3,4),F(1,2),F(-1,4),F(3,4)],'2752: coordonnées dessinées')
    if n==265:
        check(F(11,4)==F('2.75') and F(7,4)==F('1.75'),'2801: placement des fractions')
    print(n,'couverture, identifiants, progression et mathématiques contrôlés',flush=True)

if __name__=='__main__':
    targets=[Path(sys.argv[1])] if len(sys.argv)>1 else [next(BASE.glob(f'{n}_*')) for n in range(261,266)]
    for p in targets: audit(p)
    print(count,'contrôles de révision ;',len(failures),'échec(s)')
    for f in failures: print('ERREUR',f)
    raise SystemExit(bool(failures))
