"""Contrôles exacts des remplacements et preuve de conservation des anciens calculs.

Les propositions fausses des énoncés sont exclues des tests d'égalités : seuls
les corps des étapes et des résultats sont évalués, jamais les questions.
"""
from pathlib import Path
from fractions import Fraction as F
import re,json,sys,contextlib,io
import sympy as s
from revision_20261030 import DATA,simple_bill

BASE=Path(__file__).resolve().parent.parent
def blocks(t):return [b.strip() for b in re.split(r'^===[ \t]*$',t,flags=re.M) if b.strip()]
def ident(b):return int(re.search(r'^Id: (\d+)',b,re.M)[1])
def formulae(t):return re.findall(r'\${1,2}([^$]+)\${1,2}',t)
def numeric(t):
    t=t.replace('{,}','.').replace(r'\,','').replace(r'\left','').replace(r'\right','').replace(r'\displaystyle','')
    def atom(text,pos):
        if pos>=len(text):raise ValueError(text)
        if text[pos]=='{':
            depth=1;j=pos+1
            while depth:
                if text[j]=='{':depth+=1
                if text[j]=='}':depth-=1
                j+=1
            return text[pos+1:j-1],j
        return text[pos],pos+1
    while r'\frac' in t:
        pos=t.rfind(r'\frac');a,j=atom(t,pos+5);b,k=atom(t,j)
        t=t[:pos]+'(('+a+')/('+b+'))'+t[k:]
    t=t.replace(r'\times','*').replace(r'\div','/').replace('^','**').replace('{','(').replace('}',')')
    if re.search(r'[^\d\s.+*/()\-]',t) or not re.search(r'\d',t):return None
    t=re.sub(r'(?<=\d)\(', '*(',t);t=re.sub(r'\)(?=[\d(])',')*',t)
    if t.lstrip().startswith(('**','*','/')):return None
    return s.sympify(t,rational=True)

