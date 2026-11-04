# -*- coding: utf-8 -*-
"""Installe un vérificateur mathématique indépendant dans chaque notion du lot."""
from rediger_lot import ROOT,SLUGS,write,jwrite
import hashlib,json
COURSE_CHECKS=[
 [('1000*1000',1000000),('7*1000000+8*1000+30',7008030),('206*1000000+45*1000+18',206045018),('200000000+6000000+40000+5000+10+8',206045018),('206045018//10000%10',4),('206045018//1000',206045),('52406//1000%10',2),('52406//1000',52),('42907105<42970015',True),('6000000<6472850<6500000<7000000',True),('(4000000-3000000)//5',200000),('3000000+3*200000',3600000)],
 [('6*4',24),('5*7',35),('5*7+2',37),('270%2==0 and 270%5==0 and 270%10==0',True),('275%5==0 and 275%2!=0 and 275%10!=0',True),('[a*b for a,b in [(1,24),(2,12),(3,8),(4,6)]]',[24,24,24,24]),('[d for d in range(1,25) if 24%d==0]',[1,2,3,4,6,8,12,24]),('8*9',72),('[d for d in range(1,19) if 12%d==0 and 18%d==0]',[1,2,3,6]),('[n for n in range(1,31) if n%4==0 and n%6==0]',[12,24])],
 [('Fraction(5,8)==5*Fraction(1,8)',True),('Fraction(8,8)',1),('Fraction(16,8)',2),('19==3*6+1',True),('Fraction(19,6)==3+Fraction(1,6)',True),('2+Fraction(5,6)==Fraction(17,6)',True),('4<Fraction(23,5)<5',True),('Fraction(24,6)',4),('3*6+1',19)],
 [('Fraction(3,4)==Fraction(6,8)==Fraction(9,12)',True),('Fraction(5,8)<Fraction(7,8)',True),('Fraction(3,5)>Fraction(3,8)',True),('Fraction(7,8)<1<Fraction(9,8)',True),('Fraction(3,4)==Fraction(15,20)',True),('Fraction(7,10)==Fraction(14,20)',True),('Fraction(3,4)>Fraction(7,10)',True),('Fraction(3,8)+Fraction(2,8)==Fraction(5,8)',True),('Fraction(7,8)-Fraction(3,8)==Fraction(1,2)',True),('Fraction(1,2)+Fraction(3,8)==Fraction(7,8)',True),('Fraction(5,6)-Fraction(1,12)==Fraction(9,12)',True)],
 [('40//5',8),('8*3',24),('100//4*3',75),('500//10*3',150),('40-24',16),('40*Fraction(2,5)',16),('20*Fraction(1,2)',10),('36*Fraction(1,3)',12),('3*Fraction(5,4)==Fraction(15,4)==3+Fraction(3,4)',True)],
 [('Fraction(10,10)==Fraction(100,100)==Fraction(1000,1000)==1',True),('Fraction(1,10)==Fraction(10,100)==Fraction(100,1000)',True),('Fraction(1,100)==Fraction(10,1000)',True),('Fraction(4207,1000)==4+Fraction(207,1000)==4+Fraction(2,10)+Fraction(7,1000)',True),('Fraction(35,10)==Fraction(350,100)==Fraction(3500,1000)',True),('Fraction(58,10)>Fraction(5795,1000)>Fraction(579,100)',True),('4<Fraction(4207,1000)<5',True),('Fraction(42,10)<Fraction(4207,1000)<Fraction(43,10)',True),('(4300-4200)//10',10),('4200+3*10',4230),('(7682+500)//1000',8),('(7500+500)//1000',8),('(12499+500)//1000',12),('(12501+500)//1000',13)]
]
SCRIPT=r'''# -*- coding: utf-8 -*-
"""Vérifie exactement tous les calculs enregistrés, les résultats et les sources finales."""
from pathlib import Path
from fractions import Fraction
import json,hashlib,re
P=Path(__file__).resolve().parent
def norm(v):
    if isinstance(v,Fraction):return v.numerator if v.denominator==1 else [v.numerator,v.denominator]
    if isinstance(v,(tuple,list)):return [norm(x) for x in v]
    return v
def calculate(expr):
    env={'__builtins__':{},'Fraction':Fraction,'range':range,'sorted':sorted,'set':set,'list':list,'min':min,'max':max,'len':len,'sum':sum,'int':int,'str':str}
    return norm(eval(expr,env,env))
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
    while '\\frac' in s:
        i=s.index('\\frac');a,j=operand(s,i+5);b,k=operand(s,j)
        s=s[:i]+'(('+convert(a)+')/('+convert(b)+'))'+s[k:]
    for a,b in [('{,}','.'),('\\,',''),('\\times','*'),('\\div','/'),('\\ne','!='),('\\le','<='),('\\ge','>='),('\\quad',''),('&','')]:s=s.replace(a,b)
    s=s.replace('{','').replace('}','')
    return s.strip()
def literal_checks(text,origin):
    count=0
    for hit in re.finditer(r'\$\$(.*?)\$\$|\$(.*?)\$',text,re.S):
        math=hit[1] if hit[1] is not None else hit[2]
        math=re.sub(r'\\(?:begin|end)\{(?:aligned|gathered)\}','',math)
        chains=[];chain=''
        for row in math.split('\\\\'):
            if re.match(r'\s*&\s*(?:=|\\quad)',row):chain+=row
            else:
                if chain:chains.append(chain)
                chain=row
        if chain:chains.append(chain)
        for chain in chains:
            try:expr=' '.join(convert(chain).split())
            except (IndexError,ValueError):continue
            if not re.search('[=<>]',expr):continue
            if re.search(r'[^0-9\s.()+*/=<>!\-]',expr):continue
            expr=re.sub(r'(?<![<>=!])=(?!=)','==',expr)
            expr=re.sub(r'\d+(?:\.\d+)?',lambda m:"Fraction('"+m[0]+"')",expr)
            assert eval(expr,{'__builtins__':{},'Fraction':Fraction}),('Égalité ou comparaison affichée fausse',origin,chain)
            count+=1
    return count
manifest=json.loads((P/'verification_questions.json').read_text(encoding='utf-8'))
checks=json.loads((P/'verification_cours.json').read_text(encoding='utf-8'))
count=0
for ex in manifest:
    assert ex['id'].startswith('nouveau-')
    for k,q in enumerate(ex['questions'],1):
        for expr,expected in q['check']:
            assert calculate(expr)==expected,(ex['id'],k,expr,calculate(expr),expected)
            count+=1
        count+=literal_checks(q['e'],ex['id']+' étapes '+str(k))
        count+=literal_checks(q['r'],ex['id']+' résultat '+str(k))
for expr,expected in checks:
    assert calculate(expr)==expected,(expr,calculate(expr),expected)
    count+=1
for name,expected in json.loads((P/'empreintes_finales.json').read_text(encoding='utf-8')).items():
    data=(P/name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==expected,('Texte modifié après contrôle',name)
    txt=data.decode('utf-8')
    assert not any(ord(c)<32 and c not in '\n\r\t' for c in txt),('Caractère de contrôle',name)
    assert '\t' not in txt,('Tabulation suspecte dans une formule',name)
    if name!='exercices.txt':count+=literal_checks(txt,name)
extext=(P/'exercices.txt').read_text(encoding='utf-8')
for ex in manifest:
    block=next(b for b in extext.split('\n===\n') if f"Id: {ex['id']}\n" in b)
    assert len(re.findall(r'^## Question ',block,re.M))==len(ex['questions'])
    for q in ex['questions']:
        assert q['r'] in block,('Résultat absent',ex['id'],q['r'])
report={'statut':'OK','math_OK':True,'anomalies':0,'calculs_exactement_verifies':count,'exercices':len(manifest),'questions':sum(len(e['questions']) for e in manifest),'cours_et_fiche':True}
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
'''

def main():
    for idx,slug in enumerate(SLUGS):
        p=ROOT/slug
        jwrite(p/'verification_cours.json',COURSE_CHECKS[idx])
        jwrite(p/'empreintes_finales.json',{name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']})
        write(p/'verif_math.py',SCRIPT)
if __name__=='__main__':main()
