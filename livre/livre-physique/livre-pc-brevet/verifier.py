"""Contrôles du livre et rendu intégral pour la relecture visuelle."""
from pathlib import Path
import json,re,hashlib,math,sys,tokenize,io
import fitz
from PIL import Image,ImageDraw
from donnees import charger
from brevets import SUJETS
from annexes import CONCORDANCE
from corrections_activites import ACTIVITES
from revision_brevets import CORRIGES, METHODES
from annales_originales import SUJETS as ANN, CALCULS as CALCULS_ANN
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
BUILD=HERE/'build';QA=ROOT/'tmp/pdfs/qa-pc-brevet';QA.mkdir(parents=True,exist_ok=True)
checks=[];calculs=[]
def check(name,value,detail=None):
    checks.append(dict(controle=name,valide=bool(value),detail=detail))
    if not value:print('ECHEC',name,detail)
chs=charger();check('18 chapitres ordonnés',[c.numero for c in chs]==list(range(1,19)))
check('18 investigations corrigées',set(ACTIVITES)==set(range(1,19)))
all_ex=[]
for c in chs:
    check(f'{c.numero} : quatre leçons',len(c.lecons)==4)
    check(f'{c.numero} : quinze exercices',len(c.exercices)==15)
    check(f'{c.numero} : deux schémas de cours',sum(bool(l[2]) for l in c.lecons)==2)
    check(f'{c.numero} : exemple et bilan',bool(c.exemple and c.bilan and c.activite))
    for j,e in enumerate(c.exercices+[c.defi],1):
        ident=f'{c.numero}.{j}' if j<=15 else f'D{c.numero}'
        check(ident+' : questions et réponses',len(e.questions)==len(e.reponses) and all(e.questions) and all(e.reponses))
        all_ex.append((ident,e))
check('Dix sujets blancs ordonnés',[s.numero for s in SUJETS]==list(range(1,11)))
for s in SUJETS:
    check(f'BB{s.numero} : 9 points scientifiques',sum(sum(p.points) for p in s.parties)==9)
    check(f'BB{s.numero} : deux parties indépendantes',len(s.parties)==2 and all(p.exercice.document for p in s.parties))
    check(f'BB{s.numero} : sept questions',sum(len(p.points) for p in s.parties)==7)
    for k,p in enumerate(s.parties,1):
        e=p.exercice
        check(f'BB{s.numero}.{k} : barèmes complets',len(e.questions)==len(e.reponses)==len(p.points) and all('Barème' in a for a in e.reponses))
        all_ex.append((f'BB{s.numero}.{k}',e))
for ident,e in all_ex:
    for val in [e.document,*e.questions,*e.reponses,e.methode]:
        check(ident+' : texte sans échappement corrompu',not any(ord(c)<32 and c!='\n' for c in val))
    for expr,expected in e.calculs:
        got=eval(expr,{'__builtins__':{}})
        ok=math.isclose(got,expected,rel_tol=1e-10,abs_tol=1e-20)
        calculs.append(dict(exercice=ident,expression=expr,obtenu=got,attendu=expected,valide=ok))
        check(ident+' : '+expr,ok)
for expr,expected in CALCULS_ANN:
    got=eval(expr,{'__builtins__':{}},{})
    ok=math.isclose(got,expected,rel_tol=1e-10,abs_tol=1e-12)
    calculs.append(dict(exercice='Sujets 11 à 15',expression=expr,obtenu=got,attendu=expected,valide=ok))
    check('Annales originales : '+expr,ok)
check('Cinq sujets supplémentaires et 45 questions',len(ANN)==5 and sum(len(b.questions) for s in ANN for b in s.blocs)==45)
def atoms(formula):
    out={}
    for a,n in re.findall(r'([A-Z][a-z]?)(\d*)',formula):out[a]=out.get(a,0)+int(n or 1)
    return out
def total(side):
    out={}
    for coeff,formula in side:
        for a,n in atoms(formula).items():out[a]=out.get(a,0)+coeff*n
    return out
