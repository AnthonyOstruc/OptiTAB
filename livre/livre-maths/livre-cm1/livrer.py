"""Livraison des fichiers qui ont effectivement été contrôlés et relus."""
from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parent;OUT=ROOT.parent/'output'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
qa=read('build/qa/controle-pdf.json');vu=read('build/qa/relecture-visuelle.json')
cal=read('build/controles-calculs.json');fig=read('build/controles-figures.json')
pop=read('build/qa/poppler/rendus.json');man=read('manifeste-cm1.json')
repro=read('build/controle-reproduction.json');digest=sha(ROOT/'main.pdf')
assert qa['sha256']==vu['sha256']==pop['sha256']==digest
assert not vu['defauts_restants'] and vu['planches_lues']==(qa['pages']+11)//12
assert not qa['pages_blanches'] and not qa['texte_hors_page']
assert cal['controles_exercices_defis_sujets']==368 and cal['tests_scripts']==10 and not cal['erreurs']
assert fig['controles_figures']>=370 and not fig['erreurs']
assert qa['exercices']==qa['corriges']==315 and man['exercices_total']==336
assert qa['figures_avec_texte']==man['insertions_visuelles']
assert repro['fichiers_reproduits_identiques']>=180 and not repro['differences']
for sub in ['pdf','sources','verification']:(OUT/sub).mkdir(exist_ok=True)
pdf=OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - CM1 - Manuel complet.pdf'
pdf.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'main.pdf',pdf)
report=f"""# Livre OptiTAB de CM1

Édition France 2026-2027, achevée le 22 octobre 2026.

- {qa['pages']} pages ; 21 chapitres et {sum(man['cours_par_chapitre'])} pages de cours.
- 315 exercices : 105 de découverte, 105 d'entraînement, 105 problèmes.
- 21 défis facultatifs avec deux indications et solutions expliquées.
- Deux bilans originaux : 24 automatismes et huit problèmes corrigés.
- {man['visuels_uniques']} visuels vectoriels ; {man['insertions_visuelles']} insertions.
- Figures pour tous les exercices des chapitres 13 et 15 à 18 : aires et angles, géométrie, symétrie, solides et déplacements.
- Couvertures, titre, sommaire cliquable, parcours et tableau de bord.
- Quatre pages « comprendre pourquoi », quatre fiches outils et matrice de 84 repères du programme.

Le programme de mathématiques du cycle 3 publié au BO n° 16 du
17 avril 2025 est appliqué en CM1 depuis la rentrée 2025. Les rubriques
« cours moyen première année » ont été lues : objectifs d'apprentissage
et limites de chaque domaine. Les sources officielles sont liées dans le livre.

Limites respectées : entiers jusqu'à 999 999 ; fractions de dénominateur
au plus 20 et fractions décimales ; décimaux aux centièmes ; divisions
par un diviseur à un chiffre ; conversions raisonnées sans tableau ;
angles sans rapporteur ; symétrie sur quadrillage à axes horizontaux ou
verticaux ; patron du cube ; proportionnalité en langage naturel sans
produit en croix ; hasard qualitatif avec « une chance sur deux ».

## Contrôles effectués

- {cal['controles_exercices_defis_sujets']} contrôles de calcul couvrant tous les exercices, défis et questions des bilans.
- {cal['tests_scripts']} tests d'exécution des programmes de calcul et de déplacement.
- {fig['controles_figures']} contrôles de présence et de cohérence des figures.
- 315 énoncés associés aux 315 corrigés ; {qa['blocs_lecture']} blocs contrôlés.
- {qa['figures_avec_texte']} figures présentes sur la page de leur texte.
- {qa['liens']} liens et {qa['signets']} signets vérifiés ; renvois stabilisés.
- Aucun débordement LaTeX, caractère manquant, renvoi non résolu, texte hors page ou page blanche accidentelle.
- Rendu de toutes les pages et relecture des {(qa['pages']+11)//12} planches.
- Inspection de pages critiques avec un second moteur, Poppler.
- {len(qa['pages_notes'])} pages de notes lignées intentionnelles.
- {repro['fichiers_reproduits_identiques']} fichiers LaTeX, styles et images reproduits à l'identique dans un dossier isolé.

Les contrôles informatiques soutiennent la relecture mathématique et
éditoriale. Ils ne constituent pas une preuve formelle de chaque phrase.

SHA-256 : {digest}
"""
(OUT/'verification/verification-cm1.md').write_text(report,encoding='utf8')
for name in ['controle-pdf','relecture-visuelle']:shutil.copy2(ROOT/f'build/qa/{name}.json',OUT/f'verification/{name}-cm1.json')
for name in ['controles-calculs','controles-figures']:shutil.copy2(ROOT/f'build/{name}.json',OUT/f'verification/{name}-cm1.json')
shutil.copy2(ROOT/'build/controle-reproduction.json',OUT/'verification/reproduction-cm1.json')
shutil.copy2(ROOT/'manifeste-cm1.json',OUT/'verification/manifeste-cm1.json')
archive=OUT/'sources/optitab-cm1-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if p.is_file() and 'build' not in rel.parts and '__pycache__' not in rel.parts and p.suffix in ['.tex','.sty','.png','.py','.md','.json']:z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
folder=Path.home()/'Desktop'/'Livres OptiTAB - Lycée'
previous={p.name:sha(p) for p in folder.glob('*.pdf') if 'CM1' not in p.name}
assert len(previous)>=5
target=folder/'OptiTAB - Mathématiques - CM1.pdf';shutil.copy2(pdf,target)
assert sha(pdf)==sha(target)==digest
assert all(sha(folder/name)==h for name,h in previous.items())
print(json.dumps(dict(pages=qa['pages'],pdf=str(pdf),bureau=str(target),sources=str(archive),sha256=digest),ensure_ascii=True,indent=2))
