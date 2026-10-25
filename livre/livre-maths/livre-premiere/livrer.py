"""Prépare les livrables uniquement après la validation du PDF compilé."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output'
qa=json.loads((ROOT/'build/qa/controle-pdf.json').read_text(encoding='utf-8'))
maths=json.loads((ROOT/'build/audit-exercices.json').read_text(encoding='utf-8'))
programme=json.loads((ROOT/'build/couverture-programme.json').read_text(encoding='utf-8'))
structure=json.loads((ROOT/'build/verification-mathematique.json').read_text(encoding='utf-8'))
geometrie=json.loads((ROOT/'build/verification-figures.json').read_text(encoding='utf-8'))
relecture=json.loads((ROOT/'build/verification-relecture.json').read_text(encoding='utf-8'))
edition=json.loads((ROOT/'build/verification-edition-france.json').read_text(encoding='utf-8'))
code_pdf=json.loads((ROOT/'build/verification-code-pdf.json').read_text(encoding='utf-8'))
visuel=json.loads((ROOT/'build/audit-20261023/relecture-visuelle.json').read_text(encoding='utf-8'))
comparaison=json.loads((ROOT/'build/audit-20261023/comparaison.json').read_text(encoding='utf-8'))
BUREAU=Path.home()/'Desktop'/'Livres OptiTAB - Lycée'/'OptiTAB - Mathématiques - Première spécialité.pdf'
ARCHIVE=OUT/'archives'/'optitab-premiere-complet-avant-audit-2026-10-23.pdf'
# Depuis le 23 octobre 2026, la bibliothèque output/pdf est classée par pays et matière.
BIBLIOTHEQUE=OUT/'pdf'/'France'/'Mathématiques'/'OptiTAB - Mathématiques - Première spécialité - Manuel complet.pdf'
target=BIBLIOTHEQUE
target.parent.mkdir(parents=True,exist_ok=True)
digest=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest()
assert qa['source_sha256']==digest,'Le PDF a changé depuis le contrôle.'
assert code_pdf['source_sha256']==visuel['sha256']==digest
assert code_pdf['blocs_extraits']==code_pdf['blocs_executes']==28
assert code_pdf['equivalence_ast_avec_les_sources'] and not code_pdf['erreurs']
assert not visuel['defauts_restants']
assert not qa['blank_pages'] and not qa['out_of_page_text']
assert maths['exercices_controles']==210
assert qa['exercise_labels']==qa['answer_labels']==210
assert len(programme['couverture'])==60
assert geometrie['insertions_exercices_corriges']==72
assert relecture['exercices_relus']==210
assert edition['defis_controles']==14 and edition['sujets_controles']==2
assert qa['exercices_total']==224 and qa['edition_figures_with_text']==edition['insertions_visuelles']
assert comparaison['sha256_apres']==digest and visuel['pages_modifiees_relues']==comparaison['pages_modifiees']
# La version livrée avant l'audit du 23 octobre 2026 est archivée une seule fois, avant tout remplacement.
(OUT/'archives').mkdir(parents=True,exist_ok=True)
if not ARCHIVE.exists():
    shutil.copy2(target,ARCHIVE)
for sub in ('pdf','sources','verification'):
    (OUT/sub).mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/'main.pdf',target)
if BUREAU.parent.exists():
    shutil.copy2(ROOT/'main.pdf',BUREAU)
proofs=(ROOT/'annexes/demonstrations.tex').read_text(encoding='utf-8').count(r'\begin{demonstration}')
figures=sum(p.read_text(encoding='utf-8').count(r'\begin{tikzpicture}')+p.read_text(encoding='utf-8').count(r'\figureGeo')+p.read_text(encoding='utf-8').count(r'\figureLivre') for folder in ('chapitres','corriges','annexes') for p in (ROOT/folder).glob('*.tex'))
report=f'''# Vérification du livre OptiTAB de Première

Édition du 23 octobre 2026, après audit de conformité. Première générale, spécialité mathématiques.

## Contenu livré

- {qa['pages']} pages, 14 chapitres et 224 exercices corrigés : 210 exercices de chapitre et 14 défis d'approfondissement.
- Deux sujets blancs originaux au format de l'épreuve anticipée (session 2028) : 24 automatismes à réponses courtes issus des listes officielles, dont 6 lectures graphiques ou de tableau, et 4 exercices, corrigés et barème d'entraînement.
- Cours, méthodes, problèmes progressifs, {proofs} démonstrations de référence.
- {figures} représentations dans les cours, exercices et annexes : figures, graphiques, arbres et tableaux, en plus des couvertures et décors d'ouverture.
- Les 30 exercices des deux chapitres de géométrie ont chacun leur figure, également reprise et complétée dans le corrigé ; six exercices géométriques de trigonométrie sont aussi illustrés.
- Pages de garde, avant-propos, mode d'emploi, parcours de travail, sommaire et suivi des exercices.
- {qa['bookmarks']} signets et {qa['links']} liens contrôlés.

## Programme

Référence : [BO du 2 avril 2026, NOR MENE2602917A](https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A), applicable à la rentrée 2026-2027.

La matrice éditoriale repère 60 groupes de contenus, capacités, démonstrations et exemples d'algorithmes dans les cours, exercices, sujets et annexes. Les approfondissements facultatifs sont sélectionnés ; le livre ne prétend pas les inclure tous. Les ressources transversales sont destinées à être utilisées au fil de l'année.

## Vérifications effectuées

- Correspondance des 210 énoncés avec 210 corrigés et progression de difficulté.
- {maths['groupes_de_controles']} groupes de contrôles de résultats, répartis sur tous les exercices : calculs symboliques ou exacts, valeurs numériques, énumérations probabilistes et cas limites.
- Exécution des {maths['blocs_python_executes']} blocs Python des chapitres, tests des fonctions et contrôle de la reproductibilité des simulations à graine fixée.
- Contrôle des 28 programmes extraits du PDF lui-même : syntaxe valide sans substitution de caractères, structure syntaxique fidèle aux sources, exécution et tests ciblés sur les neuf anomalies de l’audit fourni. L’indentation est reconstruite à partir des positions des glyphes ; le contrôle ne garantit pas le comportement de copie de tous les lecteurs PDF.
- {structure['checks_passed']} contrôles complémentaires de structure et de calcul.
- {geometrie['controles_reussis']} contrôles de présence et de cohérence des figures : incidences sur les cercles, équations des droites et codages des angles droits.
- Passe éditoriale documentée pour les 210 couples énoncé/corrigé : choix de représentation et démarche de résolution indiqués dans la matrice jointe.
- {relecture['corriges_reecrits']} corrigés réécrits et {relecture['explications_complementaires']} explications complémentaires ciblées, avec une démarche explicite dans chaque corrigé.
- {relecture['controles_reussis']} contrôles supplémentaires de relecture, dont les poids des {relecture['arbres_controles']} arbres et les calculs de {relecture['tableaux_variations_controles']} tableaux de variations.
- {edition['controles_reussis']} contrôles de l'édition France : 14 défis, 24 automatismes, 4 problèmes et exécution des {edition['nouveaux_programmes_executes']} nouveaux programmes Python. Les {edition['nouveaux_visuels']} nouveaux visuels donnent {edition['insertions_visuelles']} insertions supplémentaires.
- Modalités de l'épreuve vérifiées sur la [note de service du 11 septembre 2026](https://www.education.gouv.fr/bo/2026/Special4/MENE2622640N) (BO spécial n° 4 du 17 septembre 2026) : application en 2026-2027, baccalauréat session 2028 ; 2 heures, coefficient 2, sans calculatrice ; automatismes à réponses courtes sur 6 points, deux ou trois exercices sur 14 points, maîtrise de la langue sur 2 points. Les sujets sont des créations et leur barème détaillé est un choix pédagogique.
- Renvois et pagination stabilisés ; absence d'avertissement de débordement, de référence non résolue ou de caractère manquant.
- Rendu de toutes les pages en PNG ; comparaison au pixel à 80 dpi avec la version précédente : {comparaison['pages_identiques']} pages identiques, {len(comparaison['pages_modifiees'])} pages modifiées toutes relues. Absence de texte hors page. Les pages de notes lignées sont intentionnelles.
- {qa['reading_blocks_checked']} blocs de lecture vérifiés ; les {qa['geometry_figures_with_exercise']+qa['new_figures_with_exercise']} représentations liées aux exercices restent sur la même page que le texte correspondant.
- {qa['edition_reading_blocks']} pages de parcours avancé et de sujets contrôlées ; les {qa['edition_figures_with_text']} figures de ces pages restent avec le texte correspondant.

Les contrôles informatiques soutiennent la relecture mathématique ; ils ne constituent pas une preuve formelle automatique de tout le texte.

## Audit de conformité du 23 octobre 2026

Le détail des écarts et des corrections figure dans `corrections-audit-premiere-20261023.md` et `revision-audit-premiere-20261023.json`. La version précédente est archivée dans `output/archives/optitab-premiere-complet-avant-audit-2026-10-23.pdf`.

## Révision du 21 octobre 2026 sur l’audit fourni

Les neuf anomalies signalées ont été reproduites dans le PDF de 317 pages :
neuf blocs échouaient à l’analyse syntaxique, à cause de douze signes moins
mathématiques U+2212. Les sources Python utilisaient déjà le signe ASCII U+002D.
La correction du style supprime cette conversion lors du rendu.

Les passages concernés sont l’énoncé 12.1, les corrigés 5.12, 11.12, 11.13,
12.3, 12.11 et 12.12, et les défis D05 et D12.
Les résultats et explications de ces passages ont été revérifiés. Le corrigé
12.11 précise les conditions sur les deux listes : non vides, de même longueur,
une probabilité par valeur, probabilités positives ou nulles de somme 1.

## Reproduire les contrôles

Depuis le dossier des sources, avec LuaLaTeX et les dépendances Python SymPy, PyMuPDF et Pillow :

```powershell
python verifier_livre.py
python auditer_exercices.py
python auditer_programme.py
python verifier_figures.py
python verifier_relecture.py
python verifier_edition_france.py
python compiler.py
python controler_pdf.py
python verifier_code_pdf.py
```

Empreinte SHA-256 du PDF livré : `{digest}`.
'''
(OUT/'verification/verification-premiere-complet.md').write_text(report,encoding='utf-8')
for source,name in [('build/audit-exercices.json','audit-exercices-premiere.json'),('build/couverture-programme.json','couverture-programme-premiere.json'),('build/verification-figures.json','verification-figures-premiere.json'),('build/verification-relecture.json','verification-relecture-premiere.json'),('revision-editoriale.json','matrice-relecture-premiere.json'),('build/verification-edition-france.json','verification-edition-france.json'),('edition-france-manifeste.json','edition-france-manifeste.json'),('build/qa/controle-pdf.json','controle-pdf-premiere.json'),('build/verification-code-pdf.json','verification-code-pdf-premiere.json'),('revision-audit-20261021.json','revision-audit-premiere-20261021.json'),('build/audit-20261021/relecture-visuelle.json','relecture-visuelle-premiere-20261021.json'),('revision-audit-20261023.json','revision-audit-premiere-20261023.json'),('build/audit-20261023/relecture-visuelle.json','relecture-visuelle-premiere-20261023.json')]:
    shutil.copy2(ROOT/source,OUT/'verification'/name)
archive=OUT/'sources/optitab-premiere-complet-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and 'build' not in p.relative_to(ROOT).parts and p.suffix in ('.tex','.sty','.png','.md','.py','.json'):
            z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
assert not BUREAU.parent.exists() or hashlib.sha256(BUREAU.read_bytes()).hexdigest()==digest
print(json.dumps({'pages':qa['pages'],'chapitres':14,'exercices':224,'sujets_blancs':2,'preuves':proofs,'figures':figures,'pdf':str(target),'bureau':str(BUREAU),'archive':str(ARCHIVE),'sources':str(archive),'rapport':str(OUT/'verification/verification-premiere-complet.md')},ensure_ascii=False,indent=2))
