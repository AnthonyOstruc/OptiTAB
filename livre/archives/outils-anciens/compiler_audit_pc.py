"""Compilation isolée de la version de Première déjà rédigée (12 chapitres)."""
from pathlib import Path
import subprocess,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'tmp/pdfs/audit-physique-20261024/premiere-sources'
BUILD=TARGET/'build'
for n in range(1,5):
    aux=BUILD/'main.aux'
    before=hashlib.sha256(aux.read_bytes()).hexdigest() if aux.exists() else None
    print('Première isolée, passe',n,flush=True)
    run=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-aux-directory=build','main.tex'],cwd=TARGET,capture_output=True)
    output=(run.stdout+run.stderr).decode('utf-8',errors='replace')
    (BUILD/f'compilation-{n}.txt').write_text(output,encoding='utf-8')
    log=(BUILD/'main.log').read_text(encoding='utf-8',errors='replace')
    assert 'Output written on main.pdf' in log and 'Fatal error' not in log,output[-2000:]
    after=hashlib.sha256(aux.read_bytes()).hexdigest()
    if before==after and not any(t in log for t in ['Label(s) may have changed','undefined references']):break
else:raise RuntimeError('Pagination non stabilisée')
assert not any(t in log for t in ['Overfull','Missing character','multiply defined'])
print(re.search(r'Output written on main.pdf[^\n]*',log).group(),flush=True)
