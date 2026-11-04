"""Relecture exacte des nombres publiés, sans régénérer les documents."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,operator,re,sys,math
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
IDS=(132,134,135,136,137,284,285)
count=0;errors=[];stats={}
def check(ok,msg):
    global count
    count+=1
    if not ok: errors.append(msg)
def evaluate(s):
    def go(n):
        if isinstance(n,ast.Expression): return go(n.body)
        if isinstance(n,ast.Constant): return F(str(n.value))
        if isinstance(n,ast.UnaryOp): return (-1 if isinstance(n.op,ast.USub) else 1)*go(n.operand)
        if isinstance(n,ast.BinOp): return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](go(n.left),go(n.right))
        if isinstance(n,ast.Compare):
            vals=[go(n.left)]+[go(x) for x in n.comparators]
            return all({ast.Lt:operator.lt,ast.Gt:operator.gt,ast.LtE:operator.le,ast.GtE:operator.ge,ast.Eq:operator.eq,ast.NotEq:operator.ne}[type(op)](a,b) for op,a,b in zip(n.ops,vals,vals[1:]))
        raise ValueError(s)
    return go(ast.parse(s,mode='eval'))
def value(s):
    s=s.strip().rstrip('.').replace('{,}','.').replace(r'\,','').replace(r'\displaystyle','')
    for a,b in [(r'\times','*'),(r'\div','/'),(r'\neq','!='),(r'\ne','!='),(r'\le','<='),(r'\ge','>=')]:s=s.replace(a,b)
    pat=re.compile(r'\\(?:d?frac)\s*(\{[^{}]*\}|[0-9])\s*(\{[^{}]*\}|[0-9])')
    while pat.search(s): s=pat.sub(lambda m:'(('+m[1].strip('{}')+')/('+m[2].strip('{}')+'))',s)
    s=s.replace(r'\left','').replace(r'\right','').replace('{','(').replace('}',')')
    if re.search(r'[A-Za-z\\]',s): raise ValueError(s)
    return evaluate(s)
def formulas(t,where):
    for pair in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^\n$]+)\$(?!\$)',t,re.S):
        s=next(x for x in pair if x).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\\&=','=')
        for line in re.split(r'\\\\|\\q(?:quad|uad)|;',s):
            line=line.replace('&','').strip().strip(',')
            if re.search(r'\\(?:le|ge|ne)|[<>]',line):
                try:result=value(line)
                except (ValueError,SyntaxError,KeyError,TypeError,ZeroDivisionError):continue
                if isinstance(result,bool):check(result,where+': comparaison fausse '+line)
                continue
            vals=[]
            for part in line.split('='):
                try: vals.append(value(part))
                except (ValueError,SyntaxError,KeyError,TypeError,ZeroDivisionError):pass
            if len(vals)>=2:check(all(v==vals[0] for v in vals),where+': égalité fausse '+line)

for n in IDS:
    d=next(BASE.glob(str(n)+'_*')); before=count
    meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
    text=(d/'exercices.txt').read_text(encoding='utf-8'); records=json.loads((d/'revision_20261030.json').read_text(encoding='utf-8'))
    oldids=[str(x['id']) for x in meta['exercices']];newids=re.findall(r'^Id: (\S+)',text,re.M)
    check(newids==oldids if n!=136 else newids==['nouveau-'+str(k) for k in range(1,9)],f'{n}: identifiants')
    check(len(set(newids))==len(newids),f'{n}: doublons')
    check(len({x['titre'] for x in records})==len(records),f'{n}: titres uniques')
    for ex in records:
        eid=ex['id']; title=ex['titre'];diff=ex['difficulte'];qs=ex['questions']
        check((diff=='easy' and title.startswith('Découverte -')) or (diff=='medium' and title.startswith('Entraînement -')) or(diff=='hard' and title.startswith('Problème -')),f'{eid}: préfixe/difficulté')
        check(all(q['methode'] and q['etapes'] and q['reponse'] for q in qs),f'{eid}: corrigé incomplet')
        check(all(t and body for q in qs for t,body in q['etapes']),f'{eid}: étapes vides')
        for q in qs:
            formulas('\n'.join(body for t,body in q['etapes']),str(eid))
        check(ex['note']!='',f'{eid}: note pédagogique')
    for f in list(d.glob('cours_*.txt'))+list(d.glob('fiche_*.txt'))+[d/'exercices.txt']:
        s=f.read_text(encoding='utf-8')
        check(not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',s),f'{n}/{f.name}: caractères de contrôle')
        if f.name!='exercices.txt':formulas(s,f'{n}/{f.name}')
    # Contrôle indépendant des données conservées et de chaque famille numérique.
    for ex in records:
        t=ex['introduction'];eid=ex['id']
        if 'Partager des tartes sans en perdre' in ex['titre']:
            a,b=map(int,re.search(r'(\d+) tartes.*?entre (\d+) personnes',t).groups())
            check(F(a,b)*b==a and F(2*a,2*b)==F(a,b),f'{eid}: partage exact')
        if 'Clôturer un potager' in ex['titre']:
            a,b=map(int,re.search(r'(\d+) m de long.*?(\d+) m de large',t).groups());need=2*(a+b)-1;roll=(need+4)//5
            check((roll-1)*5<need<=roll*5 and 0<=roll*5-need<5,f'{eid}: conditionnement')
        if 'Le réservoir du jardin' in ex['titre']:
            a,b=map(int,re.search(r'\\frac\{(\d+)\}\{(\d+)\}',t).groups());v=int(re.search(r'(\d+) L',t)[1])
            check(F(a,b)+F(1,b//2)==F(a+2,b),f'{eid}: fractions de la même référence')
            check(v*F(a+2,b)+v*F(b-a-2,b)==v,f'{eid}: bilan du volume')
        if 'Une enquête à traduire' in ex['titre']:
            total=int(re.search(r'(\d+) élèves',t)[1]);p=int(re.search(r'(\d+)\s*%',t)[1])
            check(F(total*p,100).denominator==1 and F(total*p,100)+F(total*(100-p),100)==total,f'{eid}: effectifs entiers et complément')
    stats[n]=count-before

# Résultats de décisions/énumérations non ramenés à une simple égalité affichée.
for actual,expected in [
 ([k for k in range(100) if k*70<=800],list(range(12))),
 ([(k,10-k) for k in range(1,6)],[(1,9),(2,8),(3,7),(4,6),(5,5)]),
 (math.ceil(22/3),8),(math.ceil(56/10),6),(math.ceil(28/5),6),
 (F(9,25)*100,36),(F(12,30)*100,40),(F(190,800),F(19,80)),
 (F(3,4)*5-3,F(3,4)),(F(1,3)+F(1,4),F(7,12)),
 (F(80)*F(75,100)+5,65),(F(85)*F(75,100),F('63.75'))]:check(actual==expected,'décision/énumération '+str(expected))
import runpy
pent=runpy.run_path(str(next(BASE.glob('136_*'))/'figures/figures.py'))['FIGURES']['pentagone']
outline=pent.split(r'\draw[geoTrait] ',1)[1].split('--cycle;',1)[0]
pts=[tuple(map(float,p)) for p in re.findall(r'\((-?[\d.]+),(-?[\d.]+)\)',outline)]
for i,side in enumerate((4,5,6,4,7)):
    a,b=pts[i],pts[(i+1)%5]
    check(abs(math.dist(a,b)-side)<2e-6,f'pentagone : côté {i+1}')
check(3*10+5==35,'grille des pourcentages :35cases')
check(8*1+6*F(1,2)==11,'surface des huit carreaux et six moitiés')
check(4*F(1,4)==1 and F(7,4)-F(3,4)==1,'demi-droite en quarts')
report={'controles':count,'par_notion':stats,'erreurs':errors}
(HERE/'preuves_mathematiques_20261030.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
raise SystemExit(bool(errors))
