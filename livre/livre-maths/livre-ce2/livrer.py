"""Copie contrôlée du PDF relu vers le dossier de livraison."""
from pathlib import Path
import hashlib,json,shutil
import fitz

ROOT=Path(__file__).resolve().parent
pdf=ROOT/'build/optitab-ce2-complet.pdf'
qa=json.loads((ROOT/'build/qa/controles.json').read_text(encoding='utf8'))
review=json.loads((ROOT/'build/qa/relecture-visuelle.json').read_text(encoding='utf8'))
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert sha==qa['sha256']==review['sha256'], 'La relecture doit correspondre au PDF final.'
assert review['statut']=='prêt pour validation par l’utilisateur'
assert not any(qa[k] for k in ['chevauchements','texte_hors_page','figures_hors_cadre','pages_blanches'])
dest=ROOT.parent/'output/pdf/France/Mathématiques/OptiTAB - Mathématiques - CE2 - Manuel complet.pdf'
dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(pdf,dest)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
doc=fitz.open(dest);assert len(doc)==qa['pages']
report=ROOT.parent/'output/verification/verification-ce2.md';report.parent.mkdir(parents=True,exist_ok=True)
report.write_text(f'''# OptiTAB - Mathématiques CE2

Édition France 2026-2027, livrée le 23 octobre 2026.

- {qa['pages']} pages A4 ; 36 chapitres illustrés.
- 324 exercices avec leurs corrigés expliqués et leurs pistes d’aide.
- 5 bilans, soit 30 questions et leurs réponses.
- 360 problèmes oraux sur 36 semaines, avec réponses réservées à l’adulte.
- 6 pages de méthode et une page de graphique à construire.
- Matériel de numération, fractions, monnaie, horloges, géométrie et solides.
- {qa['liens']} liens et {qa['signets']} signets.

## Références et conception

Le programme du cycle 2 publié au BO du 31 octobre 2024, applicable
depuis septembre 2025, a été relu dans ses rubriques CE2. Le livret
d’accompagnement CE2 et les supports Repères CE2 2026 ont été consultés.
Les ressources sont citées à la fin du livre et dans `livre-ce2/modele.py`.

Le contenu est original et propre au CE2. Les volumes CP et CE1 ont servi
de continuité graphique. Le livre est indépendant, sans label ministériel.
Les exercices ne sont pas présentés comme des sujets officiels.

## Contrôles effectués

- {qa['calculs_declares']} calculs déclarés pour les exercices et bilans.
- {qa['egalites_verifiees']} égalités numériques détectées contrôlées avec des fractions exactes.
- Recalcul des 360 réponses de la banque orale.
- Recalcul des {qa['calculs_fluence']} réponses des quatre séries de fluence.
- Présence des 324 couples énoncé/corrigé et des 30 réponses de bilan.
- Liens internes valides et pagination stabilisée en deux passes.
- Aucun bloc de texte en chevauchement ou hors page.
- {qa['figures_uniques_controlees']} variantes de figures contrôlées dans leur cadre réel.
- {qa['controles_echelle']} contrôles de dimensions imprimées : rectangle, triangle, segments, repère et règles en fractions d’unité.
- Aucune page blanche accidentelle.
- Rendu intégral avec PyMuPDF ; relecture des planches et de pages sensibles en grand.
- Contrôle complémentaire de pages sensibles avec Poppler.

Les contrôles ne constituent pas une preuve formelle des activités
ouvertes ni de l’efficacité pédagogique. Le volume est livré pour
validation par l’utilisateur.

SHA-256 du PDF : `{sha}`

Sources modifiables : `livre-ce2/`.
Contrôles détaillés : `livre-ce2/build/qa/controles.json`.
Relecture : `livre-ce2/build/qa/relecture-visuelle.json`.
''',encoding='utf8')
print(json.dumps(dict(pdf=dest.as_posix(),pages=len(doc),octets=dest.stat().st_size,sha256=sha),ensure_ascii=False))
