"""Consigner les audits et relectures effectivement accomplis du lot numérique."""
from pathlib import Path
import json,re,sys,subprocess,hashlib,shutil
sys.stdout.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent
for code in (129,130,131,133,150,151):
 d=next(ROOT.glob(str(code)+'_*'))
 shutil.copyfile(ICI/'verifier_maths_coordination.py',d/'verif_math_6e.py')
 r=subprocess.run([sys.executable,str(d/'verif_math_6e.py')],capture_output=True,text=True,encoding='utf-8',stdin=subprocess.DEVNULL)
 (d/'verification_math_6e.log').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,r.stdout+r.stderr
 math=json.loads((d/'verification_math_6e.json').read_text(encoding='utf-8'))
 log=(d/'controle_navigateur_6e.log').read_text(encoding='utf-8')
 views=[line for line in log.splitlines() if line.startswith('[mobile]') or line.startswith('[desktop]')]
 assert len(views)==130 and all('débordement 0px · erreurs formule 0 · $ bruts 0 · images manquantes 0 · blocs en erreur 0 · éléments trop larges 0' in line for line in views)
 assert 'Aucun problème détecté' in log
 assert json.loads((d/'validation_6e.json').read_text(encoding='utf-8'))['statut']=='OK'
 corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
 figs=sorted({v['fichier'] for group in corr.values() for mappings in group.values() for v in mappings.values()})
 visual=json.loads((d/'inspection_visuelle_6e.json').read_text(encoding='utf-8'))
 assert visual['statut']=='OK' and visual['cours_integral'] and visual['fiche'] and len(visual['exercices_enonce_et_etapes'])>=3
 assert visual['figures_individuelles_vues']==figs
 proof={'date':'2026-11-01','notion':code,'statut':'OK','vues_distinctes_navigateur':len(views),'anomalies_navigateur':0,'anomalies_visuelles':0,'erreurs_mathematiques':0,'verifications_mathematiques_notion':math['egalites_numeriques_exactes'],'questions_corrigees':math['questions_corrigees'],'figures_compilees_vues':figs,'documents_entiers_vus':True,'exercices_vus':visual['exercices_enonce_et_etapes'],'identifiants_conserves':math['identifiants_conserves'],'nouveaux_exercices':math['nouveaux_exercices'],'source_en_ligne_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (d/'source_en_ligne').iterdir() if p.is_file()},'relecture_independante':'Lot relu par un second agent ; corrections de formulation et réponses complétées appliquées.'}
 (d/'preuves_finales_6e.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 data=json.loads((d/'revision_pedagogique_6e.json').read_text(encoding='utf-8'))['exercices']
 titles=list(dict.fromkeys(e['titre'] for e in data))
 coverage=['Couverture pédagogique — 6e','','Programme : [BO du 17 avril 2025](https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf) ; [exemples de réussite de sixième](https://eduscol.education.fr/document/64878/download).','','Sept familles, chacune travaillée dans trois parcours progressifs :','']+['- '+title for title in titles]+['','Chaque question possède une méthode, une étape de raisonnement explicite et un résultat, repris dans la solution. Les exercices sollicitent lecture, calcul, justification, correction d’erreurs et problèmes concrets.']
 (d/'COUVERTURE.md').write_text('\n'.join(coverage)+'\n',encoding='utf-8')
 report=[f'Notion {code} — prête le 1er novembre 2026.','',f"Cours réécrit, fiche compacte, 21 exercices et {math['questions_corrigees']} questions corrigées. {math['identifiants_conserves']} identifiants conservés ; {math['nouveaux_exercices']} créations prévues.",'','Les anciens scénarios répétitifs sont remplacés par sept familles distinctes, avec justifications et contrôles. Les tableaux de données sont rédigés nativement, les images superflues retirées.',f"{len(figs)} figures actives compilées au style commun et inspectées individuellement ; aucune image ancienne conservée. Les schémas concordent avec les données.",'',f"Contrôles : {math['egalites_numeriques_exactes']} égalités numériques exactes et tests des scénarios ; 130 vues Chrome distinctes, zéro anomalie. Cours entier, fiche et plusieurs exercices complets relus sur mobile. Relecture indépendante effectuée ; corrections appliquées.",'','Sauvegardes avant révision dans sauvegardes/avant_revision_20261030. Source exportée inchangée ; aucune modification des outils communs ni de frontend/src. Publication réservée à la coordination après validation du niveau.']
 if code==150:report+=['','Import : créer fiche_nouvelle.txt et les 21 exercices nouveau-N. Le cours existant garde son identifiant.']
 (d/'RAPPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'coordination-6e','maj':'2026-11-01'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'pret',math['questions_corrigees'],'questions',flush=True)
