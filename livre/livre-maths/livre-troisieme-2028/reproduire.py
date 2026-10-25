"""Reconstruit le livre dans un dossier isolé à partir des seules sources, puis compare.

Usage : python reproduire.py [dossier_temporaire]
Les sources (sans build ni __pycache__) sont copiées, la chaîne complète est
exécutée, puis les fichiers LaTeX générés et les rendus de pages sont comparés
à ceux du dossier courant. Le résultat est écrit dans build/controle-reproduction.json.
"""
from pathlib import Path
import shutil,subprocess,sys,json,hashlib,os,tempfile
import fitz
ROOT=Path(__file__).resolve().parent
dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.mkdtemp(prefix='repro-3e-2028-'))/'livre'
if dest.exists():shutil.rmtree(dest)
shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('build','__pycache__','main.pdf'))
env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
for script in ['verifier_contenu.py','verifier_figures.py','construire.py','compiler.py']:
    r=subprocess.run([sys.executable,script],cwd=dest,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    assert r.returncode==0,(script,r.stdout[-2000:],r.stderr[-2000:])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
differents=[]
compares=0
for p in sorted(ROOT.rglob('*')):
    rel=p.relative_to(ROOT)
    if p.is_file() and rel.parts[0] not in ('build','__pycache__') and p.suffix in ('.tex','.sty','.json','.png'):
        compares+=1
        q=dest/rel
        if not q.exists() or sha(p)!=sha(q):differents.append(rel.as_posix())
a=fitz.open(ROOT/'main.pdf');b=fitz.open(dest/'main.pdf')
rendus=len(a)==len(b) and all(a[i].get_pixmap(dpi=60).samples==b[i].get_pixmap(dpi=60).samples for i in range(len(a)))
textes=len(a)==len(b) and all(a[i].get_text()==b[i].get_text() for i in range(len(a)))
rapport=dict(dossier=str(dest),fichiers_compares=compares,fichiers_differents=differents,sources_identiques=not differents,
             pages=len(b),rendus_identiques=rendus,textes_identiques=textes,
             remarque='Les empreintes des PDF peuvent différer par la date de création ; les rendus et les textes sont comparés page par page.')
(ROOT/'build/controle-reproduction.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rapport,ensure_ascii=True,indent=2))
assert not differents and rendus and textes
