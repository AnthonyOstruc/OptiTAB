from pathlib import Path
import json,re,hashlib,sys
import fitz
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'outils'))
from collisions_physique_20261024 import candidates

p=ROOT/'main.pdf';d=fitz.open(p);log=(ROOT/'build/main.log').read_text(encoding='utf-8')
errors=[]
for token in ('Overfull','Missing character','undefined references','multiply defined','Fatal error','Undefined control sequence'):
    if token in log:errors.append('Journal : '+token)
blocks=re.findall(r'OTBLOC\|([^|]+)\|([\d.]+)pt',log)
if len(blocks)!=516:errors.append(f'Blocs mesurés : {len(blocks)} au lieu de 516')
for i,page in enumerate(d,1):
    if abs(page.rect.width-595.276)>1 or abs(page.rect.height-841.89)>1:errors.append(f'Format page {i}')
    for b in page.get_text('dict')['blocks']:
        if b['type']!=0:continue
        for line in b['lines']:
            for span in line['spans']:
                r=fitz.Rect(span['bbox'])
                if span['text'].strip() and (r.x0 < -1 or r.y0 < -1 or r.x1>page.rect.width+1 or r.y1>page.rect.height+1):
                    errors.append(f'Hors page {i} : '+span['text'])
    for link in page.get_links():
        if link['kind']==fitz.LINK_GOTO and not (0<=link.get('page',-1)<len(d)):
            errors.append(f'Lien interne non résolu page {i}')
overlaps=candidates(p)
if overlaps:errors.append(f'{len(overlaps)} collisions candidates à relire')
reader=PdfReader(p);fonts={};unembedded=[]
for page in reader.pages:
    for _,f in (page.get('/Resources',{}).get('/Font',{}) or {}).items():
        f=f.get_object();name=str(f.get('/BaseFont',''))
        fs=f.get('/DescendantFonts',[f])
        for descendant in fs:
            fd=descendant.get_object().get('/FontDescriptor')
            embedded=bool(fd and any(k in fd.get_object() for k in ('/FontFile','/FontFile2','/FontFile3')))
            fonts[name]=embedded
for name,embedded in fonts.items():
    if not embedded:unembedded.append(name)
if unembedded:errors.append('Polices non incorporées : '+str(unembedded))
texfiles=[f for f in ROOT.rglob('*.tex') if 'build' not in f.relative_to(ROOT).parts and f.name!='controle-figures.tex']
src='\n'.join(f.read_text(encoding='utf-8') for f in texfiles)
metrics=dict(pages=len(d),taille=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
 figures_sources=len(list((ROOT/'figures').glob('*.tex'))),
 insertions_figures=len(re.findall(r'\\schema(?:\[[^\]]+\])?\{',src)),
 exercices=src.count(r'\begin{exercice}'),corriges=src.count(r'\begin{corrige}'),
 exercices_evaluations=src.count(r'\begin{exoBac}'),corriges_evaluations=src.count(r'\begin{corrigeBac}'),
 blocs_mesures=len(blocks),plus_grand_bloc_pt=max(float(h) for _,h in blocks),
 polices=len(fonts),polices_non_incorporees=unembedded,collisions=overlaps,erreurs=errors)
if metrics['exercices']!=240 or metrics['corriges']!=240:errors.append('Inventaire des exercices incomplet')
if metrics['exercices_evaluations']!=18 or metrics['corriges_evaluations']!=18:errors.append('Évaluations incomplètes')
(ROOT/'recherches/verification-pdf.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metrics,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
