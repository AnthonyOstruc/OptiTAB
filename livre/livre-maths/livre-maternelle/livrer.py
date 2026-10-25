"""Copie les trois cahiers vers output/pdf et le dossier du Bureau, puis archive les sources."""
from pathlib import Path
import hashlib, os, shutil, zipfile

RACINE = Path(__file__).resolve().parent
DEPOT = RACINE.parent
BUREAU = Path(os.environ['USERPROFILE']) / 'Desktop' / 'Livres OptiTAB - Lycée'
NOMS = {'ps': 'Petite Section', 'ms': 'Moyenne Section', 'gs': 'Grande Section'}

def livrer():
    (DEPOT / 'output' / 'pdf').mkdir(parents=True, exist_ok=True)
    (DEPOT / 'output' / 'sources').mkdir(parents=True, exist_ok=True)
    for cle, nom in NOMS.items():
        pdf = RACINE / cle / 'main.pdf'
        cible_pdf = DEPOT / 'output/pdf/France/Mathématiques' / f"OptiTAB - Mathématiques - {nom.replace(' Section', ' section')} ({cle.upper()}) - Cahier d’activités.pdf"
        cible_pdf.parent.mkdir(parents=True, exist_ok=True)
        for cible in [cible_pdf,
                      BUREAU / f'OptiTAB - Mathématiques - Maternelle {nom}.pdf']:
            shutil.copy2(pdf, cible)
        print(cle, hashlib.sha256(pdf.read_bytes()).hexdigest()[:12], pdf.stat().st_size // 1024, 'Ko')
    archive = DEPOT / 'output' / 'sources' / 'optitab-maternelle-sources.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(RACINE.rglob('*')):
            rel = p.relative_to(RACINE)
            if p.is_dir() or rel.parts[0] in ('build', '__pycache__', 'ps', 'ms', 'gs'):
                continue
            z.write(p, Path('livre-maternelle') / rel)
    print('sources :', archive.name, archive.stat().st_size // 1024, 'Ko')

if __name__ == '__main__':
    livrer()
