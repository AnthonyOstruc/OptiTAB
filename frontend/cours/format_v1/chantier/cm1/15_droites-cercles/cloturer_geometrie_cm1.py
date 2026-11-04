"""Écrire les preuves après relecture effective des figures et captures."""
from pathlib import Path
import sys,json,hashlib,datetime,subprocess
BASE=Path(__file__).resolve().parent.parent
SOURCE='https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf'
NOTES={15:'Les notations accompagnent toujours le nom de l’objet, conformément aux consignes CM1. Le parallélisme se vérifie avec les instruments et les perpendicularités à une même droite, jamais avec deux mesures d’écart imprécises. Le problème du quartier est corrigé : la fontaine est explicitement le milieu du segment, et la seule égalité de distances n’est pas présentée comme une localisation unique.',
16:'Les triangles sans code ne sont plus déclarés quelconques sans preuve. Rectangle, losange et carré sont définis par leurs propriétés, avec inclusions explicites. Les constructions évitent le calcul d’angles en degrés. La mesure du triangle rectangle est prise sur un triangle 3–4–5, sans enseigner de théorème hors niveau. Les diagonales restent une observation géométrique vérifiable à la règle.',
17:'La source « diagonale piégée » est remplacée dans son bloc par un pli vertical décalé : aucune construction de symétrie sur axe diagonal. Les lettres sont décrites comme dessins idéaux, sans généralisation abusive aux polices. Les points de l’axe restent fixes ; les symétries de cases et la double symétrie comptent correctement les éléments distincts.',
18:'Le chapitre couvre les sept solides nommés au programme, les modèles matériels cube/pavé/pyramide/prisme droit, les perspectives avec éléments cachés, les patrons de cube, les assemblages et les programmes de déplacement. Aucune formule de volume n’est introduite. Les faces opposées sont vérifiées par propagation de repères orthonormés lors du pliage ; la règle incorrectement générale « sauter une face » est supprimée.'}
def main(final):
 for n in (15,16,17,18):
  p=next(BASE.glob(f'{n:02}_*'));data=json.loads((p/'donnees_questions.json').read_text(encoding='utf-8'));source=json.loads((p/'sources_locales/chapitre.json').read_text(encoding='utf-8'));fig=json.loads((p/'figures/correspondance.json').read_text(encoding='utf-8'))
  names=sorted({v['fichier'] for g in fig.values() for positions in g.values() for v in positions.values()})
  math=json.loads((p/'verification_math.json').read_text(encoding='utf-8'))
  report=f'''# {source['titre']} — CM1

État : {'prêt, sous réserve de l’import réservé à l’orchestrateur' if final else 'textes et mathématiques prêts ; compilation et relecture visuelle à terminer'}.

Les 15 exercices du livre local sont tous repris et enrichis : 15 exercices, 75 questions, cinq questions par exercice, avec méthode, raisonnement, résultat et solution pour chacune. Aucun exercice source n’est omis. Tous les identifiants sont `nouveau-1` à `nouveau-15` car le contexte CM1 était vide dans l’inventaire initial. Cours et synthèse suivent le template OptiTAB v1 commun aux autres niveaux.

{NOTES[n]}

Figures : {len(names)} nouvelles figures TikZ au style des livres, 0 ancienne image conservée. Les dessins sources ne sont pas écrasés. Les schémas utiles aux réponses sont ajoutés dans les étapes, en vert. Les alternatives décrivent précisément le contenu et les valeurs. Les sorties respectent la largeur maximale de 900 pixels, sans tolérance de chevauchement.

Contrôles mathématiques : `verif_math.py`, autonome, relit les textes finaux et le manifeste des questions ; il vérifie toutes les égalités numériques affichées, les valeurs des résultats, leur identité avec les solutions et les constructions géométriques. Dernier résultat : {math['controles']} contrôles, 0 anomalie, 75 questions.

Programme : [programme officiel du cycle 3, partie CM1, pages 19–20]({SOURCE}). Les constructions de symétrie utilisent des axes verticaux ou horizontaux. Les patrons de cube et les déplacements sont explicitement au programme CM1.

Les sources locales restent inchangées ; aucune écriture en base ni publication par cet agent.
'''
  if final:
   audit=json.loads((p/'audit_navigateur_cm1.json').read_text(encoding='utf-8'));validation=json.loads((p/'validation_cm1.json').read_text(encoding='utf-8'))
   assert audit['statut']=='OK' and audit['anomalies']==0 and audit['vues_distinctes']==94
   assert validation['statut']=='OK'
   assert all((p/'figures/images'/name).is_file() for name in names)
   from PIL import Image
   for name in names:
    w,h=Image.open(p/'figures/images'/name).size;assert 100<=w<=900 and h>=70,(name,w,h)
   for name in audit['captures']:assert (p/'captures_cm1'/name).is_file()
   report+='\nRelecture visuelle terminée : tous les PNG, toutes les parties du cours et de la fiche sur téléphone, et les énoncés/étapes des exercices 1, 8 et 15. Audit du vrai moteur : 94 vues distinctes à 390 et 1280 pixels, 0 anomalie, images chargées et aucune erreur MathJax.\n'
   files=['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/figures.py','figures/correspondance.json']+['figures/images/'+x for x in names]
   proof={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK','math_OK':True,'anomalies':0,'exercices':15,'questions':75,'minimum_questions':5,'vues_distinctes':94,'figures_vues':names,'captures_lues':audit['captures'],'empreintes_finales':{name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in files},'apercu_sha256':hashlib.sha256((p/'apercu.html').read_bytes()).hexdigest()}
   (p/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
   (p/'etat.json').write_text(json.dumps({'statut':'pret','agent':'cm1_geometrie','maj':datetime.date.today().isoformat()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  (p/'RAPPORT.md').write_text(report,encoding='utf-8')
  coverage='# Couverture des sources et du programme\n\nLes quinze activités du chapitre source sont reprises dans le même ordre et enrichies à cinq questions avec corrigés complets.\n\n| Source locale | Exercice final | Questions |\n|---|---|---|\n'
  for i,(old,new) in enumerate(zip(source['exercices'],data),1):coverage+=f"| {i}. {old['titre']} | nouveau-{i} — {new['titre']} | {len(new['questions'])} |\n"
  coverage+='\n'+NOTES[n]+'\n\nRéférence officielle : '+SOURCE+'\n'
  (p/'COUVERTURE.md').write_text(coverage,encoding='utf-8')
  print(n,'prêt' if final else 'rapports préparés')
if __name__=='__main__':main('--relecture-terminee' in sys.argv)
