"""Livre le chapitre pilote après contrôle et relecture visuelle des pages."""
from pathlib import Path
import json,hashlib,shutil,zipfile,re
R=Path(__file__).resolve().parent; ROOT=R.parent; B=R/'build'
report=json.loads((B/'verification.json').read_text(encoding='utf-8'))
pdf=B/'main.pdf'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert report['sha256']==sha(pdf)
assert report['pages']==report['pages_prevues'] and report['pagination_conforme']
assert not report['textes_hors_page'] and not report['collisions_candidates'] and not report['liens_internes_invalides']
assert len(report['controles_numeriques'])==48
log=(B/'main.log').read_text(encoding='utf-8',errors='replace')
assert not any(x in log for x in ['Overfull','Missing character','undefined references','multiply defined'])
report['relecture_visuelle']={
    'date':'2026-10-25','pages_relues':list(range(1,report['pages']+1)),
    'methode':f'Relecture des {report["pages"]} pages rendues avec Poppler ; réinspection isolée à 100 dpi des deux pages de sommaire et de leur raccord avec le tableau de bord.',
    'pages_reinspectees_apres_ajouts':[7,8,9,10],
    'constat':'Aucun défaut de débordement ou de collision repéré dans le rendu final.',
    'corrections':'Sommaire rapproché de la Terminale PC : cinq parties, une ligne par chapitre, pointillés et pagination à droite. Page Parcours et ressources séparée. Navigation et pagination recalculées.'}
sources=[
 {'id':'BO','titre':'Programme officiel physique-chimie MPSI, annexe 2','url':'https://www.education.gouv.fr/bo/21/Special1/ESRS2035779A.htm','pdf_url':'https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/8/spe779_annexe_1373648.pdf','fichier':'programme-officiel-2021-annexes.pdf','section':'1.1, pages internes 12 et 13 ; pages PDF 49 et 50'},
 {'id':'R1','titre':'MPSI DM1 Optique analyse dimensionnelle, 10 septembre 2026','url':'https://mpsi.schleck.ovh/fichiers/devoirs/dm1_optique_ad.pdf','fichier':'dm1-schleck-2026.pdf','section':'Exercice 2, II, questions 7 et 9, page 3/3'},
 {'id':'R2','titre':'MPSI DS1 Analyse dimensionnelle et optique géométrique, 17 septembre 2026','url':'https://mpsi.schleck.ovh/fichiers/devoirs/ds01_enonce.pdf','fichier':'ds1-schleck-2026.pdf','section':'II Détecteur de pluie, page 2/5'},
 {'id':'R3','titre':'Mines-Ponts Physique I MP, 2021','url':'https://concoursminesponts.fr/annales/','archive_url':'https://wordpress.concoursminesponts.fr/wp-content/uploads/2024/07/2021.zip','fichier':'Physique-MP-1-2021.pdf','chemin_archive':'2021/MP/Physique-MP-1-2021.pdf','section':'IV, questions 21 à 24, pages imprimées 5/6 et 6/6'}]
for s in sources:
    s['consultation']='2026-10-25';s['sha256_pdf_consulte']=sha(R/'recherche'/s['fichier'])
