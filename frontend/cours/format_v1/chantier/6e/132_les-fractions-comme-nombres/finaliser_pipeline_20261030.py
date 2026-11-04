"""Reprend seulement les figures modifiées, puis contrôle le lot en série."""
from pathlib import Path
import subprocess,sys
h=Path(__file__).resolve().parent
for script,logname in [('compiler_lot_20261030.py','compilation_reprise.log'),('verif_mathematiques_20261030.py','mathematiques_revision.log'),('valider_lot_20261030.py','validation_lot.log')]:
    with (h/logname).open('w',encoding='utf-8') as log:
        p=subprocess.run([sys.executable,str(h/script)],stdout=log,stderr=log,stdin=subprocess.DEVNULL)
    print(script,p.returncode,flush=True)
    if p.returncode:break
