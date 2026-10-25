"""Rendu indépendant de pages critiques avec Poppler."""
from pathlib import Path
import re,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa/poppler';OUT.mkdir(exist_ok=True,parents=True)
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
labels=['cours-1-1','cours-3-2','cours-5-2','cours-9-2','cours-13-2','cours-15-1','cours-16-2','cours-17-2','cours-18-2','cours-21-2','exo-2-8','exo-4-6','cor-4-6','exo-13-12','cor-13-12','exo-14-6','cor-14-6','exo-15-3','exo-15-4','cor-15-13','cor-16-10','cor-16-13','cor-17-6','cor-17-13','exo-18-6','cor-18-10','cor-18-14','cor-20-7','cor-21-15','defi-cor-11','bilan-B-cor-2','references']
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
