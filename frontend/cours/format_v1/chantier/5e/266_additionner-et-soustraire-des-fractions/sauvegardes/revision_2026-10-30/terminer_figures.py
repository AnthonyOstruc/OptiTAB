"""Reprise séquentielle, sans supprimer les figures déjà produites et contrôlées."""
from pathlib import Path
import sys
import json
import time

BASE=Path(__file__).resolve().parent.parent
OUTILS=BASE.parent.parent/'outils'
sys.path.insert(0,str(OUTILS))
import figures_livre as fl

for code in range(266,271):
    d=next(BASE.glob(f'{code}_*')); mod=fl.charger(d)
    fd=d/'figures'; build=fd/'build'; images=fd/'images'
    report=[]
    for name,tex in mod.FIGURES.items():
        png=images/f'{name}.png'; sans=build/f'{name}__sans_texte.png'
        # Une compilation interrompue est reprise uniquement si nécessaire.
        source=build/f'{name}.tex'
        extra=getattr(mod,'PREAMBULE_EXTRA','')
        attendu=fl.PREAMBULE+extra+'\n\\begin{document}\n'+fl.graduations_x(tex,name,getattr(mod,'XLAB',None))+'\n\\end{document}\n'
        if png.exists() and sans.exists() and source.exists() and source.read_text(encoding='utf-8')==attendu and sans.stat().st_mtime>=png.stat().st_mtime:
            errors,warnings=fl.chevauchements(png,sans)
            if fl.taille_png(png)[0]>fl.LARGEUR_MAX_PX:errors.append('largeur excessive')
            ok=not errors
            details=errors+warnings
        else:
            _,ok,details=fl.compiler_un(name,tex,build,images,getattr(mod,'XLAB',None),getattr(mod,'PREAMBULE_EXTRA',''),getattr(mod,'TOLERE',None))
        report.append({'figure':name,'ok':ok,'remarques':details})
        (d/'compilation_figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(code,name,'OK' if ok else details,flush=True)
    fl.planche(fd,list(mod.FIGURES))
    print(code,'TERMINÉ',flush=True)
