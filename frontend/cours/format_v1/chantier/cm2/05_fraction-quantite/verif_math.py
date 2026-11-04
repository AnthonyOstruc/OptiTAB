# -*- coding: utf-8 -*-
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