def independent(code):
    """Recalcul des trente contextes nouveaux, sans lire leurs chaînes corrigées."""
    if code==266:
        assert [F(2,7)+F(3,7),F(6,9)-F(2,9),1-F(5,8)]==[F(5,7),F(4,9),F(3,8)]
        assert [F(1,2)+F(1,3),F(3,4)+F(1,8),F(5,6)-F(1,3),1+F(2,5)]==[F(5,6),F(7,8),F(1,2),F(7,5)]
        assert [F(3,8)+F(7,6),F(5,12)-F(2,9),F(7,10)+F(3,4),2-F(7,12)]==[F(37,24),F(7,36),F(29,20),F(17,12)]
        assert [F(3,4)+F(1,6),1-F(3,7),F(5,6)+F(1,3),F(11,15)-F(2,5)]==[F(11,12),F(4,7),F(7,6),F(1,3)]
        mon,tue=240*F(3,8),240*F(5,12);left=240-mon-tue;wed=left*F(2,5)
        assert (mon,tue,left,wed,(mon+tue+wed)/240,240-mon-tue-wed)==(90,100,50,20,F(7,8),30)
        used=F(1,3)+F(7,30);left=F(4,5)-used
        assert (used,left,F(1,4)-left,left-F(1,6))==(F(17,30),F(7,30),F(1,60),F(1,15))
    elif code==267:
        assert (5**2,3**3,6**2,5**3,4**3)==(25,27,36,125,64)
        assert [v*v for v in (6,7,8,9,11,12)]==[36,49,64,81,121,144]
        assert (8**2==4**3) and 7**2<50<8**2
        assert [3+2*5**2,(3+2)*5**2,(3+2)**2*5,10**3-4*3**3]==[53,125,125,892]
        assert (F('1.5')**2,F('2.5')**3,2*F('1.5')**2+3)==(F('2.25'),F('15.625'),F('7.5'))
        assert (F('4.5')/F('.5'))**2==81 and 5*20-81==19
        assert 5**2-F('4.5')**2==F('4.75')
        assert (30//5,6**2,6**3,30**3,5**3,6**3-6**2)==(6,36,216,27000,125,180)
        assert 180*125/1000==22.5
        assert (9**2,4**3,11**2)==(81,64,121)
        assert (7**2,7**3,1**2,1**3,12**2,10**3)==(49,343,1,1,144,1000)
        assert (2**3+3**2,(2+3)**2,2*3**2)==(17,25,18)
        assert 10**2-9**2==19 and 9**2<90<10**2
        assert F('1.2')**2==F('1.44') and 2**3+2**3==16 and 4**3==64 and 3**2*3==27
        assert (8**2,9**2,9**2-8**2,5**3,6**3,6**3-5**3)==(64,81,17,125,216,91)
        assert [n**3 for n in (6,7,8,9,10)]==[216,343,512,729,1000]
        assert 125+216==341 and 6**3<341<7**3
    elif code==268:
        assert (3*(4+2),3*4+2)==(18,14)
        assert (2*(8+3),8*3,2*(10+3),10*3)==(22,24,26,30)
        a=lambda x:3*x*x+2*x
        assert [a(x) for x in (0,2,F('1.5'))]==[0,16,F('9.75')]
        assert 3*(2**2+2*2)==24
        assert [n+6==3*n for n in (2,3,4)]==[False,True,False]
        n=s.Symbol('n');assert s.expand((n+2)**2-n**2-(4*n+4))==0
        assert [(n+2)**2-n*n for n in (1,2,3,10,15)]==[8,12,16,44,64]
        assert [(3*n+8,5*n) for n in (2,4,6,10)]==[(14,10),(20,20),(26,30),(38,50)]
    elif code==269:
        x,n=s.symbols('x n')
        for a,b in [(3*(x+2),3*x+6),(2*x+5*x,7*x),(3*x+4+x+2,4*x+6),(7*x-2*x+3,5*x+3),(5*(x-2),5*x-10),(F('2.5')*(x+4),F('2.5')*x+10),(3*(2*x+1)+x,7*x+3),(6*(3+x)-2*x,4*x+18),(6*x+18,6*(x+3)),(15*x-10,5*(3*x-2)),(4*x+12+2*x+6,6*(x+3)),(n+n+1,2*n+1),(n+n+1+n+2,3*(n+1)),(2*(3*x+4),6*x+8),(6*(x+1)+2,6*x+8)]:
            assert s.expand(a-b)==0
        assert 1**2+2**2==5 and 2**2<5<3**2 and 6*(5+3)==48
        assert 2*(3*2+4)==6*(2+1)+2==20 and 6*2+6==18
    else:
        assert (19-7,F('6.2')-F('2.5'),2-6)==(12,F('3.7'),-4)
        assert (F(18,4),F(0,2),7*3)==(F('4.5'),0,21)
        assert (F('12.5')-F('7.8'),F(18,4),F('7.5')/5)==(F('4.7'),F('4.5'),F('1.5'))
        assert (F(3,2)*4,9/F(3,2),F(5,4)-F(3,4))==(6,6,F(1,2))
        assert (3+4,F(3,5),5-7)==(7,F('.6'),-2)
        content=F('4.8')-F('1.2');per=content/8
        assert (content,per,per*1000,per*1000+50,10*per,10*per-content)==(F('3.6'),F('.45'),450,500,F('4.5'),F('.9'))

def main(code):
    d=next(BASE.glob(f'{code}_*'));backup=d/'sauvegardes/revision_2026-10-30'
    old=blocks((backup/'exercices.txt').read_text(encoding='utf-8'));current=blocks((d/'exercices.txt').read_text(encoding='utf-8'))
    assert [ident(b) for b in old]==[ident(b) for b in current] and len(current)==21
    # L'ancien audit exact tourne sur la version sauvegardée ; les calculs
    # conservés doivent rester identiques à cette version auditée.
    legacy=(backup/'verif_math.py').read_text(encoding='utf-8')
    legacy=legacy.replace("T = (D/'exercices.txt').read_text(encoding='utf-8')","T = (D/'sauvegardes/revision_2026-10-30/exercices.txt').read_text(encoding='utf-8')")
    legacy=legacy.replace("D/'verification_math.json'","D/'verification_math_avant_revision.json'")
    with contextlib.redirect_stdout(io.StringIO()):exec(compile(legacy,str(d/'verif_math.py'),'exec'),{'__file__':str(d/'verif_math.py')})
    titles=[];chains=0;answers=0;retained=0;replaced={e['slot'] for e in DATA[code]}
    for i,(before,b) in enumerate(zip(old,current)):
        eid=ident(b);title=re.search(r'^=== (.+)',b,re.M)[1];titles.append(title)
        diff=re.search(r'^Difficulté: (.+)',b,re.M)[1]
        assert title.startswith({'easy':'Découverte -','medium':'Entraînement -','hard':'Problème -'}[diff]),(code,eid,title,diff)
        assert not re.search(r'\\n(?![A-Za-z])',b),(code,eid,'saut de ligne littéral')
        assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',b),(code,eid,'caractère de contrôle')
        steps=b.split('Étapes:')[1].split('Solution:')[0];sol=b.split('Solution:')[1]
        results=re.findall(r'^::: resultat\n(.*?)\n:::',steps,re.M|re.S)
        short=re.findall(r'^\d+\. (.+)',sol,re.M)
        assert results==short,(code,eid,'résultats et solution')
        qs=re.findall(r'^## Question ',steps,re.M)
        assert len(qs)==len(results)==len(re.findall(r'^::: methode',steps,re.M))
        assert len(re.findall(r'^::: etape ',steps,re.M))>=len(qs)
        answers+=len(results)
        if i not in replaced and not (code==270 and simple_bill(before)):
            # Les nouvelles notes et nouveaux titres n'introduisent pas de calcul.
            assert formulae(before)==formulae(b),(code,eid,'calcul conservé modifié')
            retained+=1
        for body in re.findall(r'^::: (?:etape[^\n]*|resultat)\n(.*?)\n:::',steps,re.M|re.S):
            for f in formulae(body):
                for line in f.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
                    vals=[numeric(v.strip().replace('&','')) for v in line.split('=')]
                    for left,right in zip(vals,vals[1:]):
                        if left is not None and right is not None:
                            assert s.simplify(left-right)==0,(code,eid,line,left,right)
                            chains+=1
        if code==270 and i not in replaced and simple_bill(before):
            m=re.search(r'achète (\d+) pochettes.*?emballage à (\d+) €.*?totale est de (\d+) €',before,re.S)
            n,fee,total=map(int,m.groups());price=F(total-fee,n);delta=F(6,n)
            assert n*price+fee==total and n*(price+delta)+fee==total+6
            assert f'{n}x={total-fee}' in b
    assert len(set(titles))==21
    independent(code)
    result={'notion':code,'exercices':21,'questions':answers,'ids_conserves':True,'calculs_anciens_conserves':retained,'egalites_numeriques_controlees':chains,'nouveaux_contextes_recalcules':len(DATA[code]),'audit_avant_revision':'OK','statut':'OK'}
    (d/'verification_revision_20261030.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':
    for code in map(int,sys.argv[1:] or range(266,271)):main(code)
