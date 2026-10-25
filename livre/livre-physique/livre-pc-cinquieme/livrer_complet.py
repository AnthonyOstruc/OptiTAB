"""Copie du PDF complet relu et création d’un relevé de livraison."""
from pathlib import Path
from hashlib import sha256
import json,shutil
import fitz

ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build-complet';QA=BUILD/'qa'
SOURCE=BUILD/'optitab-physique-chimie-5e-complet.pdf'
DEST=ROOT.parent/'output/pdf/France/Physique-chimie/OptiTAB - Physique-chimie - Cinquième (5e) - Manuel complet.pdf'

def main():
    controls=json.loads((QA/'controles.json').read_text(encoding='utf8'))
    review=json.loads((QA/'relecture-visuelle.json').read_text(encoding='utf8'))
    digest=sha256(SOURCE.read_bytes()).hexdigest()
    assert digest==controls['sha256']==review['sha256'],'Le PDF a changé depuis sa vérification'
    assert review['statut']=='relecture terminée'
    assert not review['defauts_visuels_restants']
    for key in ['chevauchements','texte_hors_page','schemas_hors_cadre','pages_blanches']:
        assert not controls[key],f'Contrôle non résolu : {key}'
    assert controls['chapitres']==20 and controls['exercices']==300 and controls['defis']==20
    with fitz.open(SOURCE) as doc:assert len(doc)==controls['pages']==review['pages']
    DEST.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SOURCE,DEST)
    assert sha256(DEST.read_bytes()).hexdigest()==digest
    receipt=ROOT.parent/'output'/'verification'/'verification-physique-chimie-5e-complet.md'
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(f'''# Physique-chimie 5e - manuel complet

Livraison du 23 octobre 2026.

- {controls['pages']} pages, 20 chapitres rédigés.
- 300 exercices et 20 défis ; tous les corrigés expliqués.
- 4 bilans de thème, soit 20 missions supplémentaires corrigées.
- 80 entrées de lexique et fiches méthode.
- {controls['insertions_schemas']} insertions de schémas vectoriels.
- {controls['controles_calculs']} vérifications de calculs déclarés.
- {controls['liens']} liens et {controls['signets']} signets.
- Polices utilisées incorporées.
- Aucun texte hors page, chevauchement, schéma hors cadre ou page blanche détecté.
- Toutes les pages rendues et toutes les planches inspectées.
- Schémas distincts relus en agrandissement ; seconde inspection avec Poppler.

SHA-256 : `{digest}`

Traces : `livre-pc-cinquieme/build-complet/qa/controles.json` et
`livre-pc-cinquieme/build-complet/qa/relecture-visuelle.json`.

Programme : cycle 4, BO n° 31 du 30 juillet 2020 ; référence applicable
en 2026-2027 vérifiée sur Éduscol. Répartition de 5e proposée par le manuel.
Le livre est indépendant ; aucune validation institutionnelle n’est revendiquée.
''',encoding='utf8')
    print(json.dumps({'pdf':str(DEST),'pages':controls['pages'],'octets':DEST.stat().st_size,'sha256':digest,'verification':str(receipt)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
