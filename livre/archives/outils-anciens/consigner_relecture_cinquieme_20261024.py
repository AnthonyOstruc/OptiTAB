"""Trace la relecture effectivement achevée de la version finale de 5e."""
from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parents[1]
pdf=root/'livre-pc-cinquieme/template-terminale/main.pdf'
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert sha=='b624f23847680c65e399528093c8c41cc400b5de13b510cd549727a7f481828a'
proof=json.loads((root/'tmp/pdfs/audit-physique-20261024/preuves-cinquieme-finales/preuves.json').read_text(encoding='utf-8'))
assert proof['sha256']==sha
report=dict(statut='relecture terminée',date='2026-10-24',sha256=sha,pages=346,planches_inspectees=list(range(1,30)),pages_poppler_inspectees=proof['pages'],planches_figures_revision_inspectees=list(range(1,7)),corrections_verifiees=['Figures propres aux données de chaque exercice dans les énoncés et corrigés concernés.','Rayons arrêtés par les écrans opaques ; deux essais distincts pour les deux positions de l’écran.','Ombres comparées à source et écran fixes, avec rayons limites.','Filtration puis évaporation du filtrat ; distinction du sable retenu.','Composition de l’air : modèle approché explicite et modèle à 100 points.','Quatre bilans complets ; dernière mission et méthode de reprise solidaires.','Circuits : branche ouverte, commande commune et jonctions lisibles.','Aucune réduction automatique des fiches ; toutes les pages tiennent naturellement.'],defauts_restants=[])
(root/'livre-pc-cinquieme/template-terminale/build/qa/relecture-visuelle.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Relecture finale de 5e consignée.')
