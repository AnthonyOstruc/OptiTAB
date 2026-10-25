from pathlib import Path
import subprocess
from structure import write
from figures import F,produire_figures
ROOT=Path(__file__).resolve().parent
produire_figures()
s=(ROOT/'main.tex').read_text(encoding='utf-8').split(r'\begin{document}')[0]+r'\begin{document}\pagestyle{empty}'
for name in F:
    for mode in ('enonce','corrige'):
        s+=r'\clearpage\otPageTitre{'+name+'}{'+mode+r'}\begin{minipage}{153.5mm}\schema['+mode+']{'+name+r'}\end{minipage}'
s+=r'\end{document}'
write('controle-figures.tex',s)
(ROOT/'build').mkdir(exist_ok=True)
r=subprocess.run(['lualatex','-interaction=nonstopmode','-file-line-error','-aux-directory=build','controle-figures.tex'],cwd=ROOT,capture_output=True)
(ROOT/'build/controle-figures-console.txt').write_bytes(r.stdout+r.stderr)
log=(ROOT/'build/controle-figures.log').read_text(encoding='utf-8',errors='replace')
print(log[-1800:])
print('Overfull:',log.count('Overfull'),'Undefined:',log.count('Undefined control sequence'),'Errors:',log.count('Error:'))
