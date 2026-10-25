"""Livraison des fichiers qui ont effectivement été contrôlés et relus."""
from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parent;OUT=ROOT.parent/'output'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
qa=read('build/qa/controle-pdf.json');vu=read('build/qa/relecture-visuelle.json')
cal=read('build/controles-calculs.json');fig=read('build/controles-figures.json')
pop=read('build/qa/poppler/rendus.json');man=read('manifeste-cinquieme.json')
repro=read('build/controle-reproduction.json');digest=sha(ROOT/'main.pdf')
assert qa['sha256']==vu['sha256']==pop['sha256']==digest
assert not vu['defauts_restants'] and vu['planches_lues']==(qa['pages']+11)//12
assert not qa['pages_blanches'] and not qa['texte_hors_page']
assert cal['controles_exercices_defis_sujets']==352 and cal['tests_scripts']==20 and not cal['erreurs']
assert fig['controles_figures']>=541 and not fig['erreurs']
assert qa['exercices']==qa['corriges']==300 and man['exercices_total']==320
assert qa['figures_avec_texte']==man['insertions_visuelles']
assert repro['fichiers_reproduits_identiques']>=200 and not repro['differences']
for sub in ['pdf','sources','verification']:(OUT/sub).mkdir(exist_ok=True)
pdf=OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Cinquième (5e) - Manuel complet.pdf'
pdf.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'main.pdf',pdf)
report=f"""# Livre OptiTAB de Cinquième

Édition France 2026-2027, achevée le 22 octobre 2026 et revue le
23 octobre 2026 après un audit de conformité au programme officiel
(BO n° 10 du 5 mars 2026) et aux exemples de mise en œuvre Éduscol.
La matrice de l'audit est jointe : audit-programme-cinquieme.json.

- {qa['pages']} pages ; 20 chapitres et 44 pages de cours.
- 300 exercices : 100 de découverte, 100 d'entraînement, 100 problèmes.
- 20 défis facultatifs avec deux indications et solutions expliquées.
- Deux bilans originaux : 24 automatismes et huit problèmes corrigés.
- {man['visuels_uniques']} visuels vectoriels ; {man['insertions_visuelles']} insertions.
- Figures pour les 75 exercices des chapitres 13 à 17, les 15 exercices de repérage et les 15 exercices de programmation.
- Couvertures, titre, sommaire cliquable, parcours et tableau de bord.
- Quatre démonstrations, quatre fiches outils et matrice de 80 repères.

Le nouveau programme de mathématiques publié au BO du 5 mars 2026 est
appliqué en Cinquième depuis la rentrée 2026-2027. Ses rubriques de
Cinquième ont été lues : automatismes, objectifs et limites des notions.
Les sources officielles sont liées dans le livre.

Les fractions restent dans le cadre des sommes et différences ; les
puissances portent sur carrés et cubes ; les équations simples sont
résolues par opérations inverses. La programmation utilise une donnée
saisie en lecture et des répétitions inconditionnelles simples.
Les prolongements sur les nombres premiers sont facultatifs.

## Contrôles effectués

- {cal['controles_exercices_defis_sujets']} contrôles de calcul couvrant tous les exercices, défis et questions des bilans.
- {cal['tests_scripts']} tests d'exécution : entrées, expressions, déplacements et fermeture des figures.
- {fig['controles_figures']} contrôles de présence et de cohérence géométrique.
- 300 énoncés associés aux 300 corrigés ; {qa['blocs_lecture']} blocs contrôlés.
- {qa['figures_avec_texte']} figures présentes sur la page de leur texte.
- {qa['liens']} liens et {qa['signets']} signets vérifiés ; renvois stabilisés.
- Aucun débordement LaTeX, caractère manquant, renvoi non résolu, texte hors page ou page blanche accidentelle.
- Rendu de toutes les pages et relecture des {(qa['pages']+11)//12} planches.
- Inspection détaillée des pages critiques avec un second moteur, Poppler.
- {len(qa['pages_notes'])} pages de notes lignées intentionnelles.
- {repro['fichiers_reproduits_identiques']} fichiers LaTeX, styles et images reproduits à l'identique dans un dossier isolé.

Les contrôles informatiques soutiennent la relecture mathématique et
éditoriale. Ils ne constituent pas une preuve formelle de chaque phrase.

SHA-256 : {digest}
"""
(OUT/'verification/verification-cinquieme.md').write_text(report,encoding='utf8')
for name in ['controle-pdf','relecture-visuelle']:shutil.copy2(ROOT/f'build/qa/{name}.json',OUT/f'verification/{name}-cinquieme.json')
for name in ['controles-calculs','controles-figures']:shutil.copy2(ROOT/f'build/{name}.json',OUT/f'verification/{name}-cinquieme.json')
shutil.copy2(ROOT/'build/controle-reproduction.json',OUT/'verification/reproduction-cinquieme.json')
shutil.copy2(ROOT/'manifeste-cinquieme.json',OUT/'verification/manifeste-cinquieme.json')
audit=read('build/qa/audit-programme-2026-10-23.json')
assert audit['sha256_pdf']==digest and not audit['ecarts_restants']
shutil.copy2(ROOT/'build/qa/audit-programme-2026-10-23.json',OUT/'verification/audit-programme-cinquieme.json')
shutil.copy2(ROOT/'build/qa/poppler/rendus.json',OUT/'verification/rendus-poppler-cinquieme.json')
archive=OUT/'sources/optitab-cinquieme-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if p.is_file() and 'build' not in rel.parts and p.suffix in ['.tex','.sty','.png','.py','.md','.json']:z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
folder=Path.home()/'Desktop'/'Livres OptiTAB - Lycée'
previous={p.name:sha(p) for p in folder.glob('*.pdf') if 'Cinquième' not in p.name}
assert len(previous)>=5
# Les autres livres peuvent être relivrés en parallèle : on vérifie seulement
# qu'ils restent intacts pendant cette copie, sans figer leur empreinte.
target=folder/'OptiTAB - Mathématiques - Cinquième.pdf';shutil.copy2(pdf,target)
assert sha(pdf)==sha(target)==digest
assert all(sha(folder/name)==h for name,h in previous.items())
print(json.dumps(dict(pages=qa['pages'],pdf=str(pdf),bureau=str(target),sources=str(archive),sha256=digest),ensure_ascii=True,indent=2))
