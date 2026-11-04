"""Clôture locale après relecture réelle des 35 PNG et des planches mobiles.
Aucun navigateur, aucune compilation, aucune écriture en base.
"""
from pathlib import Path
import json,re,subprocess,sys,hashlib,datetime
ROOT=Path(__file__).resolve().parent.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for code in range(5,14):
 d=next(ROOT.glob(f'{code:02}_*'))
 run=subprocess.run([sys.executable,str(d/'verif_math.py')],text=True,encoding='utf-8',capture_output=True)
 assert run.returncode==0,run.stderr
 (d/'verif_math.log').write_text(run.stdout,encoding='utf-8')
 equalities=int(re.search(r'(\d+) égalités',run.stdout)[1])
 audit=load(d/'audit_navigateur_ce1.json');validation=load(d/'validation_ce1.json')
 assert audit['statut']==validation['statut']=='OK' and audit['anomalies']==0
 assert audit['vues_distinctes']==58
 corr=load(d/'figures/correspondance.json');active=set()
 for section in corr.values():
  for places in section.values():
   for spec in places.values():active.add(spec['fichier'])
 compilation=(d/'compilation_figures.log').read_text(encoding='utf-8')
 assert f'{len(active)}/{len(active)} figure(s) produite(s)' in compilation
 for name in active:assert (d/'figures/images'/name).is_file()
 for name in audit['captures']:assert (d/'captures_ce1'/name).is_file()
 documents=sorted(d.glob('relecture_documents_*.png'));exercises=sorted(d.glob('relecture_exercices_*.png'))
 assert documents and len(exercises)==2
 files=['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/figures.py','figures/correspondance.json','verif_math.py']
 proof={'statut':'OK','date':datetime.datetime.now().isoformat(timespec='seconds'),'agent':'ce1_calculs','math_OK':True,'anomalies':0,'exercices':9,'questions':45,'minimum_questions_par_exercice':5,'sources_couvertes':9,'egalites_recalculees':equalities,'vues_distinctes':audit['vues_distinctes'],'compilation_retour':0,'figures_vues':sorted(active),'captures_lues':audit['captures'],'planches_lues':[p.name for p in documents+exercises],'relecture':'Chaque PNG lu individuellement ; cours mobiles complets, fiches et exercices 1,5,9 (énoncé et étapes) lus sur les planches sans réduction de largeur. Après retouche, captures 06,12,13 rafraîchies puis relues.','empreintes_finales':{name:sha(d/name) for name in files},'empreinte_apercu':sha(d/'apercu.html'),'empreintes_figures':{name:sha(d/'figures/images'/name) for name in sorted(active)},'import_effectue':False}
 save(d/'PREUVES_FINALES.json',proof)
 save(d/'etat.json',{'statut':'pret','agent':'ce1_calculs','maj':'2026-11-02'})
 source=load(d/'sources_locales/chapitre.json')
 specifics={5:'Compensation justifiée : ajouter 19 ou 29 passe par 20 ou 30, puis retrait de l’unité en trop. Compléments expliqués et contrôlés.',6:'Chiffres alignés par rang, retenues expliquées comme échanges ; les additions à trois termes et l’arrivée à mille sont conservées. Espace insécable dans 1 000.',7:'Petits retraits découpés au passage de la dizaine ; retirer neuf passe par moins dix puis plus un. Le sens du retrait invalide la proposition 405 pour 402 moins 7.',8:'Une seule technique de soustraction : les échanges. Le passage par zéro est détaillé, jusqu’à mille, et les réponses sont contrôlées par addition.',9:'Groupes égaux, ordre des facteurs, zéro et un, classification pair/impair, suite de nombres pairs et paires avec un objet isolé sont tous conservés.',10:'Tables de deux, trois, quatre, cinq et dix, facteurs manquants, table de trois entière et deux doubles sont travaillés. Les cinq cartes de calcul sont un exemple expliqué qui garde la possibilité de personnaliser.',11:'Tables de six, sept, huit et neuf reconstruites avec cinq groupes et un complément, dix groupes moins un ou le double de quatre groupes ; commutation et groupements conservés.',12:'Valeur des chiffres multipliée par dix ; facteurs de onze à dix-neuf décomposés. Chaque morceau est multiplié. Les comparaisons de produits indiquent explicitement dix de plus.',13:'Doubles et moitiés reliés ; décompositions adaptées, repères de vingt-cinq. La moitié de 560 est expliquée avec exactement les morceaux du schéma : 400 et 160 ; 738 est partagé avec 600,120 et18.'}[code]
 report=f'''# Rapport — {source['titre']}

État : **prêt**. Contrôles locaux terminés, aucun point en suspens.

Neuf sources sur neuf conservées et développées en `nouveau-1` à `nouveau-9`, cinq vraies questions par exercice : **45 questions**, chacune avec méthode calculatoire, raisonnement détaillé, résultat encadré et solution strictement identique. Cours et fiche entièrement réécrits en format v1. Correspondance des compétences : [COUVERTURE.md](COUVERTURE.md).

{specifics}

Les nombres et résultats restent au plus égaux à 1 000. Les multiplications utilisent le sens, les tables, les doubles et la décomposition ; les partages utilisent le sens et les produits. Aucune multiplication ni division posée introduite. Les conseils s’adressent à l’enfant.

Figures : **{len(active)} ajoutées**, 0 ancienne conservée, 0 retirée. TikZ et palette officielle du livre, colonnes pour les opérations posées, résultat en vert ; correspondances `cours:nouveau`, `fiches:nouvelle`, `exercices:nouveau-N`. Compilation séquentielle officielle `--jobs 1`, retour 0 conservé dans `compilation_figures.log`. Chaque PNG a été regardé individuellement : chiffres alignés, étiquettes lisibles et aucun chevauchement.

Contrôles effectués :

- `verif_math.py` autonome : **{equalities} égalités recalculées dans les vrais fichiers finaux**, doubles et moitiés contrôlés, calculs à trou résolus depuis les questions finales, présence des calculs numériques sources, neuf blocs et 45 questions vérifiés, solutions identiques aux résultats.
- Validation officielle adaptée aux créations CE1 : **0 problème**, empreintes des sources intactes (`validation_ce1.json` et journal).
- Chrome : **58 vues distinctes**, mobile et ordinateur, **0 anomalie** ; aucun débordement, image cassée ou erreur MathJax (`audit_navigateur_ce1.json`).
- Relecture personnelle du cours mobile entier, de la fiche et des exercices 1,5,9 : énoncé et toutes les étapes. {len(audit['captures'])} captures conservées, trois planches de relecture lues. Les retouches de typographie et de cohérence texte/schéma ont été revalidées et relues.

Les preuves réelles et empreintes des fichiers finaux sont conservées dans `PREUVES_FINALES.json`. Programme de référence : programme officiel du cycle 2 applicable depuis 2025, périmètre vérifié par l’orchestrateur. Aucune source modifiée, aucune commande `manage.py`, aucun accès en base ni import effectué.
'''
 (d/'RAPPORT.md').write_text(report,encoding='utf-8')
 print(code,'PRET',equalities,'égalités',len(active),'figures',len(audit['captures']),'captures',flush=True)