for name,left,right in [
('Carbone',[(1,'C'),(1,'O2')],[(1,'CO2')]),
('Eau',[(2,'H2'),(1,'O2')],[(2,'H2O')]),
('Méthane',[(1,'CH4'),(2,'O2')],[(1,'CO2'),(2,'H2O')]),
('Éthanol',[(1,'C2H6O'),(3,'O2')],[(2,'CO2'),(3,'H2O')]),
('Zinc-acide',[(1,'Zn'),(2,'H')],[(1,'Zn'),(1,'H2')]),
('Fer-acide',[(1,'Fe'),(2,'H')],[(1,'Fe'),(1,'H2')]),
('Acide-base',[(1,'H'),(1,'OH')],[(1,'H2O')])]:check('Conservation atomique : '+name,total(left)==total(right))
for name,z,el,charge in [('Na+',11,10,1),('Cl-',17,18,-1),('Cu2+',29,27,2),('Al3+',13,10,3),('Fe3+',26,23,3)]:check('Charge : '+name,z-el==charge)
check('Gravitation : rapport indépendant',math.isclose((6.67e-11*20*30/4**2)/(6.67e-11*20*30/2**2),.25))
check('Énergie cinétique : rapport indépendant',(.5*70*20**2)/(.5*70*10**2)==4)
log=(BUILD/'main.log').read_text(encoding='utf8',errors='replace')
for title,pattern in [('Caractères manquants','Missing character'),('Renvois non définis',r'(?:Reference|Hyper reference).*?undefined|undefined references'),('Labels dupliqués','multiply defined'),('Renvois non stabilisés',r'Rerun to get|Label\(s\) may have changed')]:check('Absence : '+title,not re.search(pattern,log))
over=re.findall(r'Overfull \\[hv]box[^\n]*',log);check('Aucun débordement de boîte',not over,over)
aux=(BUILD/'main.aux').read_text(encoding='utf8')
for c in chs:
    for j in range(1,16):check(f'Liens {c.numero}.{j}',all(f'\\newlabel{{{tag}-{c.numero}-{j}}}' in aux for tag in ['exo','cor']))
    for t,u in [('defi-ex','cor-defi'),('activite','cor-activite')]:check(f'Liens {t} {c.numero}',all(f'\\newlabel{{{tag}-{c.numero}}}' in aux for tag in [t,u]))
for s in SUJETS:check(f'Liens BB{s.numero}',all(f'\\newlabel{{{tag}-{s.numero}}}' in aux for tag in ['bb','cor-bb']))
bad=[];bad_literals=[]
for p in list(HERE.glob('*.py'))+list(HERE.glob('*.tex'))+list((HERE/'chapitres').glob('*.tex'))+list((HERE/'corriges').glob('*.tex')):
    txt=p.read_text(encoding='utf8')
    if any(ord(c)<32 and c not in '\t\r\n' for c in txt):bad.append(p.name)
    if p.suffix=='.py':
        for tok in tokenize.generate_tokens(io.StringIO(txt).readline):
            if tok.type==tokenize.STRING and not re.match(r'(?i)[rubf]*r',tok.string) and re.search(r'(?<!\\)\\(?:unite|textbf|frac|ce\b|Omega|vspace)',tok.string):bad_literals.append([p.name,tok.start[0]])
check('Sources sans caractères de contrôle',not bad,bad)
check('Textes TeX correctement protégés',not bad_literals,bad_literals)
pdf=BUILD/'main.pdf';doc=fitz.open(pdf);texts=[p.get_text() for p in doc];text='\n'.join(texts)
check('A4',all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc))
check('Toutes les pages contiennent du texte',all(len(t.strip())>20 for t in texts))
check('Aucun caractère de remplacement','\ufffd' not in text and '\x00' not in text)
check('Aucun renvoi en attente','??' not in text)
check('Métadonnées','Brevet 2027' in doc.metadata['title'] and doc.metadata['author']=='OptiTAB')
links=[l for p in doc for l in p.get_links()]
check('Navigation interne',len(links)>750,len(links))
check('Destinations valides',all(0<=l['page']<len(doc) for l in links if l['kind']==fitz.LINK_GOTO))
outside=[]
for n,p in enumerate(doc,1):
    for b in p.get_text('dict')['blocks']:
        for li in b.get('lines',[]):
            for span in li['spans']:
                r=fitz.Rect(span['bbox'])
                if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append([n,span['text'],list(r)])
