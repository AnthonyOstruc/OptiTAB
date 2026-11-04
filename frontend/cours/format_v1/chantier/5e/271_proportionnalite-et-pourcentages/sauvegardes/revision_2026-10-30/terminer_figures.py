"""Reprise séquentielle du lot 271–275, sans supprimer aucun fichier."""
from pathlib import Path
import sys,json
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE.parent.parent/'outils'))
import figures_livre as fl
for code in range(272,276):
    d=next(BASE.glob(f'{code}_*'));mod=fl.charger(d);fd=d/'figures';build=fd/'build';images=fd/'images';report=[]
    for name,tex in mod.FIGURES.items():
        png=images/f'{name}.png';sans=build/f'{name}__sans_texte.png'
        expected=fl.PREAMBULE+getattr(mod,'PREAMBULE_EXTRA','')+'\n\\begin{document}\n'+fl.graduations_x(tex,name,getattr(mod,'XLAB',None))+'\n\\end{document}\n'
        built=build/f'{name}.tex'
        if png.exists() and sans.exists() and sans.stat().st_mtime>=png.stat().st_mtime and built.read_text(encoding='utf-8')==expected:
            errors,warnings=fl.chevauchements(png,sans)
            if fl.taille_png(png)[0]>fl.LARGEUR_MAX_PX:errors.append('largeur excessive')
            ok=not errors;details=errors+warnings
        else:
            _,ok,details=fl.compiler_un(name,tex,build,images,getattr(mod,'XLAB',None),getattr(mod,'PREAMBULE_EXTRA',''),getattr(mod,'TOLERE',None))
        report.append({'figure':name,'ok':ok,'remarques':details})
        (d/'compilation_figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(code,name,'OK' if ok else details,flush=True)
    print(code,'TERMINÉ',flush=True)
