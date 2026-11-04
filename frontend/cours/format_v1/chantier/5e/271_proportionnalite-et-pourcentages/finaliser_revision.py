"""Finalisation notion par notion : figures, maths, navigateur et captures en séquence."""
from pathlib import Path
import sys,os,json,subprocess
D=Path(__file__).resolve().parent;BASE=D.parent;OUTILS=BASE.parent.parent/'outils';sys.path.insert(0,str(OUTILS));import figures_livre as fl
env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
canonical=lambda s:'\n'.join(x for x in s.splitlines() if x.strip())
failures=[]
for code in ([int(x) for x in sys.argv[1:]] or range(271,276)):
 d=next(BASE.glob(f'{code}_*'));m=fl.charger(d);fd=d/'figures';build=fd/'build';images=fd/'images';report=[]
 for name,tex in m.FIGURES.items():
  png=images/f'{name}.png';sans=build/f'{name}__sans_texte.png';built=build/f'{name}.tex';expected=fl.PREAMBULE+'\n\\begin{document}\n'+tex+'\n\\end{document}\n'
  if png.exists() and sans.exists() and built.exists() and sans.stat().st_mtime>=png.stat().st_mtime and canonical(built.read_text(encoding='utf-8'))==canonical(expected):
   errors,warnings=fl.chevauchements(png,sans);ok=not errors;details=errors+warnings
   if fl.taille_png(png)[0]>fl.LARGEUR_MAX_PX:ok=False;details.append('largeur excessive')
  else:_,ok,details=fl.compiler_un(name,tex,build,images)
  report.append({'figure':name,'ok':ok,'remarques':details});(d/'compilation_figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(code,name,'OK' if ok else details,flush=True)
 if not all(x['ok'] for x in report):failures.append(code);continue
 print(code,'QA DÉBUT',flush=True)
 r=subprocess.run([sys.executable,'-u',str(D/'valider_lot.py'),str(code)],env=env,stdin=subprocess.DEVNULL)
 if r.returncode:failures.append(code)
 print(code,'QA FIN',flush=True)
print('Figures en échec :',failures,flush=True)
