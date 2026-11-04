from pathlib import Path
import subprocess,sys
ICI=Path(__file__).resolve().parent
for n in (11,12,13,14,20,21):
 d=next(ICI.parent.glob(f'{n:02}_*'));(d/'verif_math.py').write_bytes((ICI/'verifier_maths_root.py').read_bytes())
 subprocess.run([sys.executable,'-X','utf8',str(d/'verif_math.py')],check=True)
