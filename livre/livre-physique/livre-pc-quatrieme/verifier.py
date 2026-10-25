"""Contrôles structurels, calculs, chimie, PDF et génération des planches."""
from pathlib import Path
import json,re,hashlib,math,sys
import fitz
from PIL import Image,ImageDraw
from donnees import charger
from annexes import BILANS,EVALUATIONS,CONCORDANCE
from corrections_activites import ACTIVITES

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
BUILD=HERE/'build';QA=ROOT/'tmp/pdfs/qa-pc-quatrieme-revision';QA.mkdir(parents=True,exist_ok=True)
checks=[];calculs=[]
def check(name,value,detail=None):
    checks.append(dict(controle=name,valide=bool(value),detail=detail))
    if not value:print('ECHEC',name,detail)

chs=charger();check('20 chapitres ordonnes',[c.numero for c in chs]==list(range(1,21)))
check('20 investigations et corrections',set(ACTIVITES)==set(range(1,21)))
all_ex=[]
for c in chs:
    check(f'{c.numero} : quatre lecons',len(c.lecons)==4)
    check(f'{c.numero} : quinze exercices',len(c.exercices)==15)
    check(f'{c.numero} : bilan, exemple et investigation',bool(c.bilan and c.exemple and c.activite))
    check(f'{c.numero} : deux figures de cours',len([l[2] for l in c.lecons if l[2]])==2)
    for j,e in enumerate(c.exercices+[c.defi],1):
        ident=f'{c.numero}.{j}' if j<=15 else f'D{c.numero}'
        check(ident+' : reponses completes',len(e.questions)==len(e.reponses) and all(e.questions) and all(e.reponses))
        all_ex.append((ident,e))
for code,title,e in BILANS+EVALUATIONS:
    check(code+' : cinq questions et bareme',len(e.questions)==len(e.reponses)==5 and all('point' in a for a in e.reponses))
    all_ex.append((code,e))
for ident,e in all_ex:
    for expression,expected in e.calculs:
        got=eval(expression,{'__builtins__':{}})
        ok=math.isclose(got,expected,rel_tol=1e-10,abs_tol=1e-10)
        calculs.append(dict(exercice=ident,expression=expression,obtenu=got,attendu=expected,valide=ok))
        check(ident+' : '+expression,ok)

# Inventaires independants des bilans chimiques publies.
def atoms(formula):
    result={}
    for atom,n in re.findall(r'([A-Z][a-z]?)(\d*)',formula):result[atom]=result.get(atom,0)+int(n or 1)
    return result
def total(side):
    out={}
    for coeff,formula in side:
        for atom,n in atoms(formula).items():out[atom]=out.get(atom,0)+coeff*n
    return out
reactions=[('Carbone',[(1,'C'),(1,'O2')],[(1,'CO2')]),('Eau',[(2,'H2'),(1,'O2')],[(2,'H2O')]),('Methane',[(1,'CH4'),(2,'O2')],[(1,'CO2'),(2,'H2O')])]
for name,left,right in reactions:check('Atomes conserves : '+name,total(left)==total(right),[total(left),total(right)])
for formula,expected in [('H2O',{'H':2,'O':1}),('N2O',{'N':2,'O':1}),('CH4',{'C':1,'H':4}),('C2H6O',{'C':2,'H':6,'O':1})]:check('Formule : '+formula,atoms(formula)==expected)

log=(BUILD/'main.log').read_text(encoding='utf8',errors='replace')
check('Aucun caractere manquant','Missing character' not in log)
check('Aucun renvoi indefini',not re.search(r'(?:Reference|Hyper reference).*?undefined|undefined references',log))
check('Aucun label duplique','multiply defined' not in log)
over=re.findall(r'Overfull \\[hv]box[^\n]*',log)
check('Aucun debordement de boite',not over,over)
check('Renvois stabilises',not re.search(r'Rerun to get|Label\(s\) may have changed',log))
aux=(BUILD/'main.aux').read_text(encoding='utf8')
for c in chs:
    for j in range(1,16):check(f'{c.numero}.{j} : liens enonce et solution',all(f'\\newlabel{{{tag}-{c.numero}-{j}}}' in aux for tag in ['exo','cor']))
    check(f'{c.numero} : defi et solution',all(f'\\newlabel{{{tag}-{c.numero}}}' in aux for tag in ['defi-ex','cor-defi']))
    check(f'{c.numero} : investigation et solution',all(f'\\newlabel{{{tag}-{c.numero}}}' in aux for tag in ['activite','cor-activite']))
controls=[]
for p in list(HERE.glob('*.py'))+list(HERE.glob('*.tex'))+list((HERE/'chapitres').glob('*.tex'))+list((HERE/'corriges').glob('*.tex')):
    s=p.read_text(encoding='utf8');bad=[ord(c) for c in s if ord(c)<32 and c not in '\t\r\n']
    if bad:controls.append([p.name,bad])
check('Aucun caractere de controle dans les sources',not controls,controls)

