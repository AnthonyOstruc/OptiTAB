from pathlib import Path
import json,re,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent.parent
for n in (129,130,131,133,150,151):
 d=next(ROOT.glob(str(n)+'_*'));backup=d/'sauvegardes/avant_revision_20261030';backup.mkdir(parents=True,exist_ok=True)
 for p in list(d.glob('cours_*.txt'))+list(d.glob('fiche_*.txt'))+list(d.glob('exercices.txt')):
  if not (backup/p.name).exists():shutil.copy2(p,backup/p.name)
 (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'coordination-6e','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 if not (d/'exercices.txt').exists():continue
 blocks=re.split(r'^===[ \t]*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M)
 print('\nNOTION',n)
 for b in blocks:
  if not b.strip():continue
  pos={m[1]:m for m in re.finditer(r'^(Énoncé|Étapes|Solution):[ \t]*$',b,re.M)}
  en=b[pos['Énoncé'].end():pos['Étapes'].start()];et=b[pos['Étapes'].end():pos['Solution'].start()]
  qs=re.findall(r'^\d+\. (.+)',en,re.M)
  print(re.search(r'^Id: (.+)',b,re.M)[1],b.strip().splitlines()[0].replace('=== ',''),'|',en.strip().split('\n')[1:3], '|',qs[0] if qs else 'NONUM','| etapes',et.count('::: etape'))
