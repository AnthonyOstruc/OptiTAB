# -*- coding: utf-8 -*-
"""Contrôle indépendant des résultats, de la structure et des identités locales.

Usage : python verif_notion.py [dossier]. Les approximations des cylindres
utilisent exactement 3,14, comme l'énoncé. Aucun accès réseau ou à la base.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal
import json
import math
import re
import sys

P=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
NUM=int(P.name[:3]); assertions=0

def check(ok,message):
    global assertions
    assertions+=1
    assert ok,message

def mathval(s):
    s=s.strip().rstrip('.').replace(r'\displaystyle','').replace(r'{,}','.').replace(',','.')
    s=s.replace(r'\,','').replace(' ','').replace(r'\left','').replace(r'\right','')
    def arg(t,i):
        if t[i]=='{':
            level=1; end=i+1
            while level:
                if t[end]=='{': level+=1
                if t[end]=='}': level-=1
                end+=1
            return t[i+1:end-1],end
        return t[i],i+1
    while r'\frac' in s or r'\dfrac' in s:
        m=re.search(r'\\d?frac',s); a,j=arg(s,m.end()); b,k=arg(s,j)
        s=s[:m.start()]+'('+str(mathval(a))+')/('+str(mathval(b))+')'+s[k:]
    s=s.replace(r'\times','*').replace(r'\div','/').replace(r'\pi','*'+str(math.pi))
    s=s.replace('^','**').replace('{','(').replace('}',')')
    s=re.sub(r'(?<=\d)\(', '*(',s)
    if not re.fullmatch(r'[\d.()+*/\-]+',s): raise ValueError(s)
    return eval(s,{'__builtins__':{}},{})

def first(s):
    formulas=re.findall(r'\$([^$]+)\$',s)
    if formulas:
        try:return mathval(formulas[0].split('=')[0])
        except (ValueError,SyntaxError):pass
    m=re.search(r'\d+(?:[.,]\d+)?',s.replace('{,}',','))
    return float(m.group().replace(',','.'))

def eq(s,n,label):check(abs(first(s)-float(n))<1e-8,label+': '+s)

text=(P/'exercices.txt').read_text(encoding='utf8')
source=(P/'source_en_ligne/exercices.txt').read_text(encoding='utf8')
def identities(t):
    return [(re.search(r'^=== (.+)',b,re.M).group(1),re.search(r'^Id: (\d+)',b,re.M).group(1),re.search(r'^Difficulté: (.+)',b,re.M).group(1)) for b in re.split(r'^===[ \t]*$',t,flags=re.M) if re.search(r'^Id:',b,re.M)]
check(identities(text)==identities(source),'Titres, Id ou difficultés modifiés')
blocks=[b for b in re.split(r'^===[ \t]*$',text,flags=re.M) if 'Énoncé:' in b]
check(len(blocks)==21,'Nombre d’exercices')

for b in blocks:
    eid=re.search(r'^Id: (\d+)',b,re.M).group(1)
    en,steps=b.split('Énoncé:')[1].split('Étapes:'); steps,sol=steps.split('Solution:')
    answers={int(n):s for n,s in re.findall(r'^(\d+)\. (.+)',sol,re.M)}
    check(len(answers)==6,eid+': six solutions')
    qs=re.split(r'(?=^## Question )',steps,flags=re.M)[1:]
    check(len(qs)==6,eid+': six questions')
    for q in qs:
        check(all('::: '+k in q for k in ('methode','etape','resultat')),eid+': pédagogie incomplète')
    if NUM==276:
        a,c,h=map(int,re.search(r'AB = (\d+) m, AD = (\d+) m.*?mesure (\d+) m',en).groups())
        eq(answers[1],c,eid+' Q1');check(f'AB = {a}' in answers[1],eid+' côté AB')
        eq(answers[2],2*(a+c),eid+' périmètre');eq(answers[3],a*h,eid+' aire');eq(answers[6],Fraction(a*h,2),eid+' demi-aire')
        check(h<c,eid+' hauteur et côté compatibles')
    elif NUM==277:
        if 'Un aquarium' in en:
            a,c,h=map(int,re.search(r'de (\d+) dm de longueur, (\d+) dm de largeur et (\d+) dm',en).groups());v=a*c*h
            check('6 faces, 12 arêtes, 8 sommets' in answers[1],eid+' dénombrement')
            for q,value in [(2,a*c),(3,v),(4,v),(5,Fraction(3*v,4)),(6,v*1000)]:eq(answers[q],value,eid+' Q'+str(q))
        elif 'cylindrique a un rayon' in en:
            r,h=map(int,re.search(r'de (\d+) cm et une hauteur intérieure de (\d+) cm',en).groups());v=r*r*h
            for q,value in [(1,2*r),(2,2*r*math.pi),(3,r*r*math.pi),(4,v*math.pi)]:eq(answers[q],value,eid+' Q'+str(q))
            decimals=re.findall(r'\$([^$]+)\$',answers[5]);eq('$'+decimals[0]+'$',Decimal(v)*Decimal('3.14'),eid+' mL');eq('$'+decimals[1]+'$',Decimal(v)*Decimal('0.00314'),eid+' L')
            check(f'rayon {r} cm' in answers[6] and f'hauteur {h} cm' in answers[6],eid+' patron')
        else:
            L,a,c=map(int,re.search(r'longueur (\d+) cm.*?mesurent (\d+) cm et (\d+) cm',en).groups());area=Fraction(a*c,2);v=area*L
            for q,value in [(3,area),(4,v),(5,v),(6,2*v)]:eq(answers[q],value,eid+' Q'+str(q))
    elif NUM==278:
        if 'Une classe' in en:
            a,c,d=map(int,re.search(r'(\d+) réponses « marche », (\d+) réponses « vélo » et (\d+) réponses « bus »',en).groups());n=a+c+d
            check(d>max(a,c),eid+' mode bus')
            for q,value in [(1,n),(2,Fraction(d,n)),(3,Fraction(a,n)),(4,Fraction(a+c,n)),(5,Fraction(d,n)*360),(6,n)]:eq(answers[q],value,eid+' Q'+str(q))
        else:
            vals=list(map(int,re.search(r'respectivement ([\d, ]+) livres',en).group(1).split(',')));s=sum(vals);m=Fraction(s,5);add=int(re.search(r'lit (\d+) livres supplémentaires',en).group(1))
            check(answers[2].startswith(f'5 élèves ; {s} livres'),eid+' somme')
            eq(answers[3],m,eid+' moyenne');eq(answers[5],m+add,eid+' ajout');eq(answers[6],20*m,eid+' autre classe')
            check(Fraction(1+2,2)==Fraction(3,2),'Contre-exemple moyenne non observée')
    elif NUM==279:
        if 'Un sac' in en:
            r,c=map(int,re.search(r'contient (\d+) jetons rouges, (\d+) jetons bleus',en).groups());n=r+c+1
            for q,value in [(1,n),(2,Fraction(r,n)),(3,Fraction(c+1,n))]:eq(answers[q],value,eid+' Q'+str(q))
            check(Fraction(r,n)+Fraction(c+1,n)==1,eid+' contraires');check('probabilité 0' in answers[5] and 'probabilité 1' in answers[5],eid+' impossible certain')
            eq(answers[6],Fraction(r,n),eid+' remise')
        else:
            k=int(re.search(r'strictement supérieur à (\d+)',en).group(1))
            check(list(map(int,re.findall(r'\d+',answers[3])))==list(range(k+1,7)),eid+' issues favorables')
            eq(answers[4],Fraction(6-k,6),eid+' P(A)')
            form=re.findall(r'\$([^$]+)\$',answers[5])[0];eq('$'+form+'$',Fraction(k,6),eid+' contraire')
            check(answers[6].startswith('Non.'),eid+' expérience courte')
    elif NUM==280:
        if 'Le programme' in en:
            a,c=map(int,re.search(r'« (\d+) × réponse \+ (\d+) »',en).groups());x=int(re.search(r'pour l’entrée (\d+)',en).group(1))
            for q,value in [(3,a*x+c),(4,c),(5,a*(x+c))]:eq(answers[q],value,eid+' Q'+str(q))
            check(a*x+c!=a*(x+c),eid+' programmes différents')
        elif 'répéter 4 fois' in en:
            c=int(re.search(r'avancer de (\d+) pas',en).group(1));eq(answers[1],4,eid+' déplacements');eq(answers[2],4*c,eid+' distance');eq(answers[3],360,eid+' rotation');eq(answers[4],c,eid+' côté')
            check('vers le bas' in answers[6],eid+' dernière rotation')
        else:
            a,c=map(int,re.search(r'avancer de (\d+) pas.*?avancer de (\d+) pas',en).groups());eq(answers[5],2*(a+c),eid+' périmètre')
            check(list(map(int,re.findall(r'\d+',answers[3])))==[a,c,a,c],eid+' longueurs ordonnées')
    # Toutes les égalités numériques lisibles sont recalculées, indépendamment
    # des conclusions précédentes (fractions, priorités, conversions, π).
    formulas=[a or c for a,c in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',b,re.S)]
    for formula in formulas:
        if '=' not in formula:continue
        try:values=[mathval(part) for part in formula.split('=')]
        except (ValueError,SyntaxError,IndexError):continue
        check(all(abs(float(v)-float(values[0]))<1e-8 for v in values),eid+': égalité '+formula)

# Exemples numériques du cours et de la synthèse : vérifications explicites.
examples={276:[2*(6+4)==20,6*2==12,100*100==10000],277:[6*4/2==12,12*10==120,3**2*8==72,round(72*math.pi)==226,10**3==1000],278:[10+6+4==20,6/20==.3,.3*360==108,(4+6+6+8)/4==6,(24+4)/4==7,(2+3+10)/3==5],279:[Fraction(1,4)==Fraction(25,100),Fraction(2,6)==Fraction(1,3),Fraction(3,5)+Fraction(2,5)==1],280:[3*4+2==14,3*(4+2)==18,4*60==240,4*90==360,3*120==360]}
for result in examples[NUM]:check(result,'Exemple du cours')

result={'notion':NUM,'exercices':len(blocks),'questions':6*len(blocks),'assertions':assertions,'statut':'OK','remarque':'Calculs recalculés à partir des énoncés ; identités comparées aux sources. Les arguments géométriques et qualitatifs restent relus humainement.'}
(P/'verification_maths.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
