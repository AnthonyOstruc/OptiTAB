"""Audit mathématique exact de cette notion, sans réseau ni base."""
from pathlib import Path
import runpy

p=Path(__file__).resolve().parent
ns=runpy.run_path(str(p.parent/'261_operations-et-priorites/verif_numerique.py'))
ns['audit'](p)
scope=ns['audit'].__globals__
print(scope['checked'], 'contrôles exacts ;', len(scope['failures']), 'échec(s)')
for failure in scope['failures']: print('ERREUR', failure)
raise SystemExit(bool(scope['failures']))
