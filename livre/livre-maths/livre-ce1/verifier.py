"""Contrôles de cohérence, de calcul, de navigation et de rendu du volume CP."""
from pathlib import Path
import re,json,hashlib,sys
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image,ImageOps,ImageDraw
import modele,contenu_nombres,contenu_calcul,contenu_fractions,contenu_mesures,contenu_geometrie
from modele import CHAPITRES
from ressources import BILANS,problemes_oraux
from mise_en_page import ROOT as _ROOT
from fractions import Fraction as F
from dessins import diagram

ROOT=Path(__file__).resolve().parent;BUILD=ROOT/'build';QA=BUILD/'qa';QA.mkdir(exist_ok=True)
path=BUILD/'optitab-ce1-complet.pdf';doc=fitz.open(path)
checks=[]
def check(condition,label):
    if not condition:raise AssertionError(label)
    checks.append(label)

check(len(CHAPITRES)==32,'32 chapitres')
check(sum(len(c.exercices) for c in CHAPITRES)==288,'288 exercices')
check(sum(len(b[2]) for b in BILANS)==30,'30 questions de bilan')
eq_count=0;script_count=0
def arithmetic(text,label):
    global eq_count
    text=re.sub(r'(?<=\d)[ \u00a0](?=\d{3}\b)','',text)
    # Les chaînes d’égalités successives sont contrôlées terme à terme.
    # Les rangs, prix, mots ou variables ne sont pas interprétés comme des calculs.
    pat=r'(?<![\w])\d+(?:\s*[+\-]\s*\d+)+(?:\s*=\s*\d+(?:\s*[+\-]\s*\d+)*)+'
    for m in re.finditer(pat,text):
        vals=[eval(x.strip(),{'__builtins__':{}},{}) for x in m.group().split('=')]
        check(len(set(vals))==1,f'Égalité : {label} : {m.group()}');eq_count+=1
        check(all(0<=v<=1000 for v in vals),f'Champ du calcul : {label}')
    for m in re.finditer(r'\d+/\d+(?:\s*[+\-]\s*\d+/\d+)+\s*=\s*(?:\d+/\d+|\d+)',text):
        terms=m.group().split('=')
        vals=[eval(re.sub(r'(\d+)/(\d+)',r'F(\1,\2)',s),{'__builtins__':{}},{'F':F}) for s in terms]
        check(len(set(vals))==1,f'Fraction : {label} : {m.group()}');eq_count+=1

for c in CHAPITRES:
    check(bool(c.aide and c.vigilance),f'Accompagnement chapitre {c.numero}')
    for name,s in [('exemple',c.exemple),('guide',c.guide_reponse),*[(f'leçon {i}',s) for i,s in enumerate(c.lecon)]]:arithmetic(s,f'{c.numero} {name}')
    for i,e in enumerate(c.exercices,1):
        check(bool(e.consigne.strip() and e.reponse.strip()),f'Énoncé et corrigé {c.numero}.{i}')
        if e.check:check(bool(eval(e.check,{'__builtins__':{}},{'F':F})),f'Calcul déclaré {c.numero}.{i}');script_count+=1
        arithmetic(e.reponse,f'Corrigé {c.numero}.{i}')
for i,(_,_,items) in enumerate(BILANS,1):
    for j,e in enumerate(items,1):
        if e.check:check(bool(eval(e.check,{'__builtins__':{}},{'F':F})),f'Calcul bilan {i}.{j}');script_count+=1
        arithmetic(e.reponse,f'Bilan {i}.{j}')
bank=problemes_oraux();check(sum(len(s['problemes']) for s in bank)==360,'360 problèmes oraux')
for week in bank:
    for i,p in enumerate(week['problemes'],1):
        check(eval(p['expression'],{'__builtins__':{}},{})==p['reponse'],f'Réponse orale {week["numero"]}.{i}')
        arithmetic(p['calcul'],f'Oral {week["numero"]}.{i}')
        check('Réponse' not in p['enonce'],'Réponse non révélée dans l’énoncé oral')

meta=json.loads((BUILD/'manifeste.json').read_text(encoding='utf8'))
check(len(doc)==meta['pages'],'Pagination du manifeste')
alltext=[];links=0;outside=[];blank=[]
for i,p in enumerate(doc,1):
    text=p.get_text();alltext.append(text)
    if len(text.strip())<40:blank.append(i)
    for block in p.get_text('dict')['blocks']:
        if block['type']!=0:continue
        for line in block['lines']:
            for span in line['spans']:
                r=fitz.Rect(span['bbox'])
                if r.x0<0 or r.y0<0 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append((i,span['text']))
                check('\ufffd' not in span['text'],f'Encodage page {i}')
    for link in p.get_links():
        links+=1
        if link['kind']==fitz.LINK_GOTO:check(0<=link['page']<len(doc),f'Lien interne page {i}')
