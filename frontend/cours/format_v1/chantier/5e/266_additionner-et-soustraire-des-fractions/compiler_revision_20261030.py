"""Compile seulement les six figures nouvelles, sans effacer les précédentes."""
from pathlib import Path
import sys,json
from figures_revision_20261030 import NEW,BASE
sys.path.insert(0,str(BASE.parent.parent/'outils'))
import figures_livre as fl
for code,figs in NEW.items():
    if not figs:continue
    d=next(BASE.glob(f'{code}_*'));mod=fl.charger(d);fd=d/'figures'
    path=d/'compilation_figures.json'
    report=json.loads(path.read_text(encoding='utf-8'))
    report=[r for r in report if r['figure'] not in figs]
    for name in figs:
        _,ok,details=fl.compiler_un(name,mod.FIGURES[name],fd/'build',fd/'images',getattr(mod,'XLAB',None),getattr(mod,'PREAMBULE_EXTRA',''),getattr(mod,'TOLERE',None))
        report.append({'figure':name,'ok':ok,'remarques':details})
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(code,name,ok,details,flush=True)
    fl.planche(fd,list(mod.FIGURES))
