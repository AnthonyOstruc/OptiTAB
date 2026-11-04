"""Clôture documentaire après publication CM2 et vérification des deux accès."""
from pathlib import Path
import json,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bilan=load(ICI/'bilan_cm2.json');pub=load(ICI/'publication_cm2.json')
proof=load(ICI/'verification_publication_http_cm2.json');images=load(ICI/'images_publiees_cm2.json')
assert pub['statut'] in ('importe_et_relu','publie_et_verifie') and pub['ecriture']
assert proof['statut']=='OK' and proof['api_ok']==len(proof['api'])==126
assert proof['images_ok']==len(proof['images'])==len(images)==93
assert len(proof['navigation'])==2 and all(r['ok'] and r['notions_visibles']==21 for r in proof['navigation'])
assert all(r['ok'] for r in proof['api']+proof['images'])
assert len(pub['imports'])==bilan['notions']==21
assert (bilan['cours'],bilan['fiches'],bilan['exercices'],bilan['questions'])==(21,21,441,1365)
assert Path(pub['sauvegarde_hierarchie']).is_file()
for row in bilan['detail']:
 d=ROOT/row['dossier'];record=next(r for r in pub['imports'] if r['numero']==row['numero'])
 assert load(d/'etat.json')['statut']=='importe' and Path(record['sauvegarde']).is_file()
 for name,h in row['empreintes_sha256'].items():assert hashlib.sha256((d/name).read_bytes()).hexdigest()==h,(d.name,name)
 row.update(statut='publie_et_verifie',notion=record['notion'],url_locale=f"http://localhost:3000/course-notion/{record['notion']}",url_live=f"https://www.optitab.net/course-notion/{record['notion']}")
 p=load(d/'PREUVES_FINALES.json');p.update(import_effectue=True,verification_publication_http=True,notion_publiee=record['notion']);save(d/'PREUVES_FINALES.json',p)
 rapport=d/'RAPPORT.md';text=rapport.read_text(encoding='utf-8')
 if '## Publication CM2 vérifiée' not in text:
  text+='\n## Publication CM2 vérifiée\n\nCours, fiche, exercices et images importés et relus. Accès local et public contrôlés ; les sauvegardes des textes et illustrations d’origine sont conservées.\n'
  rapport.write_text(text,encoding='utf-8')
now=datetime.datetime.now().isoformat(timespec='seconds')
pub.update(statut='publie_et_verifie',cloture=now,verification_http='verification_publication_http_cm2.json')
bilan.update(statut='publie_et_verifie',production='publie et verifie',cloture=now,points_restants=[])
save(ICI/'publication_cm2.json',pub);save(ICI/'bilan_cm2.json',bilan)
rapport=ICI/'BILAN_CM2.md';text=rapport.read_text(encoding='utf-8').replace('Statut : prêt.','Statut : publié et vérifié.')
if 'Publication vérifiée le ' not in text:
 text+=f"\nPublication vérifiée le {now[:10]} : 126 réponses API conformes sur localhost et le serveur public, 93 images téléchargées et identiques aux PNG validés, 21 chapitres visibles sur les deux accès. 22 sauvegardes de création et tous les originaux locaux sont conservés.\n\n[Ouvrir en local]({bilan['detail'][0]['url_locale']}) · [Ouvrir le site]({bilan['detail'][0]['url_live']})\n"
rapport.write_text(text,encoding='utf-8')
sommaire=ICI/'sommaire_cm2.html';page=sommaire.read_text(encoding='utf-8')
for row in bilan['detail']:
 old=f'<a href="../{row["dossier"]}/apercu.html">'
 # Les aperçus autonomes restent accessibles ; lien direct vers la publication pour chaque chapitre.
 page=page.replace(old,f'<a href="{row["url_locale"]}">')
page=page.replace('Cours · Fiche · 21 exercices','Cours publié · Fiche · 21 exercices')
sommaire.write_text(page,encoding='utf-8')
print(json.dumps({'statut':pub['statut'],'cours':21,'syntheses':21,'exercices':441,'questions':1365,'images':93,'sauvegardes':22,'local':bilan['detail'][0]['url_locale'],'live':bilan['detail'][0]['url_live']},ensure_ascii=False))
