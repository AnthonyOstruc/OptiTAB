"""Contrôles de la version complète, rendu intégral et planches de relecture."""
from pathlib import Path
import json,hashlib,re,math,subprocess
from fractions import Fraction as F
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
import fitz
from maquette import mm
from schemas import draw
from contenu import CH1,CH2
from construire_complet import FULL,CHAPITRES
from annexes_completes import BILANS,LEXIQUE

QA=FULL/'qa';QA.mkdir(exist_ok=True)
PDF=FULL/'optitab-physique-chimie-5e-complet.pdf'
def main():
    doc=fitz.open(PDF)
    meta=json.loads((FULL/'manifeste.json').read_text(encoding='utf8'))
    blocks=json.loads((FULL/'blocs-texte.json').read_text(encoding='utf8'))
    figs=json.loads((FULL/'blocs-figures.json').read_text(encoding='utf8'))
    checks=[]
    def check(condition,label):
        if not condition:raise AssertionError(label)
        checks.append(label)
    check([ch.n for ch in CHAPITRES]==list(range(3,21)),'18 nouveaux chapitres présents')
    check(meta['chapitres_rediges']==20 and meta['exercices']==300 and meta['defis']==20,'Comptes complets')
    check(len(meta['exercices_pages'])==300,'300 énoncés navigables')
    numerical=0
    for n,exos in [(1,CH1),(2,CH2)]+[(ch.n,ch.exercices) for ch in CHAPITRES]:
        check([e.n for e in exos]==list(range(1,16)),f'Numérotation chapitre {n}')
        for e in exos:
            check(bool(e.questions and e.reponse),f'Énoncé et solution {n}.{e.n}')
            check(f'ex-{n}-{e.n}' in meta['destinations'] and f'cor-{n}-{e.n}' in meta['destinations'],f'Navigation {n}.{e.n}')
            if e.check:
                check(eval(e.check,{'__builtins__':{}},{}),f'Calcul exercice {n}.{e.n}');numerical+=1
    for letter,_,exos in BILANS:
        check(len(exos)==5,f'Cinq missions bilan {letter}')
        for e in exos:
            check(bool(e.reponse),f'Correction bilan {letter}.{e.n}')
            if e.check:check(eval(e.check,{'__builtins__':{}},{}),f'Calcul bilan {letter}.{e.n}');numerical+=1
    # Vérifications indépendantes des résultats de cours, activités et défis.
    computations=[
        (F(1231,10)-F(486,10),F(745,10),'Tare sans remise à zéro'),
        (58-40,18,'Immersion du cours'),(F(10,20),F(1,2),'Volume moyen d’une bille'),
        (F(780,10)/20,F(39,10),'Masse moyenne d’une bille'),
        (8-3,5,'Durée d’un palier'),(2*78,156,'Diazote pour 200 parts'),
        (2*21,42,'Dioxygène pour 200 parts'),(F(18,12)*40-40,20,'Eau ajoutée pour dissoudre'),
        (F(58,50),F(116,100),'Maquette de Mercure'),(F(108,50),F(216,100),'Maquette de Vénus'),
        (F(228,50),F(456,100),'Maquette de Mars'),(F(780,50),F(156,10),'Maquette de Jupiter'),
        (F(4500,45),100,'Échelle de la cour'),(F(228,100),F(228,100),'Mars dans la cour'),
        (F(10,8),F(125,100),'Vitesse de marche essai 1'),(F(10,10),1,'Vitesse de marche essai 2'),
        (8+2+5,15,'Durée de la sortie avec pause'),(F(1,1)/F(15,60),4,'Moyenne avec pause'),
        (200-40,160,'Bilan lampe A'),(200-70,130,'Bilan lampe B'),
        (120-36,84,'Économie annuelle'),(F(84,120),F(7,10),'Part économisée'),
        (300-60-40,200,'Consommation de la classe'),(F(100,300),F(1,3),'Fraction économisée'),
        (F(340)*F(6,10),204,'Trajet total de l’écho'),(F(204,2),102,'Distance au mur'),
        (8*F(1,2),4,'Durée du message'),(F(150000000,300000),500,'Délai Soleil-Terre'),
    ]
    for got,expected,label in computations:check(got==expected,label)
    numerical+=len(computations)
    code={'A':'10','B':'01','C':'11','D':'00'}
    check(''.join(code[q] for q in 'ACDA')=='10110010','Codage activité 20')
    check(''.join(code[q] for q in 'BACA')=='01101110','Codage défi 20')
    check(len(LEXIQUE)==80,'80 entrées de lexique')
    outside=[];blank=[];badglyph=[];links=0;broken=[];fonts={};texts=[]
    for n,p in enumerate(doc,1):
        txt=p.get_text();texts.append(txt)
        if len(txt.strip())<65:blank.append(n)
        spans=[s for bl in p.get_text('dict')['blocks'] if bl['type']==0 for li in bl['lines'] for s in li['spans']]
        for s in spans:
            r=fitz.Rect(s['bbox'])
            if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append((n,s['text']))
            if '\ufffd' in s['text'] or '\x00' in s['text']:badglyph.append((n,s['text']))
        used={s['font'] for s in spans}
        for f in p.get_fonts():
            if f[3].split('+')[-1] in used:fonts[f[0]]=f[3]
        for link in p.get_links():
            links+=1
            if link['kind']==fitz.LINK_GOTO and not 0<=link['page']<len(doc):broken.append((n,link))
    check(not outside,f'Texte hors page : {outside}')
    check(not badglyph,f'Glyphes : {badglyph}')
    check(not blank,f'Pages blanches : {blank}')
    check(not broken,f'Liens cassés : {broken}')
    check(all(doc.extract_font(x)[3] for x in fonts),'Polices utilisées incorporées')
    check(all('…' not in texts[n-1] for n in [3,4,5]),'Sommaire et repères résolus')
    check(not any('MAQUETTE DE VALIDATION' in t or 'DANS CET EXTRAIT' in t or 'chapitres 3 à 20 figurent' in t for t in texts),'Mentions d’aperçu absentes')
    check(len(doc)==meta['pages'],'Pagination stable')
    overlaps=[]
    for n in range(1,len(doc)+1):
        bs=[b for b in blocks if b['page']==n]
        for i,a in enumerate(bs):
            for b in bs[i+1:]:
                dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
                dy=min(a['top']+a['h'],b['top']+b['h'])-max(a['top'],b['top'])
                if dx>1 and dy>.6:overlaps.append((n,a['text'][:45],b['text'][:45],round(dy,2)))
    check(not overlaps,f'Chevauchements de texte : {overlaps}')
    unique={json.dumps(f['spec'],sort_keys=True):f for f in figs}
    variants={json.dumps([f['spec'],f['w'],f['h']],sort_keys=True):f for f in figs}
    overflow=[];plotchecks=0;graduations=0
    for f in variants.values():
        out=QA/'schema-controle.pdf';pw=f['w']*mm;ph=f['h']*mm;cv=canvas.Canvas(str(out),pagesize=(pw,ph))
        draw(cv,f['spec'],0,0,pw,ph);cv.save()
        with fitz.open(out) as d:
            p=d[0];rr=[q['rect'] for q in p.get_drawings()]
            rr+=[fitz.Rect(s['bbox']) for bl in p.get_text('dict')['blocks'] if bl['type']==0 for li in bl['lines'] for s in li['spans']]
            for r in rr:
                if r.x0<-.8 or r.y0<-.8 or r.x1>pw+.8 or r.y1>ph+.8:overflow.append((f['page'],f['spec'][0],tuple(round(q,1) for q in r)))
    check(not overflow,f'Schémas hors cadre : {overflow}')
    for f in figs:
        kind,data=f['spec']
        if kind in ['cylinders','displacement']:
            vals,maximum,step=data
            check(all(0<=v<=maximum and v%step==0 for v in vals),f'Graduations page {f["page"]}')
            if kind=='displacement':check(vals[1]>vals[0],f'Immersion page {f["page"]}')
            graduations+=1
        if kind in ['pc_temperature','pc_speed']:
            data=data or {};tt=data.get('t',[0,1,2,3,4,5] if kind=='pc_temperature' else [0,1,2,3,4]);vv=data.get('v',[-10,-5,0,0,0,5] if kind=='pc_temperature' else [0,3,6,9,12])
            check(len(tt)==len(vv) and tt==sorted(set(tt)),f'Dates ordonnées page {f["page"]}')
            check(min(vv)>=data.get('min',-10 if kind=='pc_temperature' else 0) and max(vv)<=data.get('max',10 if kind=='pc_temperature' else 12),f'Échelle de courbe page {f["page"]}')
            plotchecks+=1
    # Toutes les pages sont rendues ; les planches couvrent douze pages chacune.
    for n,p in enumerate(doc,1):p.get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False).save(QA/f'page-{n:03}.png')
    tw,th=260,368
    for start in range(0,len(doc),12):
        sheet=Image.new('RGB',(1110,1202),'#DCE2E9');pen=ImageDraw.Draw(sheet)
        for pos,idx in enumerate(range(start,min(start+12,len(doc)))):
            im=Image.open(QA/f'page-{idx+1:03}.png').convert('RGB');im.thumbnail((tw,th));xx=14+(pos%4)*274;yy=14+(pos//4)*396
            sheet.paste(im,(xx,yy));pen.text((xx+4,yy+th+4),f'Page {idx+1}',fill='black')
        sheet.save(QA/f'planche-{start//12+1:02}.jpg',quality=93)
    # Les schémas distincts sont agrandis séparément pour la relecture.
    schema_pages=[]
    for idx,f in enumerate(unique.values(),1):
        clip=fitz.Rect(f['x']*mm,f['top']*mm,(f['x']+f['w'])*mm,(f['top']+f['h'])*mm)
        doc[f['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=clip,alpha=False).save(QA/f'schema-{idx:03}.png')
        schema_pages.append(dict(index=idx,page=f['page'],spec=f['spec']))
    for start in range(0,len(schema_pages),6):
        sheet=Image.new('RGB',(1542,696),'#DCE2E9');pen=ImageDraw.Draw(sheet)
        for pos,record in enumerate(schema_pages[start:start+6]):
            im=Image.open(QA/f'schema-{record["index"]:03}.png').convert('RGB');im.thumbnail((490,290));xx=12+(pos%3)*510;yy=12+(pos//3)*338
            sheet.paste(im,(xx,yy));pen.text((xx,yy+300),f'{record["index"]} / p.{record["page"]} / {record["spec"][0]}',fill='black')
        sheet.save(QA/f'schemas-planche-{start//6+1:02}.jpg',quality=94)
    (QA/'schemas-index.json').write_text(json.dumps(schema_pages,ensure_ascii=False,indent=2),encoding='utf8')
    report=dict(pages=len(doc),chapitres=20,exercices=300,defis=20,bilans=4,missions_bilans=20,entrees_lexique=len(LEXIQUE),
        insertions_schemas=len(figs),schemas_distincts=len(unique),variantes_mise_en_page=len(variants),
        controles_calculs=numerical,controles_graduations=graduations,controles_courbes=plotchecks,
        liens=links,signets=len(doc.get_toc()),polices_utilisees=list(fonts.values()),
        chevauchements=overlaps,texte_hors_page=outside,schemas_hors_cadre=overflow,pages_blanches=blank,
        planches=math.ceil(len(doc)/12),planches_schemas=math.ceil(len(unique)/6),
        sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),
        portee='Contrôles automatisés complétés par relecture scientifique et inspection visuelle ; aucune validation institutionnelle revendiquée.')
    (QA/'controles.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
