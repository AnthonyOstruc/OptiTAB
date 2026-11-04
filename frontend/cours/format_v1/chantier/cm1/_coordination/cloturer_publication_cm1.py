"""Clôture documentaire après publication et vérification HTTP ; aucune écriture SQL."""
from pathlib import Path
import json,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bilan=load(ICI/'bilan_cm1.json');pub=load(ICI/'publication_cm1.json');proof=load(ICI/'verification_publication_http_cm1.json');images=load(ICI/'images_publiees_cm1.json')
assert pub['statut'] in ('importe_et_relu','publie_et_verifie') and pub['ecriture']
assert len(pub['imports'])==bilan['notions']==21 and bilan['cours']==bilan['fiches']==21
assert bilan['exercices']>=315 and bilan['questions']>=5*bilan['exercices'] and bilan['minimum_questions_par_exercice']>=5
assert proof['statut']=='OK' and proof['api_ok']==len(proof['api'])==126
assert proof['images_ok']==len(proof['images'])==len(images)==bilan['positions_images']
assert len(proof['navigation'])==2 and all(r['ok'] and r['notions_visibles']==21 for r in proof['navigation'])
assert all(r['ok'] for r in proof['api']+proof['images']) and Path(pub['sauvegarde_hierarchie']).is_file()
for row in bilan['detail']:
 d=ROOT/row['dossier'];record=next(r for r in pub['imports'] if r['numero']==row['numero'])
 assert load(d/'etat.json')['statut']=='importe' and Path(record['sauvegarde']).is_file()
 for name,h in row['empreintes_sha256'].items():assert hashlib.sha256((d/name).read_bytes()).hexdigest()==h,(d.name,name)
 row.update(statut='publie_et_verifie',notion=record['notion'],url_locale=f"http://localhost:3000/course-notion/{record['notion']}",url_live=f"https://www.optitab.net/course-notion/{record['notion']}")
 p=load(d/'PREUVES_FINALES.json');p.update(import_effectue=True,verification_publication_http=True,notion_publiee=record['notion']);save(d/'PREUVES_FINALES.json',p)
 rapport=d/'RAPPORT.md';text=rapport.read_text(encoding='utf-8')
 if '## Publication CM1 vérifiée' not in text:rapport.write_text(text+'\n## Publication CM1 vérifiée\n\nCours, fiche, exercices et images importés et relus. Accès local et public contrôlés. Sauvegardes et sources d’origine conservées.\n',encoding='utf-8')
now=datetime.datetime.now().isoformat(timespec='seconds')
pub.update(statut='publie_et_verifie',cloture=now,verification_http='verification_publication_http_cm1.json');bilan.update(statut='publie_et_verifie',production='publie et verifie',cloture=now,points_restants=[])
save(ICI/'publication_cm1.json',pub);save(ICI/'bilan_cm1.json',bilan)
rapport=ICI/'BILAN_CM1.md';text=rapport.read_text(encoding='utf-8').replace('Statut : prêt.','Statut : publié et vérifié.')
if 'Publication vérifiée le ' not in text:text+=f"\nPublication vérifiée le {now[:10]} : 126 réponses API conformes sur les accès local et public, {len(images)} images téléchargées identiques aux PNG validés. 21 chapitres visibles sur les deux accès ; 22 sauvegardes de création conservées.\n\n[Ouvrir en local]({bilan['detail'][0]['url_locale']}) · [Ouvrir le site]({bilan['detail'][0]['url_live']})\n"
rapport.write_text(text,encoding='utf-8')
sommaire=ICI/'sommaire_cm1.html';page=sommaire.read_text(encoding='utf-8')
for row in bilan['detail']:page=page.replace(f'<a href="../{row["dossier"]}/apercu.html">',f'<a href="{row["url_locale"]}">')
sommaire.write_text(page,encoding='utf-8')
print(json.dumps({'statut':pub['statut'],'cours':21,'syntheses':21,'exercices':bilan['exercices'],'questions':bilan['questions'],'images':len(images),'minimum_questions':bilan['minimum_questions_par_exercice'],'local':bilan['detail'][0]['url_locale'],'live':bilan['detail'][0]['url_live']},ensure_ascii=False))
