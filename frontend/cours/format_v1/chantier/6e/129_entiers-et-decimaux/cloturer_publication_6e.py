"""Clôture documentaire après import et relecture HTTP réussis, sans écriture SQL."""
from pathlib import Path
import datetime,hashlib,json

ICI=Path(__file__).resolve().parent
def load(name):return json.loads((ICI/name).read_text(encoding='utf-8'))
def save(name,value):(ICI/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

bilan=load('bilan_6e.json');publication=load('publication_6e.json')
preuve=load('verification_publication_http_6e.json');images=load('images_publiees_6e.json')
activation=load('activation_cours_6e.json');visibilite=load('verification_visibilite_6e.json')
assert activation['statut']=='OK' and activation['cours_actifs']==activation['notions_actives']==26
assert visibilite['statut']=='OK' and visibilite['controles']==52
assert publication['statut'] in ('importe_et_relu','publie_et_verifie')
assert preuve['statut']=='OK' and preuve['api_ok']==156
assert len(preuve['api'])==156 and all(r['ok'] for r in preuve['api'])
assert preuve['images_ok']==len(images)==len(preuve['images'])
assert all(r['ok'] for r in preuve['images'])
assert len(publication['imports'])==bilan['notions']==26
assert (bilan['cours'],bilan['fiches'],bilan['exercices'])==(26,26,524)
assert publication['ecriture']
for row in bilan['detail']:
    dossier=ICI.parent/row['dossier']
    for name,expected in row['empreintes_sha256'].items():
        assert hashlib.sha256((dossier/name).read_bytes()).hexdigest()==expected,(row['notion'],name)
    assert json.loads((dossier/'etat.json').read_text(encoding='utf-8'))['statut']=='importe'
    record=next(r for r in publication['imports'] if r['notion']==row['notion'])
    assert Path(record['sauvegarde']).is_file()
    row.update(statut='publie_et_verifie',url_locale=f"http://localhost:3000/course-notion/{row['notion']}",url_live=f"https://www.optitab.net/course-notion/{row['notion']}")
now=datetime.datetime.now().isoformat(timespec='seconds')
publication.update(statut='publie_et_verifie',verification_http='verification_publication_http_6e.json',cloture=now)
bilan.update(statut='publie_et_verifie',production='publie et verifie',cloture=now,points_restants=[])
save('publication_6e.json',publication);save('bilan_6e.json',bilan)
rapport=ICI/'BILAN_6E.md'
text=rapport.read_text(encoding='utf-8').replace('État : pret.','État : publié et vérifié.').replace('| pret |','| publié et vérifié |')
note=f"\nPublication vérifiée le {now[:10]} : 156 réponses API conformes (local et serveur public), {len(images)} images téléchargées et identiques aux PNG validés. Les 26 sauvegardes avant import et tous les identifiants historiques sont conservés.\n\n[Ouvrir en local](http://localhost:3000/course-notion/129) · [Ouvrir le site](https://www.optitab.net/course-notion/129)\n"
if 'Publication vérifiée le ' not in text:text+=note
rapport.write_text(text,encoding='utf-8')
sommaire=ICI/'sommaire_6e.html'
page=sommaire.read_text(encoding='utf-8').replace('31 octobre 2026','1 novembre 2026').replace('État : pret.','État : publié et vérifié.')
sommaire.write_text(page,encoding='utf-8')
print(json.dumps({'statut':publication['statut'],'cours':26,'syntheses':26,'exercices':524,'api_conformes':156,'images_conformes':len(images),'sauvegardes':26},ensure_ascii=False))
