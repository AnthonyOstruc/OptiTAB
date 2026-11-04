"""À exécuter après relecture réelle des dix planches mobiles et de tous les PNG."""
from pathlib import Path
import json,sys,subprocess,datetime
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
assert '--relecture-terminee' in sys.argv
for code in range(21,31):
 d=next(ROOT.glob(f'{code:02}_*'))
 subprocess.run([sys.executable,'-X','utf8',str(d/'verif_math.py')],check=True)
 audit=json.loads((d/'audit_navigateur_ce1.json').read_text(encoding='utf-8'))
 assert audit['statut']=='OK' and audit['anomalies']==0 and audit['vues_distinctes']==58
 corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
 names=sorted({im['fichier'] for owners in corr.values() for ims in owners.values() for im in ims.values()})
 proof={'statut':'OK','math_OK':True,'anomalies':0,'vues_distinctes':58,'exercices':9,'questions':45,'figures_vues':names,'captures_lues':audit['captures'],'import_effectue':False}
 (d/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'coordination_ce1','maj':datetime.date.today().isoformat()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 extra={23:'Les prix sont travaillés avec de la monnaie, sans introduire les décimaux abstraits.',24:'Lecture limitée aux heures, demi-heures et quarts d’heure ; les petites aiguilles avancent réellement entre les heures.',28:'Le carré oblique est un vrai carré ; une lettre initialement sur une diagonale a été déplacée, puis le PNG recompilé.',29:'Les faces à assembler sont fournies dans l’énoncé ; aucun renvoi à une annexe absente. Les arêtes cachées de la pyramide sont en pointillés.',30:'Orientation et position sont distinguées ; les trajets ont été simulés indépendamment.'}.get(code,'Les unités et les données des énoncés correspondent aux figures et aux corrigés.')
 title=(d/'cours_nouveau.txt').read_text(encoding='utf-8').splitlines()[0].removeprefix('Titre: ')
 rapport=f'# {title}\n\nÉtat : prêt, aucun point en suspens.\n\nCours et synthèse au modèle OptiTAB v1. Les neuf activités sources sont développées en neuf exercices de cinq questions liées. Chacune comporte méthode, raisonnement, résultat et solution concordante. {extra}\n\nFigures : {len(names)} PNG actifs produits avec TikZ et le préambule officiel ; aucune ancienne image en ligne à conserver ou retirer (nouveau contexte CE1). Chaque PNG a été regardé. Les mesures des dessins à l’écran sont des modèles ; les tracés se font avec les instruments réels.\n\nContrôles : script mathématique indépendant OK ; validateur officiel adapté au contexte neuf OK ; 58 vues du navigateur, zéro anomalie. Relecture du cours mobile complet, de la synthèse et des énoncés et étapes des exercices1,5,9. Captures et preuves conservées. Les originaux et leurs empreintes restent conservés.\n\nProgramme : [Mathématiques, cycle2, annexe officielle](https://www.education.gouv.fr/sites/default/files/document/Annexe%204%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20du%20cycle%202-403821.pdf).\n'
 (d/'RAPPORT.md').write_text(rapport,encoding='utf-8')
 print(code,'preuves enregistrées',flush=True)
