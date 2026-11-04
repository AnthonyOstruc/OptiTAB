"""Import éditorial de scénarios partagés ; copie locale, sans dépendance à l'exécution."""
import ast
from pathlib import Path

base=Path(__file__).resolve().parents[2]
targets=[('nombres.py',['operations','divisibilite','fractions','additions_fractions']),
    ('algebre.py',['proportionnalite']),('donnees.py',['probabilites','programmation']),('variantes.py',['de'])]
out=['"""Scénarios communs au collège, adaptés au périmètre de Sixième."""',
    'from fractions import Fraction as F','from modele_6e import ex,q,n,m','']
for name,names in targets:
    raw=(base/'5e/sources'/name).read_text(encoding='utf-8')
    for node in ast.parse(raw).body:
        if isinstance(node,ast.FunctionDef) and node.name in names:
            out.append(ast.get_source_segment(raw,node).replace('En 5e','En 6e'))
(base/'6e/sources/scenarios_communs.py').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
print('8 scénarios partagés copiés dans les sources locales de 6e.')
