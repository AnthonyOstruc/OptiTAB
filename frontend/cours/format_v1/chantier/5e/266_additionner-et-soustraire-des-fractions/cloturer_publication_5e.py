"""Consigner les preuves finales, sans ecriture en base."""
from pathlib import Path
import json,hashlib
ICI=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=load(ICI/'verification_publication_http.json')
assert checks['statut']=='OK' and checks['api_ok']==120 and checks['images_ok']==268
pub=load(ICI/'publication_5e.json');bilan=load(ICI/'bilan_5e.json')
assert len(pub['sauvegardes'])==20
for r in bilan['detail']:
    d=ICI.parent/r['dossier'];state=load(d/'etat.json')
    assert state['statut']=='importe' and Path(state['sauvegarde']).is_file()
    for name,expected in r['empreintes_sha256'].items():assert hashlib.sha256((d/name).read_bytes()).hexdigest()==expected
    r.update(statut='importe',sauvegarde=state['sauvegarde'],publication_verifiee=True)
pub.update(statut='publie_et_verifie',images_verifiees=268,lectures_api_verifiees=120,preuve_http='verification_publication_http.json')
pub.pop('images_a_verifier_http',None)
bilan.update(statut='importe',production='publie et verifie sur localhost:3000 et sur le site public',publication='publication_5e.json',preuve_http='verification_publication_http.json',images_publiees_verifiees=268)
save(ICI/'publication_5e.json',pub);save(ICI/'bilan_5e.json',bilan)
p=ICI/'BILAN_5E.md';t=p.read_text(encoding='utf-8')
t=t.replace('Version locale prête à consulter. Aucun import sur le site et aucune écriture en base. Les outils communs et frontend/src sont inchangés.',
    'Publication du 30 octobre 2026 terminée et vérifiée : 20 cours, 20 synthèses et 420 exercices en base, 120 lectures API réussies sur localhost et le serveur public, 268 emplacements d’images téléchargés et comparés aux PNG validés. Les 20 sauvegardes avant import sont conservées. Même moteur optitab:1 que la Terminale. Les outils communs et frontend/src sont inchangés.\n\n[Consulter sur localhost](http://localhost:3000/course-notion/263) · [Consulter sur le site](https://www.optitab.net/course-notion/263) · [Preuves de publication](verification_publication_http.json)')
p.write_text(t,encoding='utf-8')
p=ICI/'sommaire_5e.html';t=p.read_text(encoding='utf-8')
t=t.replace('Version préparée sur cet ordinateur, en attente d’import sur le site.',
    'Publié et vérifié : 120 lectures API et 268 images conformes. <a href="http://localhost:3000/course-notion/263">Ouvrir localhost</a> · <a href="https://www.optitab.net/course-notion/263">Ouvrir le site</a>.')
p.write_text(t,encoding='utf-8')
print('Publication 5e terminee : 20 sauvegardes, 120 lectures API, 268 images conformes. Aucun contenu valide modifie.')
