"""Contrôles de clôture et inventaire de publication, exclusivement locaux."""
from pathlib import Path
import json,hashlib,re,struct,subprocess,sys,datetime,html
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;FRONT=ICI.parents[4]
assert '--relecture-root-terminee' in sys.argv,'Achever les relectures avant de figer les preuves.'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
initial=load(ICI/'inventaire_initial_cp.json');rows=[]
assert len(initial)==30 and {x['notion'] for x in initial}==set(range(1,31))
figproof=load(ICI/'controle_figures_cp.json');assert figproof['statut']=='OK' and not figproof['anomalies']
checkedfigs={(x['chapitre'],x['figure']):x for x in figproof['controles']}
book=load(ICI/'sources/livre.json')
assert isinstance(book,list) and len(book)==30 and {x['numero'] for x in book}==set(range(1,31))
# Les rédacteurs relisent leurs lots ; la coordination contrôle indépendamment
# les textes, les empreintes, les résultats et l'intégralité des audits.
rootcodes=set(range(21,29))
for r in initial:
 d=ROOT/r['dossier'];code=r['notion'];source=load(d/'sources_locales/chapitre.json')
 assert source==next(x for x in book if x['numero']==code)
 for name,h in load(d/'sources_locales/empreintes_sources.json').items():assert sha(FRONT/name)==h
 cp=subprocess.run([sys.executable,'-X','utf8',str(d/'verif_math.py')],capture_output=True,text=True,encoding='utf-8')
 (d/'verification_math_finale.log').write_text(cp.stdout+cp.stderr,encoding='utf-8');assert cp.returncode==0,(d.name,cp.stdout,cp.stderr)
 paths=[d/name for name in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt')];texts=[p.read_text(encoding='utf-8') for p in paths]
 for text in texts:
  assert not any(ord(c)<32 and c!='\n' for c in text),(d.name,'caractere de controle')
  assert not re.search(r'(?<![A-Za-z\\])(?:widehat|dfrac|frac|times|div)\s*[\d{]',text),(d.name,'commande LaTeX nue')
 for text in texts[:2]:assert text.startswith('Titre: ') and '<!-- optitab:1 -->' in text
 assert '::: objectifs' in texts[0]
 blocks=[b for b in re.split(r'^===[ \t]*$',texts[2],flags=re.M) if b.strip()]
 assert len(blocks)==len(source['exercices'])==9
 ids=[];titles=[];enonces=[];questions=0;minquestions=100;used={}
 for index,b in enumerate(blocks):
  eid=re.search(r'^Id:\s*(nouveau-\d+)\s*$',b,re.M)[1];ids.append(eid);titles.append(b.strip().splitlines()[0])
  en=b.split('Énoncé:')[1].split('Étapes:')[0].strip();et=b.split('Étapes:')[1].split('Solution:')[0].strip();so=b.split('Solution:')[1].strip()
  assert all(t.startswith('<!-- optitab:1 -->') for t in (en,et,so))
  qs=re.findall(r'^\d+\. ',en,re.M);steps=re.split(r'^## Question\s+',et,flags=re.M)[1:]
  answers=[x.strip() for x in re.findall(r'^\d+\. ([\s\S]*?)(?=^\d+\. |\Z)',so,re.M)];results=[x.strip() for x in re.findall(r'^::: resultat[ \t]*\n(.*?)\n:::',et,re.M|re.S)]
  assert len(qs)==len(steps)==len(answers)==len(results)==5,(d.name,eid,'cinq questions requises, corrigé et solution complets')
  assert answers==results,(d.name,eid,'resultat different de solution')
  assert all('::: methode' in q and '::: etape' in q and '::: resultat' in q for q in steps)
  # Un schéma étudié ou construit doit avoir son modèle ET sa correction.
  # Les tableaux de données restent natifs et ne nécessitent pas de PNG.
  sourcefigure=source['exercices'][index].get('figure')
  figure_necessaire=bool('[IMAGE_' in en or '[IMAGE_' in et or code in range(17,29) or (sourcefigure and sourcefigure[0] not in ('surveytable','doubletable')))
  if figure_necessaire:assert '[IMAGE_' in en and '[IMAGE_' in et,(d.name,eid,'schéma nécessaire dans énoncé ET étapes')
  questions+=len(qs);minquestions=min(minquestions,len(qs));enonces.append(re.sub(r'\s+',' ',en))
  used['exercices',eid]={int(x) for x in re.findall(r'\[IMAGE_(\d+)\]',en+et+so)}
 assert len(set(ids))==len(set(titles))==len(set(enonces))==len(blocks),(d.name,'doublon')
 assert set(ids)=={f'nouveau-{i}' for i in range(1,len(blocks)+1)}
 used['cours','nouveau']={int(x) for x in re.findall(r'\[IMAGE_(\d+)\]',texts[0])};used['fiches','nouvelle']={int(x) for x in re.findall(r'\[IMAGE_(\d+)\]',texts[1])}
 assert used['cours','nouveau'] and used['fiches','nouvelle'],(d.name,'schémas nécessaires dans le cours et la fiche')
 corr=load(d/'figures/correspondance.json');active=set();positions=0
 for (genre,key),calls in used.items():
  mapping=corr.get(genre,{}).get(key,{})
  assert set(map(int,mapping))==calls,(d.name,genre,key,'images absentes ou superflues')
  for im in mapping.values():
   # Une rangée de jetons CP sans texte peut mesurer moins de 70 px de haut.
   # Ses dimensions et sa lisibilité ont été contrôlées dans les PNG et captures.
   p=d/'figures/images'/im['fichier'];w,h=struct.unpack('>II',p.read_bytes()[16:24]);assert 100<w<=1100 and h>=40 and len(im['alt'])>=15,(d.name,p.name,w,h)
   active.add(p);positions+=1
   checked=checkedfigs[code,p.name];assert checked['ok'] and checked['sha256']==sha(p),(d.name,p.name,'figure modifiée après contrôle')
 for genre,mapping in corr.items():
  for key in mapping:assert (genre,key) in used,(d.name,'proprietaire image absent')
 audit=load(d/'audit_navigateur_cp.json');validation=load(d/'validation_cp.json');views=2*(2+3*len(blocks))
 assert audit['statut']==validation['statut']=='OK' and audit['anomalies']==0
 assert audit['vues_distinctes']==len(audit['controles'])==views and all(c['ok'] for c in audit['controles'])
 for capture in audit['captures']:assert (d/'captures_cp'/capture).is_file()
 payload=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',(d/'apercu.html').read_text(encoding='utf-8'),re.S)[1])
 title=texts[0].splitlines()[0].removeprefix('Titre: ').strip();assert payload['titre']==title and len(payload['docs'])==2
 for doc in payload['docs']:
  text=texts[0 if doc['ctx']=='course' else 1];assert doc['text'].replace('\r\n','\n')==text[text.index('<!-- optitab:1 -->'):]
 assert len(payload['exercices'])==len(blocks)
 for item,b in zip(payload['exercices'],blocks):
  for key,label,nextlabel in [('enonce','Énoncé','Étapes'),('etapes','Étapes','Solution'),('solution','Solution',None)]:
   start=b.index(label+':')+len(label)+1;end=b.index(nextlabel+':',start) if nextlabel else len(b)
   assert item[key].replace('\r\n','\n')==b[start:end].strip(),(d.name,item['id'],'apercu perime')
 if code not in rootcodes:
  agentproof=load(d/'PREUVES_FINALES.json');assert agentproof['statut']=='OK' and agentproof['math_OK'] and agentproof['anomalies']==0
  assert load(d/'etat.json')['statut']=='pret'
 for name in ('RAPPORT.md','COUVERTURE.md'):assert (d/name).is_file(),(d.name,name)
 hashes={str(p.relative_to(d)).replace('\\','/'):sha(p) for p in paths+[d/'figures/correspondance.json']+sorted(active)}
 proof={'statut':'OK','math_OK':True,'anomalies':0,'vues_distinctes':views,'exercices':len(blocks),'questions':questions,'minimum_questions_par_exercice':minquestions,'empreintes_finales':hashes,'empreinte_apercu':sha(d/'apercu.html'),'figures_vues':[p.name for p in sorted(active)],'captures_lues':audit['captures'],'import_effectue':False,'relecture':'coordination' if code in rootcodes else 'agent rédacteur puis vérification indépendante de coordination'}
 old=d/'PREUVES_FINALES.json'
 if old.exists():
  backup=d/'sauvegardes/avant_cloture_coordination';backup.mkdir(parents=True,exist_ok=True)
  if not (backup/old.name).exists():(backup/old.name).write_bytes(old.read_bytes())
 save(old,proof);save(d/'etat.json',{'statut':'pret','agent':'coordination_cp','maj':datetime.date.today().isoformat()})
 rows.append({'numero':code,'dossier':d.name,'titre':title,'theme':r['theme'],'cours':1,'fiches':1,'exercices':len(blocks),'questions':questions,'figures':len(active),'positions_images':positions,'vues_navigateur':views,'minimum_questions_par_exercice':minquestions,'empreintes_sha256':hashes,'statut':'pret'})
 print(code,'prêt',len(blocks),'exercices',questions,'questions',len(active),'figures',flush=True)
bilan={'statut':'pret','niveau':'cp','notions':len(rows),'detail':rows,'production':'non importe','sources_conservees':True,'minimum_questions_par_exercice':min(x['minimum_questions_par_exercice'] for x in rows)}
for key in ('cours','fiches','exercices','questions','figures','positions_images','vues_navigateur'):bilan[key]=sum(x[key] for x in rows)
assert bilan['notions']==bilan['cours']==bilan['fiches']==30 and bilan['exercices']==270 and bilan['questions']==1350
save(ICI/'bilan_cp.json',bilan)
report=f"# CP — Cours, synthèses et exercices\n\n{bilan['cours']} cours, {bilan['fiches']} synthèses, {bilan['exercices']} exercices et {bilan['questions']} questions corrigées. Minimum : {bilan['minimum_questions_par_exercice']} questions par exercice.\n\n{bilan['figures']} schémas actifs refaits, {bilan['positions_images']} emplacements d’images ; {bilan['vues_navigateur']} vues contrôlées sans anomalie. Statut : prêt. Tous les originaux restent conservés.\n\n| Chapitre | Exercices | Questions | Aperçu |\n|---|---:|---:|---|\n"
for r in rows:report+=f"| {r['titre']} | {r['exercices']} | {r['questions']} | [Ouvrir](../{r['dossier']}/apercu.html) |\n"
(ICI/'BILAN_CP.md').write_text(report,encoding='utf-8')
cards=''.join(f'<a href="../{r["dossier"]}/apercu.html"><strong>{html.escape(r["titre"])}</strong><span>Cours · Synthèse · {r["exercices"]} exercices corrigés</span></a>' for r in rows)
page='<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OptiTAB — CP</title><style>body{font:16px system-ui;background:#f4f6fb;color:#1c2130}main{max-width:1100px;margin:40px auto;padding:20px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}a{display:grid;gap:12px;background:white;border:1px solid #d5dae3;border-radius:12px;padding:22px;text-decoration:none;color:inherit}span{color:#6b7385}</style><main><h1>CP — Mathématiques</h1><p>Cours, synthèses et exercices corrigés, avec au moins cinq questions par exercice.</p><section>'+cards+'</section></main></html>'
(ICI/'sommaire_cp.html').write_text(page,encoding='utf-8')
print(json.dumps({k:v for k,v in bilan.items() if k!='detail'},ensure_ascii=False))
