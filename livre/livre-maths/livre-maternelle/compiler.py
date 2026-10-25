"""Compile un cahier et contrôle le journal : python compiler.py ps|ms|gs"""
from pathlib import Path
import json, os, re, subprocess, sys

RACINE = Path(__file__).resolve().parent
MIKTEX = Path(os.environ['LOCALAPPDATA']) / 'Programs/MiKTeX/miktex/bin/x64'

def lualatex(dossier):
    r = subprocess.run([str(MIKTEX / 'lualatex.exe'), '-interaction=nonstopmode', '-halt-on-error', 'main.tex'],
                       cwd=dossier, capture_output=True, text=True, encoding='utf8', errors='replace')
    journal = (dossier / 'main.log').read_text(encoding='utf8', errors='replace')
    if r.returncode != 0:
        lignes = journal.splitlines()
        i = next((k for k, l in enumerate(lignes) if l.startswith('!')), max(0, len(lignes) - 40))
        sys.exit('\n'.join(lignes[i:i + 25]))
    return journal

def pages_labels(dossier):
    aux = (dossier / 'main.aux').read_text(encoding='utf8', errors='replace')
    return {m.group(1): int(m.group(2)) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}', aux)}

def compiler(cle):
    dossier = RACINE / cle
    precedent = None
    for passe in range(1, 5):
        journal = lualatex(dossier)
        labels = pages_labels(dossier)
        if passe >= 2 and labels == precedent and 'Rerun' not in journal:
            break
        precedent = labels
    problemes = []
    for motif in ['Overfull', 'Missing character', 'undefined', 'multiply defined', 'Entrée de guide trop haute']:
        for l in journal.splitlines():
            if motif in l and 'Underfull' not in l:
                problemes.append(l.strip())
    # Une activité = exactement une page.
    man = json.loads((dossier / 'manifeste.json').read_text(encoding='utf8'))
    liste = man['liste']
    for a, b in zip(liste, liste[1:]):
        ecart = labels[b['label']] - labels[a['label']]
        attendu = 2 if b['partie'] != a['partie'] else 1     # page d’ouverture de partie entre les deux
        if ecart != attendu:
            problemes.append(f'activité {a["num"]} : {ecart} page(s) au lieu de {attendu}')
    der = liste[-1]
    if labels['guide'] - labels[der['label']] != 1:
        problemes.append(f'dernière activité : {labels["guide"] - labels[der["label"]]} page(s)')
    guides = [int(float(m.group(2)[:-2])) for m in re.finditer(r'MATGUIDE\|([^|]+)\|([\d.]+pt)', journal)]
    nb_pages = int(re.search(r'Output written on main\.pdf \((\d+) pages', journal).group(1))
    print(json.dumps(dict(cahier=cle, pages=nb_pages, passes=passe, guide_max_pt=max(guides) if guides else 0,
                          problemes=len(problemes)), ensure_ascii=False))
    for p in problemes[:60]:
        print('  ', p)
    return not problemes

if __name__ == '__main__':
    sys.exit(0 if compiler(sys.argv[1]) else 1)
