"""Contrôle exact supplémentaire des égalités réellement affichées en géométrie."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
helper=ROOT/'01_grands-nombres/verif_math.py'
namespace={'__file__':str(helper),'__name__':'arithmetique_cm2'}
exec(compile(helper.read_text(encoding='utf-8').split('\nmanifest=')[0],str(helper),'exec'),namespace)
for code in range(13,18):
 d=next(ROOT.glob(f'{code:02}_*'));count=0
 for p in [d/'cours_nouveau.txt',d/'fiche_nouvelle.txt']:count+=namespace['literal_checks'](p.read_text(encoding='utf-8'),p.name)
 for b in re.split(r'^===[ \t]*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M):
  if not b.strip():continue
  eid=re.search(r'^Id: (.+)',b,re.M)[1]
  body=b.split('Étapes:')[1];body=re.sub(r'^## Question.*$','',body,flags=re.M)
  count+=namespace['literal_checks'](body,eid)
 report={'statut':'OK','egalites_et_comparaisons_exactes':count,'fichiers_finaux_lus':True}
 (d/'verification_arithmetique_supplementaire.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,count,'égalités ou comparaisons exactes')
