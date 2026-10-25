"""Livre la refonte uniquement après contrôles et relecture de son empreinte."""
from pathlib import Path
import hashlib,json,shutil
import fitz

ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'template-terminale/build'
PDF=ROOT/'template-terminale/main.pdf'
QA=BUILD/'qa'
rapport=json.loads((QA/'controles.json').read_text(encoding='utf8'))
lecture=json.loads((QA/'relecture-visuelle.json').read_text(encoding='utf8'))
revision=json.loads((BUILD/'audit-revision.json').read_text(encoding='utf8'))
sha=hashlib.sha256(PDF.read_bytes()).hexdigest()
assert sha==rapport['sha256']==lecture['sha256'],'Le PDF contrôlé et le PDF relu doivent être identiques.'
assert revision['echecs']==0 and revision['sha256']==sha
assert lecture['statut']=='relecture terminée'
assert len(lecture['planches_inspectees'])==rapport['planches']
assert lecture['pages_poppler_inspectees']
for field in ('contenus_introuvables','texte_hors_page','pages_vides','pages_fragments_isoles','glyphes_defectueux','liens_casses','schemas_hors_cadre'):
    assert not rapport[field],field
assert (rapport['chapitres'],rapport['exercices'],rapport['defis'],rapport['lexique'])==(20,300,20,80)
with fitz.open(PDF) as doc:assert len(doc)==rapport['pages']
dest=ROOT.parent/'output/pdf/France/Physique-chimie/OptiTAB - Physique-chimie - Cinquième (5e) - Manuel complet.pdf'
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(PDF,dest)
desktop=Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')/dest.name
desktop.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PDF,desktop)
assert hashlib.sha256(desktop.read_bytes()).hexdigest()==sha
receipt=ROOT.parent/'output/verification/physique-chimie-5e-template-terminale.md'
receipt.parent.mkdir(parents=True,exist_ok=True)
receipt.write_text(f'''# Physique-chimie 5e : maquette de la collection Terminale

- PDF : {dest.name}
- Empreinte SHA-256 : `{sha}`
- {rapport['pages']} pages, 20 chapitres, 300 exercices, 20 défis.
- 4 bilans et 20 missions ; 80 entrées de lexique.
- {rapport['contenus_controles']} textes comparés aux sources : aucun manquant.
- {rapport['insertions_schemas']} insertions de schémas vectoriels.
- {rapport['liens']} liens et {rapport['signets']} signets ; destinations contrôlées.
- Aucune page vide, aucun texte hors page, aucun glyphe manquant, aucun débordement LaTeX.
- Toutes les pages rendues et toutes les planches inspectées ; épreuves Poppler revues.

Le modèle de Terminale a fourni les polices, les encadrés, les bandeaux,
les onglets et les styles d’exercices et de corrigés. Les adaptations à la
cinquième sont isolées dans le dossier du manuel de 5e.
''',encoding='utf8')
print(json.dumps(dict(pdf=str(dest),pages=rapport['pages'],sha256=sha),ensure_ascii=False))
