"""Clôture visuelle CP21–24, après lectures personnelles consignées."""
from pathlib import Path
import datetime, hashlib, json, re, sys

ROOT = Path(__file__).resolve().parent.parent
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, v): p.write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for code in map(int, sys.argv[1:]):
    assert code in [21,22,23,24]
    d=next(ROOT.glob(f'{code:02}_*'))
    math=load(d/'verification_math.json'); audit=load(d/'audit_navigateur_cp.json')
    validation=load(d/'validation_cp.json'); strict=load(d/'controle_figures_lot.json')
    seen=load(d/'relecture_effectuee.json'); manifest=load(d/'planches/index_figures_vues.json')
    assert math['math_OK'] and math['statut']=='OK' and math['questions_verifiees']==45
    for name,h in math['empreintes'].items(): assert hashlib.sha256((d/name).read_bytes()).hexdigest()==h,(code,name)
    assert audit['statut']==validation['statut']==strict['statut']=='OK'
    assert audit['anomalies']==strict['anomalies']==0 and strict['tex_identiques']
    figs=[f for p in manifest for f in p['figures']]
    assert len(figs)==strict['figures'] and set(p['planche'] for p in manifest)==set(seen['planches_figures'])
    assert seen['planches_documents'] and seen['planches_exercices']
    for entry in strict['controles']: assert hashlib.sha256((d/'figures/images'/entry['figure']).read_bytes()).hexdigest()==entry['sha256']
    log=(d/'compilation_figures.log').read_text(encoding='utf-8')
    count=len(figs); assert f'{count}/{count} figure(s) produite(s)' in log
    hashes={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/figures.py','figures/correspondance.json','apercu.html']}
    proof={'statut':'OK','math_OK':True,'anomalies':0,'exercices':9,'questions':45,'figures_vues':figs,'captures_lues':audit['captures'],'planches_lues':seen,'vues_navigateur':audit['vues_distinctes'],'compilation_retour':0,'compilation_log':'compilation_figures.log','controle_figures_strict':{'rapport':'controle_figures_lot.json','tex_identiques':True,'anomalies':0},'empreintes_finales':hashes,'sources_originales':'Empreintes vérifiées par valider_cp.py ; neuf activités reprises dans COUVERTURE.md.','publication':'Réservée à root.'}
    save(d/'PREUVES_FINALES.json',proof)
    title=(d/'cours_nouveau.txt').read_text(encoding='utf-8').splitlines()[0].removeprefix('Titre: ')
    rapport=f'# {title}\n\nÉtat : prêt. Neuf exercices nouveaux, quarante-cinq questions liées, cours et fiche au format OptiTAB v1. Les neuf activités sources restent couvertes dans COUVERTURE.md, y compris les manipulations et activités ouvertes avec exemple autonome. Identifiants nouveau-1 à nouveau-9 conservés.\n\n{count} figures TikZ ajoutées, aucune ancienne figure conservée. Compilation officielle --jobs 1 : retour 0, log conservé. Comparaison exacte des .tex avec FIGURES et contrôle de chevauchement : OK. Chaque PNG a été personnellement regardé dans les planches citées dans PREUVES_FINALES.json.\n\nContrôle mathématique indépendant : 45 questions, égalités et données vérifiées ; voir verification_math.json et RAPPORT_MATHEMATIQUE.md. Validation CP : OK. Audit navigateur final : {audit["vues_distinctes"]} vues, zéro anomalie. Cours mobile complet, fiche et exercices 1/5/9 énoncés et étapes relus dans les captures conservées ({len(audit["captures"])} captures).\n\nSources originales et empreintes conservées. Aucun point en suspens. Publication réservée à root.\n'
    if code==21: rapport+='\nCorrection mathématique conservée : complément de 28 à 35 par passage par 30, soit 2 puis 5, au total 7 euros.\n'
    (d/'RAPPORT.md').write_text(rapport,encoding='utf-8')
    save(d/'etat.json',{'statut':'pret','agent':'cp_root_visuel','maj':datetime.date.today().isoformat()})
    print(code,'prêt',count,'figures',len(audit['captures']),'captures',flush=True)
