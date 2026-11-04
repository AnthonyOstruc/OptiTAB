"""Contrôle indépendant des livrables : arithmétique rationnelle exacte et structure."""
from pathlib import Path
from fractions import Fraction
import ast, hashlib, json, operator, re, datetime

D=Path(__file__).resolve().parent

def value(s):
    tree=ast.parse(s.strip(),mode='eval')
    ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
    def visit(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):
            return Fraction(ast.get_source_segment(s,n))
        if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](visit(n.left),visit(n.right))
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -visit(n.operand)
        raise ValueError(ast.dump(n))
    return visit(tree.body)

def clean(s):
    s=re.sub(r'\\text\{[^{}]*\}','',s)
    for t in (r'\,',r'\;',r'\!',r'\quad',r'\qquad',r'\left',r'\right'):s=s.replace(t,'')
    s=s.replace('{,}','.').replace(r'\times','*').replace(r'\div','/').replace('&','')
    s=s.replace(r'\leq','<=').replace(r'\geq','>=').replace(r'\ne','!=')
    s=s.replace('{','').replace('}','').strip().rstrip('.,;')
    return ' '.join(s.split())

comparators={'=':operator.eq,'!=':operator.ne,'<':operator.lt,'>':operator.gt,'<=':operator.le,'>=':operator.ge}
def check_chain(s,scope):
    global checks
    if r'\qquad' in s:
        for part in s.split(r'\qquad'):check_chain(part,scope)
        return
    s=clean(s)
    parts=re.split(r'(<=|>=|!=|=|<|>)',s)
    if len(parts)<3:return
    if any(not re.fullmatch(r'[0-9.()+\-*/\s]+',x) for x in parts[::2]):
        symbolic.append({'contexte':scope,'formule':s});return
    vals=[value(x) for x in parts[::2]]
    for a,op,b in zip(vals,parts[1::2],vals[1:]):
        ok=comparators[op](a,b)
        if scope=='cours_nouveau.txt' and s=='7*4=30-3':
            assert not ok,'Le contre-exemple annoncé faux doit rester faux.'
        else:assert ok,(scope,s,str(a),op,str(b))
        checks+=1

checks=0;symbolic=[]
files=['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/correspondance.json']
texts={name:(D/name).read_text(encoding='utf-8') for name in files[:3]}
expected=json.loads((D/'verification_attendus.json').read_text(encoding='utf-8'))
blocks=[x for x in re.split(r'^===[ \t]*$',texts['exercices.txt'],flags=re.M) if x.strip()]
assert len(blocks)==len(expected)==15
titles=[];total=0
for block,e in zip(blocks,expected):
    title=block.strip().splitlines()[0];assert title not in titles; titles.append(title)
    ident=re.search(r'^Id: (nouveau-\d+)\s*$',block,re.M)[1];assert ident==e['id']
    enonce=block.split('Énoncé:\n<!-- optitab:1 -->\n',1)[1].split('\nÉtapes:',1)[0]
    steps=block.split('Étapes:\n<!-- optitab:1 -->\n',1)[1].split('\nSolution:',1)[0]
    solution=block.split('Solution:\n<!-- optitab:1 -->\n',1)[1]
    qs=e['questions'];assert len(qs)>=5
    questions=re.findall(r'^\d+\. (.*)$',enonce,re.M)
    results=re.findall(r'^::: resultat[ \t]*\n(.*?)^:::[ \t]*$',steps,re.M|re.S)
    concise=re.findall(r'^\d+\. (.*)$',solution,re.M)
    assert questions==[q['question'] for q in qs],ident
    assert len(re.findall(r'^## Question ',steps,re.M))==len(qs),ident
    assert [v.strip() for v in results]==concise==[q['reponse'] for q in qs],ident
    assert len(re.findall(r'^::: methode',steps,re.M))==len(qs),ident
    for n,q in enumerate(qs,1):
        heading=f'## Question {n} : {q["question"]}'
        actual=steps.split(heading,1)[1].split('## Question ',1)[0]
        assert q['raison'] in actual and q['methode'] in actual,(ident,n)
        # Les chaînes sont extraites du fichier final, pas recalculées depuis le générateur.
        lines=re.findall(r'\$\$(.*?)\$\$',actual,re.S)
        assert lines==q['calcul'].splitlines() if q['calcul'] else lines==[],(ident,n,lines)
        for chain in lines:check_chain(chain,ident+f'/question{n}')
    total+=len(qs)

for name in files[:2]:
    body=texts[name]
    assert body.startswith('Titre: ') and '<!-- optitab:1 -->' in body
    for display,inline in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',body,re.S):
        math=display or inline
        if r'\begin{aligned}' in math:
            math=math.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\\','')
            check_chain(math,name)
        else:
            for line in math.split(r'\\'):check_chain(line,name)

# Les assertions des sources originales restent un second jeu de données indépendant.
source=json.loads((D/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
from sympy import Rational, symbols
for e in source['exercices']:
    exec(e['controle'],{'__builtins__':{},'Rational':Rational,'n':symbols('n'),'range':range,'divmod':divmod})

corr=json.loads((D/'figures/correspondance.json').read_text(encoding='utf-8'))
figure_source=(D/'figures/figures.py').read_text(encoding='utf-8')
assert 'TOLERE' not in figure_source,'Aucune exception graphique prévue.'
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK','exercices':len(blocks),'questions':total,'minimum_questions_par_exercice':min(len(e['questions']) for e in expected),'calculs_comparaisons_verifies':checks,'assertions_sources_verifiees':len(source['exercices']),'formules_symboliques_non_numeriques':symbolic,'empreintes_finales':{name:hashlib.sha256((D/name).read_bytes()).hexdigest() for name in files}}
(D/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(D.name,json.dumps({k:v for k,v in report.items() if k not in ('empreintes_finales','formules_symboliques_non_numeriques')},ensure_ascii=False))
