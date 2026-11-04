# -*- coding: utf-8 -*-
"""Trois dégagements d'étiquettes constatés à la relecture des PNG."""
from pathlib import Path
import runpy,re
p=Path(__file__).parent/'figures/figures.py'
f=runpy.run_path(str(p))['FIGURES']
f['symetrie_5_1']=f['symetrie_5_1'].replace('(0,-1)--(0,5)','(0,-.5)--(0,5)')
for old,new in [
 (r'\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0)',r'\node[anchor=east,text=otInk,inner sep=4pt] at (-.45,0)'),
 (r'\node[anchor=north west,text=otInk,inner sep=4pt] at (4,0)',r'\node[anchor=west,text=otInk,inner sep=4pt] at (4.45,0)'),
 (r'\node[anchor=south west,text=otInk,inner sep=4pt] at (4,4)',r'\node[anchor=west,text=otInk,inner sep=4pt] at (4.45,4)'),
 (r'\node[anchor=south east,text=otInk,inner sep=4pt] at (0,4)',r'\node[anchor=east,text=otInk,inner sep=4pt] at (-.45,4)'),
]: f['symetrie_7_2']=f['symetrie_7_2'].replace(old,new)
f['symetrie_7_3']=f['symetrie_7_3'].replace(r'\node[anchor=south west,text=otInk,inner sep=4pt] at (3.0,4.0)',r'\node[anchor=west,text=otInk,inner sep=4pt] at (3.4,4.0)')
p.write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(f)+'\n',encoding='utf-8')
textpath=Path(__file__).parent/'exercices.txt'
text=textpath.read_text(encoding='utf-8')
text=re.sub(r'\$(\d+)\$ carreau\(x\)',lambda m:'$'+m[1]+'$ '+('carreau' if m[1]=='1' else 'carreaux'),text)
textpath.write_text(text,encoding='utf-8')
