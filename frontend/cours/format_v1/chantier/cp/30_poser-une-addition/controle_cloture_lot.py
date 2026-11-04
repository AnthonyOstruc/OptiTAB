"""Contrôle final limité aux neuf notions de calcul attribuées."""
from pathlib import Path
import base64, datetime, difflib, hashlib, json, re, runpy, sys

ROOT=Path(__file__).resolve().parent.parent
OUTILS=ROOT.parents[1]/'outils'
sys.path.insert(0,str(OUTILS))
import figures_livre as official
CODES=(4,5,6,11,12,14,15,16,30)
FILES=('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/figures.py','figures/correspondance.json')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for code in CODES:
 d=next(ROOT.glob(f'{code:02}_*'))
 ns=runpy.run_path(str(d/'figures/figures.py'))
 figures=[]
 for name,body in ns['FIGURES'].items():
  image=d/'figures/images'/f'{name}.png';build=d/'figures/build'
  expected=official.PREAMBULE+ns.get('PREAMBULE_EXTRA','')+'\n'+chr(92)+'begin{document}\n'+official.graduations_x(body,name,ns.get('XLAB'))+'\n'+chr(92)+'end{document}\n'
  actual=(build/f'{name}.tex').read_text(encoding='utf-8')
  assert [x for x in actual.splitlines() if x.strip()]==[x for x in expected.splitlines() if x.strip()],(code,name,'PNG périmé')
  w,h=official.taille_png(image)
  errors,warnings=official.chevauchements(image,build/f'{name}__sans_texte.png')
  assert w<=official.LARGEUR_MAX_PX and not errors,(code,name,w,errors)
  figures.append({'fichier':image.name,'sha256':sha(image),'largeur':w,'hauteur':h,'avertissements':warnings})
 runpy.run_path(str(d/'verif_math.py'))['verify']()
 proof=d/'PREUVES_FINALES.json'
 fingerprints={name:sha(d/name) for name in FILES}
 old=json.loads(proof.read_text(encoding='utf-8')) if proof.exists() else None
 if old:
  assert old['empreintes_finales']==fingerprints,(code,'preuves périmées')
 audit=json.loads((d/'audit_navigateur_cp.json').read_text(encoding='utf-8'))
 assert audit['statut']=='OK' and audit['anomalies']==0
 # Comparer les octets embarqués : une réécriture idempotente peut changer la date.
 preview=(d/'apercu.html').read_text(encoding='utf-8')
 payload=json.loads(re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>',preview,re.S)[1])
 for item,name in zip(payload['docs'],FILES[:2]):
  text=(d/name).read_text(encoding='utf-8');text=text[text.index('<!-- optitab:1 -->'):]
  if item['text'].replace('\r\n','\n')!=text:
   print(''.join(difflib.unified_diff(item['text'].splitlines(True),text.splitlines(True))),flush=True)
   raise AssertionError((code,name,'aperçu périmé'))
 blocks=[b.strip() for b in re.split(r'^===[ \t]*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M) if b.strip()]
 assert len(blocks)==len(payload['exercices'])==9
 for block,item in zip(blocks,payload['exercices']):
  assert item['id']==re.search(r'^Id:\s*(\S+)',block,re.M)[1]
  assert item['titre']==block.splitlines()[0]
  for key,start,end in [('enonce','Énoncé','Étapes'),('etapes','Étapes','Solution'),('solution','Solution',None)]:
   value=block.split(start+':',1)[1]
   if end:value=value.split(end+':',1)[0]
   assert item[key].replace('\r\n','\n')==value.strip(),(code,item['id'],key,'aperçu périmé')
 mapping=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
 for genre,items in [('cours',payload['docs'][:1]),('fiches',payload['docs'][1:]),('exercices',payload['exercices'])]:
  for item in items:
   ident=item.get('id', 'nouveau' if genre=='cours' else 'nouvelle')
   for pos,info in mapping[genre].get(ident,{}).items():
    embedded=item['images'][pos]
    assert base64.b64decode(embedded['src'].split(',',1)[1])==(d/'figures/images'/info['fichier']).read_bytes()
    assert embedded['alt']==info['alt']
 report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK','notion':code,'empreintes_finales':fingerprints,'preuves_anterieures_conformes':bool(old),'audit_navigateur_reutilisable':True,'comparaison_apercu':'textes, correspondances et octets PNG identiques au contenu audité ; fins de ligne normalisées','figures':figures}
 (d/'controle_cloture.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'clôture technique OK',len(figures),'figures',flush=True)
