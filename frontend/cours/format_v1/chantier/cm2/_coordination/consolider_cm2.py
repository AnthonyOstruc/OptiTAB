"""Bilan contrôlé des fichiers CM2, sans aucune écriture en base."""
from pathlib import Path
import json,re,hashlib,struct,html,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;FRONT=ICI.parents[4]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for initial in load(ICI/'inventaire_initial_cm2.json'):
 d=ROOT/initial['dossier'];state=load(d/'etat.json');assert state['statut']=='pret',d.name
 proof=load(d/'PREUVES_FINALES.json');audit=load(d/'audit_navigateur_cm2.json');validation=load(d/'validation_cm2.json')
 assert proof['statut']==audit['statut']==validation['statut']=='OK'
 assert proof['math_OK'] and proof['anomalies']==audit['anomalies']==0
 for name,h in load(d/'sources_locales/empreintes_sources.json').items():assert sha(FRONT/name)==h,(d.name,name,'original altere')
 for kind,original in [('cours',FRONT/f"cours/cours_optitab/cm2/cours_{initial['slug']}_cm2.txt"),('fiche',FRONT/f"cours/resume/cm2/resume_{initial['slug']}_cm2.txt"),('exercices',FRONT/f"exercices/cm2/exercice_{initial['slug']}_cm2.txt")]:assert (d/'sources_locales'/f'{kind}.txt').read_bytes()==original.read_bytes()
 for im in load(d/'sources_locales/inventaire_images.json'):assert sha(Path(im['chemin']))==im['sha256']
 paths=[d/'cours_nouveau.txt',d/'fiche_nouvelle.txt',d/'exercices.txt'];texts=[p.read_text(encoding='utf-8') for p in paths]
 assert all(t.startswith('Titre: ') and '<!-- optitab:1 -->' in t for t in texts[:2]);assert '::: objectifs' in texts[0]
 blocks=[b for b in re.split(r'^===[ \t]*$',texts[2],flags=re.M) if b.strip()];assert len(blocks)==21
 ids=[];titles=[];statements=[];questions=0;used={}
 for b in blocks:
  ident=re.search(r'^Id:\s*(\S+)',b,re.M)[1];assert re.fullmatch(r'nouveau-\d+',ident);ids.append(ident)
  titles.append(b.strip().splitlines()[0]);en=b.split('Énoncé:')[1].split('Étapes:')[0];et=b.split('Étapes:')[1].split('Solution:')[0];so=b.split('Solution:')[1]
  assert all(t.strip().startswith('<!-- optitab:1 -->') for t in (en,et,so))
  qs=re.findall(r'^\d+\. ',en,re.M);qs_steps=re.split(r'^## Question\s+',et,flags=re.M)[1:];answers=re.findall(r'^\d+\. (.+)',so,re.M);results=[v.strip() for v in re.findall(r'^::: resultat[ \t]*\n(.*?)\n:::',et,re.M|re.S)]
  assert len(qs)==len(qs_steps)==len(answers)==len(results)>=3,(d.name,ident,'questions incompletes')
  assert results==answers,(d.name,ident,'solution incoherente')
  assert all('::: methode' in q and '::: etape' in q and '::: resultat' in q for q in qs_steps)
  statements.append(re.sub(r'\s+',' ',en).strip());questions+=len(qs)
  used['exercices',ident]={int(n) for n in re.findall(r'\[IMAGE_(\d+)\]',en+et+so)}
 assert len(set(ids))==len(set(titles))==len(set(statements))==21,(d.name,'doublon')
 assert set(ids)=={f'nouveau-{i}' for i in range(1,22)}
 used['cours','nouveau']={int(n) for n in re.findall(r'\[IMAGE_(\d+)\]',texts[0])};used['fiches','nouvelle']={int(n) for n in re.findall(r'\[IMAGE_(\d+)\]',texts[1])}
 corr=load(d/'figures/correspondance.json');active=set();positions=0
 for (genre,key),calls in used.items():
  mapping=corr.get(genre,{}).get(key,{})
  assert set(map(int,mapping))==calls,(d.name,genre,key,'correspondance incomplete ou superflue')
  for im in mapping.values():
   p=d/'figures/images'/im['fichier'];assert p.is_file() and len(im['alt'])>=15
   w,h=struct.unpack('>II',p.read_bytes()[16:24]);assert 100<w<=1100 and h>=70,(d.name,p.name,w,h)
   active.add(p);positions+=1
 for genre,mapping in corr.items():
  for key in mapping:assert (genre,key) in used,(d.name,genre,key,'proprietaire absent')
 assert audit['vues_distinctes']==proof['vues_distinctes']==130 and len(audit['controles'])==130
 assert all(c['ok'] for c in audit['controles'])
 payload=load_payload=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',(d/'apercu.html').read_text(encoding='utf-8'),re.S)[1])
 titre=texts[0].splitlines()[0].removeprefix('Titre: ').strip();assert payload['titre']==titre
 for doc in payload['docs']:
  raw=texts[0 if doc['ctx']=='course' else 1];assert doc['text'].replace('\r\n','\n')==raw[raw.index('<!-- optitab:1 -->'):],(d.name,'document aperçu différent')
 assert len(payload['exercices'])==21
 for ex,b in zip(payload['exercices'],blocks):
  assert ex['id'] in ids
  for key,label,next_label in [('enonce','Énoncé','Étapes'),('etapes','Étapes','Solution'),('solution','Solution',None)]:
   start=b.index(label+':')+len(label)+1;end=b.index(next_label+':',start) if next_label else len(b)
   assert ex[key].replace('\r\n','\n')==b[start:end].strip(),(d.name,ex['id'],key,'apercu perime')
 assert (d/'RAPPORT.md').is_file() and (d/'COUVERTURE.md').is_file()
 hashes={str(p.relative_to(d)).replace('\\','/'):sha(p) for p in paths+[d/'figures/correspondance.json']+sorted(active)}
 for name,expected in proof['empreintes_finales'].items():assert sha(d/name)==expected,(d.name,name,'modifie apres preuve')
 row={'numero':initial['notion'],'dossier':d.name,'titre':titre,'theme':initial['theme'],'cours':1,'fiches':1,'exercices':21,'questions':questions,'figures':len(active),'positions_images':positions,'vues_navigateur':130,'statut':'pret','empreintes_sha256':hashes};rows.append(row)
 print(d.name,'pret',questions,'questions',len(active),'figures',flush=True)
