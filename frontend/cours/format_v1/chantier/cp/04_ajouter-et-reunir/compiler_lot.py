from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parent.parent
TOOL=ROOT.parents[1]/'outils/figures_livre.py'
for code in [4,5,6,11,12,14,15,16,30]:
 d=next(ROOT.glob(f'{code:02}_*'))
 p=subprocess.run([sys.executable,'-X','utf8',str(TOOL),str(d),'--jobs','1','--planche'],capture_output=True,text=True,encoding='utf-8')
 (d/'compilation_figures.log').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
 (d/'compilation_figures.json').write_text(json.dumps({'retour':p.returncode,'jobs':1,'commande':'figures_livre.py --jobs 1 --planche'})+'\n',encoding='utf-8')
 print(code,'retour',p.returncode,flush=True)
 if p.returncode:print(p.stdout[-2500:],p.stderr[-1500:],flush=True);sys.exit(p.returncode)
