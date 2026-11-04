"""Validation séquentielle : exactitude, moteur web, Chrome et captures."""
from pathlib import Path
import subprocess
import sys
import json

BASE=Path(__file__).resolve().parent.parent
OUTILS=BASE.parent.parent/'outils'
for code in range(int(sys.argv[1]) if len(sys.argv)>1 else 261,(int(sys.argv[2])+1) if len(sys.argv)>2 else 266):
    p=next(BASE.glob(f'{code}_*')); results={}
    commands=[
      ('mathematiques',[sys.executable,str(Path(__file__).with_name('verif_numerique.py')),str(p)]),
      ('mathematiques_revision',[sys.executable,str(Path(__file__).with_name('verif_revision_20261030.py')),str(p)]),
      ('validation_revision',[sys.executable,str(Path(__file__).with_name('verifier_local.py')),str(p),'--navigateur']),
      ('captures_revision',['node',str(Path(__file__).with_name('capturer_revision.mjs')),str(p)]),
    ]
    for name,cmd in commands:
        with (p/f'{name}.log').open('w',encoding='utf8') as log:
            r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,encoding='utf8',stdin=subprocess.DEVNULL)
        results[name]=r.returncode
        (p/'resultats_controles.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
        print(code,name,r.returncode,flush=True)
        if r.returncode: break
