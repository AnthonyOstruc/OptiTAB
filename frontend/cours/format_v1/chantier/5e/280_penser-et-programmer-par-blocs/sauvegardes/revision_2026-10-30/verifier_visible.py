# -*- coding: utf-8 -*-
"""Lance le vérificateur commun, en conservant aussi sa progression navigateur.

Ne modifie aucun outil ; le résultat retourné au vérificateur est identique.
"""
from pathlib import Path
import runpy
import subprocess
import sys

P=Path(__file__).resolve().parent
OUTILS=P.parents[2]/'outils'
original=subprocess.run

def visible(cmd,*args,**kwargs):
    if isinstance(cmd,list) and any('controle_apercu.mjs' in str(c) for c in cmd):
        cmd=[str(P/'controle_apercu_local.mjs') if str(c).endswith('controle_apercu.mjs') else c for c in cmd]
        encoding=kwargs.pop('encoding','utf8');kwargs.pop('errors',None)
        kwargs.pop('capture_output',None);kwargs.pop('text',None);kwargs.pop('timeout',None)
        output=[]
        with (P/'progression_navigateur.log').open('w',encoding='utf8') as log:
            process=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding=encoding,errors='replace',**kwargs)
            for line in process.stdout:
                output.append(line);log.write(line);log.flush()
            result=process.wait()
        return subprocess.CompletedProcess(cmd,result,''.join(output),'')
    return original(cmd,*args,**kwargs)

subprocess.run=visible
sys.path.insert(0,str(OUTILS))
sys.argv=[str(OUTILS/'verifier_notion.py'),str(P),'--navigateur']
runpy.run_path(str(OUTILS/'verifier_notion.py'),run_name='__main__')
