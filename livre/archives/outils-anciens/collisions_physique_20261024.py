"""Repère des collisions de légendes à examiner visuellement, sans auto-correction."""
from pathlib import Path
import json,re,sys
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp/pdfs/audit-physique-20261024'

def candidates(pdf):
    doc=fitz.open(pdf);result=[]
    for n,p in enumerate(doc):
        spans=[s for b in p.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']
               if len(re.findall(r'[A-Za-zÀ-ÿ]',s['text']))>=4 and s['size']>=6.5]
        for i,s in enumerate(spans):
            r=fitz.Rect(s['bbox'])
            for t in spans[i+1:]:
                q=fitz.Rect(t['bbox']);hit=r&q
                if hit.is_empty:continue
                if hit.width>4 and hit.height>min(r.height,q.height)*.45 and hit.get_area()>min(r.get_area(),q.get_area())*.16:
                    result.append(dict(page=n+1,a=s['text'],b=t['text'],bbox=list(hit)))
    return result

if __name__=='__main__':
    targets=[Path(p) for p in sys.argv[1:]]
    for p in targets:
        found=candidates(p)
        name=p.parent.name+'-'+p.stem[:25]
        (OUT/('collisions-'+name+'.json')).write_text(json.dumps(found,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(dict(pdf=str(p),candidats=found),ensure_ascii=False))
