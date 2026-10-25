from pathlib import Path
import sys,json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1]
option=sys.argv[1];book=ROOT/('livre-maths-'+option)
r=json.loads((book/'build/verification.json').read_text(encoding='utf8'))
m=json.loads((book/'build/calculs-verifies.json').read_text(encoding='utf8'))
assert all(c['valide'] for c in r['controles']) and m['echecs']==0
pdf=book/'build/main.pdf';sha=hashlib.sha256(pdf.read_bytes()).hexdigest();assert sha==r['sha256']
assert (book/'build/validation-visuelle.json').exists(),'Contrôle visuel à terminer avant publication.'
v=json.loads((book/'build/validation-visuelle.json').read_text(encoding='utf8'));assert v['sha256']==sha and v['valide']
name=f'OptiTAB - Mathématiques - Terminale - Mathématiques {r["option"]} - Manuel complet.pdf'
targets=[ROOT/'output/pdf/France/Mathématiques'/name,Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')/name]
for target in targets:
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(pdf,target)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==sha
report=dict(option=r['option'],pages=r['pages'],sha256=sha,livraisons=[str(t.resolve()) for t in targets])
out=ROOT/'output/verification'/f'maths-{option}-livraison.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
