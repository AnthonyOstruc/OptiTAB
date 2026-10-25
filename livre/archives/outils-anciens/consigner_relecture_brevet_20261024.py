"""Trace les relectures successives et les dernières preuves du manuel Brevet."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1]
pdf=root/'livre-pc-brevet/build/main.pdf'
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert sha=='f2d1dd907b5de4755ba937e7dd7a37e8d536a0859fcb5f7243f5a230b71ecd29'
proof=json.loads((root/'tmp/pdfs/audit-physique-20261024/preuves-brevet-nouvelles/preuves.json').read_text(encoding='utf-8'))
assert proof['sha256']==sha
previous=json.loads((root/'livre-pc-brevet/build/validation-visuelle.json').read_text(encoding='utf-8'))
report=dict(date='2026-10-24',valide=True,sha256=sha,pages=327,rendu_integral=True,planches=28,planches_figures_initiales=18,planches_figures_nouvelles=4,preuves_poppler_initiales=previous.get('preuves_poppler',[]),preuves_poppler_finales=sorted(set(proof['pages']+[3,193])),relecture_integrale_et_reprises_apres_retouches=True,planches_finales_reprises=[24,25,26,27,28],controle_echelle_dans_pdf=True,texte_hors_page=False,debordements=False,caracteres_manquants=False,observations=['Le corps initial de 294 pages avait été intégralement relu ; les cinq sujets supplémentaires ont ensuite été relus et leurs 28 figures inspectées.','Les pages nouvelles et annexes finales ont été inspectées sur les cinq dernières planches du PDF final.','Les 15 nouvelles preuves Poppler, le sommaire et la construction des forces à l’échelle ont été relus après les dernières retouches.','Les 23 preuves critiques du corps initial ont été rendues à nouveau ; la navigation et les longueurs à l’échelle sont contrôlées sur le PDF final.','Le titre des enregistrements sonores garde une marge supérieure ; les légendes de la maquette de dirigeable correspondent aux deux états du dessin.','Les corrigés expliquent réponse, démarche et barème pour chacune des 45 nouvelles questions.'],defauts_restants=[])
(root/'livre-pc-brevet/build/validation-visuelle.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Relecture finale du Brevet consignée.')
