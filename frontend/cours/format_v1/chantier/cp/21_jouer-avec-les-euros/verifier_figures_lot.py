"""Audit strict des seules figures du lot nombres, sans compilation."""
from pathlib import Path
import sys, json, runpy, hashlib

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parents[1] / 'outils'))
import figures_livre as official

for code in map(int, sys.argv[1:]):
    assert code in [21, 22, 23, 24]
    d = next(ROOT.glob(f'{code:02}_*'))
    ns = runpy.run_path(str(d / 'figures/figures.py'))
    rows = []
    for name, source in ns['FIGURES'].items():
        png = d / 'figures/images' / f'{name}.png'
        build = d / 'figures/build'
        expected = official.PREAMBULE + ns.get('PREAMBULE_EXTRA', '') + '\n' + chr(92) + 'begin{document}\n' + official.graduations_x(source, name, ns.get('XLAB')) + '\n' + chr(92) + 'end{document}\n'
        actual = (build / f'{name}.tex').read_text(encoding='utf-8')
        assert actual == expected, (code, name, 'TikZ compilé périmé')
        assert (build / f'{name}__sans_texte.png').exists(), (code, name, 'contrôle sans texte absent')
        errors, warnings = official.chevauchements(png, build / f'{name}__sans_texte.png')
        width, height = official.taille_png(png)
        assert not errors and width <= official.LARGEUR_MAX_PX, (code, name, width, errors)
        rows.append({'figure': png.name, 'ok': True, 'largeur': width, 'hauteur': height, 'avertissements': warnings, 'sha256': hashlib.sha256(png.read_bytes()).hexdigest()})
    report = {'statut': 'OK', 'anomalies': 0, 'tex_identiques': True, 'figures': len(rows), 'controles': rows}
    (d / 'controle_figures_lot.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(code, 'OK', len(rows), 'figures', flush=True)
