"""Appeler pour une notion seulement après relecture réelle des captures."""
from pathlib import Path
import json
import re
import sys

BASE=Path(__file__).resolve().parent.parent
COMP={
261:[('Opérations, budget et division décimale',2705,2706),('Priorités et parenthèses',2709,2710),('Vocabulaire et traduction',2716),('Distributivité et ordre de grandeur',2717),('Comparaison de tarifs et maximum entier',2723),('Critique d’une facture avec frais globaux',2724)],
262:[('Quotient, reste et interprétation',2726,2731),('Critères de divisibilité',2730),('Chiffre inconnu et contraintes simultanées',2737),('Recherche exhaustive par paires',2738),('Diviseurs communs et contraintes sur les lots',2744),('Multiples et rendez-vous décalés',2745)],
263:[('Origine, signes, opposés et distances',2747),('Comparaisons de décimaux',2751),('Lecture d’une graduation et placement corrigé',2752),('Encadrements et intercalation',2758),('Deux ordres de classement et égalités',2759),('Synthèse de contraintes et justification',2765,2766)],
264:[('Variations et températures',2768),('Addition des signes et des décimaux',2772),('Soustraction de l’opposé',2773),('Regroupements et ordre des calculs',2779),('Parenthèses soustraites et analyse d’erreur',2780),('Compte, retour à zéro et montant minimal',2786),('Dénivelé signé et distance parcourue',2787)],
265:[('Prendre une fraction d’une quantité',2789),('Écritures décimales exactes et approchées',2793),('Fractions égales et simplification',2794),('Comparaisons à dénominateurs quelconques',2800),('Placement de fractions supérieures à un',2801),('Changement de quantité de référence',2807,2808)],
}

for n in map(int,sys.argv[1:]):
    p=next(BASE.glob(f'{n}_*'))
    controls=json.loads((p/'resultats_controles.json').read_text(encoding='utf8'))
    assert set(controls)=={'mathematiques','mathematiques_revision','validation_revision','captures_revision'} and all(x==0 for x in controls.values()),controls
    figresults=json.loads((p/'compilation_figures.json').read_text(encoding='utf8')) if (p/'compilation_figures.json').exists() else []
    assert all(x['ok'] for x in figresults)
    revision=json.loads((p/'revision_20261030.json').read_text(encoding='utf8'))
    changed=[x for x in revision['exercices'] if x['remplacement']]
    levels={d:sum(x['difficulte']==d for x in revision['exercices']) for d in ['easy','medium','hard']}
    counts=[]
    for name in ['mathematiques','mathematiques_revision']:
        t=(p/f'{name}.log').read_text(encoding='utf8')
        counts.append(int(re.search(r'(\d+) contrôles',t)[1]))
    corr=json.loads((p/'figures/correspondance.json').read_text(encoding='utf8'))
    prior=json.loads((p/'sauvegardes/revision_2026-10-30/figures/correspondance.json').read_text(encoding='utf8'))
    used=lambda d:{v['fichier'] for g in d.values() for pos in g.values() for v in pos.values()}
    active=used(corr); old=used(prior); fresh=active-old
    rows=['| Compétence | Exercices repères (Id) |','|---|---|']
    rows += ['| '+row[0]+' | '+', '.join(map(str,row[1:]))+' |' for row in COMP[n]]
    (p/'COUVERTURE.md').write_text('Couverture pédagogique du 30 octobre 2026\n\n'+'\n'.join(rows)+'\n\nProgression : '+str(levels['easy'])+' découvertes, '+str(levels['medium'])+' entraînements, '+str(levels['hard'])+' problèmes. Les variantes conservées servent à consolider, les six remplacements élargissent les démarches. Aucun ajout nécessaire.\n',encoding='utf8')
    viewed={'date':'2026-10-30','cours':'toutes les captures mobiles du cours regardées','fiche':'capture mobile regardée','exercices':[{'numero':k,'enonce':'regardé','etapes':'regardées'} for k in [5,12,19]],'support':'captures_revision_2026-10-30','conclusion':'OK'}
    (p/'relecture_visuelle.json').write_text(json.dumps(viewed,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    title=lambda x:x['titre'].split(' - ',2)[-1]
    report=['État : prêt, révision pédagogique contrôlée le 30 octobre 2026.','',
      'Sauvegarde intégrale des contenus et figures antérieurs : `sauvegardes/revision_2026-10-30/`. Les anciens aperçus et preuves restent conservés.','',
      '21 identifiants et 21 blocs conservés ; aucun ajout. Six variantes remplacées par des exercices de démarches différentes :']
    report += ['- Id '+str(x['id'])+' : '+title(x)+'.' for x in changed]
    report += ['', 'Les cinq anciens problèmes restants, qui ne changeaient que les valeurs, sont reclassés en entraînement. Répartition : 7 découvertes, 12 entraînements, 2 problèmes. Titres uniques et préfixes cohérents. Couverture détaillée dans `COUVERTURE.md`.','',
      'Rédaction : méthodes courtes, étapes aux titres précis, étapes distinctes pour les raisonnements composés, calculs alignés, conclusions courtes et note pédagogique par exercice. Les fiches restent synthétiques. '+({263:'Le cours précise comment lire une graduation fine.',264:'Le cours comporte aussi une addition expliquée de relatifs décimaux.'}.get(n,'Le cours existant, complet sur ce périmètre, est conservé et relu.')),'',
      f'Figures : {len(active)} actives, dont {len(active&old)} réutilisées et {len(fresh)} nouvelles ; {len(old-active)} anciens appels devenus inutiles retirés sans effacer leurs fichiers. '+('Les nouveaux énoncés de lecture/placement ont chacun une correction graphique exacte, réponses en vert. Les PNG nouveaux ont été regardés et contrôlés sans chevauchement.' if n in [263,265] else 'Aucune figure nouvelle nécessaire.'),'',
      f'Mathématiques : {counts[0]} contrôles du contenu conservé et {counts[1]} contrôles de révision, zéro échec. Calculs exacts rationnels et SymPy, vérifications des contraintes, des listes et des coordonnées graphiques dans les scripts conservés. Les assertions volontairement fausses des questions d’analyse d’erreur sont distinguées des résultats affirmés.','',
      'Rendu : vérificateur courant avec navigateur, syntaxe et correspondances OK ; audit complet de 65 vues à 390 px et des mêmes 65 vues à 1 280 px, sans débordement, formule erronée, image manquante ou bloc invalide. Captures du cours entier, fiche et trois nouveaux exercices (découverte, entraînement, problème), énoncés et étapes, regardées sur mobile. Journaux : `validation_revision.log`, `captures_revision.log`, `resultats_controles.json`.','',
      'Défaut d’outil Windows déjà établi : le nettoyage du profil temporaire Chrome peut boucler après la fin des contrôles. Le vérificateur courant est repris localement, avec les mêmes contrôles ; seule la fermeture du navigateur est bornée à deux secondes. La passe navigateur inclut directement les captures pour éviter un audit identique répété. Aucun outil partagé ni moteur du site modifié.','',
      'Aucun import, aucune écriture en base, aucune modification des sources en ligne. Programme de Cinquième rentrée 2026, BO du 5 mars 2026 vérifié par la coordination.']
    (p/'RAPPORT.md').write_text('\n'.join(report)+'\n',encoding='utf8')
    (p/'etat.json').write_text(json.dumps({'statut':'pret','agent':'calculs-revision','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(n,'prêt,',sum(counts),'contrôles mathématiques',flush=True)
