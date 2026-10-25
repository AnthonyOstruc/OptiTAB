"""Rendu indépendant de pages critiques avec Poppler."""
from pathlib import Path
import re,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa/poppler';OUT.mkdir(exist_ok=True,parents=True)
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
labels=['cours-1-2','cours-7-1','cours-9-1','cours-13-2','cours-14-2','cours-14-3','cours-14-4','cours-17-2','cours-18-1','cor-12-6','exo-13-10','cor-13-15','exo-14-2','cor-14-2','cor-14-3','cor-14-9','cor-14-15','cor-15-6','cor-15-10','cor-16-8','cor-17-9','cor-17-10','cor-17-15','cor-18-14','cor-20-6','cor-20-9','cor-20-10','cor-20-13','defi-cor-14','bilan-B-cor-2','references',
# Pages revues lors de l'audit de conformité du 23 octobre 2026.
'cours-3-1','cours-3-2','exo-3-10','cor-3-10','cours-10-1','cours-10-2','exo-10-6','cor-10-6','exo-11-1','cor-11-1',
'cours-13-1','exo-13-14','cor-13-14','cours-14-3','cours-14-4','cor-14-12','cours-15-2','exo-15-15','cor-15-15',
'cours-16-1','cours-17-4','exo-17-14','cor-17-14','cours-18-2','exo-18-9','cor-18-9','exo-19-1','cor-19-3',
'defi-ex-3','defi-cor-3','bilan-B-auto','bilan-B-cor-auto','couverture-programme']
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
