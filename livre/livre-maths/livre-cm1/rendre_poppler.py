"""Rendu indépendant de pages critiques avec Poppler."""
from pathlib import Path
import re,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa/poppler';OUT.mkdir(exist_ok=True,parents=True)
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
labels=['cours-1-2','cours-5-2','cours-6-1','cours-8-2','cours-13-2','cours-14-1','cours-16-3','cours-18-3','cours-21-1','exo-1-8','exo-13-1','cor-13-9','exo-14-1','cor-14-2','exo-15-11','cor-15-11','cor-16-3','cor-16-8','cor-17-5','cor-17-12','exo-18-9','cor-18-15','exo-20-4','cor-20-10','exo-21-13','defi-cor-14','bilan-B-cor-2','references']
details=[]
for label in labels:
    n=int(pages[label])+1
    (OUT/(label+'.png')).unlink(missing_ok=True)
    run=subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','135','-singlefile','-png',str(ROOT/'main.pdf'),str(OUT/label)],capture_output=True)
    assert (OUT/(label+'.png')).exists(),run.stderr.decode(errors='replace')
    details.append(dict(label=label,page_pdf=n,fichier=label+'.png'))
report=dict(sha256=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest(),moteur='Poppler pdftoppm',pages=details)
(OUT/'rendus.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True,indent=2))
