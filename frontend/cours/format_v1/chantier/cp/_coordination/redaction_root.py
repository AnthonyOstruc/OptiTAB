from commun_redaction import *
def C(prompt,method,expr,value,unit):
 lines=[];m=re.fullmatch(r'(\d+)([+-])(\d+)',expr)
 if m:
  a,op,b=m.groups();cur=int(a);b=int(b)
  for place in (10,1):
   part=(b//place%10)*place
   if part:
    nxt=cur+part if op=='+' else cur-part;lines.append(eq(f'{cur}{op}{part}',nxt));cur=nxt
  assert cur==value
 expression=expr.replace('*',chr(92)+'times ').replace('/',chr(92)+'div ')
 lines.append(eq(expression,value))
 return q(prompt,method,'\n\n'.join(dict.fromkeys(lines)),f'{value} {unit}.')
def E(title,intro,qs,images=None):
 for part in qs:
  calls=re.findall(r'\[IMAGE_\d+\]',part['resultat'])
  if calls:part['resultat']=re.sub(r'\[IMAGE_\d+\]','',part['resultat']).strip();part['etapes']+=calls
 return ex(title,intro,qs,figures=images or {})
def emit(code,items):
 def clean(s):return re.sub(r'(?<=\d)(?=[A-Za-zÀ-ÿ€])|(?<=[A-Za-zÀ-ÿ])(?=\d)',' ',s)
 for item in items:
  for key in ('titre','enonce'):item[key]=clean(item[key])
  for p in item['questions']:
   for key in ('question','methode','resultat'):p[key]=clean(p[key])
   p['etapes']=[clean(s) for s in p['etapes']]
 write(code,items);d=next(ROOT.glob(f'{code:02}_*'));source=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
 rows=['# Couverture des activités sources','','| Source | Activité du livre | Exercice final |','|---|---|---|']
 for i,s in enumerate(source['exercices'],1):rows.append(f"| {i} | {s['consigne'].replace('|','/')} | nouveau-{i} |")
 (d/'COUVERTURE.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
 (d/'RAPPORT.md').write_text('# '+source['titre']+'\n\nRédaction CP : neuf activités du livre reprises et développées en cinq questions liées chacune. Cours, synthèse et corrections au format OptiTAB v1. Sources conservées ; vérifications mathématiques et visuelles requises avant état prêt.\n',encoding='utf-8')
