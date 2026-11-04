"""Dessine les graduations blanches après les courbes pour garder les chiffres nets.

Seules les graduations d'axes utilisent le fond blanc autorisé par le guide.
Les lettres des points ne sont ni masquées ni déplacées sur les traits.
"""
from pathlib import Path
import sys,re,json,shutil
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE.parent.parent/'outils'))
import figures_livre as fl
for code in (272,275):
    d=next(BASE.glob(f'{code}_*'));mod=fl.charger(d);fd=d/'figures'
    report=json.loads((d/'compilation_figures.json').read_text(encoding='utf-8'))
    names=[e['figure'] for e in report if not e['ok']]
    fixes={}
    for name in names:
        lines=mod.FIGURES[name].splitlines()
        ticks=[line for line in lines if line.startswith(r'\node[coteTexte,')]
        lines=[line for line in lines if line not in ticks]
        pos=next((i for i,line in enumerate(lines) if line.startswith(r'\fill[')),len(lines)-2)
        lines[pos:pos]=ticks
        fixes[name]='\n'.join(lines)
    if fixes:
        backup=fd/'figures_avant_graduations_20261030.py'
        if not backup.exists():shutil.copyfile(fd/'figures.py',backup)
        with (fd/'figures.py').open('a',encoding='utf-8') as f:
            f.write('\n# Dernière correction de lisibilité des graduations.\nFIGURES.update({\n')
            for name,tex in fixes.items():f.write(f'{name!r}: r"""{tex}""",\n')
            f.write('})\n')
        for name,tex in fixes.items():
            _,ok,details=fl.compiler_un(name,tex,fd/'build',fd/'images')
            item=next(e for e in report if e['figure']==name);item.update(ok=ok,remarques=details)
            (d/'compilation_figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(code,name,ok,details,flush=True)
    fl.planche(fd,list(mod.FIGURES))
