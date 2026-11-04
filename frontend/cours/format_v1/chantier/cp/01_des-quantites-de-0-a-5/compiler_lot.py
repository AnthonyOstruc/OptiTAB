from pathlib import Path
import sys,subprocess,json,os
ROOT=Path(__file__).resolve().parent.parent
ALLOWED=[1,2,3,7,8,9,10,13]
codes=list(map(int,sys.argv[1:])) or ALLOWED
assert set(codes)<=set(ALLOWED)
env=dict(os.environ,PYTHONIOENCODING='utf-8')
for code in codes:
 d=next(ROOT.glob(f'{code:02}_*'))
 run=subprocess.run([sys.executable,str(ROOT.parents[1]/'outils/figures_livre.py'),str(d),'--jobs','1'],capture_output=True,text=True,encoding='utf-8',env=env)
 (d/'compilation_figures.log').write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
 (d/'compilation_figures.json').write_text(json.dumps({'retour':run.returncode,'commande':'figures_livre.py --jobs 1'},ensure_ascii=False),encoding='utf-8')
 print(code,'retour',run.returncode,flush=True)
 if run.returncode:
  print((run.stdout+'\n'+run.stderr)[-5000:],flush=True);sys.exit(run.returncode)
