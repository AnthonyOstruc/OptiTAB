from pathlib import Path
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent.parent
rows=[]
for d in sorted(ROOT.iterdir()):
    if not (d/'source_en_ligne/meta.json').exists():continue
    m=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
    r={'notion':m['notion'],'titre':m['titre'],'cours':len(m['cours']),'fiches':len(m['fiches']),'exercices':len(m['exercices']),'images':sum(len(x['images']) for g in ('cours','fiches','exercices') for x in m[g]),'dossier':d.name}
    rows.append(r);print(json.dumps(r,ensure_ascii=False))
(ROOT/'129_entiers-et-decimaux/inventaire_initial_6e.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('TOTAL', {k:sum(r[k] for r in rows) for k in ('cours','fiches','exercices','images')})
