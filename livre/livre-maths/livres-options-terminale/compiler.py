from pathlib import Path
import subprocess,sys,hashlib,re,json,time
ROOT=Path(__file__).resolve().parents[1]
book=ROOT/('livre-maths-'+sys.argv[1])
records=[];last=None
for n in range(1,5):
    start=time.time()
    p=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory=build','main.tex'],cwd=book,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=p.stdout.decode('utf-8',errors='replace');(book/'build'/f'compilation-{n}.txt').write_text(log,encoding='utf-8')
    print(f'Passe {n} : code {p.returncode}, {time.time()-start:.1f} s',flush=True)
    if p.returncode:
        print(log[-2400:]);sys.exit(p.returncode)
    aux=(book/'build/main.aux').read_bytes();digest=hashlib.sha256(aux).hexdigest()
    records.append(dict(passe=n,aux=digest,duree=round(time.time()-start,2)))
    if n>=2 and digest==last and not re.search(r'Rerun to get|Label\(s\) may have changed',log):break
    last=digest
else:raise RuntimeError('Les renvois ne sont pas stabilisés après quatre passes.')
(book/'build/compilations.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('PDF stabilisé.',flush=True)
