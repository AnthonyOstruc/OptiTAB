"""Contrôles séquentiels du lot 266–270, journaux conservés par notion."""
from pathlib import Path
import subprocess
import sys
import os
import json

BASE=Path(__file__).resolve().parent.parent
OUTILS=BASE.parent.parent/'outils'
ICI=Path(__file__).resolve().parent
env=dict(os.environ,PYTHONIOENCODING='utf-8')
for code in range(266,271):
    d=next(BASE.glob(f'{code}_*'))
    status=d/'controles.json'
    checks=json.loads(status.read_text(encoding='utf-8')) if status.exists() else {}
    for name,args in [
        ('verification_math',[sys.executable,str(d/'verif_math.py')]),
        ('verification',[sys.executable,str(ICI/'verifier_local.py'),str(d)]),
        ('controle_captures',['node',str(ICI/'controle_apercu_local.mjs'),str(d/'apercu.html'),str(d/'captures')]),
    ]:
        if checks.get(name)==0:
            print(code,name,'déjà OK',flush=True)
            continue
        with (d/(name+'.log')).open('w',encoding='utf-8') as log:
            r=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,env=env)
        checks[name]=r.returncode
        (d/'controles.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
        print(code,name,r.returncode,flush=True)
    print(code,'CONTRÔLES TERMINÉS',flush=True)
