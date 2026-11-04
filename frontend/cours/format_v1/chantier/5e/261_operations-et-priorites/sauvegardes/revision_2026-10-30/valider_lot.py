"""Validation séquentielle : exactitude, moteur web, Chrome et captures."""
from pathlib import Path
import subprocess
import sys
import json

BASE=Path(__file__).resolve().parent.parent
OUTILS=BASE.parent.parent/'outils'
for code in range(int(sys.argv[1]) if len(sys.argv)>1 else 261,266):
    p=next(BASE.glob(f'{code}_*')); results={}
    commands=[
      ('mathematiques',[sys.executable,str(Path(__file__).with_name('verif_numerique.py')),str(p)]),
      ('validation',[sys.executable,str(Path(__file__).with_name('verifier_local.py')),str(p),'--navigateur']),
      ('captures',['node',str(Path(__file__).with_name('controle_apercu_local.mjs')),str(p/'apercu.html'),str(p/'captures')]),
      ('capture_troisieme',['node',str(Path(__file__).with_name('capture_troisieme.mjs')),str(p)]),
    ]
    for name,cmd in commands:
        with (p/f'{name}.log').open('w',encoding='utf8') as log:
            r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,encoding='utf8')
        results[name]=r.returncode
        (p/'resultats_controles.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
        print(code,name,r.returncode,flush=True)
        if r.returncode: break
