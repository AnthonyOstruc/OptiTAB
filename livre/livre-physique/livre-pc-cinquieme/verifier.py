"""Contrôles scientifiques ciblés, navigation, cadrage et rendu intégral."""
from pathlib import Path
import json,hashlib,re
from fractions import Fraction as F
import fitz
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from maquette import ROOT,BUILD,mm
from schemas import draw
from contenu import CH1,CH2,PLAN

QA=BUILD/'qa';QA.mkdir(exist_ok=True)
path=BUILD/'optitab-physique-chimie-5e-apercu.pdf';doc=fitz.open(path)
meta=json.loads((BUILD/'manifeste.json').read_text(encoding='utf8'))
blocks=json.loads((BUILD/'blocs-texte.json').read_text(encoding='utf8'))
figs=json.loads((BUILD/'blocs-figures.json').read_text(encoding='utf8'))
checks=[]
def check(ok,label):
    if not ok:raise AssertionError(label)
    checks.append(label)
check(sum(len(c) for _,_,c in PLAN)==20,'20 chapitres au sommaire')
check(len(CH1)==len(CH2)==15,'15 exercices par chapitre')
check(len(meta['exercices_pages'])==30,'30 énoncés présents')
numeric=0
for ch,es in enumerate([CH1,CH2],1):
    for e in es:
        check(bool(e.questions and e.reponse),f'Énoncé/corrigé {ch}.{e.n}')
        check(f'ex-{ch}-{e.n}' in meta['destinations'] and f'cor-{ch}-{e.n}' in meta['destinations'],f'Renvois {ch}.{e.n}')
        if e.check:check(eval(e.check,{'__builtins__':{}},{}),f'Calcul {ch}.{e.n}');numeric+=1
for expr,label in [
    ('F(1231,10)-F(486,10)==F(745,10)','Pesée sans tare'),
    ('(30-20)/5==2','Lecture d’une division'),
    ('58-40==18','Volume par immersion du cours'),
    ('F(35,100)*1000==350','Conversion L vers mL'),
    ('F(750,1000)==F(75,100)','Conversion g vers kg'),
    ('50-40==10 and F(10,20)==F(1,2)','Volume du défi 2'),
    ('F(780,10)/20==F(39,10)','Masse du défi 2'),
]:check(eval(expr,{'__builtins__':{}},{'F':F}),label);numeric+=1

outside=[];blank=[];badglyph=[];links=0;alltext=[]
for n,p in enumerate(doc,1):
    text=p.get_text();alltext.append(text)
    if len(text.strip())<70:blank.append(n)
    for bl in p.get_text('dict')['blocks']:
        if bl['type']!=0:continue
        for li in bl['lines']:
            for s in li['spans']:
                r=fitz.Rect(s['bbox'])
                if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append((n,s['text']))
                if '\ufffd' in s['text'] or '\x00' in s['text']:badglyph.append((n,s['text']))
    for link in p.get_links():
        links+=1
        if link['kind']==fitz.LINK_GOTO:check(0<=link['page']<len(doc),f'Lien page {n}')
check(not outside,f'Texte hors page : {outside}')
check(not badglyph,f'Glyphes : {badglyph}')
check(not blank,f'Pages blanches : {blank}')
check('…' not in alltext[2] and '…' not in alltext[3],'Sommaire résolu')
check(len(doc)==meta['pages'],'Pagination stable')
overlaps=[]
for n in range(1,len(doc)+1):
    bs=[b for b in blocks if b['page']==n]
    for i,a in enumerate(bs):
        for b in bs[i+1:]:
            dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
            dy=min(a['top']+a['h'],b['top']+b['h'])-max(a['top'],b['top'])
            if dx>1 and dy>.6:overlaps.append((n,a['text'][:50],b['text'][:50],round(dy,2)))
check(not overlaps,f'Chevauchements : {overlaps}')

unique={json.dumps([f['spec'],f['w'],f['h']],sort_keys=True):f for f in figs}
overflow=[]
for f in unique.values():
    out=QA/'schema-controle.pdf';pw=f['w']*mm;ph=f['h']*mm;cv=canvas.Canvas(str(out),pagesize=(pw,ph))
    draw(cv,f['spec'],0,0,pw,ph);cv.save();d=fitz.open(out);p=d[0]
    rr=[q['rect'] for q in p.get_drawings()]
    rr+=[fitz.Rect(s['bbox']) for bl in p.get_text('dict')['blocks'] if bl['type']==0 for li in bl['lines'] for s in li['spans']]
    for r in rr:
        if r.x0<-.8 or r.y0<-.8 or r.x1>pw+.8 or r.y1>ph+.8:overflow.append((f['page'],f['spec'][0],tuple(round(q,1) for q in r)))
    d.close()
check(not overflow,f'Schémas hors cadre : {overflow}')

# Les valeurs de lecture correspondent à de vraies graduations et les
# immersions proposées donnent une différence positive sous la capacité.
gradchecks=0
for f in figs:
    kind,data=f['spec']
    if kind in ['cylinders','displacement']:
        vals,maxv,step=data
        check(all(0<=v<=maxv and v%step==0 for v in vals),f'Graduations page {f["page"]}')
        if kind=='displacement':check(vals[1]>vals[0],f'Immersion page {f["page"]}')
        gradchecks+=1

for n,p in enumerate(doc,1):p.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False).save(QA/f'page-{n:03}.png')
tw,th=260,368
for start in range(0,len(doc),8):
    sheet=Image.new('RGB',(4*(tw+14)+14,2*(th+28)+14),'#DCE2E9');pen=ImageDraw.Draw(sheet)
    for pos,idx in enumerate(range(start,min(start+8,len(doc)))):
        im=Image.open(QA/f'page-{idx+1:03}.png').convert('RGB');im.thumbnail((tw,th));xx=14+(pos%4)*(tw+14);yy=14+(pos//4)*(th+28)
        sheet.paste(im,(xx,yy));pen.text((xx+4,yy+th+4),f'Page {idx+1}',fill='black')
    sheet.save(QA/f'planche-{start//8+1:02}.jpg',quality=92)
report=dict(pages=len(doc),exercices=30,defis=2,chapitres_rediges=2,chapitres_au_sommaire=20,insertions_schemas=len(figs),schemas_uniques=len(unique),calculs_declares=numeric,controles_graduations=gradchecks,liens=links,signets=len(doc.get_toc()),blocs_texte=len(blocks),chevauchements=overlaps,texte_hors_page=outside,schemas_hors_cadre=overflow,pages_blanches=blank,planches=(len(doc)+7)//8,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),portee='Calculs et navigation contrôlés ; les observations, modèles et activités ouvertes font aussi l’objet d’une relecture visuelle et scientifique. Aucune validation institutionnelle n’est revendiquée.')
(QA/'controles.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
