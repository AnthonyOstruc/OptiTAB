"""Vérification exacte des exercices diversifiés de cette notion."""
from pathlib import Path
import runpy
p=Path(__file__).resolve().parent
ns=runpy.run_path(str(p.parent/'261_operations-et-priorites/verif_revision_20261030.py'))
ns['audit'](p)
scope=ns['audit'].__globals__
print(scope['count'],'contrôles de révision ;',len(scope['failures']),'échec(s)')
for failure in scope['failures']: print('ERREUR',failure)
raise SystemExit(bool(scope['failures']))
