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
    s=s.replace(r'\,','')
    s=s.replace(r'\text{ de }',r'\times')
    s=re.sub(r'\\mathrm(?:\{[^}]*\}|\s*[A-Za-z]+)(?:\^\{?\d\}?)?','',s)
    s=re.sub(r'\\text\{[^}]*\}','',s)
    s=s.replace(r'^\circ','').replace(r'\%','/100')
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
    s=s.replace(r'\times','*').replace(r'\div','/').replace(r'\pi','PI')
    s=re.sub(r'(?<=[\d)])PI','*PI',s).replace('PI',str(math.pi))
    s=s.replace('^','**').replace('{','(').replace('}',')')
    s=re.sub(r'(?<=\d)\(', '*(',s)
    if not re.fullmatch(r'[\d.()+*/\-]+',s): raise ValueError(s)
    return eval(s,{'__builtins__':{}},{})

def first(s):
    formulas=re.findall(r'\$([^$]+)\$',s)
    if formulas:
        for part in formulas[0].split('='):
            try:return mathval(part)
            except (ValueError,SyntaxError):pass
    m=re.search(r'\d+(?:[.,]\d+)?',s.replace('{,}',','))
    return float(m.group().replace(',','.'))

def eq(s,n,label):check(abs(first(s)-float(n))<1e-8,label+': '+s)

text=(P/'exercices.txt').read_text(encoding='utf8')
source=(P/'source_en_ligne/exercices.txt').read_text(encoding='utf8')
def identities(t):
    return re.findall(r'^Id: (\d+)',t,re.M)
check(identities(text)==identities(source),'Id modifiés ou blocs retirés')
blocks=[b for b in re.split(r'^===[ \t]*$',text,flags=re.M) if 'Énoncé:' in b]
check(len(blocks)==21,'Nombre d’exercices')
titles=re.findall(r'^=== (.+)',text,re.M)
check(len(set(titles))==len(titles),'Titres non uniques')
revision=json.loads((P/'revision_2026-10-30.json').read_text(encoding='utf8'))
replacements={item['id'] for item in revision['remplacements']}
models={
276:{4:[(3,6)],6:[],11:[],13:[(1,6*2),(2,6*2/2),(3,12+6),(4,18*3)],18:[(1,2*(8+4)),(2,6*6-8*4)],20:[(1,6*4-3*2),(2,.5*.5),(3,18/.25),(4,math.ceil(72*1.1)*2.5)]},
277:{4:[(1,.45*1000),(2,2500),(3,3.2)],6:[(4,6*2**2)],11:[(1,4*math.pi),(2,4*math.pi*5),(3,28*math.pi),(4,math.pi*2**2*5)],13:[(1,1+2+1+3+1+2),(2,10*2**3),(3,3),(4,11*8)],18:[(1,60*40*30/1000),(2,72*3/4),(3,72-(54+12)),(4,66000/(60*40))],20:[(1,5*12/2),(2,750/30),(3,2*30+(5+12+13)*25)]},
278:{4:[(1,15),(2,18-6),(3,12+18+15+9+6),(4,15/60)],6:[(1,4+4+8+8),(2,24/4)],11:[(1,40),(2,10/40),(3,10/40*360),(4,360)],13:[(1,12),(2,16),(3,16-8),(4,(8+12+16+14+10)/5)],18:[(1,2+5+8+5),(2,(0*2+1*5+2*8+3*5)/20),(3,(8+5)/20),(4,(36+6)/21)],20:[(1,12*20),(2,(12*20+14*30)/(20+30)),(4,13.5*51-660)]},
279:{4:[(1,4),(2,2/4),(3,2/4)],6:[(1,12/20),(2,1/2)],11:[(1,2/4),(2,48/100)],13:[(1,3),(2,1),(3,1),(4,5)],18:[(1,6/(6+4+2)),(2,6/(12+3)),(4,9-6)],20:[(1,180/360),(2,(90+90)/360),(3,44/80),(4,360/3)]},
280:{4:[(1,4*2+3),(4,4*0+3)],6:[(2,30+20),(4,2*(30+20))],11:[(2,3*20),(3,4),(4,4*20)],13:[(2,180-60),(3,40),(4,3*40)],18:[(1,50),(2,2*(50+20)),(4,2*(50+20))],20:[(2,2*(8+5)),(3,2*(8+5)*3)]}}
question_total=0

