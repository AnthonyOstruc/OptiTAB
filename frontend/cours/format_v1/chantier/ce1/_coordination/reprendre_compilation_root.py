from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OUTILS=ROOT.parents[1]/'outils'
d=next(ROOT.glob('28_*'))
with (d/'compilation_figures.log').open('a',encoding='utf-8') as log:
 log.write('\nCorrection : lettre C déplacée hors de la diagonale ; nouvelle compilation.\n');log.flush()
 cp=subprocess.run([sys.executable,'-X','utf8',str(OUTILS/'figures_livre.py'),str(d),'triangle_a_reproduire','--jobs','1'],stdout=log,stderr=subprocess.STDOUT)
assert cp.returncode==0,'28 : consulter le journal'
print('28 correction compilée OK',flush=True)
subprocess.run([sys.executable,'-X','utf8',str(HERE/'compiler_root.py'),'29','30'],check=True)
