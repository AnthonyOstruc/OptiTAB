"""Audit officiel complet et captures ciblées dans la même session Chrome."""
from pathlib import Path
import sys,subprocess,json,os
BASE=Path(__file__).resolve().parent.parent
ICI=Path(__file__).resolve().parent
OUTILS=BASE.parent.parent/'outils'
source=(OUTILS/'controle_apercu.mjs').read_text(encoding='utf-8')
source=source.replace('const here = path.dirname(fileURLToPath(import.meta.url))','const here = '+json.dumps(str(OUTILS)))
source=source.replace('await browser.close()',"await Promise.race([browser.close(),new Promise(r=>setTimeout(r,2000))])")
source=source.replace("querySelectorAll('mjx-merror')","querySelectorAll('mjx-merror, .mjx-merror, [data-mjx-error]')")
source=source.replace('(i === 1 || (i === 0 && k < 2))',"(JSON.parse(process.env.OPTITAB_CAPTURE_CHOIX || '[2,7,14,20]').includes(k) && i < 2)")
source=source.replace("['enonce', 'etapes', 'solution'][i]}.png`) })","['enonce', 'etapes', 'solution'][i]}.png`), style: '.ap-top{visibility:hidden!important}' })")
local=ICI/'controle_revision_20261030.mjs';local.write_text(source,encoding='utf-8')
sys.path.insert(0,str(OUTILS))
import verifier_notion
run=subprocess.run
def local_run(args,*a,**kw):
    if isinstance(args,list) and len(args)>1 and Path(args[1]).name=='controle_apercu.mjs':
        d=Path(args[2]).parent
        args=[args[0],str(local),args[2],str(d/'captures_revision_20261030')]
        r=run(args,*a,**kw)
        (d/'revision_navigateur.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
        return r
    return run(args,*a,**kw)
verifier_notion.subprocess.run=local_run
for code in map(int,sys.argv[1:] or range(266,271)):
    d=next(BASE.glob(f'{code}_*'))
    selection=[2,7,14,20]
    if code>270:
        path=d/('revision_pedagogique.json' if code<=275 else 'revision_2026-10-30.json')
        newids={str(e['id']) for e in json.loads(path.read_text(encoding='utf-8'))['remplacements']}
        import re
        bs=[b for b in re.split(r'^===[ \t]*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M) if b.strip()]
        groups={k:[] for k in ('easy','medium','hard')}
        for i,b in enumerate(bs):
            if re.search(r'^Id: (.+)',b,re.M)[1] in newids:groups[re.search(r'^Difficulté: (.+)',b,re.M)[1]].append(i)
        selection=sorted(set([groups[k][0] for k in groups if groups[k]]+[groups['hard'][-1]]))
    os.environ['OPTITAB_CAPTURE_CHOIX']=json.dumps(selection)
    (d/'selection_captures_revision.json').write_text(json.dumps([i+1 for i in selection])+'\n',encoding='utf-8')
    with (d/'revision_validation.log').open('w',encoding='utf-8') as log:
        import contextlib
        with contextlib.redirect_stdout(log):problems=verifier_notion.verifier(d,navigateur=True)
    (d/'controles_revision_20261030.json').write_text(json.dumps({'verification':len(problems),'date':'2026-10-30'},indent=2)+'\n',encoding='utf-8')
    print(code,'OK' if not problems else problems,flush=True)
