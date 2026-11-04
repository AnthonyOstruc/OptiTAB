from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
for code in range(21,29):
 d=next(ROOT.glob(f'{code:02}_*'))
 print('\nCHAPITRE',code)
 data=json.loads((d/'donnees_exercices_root.json').read_text(encoding='utf-8'))
 for i,item in enumerate(data,1):
  print(i,item['titre'],item['enonce'])
  for j,q in enumerate(item['questions'],1):print(j,q['question'],'=>',q['resultat'])
