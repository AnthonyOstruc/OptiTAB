"""Contrôles séquentiels avec journaux persistants, sans tâche lourde parallèle."""
from pathlib import Path
import os,sys,subprocess,json
BASE=Path(__file__).resolve().parent.parent;OUTILS=BASE.parent.parent/'outils';env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
for code in range(271,276):
    d=next(BASE.glob(f'{code}_*'));results=[]
    commands=[('maths',[sys.executable,str(d/'verif_notion.py')]),('validation',[sys.executable,'-u',str(Path(__file__).parent/'verifier_local.py'),str(d)]),('captures',['node',str(Path(__file__).parent/'controle_apercu_local.mjs'),str(d/'apercu.html'),str(d/'captures')]),('capture_trois',['node',str(Path(__file__).parent/'capturer_troisieme.mjs'),str(d)])]
    for name,cmd in commands:
        print(code,name,'début',flush=True)
        with (d/f'controle_{name}.log').open('w',encoding='utf-8') as log:
            r=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT)
        results.append({'controle':name,'code_retour':r.returncode})
        (d/'resultat_controles.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(code,name,'OK' if r.returncode==0 else f'ÉCHEC {r.returncode}',flush=True)
        if r.returncode:break
