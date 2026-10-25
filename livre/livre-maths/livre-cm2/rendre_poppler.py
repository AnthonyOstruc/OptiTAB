"""Rendu indépendant de pages critiques avec Poppler."""
from pathlib import Path
import re,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa/poppler';OUT.mkdir(exist_ok=True,parents=True)
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
labels=['cours-1-1','cours-5-1','cours-6-2','cours-12-1','cours-13-1','cours-16-3','cours-17-2','cours-18-2','cours-21-2','exo-1-7','exo-12-7','cor-12-7','exo-13-6','cor-13-6','cor-15-5','cor-15-6','cor-16-9','cor-16-11','cor-17-4','cor-17-7','cor-17-13','exo-18-7','cor-18-9','cor-18-14','exo-20-13','cor-21-8','defi-cor-11','bilan-B-cor-2','references']
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
