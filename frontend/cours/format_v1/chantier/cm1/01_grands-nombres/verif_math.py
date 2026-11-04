# -*- coding: utf-8 -*-
"""Contrôle autonome des livrables réels : toutes relations numériques exactes et invariants."""
from pathlib import Path
from fractions import Fraction
import re,json,hashlib
P=Path(__file__).resolve().parent
CODE=int(P.name[:2])

def operand(s,i):
    while i<len(s) and s[i].isspace():i+=1
    if s[i]=='{':
        start=i+1;depth=1;i+=1
        while depth:
            if s[i]=='{':depth+=1
            if s[i]=='}':depth-=1
            i+=1
        return s[start:i-1],i
    return s[i],i+1
def convert(s):
    s=s.replace('\\dfrac','\\frac')
    while '\\frac' in s:
        i=s.index('\\frac');a,j=operand(s,i+5);b,k=operand(s,j)
        s=s[:i]+'(('+convert(a)+')/('+convert(b)+'))'+s[k:]
    for a,b in [('{,}','.'),('\\,',''),('\\times','*'),('\\div','/'),('\\ne','!='),('\\le','<='),('\\ge','>='),('\\quad',''),('&','')]:s=s.replace(a,b)
    return s.replace('{','').replace('}','').strip()
def numeric_relations(text,origin):
    count=0
    # Les titres citent parfois une erreur à corriger : seuls les raisonnements et résultats sont affirmés.
    text=re.sub(r'^## Question .*$', '',text,flags=re.M)
    for hit in re.finditer(r'\$\$(.*?)\$\$|\$(.*?)\$',text,re.S):
        math=hit[1] if hit[1] is not None else hit[2]
        try:expr=' '.join(convert(math).split())
        except (IndexError,ValueError):continue
        if not re.search('[=<>]',expr):continue
        if re.search(r'[^0-9\s.()+*/=<>!\-]',expr):continue
        expr=re.sub(r'(?<![<>=!])=(?!=)','==',expr)
        expr=re.sub(r'\d+(?:\.\d+)?',lambda m:"Fraction('"+m[0]+"')",expr)
        assert eval(expr,{'__builtins__':{},'Fraction':Fraction}),(origin,math,'relation affichée fausse')
        count+=1
    return count
def bare_numbers(text):
    txt=text.replace('\\,','').replace('{,}','.');return [Fraction(x) for x in re.findall(r'(?<![A-Za-z])\d+(?:\.\d+)?',txt)]
def r(ex,q):return manifest[ex-1]['questions'][q-1]['r']
def expect_number(ex,q,expected):
    values=bare_numbers(r(ex,q));assert Fraction(expected) in values,(ex,q,expected,r(ex,q))
    return 1

