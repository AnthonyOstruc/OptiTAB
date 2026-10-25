"""Livraison de l’édition 2028-2029, conditionnée aux contrôles du PDF et à sa relecture visuelle.

Tous les fichiers produits portent des noms propres à cette édition : aucun fichier
de l’édition 2026-2027 (brevet 2027) ni d’un autre livre n’est remplacé.
"""
from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
qa=read('build/qa/controle-pdf.json')
visuel=read('build/qa/relecture-visuelle.json')
maths=read('build/controles-calculs.json')
figs=read('build/controles-figures.json')
repro=read('build/controle-reproduction.json')
man=read('manifeste-troisieme-2028.json')
digest=sha(ROOT/'main.pdf')
assert qa['sha256']==visuel['sha256']==digest
assert not visuel['defauts_restants'] and visuel['planches_lues']==qa['planches'] and visuel['pages']==qa['pages']
assert not qa['pages_blanches'] and not qa['texte_hors_page'] and not qa['mentions_obsoletes']
assert maths['controles_exercices_defis_sujets']==320 and not maths['erreurs']
assert maths['tests_scripts']==22 and figs['controles']>=437
assert qa['exercices']==qa['corriges']==270 and man['exercices_total']==288
assert qa['figures_avec_texte']==man['insertions_visuelles']
assert repro['sources_identiques'] and repro['rendus_identiques']
for sub in ['pdf','sources','verification']:(OUT/sub).mkdir(exist_ok=True)
# Fichiers de l’édition précédente : ils doivent rester intacts.
anciens=[OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Troisième (3e) - Brevet 2027 - Manuel complet.pdf',OUT/'sources/optitab-troisieme-brevet-sources.zip',
         OUT/'verification/controle-pdf-troisieme.json',OUT/'verification/manifeste-troisieme.json']
