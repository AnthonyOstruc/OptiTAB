"""Audits séquentiels du lot, au fur et à mesure des compilations achevées."""
from pathlib import Path
import json, os, subprocess, sys, time

ICI = Path(__file__).resolve().parent
ROOT = ICI.parent
env = dict(os.environ, PYTHONIOENCODING='utf-8')
for code in map(int, sys.argv[1:]):
    assert code in [1, 2, 3, 7, 8, 9, 10, 13]
    d = next(ROOT.glob(f'{code:02}_*'))
    while not (d / 'compilation_figures.json').exists():
        time.sleep(3)
    assert json.loads((d / 'compilation_figures.json').read_text(encoding='utf-8'))['retour'] == 0
    for args in [
        [str(ICI / 'verifier_figures_lot.py'), str(code)],
        [str(ICI / 'planches_lot.py'), str(code)],
        [str(ROOT / '_coordination/valider_cp.py'), str(code), '--navigateur'],
        [str(ROOT / '_coordination/planches_relecture_cp.py'), str(code)],
    ]:
        subprocess.run([sys.executable, *args], check=True, env=env)
    print(code, 'captures et figures prêtes à lire', flush=True)
