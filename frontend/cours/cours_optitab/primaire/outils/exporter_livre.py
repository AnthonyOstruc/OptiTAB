"""Exporte les sources éditoriales originales sans mélanger les modules des livres."""
import importlib
import json
import re
import sys
import unicodedata
from dataclasses import asdict
from config import GRADE, ROOT, BOOK, LABEL

sys.path.insert(0,str(BOOK))
if GRADE.startswith('cm'):
    for p in sorted(BOOK.glob('contenu_*.py')): importlib.import_module(p.stem)
else:
    modules=['nombres','calcul']
    if GRADE=='ce2': modules+=['multiplication','problemes']
    modules+=['fractions','mesures']
    if GRADE=='ce2': modules+=['temps']
    modules+=['geometrie']
    for name in modules: importlib.import_module('contenu_'+name)
from modele import CHAPITRES

def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub('[^a-z0-9]+','-',s).strip('-')

out=[]
for c in CHAPITRES:
    d=asdict(c)
    if GRADE.startswith('ce'):
        d['slug']=slug(c.titre)
        d['objectifs']=[c.objectif]
        d['prerequis']=['Préparer le matériel indiqué et expliquer ses choix à voix haute.']
        d['reperes']=c.lecon
    out.append(d)
(ROOT/'sources').mkdir(parents=True,exist_ok=True)
(ROOT/'verifications').mkdir(exist_ok=True)
(ROOT/'sources/livre.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(LABEL+': '+str(len(out))+' chapitres exportés.')
print('\n'.join(str(c['numero'])+' '+c['slug'] for c in out))
