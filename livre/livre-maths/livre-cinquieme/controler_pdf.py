"""Contrôle du document livré, renvois et rendus de chaque page."""
from pathlib import Path
import re,json,hashlib,sys
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa';OUT.mkdir(exist_ok=True)
pdf=fitz.open(ROOT/'main.pdf')
man=json.loads((ROOT/'manifeste-cinquieme.json').read_text(encoding='utf8'))
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
log=(ROOT/'build/main.log').read_text(encoding='utf8',errors='replace')
assert len(pdf)>250
for t in ['Overfull','undefined references','multiply defined','Missing character','Label(s) may have changed']:assert t not in log,t
ex=re.findall(r'\\newlabel\{exo-(\d+)-(\d+)\}',aux)
cor=re.findall(r'\\newlabel\{cor-(\d+)-(\d+)\}',aux)
assert len(ex)==len(cor)==300 and set(ex)==set(cor)
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
for f in man['figures']:assert pages[f['label']]==pages[f['texte']],f
for p in man['pages_annexes']:assert p['label'] in pages,p
for c in range(1,21):
    assert int(pages[f'exo-{c}-1'])-int(pages[f'chap-{c}'])==1+man['cours_par_chapitre'][c-1],(c,'pages de cours attendues')
blocs=re.findall(r'OTBLOC\|([^|]+)\|([\d.]+)pt',log)
assert len(blocs)==600
ed=re.findall(r'OTEDITION\|([^|]+)\|([\d.]+)pt',log)
assert len(ed)==len(man['pages_annexes']) and all(float(h)<=560 for _,h in ed)
bad=[];blank=[];notes=[];liens=0;tiles=[];texts=[]
for num,page in enumerate(pdf,1):
    t=page.get_text();texts.append(f'{num}: '+t[:120].replace('\n',' | '))
    if t.strip()=='Notes' and len(page.get_drawings())>=20:notes.append(num)
    elif len(t.strip())<12:blank.append(num)
    assert '??' not in t and '\ufffd' not in t,(num,'caractère ou renvoi')
    for parasite in ['oprule','midrule','bottomrule','extcolor']:
        assert parasite not in t,(num,parasite)
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for s in line['spans']:
                x0,y0,x1,y1=s['bbox']
                if x0<-.5 or y0<-.5 or x1>page.rect.width+.5 or y1>page.rect.height+.5:bad.append([num,s['text'],s['bbox']])
    for link in page.get_links():
        liens+=1
        if link['kind']==fitz.LINK_GOTO:assert 0<=link['page']<len(pdf),(num,link)
    if '--sans-rendu' not in sys.argv:
        pix=page.get_pixmap(dpi=100)
        pix.save(OUT/f'page-{num:03}.png')
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((280,400))
        tile=Image.new('RGB',(300,430),'#e6e8eb');tile.paste(im,((300-im.width)//2,20));ImageDraw.Draw(tile).text((8,4),str(num),fill='black');tiles.append(tile)
if tiles:
    for start in range(0,len(tiles),12):
        sheet=Image.new('RGB',(1200,1290),'white')
        for j,t in enumerate(tiles[start:start+12]):sheet.paste(t,((j%4)*300,(j//4)*430))
        sheet.save(OUT/f'planche-{start//12+1:02}.png')
report=dict(pages=len(pdf),liens=liens,signets=len(pdf.get_toc()),exercices=300,corriges=300,figures_avec_texte=len(man['figures']),blocs_lecture=len(blocs),pages_annexes=len(ed),max_bloc_pt=max(float(h) for _,h in blocs),pages_notes=notes,pages_blanches=blank,texte_hors_page=bad,sha256=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest())
(OUT/'controle-pdf.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'pages.txt').write_text('\n'.join(texts),encoding='utf8')
print(json.dumps(report,ensure_ascii=True,indent=2))
assert not blank and not bad
