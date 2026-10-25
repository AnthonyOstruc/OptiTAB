"""Régénère toutes les sources dans un dossier isolé et compare à l'identique."""
from pathlib import Path
import json,shutil,subprocess,sys,tempfile,hashlib,datetime
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
tmp=Path(tempfile.mkdtemp(prefix='reproduction-sixieme-'))
for p in ROOT.glob('*.py'):shutil.copy2(p,tmp/p.name)
shutil.copytree(ROOT/'_modele_collection',tmp/'_modele_collection')
shutil.copytree(ROOT/'images',tmp/'images')
run=subprocess.run([sys.executable,'-X','utf8','construire.py'],cwd=tmp,capture_output=True)
assert run.returncode==0,run.stderr.decode(errors='replace')[-2000:]
identiques=0;differences=[]
for sub in ['chapitres','corriges','annexes','liminaires','couverture','figures']:
    for p in sorted((tmp/sub).glob('*')):
        orig=ROOT/sub/p.name
        if not orig.exists():differences.append(f'{sub}/{p.name} absent de l’original');continue
        if sha(p)==sha(orig):identiques+=1
        else:differences.append(f'{sub}/{p.name} différent')
for name in ['main.tex','plan.tex','optitab-livre.sty','manifeste-sixieme.json']:
    if sha(tmp/name)==sha(ROOT/name):identiques+=1
    else:differences.append(name+' différent')
report=dict(date=str(datetime.date.today()),fichiers_reproduits_identiques=identiques,differences=differences,dependance_autres_livres=False,repertoire_test=str(tmp))
(ROOT/'build/controle-reproduction.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True,indent=2))
assert not differences