pdf=BUILD/'main.pdf';doc=fitz.open(pdf);texts=[p.get_text() for p in doc];text='\n'.join(texts)
check('Format A4',all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc))
check('Toutes les pages ont du texte',all(len(t.strip())>20 for t in texts))
check('Aucun texte de remplacement','\ufffd' not in text and '\x00' not in text)
check('Aucun renvoi en attente','??' not in text)
check('Metadonnees presentes','Quatrième' in doc.metadata['title'] and doc.metadata['author']=='OptiTAB')
links=[l for p in doc for l in p.get_links()]
check('Navigation interne riche',len(links)>700,len(links))
check('Destinations internes valides',all(0<=l['page']<len(doc) for l in links if l['kind']==fitz.LINK_GOTO))
outside=[]
for n,p in enumerate(doc,1):
    for b in p.get_text('dict')['blocks']:
        for li in b.get('lines',[]):
            for span in li['spans']:
                r=fitz.Rect(span['bbox'])
                if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append([n,span['text'],list(r)])
check('Aucun texte hors page',not outside,outside[:25])
for code,title,ch,ex,mode in CONCORDANCE:check('Concordance '+code,code in text and 1<=ch<=20 and all(1<=int(n.strip())<=15 for n in ex.split(',')))
from revision_exercices import ILLUSTRATIONS,METHODES,ANNEXES
figmanifest=json.loads((BUILD/'figures-exercices.json').read_text(encoding='utf8'))
audit=json.loads((BUILD/'audit-exercices.json').read_text(encoding='utf8'))
figs=list((HERE/'figures').glob('*.pdf'));check('Figures de cours et exercices',len(figs)==40+figmanifest['nombre'],len(figs))
check('326 exercices, défis, bilans et évaluations audités',audit['exercices_audites']+audit['defis_audites']+audit['bilans_evaluations_audites']==326)
check('Aucune légende coupée dans les figures nouvelles',not audit['legendes_hors_cadre'],audit['legendes_hors_cadre'])
for ident,entry in ILLUSTRATIONS.items():
    if ident.startswith('D'):n=int(ident[1:])
    else:n=int(ident.split('.')[0])
    for key,folder in [('figure','chapitres'),('figure_correction','corriges')]:
        name=entry[key]
        if name:check(ident+' : figure intégrée '+folder,name in (HERE/f'{folder}/{n:02}.tex').read_text(encoding='utf8') and (HERE/'figures'/(name+'.pdf')).is_file())
    for key,figkey,folder in [('figure_exacte','figure','chapitres'),('correction_exacte','figure_correction','corriges')]:
        if entry[key]:
            name=entry[figkey];fd=fitz.open(HERE/'figures'/(name+'.pdf'))
            check(ident+' : échelle physique conservée '+folder,fd[0].rect.width<164/25.4*72 and ('\\pcFigureExact{figures/'+name+'.pdf}') in (HERE/f'{folder}/{n:02}.tex').read_text(encoding='utf8'))
for code,entry in ANNEXES.items():
    for mode,questions in entry.items():
        for num,(name,caption,exact) in questions.items():
            check(f'{code} Q{num} : figure {mode}',name in (HERE/'annexes.tex').read_text(encoding='utf8') and (HERE/'figures'/(name+'.pdf')).is_file())
            if exact:check(f'{code} Q{num} : échelle physique conservée',('\\pcFigureExact{figures/'+name+'.pdf}') in (HERE/'annexes.tex').read_text(encoding='utf8'))
for name,entry in figmanifest['figures'].items():
    if 'entree' in entry:check(name+' : conservation du bilan énergétique',entry['entree']==entry['sortie1']+entry['sortie2']+entry['stockage'])
    if entry.get('distance') is not None and 'vitesse' in entry:check(name+' : aller-retour cohérent',math.isclose(entry['vitesse']*entry['duree']/2,entry['distance']))
    if 'motifs' in entry:check(name+' : fréquence cohérente',math.isclose(entry['motifs']/entry['duree_s'],entry['frequence_Hz']))
for p in figs:
    d=fitz.open(p);check('Figure exploitable : '+p.stem,len(d)==1 and len(d[0].get_text().strip())>3)

for n,p in enumerate(doc,1):p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(QA/f'page-{n:03}.png')
for start in range(0,len(doc),12):
    sheet=Image.new('RGB',(1260,2480),'#e7eaf0');draw=ImageDraw.Draw(sheet)
    for j in range(start,min(start+12,len(doc))):
        im=Image.open(QA/f'page-{j+1:03}.png');im.thumbnail((400,580));x=(j-start)%3*420+(420-im.width)//2;y=(j-start)//3*620+25
        sheet.paste(im,(x,y));draw.text((x,y-18),f'PDF {j+1}',fill='#1B3C8E')
    sheet.save(QA/f'planche-{start//12+1:02}.png')
report=dict(date='2026-10-24',pages=len(doc),chapitres=20,exercices=300,questions_exercices=sum(len(e.questions) for c in chs for e in c.exercices),defis=20,investigations=20,bilans=4,evaluations=2,figures=len(figs),figures_cours=40,figures_exercices=figmanifest['nombre'],enonces_illustres=audit['exercices_avec_figure_enonce'],corriges_illustres=audit['exercices_avec_figure_correction'],demarches_ajoutees=audit['corriges_avec_demarche_ajoutee'],liens=len(links),signets=len(doc.get_toc()),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),controles=len(checks),calculs=len(calculs),echecs=sum(not c['valide'] for c in checks),details=checks,calculs_verifies=calculs,pages_courtes=[dict(page=i+1,caracteres=len(t)) for i,t in enumerate(texts) if len(t)<300])
(BUILD/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k not in ['details','calculs_verifies','pages_courtes']},ensure_ascii=True,indent=2))
sys.exit(1 if report['echecs'] else 0)
