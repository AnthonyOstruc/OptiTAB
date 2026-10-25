"""Vérifie les approfondissements, les bilans et les programmes d'atelier."""
from pathlib import Path
import contextlib,io,json,re
import sympy as sp
from approfondissements import DEFIS
from bilans import BILANS
from demonstrations import PREUVES
from ateliers import ATELIERS
ROOT=Path(__file__).resolve().parent
env={k:getattr(sp,k) for k in dir(sp) if not k.startswith('_')}
env.update(dict(zip(['x','y','p'],sp.symbols('x y p',real=True))))
verified=[];errors=[];programs=[]
def check(name,code):
    try:exec(code,dict(env));verified.append(name)
    except Exception as e:errors.append([name,type(e).__name__,str(e),code])
for i,d in enumerate(DEFIS,1):
    check(f'D{i:02d}',d.controle)
    assert len(d.indices)==2 and len(d.solutions)>=1
    for j,text in enumerate(d.solutions,1):
        for code in re.findall(r'\\begin\{python\}(.*?)\\end\{python\}',text,re.S):
            ns={}
            exec(code.strip(),ns)
            assert ns['effectifs']()==(25,27)
            programs.append(f'D{i:02d}.{j}')
for b in BILANS:
    assert len(b.automatismes)==10 and len(b.problemes)==3
    for i,(q,s,k) in enumerate(b.automatismes,1):check(f'Bilan {b.lettre} auto {i}',k)
    for i,p in enumerate(b.problemes,1):check(f'Bilan {b.lettre} problème {i}',p.controle)
for label,title,sub,body in ATELIERS:
    ns={}
    for code in re.findall(r'\\begin\{python\}(.*?)\\end\{python\}',body,re.S):
        exec(code.strip(),ns)
        if label=='atelier-debut':
            assert ns['balayage'](3)==(1.0,3.91)
            assert abs(ns['balayage'](30)[0]-1.3)<1e-12 and abs(ns['balayage'](30)[1]-4)<1e-12
        if label=='atelier-filtres':
            G,R=ns['groupe'],ns['reponse']
            assert len(G)==len(R)==8
            assert all(ns['compter'](g,r)==2 for g in ['A','B'] for r in ['O','N'])
            assert ns['freq_cond']('O','A')==0.5 and sum(r=='O' for r in R)/8==0.5
            assert sum(G[i]=='A' or R[i]=='O' for i in range(8))==6
            assert sum(not R[i]=='O' for i in range(8))==4
        programs.append(label)
# Questions flash : contrôles exacts et couverture des 30 capacités « Automatismes ».
from automatismes import SERIES,REPERES_AUTOMATISMES,DROITE_GRADUEE,COURBE_FLASH
couverts=set();questions_flash=0
for lettre,titre,questions in SERIES:
    assert len(questions)==10,lettre
    for i,(q,s,k,bloc,reperes) in enumerate(questions,1):
        check(f'Automatismes {lettre}{i}',k);questions_flash+=1
        assert reperes and set(reperes)<=set(REPERES_AUTOMATISMES),(lettre,i)
        couverts|=set(reperes)
assert couverts==set(REPERES_AUTOMATISMES),sorted(set(REPERES_AUTOMATISMES)-couverts)
assert '(-1.25,0)' in DROITE_GRADUEE and '(.75,0)' in DROITE_GRADUEE
assert '(-2,3)--(0,-1)--(4,3)' in COURBE_FLASH and '(3,-2)' in COURBE_FLASH
# Contrôles numériques indépendants des figures de concours et des contraintes.
A=sp.Matrix([0,0]);B=sp.Matrix([6,0]);C=sp.Matrix([2,4])
H=sp.Matrix([2,2]);O=sp.Matrix([3,1])
assert (H-C)[0]==0
assert (H-A).dot(C-B)==0 and (H-B).dot(C-A)==0
assert (A-O).dot(A-O)==(B-O).dot(B-O)==(C-O).dot(C-O)==10
for a in range(-10,11):
    for b in range(0,12):
        if a>=0 and a+b<=8 and a+2*b<=12: assert 3*a+4*b<=28
manifest=json.loads((ROOT/'manifeste-seconde.json').read_text(encoding='utf-8'))
for fig in manifest['figures']:
    assert (ROOT/'figures'/(fig['figure']+'.tex')).exists(),fig
for path in ROOT.rglob('*.tex'):
    if 'build' in path.relative_to(ROOT).parts:continue
    text=path.read_text(encoding='utf-8')
    assert not any(ord(c)<32 and c not in '\n\r\t' for c in text),str(path)
report={'defis':16,'automatismes':20,'problemes_bilans':6,'questions_flash':questions_flash,
 'capacites_automatismes_couvertes':len(couverts),'groupes_de_controles':len(verified),
 'programmes_complementaires':programs,'demonstrations':sum(len(p) for t,p in PREUVES),
 'visuels_uniques':manifest['visuels_uniques'],'insertions_visuelles':manifest['insertions_visuelles'],
 'controles':verified,'erreurs':errors}
(ROOT/'build/verification-complements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
if errors:raise SystemExit(1)