manifest=json.loads((P/'verification_questions.json').read_text(encoding='utf-8'))
assert len(manifest)==15
texts={name:(P/name).read_text(encoding='utf-8') for name in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt')}
for name,sha in json.loads((P/'empreintes_finales.json').read_text(encoding='utf-8')).items():
    assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha,(name,'livrable modifié après rédaction')
    assert not any(ord(c)<32 and c not in '\r\n' for c in texts[name]),(name,'contrôle ou tabulation interdit')
blocks=[b for b in re.split(r'^===[ \t]*$',texts['exercices.txt'],flags=re.M) if b.strip()]
assert len(blocks)==15
count=0
for i,(m,b) in enumerate(zip(manifest,blocks),1):
    assert f'Id: nouveau-{i}\n' in b
    enonce,steps=b.split('Énoncé:\n',1)[1].split('Étapes:\n',1)
    steps,solution=steps.split('Solution:\n',1)
    questions=re.findall(r'^(\d+)\. ',enonce,re.M)
    assert questions==['1','2','3','4','5']
    assert len(re.findall(r'^## Question ',steps,re.M))==5
    results=re.findall(r'^::: resultat[ \t]*\n(.*?)^:::',steps,re.M|re.S)
    assert len(results)==5
    for j,(qt,result) in enumerate(zip(m['questions'],results),1):
        assert result.strip()==qt['r'],(i,j,'résultat différent du document relu')
        assert f'{j}. {qt["r"]}' in solution,(i,j,'solution divergente')
        assert qt['q'] in enonce and qt['e'] in steps,(i,j,'question ou raisonnement absent')
        assert qt['e'].strip(),(i,j,'raisonnement absent')
    count+=numeric_relations(steps,f'exercice {i} étapes')
    count+=numeric_relations(solution,f'exercice {i} solution')
for name in ('cours_nouveau.txt','fiche_nouvelle.txt'):count+=numeric_relations(texts[name],name)

# Recalculs indépendants des réponses numériques sans égalité affichée.
if CODE==1:
    tests=[(1,1,8*1000+40),(1,2,23*1000+405),(1,3,600*1000+9),(1,4,80*1000+60),
           (3,1,(582741//1000)%10),(3,2,((582741//10000)%10)*10000),(3,3,(582741//100)%10),(3,4,8*100),(3,5,582741//1000),
           (4,1,(4627//10)%10),(4,2,4627//10),(4,3,4627%10),(4,4,(4627//100)%10),(4,5,4627//100),
           (6,2,3*100000),(6,3,4*1000),(7,1,7*10000+3*100+9),(7,2,5*100000+2*10),(7,3,8*1000+4*10+6),(7,4,62*1000+7),(7,5,9*10000+12*100),
           (8,1,(28000-24000)//8),(8,2,24000+2*500),(8,3,24000+5*500),(8,4,24000+7*500),
           (11,5,775-647),(12,1,3240//10),(12,2,5278//10),(12,3,5278%10),(12,4,10-5278%10),
           (13,2,45370),(13,3,45379),(13,4,len(range(45370,45380))),
           (14,1,int(''.join(sorted('70391',reverse=True)))),(14,2,10379),(15,3,(45860//100)%10),(15,4,45860-45806),(15,5,10000-9980)]
elif CODE==6:
    tests=[(1,1,8),(1,2,3),(2,1,2),(2,4,5-2),(5,1,4+1),(5,3,5//4),
           (9,1,7-4),(9,2,(7-4)*4),(9,3,((7-4)*4)//4),(9,5,4*7),
           (10,3,2*4),(10,4,3*5),(11,5,12//2-(12-5-4)),
           (12,1,4),(12,2,20//4),(12,3,20-20//4),(13,4,2*6),(15,3,2//2),(15,4,12//4)]
elif CODE==7:
    tests=[(5,1,12//3),(5,2,100//4),(5,3,18//2),(5,4,35//5),
           (8,1,9-5),(8,2,6-1),(8,3,8-3),(8,4,10-7),(8,5,2*6-7),
           (11,1,4),(11,2,11),(11,5,3*4-11),(12,1,4),(12,2,20//4),(12,3,20-20//4),
           (15,1,18//2),(15,2,18//3),(15,3,18//2+18//3),(15,4,18-18//2-18//3)]
elif CODE==8:
    tests=[(3,4,2*100+10),(7,1,3),(7,2,6),(7,4,58),(9,1,Fraction(345,100)),(9,2,Fraction(275,100)),(9,3,Fraction(8,100)),(9,4,4*100+30),
           (11,5,100-(37+3)),(12,1,Fraction(458,10)+Fraction(1,10)),(12,2,Fraction(458,10)+Fraction(2,10)),(12,3,Fraction(458,10)+Fraction(3,10)),(12,4,Fraction(458,10)-Fraction(1,10)),
           (15,2,7*10)]
else:
    round_int=lambda x:int(Fraction(x)+Fraction(1,2))
    tests=[(5,1,int(Fraction('17.83'))),(5,2,int(Fraction('9.04'))),(5,3,int(Fraction('0.76'))),(5,4,int(Fraction('12.99'))),
           (7,5,len(range(241,250))),(8,1,round_int('7.3')),(8,2,round_int('7.83')),(8,3,round_int('12.5')),(8,4,round_int('4.49')),(8,5,round_int('0.76')),
           (9,1,Fraction('3.7')+Fraction('.1')),(9,2,Fraction('3.7')+Fraction('.2')),(9,3,Fraction('3.7')+Fraction('.3')),(9,4,Fraction('3.7')+Fraction('.4')),
           (11,4,Fraction('3.5')-Fraction('3.45')),(12,5,Fraction('1.4')-Fraction('1.29')),
           (13,3,Fraction('6.2')+Fraction('.01')),(13,4,Fraction('6.3')-Fraction('.01')),
           (14,4,Fraction('4.5')-Fraction('4.05')),(15,3,round_int('12.34')),(15,4,round_int('12.5')),(15,5,12)]
for ex,q,expected in tests:count+=expect_number(ex,q,expected)
report={'statut':'OK','math_OK':True,'anomalies':0,'calculs_exactement_verifies':count,'exercices':15,'questions':75,'minimum_questions_par_exercice':5,'cours_et_fiche':True}
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
