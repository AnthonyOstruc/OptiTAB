"""Construit un cahier de maternelle : python construire.py ps|ms|gs"""
from pathlib import Path
import importlib, json, re, shutil, sys
from outils import P, f

RACINE = Path(__file__).resolve().parent
SOURCES = [
    ('Programme d’enseignement de l’école maternelle',
     'Arrêté publié au BO n° 41 du 31 octobre 2024, applicable à la rentrée 2025 ; version consolidée intégrant le BO n° 19 du 7 mai 2026. Domaine « L’acquisition des premiers outils mathématiques » et partie « Se repérer dans l’espace ».',
     'https://eduscol.education.gouv.fr/sites/default/files/document/programme-cycle-1-consolide-127565.pdf'),
    ('Ressources d’accompagnement Éduscol',
     'Ressources pour le cycle 1 : construction du nombre, résolution de problèmes, formes et grandeurs, motifs organisés.',
     'https://eduscol.education.gouv.fr/'),
]

def gras(t):
    return re.sub(r'<b>(.*?)</b>', r'{\\otBold\\color{otNavy}\1}', t)

def tex_safe(t):
    return t.replace('%', r'\%')

def ecrire(chemin, texte):
    assert not any(ord(c) < 32 and c not in '\n\r\t' for c in texte), chemin
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(texte, encoding='utf8')

def decor_partie(theme):
    """Quelques illustrations dans le bandeau d’ouverture (coordonnées en mm dans un bandeau de 210 x 118)."""
    # Zone réservée au décor : x de 120 à 196 mm, y de 54 à 112 mm (le titre occupe le bas du bandeau).
    jeux = {
        'pomme': [('panier', 168, 64, 2.6, None), ('pomme', 160, 74, 1.5, 'matRouge'), ('pomme', 175, 75, 1.5, 'matVert'),
                  ('pomme', 167, 84, 1.5, 'matRouge'), ('pomme', 140, 96, 1.9, 'matRouge'), ('pomme', 188, 98, 1.4, 'matVert')],
        'de': [('de', 146, 90, 1.7, None, 3), ('de', 172, 70, 1.7, None, 2), ('main', 186, 96, 2.1, None, 3), ('de', 132, 66, 1.3, None, 1)],
        'ours': [('ours', 150, 80, 2.6, 'matBrun'), ('valise', 182, 68, 2.4, 'matOrange'), ('ours', 186, 98, 1.5, 'matJaune')],
        'formes': [], 'serpent': [('serpent', 124, 94, 1.0, 'matVert'), ('serpent', 136, 70, 1.0, 'matOrange')],
        'perle': [('perle', 120 + 11 * k, 78 + (5 if k % 2 else 0), 1.4, ['matRouge', 'matBleu'][k % 2]) for k in range(7)],
        'souris': [('souris', 146, 70, 2.2, None), ('fromage', 184, 66, 2.0, None), ('arbre', 168, 96, 2.0, None)],
        'nombre': [('de', 140, 92, 1.7, None, 5), ('main', 178, 92, 2.3, None, 4), ('de', 160, 66, 1.4, None, 6)],
        'balance': [('balance', 160, 82, 2.4, None, -1), ('pasteque', 135, 99, 1.2, None), ('plume', 186, 105, 1.3, None)],
        'train': [('locomotive', 130, 74, 1.6, 'matRouge')] + [('wagon', 146 + 14 * k, 73, 1.6, ['matBleu', 'matJaune', 'matVert'][k % 3]) for k in range(4)],
        'oie': [('pion', 140, 80, 1.8, 'matRouge'), ('pion', 158, 72, 1.8, 'matBleu'), ('de', 182, 92, 1.6, None, 4)],
        'etoile': [('etoile', 140, 92, 2.0, 'matJaune'), ('etoile', 170, 70, 1.4, 'matOrange'), ('etoile', 186, 100, 1.2, 'matJaune')],
    }
    code = ''
    if theme == 'formes':
        from outils import forme
        code += forme('disque', 15.0, 8.0, 1.2, couleur='matRouge') + forme('carre', 18.0, 9.4, 0.9, 25, 'matJaune') + forme('triangle', 17.8, 5.6, 1.1, 10, 'otGreen')
        return code
    for item in jeux.get(theme, []):
        nom, x, y, s, c = item[:5]
        n = item[5] if len(item) > 5 else None
        code += P(nom, x / 10, y / 10, s, c=c, n=n, l=(6.0 if x < 130 else 4.6) if nom == 'serpent' else None)
    return code

