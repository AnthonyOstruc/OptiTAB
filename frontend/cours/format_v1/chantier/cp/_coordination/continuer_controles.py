from pathlib import Path
import sys,subprocess,runpy,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OUTILS=ROOT.parents[1]/'outils'
mode=sys.argv[1];codes=[int(x) for x in sys.argv[2:]] or list(range(1,31))
for code in codes:
 d=next(ROOT.glob(f'{code:02}_*'))
 if mode=='figures':
  figs=runpy.run_path(str(d/'figures/figures.py'))['FIGURES']
  missing=[n for n in figs if not (d/'figures/images'/f'{n}.png').exists()]
  if missing:subprocess.run([sys.executable,'-X','utf8',str(OUTILS/'figures_livre.py'),str(d),*missing,'--jobs','1'],check=True,stdout=subprocess.DEVNULL)
 elif mode=='navigateur':
  # Regénérer l’aperçu depuis les textes actuels avant chaque audit.
  subprocess.run([sys.executable,'-X','utf8',str(HERE/'valider_cp.py'),str(code),'--navigateur'],check=True)
  subprocess.run([sys.executable,'-X','utf8',str(HERE/'planches_relecture_cp.py'),str(code)],check=True,stdout=subprocess.DEVNULL)
 else:raise ValueError(mode)
 print(mode,code,'OK',flush=True)
