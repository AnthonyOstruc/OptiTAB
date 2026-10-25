"""Second moteur de rendu pour une sélection de pages critiques."""
from pathlib import Path
import re,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build/qa/poppler';OUT.mkdir(parents=True,exist_ok=True)
aux=(ROOT/'build/main.aux').read_text(encoding='utf8')
pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
labels=['nouveautes','exo-2-15','cor-5-5','exo-8-12','exo-10-12','cor-10-8','cor-11-11','cor-12-13','exo-12-15',
        'exo-13-11','cor-13-12','exo-15-1','cor-15-9','cor-15-10','exo-16-7','cor-16-14','exo-17-15','cor-17-14',
        'defi-ex-15','defi-cor-13','bilan-A-ex-2','bilan-B-cor-4','preuves-3','outils-2','couverture-programme','references']
details=[]
for old in OUT.glob('*.png'):old.unlink()
for label in labels:
    n=int(pages[label])+1
    run=subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','135','-singlefile','-png',str(ROOT/'main.pdf'),str(OUT/label)],capture_output=True)
    assert (OUT/(label+'.png')).exists(),run.stderr.decode(errors='replace')
    details.append(dict(label=label,page_pdf=n,fichier=label+'.png'))
rapport=dict(sha256=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest(),moteur='Poppler pdftoppm',pages=details)
(OUT/'rendus.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rapport,ensure_ascii=True,indent=2))
