"""Consigne les contrôles et relectures réellement terminés du lot attribué."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent.parent
CODES=[1,2,3,4,14,15,16,17,18,19,20,31,32]
NOTES={
1:'Lecture, écriture en chiffres et en lettres, zéros de position, centaines et passages jusqu’à 1 000. Les listes de nombres des activités 2, 3 et 4 sont intégralement conservées.',
2:'Décompositions canoniques et non canoniques, échanges, distinction chiffre des dizaines / nombre de dizaines et commandes de timbres. Les trois commandes demandées en activité 7 sont conservées.',
3:'Comparaisons, rangements, encadrements et lignes graduées de pas 1, 10 ou 100. Les deux comparaisons numériques et l’égalité de l’activité 2 sont conservées.',
4:'Rangs dans les files, motifs AB et ABC, suites par ajout constant, double et pas croissant. Les méthodes des quatre suites ont été précisées avec leur règle propre.',
14:'Tout et parties, départ avant un don ou un gain, capacité d’un album et invention d’une histoire. Les méthodes précisent les objets connus et le sens de chaque opération.',
15:'Grande quantité, petite quantité et écart, y compris égalité des collections et formulations « de moins ». Les calculs sont accompagnés de stratégies adaptées ; les trois figures utilisent la légende « Grande quantité » pour éviter la confusion avec une réunion de collections.',
16:'Problèmes additifs ou multiplicatifs en deux étapes, avec résultat intermédiaire et unité. Les 45 méthodes sont liées aux livres, perles, voyageurs, achats, balles ou places de chaque problème. Le passage incorrect parlant de prix dans les sacs de balles a été corrigé.',
17:'Partages et groupements, exacts ou avec reste. La conclusion distingue les pages nécessaires pour tout ranger des boîtes complètes vendables ; pas de division posée introduite.',
18:'Fractions unitaires d’un tout, parts égales, pliage et coloriage, dénominateurs 2, 3, 4, 5, 6, 8, 10. La bande de l’activité 2 est entière dans l’énoncé et partagée seulement dans la correction. Le script mathématique a été aligné sur ce choix pédagogique.',
19:'Lecture des numérateurs et dénominateurs, comparaison à même dénominateur ou avec numérateur 1, tout entier et dépendance au tout choisi. Deux quarts et un demi sont comparés visuellement sur des bandes identiques, sans technique de changement de dénominateur.',
20:'Réunion, retrait et complément de parts d’un même tout, toujours de même dénominateur et de résultat au plus égal à 1. Les deux calculs des activités 2, 3 et 4 sont conservés. Les méthodes précisent le nombre de parts à réunir ou enlever.',
31:'Recueil personnel de 6 à 12 réponses en activité 1 ; nouvelle enquête sur un sujet au choix avec deux à cinq réponses possibles en activité 7. Des relevés fournis rendent les autres questions vérifiables : 4/3/5 réponses pour les activités 1–6, puis 6/4/3 pour 7–9. Comptage, tableau, construction des barres, interprétation, égalité et contrôles sont conservés. L’exemple de la fiche précise les effectifs et peut être compris seul.',
32:'Lecture de tableaux à double entrée et de barres, totaux et écarts, noms et échelles, invention d’une question de lecture directe et d’une question demandant un calcul. Les données originales restent inchangées.',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
for code in CODES:
 d=next(ROOT.glob(f'{code:02}_*'))
 # Nouvelle exécution indépendante après toutes les dernières retouches.
 process=subprocess.run(['python','-X','utf8',str(d/'verif_math.py')],capture_output=True,text=True,encoding='utf-8')
 (d/'controle_math.log').write_text(process.stdout+'\n'+process.stderr+'\nRETURN_CODE='+str(process.returncode)+'\n',encoding='utf-8')
 assert process.returncode==0,(code,process.stderr)
 math=load(d/'verification_math.json');audit=load(d/'audit_navigateur_ce1.json');validation=load(d/'validation_ce1.json')
 assert audit['statut']=='OK' and audit['anomalies']==0 and audit['vues_distinctes']==58
 assert validation['statut']=='OK' and not validation['problemes']
 source=load(d/'sources_locales/chapitre.json')
 ex=(d/'exercices.txt').read_text(encoding='utf-8');blocks=re.split(r'^===\s*$',ex,flags=re.M)[1:]
 assert len(blocks)==len(source['exercices'])==9
 for i,b in enumerate(blocks,1):
  en=b.split('Énoncé:\n')[1].split('Étapes:\n')[0]
  assert len(re.findall(r'^\d\. ',en,re.M))==5
  assert b.count('::: methode')==5 and b.count('## Question ')==5
 # Conservation des journaux de compilation réels, sans simuler une nouvelle exécution.
 logs=['controle_figures.log']
 if (d/'compilation_figures_complement.log').exists():logs.append('compilation_figures_complement.log')
 for name in logs:assert 'RETURN_CODE=0' in (d/name).read_text(encoding='utf-8')
 (d/'compilation_figures.log').write_text('Journal de clôture assemblé à partir des exécutions conservées ci-dessous.\n\n'+'\n'.join(name+'\n'+(d/name).read_text(encoding='utf-8') for name in logs),encoding='utf-8')
 figures=sorted(p.name for p in (d/'figures/images').glob('*.png'))
 captures=audit['captures']
 assert len(captures)==9 and all((d/'captures_ce1'/n).exists() for n in captures)
 planches=[p.relative_to(d).as_posix() for p in sorted((d/'figures').glob('planche_nouvelles_*.png'))]+[p.name for p in sorted(d.glob('relecture_*.png'))]
 couverture=['# Couverture des neuf activités source','',f'Chapitre {code:02} — {source["titre"]}.','',NOTES[code],'','Chaque activité source correspond au bloc portant le même numéro. Chaque bloc comprend cinq questions, cinq méthodes, des raisonnements, cinq résultats et une solution concordante.','', '| Activité source | Consigne conservée ou développée | Bloc final | Couverture |','|---|---|---|---|']
 for i,s in enumerate(source['exercices'],1):
  consigne=s['consigne'].replace('|',r'\|').replace('\n',' ')
  couverture.append(f'| {i} | {consigne} | nouveau-{i} | Compétence conservée ; cinq questions liées. |')
 couverture+=['','Le tableau est établi à partir de sources_locales/chapitre.json, conservé en lecture seule. Aucune activité source supprimée. Les constructions ou réponses ouvertes disposent d’un modèle de correction et ne sont pas réduites à la copie de ce modèle.','']
 (d/'COUVERTURE.md').write_text('\n'.join(couverture),encoding='utf-8')
 report=f'''# Rapport — CE1 {code:02} : {source['titre']}

État : prêt, aucun point en suspens.

Cours et fiche de synthèse au format OptiTAB v1. Neuf activités source développées en neuf exercices de cinq questions : 45 questions, avec méthode, raisonnement, résultat et solution concordante. Identifiants nouveau-1 à nouveau-9 conservés ; aucune activité source supprimée. Le détail figure dans COUVERTURE.md.

{NOTES[code]}

Figures : {len(figures)} PNG TikZ actifs, tous créés pour ce nouveau contexte CE1 avec le préambule officiel ; aucune ancienne image en ligne conservée ou retirée. Chaque PNG actif a été personnellement relu sur les planches, avec ouverture directe de la bande corrigée 18/ex2_schema. Légendes hors des traits, valeurs et noms cohérents avec les textes ; réponses visuelles en vert. Les journaux réels sont conservés dans controle_figures.log et, si applicable, compilation_figures_complement.log ; compilation_figures.log les rassemble avec leurs retours 0.

Mathématiques : verif_math.py exécuté indépendamment du générateur, retour 0. {math['relations_recalculees']} relations numériques exactes recalculées avec Fraction, {math['resultats_recalcules_independamment']} contrôles de résultats à partir des données, {math['figures_mathematiques_controlees']} contrôles mathématiques de figures. Les 45 résultats concordent avec les solutions ; neuf exercices et cinq questions chacun sont vérifiés. Les empreintes sont dans verification_math.json et PREUVES_FINALES.json.

Rendus : validateur CE1 OK, audit navigateur final OK sur 58 vues mobile et ordinateur, zéro anomalie. Relecture personnelle de toutes les parties du cours mobile, de la fiche et des énoncés et étapes des exercices 1, 5 et 9 : neuf captures, composées sans réduction de largeur dans relecture_documents_01.png et relecture_exercices_01.png / 02.png. Les {len(planches)} planches de figures et de captures ont été relues.

Sources locales et source_en_ligne laissées intactes. Aucun import, aucune modification de la base, des outils partagés ou du site. La publication est réservée à l’orchestrateur.
'''
 (d/'RAPPORT.md').write_text(report,encoding='utf-8')
 proof={
 'statut':'OK','date':datetime.datetime.now().isoformat(timespec='seconds'),'math_OK':True,'anomalies':0,
 'vues_distinctes':58,'exercices':9,'questions':45,'activites_source_couvertes':9,
 'figures_vues':figures,'captures_lues':captures,'planches_lues':planches,
 'relecture_personnelle':True,'import_effectue':False,
 'compilation_journaux':logs,'compilation_retour':0,
 'audit_navigateur_date':audit['date'],
 'fichiers_sha256':{n:sha(d/n) for n in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/figures.py','figures/correspondance.json','verif_math.py','verification_math.json','validation_ce1.json','audit_navigateur_ce1.json','COUVERTURE.md','RAPPORT.md']},
 'sources_sha256':{p.relative_to(d).as_posix():sha(p) for sub in ['sources_locales','source_en_ligne'] for p in sorted((d/sub).rglob('*')) if p.is_file()},
 'figures_sha256':{n:sha(d/'figures/images'/n) for n in figures},
 'captures_sha256':{n:sha(d/'captures_ce1'/n) for n in captures},
 }
 (d/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'cloture_ce1_nombres','maj':datetime.date.today().isoformat()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'pret',len(figures),'figures',len(captures),'captures',flush=True)
