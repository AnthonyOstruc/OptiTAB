"""Contrôle le PDF livré, ses liens et ses blocs, puis rend toutes les pages."""
from pathlib import Path
import hashlib,json,re
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa';OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'manifeste-seconde.json').read_text(encoding='utf-8'))
pdf=fitz.open(ROOT/'main.pdf')
assert len(pdf)>200
aux=(ROOT/'build/main.aux').read_text(encoding='utf-8')
log=(ROOT/'build/main.log').read_text(encoding='utf-8',errors='replace')
for token in ['Overfull','undefined references','Missing character','multiply defined','Label(s) may have changed']:
    assert token not in log,token
labels=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
ex={k for k in labels if re.fullmatch(r'exo-\d+-\d+',k)}
cor={k for k in labels if re.fullmatch(r'cor-\d+-\d+',k)}
assert len(ex)==len(cor)==240
assert {k.replace('exo-','') for k in ex}=={k.replace('cor-','') for k in cor}
for pic in manifest['figures']:
    assert labels[pic['label']]==labels[pic['texte']],pic
for p in manifest['pages_annexes']:assert p['label'] in labels,p
blocks=re.findall(r'OTBLOC\|([^|]+)\|([\d.]+)pt',log)
extras=re.findall(r'OTEDITION\|([^|]+)\|([\d.]+)pt',log)
assert len(blocks)==480
assert len(extras)==len(manifest['pages_annexes'])
assert all(float(h)<=560 for k,h in extras)
for c in range(1,17):
    assert all(k in labels for k in [f'chap-{c}',f'ess-{c}',f'corchap-{c}'])
blank=[];notes=[];outside=[];links=0;tiles=[];pageindex=[]
for n,page in enumerate(pdf,1):
    text=page.get_text()
    assert '??' not in text,(n,'renvoi non résolu')
    assert not re.search(r'oprule|idrule|ottomrule|extbf|extit|ightarrow|egin\{',text),(n,'fragment de commande LaTeX visible')
    assert '\ufffd' not in text,(n,'caractère de remplacement')
    if text.strip()=='Notes':notes.append(n)
    elif len(text.strip())<12:blank.append(n)
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                x0,y0,x1,y1=span['bbox']
                if min(x0,y0)<-1 or x1>page.rect.width+1 or y1>page.rect.height+1:
                    outside.append([n,span['text'],span['bbox']])
    for link in page.get_links():
        links+=1
        if link['kind']==fitz.LINK_GOTO:assert 0<=link['page']<len(pdf)
    pix=page.get_pixmap(dpi=100);pix.save(OUT/f'page-{n}.png')
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.thumbnail((245,348))
    tile=Image.new('RGB',(260,375),'#ddd');tile.paste(im,((260-im.width)//2,22))
    ImageDraw.Draw(tile).text((8,4),str(n),fill='black');tiles.append(tile)
    pageindex.append({'page_physique':n,'debut':text[:130]})
    if n%50==0:print(f'Rendu : {n}/{len(pdf)}',flush=True)
for start in range(0,len(tiles),12):
    sheet=Image.new('RGB',(1040,1125),'#ddd')
    for j,t in enumerate(tiles[start:start+12]):sheet.paste(t,((j%4)*260,(j//4)*375))
    sheet.save(OUT/f'planche-{start//12+1}.png')
report={'pages':len(pdf),'exercices_chapitres':240,'defis':16,'bilans':2,
 'automatismes_bilans':20,'problemes_bilans':6,'signets':len(pdf.get_toc()),'liens':links,
 'blocs_chapitres':len(blocks),'blocs_annexes':len(extras),
 'bloc_chapitre_max_pt':max(float(h) for k,h in blocks),'bloc_annexe_max_pt':max(float(h) for k,h in extras),
 'figures_avec_leur_texte':len(manifest['figures']),'pages_vides':blank,'pages_notes':notes,
 'texte_hors_page':outside,'sha256':hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest()}
(OUT/'controle-pdf.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'index-pages.json').write_text(json.dumps({'pages':pageindex,'labels':{k:int(v)+1 for k,v in labels.items()}},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
assert not blank and not outside
assert links>=480 and len(pdf.get_toc())>=70
