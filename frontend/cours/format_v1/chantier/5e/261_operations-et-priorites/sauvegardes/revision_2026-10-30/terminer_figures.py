"""Reprise séquentielle des figures 261–265, sans effacer les sorties existantes."""
from pathlib import Path
import sys
import json

BASE=Path(__file__).resolve().parent.parent
OUTILS=BASE.parent.parent/'outils'
sys.path.insert(0,str(OUTILS))
import figures_livre as fl

for code in range(261,266):
    p=next(BASE.glob(f'{code}_*')); mod=fl.charger(p)
    fd=p/'figures'; build=fd/'build'; images=fd/'images'; report=[]
    for name,tex in mod.FIGURES.items():
        png=images/f'{name}.png'; sans=build/f'{name}__sans_texte.png'; texfile=build/f'{name}.tex'
        extra=getattr(mod,'PREAMBULE_EXTRA',''); xlab=getattr(mod,'XLAB',None)
        expected=fl.PREAMBULE+extra+'\n\\begin{document}\n'+fl.graduations_x(tex,name,xlab)+'\n\\end{document}\n'
        fresh=texfile.exists() and texfile.read_text(encoding='utf8')==expected
        reusable=png.exists() and sans.exists() and fresh and sans.stat().st_mtime>=png.stat().st_mtime
        details=[]; ok=False
        if reusable:
            errors,warnings=fl.chevauchements(png,sans)
            if fl.taille_png(png)[0]>fl.LARGEUR_MAX_PX: errors.append('largeur excessive')
            ok=not errors; details=errors+warnings
        if not ok:
            _,ok,details=fl.compiler_un(name,tex,build,images,xlab,extra,getattr(mod,'TOLERE',None))
        report.append({'figure':name,'ok':ok,'remarques':details})
        (p/'compilation_figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(code,name,'OK' if ok else details,flush=True)
    if mod.FIGURES: fl.planche(fd,list(mod.FIGURES))
    print(code,'TERMINÉ',flush=True)