report={'date':datetime.date.today().isoformat(),'niveau':'cm2','statut':'pret','notions':21,'detail':rows,'production':'non importe','sources_locales_conservees':True}
for key in ('cours','fiches','exercices','questions','figures','positions_images','vues_navigateur'):report[key]=sum(r[key] for r in rows)
(ICI/'bilan_cm2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text=f"# CM2 — cours, synthèses et exercices\n\n{report['cours']} cours, {report['fiches']} fiches, {report['exercices']} exercices et {report['questions']} questions corrigées.\n\n{report['figures']} PNG actifs, {report['positions_images']} emplacements d’images, {report['vues_navigateur']} vues contrôlées sans anomalie. Statut : prêt.\n\nTous les textes et illustrations d’origine sont conservés. Format optitab:1 identique à la 6e et la 5e. Nouveau contexte CM2 : aucun ancien identifiant en ligne à modifier.\n\n| Chapitre | Exercices | Questions | Aperçu |\n|---|---:|---:|---|\n"
for r in rows:text+=f"| {r['titre']} | 21 | {r['questions']} | [Ouvrir](../{r['dossier']}/apercu.html) |\n"
(ICI/'BILAN_CM2.md').write_text(text,encoding='utf-8')
cards=''.join(f'<a href="../{r["dossier"]}/apercu.html"><strong>{html.escape(r["titre"])}</strong><span>Cours · Fiche · 21 exercices</span></a>' for r in rows)
page='<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OptiTAB — Mathématiques CM2</title><style>body{font:16px system-ui;background:#f4f6fb;color:#1c2130}main{max-width:1100px;margin:40px auto;padding:20px}h1{color:#1b3c8e}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}a{display:grid;gap:12px;background:white;border:1px solid #d5dae3;border-radius:12px;padding:22px;text-decoration:none;color:inherit}span{color:#6b7385}</style><main><h1>CM2 — Mathématiques</h1><p>Choisis un chapitre pour ouvrir le cours, la synthèse et les exercices corrigés.</p><section>'+cards+'</section></main></html>'
(ICI/'sommaire_cm2.html').write_text(page,encoding='utf-8')
print(json.dumps({k:report[k] for k in ('statut','notions','cours','fiches','exercices','questions','figures','positions_images','vues_navigateur')}))
