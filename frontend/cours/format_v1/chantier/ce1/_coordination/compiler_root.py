from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OUTILS=ROOT.parents[1]/'outils'
for code in [int(x) for x in sys.argv[1:]] or range(21,31):
 d=next(ROOT.glob(f'{code:02}_*'))
 with (d/'compilation_figures.log').open('w',encoding='utf-8') as log:
  cp=subprocess.run([sys.executable,'-X','utf8',str(OUTILS/'figures_livre.py'),str(d),'--jobs','1'],stdout=log,stderr=subprocess.STDOUT)
 assert cp.returncode==0,(code,'Consulter compilation_figures.log')
 print(code,'compilation officielle OK',flush=True)
