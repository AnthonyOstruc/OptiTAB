# -*- coding: utf-8 -*-
"""Contrôle ciblé après les derniers ajustements de tableaux et de sous-titre."""
from pathlib import Path
import json
import os
import subprocess
import sys
BASE=Path(__file__).resolve().parent.parent;OUTILS=BASE.parent.parent/'outils'
env={**os.environ,'PYTHONIOENCODING':'utf-8'}
for code in [276,277,278]:
    p=next(BASE.glob(f'{code}_*'));status={}
    cmds=[('validation_documents.log',[sys.executable,str(OUTILS/'verifier_notion.py'),str(p)]),('captures_documents.log',['node',str(p/'controle_apercu_local.mjs'),str(p/'apercu.html'),str(p/'captures'),'--documents'])]
    for log,cmd in cmds:
        with (p/log).open('w',encoding='utf8') as f:
            result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,env=env)
        status[log]=result.returncode
        (p/'controle_documents_statut.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(code,log,result.returncode,flush=True)
        if result.returncode:sys.exit(result.returncode)
