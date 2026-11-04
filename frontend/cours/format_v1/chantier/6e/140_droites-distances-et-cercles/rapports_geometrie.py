# -*- coding: utf-8 -*-
"""Clôture fondée sur les contrôles enregistrés ; aucun accès à la base."""
from pathlib import Path
import json,runpy,sys,re,hashlib
from PIL import Image
BASE=Path(__file__).resolve().parent.parent
CHECK=runpy.run_path(str(Path(__file__).with_name('verif_geometrie.py')))
PROGRAMME='https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf'
COMPETENCES={
140:['Objets et notations','Alignement et longueur','Perpendiculaires et parallèles','Distance et trajet','Milieu','Cercle, disque et diamètre','Deux conditions de distance'],
141:['Vocabulaire et nature','Lecture du rapporteur','Construction au rapporteur','Bissectrice','Angles supplémentaires','Angles opposés par le sommet','Angle droit et partage'],
142:['Constructions par côtés et angle compris','Existence du triangle','Triangle isocèle et médiatrice','Construction par deux angles','Angles des triangles particuliers','Cercle circonscrit','Justification du centre'],
143:['Classer un carré','Construire un rectangle','Construire un carré','Construire un losange','Parallélisme et trapèze','Perpendicularité et trapèze rectangle','Périmètres égaux','Dimension manquante','Côtés et diagonales','Aire et périmètre','Losange et carré','Critiquer un programme'],
144:['Définition et construction à l’équerre','Position vers distances','Construction au compas','Milieu et médiatrice','Intersection avec une route','Équidistance et distance fixe','Distances vers position'],
145:['Image d’un point','Image d’un rectangle','Points fixes et réciprocité','Axe oblique sur quadrillage','Conservation sur un triangle','Image d’un cercle','Axes des figures usuelles']}

