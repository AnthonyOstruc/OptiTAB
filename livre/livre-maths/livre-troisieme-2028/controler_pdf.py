"""Contrôle du document livré, renvois et rendus de chaque page."""
from pathlib import Path
import re,json,hashlib,sys
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa';OUT.mkdir(parents=True,exist_ok=True)
pdf=fitz.open(ROOT/'main.pdf')
man=json.loads((ROOT/'manifeste-troisieme-2028.json').read_text(encoding='utf8'))
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
log=(ROOT/'build/main.log').read_text(encoding='utf8',errors='replace')
assert len(pdf)>250
for t in ['Overfull','undefined references','multiply defined','Missing character','Label(s) may have changed']:assert t not in log,t
ex=re.findall(r'\\newlabel\{exo-(\d+)-(\d+)\}',aux)
cor=re.findall(r'\\newlabel\{cor-(\d+)-(\d+)\}',aux)
assert len(ex)==len(cor)==270 and set(ex)==set(cor)
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
for f in man['figures']:assert pages[f['label']]==pages[f['texte']],f
for p in man['pages_annexes']:assert p['label'] in pages,p
for c in range(1,19):
    assert int(pages[f'exo-{c}-1'])-int(pages[f'chap-{c}'])==3,(c,'deux pages de cours attendues')
blocs=re.findall(r'OTBLOC\|([^|]+)\|([\d.]+)pt',log)
assert len(blocs)==540
ed=re.findall(r'OTEDITION\|([^|]+)\|([\d.]+)pt',log)
assert len(ed)==len(man['pages_annexes']) and all(float(h)<=560 for _,h in ed)
# Mentions propres à l’édition précédente qui ne doivent plus apparaître.
interdits=['Brevet 2027','2026-2027','latitude','homothétie de','triangles semblables sont']
bad=[];blank=[];notes=[];liens=0;tiles=[];texts=[];mentions=[]
for num,page in enumerate(pdf,1):
    t=page.get_text();texts.append(f'{num}: '+t[:120].replace('\n',' | '))
    if t.strip()=='Notes' and len(page.get_drawings())>=20:notes.append(num)
    elif len(t.strip())<12:blank.append(num)
    assert '??' not in t and '\ufffd' not in t,(num,'caractère ou renvoi')
    for parasite in ['oprule','midrule','bottomrule','extcolor']:
        assert parasite not in t,(num,parasite)
    for mot in interdits:
        if mot in t.replace('\n',' '):mentions.append([num,mot])
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
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((400,566))
        tile=Image.new('RGB',(420,600),'#e6e8eb');tile.paste(im,((420-im.width)//2,26));ImageDraw.Draw(tile).text((8,6),str(num),fill='black');tiles.append(tile)
if tiles:
    for old in OUT.glob('planche-*.png'):old.unlink()
    for start in range(0,len(tiles),6):
        sheet=Image.new('RGB',(1260,1200),'white')
        for j,t in enumerate(tiles[start:start+6]):sheet.paste(t,((j%3)*420,(j//3)*600))
        sheet.save(OUT/f'planche-{start//6+1:02}.png')
report=dict(pages=len(pdf),liens=liens,signets=len(pdf.get_toc()),exercices=270,corriges=270,figures_avec_texte=len(man['figures']),blocs_lecture=len(blocs),pages_annexes=len(ed),max_bloc_pt=max(float(h) for _,h in blocs),pages_notes=notes,pages_blanches=blank,texte_hors_page=bad,mentions_obsoletes=mentions,planches=(len(pdf)+5)//6,sha256=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest())
(OUT/'controle-pdf.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'pages.txt').write_text('\n'.join(texts),encoding='utf8')
print(json.dumps(report,ensure_ascii=True,indent=2))
assert not blank and not bad and not mentions
