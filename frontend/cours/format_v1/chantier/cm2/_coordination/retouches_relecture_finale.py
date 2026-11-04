from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
d=ROOT/'18_durees'
changes={'1 min 50 s.':'1 h 50 min.','2 min .':'2 h 00 min.','2 min 50 s.':'2 h 50 min.'}
data=json.loads((d/'donnees_exercices_root.json').read_text(encoding='utf-8'))
text=(d/'exercices.txt').read_text(encoding='utf-8')
for spec in data:
 if spec['parametres']['famille']=='decimal':
  old=spec['enonce'];new=old
  for a,b in changes.items():new=new.replace(a,b)
  assert old!=new
  assert old in text
  text=text.replace(old,new);spec['enonce']=new
(d/'donnees_exercices_root.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(d/'exercices.txt').write_text(text,encoding='utf-8')
for d in ROOT.glob('[0-9]*_*'):
 for name in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt'):
  for n,line in enumerate((d/name).read_text(encoding='utf-8').splitlines(),1):
   if re.search(r'\b(?:a|de|et|à|sur|avec|en)\d',line):print(d.name,name,n,line)
