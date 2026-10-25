"""Contrôle du contenu, des liens et du rendu de la refonte LuaLaTeX."""
from pathlib import Path
import hashlib, html, json, math, re, subprocess, unicodedata
import fitz
from PIL import Image, ImageDraw
import construire_template_terminale as livre

ROOT=livre.ROOT
OUT=livre.OUT
QA=OUT/'build/qa'
QA.mkdir(parents=True,exist_ok=True)
PDF=OUT/'main.pdf'

def normal(s):
    s=html.unescape(re.sub('<[^>]+>','',str(s))).lower().replace('œ','oe')
    return ''.join(c for c in unicodedata.normalize('NFKD',s) if c.isalnum())

def main():
    doc=fitz.open(PDF)
    log=(OUT/'build/main.log').read_text(encoding='utf8',errors='replace')
    aux=(OUT/'build/main.aux').read_text(encoding='utf8',errors='replace')
    meta=json.loads((OUT/'build/contenu.json').read_text(encoding='utf8'))
    text='\n'.join(p.get_text(sort=False) for p in doc)
    flat=normal(text)
    tests=[]
    def check(value,label):
        if not value:raise AssertionError(label)
        tests.append(label)
    for token in ('Overfull','Missing character','multiply defined','undefined references','PCFICHE-TROP'):
        check(token not in log,'Journal sans '+token)
    check(meta['chapitres']==20 and meta['exercices']==300 and meta['defis']==20,'20 chapitres, 300 exercices, 20 défis')
    labels=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{([^}]+)\}',aux))
    for n in range(1,21):
        for target in (f'chap-{n}',f'ess-{n}',f'corchap-{n}',f'defi-ex-{n}'):
            check(target in labels,'Destination '+target)
        for e in livre.EXOS[n]:
            for target in (f'exo-{n}-{e.n}',f'cor-{n}-{e.n}'):
                check(target in labels,'Destination '+target)
            if e.check:check(eval(e.check,{'__builtins__':{}},{}),f'Calcul {n}.{e.n}')
    # Les chaînes sont comparées sans les espaces et les coupures de lignes.
    # Le texte des 300 énoncés et des 300 corrigés doit être intégralement présent.
    missing=[];content_count=0
    def content(s,label):
        nonlocal content_count
        content_count+=1
        if normal(s) not in flat:missing.append((label,str(s)))
    for n,items in livre.EXOS.items():
        for e in items:
            content(e.titre,f'Titre {n}.{e.n}')
            if e.document:content(e.document,f'Document {n}.{e.n}')
            for i,q in enumerate(e.questions,1):content(q,f'Question {n}.{e.n}.{i}')
            content(e.reponse,f'Corrigé {n}.{e.n}')
    for n,ch in livre.CHS.items():
        for k,le in enumerate(ch.lecons,1):
            for field in ('texte','retenir','methode'):
                content(getattr(le,field),f'Cours {n}.{k} {field}')
        for field in ('mission','correction'):content(getattr(ch.activite,field),f'Activité {n} {field}')
        for k,s in enumerate(ch.activite.etapes):content(s,f'Activité {n} étape {k}')
        for k,s in enumerate(ch.activite.questions):content(s,f'Activité {n} question {k}')
        for field in ('situation','aide','correction'):content(getattr(ch.defi,field),f'Défi {n} {field}')
        for k,s in enumerate(ch.defi.questions):content(s,f'Défi {n} question {k}')
        for k,s in enumerate(ch.bilan):content(s,f'Bilan chapitre {n} repère {k}')
        content(ch.erreur,f'Erreur chapitre {n}')
    for n,fn in ((1,livre.ancien.cours1),(2,livre.ancien.cours2)):
        cap=livre.Capture();fn(cap)
        for page in cap.pages:
            if page['key'].endswith('ouverture'):continue
            for b in page['blocks']:
                if b[0]=='p':content(b[1],page['key'])
                elif b[0]=='box':content(b[2],page['key'])
                elif b[0]=='bullets':
                    for q in b[1]:content(q,page['key'])
    for letter,_,items in livre.BILANS:
        check(len(items)==5,'Cinq missions bilan '+letter)
        for e in items:
            for q in e.questions:content(q,f'Bilan {letter}.{e.n}')
            content(e.reponse,f'Correction bilan {letter}.{e.n}')
            if e.check:check(eval(e.check,{'__builtins__':{}},{}),f'Calcul bilan {letter}.{e.n}')
    for term,definition,n in livre.LEXIQUE:
        content(term,'Lexique '+term);content(definition,'Définition '+term)
    (QA/'contenus-manquants.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2),encoding='utf8')
    print('Contenus contrôlés :',content_count,'; introuvables :',len(missing),flush=True)
    outside=[];blank=[];badglyph=[];broken=[];fonts={};links=0;small=[];thin=[]
    for n,p in enumerate(doc,1):
        txt=p.get_text()
        if len(txt.strip())<65:blank.append(n)
        spans=[s for b in p.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']]
        body_text=''.join(s['text'] for s in spans if 100<fitz.Rect(s['bbox']).y0<760)
        if len(re.sub(r'\s','',body_text))<60:thin.append(n)
        for s in spans:
            r=fitz.Rect(s['bbox'])
            if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append((n,s['text'],tuple(r)))
            if '\ufffd' in s['text'] or '\x00' in s['text']:badglyph.append((n,s['text']))
            if 100<r.y0<750 and len(s['text'])>30 and s['size']<8:small.append((n,s['size'],s['text']))
        used={s['font'].replace(' ','') for s in spans}
        for f in p.get_fonts():
            if f[3].split('+')[-1].replace(' ','') in used:fonts[f[0]]=f[3]
        for link in p.get_links():
            links+=1
            if link['kind']==fitz.LINK_GOTO and not 0<=link['page']<len(doc):broken.append((n,link))
    # Vérification des schémas exportés, y compris leurs textes et graduations.
    figure_overflow=[]
    for f in meta['figures']:
        with fitz.open(OUT/'figures'/f['file']) as diagram:
            p=diagram[0]
            rr=[q['rect'] for q in p.get_drawings()]
            rr.extend(fitz.Rect(s['bbox']) for b in p.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans'])
            for r in rr:
                if r.x0<-.8 or r.y0<-.8 or r.x1>p.rect.width+.8 or r.y1>p.rect.height+.8:figure_overflow.append((f['schema'],tuple(r)))
    check(not outside,'Aucun texte hors page')
    check(not blank,'Aucune page vide')
    check(not thin,'Aucune page réduite à un renvoi ou un fragment isolé')
    check(not badglyph,'Aucun glyphe défectueux')
    check(not broken,'Tous les liens internes ont une destination valide')
    check(not figure_overflow,'Schémas vectoriels dans leurs cadres')
    check(all(doc.extract_font(x)[3] for x in fonts),'Polices incorporées')
    # Chaque page est rendue en PNG pour la relecture, sans substitution d'image.
    for pattern in ('page-*.png','planche-*.png'):
        for old in QA.glob(pattern):old.unlink()
    for n,p in enumerate(doc,1):
        p.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False).save(QA/f'page-{n:03}.png')
    tw,th=270,382
    for start in range(0,len(doc),12):
        sheet=Image.new('RGB',(1160,1250),'#DCE2E9');pen=ImageDraw.Draw(sheet)
        for j in range(12):
            if start+j>=len(doc):break
            im=Image.open(QA/f'page-{start+j+1:03}.png');im.thumbnail((tw,th))
            x=12+(j%4)*288;y=24+(j//4)*413
            sheet.paste(im,(x,y));pen.text((x,y-17),str(start+j+1),fill='#1B3C8E')
        sheet.save(QA/f'planche-{start//12+1:02}.png')
    # Épreuves par un deuxième moteur, Poppler, sur les types de pages sensibles.
    selected={1,2,3,4,5,6,len(doc)}
    for key in ['chap-1','ess-1','rub-1-1','chap-3','ess-3','chap-6','chap-10','chap-13','chap-15','chap-18','chap-19','chap-20','corchap-1','corchap-10','corchap-20','bilan-A','unites','lexique','programme',
                'ch-6-cours-3','ch-7-cours-2','ch-8-cours-1','ch-11-cours-2','ch-13-cours-2','ch-15-cours-2','ch-17-cours-2','ch-18-cours-2','ch-19-cours-1','ch-20-cours-3']:
        if key in labels:selected.add(int(labels[key])+1)
    poppler=QA/'poppler';poppler.mkdir(exist_ok=True)
    for p in sorted(selected):
        subprocess.run(['pdftoppm','-f',str(p),'-l',str(p),'-scale-to','1500','-singlefile','-png',str(PDF),str(poppler/f'page-{p:03}')],capture_output=True,check=True)
    report=dict(pdf=str(PDF),sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),pages=len(doc),
                chapitres=20,exercices=300,defis=20,bilans=4,missions=20,lexique=80,
                contenus_controles=content_count,contenus_introuvables=missing,
                insertions_schemas=meta['insertions'],figures_vectorielles=len(meta['figures']),
                liens=links,signets=len(doc.get_toc()),polices=list(fonts.values()),
                texte_hors_page=outside,pages_vides=blank,pages_fragments_isoles=thin,glyphes_defectueux=badglyph,liens_casses=broken,
                schemas_hors_cadre=figure_overflow,petits_textes_a_revoir=small,
                planches=math.ceil(len(doc)/12),epreuves_poppler=sorted(selected),tests=len(tests))
    (QA/'controles.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['polices','epreuves_poppler','contenus_introuvables','petits_textes_a_revoir']},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
