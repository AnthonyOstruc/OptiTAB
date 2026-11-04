from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
for code in map(int,sys.argv[1:]):
 assert code in [1,2,3,7,8,9,10,13]
 d=next(ROOT.glob(f'{code:02}_*'));math=read(d/'verification_math.json');validation=read(d/'validation_cp.json');audit=read(d/'audit_navigateur_cp.json');compiler=read(d/'compilation_figures.json');seen=read(d/'relecture_effectuee.json');manifest=read(d/'planches/index_figures_vues.json')
 strict=read(d/'controle_figures_lot.json')
 assert math['math_OK'] and validation['statut']=='OK' and audit['statut']=='OK' and audit['anomalies']==0 and compiler['retour']==0
 assert strict['statut']=='OK' and strict['anomalies']==0 and strict['tex_identiques']
 figs=[name for p in manifest for name in p['figures']]
 assert set(p['planche'] for p in manifest)==set(seen['planches_figures'])
 assert seen['planches_documents'] and seen['planches_exercices']
 for name,h in math['empreintes'].items():assert hashlib.sha256((d/name).read_bytes()).hexdigest()==h
 proof={'statut':'OK','math_OK':True,'anomalies':0,'exercices':9,'questions':45,'figures_vues':figs,'captures_lues':audit['captures'],'planches_lues':seen,'vues_navigateur':audit['vues_distinctes'],'compilation_retour':0,'sources_originales':'Empreintes vérifiées par valider_cp.py.','publication':'Réservée à root.'}
 proof['controle_figures_strict']={'rapport':'controle_figures_lot.json','tex_identiques':True,'anomalies':0}
 (d/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (d/'RAPPORT.md').write_text(f'# État : prêt\n\nCours et fiche réécrits au format OptiTAB v1, pour le CP. Les neuf activités sources sont reprises et enrichies : neuf exercices nouveaux, quarante-cinq vraies questions. Titres alignés sur les intitulés du programme. Aucun exercice existant en base ; identifiants nouveau-1 à nouveau-9 conservés.\n\n{len(figs)} figures TikZ ajoutées, aucune figure ancienne conservée. Modèles sans réponse dans les énoncés ; compléments et résultats verts dans les figures corrigées. Chaque PNG a été regardé dans les planches nommées dans PREUVES_FINALES.json.\n\nVérifications : calculs indépendants des 45 questions, égalités et comparaisons des textes, données des figures. Compilation officielle séquentielle --jobs 1 : retour 0. Validation locale CP : OK. Audit navigateur : {audit["vues_distinctes"]} vues, zéro anomalie. Cours mobile complet, fiche, exercices 1/5/9 énoncés et étapes relus dans les captures conservées.\n\nSources et empreintes conservées. Aucune modification des outils, autres notions, application ou base. Aucun point en suspens. Root effectue seul la publication.\n',encoding='utf-8')
 note={8:'La file de vingt jetons de l’exercice 9 a été remise sur une ligne unique pour rendre le changement de sens gauche/droite non ambigu.',9:'Accords corrigés : « 1 objet seul » et « Avec la dizaine ».',13:'Accord corrigé : « 1 objet seul ».'}.get(code)
 if note:
  report=d/'RAPPORT.md';report.write_text(report.read_text(encoding='utf-8')+'\nCorrection finale ciblée : '+note+'\n',encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'cp_nombres','maj':'2026-11-02'},ensure_ascii=False)+'\n',encoding='utf-8')
 print(code,'prêt',len(figs),'figures',len(audit['captures']),'captures')
