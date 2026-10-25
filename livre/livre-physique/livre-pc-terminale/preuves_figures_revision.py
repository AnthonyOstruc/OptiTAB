"""Compile les figures à part pour corriger le dessin avant la compilation du livre."""
from pathlib import Path
import json,subprocess
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build/qa-revision-figures'
BUILD.mkdir(exist_ok=True)
names=['12-ex11']+['rev-'+n for n in json.loads((ROOT/'build/revision-figures.json').read_text(encoding='utf-8'))['figures']]
s=(ROOT/'main.tex').read_text(encoding='utf-8').split(r'\begin{document}')[0]+r'\begin{document}\pagestyle{empty}'+'\n'
for name in names:s+='\\noindent\\textbf{'+name+'}\\par\\bigskip\n\\schema[corrige]{'+name+'}\n\\clearpage\n'
s+='\\end{document}\n'
(BUILD/'preuves.tex').write_text(s,encoding='utf-8')
r=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-jobname=preuves','-output-directory='+str(BUILD),'\\input{'+str(BUILD/'preuves.tex').replace('\\','/')+'}'],cwd=ROOT,capture_output=True)
log=(r.stdout+r.stderr).decode('utf-8',errors='replace');(BUILD/'compilation.txt').write_text(log,encoding='utf-8')
assert 'Output written on' in log and 'Fatal error' not in log,log[-2000:]
doc=fitz.open(BUILD/'preuves.pdf')
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(BUILD/(names[i]+'.png'))
print(len(doc),'figures rendues')
