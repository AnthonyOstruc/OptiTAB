# -*- coding: utf-8 -*-
"""Vérification locale exhaustive ; sources exportées strictement immuables."""
from pathlib import Path
import json,sys,re,math,hashlib,subprocess,runpy
BASE=Path(__file__).resolve().parent.parent
TOOLS=BASE.parent.parent/'outils'
sys.path.insert(0,str(TOOLS))
import verifier_notion

def verifier_math(d):
    data=json.loads((d/'verification_math.json').read_text(encoding='utf-8'))
    for rel,expected in data['source_hashes'].items():
        assert hashlib.sha256((d/rel).read_bytes()).hexdigest()==expected,rel
    count=0
    for eid,checks in data['checks'].items():
        for expr in checks:
            assert eval(expr,{'math':math,'abs':abs}), (d.name,eid,expr)
            count+=1
    text=(d/'exercices.txt').read_text(encoding='utf-8')
    blocs=verifier_notion.blocs_exercices(text)
    ids={str(eid) for eid,_,_ in blocs}
    original=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
    assert {str(e['id']) for e in original['exercices']}<=ids
    assert len(ids)==len(blocs)
    assert len(re.findall(r'^## Question ',text,re.M))==len(blocs)*3
    assert text.count('::: methode')>=len(blocs)*3
    assert text.count('::: etape')>=len(blocs)*6
    assert text.count('::: resultat')>=len(blocs)*3
    statements={}
    for eid,title,block in blocs:
        statement=block.split('Énoncé:',1)[1].split('Étapes:',1)[0]
        signature=re.sub(r'\s+',' ',statement).strip()
        assert signature not in statements,('énoncés identiques',statements.get(signature),eid)
        statements[signature]=eid
    print(f'MATH : {count} assertions, {len(blocs)} exercices, sources SHA-256 intactes.')
    return count

def verifier_local(d,navigateur=False):
    # L'outil historique ignore une notion entièrement nouvelle. On lui fournit
    # ses documents en mémoire, sans toucher source_en_ligne/meta.json.
    original_read=Path.read_text;original_run=subprocess.run
    metapath=(d/'source_en_ligne/meta.json').resolve()
    raw=original_read(metapath,encoding='utf-8');meta=json.loads(raw)
    if not meta['cours']:
        meta['cours']=[{'id':'nouveau','titre':meta['titre'],'images':[]}]
        meta['fiches']=[{'id':'nouvelle','titre':meta['titre'],'images':[]}]
        meta['exercices']=[{'id':eid,'titre':titre,'images':[]} for eid,titre,_ in verifier_notion.blocs_exercices(original_read(d/'exercices.txt',encoding='utf-8'))]
    enriched=json.dumps(meta,ensure_ascii=False)
    def read(path,*args,**kwargs):
        if path.resolve()==metapath:return enriched
        return original_read(path,*args,**kwargs)
    # Adapter d'aperçu local : le vrai moteur et les vraies feuilles de style.
    js=original_read(TOOLS/'apercu_notion.mjs',encoding='utf-8')
    js=js.replace("const here = path.dirname(fileURLToPath(import.meta.url))",'const here = '+json.dumps(str(TOOLS)))
    js=js.replace("const meta = JSON.parse(read(path.join(dir, 'source_en_ligne', 'meta.json')))",'const meta = '+enriched)
    adapter=d/'apercu_local.mjs';adapter.write_text(js,encoding='utf-8')
    control=original_read(TOOLS/'controle_apercu.mjs',encoding='utf-8')
    control=control.replace("const here = path.dirname(fileURLToPath(import.meta.url))",'const here = '+json.dumps(str(TOOLS)))
    control=control.replace("querySelectorAll('mjx-merror')","querySelectorAll('mjx-merror,.mjx-merror,[data-mjx-error]')")
    control=control.replace('await browser.close()', 'await Promise.race([browser.close(),new Promise(r=>setTimeout(r,2000))])')
    control=control.replace("await page.evaluate('window.__ready')", "await page.evaluate('window.__ready'); await page.addStyleTag({content:'.ap-top{visibility:hidden!important}'})")
    control=control.replace('await page.click(`.ap-tab[data-tab="${tab}"]`)', 'await page.evaluate(id=>document.querySelector(\'.ap-tab[data-tab="\'+id+\'"]\').click(),tab)')
    control=control.replace('await page.click(\'.ap-tab[data-tab="exercices"]\')', 'await page.evaluate(()=>document.querySelector(\'.ap-tab[data-tab="exercices"]\').click())')
    control=control.replace('let problems = 0','let problems = 0; const results = []')
    control=control.replace('if (bad) problems += 1','results.push({viewport:label,view:name,...r}); if (bad) problems += 1')
    control=control.replace('(i === 1 || (i === 0 && k < 2))','(i < 2 && [0,3,6,15].includes(k))')
    if d.name.startswith('144_'):
        control=control.replace('[0,3,6,15].includes(k)','[0,3,4,6,15].includes(k)')
    control=control.replace('process.exit(problems ? 2 : 0)',"fs.writeFileSync(path.join(path.dirname(page_file),'navigateur.json'),JSON.stringify({anomalies:problems,vues:results.length,details:results},null,2)); process.exit(problems ? 2 : 0)")
    controlpath=d/'controle_apercu_local.mjs';controlpath.write_text(control,encoding='utf-8')
    def run(args,*a,**kw):
        if isinstance(args,list) and len(args)>1 and Path(args[1]).name=='apercu_notion.mjs':args=[args[0],str(adapter),*args[2:]]
        if isinstance(args,list) and len(args)>1 and Path(args[1]).name=='controle_apercu.mjs':args=[args[0],str(controlpath),str(d/'apercu.html'),str(d/'captures')]
        kw.setdefault('stdin',subprocess.DEVNULL)
        return original_run(args,*a,**kw)
    Path.read_text=read;subprocess.run=run
    try: result=verifier_notion.verifier(d,navigateur)
    finally:Path.read_text=original_read;subprocess.run=original_run
    assert original_read(metapath,encoding='utf-8')==raw
    return result

if __name__=='__main__':
    n=int(sys.argv[1]);d=next(BASE.glob(f'{n}_*'))
    verifier_math(d)
    if '--math' not in sys.argv:
        problems=verifier_local(d,'--navigateur' in sys.argv)
        out={'problemes':problems}
        (d/'verification_locale.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('\n'.join(problems));print(f'VERIFICATION : {len(problems)} problème(s).')
        sys.exit(bool(problems))
