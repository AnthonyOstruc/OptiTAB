from pathlib import Path
import runpy,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
for code in map(int,sys.argv[1:]):
 d=next(ROOT.glob(f'{code:02}_*'));n=len(runpy.run_path(str(d/'figures/figures.py'))['FIGURES'])
 log=d/'compilation_figures.log'
 while not log.exists() or f'{n}/{n} figure(s) produite(s)' not in log.read_text(encoding='utf-8'):
  time.sleep(5)
 subprocess.run([sys.executable,'-X','utf8',str(HERE/'continuer_controles.py'),'navigateur',str(code)],check=True)
