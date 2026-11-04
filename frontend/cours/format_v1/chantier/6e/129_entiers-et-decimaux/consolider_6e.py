"""Bilan du niveau à partir des fichiers et preuves réellement terminés."""
from pathlib import Path
import json,re,hashlib,struct,sys,html
sys.stdout.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[];errors=[];images_total=0;initial=load(ICI/'inventaire_initial_6e.json')
for item in initial:
 d=ROOT/item['dossier'];meta=load(d/'source_en_ligne/meta.json');state=load(d/'etat.json');problems=[]
 docs=list(d.glob('cours_*.txt'))+list(d.glob('fiche_*.txt'))
 assert len(list(d.glob('cours_*.txt')))==1 and len(list(d.glob('fiche_*.txt')))==1,(d.name,'documents incomplets')
 for p in docs:
  text=p.read_text(encoding='utf-8');assert text.startswith('Titre: ') and '<!-- optitab:1 -->' in text
  if p.name.startswith('cours_'):assert '::: objectifs' in text
 texts=docs+[d/'exercices.txt'];raw=(d/'exercices.txt').read_text(encoding='utf-8')
 blocks=[b for b in re.split(r'^===[ \t]*$',raw,flags=re.M) if b.strip()]
 seen=[];titles=[];statements=[];questions=0;used={}
 for b in blocks:
  eid=re.search(r'^Id:\s*(\S+)',b,re.M)[1];seen.append(eid);titles.append(b.strip().splitlines()[0])
  en=b.split('Énoncé:')[1].split('Étapes:')[0];et=b.split('Étapes:')[1].split('Solution:')[0];so=b.split('Solution:')[1]
  assert all(x.strip().startswith('<!-- optitab:1 -->') for x in (en,et,so)),(meta['notion'],eid,'marqueur')
  qs=re.findall(r'^\d+[.)]\s+',en,re.M);qet=re.split(r'^## Question\s+',et,flags=re.M)[1:]
  answers=re.findall(r'^\d+[.)]\s+',so,re.M)
  assert len(qs)==len(qet)==len(answers) and len(qs)>=2,(meta['notion'],eid,'questions/corriges',len(qs),len(qet),len(answers))
  assert all('::: methode' in q and '::: etape' in q and '::: resultat' in q for q in qet),(meta['notion'],eid,'correction incomplete')
  statements.append(re.sub(r'\s+',' ',en).strip());questions+=len(qs)
  used[('exercices',eid)]={int(x) for x in re.findall(r'\[IMAGE_(\d+)\]',en+et+so)}
 assert len(seen)==len(set(seen)) and len(titles)==len(set(titles)) and len(statements)==len(set(statements)),(meta['notion'],'doublon')
 assert {str(x['id']) for x in meta['exercices']}<={i for i in seen if i.isdigit()},(meta['notion'],'ID historique perdu')
 assert all(i.isdigit() or re.fullmatch(r'nouveau-\d+',i) for i in seen)
 for p in docs:
  genre='cours' if p.name.startswith('cours_') else 'fiches';key=p.stem.split('_',1)[1]
  used[(genre,key)]={int(x) for x in re.findall(r'\[IMAGE_(\d+)\]',p.read_text(encoding='utf-8'))}
 corr=load(d/'figures/correspondance.json');active=set();positions=0
 for (genre,key),positions_used in used.items():
  mappings=corr.get(genre,{}).get(key,{})
  assert set(map(int,mappings))==positions_used,(meta['notion'],genre,key,'mapping incomplet ou inutilise')
  for v in mappings.values():
   p=d/'figures/images'/v['fichier'];assert p.exists() and len(v['alt'])>=15
   with p.open('rb') as f:w,h=struct.unpack('>II',f.read(24)[16:24])
   assert 0<w<=1100 and h>0,(meta['notion'],p.name,w,h)
   active.add(p);positions+=1
 for genre,objs in corr.items():
  for key in objs:assert (genre,key) in used,(meta['notion'],genre,key,'proprietaire inconnu')
 assert (d/'RAPPORT.md').exists() and any(d.glob('COUVERTURE*.md')),(meta['notion'],'rapport ou couverture absent')
 proofpath=next((d/name for name in ('PREUVES_FINALES.json','preuves_finales_20261031.json','preuves_finales_6e.json','VALIDATION_FINALE.json') if (d/name).exists()),None)
 if state['statut']!='pret':problems.append('statut non pret')
 if not proofpath:problems.append('preuve finale absente');proof={}
 else:
  proof=load(proofpath)
  if proof.get('statut')!='OK':problems.append('preuve finale non OK')
  for key in ('anomalies','anomalies_navigateur','navigateur_anomalies','verifier_notion_problemes','anomalies_visuelles','erreurs_mathematiques'):
   if proof.get(key,0)!=0:problems.append('preuve en ecart : '+key)
  if proof.get('math_OK',True) is not True:problems.append('verification mathematique non OK')
 views=proof.get('vues_distinctes',proof.get('vues_distinctes_navigateur',0))
 assert not proof or views==2*(2+len(blocks)*3),(meta['notion'],'nombre de vues distinctes incorrect',views)
 hashes={p.name:sha(p) for p in texts}
 hashes['figures/correspondance.json']=sha(d/'figures/correspondance.json')
 hashes.update({str(p.relative_to(d)).replace('\\','/'):sha(p) for p in active})
 row={'notion':meta['notion'],'dossier':d.name,'titre':meta['titre'],'cours':1,'fiches':1,'exercices':len(blocks),'questions':questions,'identifiants_conserves':len(meta['exercices']),'exercices_ajoutes':sum(not i.isdigit() for i in seen),'figures_actives':len(active),'positions_images':positions,'vues_navigateur':views,'preuve_finale':proofpath.name if proofpath else None,'statut':'pret' if not problems else 'en_cours','empreintes_sha256':hashes,'points_restants':problems}
 rows.append(row);errors.extend({'notion':meta['notion'],'point':p} for p in problems)
 print(meta['notion'],row['statut'],len(blocks),'exercices',len(active),'figures',flush=True)
