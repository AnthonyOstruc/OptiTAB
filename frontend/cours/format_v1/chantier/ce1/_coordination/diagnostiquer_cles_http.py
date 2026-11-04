from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
pub=json.loads((HERE/'publication_ce1.json').read_text(encoding='utf-8'))
for r in pub['imports']:
 t=(HERE.parent/r['dossier']/'exercices.txt').read_text(encoding='utf-8')
 print(r['numero'],repr(next(iter(r['exercices']))),re.findall(r'^Id:.*$',t,re.M)[:1])
