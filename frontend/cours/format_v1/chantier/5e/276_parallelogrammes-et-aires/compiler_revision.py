# -*- coding: utf-8 -*-
"""Compilation séquentielle avec reprise des seules figures modifiées."""
from pathlib import Path
import json
import sys
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE.parent.parent/'outils'))
import figures_livre as fl
for code in range(276,281):
    p=next(BASE.glob(f'{code}_*'));m=fl.charger(p);build=p/'figures/build';out=p/'figures/images';report=[]
    for name,tex in m.FIGURES.items():
        png=out/f'{name}.png';sans=build/f'{name}__sans_texte.png';old=build/f'{name}.tex'
        if old.exists() and tex.strip() in old.read_text(encoding='utf8') and png.exists() and sans.exists() and sans.stat().st_mtime>=png.stat().st_mtime:
            errors,warnings=fl.chevauchements(png,sans);ok=not errors;details=errors+warnings
        else:
            _,ok,details=fl.compiler_un(name,tex,build,out,getattr(m,'XLAB',None),getattr(m,'PREAMBULE_EXTRA',''),getattr(m,'TOLERE',None))
        report.append({'figure':name,'ok':ok,'remarques':details})
        (p/'compilation_revision.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(code,name,'OK' if ok else details,flush=True)
    if m.FIGURES:fl.planche(p/'figures',list(m.FIGURES))