report={'date':'2026-11-01','niveau':'6e','statut':'pret' if not errors and len(rows)==26 else 'en_cours','notions':len(rows),'detail':rows,'points_restants':errors,'production':'non importe'}
for k in ('cours','fiches','exercices','questions','identifiants_conserves','exercices_ajoutes','figures_actives','positions_images','vues_navigateur'):report[k]=sum(r[k] for r in rows)
(ICI/'bilan_6e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['Mathématiques — 6e','',f"{report['cours']} cours, {report['fiches']} synthèses, {report['exercices']} exercices et {report['questions']} questions corrigées.",'',f"{report['identifiants_conserves']} identifiants historiques conservés, {report['exercices_ajoutes']} exercices ajoutés. {report['figures_actives']} figures actives pour {report['positions_images']} emplacements.",'',f"{report['vues_navigateur']} vues distinctes sur téléphone et ordinateur. État : {report['statut']}.",'','Même moteur optitab:1 et même présentation que la Terminale et la 5e. Les sources initiales et sauvegardes sont conservées.','', '[Ouvrir le sommaire](sommaire_6e.html)','','| Chapitre | Exercices | Questions | État |','|---|---:|---:|---|']
for r in rows:lines.append(f"| [{r['titre']}](../{r['dossier']}/apercu.html) | {r['exercices']} | {r['questions']} | {r['statut']} |")
(ICI/'BILAN_6E.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
cards=''.join(f'<a href="../{r["dossier"]}/apercu.html"><small>Chapitre {i:02}</small><strong>{html.escape(r["titre"])}</strong><span>Cours · Synthèse · {r["exercices"]} exercices</span></a>' for i,r in enumerate(rows,1))
page='''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OptiTAB — Mathématiques 6e</title><style>body{font:16px system-ui;background:#f4f6fb;color:#1c2130;margin:0}main{max-width:1080px;margin:auto;padding:40px 20px}h1{color:#1b3c8e}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin:28px 0}a{background:white;padding:22px;border:1px solid #d5dae3;border-radius:12px;text-decoration:none;color:inherit;display:grid;gap:10px}a:hover{border-color:#1b3c8e}small{color:#3b8544}span,footer{font-size:14px;color:#6b7385}</style><main><small>OPTITAB · MATHÉMATIQUES</small><h1>Sixième — Cours, synthèses et exercices</h1><p>Choisis un chapitre, puis ouvre le cours, la fiche ou les exercices. Chaque corrigé expose la méthode, les étapes et le résultat.</p><section>'''+cards+f'''</section><footer>Révision du 31 octobre 2026 · {report['cours']} cours · {report['fiches']} fiches · {report['exercices']} exercices. État : {report['statut']}.</footer></main></html>'''
(ICI/'sommaire_6e.html').write_text(page,encoding='utf-8')
print(json.dumps({k:report[k] for k in ('statut','notions','cours','fiches','exercices','questions','figures_actives','positions_images','vues_navigateur')},ensure_ascii=False))
