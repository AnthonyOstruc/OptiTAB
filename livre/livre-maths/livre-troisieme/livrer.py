"""Livraison conditionnée aux contrôles du PDF et à sa relecture visuelle."""
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
man=read('manifeste-troisieme.json')
digest=sha(ROOT/'main.pdf')
assert qa['sha256']==visuel['sha256']==digest
assert not visuel['defauts_restants'] and visuel['planches_lues']==(qa['pages']+11)//12
assert not qa['pages_blanches'] and not qa['texte_hors_page']
assert maths['controles_exercices_defis_sujets']==320 and not maths['erreurs']
assert maths['tests_scripts']==14 and figs['controles']>=415
assert qa['exercices']==qa['corriges']==270 and man['exercices_total']==288
assert qa['figures_avec_texte']==man['insertions_visuelles']==259
for sub in ['pdf','sources','verification']:(OUT/sub).mkdir(exist_ok=True)
pdf=OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Troisième (3e) - Brevet 2027 - Manuel complet.pdf'
pdf.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/'main.pdf',pdf)
report=f'''# Livre OptiTAB de Troisième — Brevet 2027

Édition du 21 octobre 2026. France, année scolaire 2026-2027, DNB série générale.
Vérifications finales achevées le 22 octobre 2026.

## Livre livré

- {qa['pages']} pages, 18 chapitres et deux pages de cours par chapitre.
- 270 exercices progressifs (5 de découverte, 5 d'entraînement, 5 problèmes par chapitre).
- 18 défis facultatifs, deux indications par défi et solutions rédigées.
- Deux brevets blancs originaux : 24 automatismes et 8 problèmes corrigés.
- {man['visuels_uniques']} visuels vectoriels utilisés, {man['insertions_visuelles']} insertions dans les cours, énoncés et corrigés.
- Figures pour chacun des 75 exercices des cinq chapitres de géométrie et représentations pour les 15 exercices d'algorithmique.
- Couvertures, page de titre, avant-propos, mode d'emploi, parcours, sommaire cliquable et tableau de bord.
- Démonstrations expliquées, quatre fiches outils et matrice de 72 repères reliés aux exercices.

## Références

Le livre suit les attendus annuels de Troisième applicables en 2026-2027,
en réactivant les connaissances utiles du cycle 4.
Le nouveau programme publié en 2026 ne s'appliquera en Troisième qu'en 2028-2029.
Les sources officielles et leurs liens sont incluses à la fin du livre.

Le format retenu pour la session 2027 suit la note de septembre 2026 :
20 minutes sans calculatrice, 6 points d'automatismes et applications directes ;
puis 1 h 40 avec calculatrice autorisée, 14 points de raisonnement et problèmes,
sans QCM dans la seconde partie. Les 2 points de qualité de l'expression sont
inclus dans la note. Le barème détaillé des sujets du livre est un choix pédagogique.

## Contrôles effectués

- {maths['controles_exercices_defis_sujets']} contrôles exacts, symboliques, numériques ou par énumération, couvrant chaque exercice, défi et question des sujets.
- {maths['tests_scripts']} tests de trace des scripts par blocs, avec tests de frontière, boucle et retour du dessin au point de départ.
- {figs['controles']} contrôles de présence et de cohérence des figures, dont angles droits, configurations de Thalès, probabilités des branches et sections sphériques.
- Concordance de 270 énoncés et 270 corrigés ; difficulté répartie en trois séries.
- {qa['blocs_lecture']} blocs de lecture et {qa['pages_annexes']} pages d'annexes contrôlés en hauteur.
- Les {qa['figures_avec_texte']} représentations sont sur la même page que leur texte associé.
- {qa['liens']} liens et {qa['signets']} signets ; renvois et pagination stabilisés.
- Aucun avertissement de débordement, caractère manquant ou référence non résolue.
- Rendu des {qa['pages']} pages, lecture de toutes les planches et vérification détaillée des pages critiques.
- Comparaison raster : {visuel['pages_identiques']} pages identiques au premier rendu relu et {len(visuel['pages_modifiees_relues'])} pages modifiées relues.
- Contrôle complémentaire de {len(visuel['pages_poppler_relues'])} pages critiques avec Poppler.
- Aucun texte hors page ni page blanche accidentelle. Les {len(qa['pages_notes'])} pages de notes lignées sont intentionnelles.

La relecture a notamment corrigé les proportions de triangles, une configuration
non parallèle, les figures d'homothéties, le repérage sphérique et l'affichage
des références absolues du tableur, les en-têtes de tableaux, une cote donnant
prématurément une réponse, et le placement des étiquettes. Les contrôles informatiques soutiennent la
relecture ; ils ne sont pas une preuve formelle de tout le texte.

Empreinte SHA-256 du PDF : {digest}

## Reproduire

Voir le README dans l'archive des sources. Exécuter successivement
verifier_contenu.py, verifier_figures.py, construire.py, compiler.py et
controler_pdf.py, puis relire les rendus.
'''
(OUT/'verification/verification-troisieme-brevet.md').write_text(report,encoding='utf8')
for source,nom in [('build/qa/controle-pdf.json','controle-pdf-troisieme.json'),
 ('build/qa/relecture-visuelle.json','relecture-visuelle-troisieme.json'),
 ('build/controles-calculs.json','controles-calculs-troisieme.json'),
 ('build/controles-figures.json','controles-figures-troisieme.json'),
 ('manifeste-troisieme.json','manifeste-troisieme.json')]:
    shutil.copy2(ROOT/source,OUT/'verification'/nom)
archive=OUT/'sources/optitab-troisieme-brevet-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and 'build' not in p.relative_to(ROOT).parts and p.suffix in ['.tex','.sty','.png','.py','.md','.json']:
            z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
folder=Path.home()/'Desktop'/'Livres OptiTAB - Lycée'
assert folder.is_dir()
existants={
 'OptiTAB - Mathématiques - Seconde.pdf':'ef9c502598f54fdc95c79bd00cf82f91597780428d3dcaffe60f2501fdb27116',
 'OptiTAB - Mathématiques - Première spécialité.pdf':'3040f3a2de2b82050655c6f9cb9de6a0b1814e9385259d93b3aacbec1c088448',
 'OptiTAB - Mathématiques - Terminale spécialité.pdf':'74b39fbee78807b905f4ef6b1e0fb3b255dfd6091832f783227a07845fa17ca7'
}
for nom,empreinte in existants.items():assert sha(folder/nom)==empreinte,nom
desktop=folder/'OptiTAB - Mathématiques - Troisième - Brevet 2027.pdf'
shutil.copy2(pdf,desktop)
assert sha(desktop)==sha(pdf)==digest
for nom,empreinte in existants.items():assert sha(folder/nom)==empreinte
print(json.dumps(dict(pages=qa['pages'],pdf=str(pdf),bureau=str(desktop),sources=str(archive),sha256=digest),ensure_ascii=True,indent=2))
