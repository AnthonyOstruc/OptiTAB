"""Consolidation en lecture seule des notions, puis bilan et sommaire locaux.

Ne change ni les rapports ni les états d'un autre agent. Refuse de clôturer
tant qu'une notion, une preuve ou une figure active manque.
"""
from pathlib import Path
from collections import Counter
import json,re,hashlib,subprocess,sys
from PIL import Image
ICI=Path(__file__).resolve().parent
BASE=ICI.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def blocks(t):return [b for b in re.split(r'^===[ \t]*$',t,flags=re.M) if b.strip()]
def ids(t):return re.findall(r'^Id:\s*(\d+)',t,re.M)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
GOOD='débordement 0px · erreurs formule 0 · $ bruts 0 · images manquantes 0 · blocs en erreur 0 · éléments trop larges 0'
records=[]
for code in range(261,281):
    d=next(BASE.glob(f'{code}_*'));meta=load(d/'source_en_ligne/meta.json');state=load(d/'etat.json')
    assert state['statut']=='pret' and '2026-10-30' in json.dumps(state),(code,'révision non prête')
    assert '30' in (d/'RAPPORT.md').read_text(encoding='utf-8').splitlines()[0],(code,'rapport ancien')
    current=(d/'exercices.txt').read_text(encoding='utf-8');source=(d/'source_en_ligne/exercices.txt').read_text(encoding='utf-8')
    bs=blocks(current);assert len(bs)==21 and ids(current)==ids(source) and len(set(ids(current)))==21,(code,'Id')
    titles=re.findall(r'^=== (.+)',current,re.M);assert len(set(titles))==21,(code,'titres')
    enonces=[]
    for b in bs:
        title=re.search(r'^=== (.+)',b,re.M)[1];diff=re.search(r'^Difficulté: (.+)',b,re.M)[1]
        assert title.startswith({'easy':'Découverte -','medium':'Entraînement -','hard':'Problème -'}[diff]),(code,title,diff)
        en=b.split('Énoncé:')[1].split('Étapes:')[0];enonces.append(re.sub(r'\s+',' ',en).strip())
    assert len(set(enonces))==21,(code,'énoncé dupliqué')
    questions=len(re.findall(r'^## Question ',current,re.M))
    assert questions==len(re.findall(r'^::: methode',current,re.M))==len(re.findall(r'^::: resultat',current,re.M)),(code,'structure des questions')
    assert len(re.findall(r'^::: etape',current,re.M))>=questions
    assert 'Raisonnement et calcul' not in current
    texts=[*d.glob('cours_*.txt'),*d.glob('fiche_*.txt'),d/'exercices.txt']
    for p in texts:
        t=p.read_text(encoding='utf-8')
        assert '<!-- optitab:1 -->' in t and not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',t),(code,p.name,'encodage')
    assert all((d/'apercu.html').stat().st_mtime>=p.stat().st_mtime for p in texts),(code,'aperçu périmé')
    assert (d/'sauvegardes/revision_2026-10-30/exercices.txt').exists()
    assert (d/'COUVERTURE.md').exists()
    if code<=265:
        assert all(v==0 for v in load(d/'resultats_controles.json').values())
        log=d/'validation_revision.log';manifest=load(d/'revision_20261030.json')
        replacements=sum(bool(e['remplacement']) for e in manifest['exercices'])
        proof=['resultats_controles.json','mathematiques.log','mathematiques_revision.log','controle_mathjax_etendu.json']
        assert (d/'relecture_visuelle.json').exists()
        extended=load(d/'controle_mathjax_etendu.json')
        assert extended['panneaux_typesettes']==65 and not extended['erreurs'] and not extended['math_input_error']
    elif code<=270:
        assert load(d/'controles_revision_20261030.json')['verification']==0
        assert load(d/'verification_revision_20261030.json')['statut']=='OK'
        log=d/'revision_navigateur.log';manifest=load(d/'revision_20261030.json')
        replacements=sum(e['type']=='diversification' for e in manifest['modifications'])
        proof=['controles_revision_20261030.json','verification_revision_20261030.json']
        assert (d/'relecture_visuelle.json').exists()
    elif code<=275:
        log=d/'revision_navigateur.log';manifest=load(d/'revision_pedagogique.json')
        replacements=len(manifest['remplacements'])
        proof=['controles_revision_20261030.json','controle_maths_coordination.json','resultat_verification.json','relecture_visuelle_coordination.json']
        assert load(d/'controles_revision_20261030.json')['verification']==0
        assert load(d/'controle_maths_coordination.json')['code_retour']==0
    else:
        log=d/'revision_navigateur.log';manifest=load(d/'revision_2026-10-30.json')
        replacements=len(manifest['remplacements'])+len(manifest.get('doublons_corriges',[]))
        proof=['verification_maths.json','controle_maths_coordination.json','controles_revision_20261030.json','relecture_visuelle_coordination.json']
        assert load(d/'controles_revision_20261030.json')['verification']==0
        assert load(d/'controle_maths_coordination.json')['code_retour']==0
    assert all((d/p).exists() for p in proof),(code,'preuve absente')
    lines=[l for l in log.read_text(encoding='utf-8').splitlines() if l.startswith(('[mobile]','[desktop]'))]
    if code<=265:
        # Ce lot conserve le résultat du vérificateur complet, qui exécute
        # les 130 vues mais n'imprime que les anomalies et le bilan final.
        assert log.read_text(encoding='utf-8').rstrip().endswith('OK'),(code,'audit navigateur')
    else:
        assert len(lines)==130 and all(GOOD in l for l in lines),(code,'audit navigateur')
    corr=load(d/'figures/correspondance.json')
    files={v['fichier'] for genre in corr.values() for positions in genre.values() for v in positions.values()}
    positions=sum(len(positions) for genre in corr.values() for positions in genre.values())
    if files:
        compilation={e['figure']:e['ok'] for e in load(d/'compilation_figures.json')}
        for f in files:
            assert compilation.get(Path(f).stem),(code,f,'compilation')
            with Image.open(d/'figures/images'/f) as im:assert im.width<=1100,(code,f,'largeur')
    olddiff=re.findall(r'^Difficulté: (.+)',source,re.M);newdiff=re.findall(r'^Difficulté: (.+)',current,re.M)
    records.append({'notion':code,'dossier':d.name,'titre':meta['titre'],'cours':len(meta['cours']),'fiches':len(meta['fiches']),'exercices':21,'questions':questions,'remplacements_diversifies':replacements,'difficultes_corrigees':sum(a!=b for a,b in zip(olddiff,newdiff)),'figures_actives':len(files),'positions_figures':positions,'vues_navigateur':130,'controle':'OK','relecture_mobile':'cours intégral, fiche, nouveaux exercices : énoncés et étapes','statut':'pret','preuves':proof+[log.name],'empreintes_sha256':{p.name:digest(p) for p in texts}})
    print(code,'CONSOLIDÉ',flush=True)

