"""Une seule compilation active ; reprise uniquement des sorties absentes ou modifiées."""
from pathlib import Path
import sys,json
BASE=Path(__file__).resolve().parent.parent
OUTILS=BASE.parent.parent/'outils';sys.path.insert(0,str(OUTILS))
import figures_livre as fl
import planche as pl
d=next(BASE.glob('136_*'))
output=d/'planches';output.mkdir(exist_ok=True)
if not (output/'planche_01.png').exists():
    sources=[(f'{genre} {eid} · {im["position"]}',pl.telecharger(d,im)) for genre,eid,im in pl.images(d)]
    for k in range(0,len(sources),24):pl.composer(sources[k:k+24],output/f'planche_{k//24+1:02d}.png')
for n in (132,134,135,136,137,284,285):
    d=next(BASE.glob(str(n)+'_*'));mod=fl.charger(d);fd=d/'figures';build=fd/'build';images=fd/'images';report=[]
    for name,tex in mod.FIGURES.items():
        png=images/(name+'.png');sans=build/(name+'__sans_texte.png');src=build/(name+'.tex')
        expected=fl.PREAMBULE+'\n\\begin{document}\n'+tex+'\n\\end{document}\n'
        reusable=png.exists() and sans.exists() and src.exists() and src.read_text(encoding='utf-8')==expected and sans.stat().st_mtime>=png.stat().st_mtime
        ok=False;details=[]
        if reusable:
            errors,warnings=fl.chevauchements(png,sans);ok=not errors and fl.taille_png(png)[0]<=fl.LARGEUR_MAX_PX;details=errors+warnings
        if not ok:_,ok,details=fl.compiler_un(name,tex,build,images,None,'',None)
        report.append(dict(figure=name,ok=ok,remarques=details))
        (d/'compilation_figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(n,name,'OK' if ok else details,flush=True)
    if mod.FIGURES:fl.planche(fd,list(mod.FIGURES))
    print(n,'TERMINE',flush=True)
