# -*- coding: utf-8 -*-
"""Un seul passage complet 130 vues : audit commun et captures simultanément."""
from pathlib import Path
import os,json,subprocess,sys,shutil
P=Path(__file__).resolve().parent;env={**os.environ,'PYTHONIOENCODING':'utf-8'};state={}
for log,cmd in [('validation.log',[sys.executable,str(P/'verifier_visible.py')]),('captures_complementaires.log',['node',str(P/'captures_complementaires.mjs')])]:
 with (P/log).open('w',encoding='utf8') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
 state[log]={'code':r.returncode}
 if log=='validation.log':
  if (P/'progression_navigateur.log').exists():shutil.copy2(P/'progression_navigateur.log',P/'captures.log')
  state['captures.log']={'code':r.returncode,'origine':'Même passage navigateur : audits et captures.'}
 (P/'controle_statut.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf8')
 print(log,r.returncode,flush=True)
 if r.returncode:print((P/log).read_text(encoding='utf8')[-6000:]);sys.exit(r.returncode)