avant={str(p):sha(p) for p in anciens if p.exists()}
folder=Path.home()/'Desktop'/'Livres OptiTAB - Lycée'
assert folder.is_dir()
desktop=folder/'OptiTAB - Mathématiques - Troisième (programme 2028).pdf'
bureau_avant={p.name:sha(p) for p in folder.iterdir() if p.is_file() and p.name!=desktop.name}
pdf=OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Troisième (3e) - Programme 2028 - Brevet 2029 - Manuel complet.pdf'
pdf.parent.mkdir(parents=True,exist_ok=True)
assert str(pdf) not in avant
shutil.copy2(ROOT/'main.pdf',pdf)
report=f'''# Livre OptiTAB de Troisième — édition 2028-2029, nouveau programme, brevet 2029

Édition du 23 octobre 2026. France, année scolaire 2028-2029, DNB série générale.
Nouvelle édition construite à partir de l’édition 2026-2027 (brevet 2027), qui reste
valable et n’a pas été modifiée.

## Livre livré

- {qa['pages']} pages, 18 chapitres et deux pages de cours par chapitre.
- 270 exercices progressifs (5 de découverte, 5 d’entraînement, 5 problèmes par chapitre).
- 18 défis facultatifs, deux indications par défi et solutions rédigées.
- Deux brevets blancs originaux : 24 automatismes et 8 problèmes corrigés.
- {man['visuels_uniques']} visuels vectoriels, {man['insertions_visuelles']} insertions dans les énoncés et corrigés.
- Une page « Nouveau programme : ce qui change », une correspondance rubrique par rubrique
  avec le programme de Troisième et une matrice de 72 repères reliés aux exercices.

## Références officielles

- Arrêté du 18-2-2026 (JO du 4-3-2026, NOR MENE2602912A), BO n° 10 du 5 mars 2026 :
  programme de mathématiques du cycle 4 (annexe 2), applicable en Troisième à la rentrée 2028-2029.
- Éduscol : « Mathématiques. Exemples pour la mise en œuvre des programmes 2026. Cycle 4 ».
- Note de service du 11-9-2026 (NOR MENE2623228N), BO spécial n° 4 du 17 septembre 2026 :
  définition des épreuves du DNB à compter de la session 2027.
- Note de service du 11-9-2026 (NOR MENE2623195N), même BO : maîtrise de la langue aux examens.

Au 23 octobre 2026, aucun texte propre à la session 2029 n’était publié. Les brevets
blancs suivent la définition en vigueur à compter de la session 2027 : 20 minutes sans
calculatrice et 6 points d’automatismes à réponses courtes, puis 1 h 40 avec calculatrice
et 14 points de raisonnement et de résolution de problèmes, sans QCM, dont 2 points de
maîtrise de la langue. Ce point est signalé dans le livre (copyright, guide des brevets,
sources) et devra être revérifié avant la session 2029.

## Contrôles effectués

- Reproduction : la copie de l’édition 2026-2027 a été reconstruite à l’identique avant toute modification.
- {maths['controles_exercices_defis_sujets']} contrôles exacts (SymPy, énumération, coordonnées) couvrant chaque exercice, défi et question des sujets.
- {maths['tests_scripts']} tests de trace des scripts par blocs, dont conditions composées, boucles conditionnelles, blocs personnalisés et simulations.
- {figs['controles']} contrôles de figures : angles droits, configurations de Thalès, égalités de vecteurs, parallélogrammes, quartiles des boîtes, dénombrements.
- {qa['blocs_lecture']} blocs de lecture et {qa['pages_annexes']} pages d’annexes contrôlés en hauteur.
- Les {qa['figures_avec_texte']} représentations sont sur la même page que leur texte associé.
- {qa['liens']} liens et {qa['signets']} signets ; renvois et pagination stabilisés.
- Aucun débordement, caractère manquant, référence non résolue ni mention obsolète de l’édition précédente.
- Rendu des {qa['pages']} pages en {qa['planches']} planches, toutes relues ; pages critiques relues en détail.
- Rendu complémentaire de {len(visuel['pages_poppler_relues'])} pages critiques avec Poppler.
- Les {len(qa['pages_notes'])} pages de notes lignées sont intentionnelles.
- Reconstruction isolée des sources : {"identique" if repro['sources_identiques'] else "différente"}.

Défauts relevés à la relecture et corrigés : {len(visuel['defauts_corriges'])}.

Les contrôles informatiques soutiennent la relecture ; ils ne sont pas une preuve
formelle de tout le texte.

## Remarque sur l’édition 2026-2027 (non modifiée)

Dans les sources de l’édition 2026-2027 (livre-troisieme, chapitre 6), quinze signes %
ne sont pas échappés : dans le PDF livré, la fin de plusieurs phrases disparaît
(par exemple « Son prix baisse de 25 » sans la suite). Ce défaut est corrigé dans
l’édition 2028-2029 ; l’édition 2026-2027 n’a pas été touchée, conformément à la consigne.

Empreinte SHA-256 du PDF : {digest}

## Reproduire

Voir le README dans l’archive des sources. Exécuter successivement
verifier_contenu.py, verifier_figures.py, construire.py, compiler.py,
controler_pdf.py et rendre_poppler.py, puis relire les rendus.
'''
(OUT/'verification/verification-troisieme-2028.md').write_text(report,encoding='utf8')
for source,nom in [('build/qa/controle-pdf.json','controle-pdf-troisieme-2028.json'),
 ('build/qa/relecture-visuelle.json','relecture-visuelle-troisieme-2028.json'),
 ('build/controles-calculs.json','controles-calculs-troisieme-2028.json'),
 ('build/controles-figures.json','controles-figures-troisieme-2028.json'),
 ('build/controle-reproduction.json','controle-reproduction-troisieme-2028.json'),
 ('build/controle-reproduction-initiale.json','reproduction-initiale-troisieme-2028.json'),
 ('build/qa/poppler/rendus.json','rendus-poppler-troisieme-2028.json'),
 ('manifeste-troisieme-2028.json','manifeste-troisieme-2028.json'),
 ('MATRICE-PROGRAMME-2028.md','matrice-programme-troisieme-2028.md')]:
    cible=OUT/'verification'/nom
    assert str(cible) not in avant
    shutil.copy2(ROOT/source,cible)
archive=OUT/'sources/optitab-troisieme-2028-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if p.is_file() and rel.parts[0] not in ('build','__pycache__') and p.suffix in ['.tex','.sty','.png','.py','.md','.json']:
            z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
shutil.copy2(pdf,desktop)
assert sha(desktop)==sha(pdf)==digest
for p,h in avant.items():assert sha(Path(p))==h,p
for nom,h in bureau_avant.items():assert sha(folder/nom)==h,nom
print(json.dumps(dict(pages=qa['pages'],pdf=str(pdf),bureau=str(desktop),sources=str(archive),sha256=digest),ensure_ascii=True,indent=2))
