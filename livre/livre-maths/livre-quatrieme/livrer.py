"""Copie finale après vérifications et relecture du même PDF."""
from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
qa=read('build/qa/controle-pdf.json');vu=read('build/qa/relecture-visuelle.json')
cal=read('build/controles-calculs.json');fig=read('build/controles-figures.json')
man=read('manifeste-quatrieme.json');pop=read('build/qa/poppler/rendus.json')
repro=read('build/controle-reproduction.json')
digest=sha(ROOT/'main.pdf')
assert qa['sha256']==vu['sha256']==pop['sha256']==digest
assert not vu['defauts_restants'] and vu['planches_lues']==(qa['pages']+11)//12
assert not qa['pages_blanches'] and not qa['texte_hors_page']
assert cal['controles_exercices_defis_sujets']==320 and cal['tests_scripts']==21 and not cal['erreurs']
assert fig['controles_figures']>=461 and not fig['erreurs']
assert qa['exercices']==qa['corriges']==270 and man['exercices_total']==288
assert qa['figures_avec_texte']==man['insertions_visuelles']
assert repro['fichiers_reproduits_identiques']>=233 and not repro['differences']
for sub in ['pdf','sources','verification']:(OUT/sub).mkdir(exist_ok=True)
pdf=OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Quatrième (4e) - Manuel complet.pdf'
pdf.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'main.pdf',pdf)
rapport=f"""# Livre OptiTAB de Quatrième

Édition France 2026-2027, achevée le 22 octobre 2026.

## Contenu

- {qa['pages']} pages ; 18 chapitres avec objectifs, prérequis et deux pages de cours.
- 270 exercices progressifs : 90 de découverte, 90 d'entraînement et 90 problèmes.
- 18 défis facultatifs avec deux indications séparées et solutions expliquées.
- Deux bilans annuels : 24 automatismes et huit problèmes corrigés.
- {man['visuels_uniques']} visuels vectoriels utilisés ; {man['insertions_visuelles']} insertions dans les cours, énoncés et corrigés.
- Schémas pour les 90 exercices de géométrie et d'espace, et blocs pour les 15 exercices de programmation.
- Couvertures, page de titre, sommaire cliquable, tableau de bord et parcours.
- Quatre démonstrations, quatre fiches outils et matrice de 72 repères.

## Périmètre

Le programme de cycle 4 de 2020, les attendus annuels de Quatrième et les repères
annuels ont été consultés. L'article 3 de l'arrêté du 18 février 2026 fait entrer
le nouveau programme en Quatrième à la rentrée 2027-2028 : cette édition suit
le programme applicable en 2026-2027. Les sources sont liées dans le livre.

Points couverts : relatifs et rationnels ; inverse ; nombres premiers jusqu'à 100 ;
puissances positives ; puissances de dix positives et négatives ; préfixes de nano
à giga ; notation scientifique ; carrés de 1 à 144 ; racines ; distributivité
simple et factorisation ; équations du premier degré ; proportionnalité et
graphiques ; grandeurs composées ; médiane et diagrammes circulaires ;
probabilités à une épreuve et contraire ; cas d'égalité des triangles ;
Pythagore et réciproque ; Thalès emboîté et réciproque ; cosinus ; translations ;
frises et pavages ; rapports de longueurs, aires et volumes ; patrons et
perspectives ; repérage dans un pavé ; pyramides et cônes ; programmation
par blocs de niveaux 1 et 2.

Les notations formelles de fonctions, Thalès en papillon, le sinus, la tangente
et les homothéties négatives ne sont pas présentés comme attendus de cette classe.
Les deux bilans sont des entraînements, sans statut d'examen officiel.

## Vérifications

- {cal['controles_exercices_defis_sujets']} contrôles de calcul couvrant chaque exercice, défi et question des bilans.
- {cal['tests_scripts']} tests de scripts : résultats, frontières, répétitions et fermeture des figures.
- {fig['controles_figures']} contrôles de présence, coordonnées, longueurs, angles droits, parallélismes, translations, secteurs et patron de cône.
- Concordance des 270 énoncés et corrections.
- {qa['figures_avec_texte']} insertions sur la page de leur texte ; {qa['blocs_lecture']} blocs et {qa['pages_annexes']} pages d'annexes contrôlés en hauteur.
- {qa['liens']} liens et {qa['signets']} signets ; pagination et renvois stabilisés.
- Aucun débordement LaTeX, caractère manquant, référence non résolue, texte hors page ou page blanche accidentelle.
- Rendu de toutes les pages ; relecture des {(qa['pages']+11)//12} planches et des pages critiques.
- Second moteur Poppler : {len(pop['pages'])} pages critiques relues.
- {len(qa['pages_notes'])} pages de notes lignées intentionnelles.
- Sources autonomes : {repro['fichiers_reproduits_identiques']} fichiers LaTeX, styles et images régénérés à l'identique dans un dossier isolé.

Les contrôles informatiques soutiennent la relecture et ne prouvent pas
formellement chaque phrase. Les solutions, unités, hypothèses et limites
du niveau ont aussi fait l'objet d'une relecture éditoriale.

SHA-256 du PDF : {digest}
"""
(OUT/'verification/verification-quatrieme.md').write_text(rapport,encoding='utf8')
for name in ['controle-pdf','relecture-visuelle']:
    shutil.copy2(ROOT/f'build/qa/{name}.json',OUT/f'verification/{name}-quatrieme.json')
for name in ['controles-calculs','controles-figures']:
    shutil.copy2(ROOT/f'build/{name}.json',OUT/f'verification/{name}-quatrieme.json')
shutil.copy2(ROOT/'manifeste-quatrieme.json',OUT/'verification/manifeste-quatrieme.json')
shutil.copy2(ROOT/'build/controle-reproduction.json',OUT/'verification/reproduction-quatrieme.json')
archive=OUT/'sources/optitab-quatrieme-sources.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if p.is_file() and 'build' not in rel.parts and p.name not in ['adapter_collection.py','corrections_editoriales.py'] and p.suffix in ['.tex','.sty','.png','.py','.md','.json']:
            z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
folder=Path.home()/'Desktop'/'Livres OptiTAB - Lycée'
prior={
'OptiTAB - Mathématiques - Seconde.pdf':'51e757967d78dfbc381cbf0e773612feebb9784f10a1bc3bc4417c8d9cc0d72d',
'OptiTAB - Mathématiques - Première spécialité.pdf':'709979da6b0219bfb068e55eb13dac906075a14dc09e57867229bc086412e0a4',
'OptiTAB - Mathématiques - Terminale spécialité.pdf':'74b39fbee78807b905f4ef6b1e0fb3b255dfd6091832f783227a07845fa17ca7',
'OptiTAB - Mathématiques - Troisième - Brevet 2027.pdf':'431d76b86b3b02ba7ec565e1462a806b084466dc871f49578a0c4d2b64970c23'}
for name,h in prior.items():assert sha(folder/name)==h,name
target=folder/'OptiTAB - Mathématiques - Quatrième.pdf'
shutil.copy2(pdf,target)
assert sha(target)==sha(pdf)==digest
for name,h in prior.items():assert sha(folder/name)==h,name
print(json.dumps({'pages':qa['pages'],'pdf':str(pdf),'bureau':str(target),'sources':str(archive),'sha256':digest},ensure_ascii=True,indent=2))
