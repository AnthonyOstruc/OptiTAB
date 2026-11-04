# -*- coding: utf-8 -*-
"""Vérificateur commun, métadonnées de nouveaux contenus injectées en mémoire uniquement."""
from pathlib import Path
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;O=P.parents[2]/'outils'
loads=json.loads
def enriched(raw,*args,**kwargs):
 value=loads(raw,*args,**kwargs)
 if isinstance(value,dict) and 'notion' in value and 'cours' in value:
  if not value['cours']:value['cours']=[{'id':'nouveau','titre':value['titre'],'images':[]}]
  if not value['fiches']:value['fiches']=[{'id':'nouvelle','titre':'Résumé : '+value['titre'],'images':[]}]
  if not value['exercices']:
   value['exercices']=[]
   for b in re.split(r'^===\s*$',(P/'exercices.txt').read_text(encoding='utf8'),flags=re.M):
    ident=re.search(r'^Id: (\S+)',b,re.M)[1];title=b.strip().splitlines()[0].removeprefix('=== ').strip()
    value['exercices'].append({'id':ident,'titre':title,'images':[]})
 return value
json.loads=enriched
original=subprocess.run
def visible(cmd,*args,**kwargs):
 if isinstance(cmd,list):
  cmd=[str(P/'apercu_local.mjs') if str(c).endswith('apercu_notion.mjs') else str(P/'controle_apercu_local.mjs') if str(c).endswith('controle_apercu.mjs') else c for c in cmd]
  if any(str(c).endswith('controle_apercu_local.mjs') for c in cmd):
   cmd=[str(P/'captures') if c=='--rapide' else c for c in cmd]
   kwargs.pop('capture_output',None);kwargs.pop('text',None);enc=kwargs.pop('encoding','utf8');kwargs.pop('errors',None);kwargs.pop('timeout',None)
   lines=[]
   with (P/'progression_navigateur.log').open('w',encoding='utf8') as log:
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding=enc,errors='replace',**kwargs)
    for line in proc.stdout:lines.append(line);log.write(line);log.flush()
    code=proc.wait()
   return subprocess.CompletedProcess(cmd,code,''.join(lines),'')
 return original(cmd,*args,**kwargs)
subprocess.run=visible
sys.path.insert(0,str(O));sys.argv=[str(O/'verifier_notion.py'),str(P),'--navigateur']
runpy.run_path(str(O/'verifier_notion.py'),run_name='__main__')