check(not outside,f'Texte hors page : {outside}')
check(not blank,f'Pages blanches : {blank}')
check(links>350,'Navigation interne et sources présentes')
check(len(doc.get_toc())>=65,'Signets du document')
check('…' not in alltext[4] and '…' not in alltext[5],'Pagination du sommaire résolue')
# Tous les blocs principaux ont été positionnés avec une limite explicite à la construction.
blocks=json.loads((BUILD/'blocs-texte.json').read_text(encoding='utf8'))
overlaps=[]
for page in range(1,len(doc)+1):
    bs=[x for x in blocks if x['page']==page]
    for j,a in enumerate(bs):
        for b in bs[j+1:]:
            dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
            dy=min(a['top']+a['h'],b['top']+b['h'])-max(a['top'],b['top'])
            if dx>1 and dy>.6:overlaps.append((page,a['texte'][:55],b['texte'][:55],round(dy,2)))
check(not overlaps,f'Blocs de texte qui se chevauchent : {overlaps}')

# Chaque dessin est aussi rendu seul dans son cadre réel : aucun élément
# graphique ou libellé ne doit déborder sur la consigne voisine.
figs=json.loads((BUILD/'blocs-figures.json').read_text(encoding='utf8'))
uniques={json.dumps([f['figure'],f['w'],f['h']],sort_keys=True):f for f in figs}
figure_overflow=[]
for idx,f in enumerate(uniques.values()):
    pw,ph=f['w']*mm,f['h']*mm
    out=QA/'figure-controle.pdf';cv=canvas.Canvas(str(out),pagesize=(pw,ph))
    diagram(cv,f['figure'],0,0,pw,ph);cv.save()
    fd=fitz.open(out);pg=fd[0]
    bounds=[d['rect'] for d in pg.get_drawings()]
    bounds += [fitz.Rect(s['bbox']) for bl in pg.get_text('dict')['blocks'] if bl['type']==0 for li in bl['lines'] for s in li['spans']]
    for r in bounds:
        if r.x0<-.8 or r.y0<-.8 or r.x1>pw+.8 or r.y1>ph+.8:
            figure_overflow.append((f['page'],f['figure'][0],tuple(round(v,1) for v in r)))
    fd.close()
check(not figure_overflow,f'Dessin sortant de son cadre : {figure_overflow}')

# Rendu intégral. Un montage par 12 pages, plus les pages à vérifier en grand.
for i,p in enumerate(doc,1):
    pix=p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    pix.save(str(QA/f'page-{i:03}.png'))
thumbw=260;thumbh=368
for start in range(0,len(doc),12):
    sheet=Image.new('RGB',(4*(thumbw+14)+14,3*(thumbh+30)+14),'#DCE1E8');draw=ImageDraw.Draw(sheet)
    for pos,idx in enumerate(range(start,min(start+12,len(doc)))):
        im=Image.open(QA/f'page-{idx+1:03}.png').convert('RGB');im.thumbnail((thumbw,thumbh))
        x=14+(pos%4)*(thumbw+14);y=14+(pos//4)*(thumbh+30)
        sheet.paste(im,(x,y));draw.text((x+4,y+thumbh+4),f'Page {idx+1}',fill='black')
    sheet.save(QA/f'planche-{start//12+1:02}.jpg',quality=90)
report=dict(pages=len(doc),chapitres=32,exercices=288,questions_bilans=30,problemes_oraux=360,calculs_declares=script_count,egalites_verifiees=eq_count,liens=links,signets=len(doc.get_toc()),blocs_texte=len(blocks),chevauchements=overlaps,texte_hors_page=outside,figures_uniques_controlees=len(uniques),figures_hors_cadre=figure_overflow,pages_blanches=blank,planches=(len(doc)+11)//12,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),portee='Les calculs déclarés et les égalités numériques détectées sont vérifiés. Les réponses graphiques, les manipulations et la pertinence pédagogique nécessitent une relecture humaine ou visuelle. Aucun label ministériel ni perfection absolue ne sont revendiqués.')
(QA/'controles.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
