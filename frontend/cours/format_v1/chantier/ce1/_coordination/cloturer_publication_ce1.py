"""Clôture documentaire après publication et vérification HTTP ; aucune écriture SQL."""
from pathlib import Path
import json,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bilan=load(ICI/'bilan_ce1.json');pub=load(ICI/'publication_ce1.json');proof=load(ICI/'verification_publication_http_ce1.json');images=load(ICI/'images_publiees_ce1.json')
liaison=load(ICI/'liaison_identifiants_ce1.json');assert liaison['statut']=='OK' and len(liaison['detail'])==32
assert pub['statut'] in ('importe_et_relu','publie_et_verifie') and pub['ecriture']
assert len(pub['imports'])==bilan['notions']==32 and bilan['cours']==bilan['fiches']==32
assert bilan['exercices']>=288 and bilan['questions']>=5*bilan['exercices'] and bilan['minimum_questions_par_exercice']>=5
assert proof['statut']=='OK' and proof['api_ok']==len(proof['api'])==192
assert proof['images_ok']==len(proof['images'])==len(images)==bilan['positions_images']
assert len(proof['navigation'])==2 and all(r['ok'] and r['notions_visibles']==32 for r in proof['navigation'])
assert all(r['ok'] for r in proof['api']+proof['images']) and Path(pub['sauvegarde_hierarchie']).is_file()
for row in bilan['detail']:
 d=ROOT/row['dossier'];record=next(r for r in pub['imports'] if r['numero']==row['numero'])
 assert load(d/'etat.json')['statut']=='importe' and Path(record['sauvegarde']).is_file()
 linked=next(x for x in liaison['detail'] if x['numero']==row['numero'])
 assert linked['seuls_identifiants_modifies'] and linked['identifiants']==record['exercices']
 assert linked['empreintes_avant']==row.get('empreintes_validation',row['empreintes_sha256'])
 for name,h in linked['empreintes_apres'].items():assert hashlib.sha256((d/name).read_bytes()).hexdigest()==h,(d.name,name)
 row.update(empreintes_validation=linked['empreintes_avant'],empreintes_sha256=linked['empreintes_apres'],liaison_identifiants_verifiee=True)
 row.update(statut='publie_et_verifie',notion=record['notion'],url_locale=f"http://localhost:3000/course-notion/{record['notion']}",url_live=f"https://www.optitab.net/course-notion/{record['notion']}")
 p=load(d/'PREUVES_FINALES.json');p.update(import_effectue=True,verification_publication_http=True,notion_publiee=record['notion'],empreintes_validation=linked['empreintes_avant'],empreintes_finales=linked['empreintes_apres'],liaison_identifiants_verifiee=True);save(d/'PREUVES_FINALES.json',p)
 rapport=d/'RAPPORT.md';text=rapport.read_text(encoding='utf-8')
 if '## Publication CE1 vérifiée' not in text:rapport.write_text(text+'\n## Publication CE1 vérifiée\n\nCours, fiche, exercices et images importés et relus. Accès local et public contrôlés. Sauvegardes et sources d’origine conservées.\n',encoding='utf-8')
now=datetime.datetime.now().isoformat(timespec='seconds')
pub.update(statut='publie_et_verifie',cloture=now,verification_http='verification_publication_http_ce1.json');bilan.update(statut='publie_et_verifie',production='publie et verifie',cloture=now,points_restants=[])
save(ICI/'publication_ce1.json',pub);save(ICI/'bilan_ce1.json',bilan)
rapport=ICI/'BILAN_CE1.md';text=rapport.read_text(encoding='utf-8').replace('Statut : prêt.','Statut : publié et vérifié.')
if 'Publication vérifiée le ' not in text:text+=f"\nPublication vérifiée le {now[:10]} : 192 réponses API conformes sur les accès local et public, {len(images)} images téléchargées identiques aux PNG validés. 32 chapitres visibles sur les deux accès ; 33 sauvegardes de création conservées.\n\n[Ouvrir en local]({bilan['detail'][0]['url_locale']}) · [Ouvrir le site]({bilan['detail'][0]['url_live']})\n"
rapport.write_text(text,encoding='utf-8')
sommaire=ICI/'sommaire_ce1.html';page=sommaire.read_text(encoding='utf-8')
for row in bilan['detail']:page=page.replace(f'<a href="../{row["dossier"]}/apercu.html">',f'<a href="{row["url_locale"]}">')
sommaire.write_text(page,encoding='utf-8')
print(json.dumps({'statut':pub['statut'],'cours':32,'syntheses':32,'exercices':bilan['exercices'],'questions':bilan['questions'],'images':len(images),'minimum_questions':bilan['minimum_questions_par_exercice'],'local':bilan['detail'][0]['url_locale'],'live':bilan['detail'][0]['url_live']},ensure_ascii=False))
