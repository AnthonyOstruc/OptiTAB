"""Livraison de l'édition 2027-2028 (nouveau programme) après vérifications et relecture du même PDF.

Écrit uniquement des fichiers nouveaux, suffixés « 2027 ». Les fichiers de
l'édition 2026-2027 de Quatrième ne sont jamais réécrits : leurs empreintes
sont contrôlées avant et après la copie.
"""
from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output'
SUFFIXE='quatrieme-2027'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
qa=read('build/qa/controle-pdf.json');vu=read('build/qa/relecture-visuelle.json')
cal=read('build/controles-calculs.json');fig=read('build/controles-figures.json')
man=read('manifeste-quatrieme-2027.json');pop=read('build/qa/poppler/rendus.json')
repro=read('build/controle-reproduction.json')
digest=sha(ROOT/'main.pdf')
assert qa['sha256']==vu['sha256']==pop['sha256']==digest
assert not vu['defauts_restants'] and vu['planches_lues']==(qa['pages']+11)//12
assert not qa['pages_blanches'] and not qa['texte_hors_page']
assert cal['controles_exercices_defis_sujets']==320 and cal['tests_scripts']==24 and not cal['erreurs']
assert fig['controles_figures']>=561 and not fig['erreurs']
assert qa['exercices']==qa['corriges']==270 and man['exercices_total']==288
assert qa['figures_avec_texte']==man['insertions_visuelles']
assert repro['fichiers_reproduits_identiques']>=250 and not repro['differences']
# Fichiers de l'édition 2026-2027 à préserver.
anciens=[OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Quatrième (4e) - Manuel complet.pdf',
         OUT/'sources/optitab-quatrieme-sources.zip',OUT/'verification/verification-quatrieme.md']
bureau=Path.home()/'Desktop'/'Livres OptiTAB - Lycée'
anciens.append(bureau/'OptiTAB - Mathématiques - Quatrième.pdf')
avant={str(p):sha(p) for p in anciens if p.exists()}
for sub in ['pdf','sources','verification']:(OUT/sub).mkdir(exist_ok=True)
# Bibliothèque classée par pays et par matière (output/pdf/README.md).
pdf=OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Quatrième (4e) - Programme 2027 - Manuel complet.pdf'
assert pdf.name not in [p.name for p in anciens]
shutil.copy2(ROOT/'main.pdf',pdf)
matrice=(ROOT/'build/matrice-programme.md').read_text(encoding='utf8')
rapport=f"""# Livre OptiTAB de Quatrième — édition 2027-2028, nouveau programme

Édition France 2027-2028, achevée le 23 octobre 2026. Programme : arrêté du
18 février 2026, BO n° 10 du 5 mars 2026 (MENE2602912A), annexe 2 ;
application en Quatrième à la rentrée 2027-2028.

## Contenu

- {qa['pages']} pages ; 18 chapitres avec objectifs, prérequis et deux pages de cours.
- 270 exercices progressifs : 90 de découverte, 90 d'entraînement et 90 problèmes.
- 18 défis facultatifs avec deux indications séparées et solutions expliquées.
- Deux bilans annuels : 24 automatismes et huit problèmes corrigés.
- {man['visuels_uniques']} visuels vectoriels ; {man['insertions_visuelles']} insertions dans les cours, énoncés et corrigés.
- Page « Ce qui change », quatre démonstrations, quatre fiches outils, repérage des exercices
  et matrice des objectifs officiels de Quatrième.

## Vérifications

- {cal['controles_exercices_defis_sujets']} contrôles de calcul (SymPy) couvrant chaque exercice, défi et question des bilans.
- {cal['tests_scripts']} tests de scripts, dont la règle « une seule variable par script » du programme de Quatrième.
- {fig['controles_figures']} contrôles géométriques : milieux, parallélismes, angles droits, cercles, translations.
- {qa['figures_avec_texte']} insertions sur la page de leur texte ; {qa['blocs_lecture']} blocs et {qa['pages_annexes']} pages d'annexes contrôlés en hauteur.
- {qa['liens']} liens et {qa['signets']} signets ; pagination et renvois stabilisés.
- Aucun débordement LaTeX, caractère manquant, référence non résolue, texte hors page ou page blanche accidentelle.
- Rendu de toutes les pages ; relecture des {(qa['pages']+11)//12} planches et des pages critiques ; second moteur Poppler ({len(pop['pages'])} pages).
- Sources autonomes : {repro['fichiers_reproduits_identiques']} fichiers régénérés à l'identique dans un dossier isolé.

Les contrôles informatiques soutiennent la relecture et ne prouvent pas
formellement chaque phrase. SHA-256 du PDF : {digest}

{matrice}
"""
(OUT/f'verification/verification-{SUFFIXE}.md').write_text(rapport,encoding='utf8')
(OUT/f'verification/matrice-programme-{SUFFIXE}.md').write_text(matrice,encoding='utf8')
for name in ['controle-pdf','relecture-visuelle']:
    shutil.copy2(ROOT/f'build/qa/{name}.json',OUT/f'verification/{name}-{SUFFIXE}.json')
for name in ['controles-calculs','controles-figures']:
    shutil.copy2(ROOT/f'build/{name}.json',OUT/f'verification/{name}-{SUFFIXE}.json')
shutil.copy2(ROOT/'manifeste-quatrieme-2027.json',OUT/f'verification/manifeste-{SUFFIXE}.json')
shutil.copy2(ROOT/'build/controle-reproduction.json',OUT/f'verification/reproduction-{SUFFIXE}.json')
shutil.copy2(ROOT/'build/controle-copie-initiale.json',OUT/f'verification/copie-initiale-{SUFFIXE}.json')
archive=OUT/f'sources/optitab-{SUFFIXE}-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if p.is_file() and 'build' not in rel.parts and '__pycache__' not in rel.parts and p.suffix in ['.tex','.sty','.png','.py','.md','.json']:
            z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
target=bureau/'OptiTAB - Mathématiques - Quatrième (programme 2027).pdf'
assert target.name!='OptiTAB - Mathématiques - Quatrième.pdf'
shutil.copy2(pdf,target)
assert sha(target)==sha(pdf)==digest
for p,h in avant.items():assert sha(Path(p))==h,('fichier 2026-2027 modifié',p)
print(json.dumps({'pages':qa['pages'],'pdf':str(pdf),'bureau':str(target),'sources':str(archive),'sha256':digest,'fichiers_2026_inchanges':len(avant)},ensure_ascii=True,indent=2))
