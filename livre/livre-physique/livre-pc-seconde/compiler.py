"""Compile et stabilise le livre en conservant les journaux de chaque passe."""
from pathlib import Path
import hashlib,re,subprocess,shutil
ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build'
BUILD.mkdir(exist_ok=True)
SNAP=BUILD/'compilation-isolee'
SNAP.mkdir(exist_ok=True)
(SNAP/'build').mkdir(exist_ok=True)
sources=[p for p in ROOT.rglob('*') if p.is_file() and 'build' not in p.relative_to(ROOT).parts and p.suffix in ('.tex','.sty','.png','.dat','.pdf')]
source_hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
for p in sources:
    target=SNAP/p.relative_to(ROOT)
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,target)
def aux_hash():
    p=SNAP/'build/main.aux'
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
for index in range(1,6):
    before=aux_hash()
    print(f'Compilation, passe {index}...',flush=True)
    run=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-aux-directory=build','main.tex'],cwd=SNAP,capture_output=True)
    output=(run.stdout+run.stderr).decode('utf-8',errors='replace')
    (BUILD/f'compilation-complete-{index}.txt').write_text(output,encoding='utf-8')
    log=(SNAP/'build/main.log').read_text(encoding='utf-8',errors='replace')
    # MiKTeX peut sortir avec un code de maintenance non nul alors que le PDF
    # a été produit. Le journal de la compilation fait foi pour ce contrôle.
    if 'Output written on main.pdf' not in log or 'Fatal error' in log:
        raise RuntimeError('Compilation interrompue. Consulter build/compilation-isolee/build/main.log.\n'+output[-2500:])
    unstable=any(t in log for t in ('Label(s) may have changed','undefined references'))
    if not unstable and before==aux_hash():
        print('Renvois et pagination stabilisés.',flush=True)
        break
else:
    raise RuntimeError('Les renvois ne sont pas stabilisés après cinq passes.')
for token in ('Overfull','Missing character','multiply defined'):
    if token in log:
        raise RuntimeError(f'Contrôle typographique à reprendre : {token}')
assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in source_hashes.items()),'Les sources ont changé pendant la compilation : relancer pour inclure les modifications.'
shutil.copy2(SNAP/'main.pdf',ROOT/'main.pdf')
for suffix in ('.aux','.log','.out'):
    p=SNAP/'build'/('main'+suffix)
    if p.exists():
        shutil.copy2(p,BUILD/p.name)
print(re.search(r'Output written on main.pdf[^\n]*',log).group(0),flush=True)