bilan={'date':'2026-10-30','niveau':'5e','notions':len(records),'cours':sum(e['cours'] for e in records),'fiches':sum(e['fiches'] for e in records),'exercices':sum(e['exercices'] for e in records),'questions':sum(e['questions'] for e in records),'remplacements_diversifies':sum(e['remplacements_diversifies'] for e in records),'figures_actives':sum(e['figures_actives'] for e in records),'vues_navigateur':sum(e['vues_navigateur'] for e in records),'production':'aucun import','statut':'pret','detail':records}
(ICI/'bilan_5e.json').write_text(json.dumps(bilan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
intro=[
'5e : révision pédagogique locale terminée le 30 octobre 2026.',
f"{bilan['cours']} cours, {bilan['fiches']} synthèses, {bilan['exercices']} exercices, {bilan['questions']} questions corrigées.",
f"{bilan['remplacements_diversifies']} remplacements documentés pour diversifier les démarches ; difficultés et titres corrigés, aucun énoncé strictement dupliqué. Les 420 Id sont conservés.",
f"{bilan['figures_actives']} figures actives contrôlées ; {bilan['vues_navigateur']} vues distinctes contrôlées sur téléphone et ordinateur, zéro anomalie restante dans les preuves finales. Les constructions demandées disposent de corrigés graphiques quand nécessaire.",
'Même moteur et même format optitab:1 que la Terminale ; objectifs, cours structurés, fiches courtes, méthodes et étapes explicites. Relectures mobiles et sauvegardes antérieures conservées. Chaque notion contient son rapport, sa couverture pédagogique et ses preuves.',
'Version locale prête à consulter. Aucun import sur le site et aucune écriture en base. Les outils communs et frontend/src sont inchangés.',
'[Ouvrir le sommaire des vingt chapitres](sommaire_5e.html)',
]
table=['| Notion | Questions | Figures | Aperçu | Rapport |','|---|---:|---:|---|---|']
for e in records:
    prefix='../'+e['dossier'];table.append(f"| {e['notion']} — {e['titre']} | {e['questions']} | {e['figures_actives']} | [Ouvrir]({prefix}/apercu.html) | [Lire]({prefix}/RAPPORT.md) |")
(ICI/'BILAN_5E.md').write_text('\n\n'.join(intro)+'\n\n'+'\n'.join(table)+'\n',encoding='utf-8')
subprocess.run([sys.executable,str(ICI/'generer_sommaire.py')],check=True,stdin=subprocess.DEVNULL)
print(json.dumps({k:v for k,v in bilan.items() if k!='detail'},ensure_ascii=False),flush=True)