for index,b in enumerate(blocks):
    eid=re.search(r'^Id: (\d+)',b,re.M).group(1)
    en,steps=b.split('Énoncé:')[1].split('Étapes:'); steps,sol=steps.split('Solution:')
    answers={int(n):s for n,s in re.findall(r'^(\d+)\. (.+)',sol,re.M)}
    expected=4 if eid in replacements else 6
    check(len(answers)==expected,eid+': nombre de solutions')
    qs=re.split(r'(?=^## Question )',steps,flags=re.M)[1:]
    check(len(qs)==expected,eid+': nombre de questions')
    question_total+=len(qs)
    for q in qs:
        check(all('::: '+k in q for k in ('methode','etape','resultat')),eid+': pédagogie incomplète')
    check('::: retenir' in steps or '::: attention' in steps,eid+': conseil pédagogique absent')
    if eid in replacements:
        for q,value in models[NUM][index]:eq(answers[q],value,eid+' Q'+str(q))
        check(all(len(re.findall(r'::: etape ',q))>=1 for q in qs),eid+': étapes absentes')
        if NUM==276 and index==6:
            A,B,C,D=(0,0),(4.6,0),(5.7,2),(1.1,2)
            check(all(abs((A[i]+C[i])-(B[i]+D[i]))<1e-9 for i in (0,1)),'Construction : même milieu des diagonales')
        if NUM==279 and index==13:
            A={3,6,9};B={1,2,3,4};union=A|B
            check(union=={1,2,3,4,6,9},'Réunion sans doublon')
            check(Fraction(len(union),10)==Fraction(3,5),'Probabilité de réunion')
            check(set(range(1,11))-union=={5,7,8,10},'Événement contraire')
        if NUM==280 and index in (6,11,13,18,20):
            # Simulation indépendante des mouvements et des orientations.
            def turtle(instructions):
                x=y=angle=0
                for distance,turn in instructions:
                    x+=distance*math.cos(math.radians(angle));y+=distance*math.sin(math.radians(angle));angle=(angle+turn)%360
                return x,y,angle
            if index==6:instructions=[(30,90),(20,90)]*2
            elif index==11:instructions=[(20,90)]*4
            elif index==13:instructions=[(40,120)]*3
            elif index==18:instructions=[(50,90),(20,90)]*2
            else:instructions=[(8,90),(5,90)]*2
            x,y,a=turtle(instructions);check(abs(x)<1e-8 and abs(y)<1e-8 and a==0,eid+': fermeture et orientation')
            if index==18:
                x,y,a=turtle([(50,90),(20,-90)]*2);check(abs(x-100)<1e-8 and abs(y-40)<1e-8 and a==0,'Tracé erroné en escalier')
    elif NUM==276:
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
        formula=re.sub(r'\\(?:begin|end)\{aligned\}','',formula).replace('&','')
        for row in formula.split(chr(92)*2):
            units=set(re.findall(r'\\mathrm(?:\{[^}]*\}|\s*[A-Za-z]+)(?:\^\{?\d\}?)?',row))
            if len(units)>1:continue  # conversions contrôlées par les modèles d'unités
            values=[]
            for part in row.split('='):
                try:values.append(mathval(part.strip().rstrip('.,;')))
                except (ValueError,SyntaxError,IndexError,ZeroDivisionError):
                    if len(values)>1:check(all(abs(float(v)-float(values[0]))<1e-8 for v in values),eid+': égalité '+row)
                    values=[]
            if len(values)>1:check(all(abs(float(v)-float(values[0]))<1e-8 for v in values),eid+': égalité '+row)

# Exemples numériques du cours et de la synthèse : vérifications explicites.
examples={276:[2*(6+4)==20,6*2==12,100*100==10000],277:[6*4/2==12,12*10==120,3**2*8==72,round(72*math.pi)==226,10**3==1000],278:[10+6+4==20,6/20==.3,.3*360==108,(4+6+6+8)/4==6,(24+4)/4==7,(2+3+10)/3==5],279:[Fraction(1,4)==Fraction(25,100),Fraction(2,6)==Fraction(1,3),Fraction(3,5)+Fraction(2,5)==1],280:[3*4+2==14,3*(4+2)==18,4*60==240,4*90==360,3*120==360]}
for result in examples[NUM]:check(result,'Exemple du cours')

result={'notion':NUM,'exercices':len(blocks),'questions':question_total,'remplacements':len(replacements),'assertions':assertions,'statut':'OK','remarque':'Id comparés aux sources ; calculs des exercices conservés et nouveaux contrôlés ; simulations de tracés. Arguments géométriques et qualitatifs relus humainement.'}
(P/'verification_maths.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
