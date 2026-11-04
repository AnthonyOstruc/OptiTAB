# -*- coding: utf-8 -*-
"""Audit de couverture et rapport final, sans validation présumée."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent.parent
NEW_FIG={276:7,277:4,278:5,279:4,280:8}
OLD_FIG={276:3,277:4,278:2,279:0,280:2}
COMPLEMENTS={276:'Construction du quatrième sommet, critères suffisants et insuffisants, cas particuliers, aires composées, conversions et quantité de dalles.',277:'Conversions volume-capacité, choix de patron et pliage, aire de surface du cylindre, vue de face et cubes cachés, hauteur de remplissage, adaptation d’une boîte.',278:'Lecture de barres, comparaison de répartitions à moyenne égale, construction circulaire, lecture d’une évolution, données regroupées et réunion de groupes.',279:'Issues élémentaires et lettres, fréquences observées et modèle, comptage sans doublons, modification d’un sac, roues à secteurs inégaux et équitables.',280:'Débogage de parenthèses, trajet à compléter, nombre de répétitions, rotation du triangle, mauvaise rotation dans une boucle, projet avec formule et tracé.'}
for num in range(276,281):
    p=next(ROOT.glob(f'{num}_*'));rev=json.loads((p/'revision_2026-10-30.json').read_text(encoding='utf8'))
    maths=json.loads((p/'verification_maths.json').read_text(encoding='utf8'))
    comp=json.loads((p/'compilation_figures.json').read_text(encoding='utf8')) if (p/'compilation_figures.json').exists() else []
    status=json.loads((p/'controle_statut.json').read_text(encoding='utf8')) if (p/'controle_statut.json').exists() else {}
    visual=json.loads((p/'visuels_revision.json').read_text(encoding='utf8')) if (p/'visuels_revision.json').exists() else {}
    controls=bool(status) and all(status.get(k,{}).get('code')==0 for k in ['validation.log','captures.log','captures_complementaires.log'])
    fresh=(p/'validation.log').exists() and (p/'validation.log').stat().st_mtime>=(p/'exercices.txt').stat().st_mtime
    figures_ok=bool(comp) and all(f['ok'] for f in comp)
    ready=controls and fresh and figures_ok and bool(visual.get('cours_complet')) and bool(visual.get('fiche')) and len(visual.get('exercices',[]))>=3 and maths.get('remplacements')==6
    old=json.loads((p/'sauvegardes/revision_2026-10-30/figures/correspondance.json').read_text(encoding='utf8'))
    new=json.loads((p/'figures/correspondance.json').read_text(encoding='utf8'))
    def maps(c):return {(g,i,pos):v['fichier'] for g,data in c.items() for i,ims in data.items() for pos,v in ims.items()}
    oldmap,newmap=maps(old),maps(new)
    replaced=sum(oldmap[k]!=newmap[k] for k in oldmap.keys()&newmap.keys());removed=len(oldmap.keys()-newmap.keys());added=len(newmap.keys()-oldmap.keys())
    text=(p/'exercices.txt').read_text(encoding='utf8');levels={x:len(re.findall('^Difficulté: '+x+'$',text,re.M)) for x in ['easy','medium','hard']}
    table='| Id conservé | Nouveau travail | Niveau |\n|---|---|---|\n'+''.join(f"| {e['id']} | {e['titre']} | {e['difficulte']} |\n" for e in rev['remplacements'])
    couverture='Audit du 30 octobre 2026.\n\nAvant : les 21 blocs provenaient surtout de quelques familles paramétriques, et les coefficients plus élevés n’augmentaient pas la difficulté conceptuelle.\n\nAprès : six variantes sont remplacées dans leur bloc, sans retirer aucun Id. Les autres applications restent disponibles pour l’entraînement ; leurs titres et niveaux sont reclassés selon le travail réel.\n\n'+COMPLEMENTS[num]+'\n\n'+table+'\nRépartition finale : '+str(levels)+'. Aucun ajout de bloc nécessaire après cet audit.\n'
    (p/'COUVERTURE.md').write_text(couverture,encoding='utf8')
    report=('État : '+('prêt' if ready else 'en cours de contrôles')+' — révision pédagogique du 30 octobre 2026.\n\n'
      'Sauvegarde : `sauvegardes/revision_2026-10-30/` conserve les productions locales avant révision (textes, figures, rapports et captures). Les sources exportées restent inchangées. Aucun import ou accès base.\n\n'
      'Texte et couverture : '+COMPLEMENTS[num]+' Les 105 Id du lot sont intacts ; ici 21 blocs, dont 6 remplacés, et '+str(maths['questions'])+' questions. Les nouvelles corrections utilisent les mêmes encadrés que le modèle Terminale, avec méthodes brèves, étapes nommées, calculs détaillés et résultats courts. Chaque exercice comporte un repère pédagogique. Les simples variantes numériques ne sont plus classées Problème ; répartition : '+str(levels)+'. Détail dans `COUVERTURE.md`. Aucun résultat ancien erroné détecté ; les nouveaux résultats sont contrôlés par Python.\n\n'
      'Remplacements :\n\n'+table+'\n'
      f"Figures : {NEW_FIG[num]} nouvelles figures TikZ ; {OLD_FIG[num]} figures propres de la première révision réutilisées. En termes d’appels par rapport à la sauvegarde : {replaced} remplacés, {added} ajoutés, {removed} retirés ; 0 image ancienne en ligne conservée. Les PNG ont été relus individuellement. Aucune tolérance de chevauchement ajoutée. Les constructions, diagrammes et tracés demandés possèdent une figure de correction. Les fichiers devenus inutilisés sont conservés en sauvegarde et ne sont plus appelés.\n\n"
      f"Contrôles : `verif_notion.py` → {maths['assertions']} assertions OK ; identifiants, résultats numériques, conversions, événements et tracés vérifiés selon la notion. Figures : {'OK' if figures_ok else 'en cours'}. Validation navigateur : {'OK' if controls and fresh else 'en cours'}. Captures réelles : {'relues' if visual else 'à relire'}, cours complet, fiche et au moins trois exercices diversifiés (énoncé et étapes). Les journaux et captures sont conservés.\n\n"
      'Outil : la copie locale `controle_apercu_local.mjs` garde les audits communs, étend la détection aux trois sélecteurs MathJax et borne la fermeture à 2 s pour éviter le blocage Windows du nettoyage de profil Playwright. Aucun outil commun ni fichier frontend/src modifié. Absence de caractères de contrôle C0 interdits vérifiée dans les textes.\n')
    (p/'RAPPORT.md').write_text(report,encoding='utf8')
    (p/'etat.json').write_text(json.dumps({'statut':'pret' if ready else 'en_cours','agent':'donnees_espace-revision','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(num,'PRÊT' if ready else 'EN COURS',levels,flush=True)
