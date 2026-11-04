# -*- coding: utf-8 -*-
"""Reprise et contrôles strictement séquentiels du lot 276 à 280."""
from pathlib import Path
import json
import subprocess
import sys

BASE=Path(__file__).resolve().parent.parent
OUTILS=BASE.parent.parent/'outils'
sys.path.insert(0,str(OUTILS))
import figures_livre as fl

for code in range(276,281):
    d=next(BASE.glob(f'{code}_*')); mod=fl.charger(d)
    fd=d/'figures'; build=fd/'build'; images=fd/'images'; report=[]
    for name,tex in mod.FIGURES.items():
        png=images/f'{name}.png'; sans=build/f'{name}__sans_texte.png'
        source_ok=(build/f'{name}.tex').exists() and tex.strip() in (build/f'{name}.tex').read_text(encoding='utf8')
        if source_ok and png.exists() and sans.exists() and sans.stat().st_mtime>=png.stat().st_mtime:
            errors,warnings=fl.chevauchements(png,sans)
            if fl.taille_png(png)[0]>fl.LARGEUR_MAX_PX:errors.append('largeur excessive')
            ok=not errors;details=errors+warnings
        else:
            _,ok,details=fl.compiler_un(name,tex,build,images,getattr(mod,'XLAB',None),getattr(mod,'PREAMBULE_EXTRA',''),getattr(mod,'TOLERE',None))
        report.append({'figure':name,'ok':ok,'remarques':details})
        (d/'compilation_figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(code,name,'OK' if ok else details,flush=True)
        if not ok:sys.exit(2)
    if mod.FIGURES:fl.planche(fd,list(mod.FIGURES))
    # Aucun nouveau processus lourd n'est lancé avant la fin du précédent.
    result=subprocess.run([sys.executable,str(d/'controle_final.py')])
    if result.returncode:sys.exit(result.returncode)
    print(code,'CONTRÔLES TERMINÉS',flush=True)