(R/'recherche/sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
report['sources']=sources
report['empreintes_sources_livre']={p.relative_to(R).as_posix():sha(p) for p in R.rglob('*') if p.is_file() and 'build' not in p.relative_to(R).parts and 'recherche' not in p.relative_to(R).parts and p.suffix in ['.tex','.sty','.py','.png']}
OUT=ROOT/'output/pdf/France/Physique-chimie';OUT.mkdir(parents=True,exist_ok=True)
previous_name='OptiTAB - Physique - MPSI - Chapitre 01 - Formation des images.pdf'
name='OptiTAB - Physique - MPSI - Chapitre 01 - Formation des images - Sommaire revise.pdf'
target=OUT/name
desktop=Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')/name
shutil.copy2(pdf,target);shutil.copy2(pdf,desktop)
assert sha(pdf)==sha(target)==sha(desktop)
V=ROOT/'output/verification';V.mkdir(exist_ok=True)
report['livraisons']=[str(target),str(desktop)]
report['statut']='Chapitre pilote livré pour validation ; suite non commencée.'
(V/'physique-mpsi-chapitre-01.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
md=f'''# Vérification du chapitre pilote de physique MPSI

Livraison révisée du 25 octobre 2026. **{report['pages']} pages ; premier chapitre avec pages liminaires complètes.**

Le document développe la section 1.1 Formation des images du programme de 2021.
La concordance des capacités figure page {report['positions_sections']['concordance']}. Il contient une page de titre,
les mentions éditoriales, un avant-propos, un mode d'emploi, un parcours de travail,
un sommaire général de 28 chapitres de physique dans la présentation de Terminale PC,
une page Parcours et ressources avec les liens du chapitre disponible,
un tableau de progression, une ouverture de chapitre, un diagnostic, 19 pages
de cours et méthodes, 24 exercices corrigés, 3 défis corrigés, un TP, une activité
numérique, un DM sur 20, un DS de 2 h sur 20 et trois parcours sur des supports
authentiques référencés. Les exercices OptiTAB sont identifiés comme originaux.

## Contrôles

- Compilation LuaLaTeX stabilisée : aucun Overfull, caractère manquant,
  renvoi indéfini ou étiquette en double.
- Pagination : {report['pages']} pages pour {report['pages_prevues']} pages prévues ; pas de page de continuation isolée.
- {report['entrees_sommaires_paginees']} entrées de navigation paginées vérifiées ; les chapitres à venir n'ont pas de pagination fictive.
- 48 contrôles numériques, incluant les conjugaisons, Newton, réfraction,
  projection, fibre, profondeur de champ, microscope, incertitudes et simulation.
- {report['placements_figures']} placements de figures vectorielles,
  {report['figures_uniques_utilisees']} figures distinctes utilisées.
- Aucun texte hors page et aucune collision de textes candidate détectés.
- {report['liens']} liens PDF ; aucun lien interne invalide détecté.
- Relecture visuelle des {report['pages']} pages de la nouvelle édition rendue avec Poppler ;
  réinspection isolée des pages 7 à 10 (sommaire, ressources, tableau de bord et ouverture).
- Aucun débordement, texte tronqué ou chevauchement de figure repéré dans le rendu final.
- Copie de bibliothèque et copie du Bureau identiques au PDF contrôlé.

Ces contrôles associent calculs, extraction géométrique et inspection visuelle.
Ils ne remplacent pas la validation pédagogique et éditoriale du propriétaire.
La vérification du programme concerne ce chapitre, pas les chapitres annuels à venir.

## Traçabilité

Empreinte SHA-256 du PDF : `{sha(pdf)}`.

Les références exactes, URL, pages et empreintes des quatre PDF consultés sont
dans le rapport JSON et dans `livre-physique-mpsi/recherche/sources.json`.
Les fichiers des auteurs extérieurs ne sont pas incorporés dans l'archive de sources
OptiTAB ; les liens du livre donnent accès aux supports originaux.

## Statut

**À valider ensemble avant la suite.** Aucun autre chapitre n'a été rédigé.
'''
(V/'physique-mpsi-chapitre-01.md').write_text(md,encoding='utf-8')
Z=ROOT/'output/sources';Z.mkdir(exist_ok=True)
archive=Z/'optitab-physique-mpsi-chapitre-01-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in R.rglob('*'):
        if p.is_file() and 'build' not in p.relative_to(R).parts and 'recherche' not in p.relative_to(R).parts and p.suffix in ['.tex','.sty','.py','.md','.png']:
            z.write(p,'livre-physique-mpsi/'+p.relative_to(R).as_posix())
    z.write(R/'recherche/sources.json','livre-physique-mpsi/recherche/sources.json')
index=ROOT/'output/pdf/README.md'
text=index.read_text(encoding='utf-8')
row=f'| MPSI - Physique | [Chapitre 01 - Formation des images - Pilote à valider](<France/Physique-chimie/{name}>) | {report["pages"]} |'
lines=text.splitlines()
if any(name in line or previous_name in line for line in lines):lines=[row if name in line or previous_name in line else line for line in lines]
else:lines.append(row)
index.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'pdf':str(target),'bureau':str(desktop),'sources':str(archive),'rapport':str(V/'physique-mpsi-chapitre-01.md'),'pages':report['pages'],'schema_placements':report['placements_figures'],'schema_distincts':report['figures_uniques_utilisees'],'sha256':sha(target)},ensure_ascii=False,indent=2))