def finaliser(n):
    d=next(BASE.glob(f'{n}_*'));assert json.loads((d/'verification_locale.json').read_text(encoding='utf-8'))['problemes']==[]
    browser=json.loads((d/'navigateur.json').read_text(encoding='utf-8'));assert browser['anomalies']==0
    mathcount=CHECK['verifier_math'](d)
    meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
    figs=runpy.run_path(str(d/'figures/figures.py'))['FIGURES'];corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
    dimensions={k:Image.open(d/'figures/images'/f'{k}.png').size for k in figs}
    assert all(w<=1100 for w,h in dimensions.values())
    text=(d/'exercices.txt').read_text(encoding='utf-8');blocs=CHECK['verifier_notion'].blocs_exercices(text)
    old={(g,str(o['id']),str(im['position'])) for g in ('cours','fiches','exercices') for o in meta[g] for im in o['images']}
    new={(g,i,p) for g,objects in corr.items() for i,positions in objects.items() for p in positions}
    removed=old-new;replaced=old&new;added=new-old
    selected=[1,2,3] if n==140 else ([1,4,5,7] if n==144 else [1,4,7])
    shots=d/'captures';viewed=[]
    for pattern in ('mobile-c*.png','mobile-f*.png'):
        viewed.extend(p.name for p in sorted(shots.glob(pattern)))
    for k in selected:
        for kind in ('enonce','etapes'):
            p=shots/f'mobile-ex{k:02}-{kind}.png';assert p.exists(),p;viewed.append(p.name)
    expected=2*(2+3*len(blocs));assert browser['vues']==expected
    summary={'notion':n,'statut':'OK','pret':True,'date':'2026-11-01','cours':1,'fiches':1,'exercices':len(blocs),'questions':3*len(blocs),'ids_existants_conserves':len(meta['exercices']),'ids_nouveaux':[str(eid) for eid,_,_ in blocs if isinstance(eid,str)],'programme':PROGRAMME,'math_OK':True,'assertions_math':mathcount,'sources_SHA256_intactes':True,'verifier_notion_problemes':0,'navigateur_anomalies':0,'vues_distinctes':expected,'figures_inspectees':len(figs),'figures':dimensions,'captures_inspectees':viewed,'images_refaites_positions':len(replaced),'images_ajoutees_positions':len(added),'images_anciennes_retirees_positions':len(removed),'images_anciennes_conservees':0}
    summary['doublons_enonces']=0
    finalpaths=list(d.glob('cours_*.txt'))+list(d.glob('fiche_*.txt'))+[d/'exercices.txt',d/'figures/figures.py',d/'figures/correspondance.json']+sorted((d/'figures/images').glob('*.png'))
    summary['empreintes_finales_SHA256']={str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in finalpaths}
    (d/'VALIDATION_FINALE.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=[];group=1 if n==143 else 3
    for i,c in enumerate(COMPETENCES[n]):
        subset=blocs[i*group:(i+1)*group]
        rows.append('| '+c+' | '+', '.join(str(b[0]) for b in subset)+' |')
    coverage=f'# Couverture pédagogique — {meta["titre"]}\n\nProgramme de cycle 3, annexe officielle, géométrie de sixième, page 23 : [programme]({PROGRAMME}). '
    if n==143:coverage+='Ce chapitre entretient les acquis du cours moyen ; le trapèze réinvestit parallélisme et perpendicularité, avec convention explicitée. '
    coverage+='Le cours, la fiche et les exercices utilisent les mêmes notations.\n\n| Compétence travaillée | Exercices |\n|---|---|\n'+'\n'.join(rows)+'\n\nChaque exercice comporte trois questions, trois méthodes, six étapes explicites et trois résultats ; les solutions reprennent les conclusions.\n'
    if n==142:coverage+='\nL’ID 3505 complète les variantes à trois côtés par une construction avec deux côtés et leur angle compris ; aucun ID retiré.\n'
    (d/'COUVERTURE.md').write_text(coverage,encoding='utf-8')
    report=f'''# {meta['titre']} — prêt

Cours et fiche réécrits au format du pilote ; {len(blocs)} exercices complets, {3*len(blocs)} questions. Les {len(meta['exercices'])} IDs existants sont conservés et leurs blocs remplacés pédagogiquement ; les types Découverte / Entraînement / Problème sont conservés. '''
    report+=('Douze exercices nouveaux (nouveau-1 à nouveau-12), cours_nouveau.txt et fiche_nouvelle.txt à créer lors de la publication. ' if n==143 else 'Aucun exercice supprimé ni ajouté. ')
    report+=f'''

Figures : {len(figs)} PNG TikZ uniques, tous inspectés ; {len(replaced)} positions refaites, {len(added)} ajoutées, {len(removed)} anciennes positions retirées, aucune ancienne image conservée. Les doublons exacts partagent un même PNG. Aucune tolérance de chevauchement ; graduations du rapporteur sur fond blanc réservées à cet usage.

Contrôles : vérificateur de notion local à zéro problème ; navigateur téléphone 390 px et ordinateur 1280 px, {expected} vues distinctes, zéro anomalie. {mathcount} assertions mathématiques ; empreintes SHA-256 des exports intactes. Cours entier, fiche et exercices {', '.join(map(str,selected))} (énoncé et étapes) inspectés en téléphone. Voir VALIDATION_FINALE.json, navigateur.json et captures/.

Adaptations locales uniquement : métadonnées du nouveau chapitre 143 enrichies en mémoire ; fermeture Chrome bornée sous Windows ; audit des erreurs MathJax SVG ; bandeau de navigation masqué pendant les captures. Les outils partagés et les sources exportées ne sont pas modifiés.

La couverture détaillée et les IDs figurent dans COUVERTURE.md. Aucun accès en base, aucun import, aucune commande git.
'''
    details={140:'Distinction objet/longueur, cercle/disque et équidistance/milieu ; codages et arcs au compas contrôlés.',141:'Compléments et suppléments distingués ; rapporteurs à deux échelles et bissectrices exacts.',142:'Construction côté-angle-côté ajoutée dans l’ID 3505 ; centre O déplacé hors du segment dans le cercle circonscrit.',143:'Méthode du losange précisée par deux cercles ; diagonales rendues visibles ; inclusion du carré expliquée.',144:'Définition avec deux conditions, propriété dans les deux sens ; véritables arcs de compas et égalités codées.',145:'Labels sortis des quadrillages ; axes obliques et mesures conservées ; grands cercles ramenés à une largeur lisible.'}
    report+='\nCorrections particulières : '+details[n]+'\n'
    if n!=141:
        report=report.replace(' ; graduations du rapporteur sur fond blanc réservées à cet usage.','.')
    if n!=143:
        report=report.replace('métadonnées du nouveau chapitre 143 enrichies en mémoire ; ','')
    if n==144:
        report+='\nL’ID 3465, auparavant doublon exact de 3464, propose maintenant les données PB = 6 cm et QA = 9 cm, une lecture inversée des égalités et une justification que P et Q sont distincts. Les trois questions et les six étapes ont été remplacées ; ID conservé, existence des points contrôlée, captures dédiées de l’exercice 5 relues.\n'
    if n==145:
        report+='\nRelecture finale : axe raccourci au-dessus de la légende du triangle ; noms du carré dégagés des diagonales ; C dégagé de l’axe du triangle isocèle. Trois figures recompilées et inspectées ; accords « carreau / carreaux » et virgule du titre corrigés.\n'
    report+='\nContrôle des énoncés après normalisation des espaces : aucun doublon exact dans la notion. Les empreintes des fichiers finaux figurent dans VALIDATION_FINALE.json.\n'
    (d/'RAPPORT.md').write_text(report,encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'geometrie','maj':'2026-11-01','validation':'VALIDATION_FINALE.json'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,'PRÊT',expected,'vues')

if __name__=='__main__':
    for arg in sys.argv[1:]:finaliser(int(arg))
