from pathlib import Path
import sys,json,hashlib,datetime
ROOT=Path(__file__).resolve().parent.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for code in map(int,sys.argv[1:]):
 d=next(ROOT.glob(f'{code:02}_*'))
 math=load(d/'verification_math.json');validation=load(d/'validation_cp.json');audit=load(d/'audit_navigateur_cp.json');seen=load(d/'journal_relecture.json')
 assert math['math_OK'] and math['statut']=='OK' and validation['statut']=='OK' and audit['statut']=='OK' and audit['anomalies']==0
 assert (d/'compilation_retour.txt').read_text().strip()=='0'
 corr=load(d/'figures/correspondance.json');names={v['fichier'] for g in corr.values() for m in g.values() for v in m.values()}
 assert names==set(seen['figures']),('figures non relues',code,names-set(seen['figures']))
 for name in names:assert digest(d/'figures/images'/name)==seen['figures'][name],('figure modifiée après lecture',name)
 assert set(audit['captures'])==set(seen['captures'])
 for name in audit['captures']:assert digest(d/'captures_cp'/name)==seen['captures'][name],('capture modifiée',name)
 report={'statut':'OK','math_OK':True,'anomalies':0,'date':datetime.datetime.now().isoformat(timespec='seconds'),'cours':1,'fiches':1,'exercices':9,'questions':45,'figures_vues':sorted(names),'captures_lues':audit['captures'],'vues_navigateur':audit['vues_distinctes'],'verifications_math':math['verifications'],'compilation_retour':0,'validation':'validation_cp.json','audit':'audit_navigateur_cp.json','journal':'journal_relecture.json'}
 (d/'PREUVES_FINALES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 special={17:'Les problèmes du départ sont reconstruits par addition. Les exercices 6 et 8 explicitent les dizaines. Le problème à deux étapes reste sous 30.',18:'Groupes manipulés, dessins de rangées et de fleurs. Aucun symbole de multiplication. La situation de groupes inégaux est corrigée puis redessinée.',19:'Les activités sources 6 et 7 sur les bandes et les fractions sont remplacées par deux puis quatre collections égales, dont une à colorier. Aucune fraction. Les paquets et les parts égales restent dans le champ 0 à 30.',20:'Les neuf histoires sources sont reprises. Tous les nombres et résultats intermédiaires sont dans le champ 0 à 30. Les diagrammes montrent les deux changements dans leur ordre.',29:'Les enquêtes personnelles sont réellement demandées. Elles sont accompagnées de relevés autonomes de huit ou neuf réponses, recomptés indépendamment. Tableaux et double entrée en texte natif ; diagrammes en TikZ. Deux ou trois choix et moins de 40 personnes.'}[code]
 text=f'# Rapport CP{code}\n\nÉtat : prêt.\n\nUn cours, une fiche, neuf exercices nouveaux, chacun avec cinq questions liées (45 questions). Phrases courtes, méthodes et démarches détaillées, résultats repris à l’identique dans les solutions. Titres alignés sur les rubriques du programme.\n\n{special}\n\nFigures : {len(names)} figures TikZ ajoutées, aucune conservée ou retirée du site (nouveau chapitre). Modèles sans réponse dans les énoncés, réponses et constructions en vert dans les corrections. Aucun tableau de données en image.\n\nContrôles : compilation officielle séquentielle --jobs 1, retour 0 ; validation_cp OK ; {math["verifications"]} vérifications mathématiques indépendantes ; audit Chrome mobile et ordinateur, {audit["vues_distinctes"]} vues, zéro anomalie. Toutes les figures et les captures du cours mobile complet, de la fiche et des exercices 1, 5, 9 (énoncés et étapes) ont été lues. Empreintes des fichiers relus conservées dans journal_relecture.json.\n\nAucune source modifiée, aucun import. Aucun point en suspens. Publication réservée à l’orchestrateur.\n'
 (d/'RAPPORT.md').write_text(text,encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'cp_problemes_donnees','maj':'2026-11-02'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'prêt',len(names),'figures',len(audit['captures']),'captures')
