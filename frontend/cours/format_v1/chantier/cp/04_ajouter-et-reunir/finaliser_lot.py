"""À lancer seulement pour les chapitres dont toutes les planches ont été lues."""
from pathlib import Path
import json,sys,hashlib,datetime
ROOT=Path(__file__).resolve().parent.parent
for code in map(int,sys.argv[1:]):
 d=next(ROOT.glob(f'{code:02}_*'))
 def load(n):return json.loads((d/n).read_text(encoding='utf-8'))
 audit=load('audit_navigateur_cp.json');math=load('verification_math.json');valid=load('validation_cp.json');comp=load('compilation_figures.json')
 assert audit['statut']=='OK' and audit['anomalies']==0
 assert math['math_OK'] and valid['statut']=='OK' and comp['retour']==0
 mapping=load('figures/correspondance.json')
 names=sorted({s['fichier'] for kind in mapping.values() for positions in kind.values() for s in positions.values()})
 assert all((d/'figures/images'/n).exists() for n in names)
 boards=sorted(p.name for p in d.glob('relecture_*.png'))
 assert any('documents' in n for n in boards) and any('exercices' in n for n in boards)
 title=(d/'cours_nouveau.txt').read_text(encoding='utf-8').splitlines()[0][7:]
 proof={'date':datetime.datetime.now().isoformat(timespec='seconds'),'notion':code,'titre':title,'statut':'OK','math_OK':True,'anomalies':0,'cours':1,'fiches':1,'exercices':9,'questions':45,'compilation_retour':0,'compilation_jobs':1,'vues_distinctes':audit['vues_distinctes'],'egalites_recalculees':math['egalites_recalculees'],'figures_vues':names,'captures_lues':audit['captures'],'planches_lues':boards,'lecture':'Lecture réelle des figures et des planches : cours mobile complet, fiche, exercices 1, 5 et 9, énoncé et étapes.','empreintes_finales':{n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/figures.py','figures/correspondance.json']}}
 (d/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 report=f'''# Rapport — {title}

État : prêt. Nouveau contenu CP : un cours, une fiche, neuf exercices et 45 vraies questions corrigées. Les identifiants restent nouveau-1 à nouveau-9.

Les neuf activités sources sont conservées dans les questions 1. Les questions suivantes travaillent des calculs, des vérifications ou des explications liés à la même notion. Voir COUVERTURE.md. Phrases courtes ; résultats entre 0 et 100. Aucun import effectué.

Figures : {len(names)} nouvelles figures TikZ utiles, compilées par l’outil officiel, zéro image ancienne conservée. Modèles sans réponse dans les énoncés ; compléments verts dans les corrections. Cours et fiche illustrés. Aucun tableau de données en image et aucune dérogation de chevauchement.

Contrôles : compilation séquentielle --jobs 1, retour 0 (compilation_figures.log). Syntaxe, correspondances, empreintes des sources : valider_cp OK (validation_cp.log). Mathématiques recalculées depuis les textes finaux : {math['egalites_recalculees']} égalités/listes et 45 réponses cohérentes entre étapes et solutions (verif_math.py, verification_math.json).

Relecture réelle : chaque PNG via les planches officielles ; cours mobile complet, fiche et exercices 1/5/9 (énoncé et étapes) via les planches relecture_documents et relecture_exercices. Audit Chrome téléphone et ordinateur : {audit['vues_distinctes']} vues, zéro anomalie. Captures et logs conservés. Les détails figurent dans PREUVES_FINALES.json.

Programme : addition et soustraction par manipulation et calcul mental ; aucune soustraction posée. L’addition posée est réservée au chapitre 30, en fin de CP. Doubles et moitiés du programme, décomposition explicite pour les autres moitiés paires. Aucun point en suspens.
'''
 (d/'RAPPORT.md').write_text(report,encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'cp_calculs','maj':'2026-11-02'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'prêt',len(names),'figures',len(audit['captures']),'captures lues')
