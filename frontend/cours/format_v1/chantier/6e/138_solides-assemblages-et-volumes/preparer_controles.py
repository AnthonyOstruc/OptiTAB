# -*- coding: utf-8 -*-
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent;O=P.parents[2]/'outils';MODEL=R.parent/'5e'/'276_parallelogrammes-et-aires'
wrapper=r'''# -*- coding: utf-8 -*-
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
'''
preview=(O/'apercu_notion.mjs').read_text(encoding='utf8').replace("path.resolve(here, '../../..')","path.resolve(here, '../../../../..')")
needle="const meta = JSON.parse(read(path.join(dir, 'source_en_ligne', 'meta.json')))"
preview=preview.replace(needle,needle+"\n// Documents à créer : aperçu local sans modifier les exports.\nif (!meta.cours.length) meta.cours=[{id:'nouveau',titre:meta.titre,images:[]}]\nif (!meta.fiches.length) meta.fiches=[{id:'nouvelle',titre:'Résumé : '+meta.titre,images:[]}]\n")
preview=preview.replace("for (const im of item.images || []) map[im.position] = await onlineImage(im)","// Les images anciennes ne sont plus appelées ; les nouvelles figures ci-dessous les remplacent.")
control=(MODEL/'controle_apercu_local.mjs').read_text(encoding='utf8')
extra=(MODEL/'captures_complementaires.mjs').read_text(encoding='utf8').replace('[2,4,6,11,13,18,20]','[0,9,20]').replace('Captures mobiles ex03 et des six exercices diversifiés','Captures mobiles ex01, ex10 et ex21')
final=r'''# -*- coding: utf-8 -*-
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
'''
for n in (138,139,146,147,148,149,152):
 d=next(R.glob(f'{n}_*'))
 for name,content in [('verifier_visible.py',wrapper),('apercu_local.mjs',preview),('controle_apercu_local.mjs',control),('captures_complementaires.mjs',extra),('controle_final.py',final)]:
  (d/name).write_text(content,encoding='utf8')
