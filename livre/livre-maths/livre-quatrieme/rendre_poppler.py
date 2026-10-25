"""Second moteur de rendu pour une sélection de pages critiques."""
from pathlib import Path
import re,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa/poppler';OUT.mkdir(exist_ok=True,parents=True)
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
labels=['cours-3-2','cours-10-2','exo-12-2','cor-12-3','cor-12-7','cor-12-15','cor-13-10','cor-13-8','cor-14-8','cor-14-15','exo-15-14','cor-15-15','cor-16-13','exo-17-4','cor-17-9','cor-17-10','cor-18-6','exo-18-15','defi-cor-16','preuves-3','preuves-4','references']
details=[]
for label in labels:
    n=int(pages[label])+1
    (OUT/(label+'.png')).unlink(missing_ok=True)
    run=subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','135','-singlefile','-png',str(ROOT/'main.pdf'),str(OUT/label)],capture_output=True)
    assert (OUT/(label+'.png')).exists(),run.stderr.decode(errors='replace')
    details.append(dict(label=label,page_pdf=n,fichier=label+'.png'))
rapport=dict(sha256=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest(),moteur='Poppler pdftoppm',pages=details)
(OUT/'rendus.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rapport,ensure_ascii=True,indent=2))
