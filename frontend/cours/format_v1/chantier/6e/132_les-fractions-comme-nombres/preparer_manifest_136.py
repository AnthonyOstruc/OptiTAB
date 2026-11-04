"""Métadonnées d’aperçu des ajouts 136 ; export historique inchangé."""
from pathlib import Path
import json
d=next(Path(__file__).resolve().parent.parent.glob('136_*'))
m=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
m['fiches']=[dict(id='nouvelle',titre='Périmètres',images=[])]
m['exercices']=[dict(id=x['id'],titre=x['titre'],images=[]) for x in json.loads((d/'revision_20261030.json').read_text(encoding='utf-8'))]
(d/'meta_apercu.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
