# -*- coding: utf-8 -*-
"""Exécute et conserve les vrais contrôles communs, sans changer les outils."""
from pathlib import Path
import os
import json
import subprocess
import sys

P=Path(__file__).resolve().parent
OUTILS=P.parents[2]/'outils'
env={**os.environ,'PYTHONIOENCODING':'utf-8'}
checks=[('validation.log',[sys.executable,str(P/'verifier_visible.py')]),('captures.log',['node',str(P/'controle_apercu_local.mjs'),str(P/'apercu.html'),str(P/'captures')]),('captures_complementaires.log',['node',str(P/'captures_complementaires.mjs')])]
state={}
for log,cmd in checks:
    with (P/log).open('w',encoding='utf8') as handle:
        result=subprocess.run(cmd,stdout=handle,stderr=subprocess.STDOUT,env=env)
    state[log]={'code':result.returncode}
    (P/'controle_statut.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(log, 'OK' if result.returncode==0 else 'ÉCHEC',flush=True)
    if result.returncode:
        print((P/log).read_text(encoding='utf8')[-5000:]);sys.exit(result.returncode)
