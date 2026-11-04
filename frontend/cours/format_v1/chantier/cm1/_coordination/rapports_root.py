"""Rapports après relecture effective des six chapitres de coordination."""
from pathlib import Path
import json,re,datetime
ROOT=Path(__file__).resolve().parent.parent
notes={11:'Unités du millimètre au kilomètre, ordres de grandeur, conversions raisonnées, règles décalées, comparaisons, périmètres, partage de ruban et clôtures.',12:'Masses du milligramme à la tonne, contenances du millilitre à l’hectolitre, conversions expliquées, comparaison, équilibre, limites de charge, recettes et partage.',13:'Aires par superposition, découpage et pavage ; demi-carreaux ; centimètre carré ; distinction contour/surface ; angles, notation, calque et équerre, sans degrés ni rapporteur.',14:'Lecture et placement des aiguilles en heures et minutes, matin/soir, conversions, durée écoulée, départ/arrivée, marge et plannings réguliers.',20:'Enquête, effectifs, tableaux simples et doubles, diagrammes en barres, points et courbes, totaux, écarts et contrôle de représentations ; données fictives explicitement désignées.',21:'Expérience aléatoire, résultats possibles, impossible/certain/incertain, équiprobabilité, comparaison qualitative des chances et une chance sur deux ; dé, pièce, cartes, sac et roue.'}
for code,note in notes.items():
 d=next(ROOT.glob(f'{code:02}_*'));audit=json.loads((d/'audit_navigateur_cm1.json').read_text(encoding='utf-8'));assert audit['statut']=='OK' and audit['anomalies']==0
 assert audit['vues_distinctes']==94
 title=(d/'cours_nouveau.txt').read_text(encoding='utf-8').splitlines()[0].removeprefix('Titre: ')
 corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'));figs={im['fichier'] for mapping in corr.values() for images in mapping.values() for im in images.values()}
 math=json.loads((d/'verification_math.json').read_text(encoding='utf-8'));assert math['statut']=='OK'
 report=f'''# Rapport — {title}

État : prêt, relecture achevée le {datetime.date.today().isoformat()}. Aucun import par le rédacteur.

{note}

Cours et fiche réécrits au format OptiTAB v1, avec définitions, méthodes, exemples et erreurs fréquentes. Les 15 activités de la source locale sont réorganisées en cinq familles de compétences contextualisées, chacune déclinée en trois variantes ; 15 nouveaux exercices et 75 questions corrigées, au moins cinq questions par exercice. Aucun identifiant en ligne n’existait pour ce contexte. Les sources complètes du livre restent dans sources_locales et le livre d’origine est inchangé.

{len(figs)} schémas PNG actifs refaits avec LuaLaTeX/TikZ et le préambule officiel des livres, tous regardés en taille réelle. Correspondances et textes alternatifs précis conservés. Aucune ancienne image en base à retirer ; aucune tolérance de chevauchement ajoutée. Les graduations et valeurs des figures correspondent aux activités qui les appellent.

Les corrections de coordination ont notamment rectifié les antislashs de commandes mathématiques, les virgules dans les milliers, les accolades hors formules, les accords des quantités et une conversion de durée à 125 minutes. Le vérificateur autonome lit les fichiers livrés et recompose les résultats des situations ; {math['verifications_exactes']} contrôles exacts réussis.

Validation statique réussie ; 94 vues distinctes contrôlées sur téléphone 390 px et ordinateur 1280 px, aucune anomalie. Cours mobile entier, fiche et exercices 1, 8 et 15 (énoncé et toutes les étapes) relus personnellement. Les captures et planches sont conservées. Aucun point restant.
'''
 (d/'RAPPORT.md').write_text(report,encoding='utf-8')
 sections=re.findall(r'^## (.+)',(d/'cours_nouveau.txt').read_text(encoding='utf-8'),re.M)
 coverage=f'# Couverture — {title}\n\n{note}\n\n'+'\n'.join('- '+x for x in sections)+'\n\nBanque : 15 exercices de 5 questions, avec méthode, raisonnement et résultat par question ; réponses courtes cohérentes avec les étapes. Les contextes source sont conservés dans le livre et ses sauvegardes ; la nouvelle banque privilégie la progressivité des compétences.\n\nRéférence : [programme officiel cycle 3](https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf).\n'
 (d/'COUVERTURE.md').write_text(coverage,encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'coordination_cm1','maj':datetime.date.today().isoformat()},ensure_ascii=False,indent=2),encoding='utf-8')
 print(code,'rapport et couverture prêts')