check('Aucun texte hors page',not outside,outside[:20])
for title,needle,lengths in [('Forces 12 N et 10 N','3 cm et 2,5 cm',[3,2.5]),('Caisse 39,2 N','Deux flèches de 3,92 cm',[3.92,3.92])]:
    candidate=[i for i,t in enumerate(texts) if needle in t.replace('\n',' ')]
    mesures=[]
    for i in candidate:
        vals=[]
        for dr in doc[i].get_drawings():
            if (dr.get('width') or 0)<1.5:continue
            for item in dr['items']:
                if item[0]=='l':
                    a,b=item[1:];vals.append(math.hypot(a.x-b.x,a.y-b.y)/72*2.54)
        mesures.append(vals)
    check('Échelle physique dans le livre : '+title,any(all(sum(abs(v-l)<.001 for v in vals)>=lengths.count(l) for l in set(lengths)) for vals in mesures),candidate)
for code,title,ch,ex,mode in CONCORDANCE:check('Concordance '+code,code in text and 1<=ch<=18 and all(1<=int(n.strip())<=15 for n in ex.split(',')))
manifest=json.loads((BUILD/'figures.json').read_text(encoding='utf8'))
figs=list((HERE/'figures').glob('*.pdf'));check('Figures utilisées exclusivement',{p.stem for p in figs}==set(manifest['figures']))
check('70 démarches de brevet',set(METHODES)=={(n,j) for n in range(1,11) for j in range(1,8)})
check('Dix sujets avec corrigés illustrés',set(CORRIGES)==set(range(1,11)))
for p in figs:
    d=fitz.open(p);check('Figure vectorielle '+p.stem,len(d)==1 and len(d[0].get_text().strip())>3 and not d[0].get_images())
check('Format 2027 annoncé','9 points scientifiques' in text and 'point de langue' in text)
for c in chs:
    pages=[i for i,t in enumerate(texts) if 'Pistes pour l’investigation' in t and f'D{c.numero}' in t]
    check(f'Investigation {c.numero} : avec le défi corrigé',bool(pages))
grilles=[t for t in texts if 'MA GRILLE DE BILAN APRÈS LES SEPT QUESTIONS' in t.replace('\n',' ').upper()]
check('Dix grilles de bilan regroupées',len(grilles)==10)
check('Renvois de remédiation avec les réponses',all('Question 3' in t and 'Pour reprendre le cours' in t for t in grilles))
for n,p in enumerate(doc,1):p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(QA/f'page-{n:03}.png')
for start in range(0,len(doc),12):
    sheet=Image.new('RGB',(1260,2480),'#e7eaf0');draw=ImageDraw.Draw(sheet)
    for j in range(start,min(start+12,len(doc))):
        im=Image.open(QA/f'page-{j+1:03}.png');im.thumbnail((400,580));x=(j-start)%3*420+(420-im.width)//2;y=(j-start)//3*620+25
        sheet.paste(im,(x,y));draw.text((x,y-18),f'PDF {j+1}',fill='#1B3C8E')
    sheet.save(QA/f'planche-{start//12+1:02}.png')
report=dict(date='2026-10-24',pages=len(doc),chapitres=18,exercices=270,questions_exercices=sum(len(e.questions) for c in chs for e in c.exercices),defis=18,investigations=18,brevets_blancs=15,sujets_format_annales=5,questions_brevets=115,figures=len(figs),liens=len(links),signets=len(doc.get_toc()),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),controles=len(checks),calculs=len(calculs),echecs=sum(not c['valide'] for c in checks),details=checks,calculs_verifies=calculs,pages_courtes=[dict(page=i+1,caracteres=len(t)) for i,t in enumerate(texts) if len(t)<300])
(BUILD/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k not in ['details','calculs_verifies','pages_courtes']},ensure_ascii=True,indent=2))
sys.exit(1 if report['echecs'] else 0)
