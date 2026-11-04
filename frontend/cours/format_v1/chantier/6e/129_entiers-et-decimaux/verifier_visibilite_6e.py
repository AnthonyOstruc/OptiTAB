"""Vérifie la visibilité publique des 26 notions, sans compte administrateur."""
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import json,datetime
ICI=Path(__file__).resolve().parent
publication=json.loads((ICI/'publication_6e.json').read_text(encoding='utf-8'))
tasks=[(r['notion'],base) for r in publication['imports'] for base in ('http://localhost:3000','https://optitab-backend.onrender.com')]
def check(item):
    notion,base=item
    try:
        request=Request(f'{base}/api/notions/{notion}/',headers={'Accept':'application/json'})
        with urlopen(request,timeout=45) as response:data=json.load(response)
        return {'notion':notion,'serveur':base,'ok':data.get('id')==notion}
    except Exception as error:
        return {'notion':notion,'serveur':base,'ok':False,'erreur':type(error).__name__}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,tasks))
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK' if all(r['ok'] for r in results) else 'a_verifier','controles':len(results),'resultats':results}
(ICI/'verification_visibilite_6e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('statut','controles')}))
if report['statut']!='OK':raise SystemExit(2)
