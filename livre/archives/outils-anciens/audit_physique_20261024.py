"""Inventaire de relecture des figures et des consignes, sans modifier les livres."""
from pathlib import Path
import json, re, hashlib, shutil
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tmp/pdfs/audit-physique-20261024'
OUT.mkdir(parents=True, exist_ok=True)

def latex_blocks(path, env):
    text = path.read_text(encoding='utf-8')
    return re.findall(r'\\begin\{' + env + r'\}.*?\\end\{' + env + r'\}', text, re.S)

def figures(s):
    return re.findall(r'\\schema(?:\[[^\]]+\])?\{([^}]+)\}', s)

def inventory():
    records = []
    for book in ('premiere', 'terminale'):
        folder = ROOT / ('livre-pc-' + book)
        for p in sorted((folder/'chapitres').glob('*.tex')):
            cor = folder/'corriges'/p.name
            answers = latex_blocks(cor, 'corrige') if cor.exists() else []
            for i, block in enumerate(latex_blocks(p, 'exercice'), 1):
                answer = answers[i-1] if i <= len(answers) else ''
                needs = re.findall(r'.{0,100}(?:[Tt]rac[ée]|[Rr]epr[ée]sent|[Dd]essin|[Cc]ompl[ée]t|[Ss]ch[ée]ma|[Cc]ourbe|[Gg]raphique|[Dd]iagramme).{0,200}', block)
                records.append(dict(book=book, file=p.relative_to(ROOT).as_posix(), n=i,
                                    statement=block, answer=answer,
                                    figures=figures(block), correction_figures=figures(answer),
                                    signals=needs))
    (OUT/'exercices-lycee.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    selected = [r for r in records if r['signals'] and (not r['figures'] or not r['correction_figures'])]
    lines=[]
    for r in selected:
        lines.append(f"\n{r['book']} {Path(r['file']).name} EX {r['n']} : énoncé={r['figures']}, corrigé={r['correction_figures']}\n"+'\n'.join(r['signals']))
    (OUT/'consignes-a-relire.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(dict(exercices=len(records), consignes_a_relire=len(selected)), ensure_ascii=False))

def render(book, pdf):
    dest = OUT/book
    dest.mkdir(exist_ok=True)
    doc=fitz.open(pdf)
    problems=[]
    for index,page in enumerate(doc):
        # Le contrôle des limites ne remplace pas la relecture des figures.
        for b in page.get_text('dict')['blocks']:
            if b['type'] != 0: continue
            for line in b['lines']:
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    if span['text'].strip() and (x0 < -1 or y0 < -1 or x1>page.rect.width+1 or y1>page.rect.height+1):
                        problems.append(dict(page=index+1,text=span['text'],bbox=span['bbox']))
        target=dest/f'p{index+1:04}.png'
        if not target.exists() or target.stat().st_mtime < Path(pdf).stat().st_mtime:
            page.get_pixmap(matrix=fitz.Matrix(.65,.65), alpha=False).save(target)
    sheets=[]
    for start in range(0,len(doc),20):
        sheet=Image.new('RGB',(5*390,4*575),'#dce2e8')
        draw=ImageDraw.Draw(sheet)
        for k in range(20):
            n=start+k
            if n>=len(doc): break
            im=Image.open(dest/f'p{n+1:04}.png');im.thumbnail((380,540))
            x=(k%5)*390;y=(k//5)*575
            sheet.paste(im,(x+(390-im.width)//2,y+25));draw.text((x+10,y+6),str(n+1),fill='black')
        target=dest/f'planche-{start//20+1:02}.jpg'
        sheet.save(target,quality=90);sheets.append(str(target))
    report=dict(book=book,pdf=str(pdf),pages=len(doc),sha256=hashlib.sha256(Path(pdf).read_bytes()).hexdigest(),hors_page=problems,planches=sheets)
    (dest/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['planches']},ensure_ascii=False))

if __name__=='__main__':
    import sys
    if len(sys.argv)==1: inventory()
    else: render(sys.argv[1],Path(sys.argv[2]))
