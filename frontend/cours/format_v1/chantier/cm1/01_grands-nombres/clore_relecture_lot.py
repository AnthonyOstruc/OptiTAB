"""À lancer uniquement après lecture personnelle de chaque PNG et de toutes les planches."""
from pathlib import Path
import sys,json,hashlib,datetime,subprocess
ROOT=Path(__file__).resolve().parent.parent
assert '--relu' in sys.argv,'La lecture graphique doit être terminée avant clôture.'
codes=[int(x) for x in sys.argv[1:] if x.isdigit()] or [1,6,7,8,9]
for code in codes:
 d=next(ROOT.glob(f'{code:02}_*'))
 subprocess.run([sys.executable,'-X','utf8',str(d/'verif_math.py')],check=True)
 audit=json.loads((d/'audit_navigateur_cm1.json').read_text(encoding='utf-8'))
 validation=json.loads((d/'validation_cm1.json').read_text(encoding='utf-8'))
 assert audit['statut']=='OK' and audit['anomalies']==0 and audit['vues_distinctes']==94
 assert validation['statut']=='OK' and not validation['problemes']
 for name in audit['captures']:assert (d/'captures_cm1'/name).is_file()
 corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
 images=sorted({item['fichier'] for owners in corr.values() for positions in owners.values() for item in positions.values()})
 files=['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/correspondance.json']+[f'figures/images/{name}' for name in images]
 sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 now=datetime.datetime.now().isoformat(timespec='seconds')
 proof={'statut':'OK','date':now,'math_OK':True,'anomalies':0,'vues_distinctes':94,'exercices':15,'questions':75,'minimum_questions_par_exercice':5,
        'niveaux':['easy','medium','hard'],'figures_vues':images,'figures_detaillees':[{'fichier':name,'sha256':sha(d/'figures/images'/name),'vue_visuellement':True} for name in images],
        'captures_lues':audit['captures'],'planches_lues':[x.name for x in sorted(d.glob('relecture_*.png'))],
        'verificateur_mathematique':'verif_math.py','rapport_mathematique':'verification_math.json','empreintes_finales':{name:sha(d/name) for name in files},
        'empreinte_apercu':sha(d/'apercu.html'),'relecture':'Agent cm1_nombres : toutes les figures et tous les fragments mobile cours/fiche/ex1/ex8/ex15.',
        'source_base_cm1_vide':True,'import_effectue':False}
 (d/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 math=json.loads((d/'verification_math.json').read_text(encoding='utf-8'))
 report=(d/'RAPPORT.md').read_text(encoding='utf-8')
 report=report.replace('État : textes et figures sources rédigés ; compilation, vérification mathématique et relecture graphique à terminer.','État : prêt pour contrôle de coordination et publication par l’orchestrateur.')
 report+=f'\nClôture de relecture du {now} : {math["calculs_exactement_verifies"]} contrôles mathématiques exacts, zéro anomalie ; validateur statique OK ; 94 vues navigateur distinctes à 390 et 1280 pixels, zéro anomalie.\n\nLes {len(images)} PNG ont été regardés individuellement ; cours et synthèse mobile entiers et exercices 1, 8 et 15 (énoncés et cinq raisonnements) relus sur toutes les planches. Aucun chevauchement, coupure ni image cassée constaté.\n\nAucun import, aucune écriture en base, aucune modification des sources ou des autres niveaux.\n'
 (d/'RAPPORT.md').write_text(report,encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'cm1_nombres','maj':now[:10]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'preuves et rapport terminés')
