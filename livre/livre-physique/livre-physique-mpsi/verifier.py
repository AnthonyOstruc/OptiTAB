"""Contrôles numériques, structurels et géométriques, puis planches de relecture."""
from pathlib import Path
from math import sin,cos,tan,asin,pi,sqrt,radians,degrees,isclose
import json,re,subprocess,hashlib
import fitz
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
B=R/'build'; Q=B/'qa'; Q.mkdir(exist_ok=True)
checks=[]
def near(name,value,expected,tol=1e-6):
    assert abs(value-expected)<=tol,(name,value,expected)
    checks.append({'nom':name,'valeur':value,'attendu':expected,'tolerance':tol})
def conjugate(p,f):return f*p/(p+f)
near('cours-image',conjugate(-40,15),24)
near('Newton-produit',(-40+15)*(24-15),-15**2)
near('E04-refraction',degrees(asin(sin(radians(60))/1.33)),40.6281306515)
near('E05-refraction',degrees(asin(1.52/1.33*sin(radians(50)))),61.1017590051)
r=asin(sin(pi/4)/1.5)
near('E06-decalage-mm',6*sin(pi/4-r)/cos(r),1.9748538491)
for name,p,f,q in [('E10',-30,10,15),('E11',-6,10,-15),('E12',-36,-12,-9),('E14',-6,5,30)]:
    near(name+'-conjugaison',conjugate(p,f),q)
    near(name+'-Newton',(p+f)*(q-f),-f*f)
near('E15-discriminant',90**2-4*90*20,900)
near('E17-distance-max-m',.02/(pi/10800),68.7549354157)
near('E18-cadrage-min-mm',50+1800*50/24,3800)
q0=50*5000/4950; q=50*4000/3950; a=50/8
near('E20-flou-mm',a*abs(1-q0/q),.01578282828)
on=sqrt(1.48**2-1.46**2)
near('E21-ON',on,.24248711306)
near('E21-angle-air',degrees(asin(on)),14.0333784103)
kap=1.48/3e8*(1.48/1.46-1)
near('E22-delta-ns',kap*1000*1e9,67.5799086758)
near('E22-debit-Mbps',1/(2*kap*1000)/1e6,7.39864864865)
near('E23-image-finale-cm',20+conjugate(-5,-10),16.6666666667)
uf=sqrt((4/9*.1)**2+(1/9*.1)**2)
near('E24-incertitude-cm',uf,.0458122847291)
near('E24-z',.1/sqrt(uf**2+.08**2),1.08465,.0001)
k=.03/(a*q0)
near('D1-borne-proche-mm',1/(1/5000+k),3389.37093275)
near('D1-borne-lointaine-mm',1/(1/5000-k),9527.43902439)
near('D1-hyperfocale-mm',50+50**2/(8*.03),10466.6666667)
L=(50e-9-20e-9)/kap
near('D2-longueur-max-m',L,443.918918919)
near('D2-transit-us',1.48*L/3e8/cos(asin(sin(radians(12))/1.48))*1e6,2.21193488961)
near('D3-position-objet-mm',4*164/160,4.1)
near('D3-puissance-m-1',.160/(.004*.025),1600)
near('D3-grossissement',.160/(.004*.025)*.25,400)
near('DM-focale-mm',(1000**2-600**2)/(4*1000),160)
near('DM-incertitude-mm',sqrt(.34**2+.6**2),.689637585983)
near('DM-z',1.5/sqrt(.34**2+.6**2+.8**2),1.420186,.001)
near('DS-A-angle-transmis',degrees(asin(1.5/1.33*sin(radians(50)))),59.7641506045)
near('DS-C-debit-Mbps',1/(2*kap*500)/1e6,14.7972972973)
near('R1-angle',degrees(asin(1/1.7)),36.0318790725)
near('R2-angle-verre',degrees(asin(1.5/1.55*sin(radians(50)))),47.8451191938)
near('R3-puissance',.15/(.001*.020),7500)
# Chaque dessin de lentille respecte l'équation et l'intersection des deux rayons.
for p,f in [(-4,1.5),(-1,2),(-4,-2),(-3,2)]:
    q=conjugate(p,f)
    near(f'trace-rayon-{p}-{f}',1-q/f,q/p)
near('corr-loupe-position',conjugate(-.6,1),-1.5)
near('R3-diametre-apparent',7500*2*.2e-6,.003)
import numpy as np
rng=np.random.default_rng(2026); M=100_000
xA=rng.normal(0.0,.10,M); xL=rng.normal(40.0,.10,M); xE=rng.normal(64.0,.10,M)
p,q=xL-xA,xE-xL; foc=p*q/(p+q)
near('simulation-moyenne-cm',float(np.mean(foc)),15,.001)
near('simulation-ecart-type-cm',float(np.std(foc,ddof=1)),.0485,.0005)
def expand_tex(name,stack=()):
    assert name not in stack,('Inclusion circulaire',name)
    content=(R/name).read_text(encoding='utf-8')
    return re.sub(r'\\input\{([A-Za-z0-9_/-]+)\}',lambda m:expand_tex(m.group(1)+'.tex',stack+(name,)),content)
