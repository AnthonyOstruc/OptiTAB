from pathlib import Path
import subprocess,time,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
BUILD=HERE/'build';BUILD.mkdir(exist_ok=True)
last=None;records=[]
for n in range(1,5):
    start=time.time()
    p=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory=build','main.tex'],cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=p.stdout.decode('utf8',errors='replace')
    (BUILD/f'compilation-{n}.txt').write_text(log,encoding='utf8')
    print(f'Passe {n} : code {p.returncode}, {time.time()-start:.1f} s',flush=True)
    if p.returncode:
        print(log[-3500:]);sys.exit(p.returncode)
    digest=hashlib.sha256((BUILD/'main.aux').read_bytes()).hexdigest()
    records.append(dict(passe=n,duree=round(time.time()-start,2),aux=digest))
    if n>=2 and digest==last and not re.search(r'Rerun to get|Label\(s\) may have changed',log):break
    last=digest
else:raise RuntimeError('Renvois non stabilises apres quatre passes.')
(BUILD/'compilations.json').write_text(json.dumps(records,indent=2),encoding='utf8')
print('Compilation stabilisee.',flush=True)
