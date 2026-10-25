"""Livrer uniquement le PDF dont les contrôles et la relecture concordent."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
import fitz

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / 'build'
QA = BUILD / 'qa'
SOURCE = BUILD / 'optitab-physique-chimie-5e-apercu.pdf'
DEST = ROOT.parent / 'output/pdf/France/Physique-chimie/OptiTAB - Physique-chimie - Cinquième (5e) - Aperçu (chapitres 1 et 2).pdf'


def main():
    controles = json.loads((QA / 'controles.json').read_text(encoding='utf8'))
    relecture = json.loads((QA / 'relecture-visuelle.json').read_text(encoding='utf8'))
    empreinte = sha256(SOURCE.read_bytes()).hexdigest()
    assert empreinte == controles['sha256'] == relecture['sha256'], 'PDF modifié depuis les contrôles ou la relecture'
    assert relecture['statut'] == 'prêt pour validation par l’utilisateur'
    assert not relecture['defauts_visuels_restants']
    for key in ['chevauchements', 'texte_hors_page', 'schemas_hors_cadre', 'pages_blanches']:
        assert not controles[key], f'Contrôle non résolu : {key}'
    with fitz.open(SOURCE) as doc:
        assert len(doc) == controles['pages'] == relecture['pages'] == 43
        for page in doc:
            used = {span['font'] for block in page.get_text('dict')['blocks']
                    if block['type'] == 0 for line in block['lines'] for span in line['spans']}
            for font in page.get_fonts():
                # ReportLab déclare aussi Helvetica sans l’utiliser. Vérifier
                # les polices qui apparaissent effectivement dans le texte.
                if font[0] and font[3].split('+')[-1] in used:
                    assert doc.extract_font(font[0])[3], f'Police non incorporée : {font[3]}'
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, DEST)
    assert sha256(DEST.read_bytes()).hexdigest() == empreinte

    receipt = ROOT.parent / 'output' / 'verification' / 'verification-physique-chimie-5e-apercu.md'
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(f'''# Aperçu physique-chimie 5e - vérification du 23 octobre 2026

Statut : prêt pour validation par l’utilisateur.

- 43 pages ; sommaire de 20 chapitres ; chapitres 1 et 2 rédigés.
- 30 exercices et 2 défis, tous accompagnés d’un corrigé expliqué.
- 25 insertions de schémas vectoriels ; 68 liens ; 7 signets.
- 18 calculs déclarés vérifiés et 4 contrôles de graduations.
- Aucun chevauchement, texte hors page, schéma hors cadre ou page blanche détecté.
- Rendu intégral des 43 pages par PyMuPDF et inspection des 6 planches.
- Inspection en grand format de 16 pages sensibles, rendues par Poppler.
- Polices utilisées incorporées et empreinte du fichier livré vérifiées.

SHA-256 : `{empreinte}`

Les contrôles automatisés sont complétés par la relecture des schémas,
des conditions expérimentales et des corrigés. Ils ne constituent pas une
validation institutionnelle. La validation de l’utilisateur reste attendue
avant la rédaction des chapitres suivants.

Programme : BO n° 31 du 30 juillet 2020, cycle 4, référence applicable
en 2026-2027 vérifiée sur Éduscol. Sources détaillées dans le PDF.

Traces : `livre-pc-cinquieme/build/qa/controles.json` et
`livre-pc-cinquieme/build/qa/relecture-visuelle.json`.
''', encoding='utf8')
    print(json.dumps({'pdf': str(DEST), 'pages': 43, 'octets': DEST.stat().st_size,
                      'sha256': empreinte, 'verification': str(receipt)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
