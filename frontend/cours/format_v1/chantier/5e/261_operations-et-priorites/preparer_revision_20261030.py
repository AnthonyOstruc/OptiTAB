"""Sauvegarde non destructive avant la révision pédagogique du 30 octobre."""
from pathlib import Path
import shutil
import json
BASE=Path(__file__).resolve().parent.parent
for n in range(261,266):
    p=next(BASE.glob(f'{n}_*')); dest=p/'sauvegardes/revision_2026-10-30'
    dest.mkdir(parents=True,exist_ok=True)
    for item in p.iterdir():
        if item.is_file() and item.suffix in {'.txt','.json','.md','.py','.mjs','.log','.html'}:
            if not (dest/item.name).exists(): shutil.copy2(item,dest/item.name)
    if not (dest/'figures').exists(): shutil.copytree(p/'figures',dest/'figures')
    (p/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'calculs-revision','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(n,'sauvegarde conservée',flush=True)
