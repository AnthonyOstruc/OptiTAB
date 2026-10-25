"""Contrôles de cohérence du livre de physique-chimie (Terminale).

- plan.tex et chiffres clés de la charte (chapitres, exercices, défis) ;
- pour chaque chapitre rédigé : nombre d'exercices, rubriques, correspondance des titres
  entre énoncés et corrigés, présence du défi, de ses indices et de son corrigé ;
- existence de toutes les figures appelées par \\schema ;
- exécution des scripts de vérification numérique verifications/chapitre_NN.py et sujets_bac.py.

Lancer : python -I -X utf8 verifier_livre.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ERREURS = []


def erreur(message):
    ERREURS.append(message)
    print('ÉCHEC', message)


def lire(chemin):
    return (ROOT / chemin).read_text(encoding='utf-8')


# Plan et chiffres clés
plan = re.findall(r'\\otPlanChap\{(\d+)\}\{([^}]*)\}\{(\d+)\}', lire('plan.tex'))
charte = lire('optitab-livre.sty')
cle = {nom: int(val) for nom, val in re.findall(r'\\newcommand\{\\otNb(\w+)\}\{(\d+)\}', charte)}
if len(plan) != cle['Chapitres']:
    erreur(f"plan : {len(plan)} chapitres, charte : {cle['Chapitres']}")
if sum(int(n) for _, _, n in plan) != cle['ExosChapitres']:
    erreur("somme des exercices du plan différente de \\otNbExosChapitres")
if cle['ExosChapitres'] + cle['Defis'] != cle['ExosTotal']:
    erreur("\\otNbExosTotal doit valoir exercices de chapitre + défis")
print(f"ok  plan : {len(plan)} chapitres, {cle['ExosChapitres']} exercices, {cle['Defis']} défis")

main = lire('main.tex')
defis_enonces = lire('annexes/defis-enonces.tex')
defis_indices = lire('annexes/indices-defis.tex')
defis_corriges = lire('annexes/defis-corriges.tex')
redige = 0
for num, titre, nb in plan:
    n = int(num)
    fichiers = sorted((ROOT / 'chapitres').glob(f'{n:02d}-*.tex'))
    if not fichiers:
        continue
    redige += 1
    chap = fichiers[0]
    cor = ROOT / 'corriges' / chap.name
    texte = chap.read_text(encoding='utf-8')
    if f'\\input{{chapitres/{chap.stem}}}' not in main:
        erreur(f'{chap.name} absent de main.tex')
    if f'\\input{{corriges/{chap.stem}}}' not in main:
        erreur(f'corrigé de {chap.name} absent de main.tex')
    ouverture = re.search(r'\\begin\{ouverture\}(?:\[[^\]]*\])?\{(\d+)\}\{([^}]*)\}', texte)
    if not ouverture or int(ouverture.group(1)) != n or ouverture.group(2) != titre:
        erreur(f'{chap.name} : ouverture différente du plan')
    exos = re.findall(r'\\begin\{exercice\}\[(\d)\]\{([^}]*)\}', texte)
    if len(exos) != int(nb):
        erreur(f'{chap.name} : {len(exos)} exercices au lieu de {nb}')
    rubriques = re.findall(r'\\rubrique\{([^}]*)\}', texte)
    if rubriques != ['Découverte', 'Entraînement', 'Objectif bac']:
        erreur(f'{chap.name} : rubriques {rubriques}')
    niveaux = [int(d) for d, _ in exos]
    if niveaux != sorted(niveaux):
        erreur(f'{chap.name} : difficultés non progressives {niveaux}')
    if not cor.exists():
        erreur(f'corrigé manquant : {cor.name}')
        continue
    corriges = re.findall(r'\\begin\{corrige\}\{(\d+)\}\{([^}]*)\}', cor.read_text(encoding='utf-8'))
    if [int(k) for k, _ in corriges] != list(range(1, len(exos) + 1)):
        erreur(f'{cor.name} : numérotation des corrigés {[k for k, _ in corriges]}')
    for (d, t_ex), (k, t_cor) in zip(exos, corriges):
        if t_ex != t_cor:
            erreur(f'chapitre {n}, exercice {k} : titres différents « {t_ex} » / « {t_cor} »')
    for etiquette, source in ((f'defi-ex-{n}', defis_enonces), (f'defi-cor-{n}-1', defis_corriges)):
        if f'{{{etiquette}}}' not in source:
            erreur(f'chapitre {n} : étiquette {etiquette} introuvable')
    if f'D{n:02d} ·' not in defis_indices:
        erreur(f'chapitre {n} : indices du défi D{n:02d} introuvables')
    print(f'ok  chapitre {n:02d} « {titre} » : {len(exos)} exercices, difficultés {niveaux}, corrigés et défi présents')

# Figures appelées
for source in list((ROOT / 'chapitres').glob('*.tex')) + list((ROOT / 'corriges').glob('*.tex')) \
        + list((ROOT / 'annexes').glob('*.tex')) + list((ROOT / 'bac').glob('*.tex')):
    for nom in re.findall(r'\\schema(?:\[[^\]]*\])?\{([^}]*)\}', source.read_text(encoding='utf-8')):
        if not (ROOT / 'figures' / f'{nom}.tex').exists():
            erreur(f'{source.name} : figure manquante {nom}')
print('ok  figures appelées présentes')

# Vérifications numériques des chapitres rédigés
for script in sorted((ROOT / 'verifications').glob('chapitre_*.py')) + [ROOT / 'verifications' / 'sujets_bac.py']:
    run = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(script)], capture_output=True, text=True,
                         encoding='utf-8')
    if run.returncode != 0:
        erreur(f'{script.name} :\n{run.stdout[-1500:]}{run.stderr[-1500:]}')
    else:
        print(f'ok  {script.name} : {run.stdout.strip().splitlines()[-1]}')

print(f'\n{redige} chapitre(s) rédigé(s) sur {len(plan)}.')
if ERREURS:
    raise SystemExit(f'{len(ERREURS)} problème(s) à corriger.')
print('Toutes les vérifications sont satisfaites.')
