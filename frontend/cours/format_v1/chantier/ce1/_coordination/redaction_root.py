from commun_redaction import *
def calc(expr,value):return eq(expr.replace('*',chr(92)+'times ').replace('/',chr(92)+'div '),value)
def C(prompt,method,expr,value,unit):
 parts=re.fullmatch(r'(\d+)([+-])(\d+)',expr);lines=[]
 if parts:
  a,op,b=parts.groups();cur=int(a);b=int(b)
  for k in range(len(str(b))-1,-1,-1):
   part=b//10**k%10*10**k
   if part:
    nxt=cur+part if op=='+' else cur-part;lines.append(calc(f'{cur}{op}{part}',nxt));cur=nxt
  assert cur==value
 lines.append(calc(expr,value))
 return q(prompt,method,'\n\n'.join(dict.fromkeys(lines)),f'{value} {unit}.')
def E(title,intro,qs,figures=None):
 for part in qs:
  calls=re.findall(r'\[IMAGE_\d+\]',part['resultat'])
  if calls:
   part['resultat']=re.sub(r'\[IMAGE_\d+\]','',part['resultat']).strip();part['etapes']+=calls
 return ex(title,intro,qs,figures=figures)
def emit(code,items):
 write(code,items);d=next(ROOT.glob(f'{code:02}_*'));src=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
 lines=['# Couverture des sources','', 'Neuf activités sources développées en cinq questions liées, avec raisonnement et contrôle. Les originaux restent inchangés.','','| Source | Compétence initiale | Activité finale |','|---|---|---|']
 for i,(s,e) in enumerate(zip(src['exercices'],items),1):lines.append(f"| {i} | {s['consigne'].replace('|','/')} | nouveau-{i} — {e['titre']} |")
 (d/'COUVERTURE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 (d/'RAPPORT.md').write_text('# '+src['titre']+'\n\nCours et synthèse au format OptiTAB v1. Neuf exercices, 45 questions détaillées : méthode, raisonnement, résultat et solution concordante. Les données et activités du livre sont conservées ou rendues autonomes pour le site, sans renvoi à une annexe absente.\n\nLes figures TikZ utilisent la chaîne officielle. Les données restent en tableaux natifs. Les sources restent conservées. Vérifications mathématiques indépendantes et contrôles du rendu dans le navigateur avant publication par la coordination.\n',encoding='utf-8')
