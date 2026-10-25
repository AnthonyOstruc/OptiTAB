"""Traçabilité des figures, des explications et des constructions à l’échelle."""
from pathlib import Path
import json,math,re
import fitz
from PIL import Image,ImageDraw
from donnees import charger
from brevets import SUJETS
from revision_brevets import CORRIGES,METHODES
from construire import normaliser
HERE=Path(__file__).parent;QA=HERE.parent/'tmp/pdfs/qa-pc-brevet';QA.mkdir(parents=True,exist_ok=True)
entries=[];checks=[]
def check(n,b):
    checks.append(dict(controle=n,valide=bool(b)))
    if not b:print('ECHEC',n)
for c in charger():
    tex=(HERE/f'chapitres/{c.numero:02}.tex').read_text(encoding='utf8')
    cor=(HERE/f'corriges/{c.numero:02}.tex').read_text(encoding='utf8')
    for j,e in enumerate(c.exercices+[c.defi],1):
        ident=f'{c.numero}.{j}' if j<=15 else f'D{c.numero}'
        for name,txt in [(e.figure,tex),(e.figure_correction,cor)]:
            if name:check(ident+' : figure présente '+name,(HERE/'figures'/(name+'.pdf')).exists() and f'figures/{name}.pdf' in txt)
        if e.methode:check(ident+' : démarche composée',normaliser(e.methode) in cor)
        entries.append(dict(exercice=ident,titre=e.titre,figure_enonce=e.figure,figure_corrige=e.figure_correction,demarche=bool(e.methode),decision='Schéma présent aux étapes utiles.' if e.figure or e.figure_correction else 'Question de vocabulaire, de calcul ou d’argumentation autonome ; pas de construction graphique requise.'))
ann=(HERE/'annexes.tex').read_text(encoding='utf8')
for s in SUJETS:
    for k,p in enumerate(s.parties,1):
        e=p.exercice
        if e.figure:check(f'BB{s.numero}.{k} : document figuré',f'figures/{e.figure}.pdf' in ann)
        start=1 if k==1 else 4
        figs={q:v[0] for q,v in CORRIGES[s.numero].items() if start<=q<start+len(e.questions)}
        for q,name in figs.items():check(f'BB{s.numero} Q{q} : correction illustrée',f'figures/{name}.pdf' in ann)
        for q in range(start,start+len(e.questions)):check(f'BB{s.numero} Q{q} : démarche explicite',normaliser(METHODES[s.numero,q]) in ann)
        entries.append(dict(exercice=f'BB{s.numero}.{k}',titre=p.titre,figure_enonce=e.figure,figures_corrige=figs,questions_avec_demarche=len(e.questions)))
registry={}
for file in ['figures-reprises.json','figures-nouvelles.json']:registry.update(json.loads((HERE/'build'/file).read_text(encoding='utf8')))
used=set(json.loads((HERE/'build/figures.json').read_text(encoding='utf8'))['figures'])
for name,data in registry.items():
    if name in used:check(name+' : texte dans le cadre',not data.get('textes_hors_cadre'))
check('308 entraînements et parties audités',len(entries)==308)
for name,lengths in [('rev-cor-force-echelle',[3,2.5]),('rev-cor-caisse',[3.92,3.92])]:
    p=fitz.open(HERE/'figures'/(name+'.pdf'))[0]
    check(name+' : largeur 150 mm',abs(p.rect.width/72*25.4-150)<.01)
    found=[]
    for dr in p.get_drawings():
        for item in dr['items']:
            if item[0]=='l' and dr.get('width',0)>1.5:
                a,b=item[1:];found.append(math.hypot(a.x-b.x,a.y-b.y)/72*2.54)
    for l in lengths:check(name+' : longueur réelle '+str(l),any(abs(v-l)<1e-5 for v in found))
    tex=(HERE/'corriges'/('09.tex')).read_text(encoding='utf8');check(name+' : sans redimensionnement',f'\\pcFigureExact{{figures/{name}.pdf}}' in tex)
# Vérifications indépendantes sur les nouveaux documents chiffrés.
for name in ['rev-ex-immersion','rev-cor-immersion','rev-bb7-enonce','rev-bb7-corrige']:
    d=registry[name];check(name+' : déplacement et densité',d['Vf_mL']-d['Vi_mL']==d['volume_cm3'] and math.isclose(d['masse_g']/d['volume_cm3'],d['rho']))
for name in ['rev-bb6-sonar-cor','rev-bb4-radio-cor']:
    d=registry[name];check(name+' : aller-retour',math.isclose(2*d['distance'],d['vitesse']*d['aller_retour_s']))
for name in ['rev-cor-atome-na','rev-cor-atome-cu','rev-cor-atome-cl','rev-cor-atome-al','rev-cor-atome-mg','rev-cor-atome-isotopes','rev-cor-atome-fe3','rev-cor-atome-fe2']:
    for title,p,n,e,ch in registry[name]['constituants']:check(name+' : charge '+title,p-e==int(ch.replace('−','-')))
for name in ['rev-cor-resistances-6','rev-cor-resistances-12']:
    d=registry[name];check(name+' : loi Ohm',all(math.isclose(r*i,d['tension']) for r,i in zip(d['resistances'],d['courants'])))
check('Bilan énergétique recyclage',registry['rev-bb7-bilan']['conservation'])
files=sorted(HERE.joinpath('figures').glob('*.pdf'))
for start in range(0,len(files),12):
    sheet=Image.new('RGB',(1600,1950),'#e9ecf2');draw=ImageDraw.Draw(sheet)
    for j,p in enumerate(files[start:start+12]):
        doc=fitz.open(p);pix=doc[0].get_pixmap(matrix=fitz.Matrix(1.8,1.8),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((765,270))
        x=j%2*800+(800-im.width)//2;y=j//2*325+35;sheet.paste(im,(x,y));draw.text((j%2*800+20,y-23),p.stem,fill='#1B3C8E')
    sheet.save(QA/f'figures-{start//12+1:02}.png')
report=dict(entrees=entries,figures=len(used),enonces_illustres=sum(bool(e.get('figure_enonce')) for e in entries),corriges_illustres=sum(bool(e.get('figure_corrige') or e.get('figures_corrige')) for e in entries),demarches_chapitres=sum(bool(e.get('demarche')) for e in entries),demarches_brevets=70,controles=len(checks),echecs=sum(not c['valide'] for c in checks),details=checks)
(HERE/'build/audit-revision.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k not in ['entrees','details']},ensure_ascii=True,indent=2))
assert report['echecs']==0
