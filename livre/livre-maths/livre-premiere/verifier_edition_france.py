"""Contrôles des 14 défis, 24 automatismes et 4 problèmes des sujets originaux."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json,math,re,hashlib
import sympy as S
from edition_france_contenu import DEFIS
from edition_france_sujets import SUJETS
from edition_france_figures import FIGURES,frac

R=Path(__file__).resolve().parent
revision_audit=json.loads((R/'revision-audit-20261021.json').read_text(encoding='utf-8'))
(R/'build').mkdir(exist_ok=True)
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
def eq(name,a,b):check(name,S.simplify(a-b)==0)
x,m,a,k,t,r=S.symbols('x m a k t r',real=True)
manifest=json.loads((R/'edition-france-manifeste.json').read_text(encoding='utf-8'))
check('14 défis numérotés', [d['numero'] for d in DEFIS]==list(range(1,15)))
check('224 exercices',manifest['base_exercices']+len(DEFIS)==224)
check('Deux sujets, 24 automatismes et 4 problèmes',len(SUJETS)==2 and sum(len(s['auto']) for s in SUJETS)==24 and sum(len(s['problemes']) for s in SUJETS)==4)
for d in DEFIS:
    check(f'D{d["numero"]:02} : énoncé, indices et corrigé',bool(d['enonce']) and len(d['indices'])==2 and len(d['corrige'])>=1)
    for text in [d['enonce'],*d['corrige'],*d['indices']]:
        check(f'D{d["numero"]:02} : caractères et mathématiques',not any(ord(c)<32 and c not in '\n\r\t' for c in text))
        clean=re.sub(r'\\begin\{python\}.*?\\end\{python\}','',text,flags=re.S)
        clean=re.sub(r'\\begin\{align\*?\}.*?\\end\{align\*?\}','',clean,flags=re.S)
        while r'\res{' in clean:
            start=clean.index(r'\res{');end=start+5;depth=1
            while depth:
                if clean[end]=='{':depth+=1
                elif clean[end]=='}':depth-=1
                end+=1
            clean=clean[:start]+clean[end:]
        clean=re.sub(r'\$[^$]*\$|\\\[.*?\\\]','',clean,flags=re.S)
        check(f'D{d["numero"]:02} : indices en mode mathématique','_' not in clean and '^' not in clean)
for key,body in FIGURES.items():
    check(key+' : fichier fidèle', (R/'figures'/f'{key}.tex').read_text(encoding='utf-8')==body)
# Révisions successives et tracées : 21 octobre (audit du code), 23 octobre (audit de conformité).
revisions=[revision_audit]+[json.loads((R/n).read_text(encoding='utf-8')) for n in ('revision-audit-20261023.json',)]
for folder in ('chapitres','corriges'):
    for p in (R/folder).glob('*.tex'):
        old=R/'build/edition-france-original'/folder/p.name
        if old.exists():
            nom=folder+'/'+p.name
            chaine=[rev['fichiers_modifies'][nom] for rev in revisions if nom in rev['fichiers_modifies']]
            if chaine:
                etat=hashlib.sha256(old.read_bytes()).hexdigest()
                for modification in chaine:
                    check(nom+' : révision enchaînée',modification['avant']==etat)
                    etat=modification['apres']
                check(nom+' : revision demandee et tracee',hashlib.sha256(p.read_bytes()).hexdigest()==etat)
            else:
                check(nom+' : base relue préservée',p.read_bytes()==old.read_bytes())

P=x*x-2*m*x+m
eq('D01 discriminant',S.discriminant(P,x),4*m*(m-1))
for v in [-2,0,S.Rational(1,2),1,S.Rational(11,10),S.Rational(6,5),S.Rational(4,3),S.Rational(3,2),2,3]:
    roots=S.solve(P.subs(m,v),x)
    good=len(roots)==2 and all(z.is_real and 0<z<2 for z in roots)
    check('D01 discussion m='+str(v),bool(good)==bool(1<v<S.Rational(4,3)))

q=S.Rational(4,5)
u=lambda n:300*(1-q**n)
Av=lambda n:sum(u(j) for j in range(n))/n
eq('D02 relation affine',q*(x+300)+60-300,q*x)
for n in (1,2,8,24,25):eq('D02 somme n='+str(n),Av(n),300-S.Rational(1500,n)*(1-q**n))
check('D02 premier rang exact',all(Av(n)<240 for n in range(1,25)) and Av(25)>=240)

f=x**3-3*x;g=-2*t**3+3*t*t-3
eq('D03 équation tangente',S.diff(f,x).subs(x,t)*(x-t)+f.subs(x,t),(3*t*t-3)*x-2*t**3)
eq('D03 dérivée de g',S.diff(g,t),6*t*(1-t))
for b,count in [(-8,0),(-7,1),(-5,1),(-3,2),(S.Rational(-5,2),3),(-2,2),(0,1),(2,1),(3,0)]:
    roots=set(S.real_roots(g-b));actual=sum(bool(-1<=z<=2) for z in roots)
    check('D03 nombre de tangentes b='+str(b),actual==count)
eq('D03 factorisation',4*t**3-6*t*t+1,(2*t-1)*(2*t*t-2*t-1))
for v in [(1-S.sqrt(3))/2,S.Rational(1,2),(1+S.sqrt(3))/2]:
    eq('D03 point imposé t='+str(v),g.subs(t,v),S.Rational(-5,2))

h=10-(2+S.pi)*r/2;area=2*r*h+S.pi*r*r/2;opt=20/(4+S.pi)
eq('D04 contour',2*h+(2+S.pi)*r,20)
eq('D04 aire',area,20*r-(2+S.pi/2)*r*r)
eq('D04 stationnarité',S.diff(area,r).subs(r,opt),0)
eq('D04 hauteur optimale',h.subs(r,opt),opt)
eq('D04 aire maximale',area.subs(r,opt),200/(4+S.pi))
check('D04 domaine',bool(0<opt<20/(2+S.pi)))

eq('D05 inégalité fondamentale, dérivée',S.diff(S.exp(x)-1-x,x),S.exp(x)-1)
outside={10:('1.62889','1.67019'),100:('1.64666','1.65080'),1000:('1.64851','1.64893')}
target=S.exp(S.Rational(1,2)).evalf(60)
for n in (1,10,100,1000):
    lo=(1+S.Rational(1,2*n))**n;hi=(1-S.Rational(1,2*n))**(-n)
    check('D05 encadrement exact n='+str(n),lo.evalf(60)<target<hi.evalf(60))
    if n in outside:
        l,h=map(S.Rational,outside[n]);check('D05 arrondis extérieurs n='+str(n),l<=lo and hi<=h)

z=S.sqrt(2-k*k);xx=(k+z)/2;yy=(k-z)/2
eq('D06 somme',xx+yy,k);eq('D06 cercle',xx*xx+yy*yy,1)
for value,angles in [(0,[3*S.pi/4,7*S.pi/4]),(1,[0,S.pi/2]),(S.sqrt(2),[S.pi/4])]:
    for angle in angles:eq('D06 angle '+str(angle),S.cos(angle)+S.sin(angle),value)

xx=6-k/4;yy2=4-xx*xx
eq('D07 somme pondérée',8+4*x+2*(8-4*x),24-4*x)
for value,count in [(15,0),(16,1),(20,2),(24,2),(32,1),(33,0)]:
    y2=yy2.subs(k,value);actual=2 if y2>0 else 1 if y2==0 else 0
    check('D07 intersections k='+str(value),actual==count)
eq('D07 cas isocèle',xx.subs(k,24),0)

circle=x*x+r*r-4*x-2*m*r
eq('D08 carrés',circle,(x-2)**2+(r-m)**2-(4+m*m))
pol=circle.subs(r,6-x)
eq('D08 discriminant',S.discriminant(pol,x),4*(m*m+8*m-8))
hx=4-m/2;hy=2+m/2
eq('D08 appartenance à d',hx+hy,6)
for mv in [-4-2*S.sqrt(6),-4+2*S.sqrt(6)]:
    eq('D08 rayon et distance '+str(mv),((hx-2)**2+(hy-m)**2-4-m*m).subs(m,mv),0)

paths={}
for state,first,second in product(range(2),repeat=3):
    p=Q(9,10) if state==0 else Q(1,5);prior=Q(1,10) if state==0 else Q(9,10)
    mass=prior*(p if first==0 else 1-p)*(p if second==0 else 1-p)
    paths[state,first,second]=mass
    check('D09 feuille '+str((state,first,second)),('P='+frac(mass)) in FIGURES['fr-d09'])
check('D09 totalité',sum(paths.values())==1)
both=sum(v for (s,a,b),v in paths.items() if a==0 and b==0)
one=sum(v for (s,a,b),v in paths.items() if a==0)
check('D09 indépendance globale absente',both==Q(117,1000) and one==Q(27,100) and both!=one*one)
check('D09 conditionnement simple',sum(v for (s,a,b),v in paths.items() if s==0 and a==0)/one==Q(1,3))
check('D09 conditionnement double',paths[0,0,0]/both==Q(9,13))
errU=[sum(v for (s,a,b),v in paths.items() if s==1 and (a==0 or b==0)),paths[0,1,1]]
errB=[paths[1,0,0],sum(v for (s,a,b),v in paths.items() if s==0 and (a==1 or b==1))]
check('D09 erreurs et seuil de coût',errU==[Q(324,1000),Q(1,1000)] and errB==[Q(36,1000),Q(19,1000)] and (errU[0]-errB[0])/(errB[1]-errU[1])==16)

values=[2*a,2-a,6];prob=[S.Rational(1,4),S.Rational(1,2),S.Rational(1,4)]
mu=sum(v*p for v,p in zip(values,prob));var=sum((v-mu)**2*p for v,p in zip(values,prob))
eq('D10 moyenne fixe',mu,S.Rational(5,2));eq('D10 variance',var,3*a*a/2-2*a+S.Rational(19,4))
eq('D10 forme canonique',var,S.Rational(3,2)*(a-S.Rational(2,3))**2+S.Rational(49,12))
for av,expected in [(0,Q(1,4)),(S.Rational(2,3),Q(1,4)),(S.Rational(5,4),Q(1,4)),(2,Q(1,2))]:
    check('D10 gain strict a='+str(av),sum(p for v,p in zip(values,prob) if (S.sympify(v)-S.Rational(5,2)).subs(a,av)>0)==expected)
eq('D10 perte quadratique',sum((v-r)**2*p for v,p in zip(values,prob)),var+(r-S.Rational(5,2))**2)

def stats(vals):
    mean=sum(map(S.Rational,vals))/len(vals)
    return mean,sum((S.Rational(v)-mean)**2 for v in vals)/len(vals)
check('D11 exemple',stats([0,2])==(1,1) and stats([8,10])==(9,1) and stats([0,2,8,10])==(5,17))
for A,B in [([0,2],[8,10]),([1,2,5],[9,11]),([-1,1],[99,101])]:
    ma,va=stats(A);mb,vb=stats(B);mm,vv=stats(A+B);p=S.Rational(len(A),len(A)+len(B))
    eq('D11 moyenne pondérée '+str(A),mm,p*ma+(1-p)*mb)
    eq('D11 décomposition '+str(A),vv,p*va+(1-p)*vb+p*(1-p)*(ma-mb)**2)

fn=x**3+x-1
eq('D12 signe gauche exact',fn.subs(x,S.Rational(698,1024)),S.Rational(-1767384,1073741824))
eq('D12 signe droit exact',fn.subs(x,S.Rational(699,1024)),S.Rational(744899,1073741824))
check('D12 précision minimale',Q(1,512)>Q(1,1000)>=Q(1,1024) and Q(1,2048)<Q(5,10000))
for mv in [-2,0,S.Rational(1,4),S.Rational(1,2),1,2]:
    candidates=[P.subs({m:mv,x:v}) for v in [0,1]+([mv] if 0<=mv<=1 else [])]
    expected=mv if mv<0 else mv*(1-mv) if mv<=1 else 1-mv
    check('D13 minimum sur segment m='+str(mv),min(candidates)==expected)
eq('D13 valeur commune',P.subs(x,S.Rational(1,2)),S.Rational(1,4))

p=S.exp(-x)/5;g=12-2*x-4*S.exp(-x)
eq('D14 espérance',(12-2*x)*(1-p)+(-8-2*x)*p,g)
eq('D14 variance',400*p*(1-p),80*S.exp(-x)-16*S.exp(-2*x))
eq('D14 dérivée de variance',S.diff(400*p*(1-p),x),16*S.exp(-x)*(2*S.exp(-x)-5))
eq('D14 variance optimale',(400*p*(1-p)).subs(x,S.log(2)),36)
check('D14 deux articles',1-Q(9,10)**2==Q(19,100))

# Exécuter les programmes réellement imprimés dans les nouvelles corrections.
scopes={};count=0
for d in DEFIS:
    for body in d['corrige']:
        for code in re.findall(r'\\begin\{python\}\s*(.*?)\\end\{python\}',body,re.S):
            scope={};exec(compile(code,f'defi-{d["numero"]}','exec'),scope);scopes[d['numero']]=scope;count+=1
check('D02 programme de moyenne',scopes[2]['seuil_moyenne']()==25)
for n in (1,10,100,1000):
    l,h=scopes[5]['bornes_exponentielle'](n)
    check('D05 programme n='+str(n),l<math.sqrt(math.e)<h)
for n in (0,1,4,10,20):
    l,h=scopes[12]['encadrer_racine'](n)
    check('D12 programme n='+str(n),h-l==2**(-n) and l**3+l-1<=0<=h**3+h-1)
    l,h=scopes[14]['encadrer_reglage'](n)
    check('D14 programme n='+str(n),h-l==2**(-n) and l<=math.log(2)<=h)

f=x**3-6*x*x+9*x+2
eq('Sujet A1 dérivée',S.diff(f,x),3*(x-1)*(x-3))
check('Sujet A1 valeurs', [f.subs(x,j) for j in (0,1,3,4)]==[2,6,2,6])
eq('Sujet A1 tangente',S.diff(f,x).subs(x,2)*(x-2)+f.subs(x,2),-3*x+10)
eq('Sujet A1 position relative',f-(-3*x+10),(x-2)**3)
pd=Q(3,5)*Q(1,20)+Q(2,5)*Q(1,10)
check('Sujet A2 probabilités',pd==Q(7,100) and Q(2,5)*Q(1,10)/pd==Q(4,7))
mu=12*(1-pd)-8*pd;var=144*(1-pd)+64*pd-mu*mu
check('Sujet A2 loi, moments et répétition',mu==Q(53,5) and var==Q(651,25) and 1-(1-pd)**2==Q(1351,10000))
eq('Sujet B1 relation affine',S.Rational(3,4)*(x+40)+10-40,S.Rational(3,4)*x)
check('Sujet B1 premier seuil exact',Q(3,4)**4>Q(1,4)>=Q(3,4)**5)
code=re.search(r'\\begin\{python\}\s*(.*?)\\end\{python\}',SUJETS[1]['problemes'][0]['corrige'],re.S)[1]
scope={};exec(compile(code,'sujet-B-1','exec'),scope);count+=1
check('Sujet B1 programme',scope['premier_rang']()==5)
H=(S.Rational(23,5),S.Rational(24,5))
eq('Sujet B2 médiatrice AC',(x-1)**2+(r-3)**2-x*x-r*r,-2*x-6*r+10)
eq('Sujet B2 H sur tangente',-H[0]+2*H[1]-5,0)
eq('Sujet B2 projection perpendiculaire',2*(H[0]-5)+(H[1]-4),0)
eq('Sujet B2 distance',(H[0]-5)**2+(H[1]-4)**2,S.Rational(4,5))

# Automatismes : réponses recalculées, puis comparées aux réponses imprimées dans les corrigés.
V,rr,hh=S.symbols('V r h',positive=True)
fA=(x*x-2*x-1)/2;gB=-(x+1)*(x-3)/2
autoA=[60*S.Rational(115,100),75/S.Rational(125,100),(1/S.Rational(4,5)-1)*100,(2-S.sqrt(3))*(2+S.sqrt(3)),
    set(S.solve((2*x-1)*(x+3),x)),S.solve_univariate_inequality(-3*x+6>0,x).as_set(),
    S.solve_univariate_inequality((x-1)*(x+4)<0,x).as_set(),S.Rational(-5-3,3-(-1)),
    S.Rational(2,5)*S.Rational(1,4),sorted([1,2,2,5,10])[2],
    S.solve_univariate_inequality(fA<=1,x,relational=False).intersect(S.Interval(-2,4)),
    S.Rational(2-3,2-0)*x+3]
expectedA=[69,60,25,1,{-3,S.Rational(1,2)},S.Interval.open(-S.oo,2),S.Interval.open(-4,1),-2,S.Rational(1,10),2,
    S.Interval(-1,3),-x/2+3]
for i,(v,e) in enumerate(zip(autoA,expectedA),1):check('Automatisme A'+str(i),v==e if not isinstance(v,S.Expr) else S.simplify(v-e)==0)
check('Automatisme A11 : lecture aux nœuds',[fA.subs(x,k) for k in (-2,-1,1,3,4)]==[S.Rational(7,2),1,-1,1,S.Rational(7,2)])
check('Automatisme A12 : points lus sur d',[(-x/2+3).subs(x,k) for k in (0,2,4,6)]==[3,2,1,0])
autoB=[S.Rational(3,4)+S.Rational(1,6),S.Rational((2**3)**2,2**4),S.expand((3*x-1)*(3*x+1)),S.Rational(92-80,80),
    S.sqrt(S.Rational(121,100))-1,S.solve(S.Eq(V,S.pi*rr**2*hh),hh)[0],S.Rational(3)+(-2)*(x-0),
    S.Rational(8+2*12+15,4),S.Rational(30,120),(S.Rational(30,200),S.Rational(30,60)),
    S.solve_univariate_inequality(gB>0,x,relational=False),(sorted([9,12,15])[1],15-9)]
expectedB=[S.Rational(11,12),4,9*x*x-1,S.Rational(15,100),S.Rational(1,10),V/(S.pi*rr**2),3-2*x,S.Rational(47,4),
    S.Rational(1,4),(S.Rational(3,20),S.Rational(1,2)),S.Interval.open(-1,3),(12,6)]
for i,(v,e) in enumerate(zip(autoB,expectedB),1):check('Automatisme B'+str(i),S.simplify(v-e)==0 if isinstance(v,S.Expr) and not isinstance(v,S.Set) else v==e)
check('Automatisme B9 : tableau croisé cohérent',30+90==120 and 30+50==80 and 30+30==60 and 90+50==140 and 120+80==60+140==200)
check('Automatisme B11 : lecture aux nœuds',[gB.subs(x,k) for k in (-2,-1,1,3,4)]==[S.Rational(-5,2),0,2,0,S.Rational(-5,2)])
# Les valeurs encadrées du corrigé correspondent aux calculs ci-dessus.
printed={s['lettre']:[a for q,a in s['auto']] for s in SUJETS}
for token,i in [('69',0),('60',1),('25',2),('{1}',3),(r'\{-3\,;\,1/2\}',4),('x<2',5),('{]}-4;1[',6),('{-2}',7),('0{,}1',8),('{2}',9),('[-1;3]',10),(r'-\tfrac12x+3',11)]:
    check(f'Automatisme A{i+1} : réponse imprimée',token in printed['A'][i])
for token,i in [(r'\dfrac{11}{12}',0),('{4}',1),('(3x-1)(3x+1)',2),('15',3),('t=10',4),(r'\dfrac{V}{\pi r^2}',5),('y=-2x+3',6),('11{,}75',7),(r'\dfrac14',8),(r'\dfrac3{20}',9),('{]}-1;3[',10),('{6}',11)]:
    check(f'Automatisme B{i+1} : réponse imprimée',token in printed['B'][i])
check('Automatismes : aucune notion propre aux chapitres de spécialité',all(not re.search(r"\\cos|\\sin|e\^\{|\\vect|\\code|dériv|tangente|suite|exponentielle",q) for s in SUJETS for q,a in s['auto']))
check('Automatismes : figures des lectures graphiques',[s.get('figures_auto') for s in SUJETS]==[['fr-sa-auto'],['fr-sb-auto']])

report=dict(exercices_base=210,defis_controles=14,sujets_controles=2,automatismes_controles=24,
            problemes_sujets_controles=4,nouveaux_programmes_executes=count,
            nouveaux_visuels=len(FIGURES),insertions_visuelles=len(manifest['figures']),
            controles_reussis=len(checks),controles=checks,
            portee='Contrôles exacts ou symboliques, cas frontières et exécution des programmes ; les preuves rédigées restent relues humainement.')
(R/'build/verification-edition-france.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('controles','portee')},indent=2))