def construire(cle):
    mod = importlib.import_module(cle)
    niv = mod.NIVEAU
    dossier = RACINE / cle
    if (dossier / 'figures').exists():
        shutil.rmtree(dossier / 'figures')
    dossier.mkdir(exist_ok=True)
    for nom in ['maternelle.sty', 'objets.sty', 'couverture.tex', 'liminaires.tex', 'dos.tex']:
        shutil.copy2(RACINE / 'commun' / nom, dossier / nom)
    (dossier / 'images').mkdir(exist_ok=True)
    for img in (RACINE / 'images').glob('*.png'):
        shutil.copy2(img, dossier / 'images' / img.name)

    parties = []
    num = 0
    for (titre, sous, prog, fabriques, theme) in mod.PARTIES:
        acts = []
        for fab in fabriques:
            num += 1
            a = fab()
            a.num = num
            a.label = f'act-{cle}-{num}'
            a.fig = f'{cle}-{num:02d}'
            acts.append(a)
        parties.append((titre, sous, prog, acts, theme))
    toutes = [a for p in parties for a in p[3]]

    # Contrôles de conformité au programme et de cohérence des données.
    erreurs = []
    for a in toutes:
        for q in a.quantites:
            if not (1 <= q <= niv['max_quantite']):
                erreurs.append(f'{a.num} {a.titre} : quantité {q} hors du programme {niv["court"]}')
        for q in a.globales:
            if not (1 <= q <= niv['max_globale']):
                erreurs.append(f'{a.num} {a.titre} : collection {q} trop grande')
        for ok, msg in a.controles:
            if not ok:
                erreurs.append(f'{a.num} {a.titre} : contrôle « {msg} » faux')
        # La page d’activité ajuste l’échelle ; au-delà de ces dimensions, la réduction rendrait les dessins trop petits.
        if a.hauteur > 20.0 or a.largeur > 17.2:
            erreurs.append(f'{a.num} {a.titre} : figure trop grande ({a.largeur} x {a.hauteur})')
        if a.rubrique not in mod.R:
            erreurs.append(f'{a.num} : rubrique inconnue {a.rubrique}')
    rub_utilisees = {a.rubrique for a in toutes}
    for k in mod.R:
        if k not in rub_utilisees:
            erreurs.append(f'rubrique du programme non travaillée : {k} {mod.R[k]}')
    assert not erreurs, '\n'.join(erreurs)

    for a in toutes:
        ecrire(dossier / 'figures' / f'{a.fig}.tex', a.figure + '\n')

    pages = []
    for i, (titre, sous, prog, acts, theme) in enumerate(parties, 1):
        liste = ''.join(rf'\ligneAct{{{a.num}}}{{{a.titre}}}{{{a.label}}}' for a in acts)
        pages.append(rf'\partieMat{{{i}}}{{{titre}}}{{{sous}}}{{{decor_partie(theme)}}}{{{prog}}}{{{liste}}}')
        for a in acts:
            pictos = ','.join(a.pictos)
            pages.append(rf'\begin{{activite}}{{{a.num}}}{{{a.titre}}}{{{pictos}}}{{{gras(a.consigne)}}}{{{a.objectif}}}{{{a.label}}}'
                         + '\n' + rf'\matFigurePage{{{a.fig}}}' + '\n' + r'\end{activite}')
    ecrire(dossier / 'activites.tex', '\n'.join(pages) + '\n')

    guide = r'\clearpage\pagestyle{matSimple}\phantomsection\label{guide}\pdfbookmark[0]{Guide de l’adulte}{bm-guide}' + '\n'
    guide += r'\matPageTitre{Guide de l’adulte}{Objectifs, manipulations, mots à faire dire et réponses}' + '\n'
    guide += (r'{\fontsize{9.5}{13.5}\selectfont Pour chaque activité : l’objectif tiré du programme, ce que l’on peut faire '
              r'avec de vrais objets avant la fiche, les mots que l’enfant est invité à dire, puis la réponse attendue. '
              r'Les images en vert montrent une réponse correcte ; d’autres réponses peuvent être justes lorsque la consigne le permet.\par}' + '\n')
    for i, (titre, sous, prog, acts, theme) in enumerate(parties, 1):
        guide += rf'\par\needspace{{62mm}}\vspace{{6mm}}{{\otSemi\fontsize{{9}}{{11}}\selectfont\color{{matAccent}}\otCaps[8]{{Partie {i} · {titre}}}}}\par\vspace{{1mm}}' + '\n'
        for a in acts:
            vignette = a.fig if a.corrige else ''
            guide += rf'\guideEntree{{{a.label}}}{{{a.num}}}{{{a.titre}}}{{{a.objectif}}}{{{a.avant}}}{{{a.dire}}}{{{a.reponse}}}{{{vignette}}}' + '\n'
    ecrire(dossier / 'guide.tex', guide)

    rep = r'\clearpage\pagestyle{matSimple}\phantomsection\label{reperage}\pdfbookmark[0]{Repérage du programme}{bm-reperage}' + '\n'
    rep += r'\matPageTitre{Repérage du programme}{' + niv['nom'] + ' · objectifs « ' + niv['age'] + ' » du programme de maternelle}' + '\n'
    rep += (r'{\fontsize{9.5}{13.5}\selectfont Chaque objectif d’apprentissage du programme pour cette tranche d’âge est relié aux activités '
            r'qui le travaillent. Les numéros renvoient aux pages du cahier.\par}\vspace{5mm}' + '\n')
    rep += r'{\fontsize{9.5}{13}\selectfont\begin{tabularx}{\linewidth}{@{}Xr@{}}\toprule' + '\n'
    rep += r'{\otSemi Objectif du programme} & {\otSemi Activités}\\\midrule' + '\n'
    for k, lib in mod.R.items():
        nums = [a for a in toutes if a.rubrique == k]
        refs = ', '.join(rf'\hyperref[{a.label}]{{{a.num}}}' for a in nums)
        rep += rf'{lib} & {refs}\\[1.6mm]' + '\n'
    rep += r'\bottomrule\end{tabularx}\par}' + '\n'
    ecrire(dossier / 'reperage.tex', rep)

    sources = r'\clearpage\pagestyle{matSimple}\phantomsection\label{sources}\pdfbookmark[0]{Sources}{bm-sources}' + '\n'
    sources += r'\matPageTitre{Sources et édition}{Références officielles · France}' + '\n' + r'{\fontsize{9.5}{13.5}\selectfont '
    for i, (t, d, u) in enumerate(SOURCES, 1):
        sources += rf'\textbf{{{i}. {t}}}\par {d}\par\href{{{u}}}{{\textcolor{{otGreenDark}}{{Consulter la source officielle}}}}\par\medskip' + '\n'
    sources += mod.PERIMETRE + r'\par}' + '\n'
    ecrire(dossier / 'sources.tex', sources)

    etoiles = ''
    for a in toutes:
        etoiles += (rf'\begin{{tikzpicture}}\pic[scale=1.25,mat/c=white] at (0,0) {{etoile}};'
                    rf'\node[font=\otSemi\fontsize{{9}}{{9}}\selectfont,text=otNavy] at (0,-0.95) {{{a.num}}};\end{{tikzpicture}}\hspace{{3.2mm}}')
    ecrire(dossier / 'parcours.tex', r'{\centering ' + etoiles + r'\par}' + '\n')

    sommaire = ''
    for i, (titre, sous, prog, acts, theme) in enumerate(parties, 1):
        sommaire += (rf'\par\vspace{{3.4mm}}{{\otSemi\fontsize{{8}}{{10}}\selectfont\color{{matAccent}}\otCaps[6]{{Partie {i}}}}}\hspace{{2mm}}'
                     rf'{{\otSemi\fontsize{{12}}{{15}}\selectfont\color{{otNavy}}{titre}}}\dotfill{{\otMedium\small activités {acts[0].num} à {acts[-1].num} · p.\,\pageref*{{{acts[0].label}}}}}\par' + '\n')
    for lab, t in [('guide', 'Guide de l’adulte : objectifs, conseils et réponses'), ('reperage', 'Repérage du programme'), ('sources', 'Sources et édition')]:
        sommaire += rf'\par\vspace{{3.4mm}}{{\otMedium\fontsize{{11}}{{14}}\selectfont {t}}}\dotfill{{\otMedium\small p.\,\pageref*{{{lab}}}}}\par' + '\n'
    ecrire(dossier / 'sommaire.tex', sommaire)

    nb = len(toutes)
    ecrire(dossier / 'niveau.tex', '\n'.join([
        rf'\renewcommand{{\matNiveau}}{{{niv["nom"]}}}',
        rf'\renewcommand{{\matNiveauCourt}}{{{niv["court"]}}}',
        rf'\renewcommand{{\matAge}}{{{niv["age"]}}}',
        rf'\colorlet{{matAccent}}{{{niv["accent"]}}}',
        rf'\newcommand{{\matNbActivites}}{{{nb}}}',
        r'\newcommand{\matResume}{' + mod.RESUME + '}',
        rf'\newcommand{{\matCouvMain}}{{{niv["couv"][0]}}}\newcommand{{\matCouvDe}}{{{niv["couv"][1]}}}',
        rf'\hypersetup{{pdftitle={{Mathématiques - Maternelle - {niv["nom"]}}},pdfauthor={{OptiTAB}},pdfsubject={{Cahier d’activités : {nb} activités et guide de l’adulte}}}}',
    ]) + '\n')

    main = r'''% !TEX program = lualatex
\documentclass[11pt,twoside,openany]{book}
\usepackage{maternelle}
\input{niveau}
\begin{document}
\pagenumbering{alph}
\input{couverture}
\pagenumbering{arabic}
\input{liminaires}
\input{activites}
\input{guide}
\input{reperage}
\input{sources}
\input{dos}
\end{document}
'''
    ecrire(dossier / 'main.tex', main)
    manifeste = dict(niveau=niv['nom'], cle=cle, age=niv['age'], activites=nb, parties=[p[0] for p in parties],
                     liste=[dict(num=a.num, titre=a.titre, rubrique=a.rubrique, label=a.label, figure=a.fig, partie=i)
                            for i, p in enumerate(parties, 1) for a in p[3]])
    ecrire(dossier / 'manifeste.json', json.dumps(manifeste, ensure_ascii=False, indent=2))
    print(json.dumps(dict(niveau=niv['nom'], activites=nb, parties=len(parties)), ensure_ascii=True))

if __name__ == '__main__':
    construire(sys.argv[1])
