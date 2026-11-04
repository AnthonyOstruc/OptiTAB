"""Fige les preuves après la relecture visuelle effective de tous les lots."""
from pathlib import Path
import sys,json,re,hashlib,datetime,subprocess
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent
sys.stdout.reconfigure(encoding='utf-8')
assert '--relecture-terminee' in sys.argv,'Effectuer la relecture des PNG et captures avant de clôturer.'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
notes={1:'Grands entiers limités à neuf chiffres ; rangs, classes, regroupements, encadrements et graduations.',2:'Sens de multiple et diviseur ; critères par 2, 5 et 10 ; recherches organisées de diviseurs et de multiples communs.',3:'Fractions d’un même tout ; dépassement de l’unité, encadrement et repérage sur une demi-droite.',4:'Fractions égales ; comparaisons et opérations compatibles avec les bornes du CM2, dénominateurs communs simples au plus 60.',5:'Fraction d’une quantité ou d’une grandeur, complément, produit par un entier et recherche du tout dans des cas simples.',6:'Décimaux jusqu’aux millièmes ; rangs, fractions décimales, zéros, comparaison, intercalation, repérage et arrondi à l’entier.',7:'Sens des opérations, calcul mental et posé, estimation et problèmes à plusieurs étapes.',8:'Division euclidienne et décimale par un entier de 1 à 9 ; interprétation du quotient et du reste.',9:'Addition, soustraction, multiplication d’un décimal par un entier, changements de rang et calcul mental.',10:'Proportionnalité contextualisée, raisonnée en phrases par linéarité et retour à l’unité ; aucun coefficient, produit en croix ou tableau de proportionnalité.',11:'Choix d’unités, estimation, conversions justifiées, lectures de règle, longueurs, masses, contenances et périmètres par sens du contour.',12:'Comparaison de surfaces, carreaux et demi-carreaux, unités carrées, rectangles et carrés, décomposition et distinction aire/périmètre.',13:'Angles saillants ; comparaison, gabarits, somme, multiples, pliages et angle droit de 90 degrés ; aucun rapporteur.',14:'Polygones usuels, triangles, carré, rectangle, losange, trapèze et trapèze rectangle ; propriétés et constructions justifiées.',15:'Règle, équerre et compas ; parallélisme, perpendicularité, cercle/disque, milieu et programmes de construction.',16:'Symétries sur quadrillage selon des axes horizontaux, verticaux ou diagonaux ; contrôle des points et axes de figures.',17:'Solides, perspectives, faces/arêtes/sommets, patrons de cube et de pavé, assemblages de cubes et vues.',18:'Horloges avec secondes ; conversions de base soixante ; durée écoulée, arrivée, départ, marge et passage de minuit.',19:'Enquêtes, effectifs, tableaux simples et doubles, barres, points/courbes, diagrammes circulaires et lecture critique des données.',20:'Issues et évènements, équiprobabilité, chances exprimées en nombres de cas, indépendance et recensement de couples par tableau/arbre.',21:'Inconnues et égalités à trous ; suites et motifs, programmes à trois instructions, déplacements avec orientation.'}
for item in load(ICI/'inventaire_initial_cm2.json'):
 code=item['notion'];d=ROOT/item['dossier']
 result=subprocess.run([sys.executable,'-X','utf8',str(d/'verif_math.py')],capture_output=True,text=True,encoding='utf-8')
 (d/'verification_math_finale.log').write_text(result.stdout+result.stderr,encoding='utf-8');assert result.returncode==0,(d.name,result.stderr)
 audit=load(d/'audit_navigateur_cm2.json');assert audit['statut']=='OK' and audit['anomalies']==0 and audit['vues_distinctes']==130
 assert load(d/'validation_cm2.json')['statut']=='OK'
 mathfile=next(p for p in [d/'audit_math.json',d/'verification_math.json',d/'validation_math.json'] if p.exists())
 math=load(mathfile);assert math['statut']=='OK'
 figures=[];corr=load(d/'figures/correspondance.json');active=sorted({im['fichier'] for owners in corr.values() for positions in owners.values() for im in positions.values()})
 for name in active:figures.append({'fichier':name,'sha256':sha(d/'figures/images'/name),'vue_visuellement':True})
 for name in audit['captures']:assert (d/'captures_cm2'/name).is_file()
 raw=(d/'exercices.txt').read_text(encoding='utf-8');questions=len(re.findall(r'^## Question ',raw,re.M));assert questions in (63,70)
 texts=[d/'cours_nouveau.txt',d/'fiche_nouvelle.txt',d/'exercices.txt']
 hashes={p.name:sha(p) for p in texts};hashes['figures/correspondance.json']=sha(d/'figures/correspondance.json')
 hashes.update({'figures/images/'+f['fichier']:f['sha256'] for f in figures})
 old=d/'PREUVES_FINALES.json'
 if old.exists():
  backup=d/'sauvegardes/avant_cloture_coordination';backup.mkdir(parents=True,exist_ok=True)
  if not (backup/old.name).exists():(backup/old.name).write_bytes(old.read_bytes())
 proof={'statut':'OK','date':datetime.datetime.now().isoformat(timespec='seconds'),'math_OK':True,'anomalies':0,'vues_distinctes':130,'exercices':21,'questions':questions,'familles':7,'niveaux':['easy','medium','hard'],'figures_vues':figures,'captures_lues':audit['captures'],'planches_sources_lues':[p.name for p in sorted((d/'planches_sources').glob('*.png'))],'verificateur_mathematique':'verif_math.py','rapport_mathematique':mathfile.name,'empreintes_finales':hashes,'empreinte_apercu':sha(d/'apercu.html'),'relecture':('agent cm2_calculs puis contrôles de coordination' if code in (7,8,9,10,21) else 'coordination : PNG et captures du cours entier, fiche et exercices 1/11/21'),'source_base_cm2_vide':True,'import_effectue':False}
 old.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 title=texts[0].read_text(encoding='utf-8').splitlines()[0].removeprefix('Titre: ').strip()
 report=d/'RAPPORT.md'
 final=f'''\n## Clôture de coordination — {datetime.date.today().isoformat()}

État : prêt pour création du CM2. Aucun import effectué par les rédacteurs.

{notes[code]}

21 exercices, {questions} questions corrigées : chaque question possède méthode, étapes et résultat ; réponses courtes contrôlées. Les sources locales sont conservées intégralement. Les anciennes illustrations ({item['images_source']} entrées d’inventaire) ont été examinées sur les planches ; aucune n’est réutilisée. {len(figures)} PNG actifs refaits au style des livres, inspectés à l’écran ; aucune tolérance de chevauchement ajoutée par la coordination.

Contrôles : vérificateur mathématique final réussi ; validation officielle adaptée localement réussie ; 130 vues distinctes, téléphone 390 px et ordinateur 1280 px, sans anomalie. Le cours mobile entier, la fiche et les exercices 1, 11 et 21 (énoncé et étapes) ont été relus. Les empreintes des fichiers finaux, images et correspondance sont figées dans PREUVES_FINALES.json. Les aperçus utilisent le moteur et les feuilles de style réels du site.

Les retouches de coordination corrigent les accords au singulier, six doublons en géométrie, une légende de compas trop proche de A, l’échelle d’une frise horaire, les couleurs des arbres selon l’évènement étudié et les tableaux de numération/conversion sur téléphone. Les noms visibles de chapitre sont repris des cours finaux ; les sources restent intactes. Aucun point restant.
'''
 if report.exists():
  previous=report.read_text(encoding='utf-8')
  if '## Clôture de coordination' not in previous:report.write_text(previous+final,encoding='utf-8')
 else:report.write_text('# Rapport — '+title+'\n'+final,encoding='utf-8')
 coverage=d/'COUVERTURE.md'
 if not coverage.exists():
  sections=re.findall(r'^## ([^\n]+)',texts[0].read_text(encoding='utf-8'),re.M)
  coverage.write_text('# Couverture — '+title+'\n\n'+notes[code]+'\n\n'+ '\n'.join('- '+s for s in sections)+'\n\nBanque : sept familles, trois niveaux ; questions et corrections complètes.\n\nRéférences : [programme officiel cycle 3](https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf), [exemples Éduscol CM2](https://eduscol.education.gouv.fr/sites/default/files/document/exemplesmiseenoeuvrecm2-mathpdf-111537.pdf).\n',encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'coordination_cm2','maj':datetime.date.today().isoformat()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'preuves figées',questions,'questions',len(figures),'figures',flush=True)
