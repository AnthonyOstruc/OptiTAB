"""Livre le PDF uniquement après les contrôles et la revue visuelle consignés."""
from pathlib import Path
import json,hashlib,shutil
import fitz

ROOT=Path(__file__).resolve().parent
source=ROOT/'build/optitab-cp-complet.pdf'
qa=json.loads((ROOT/'build/qa/controles.json').read_text(encoding='utf8'))
review=json.loads((ROOT/'build/qa/relecture-visuelle.json').read_text(encoding='utf8'))
sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert sha==qa['sha256']==review['sha256']
assert review['statut']=='validé pour relecture par l’utilisateur'
assert not any(qa[k] for k in ['chevauchements','texte_hors_page','figures_hors_cadre','pages_blanches'])
dest=ROOT.parent/'output/pdf/France/Mathématiques/OptiTAB - Mathématiques - CP - Manuel complet.pdf';dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(source,dest)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
d=fitz.open(dest);assert len(d)==262
report=ROOT.parent/'output/verification/verification-cp.md';report.parent.mkdir(parents=True,exist_ok=True)
report.write_text(f'''# OptiTAB - Mathématiques CP

Édition France 2026-2027, livrée le 23 octobre 2026.

- 262 pages A4 ; 30 chapitres illustrés.
- 270 exercices numérotés et corrigés expliqués.
- 5 bilans : 30 questions avec corrigés.
- 360 problèmes oraux : 36 semaines de 10 problèmes, réponses pour l’adulte.
- 107 insertions de schémas vectoriels ; 91 variantes de dessin contrôlées dans leur cadre.
- Matériel à photocopier : dizaines, boîtes de dix, monnaie de jeu, horloges, formes, six faces de cube, quadrillage ; fiches de numération et calcul.
- Sommaire cliquable, liens entre exercices et corrigés, 71 signets.

## Recherche et périmètre

Les livres OptiTAB existants ont été examinés, notamment la structure, la
charte et le contenu du CM1. La présentation du CP reprend les couleurs et
logos de la collection, avec une composition adaptée aux jeunes lecteurs.

Le programme du cycle 2 publié au BO du 31 octobre 2024, le livret
d’accompagnement CP 2025, le cahier et le guide Repères CP 2026, ainsi que
les ressources Éduscol du point d’étape ont été consultés. Les références
cliquables figurent à la fin du livre et dans `livre-cp/modele.py`.

Les énoncés et les dessins sont originaux. Ce livre indépendant n’est pas
un recueil de sujets officiels et ne bénéficie d’aucun label du ministère.

Le parcours traite les nombres et calculs jusqu’à 100 ; les problèmes en
deux étapes, groupes égaux et partages restent jusqu’à 30. La monnaie est
en euros entiers et les heures sont entières. L’addition posée est située
en P4 ou P5. Une progression sur cinq périodes précise les reprises et
l’alternance des domaines.

## Vérifications

- {qa['calculs_declares']} vérifications explicites de calcul ; 508 égalités numériques détectées contrôlées.
- Les réponses des 360 problèmes oraux sont recalculées.
- Présence des 270 couples énoncé/corrigé et des 30 réponses de bilans.
- {qa['liens']} liens contrôlés ; sommaire stabilisé en deux passes.
- Aucun bloc de texte en chevauchement ou hors page, aucune figure hors de son cadre, aucune page blanche accidentelle.
- Rendu intégral des 262 pages avec PyMuPDF ; inspection de 22 planches au cours de la mise au point et de pages sensibles en grand.
- Contre-vérification visuelle avec Poppler, dont la dernière version des sauts de calcul et le grand graphique d’enquête.
- Inspection finale des pages modifiées après les corrections graphiques et éditoriales.

Les contrôles informatiques et la relecture ne constituent pas une preuve
formelle de toutes les phrases, de tous les tracés libres ou de l’efficacité
pédagogique. Le livre est livré pour validation par l’utilisateur avant le
passage au CE1.

SHA-256 du PDF livré : `{sha}`

Sources modifiables et scripts : `livre-cp/`. Rapport automatique :
`livre-cp/build/qa/controles.json`.
''',encoding='utf8')
print(json.dumps(dict(pdf=dest.as_posix(),pages=len(d),octets=dest.stat().st_size,sha256=sha),ensure_ascii=False))
