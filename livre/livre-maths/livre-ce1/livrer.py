"""Livraison du CE1 après contrôles automatiques et revue visuelle consignée."""
from pathlib import Path
import json,hashlib,shutil
import fitz
ROOT=Path(__file__).resolve().parent
pdf=ROOT/'build/optitab-ce1-complet.pdf'
qa=json.loads((ROOT/'build/qa/controles.json').read_text(encoding='utf8'))
review=json.loads((ROOT/'build/qa/relecture-visuelle.json').read_text(encoding='utf8'))
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert sha==qa['sha256']==review['sha256']
assert review['statut']=='prêt pour validation par l’utilisateur'
assert not any(qa[k] for k in ['chevauchements','texte_hors_page','figures_hors_cadre','pages_blanches'])
dest=ROOT.parent/'output/pdf/France/Mathématiques/OptiTAB - Mathématiques - CE1 - Manuel complet.pdf';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(pdf,dest)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
d=fitz.open(dest);assert len(d)==277
report=ROOT.parent/'output/verification/verification-ce1.md';report.parent.mkdir(parents=True,exist_ok=True)
report.write_text(f'''# OptiTAB - Mathématiques CE1

Édition France 2026-2027, livrée le 23 octobre 2026.

- 277 pages A4 ; 32 chapitres illustrés.
- 288 exercices et corrigés expliqués.
- 5 bilans : 30 questions avec corrigés.
- 360 problèmes oraux sur 36 semaines, avec réponses réservées à l’adulte.
- 101 insertions de schémas vectoriels ; 94 variantes de dessin contrôlées dans leur cadre.
- Annexes : numération, tables, doubles et moitiés, fractions, monnaie, horloges, quadrillage, papier pointé, faces de cube et de pyramide, observations de fluence.
- Sommaire cliquable, {qa['liens']} liens et {qa['signets']} signets.

## Recherche et progression

Le livre de CP et la charte OptiTAB ont servi de continuité graphique.
Le contenu est propre au CE1. Le programme du cycle 2 publié au BO du
31 octobre 2024, le livret d’accompagnement CE1 et les supports Repères
CE1 2026 ont été consultés. Les liens sont dans le livre et dans
`livre-ce1/modele.py`.

Les leçons, exercices et schémas sont originaux. Le livre est indépendant,
sans label ministériel ; il ne présente pas ses exercices comme des
sujets officiels.

Repères pris en compte : centaine dès P1, nombres jusqu’à 1 000 au plus
tard en P2, fractions unitaires dès P2, soustraction posée au plus tard
en P3, centimes au plus tard en P2 et prix à virgule dès P3. Les tables
se construisent et se reprennent sur toute l’année.

La soustraction utilise les échanges. Les fractions sont des fractions
d’un tout au plus égales à 1 ; les dénominateurs sont 2, 3, 4, 5, 6, 8 ou
10. Les opérations sur les fractions gardent le même dénominateur.
Les prix à virgule sont traités avec les euros et centimes ; les longueurs
restent en cm, m et km, les masses en g et kg. Les heures et durées
utilisent les heures entières, demi-heures et quarts d’heure.

## Contrôles effectués

- {qa['calculs_declares']} contrôles de calcul explicitement associés aux exercices et bilans.
- {qa['egalites_verifiees']} égalités numériques détectées contrôlées, avec fractions exactes lorsque nécessaire.
- Recalcul des 360 réponses de la banque orale.
- Présence des 288 couples énoncé/corrigé et des 30 réponses de bilan.
- Liens internes valides et pagination du sommaire stabilisée en deux passes.
- Aucun bloc de texte en chevauchement ou hors page, aucune figure hors de son cadre, aucune page blanche accidentelle.
- Rendu intégral avec PyMuPDF ; inspection de 24 planches et de pages sensibles en grand.
- Vérification avec Poppler des soustractions, fractions, horloges, constructions, graphique et matériel de pyramide.

Les contrôles ne constituent pas une preuve formelle de toutes les
phrases, des activités ouvertes ni de l’efficacité pédagogique. Le
livre est livré pour validation par l’utilisateur avant le CE2.

SHA-256 du PDF livré : `{sha}`

Sources modifiables : `livre-ce1/`.
Rapport automatique : `livre-ce1/build/qa/controles.json`.
''',encoding='utf8')
print(json.dumps(dict(pdf=dest.as_posix(),pages=len(d),octets=dest.stat().st_size,sha256=sha),ensure_ascii=False))