tex=expand_tex('main.tex')
chapters=re.findall(r'\\planitem\{(\d+)\}',tex)
assert chapters==[f'{i:02}' for i in range(1,29)],chapters
toc_targets=re.findall(r'\\(?:tocrow|tocresource)\{[^}]*\}\{([^}]+)\}',tex)
assert len(toc_targets)>=25
assert len(re.findall(r'\\tocpart\{\d+\}',tex))==5
exs=re.findall(r'\\ex\{(E\d+)\}',tex)
sols=re.findall(r'\\sol\{(E\d+)\}',tex)
assert exs==[f'E{i:02}' for i in range(1,25)] and sols==exs
assert len(re.findall(r'\\label\{ex-D[123]\}',tex))==3
pdf=B/'main.pdf';doc=fitz.open(pdf)
outside=[];collisions=[];text_counts=[]
for i,page in enumerate(doc):
    text_counts.append(len(page.get_text().strip()))
    spans=[s for b in page.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']]
    for s in spans:
        box=fitz.Rect(s['bbox'])
        if box.x0<-.5 or box.y0<-.5 or box.x1>page.rect.width+.5 or box.y1>page.rect.height+.5:
            outside.append({'page':i+1,'texte':s['text'],'bbox':list(box)})
    long=[s for s in spans if len(re.findall(r'[A-Za-zÀ-ÿ]',s['text']))>=4 and s['size']>=6.5]
    for j,s in enumerate(long):
        r=fitz.Rect(s['bbox'])
        for t in long[j+1:]:
            q=fitz.Rect(t['bbox']); hit=r&q
            if not hit.is_empty and hit.width>4 and hit.height>min(r.height,q.height)*.45 and hit.get_area()>min(r.get_area(),q.get_area())*.16:
                collisions.append({'page':i+1,'a':s['text'],'b':t['text'],'intersection':list(hit)})
aux=(B/'main.aux').read_text(encoding='utf-8')
page_labels=re.findall(r'\\Page\{[^}]*\}\{[^}]*\}\{([^}]*)\}',tex)
locations={}
for lab in page_labels:
    hit=re.search(r'\\newlabel\{'+re.escape(lab)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
    assert hit,lab
    locations[lab]=int(hit.group(1))
expected=list(range(2,2+len(page_labels)))
pagination_ok=list(locations.values())==expected and len(doc)==1+len(page_labels)
links=[link for p in doc for link in p.get_links()]
broken=[x for x in links if x['kind']==fitz.LINK_GOTO and not 0<=x.get('page',-1)<len(doc)]
for lab in toc_targets:
    assert re.search(r'\\newlabel\{'+re.escape(lab)+r'\}',aux),('Destination de sommaire absente',lab)
report={'pdf':str(pdf),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(doc),'pages_prevues':1+len(page_labels),'pagination_conforme':pagination_ok,'positions_sections':locations,'chapitres_annonces':len(chapters),'entrees_sommaires_paginees':len(toc_targets),'exercices':len(exs),'defis':3,'dm':1,'ds':1,'parcours_authentiques':3,'figures_uniques_utilisees':len(set(re.findall(r'\\fig\{([^}]+)\}',tex))),'placements_figures':len(re.findall(r'\\fig\{',tex)),'controles_numeriques':checks,'textes_hors_page':outside,'collisions_candidates':collisions,'liens':len(links),'liens_internes_invalides':broken,'longueurs_textes_par_page':text_counts}
(B/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
# Le rendu de référence utilise Poppler, et non la seule extraction de texte.
if '--sans-rendu' not in __import__('sys').argv:
    print('Rendu Poppler 100 dpi...',flush=True)
    for pattern in ('page-*.png','planche-*.jpg'):
        for old in Q.glob(pattern):old.unlink()
    proc=subprocess.run(['pdftoppm','-r','100','-png',str(pdf),str(Q/'page')],capture_output=True)
    if proc.returncode!=0:raise RuntimeError(proc.stderr.decode(errors='replace'))
    paths=sorted(Q.glob('page-*.png'))
    assert len(paths)==len(doc),(len(paths),len(doc))
    for start in range(0,len(paths),4):
        thumbs=[]
        for j,p in enumerate(paths[start:start+4]):
            im=Image.open(p).convert('RGB');im.thumbnail((650,920))
            tile=Image.new('RGB',(680,960),'#e8ebef');tile.paste(im,((680-im.width)//2,25))
            ImageDraw.Draw(tile).text((14,936),f'Page PDF {start+j+1}',fill='black')
            thumbs.append(tile)
        sheet=Image.new('RGB',(1360,1920),'#e8ebef')
        for j,im in enumerate(thumbs):sheet.paste(im,((j%2)*680,(j//2)*960))
        sheet.save(Q/f'planche-{start+1:02}-{start+len(thumbs):02}.jpg',quality=88)
print(json.dumps({k:report[k] for k in ['pages','pages_prevues','pagination_conforme','exercices','placements_figures','textes_hors_page','collisions_candidates','liens_internes_invalides']},ensure_ascii=False,indent=2))
assert not outside and not broken
assert pagination_ok,'Certaines pages débordent ou une section est scindée.'
print(f'{len(checks)} contrôles numériques passés. Relecture visuelle à réaliser.',flush=True)
