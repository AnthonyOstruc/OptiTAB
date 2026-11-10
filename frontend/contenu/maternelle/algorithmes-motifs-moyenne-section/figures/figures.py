# -*- coding: utf-8 -*-
"""Figures de la page « Algorithmes et motifs en moyenne section » (ressources gratuites, maternelle).

    python frontend/contenu/maternelle/algorithmes-motifs-moyenne-section/figures/figures.py

Les dessins viennent tels quels du cahier OptiTAB de Moyenne Section
(livre/livre-maths/livre-maternelle/ms.py, lu sans être modifié) : même
bibliothèque d'illustrations (commun/objets.sty), mêmes couleurs, même couche
de correction en vert. Chaque activité donne deux images :
    <nom>_enonce.png   la figure que l'enfant complète ;
    <nom>_reponse.png  la même figure complétée (couche « solution » du cahier).
Les deux images d'une activité ont exactement le même cadre (celui de la
réponse), pour qu'on puisse les comparer d'un coup d'œil.

Sortie : figures/images/*.png, toutes à la même échelle, au plus LARGEUR_PX
pixels de large (affichées à moitié sur le site, comme les autres figures).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True   # rien n'est écrit dans le dossier du livre

ICI = Path(__file__).resolve().parent
LIVRE = ICI.parents[4] / 'livre' / 'livre-maths' / 'livre-maternelle'
MIKTEX = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/MiKTeX/miktex/bin/x64'
LUALATEX = str(MIKTEX / 'lualatex.exe') if (MIKTEX / 'lualatex.exe').exists() else 'lualatex'
PDFTOCAIRO = str(MIKTEX / 'pdftocairo.exe') if (MIKTEX / 'pdftocairo.exe').exists() else 'pdftocairo'

LARGEUR_PX = 1400   # affichée à 700 px au plus

# Activité du cahier → nom des images sur le site.
ACTIVITES = {
    'continuer': 'a_prolonger',       # Continue la rangée (prolonger un motif)
    'intrus': 'a_intrus_motif',       # L'intrus de la rangée (trouver l'erreur)
    'memoire': 'a_memoire',           # La tour de mémoire (mémoriser un motif)
}

# Retouches pour l'écran (le livre n'est pas modifié) :
#  - « Continue la rangée » : dans la réponse, les étoiles dessinées dans les
#    cases en pointillés dépassaient du cadre ; on les réduit et on les centre
#    pour qu'elles ne touchent plus le trait ; même chose pour les triangles,
#    dont la pointe touchait presque le haut de la case ;
#  - « L'intrus de la rangée » : trois étoiles côte à côte se touchaient presque ;
#    on les réduit un peu pour que chaque forme soit bien séparée ;
#  - « La tour de mémoire » : les deux étiquettes (12 pt dans le cahier A4)
#    seraient illisibles sur téléphone ; on les agrandit.
_ETOILE = r'\pic[scale={},mat/c=matJaune] at ({},{}) {{etoile}}'
_TRIANGLE = r'\draw[mat contour,fill=otGreen] ({},{}) -- ({},{}) -- ({},{}) -- cycle;'
_INTRUS_ETOILES = [(x, 12.4) for x in (1, 4.32, 7.64, 9.3, 10.96, 14.28)] + [(4.32, 3.6), (14.28, 3.6)]
RETOUCHES = {
    'continuer': [(_ETOILE.format(1.9, x, y), _ETOILE.format(1.4, x, round(y - 0.06, 2)))
                  for x, y in ((12, 13.4), (15.5, 13.4), (12, 9.5), (15.5, 1.7))]
                 + [(_TRIANGLE.format(x, y + 0.75, x - 0.65, y - 0.375, x + 0.65, y - 0.375),
                     _TRIANGLE.format(x, round(y + 0.495, 3), round(x - 0.572, 3), round(y - 0.495, 3), round(x + 0.572, 3), round(y - 0.495, 3)))
                    for x, y in ((15.5, 5.6), (13.75, 1.7))],
    'intrus': [(_ETOILE.format(1.71, x, y), _ETOILE.format(1.55, x, round(y - 0.03, 2)))
               for x, y in _INTRUS_ETOILES],
    'memoire': [(r'\fontsize{12}{14}\selectfont,text=otMuted] at (4,9.9) {le modèle}',
                 r'\fontsize{19}{22}\selectfont,text=otMuted] at (4,9.75) {le modèle}'),
                (r'\fontsize{12}{14}\selectfont,text=otMuted] at (13,9.9) {de mémoire}',
                 r'\fontsize{19}{22}\selectfont,text=otMuted] at (13,9.75) {de mémoire}')],
}

PREAMBULE = r"""\documentclass[border=10pt]{standalone}
\usepackage{fontspec}
\setmainfont{Montserrat}[Extension=.otf,UprightFont=*-Regular,BoldFont=*-SemiBold]
\newfontfamily\otMedium{Montserrat}[Extension=.otf,UprightFont=*-Medium,BoldFont=*-SemiBold]
\newfontfamily\otSemi{Montserrat}[Extension=.otf,UprightFont=*-SemiBold,BoldFont=*-Bold]
\newfontfamily\otBold{Montserrat}[Extension=.otf,UprightFont=*-Bold,BoldFont=*-ExtraBold]
\usepackage{xcolor}
\definecolor{otNavy}{HTML}{1B3C8E}
\definecolor{otGreen}{HTML}{5FAC60}
\definecolor{otGreenDark}{HTML}{3B8544}
\definecolor{otInk}{HTML}{1C2130}
\definecolor{otMuted}{HTML}{6B7385}
\definecolor{otRule}{HTML}{D5DAE3}
\definecolor{otOrange}{HTML}{F0A23B}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,shapes.geometric}
\usepackage{objets}
\colorlet{matAccent}{otOrange}
\newif\ifmatSolution
\newcommand{\sol}[1]{\ifmatSolution #1\fi}
\newcommand{\enonce}[1]{\ifmatSolution\else #1\fi}
\tikzset{
  sol trait/.style={draw=otGreenDark,line width=2.2pt,line cap=round,line join=round},
  sol entoure/.style={draw=otGreenDark,line width=2pt},
  zone/.style={draw=otRule,line width=1pt,rounded corners=6pt,fill=white},
  zone pleine/.style={draw=otRule,line width=1pt,rounded corners=6pt,fill=matAccent!8},
  point relier/.style={fill=matTrait,draw=white,line width=.8pt},
  pointille/.style={draw=otMuted!60,line width=1pt,dash pattern=on 3pt off 3pt},
}
"""

# Cadre de la figure complétée, écrit dans le journal pour être réutilisé par l'énoncé.
MESURE = (r'\pgfpointanchor{current bounding box}{south west}\pgfgetlastxy{\matXa}{\matYa}'
          r'\pgfpointanchor{current bounding box}{north east}\pgfgetlastxy{\matXb}{\matYb}'
          r'\typeout{MATBBOX|\matXa|\matYa|\matXb|\matYb|}')


# Collections « en vrac » plus aérées : dans le cahier, la feuille d'une pomme
# touche parfois la pomme voisine ; à l'écran, chaque objet doit être bien séparé.
ESPACEMENT = {}


def activites():
    sys.path.insert(0, str(LIVRE))
    import ms  # noqa: E402  (module du cahier, lu seulement)
    import outils  # noqa: E402
    origine = outils.positions
    sortie = {}
    for nom, fonction in ACTIVITES.items():
        k = ESPACEMENT.get(nom, 1.0)
        outils.positions = lambda n, kind, cx, cy, w, h, d=1.0, graine=0: origine(
            n, kind, cx, cy, w, h, d * k if kind == 'vrac' else d, graine)
        a = getattr(ms, fonction)()
        outils.positions = origine
        assert all(ok for ok, _ in a.controles), f'{nom} : contrôle du cahier faux'
        code = a.figure
        for avant, apres in RETOUCHES.get(nom, []):
            assert avant in code, f'retouche introuvable pour {nom}'
            code = code.replace(avant, apres)
        sortie[nom] = code
    return sortie


def compiler(build, nom, code, solution, cadre=None):
    corps = code
    if cadre:
        corps = corps.replace(r'\end{tikzpicture}', rf'\path ({cadre[0]},{cadre[1]}) rectangle ({cadre[2]},{cadre[3]});\end{{tikzpicture}}')
    else:
        corps = corps.replace(r'\end{tikzpicture}', MESURE + r'\end{tikzpicture}')
    drapeau = r'\matSolutiontrue' if solution else r'\matSolutionfalse'
    tex = build / f'{nom}.tex'
    tex.write_text(PREAMBULE + '\\begin{document}\n' + drapeau + '\n' + corps + '\n\\end{document}\n', encoding='utf-8')
    env = dict(os.environ, TEXINPUTS=f'{LIVRE / "commun"}{os.pathsep}')
    r = subprocess.run([LUALATEX, '-interaction=nonstopmode', '-halt-on-error', tex.name], cwd=build, env=env,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    log = (build / f'{nom}.log').read_text(encoding='utf-8', errors='replace')
    if r.returncode != 0:
        sys.exit(f'{nom} : échec de compilation\n' + '\n'.join(l for l in log.splitlines() if l.startswith('!'))[:800])
    for motif in ('Missing character', 'Overfull'):
        if motif in log:
            sys.exit(f'{nom} : « {motif} » dans le journal')
    m = re.search(r'MATBBOX\|([-\d.]+pt)\|([-\d.]+pt)\|([-\d.]+pt)\|([-\d.]+pt)\|', log)
    return build / f'{nom}.pdf', (m.groups() if m else None)


def taille_pdf_pt(pdf):
    """Largeur et hauteur de la page (MediaBox) en points PostScript."""
    data = pdf.read_bytes()
    m = re.search(rb'/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]', data)
    x0, y0, x1, y1 = (float(v) for v in m.groups())
    return x1 - x0, y1 - y0


def main():
    sortie = ICI / 'images'
    sortie.mkdir(exist_ok=True)
    codes = activites()
    with tempfile.TemporaryDirectory(prefix='mat_figures_') as dossier:
        build = Path(dossier)
        for f in ('objets.sty',):
            shutil.copy2(LIVRE / 'commun' / f, build / f)
        pdfs = {}
        for nom, code in codes.items():
            pdf_rep, cadre = compiler(build, f'{nom}_reponse', code, True)
            assert cadre, f'{nom} : cadre non mesuré'
            pdf_en, _ = compiler(build, f'{nom}_enonce', code, False, cadre)
            assert taille_pdf_pt(pdf_rep) == taille_pdf_pt(pdf_en), f'{nom} : cadres différents'
            pdfs[f'{nom}_enonce'] = pdf_en
            pdfs[f'{nom}_reponse'] = pdf_rep
        # Une seule échelle pour toutes les figures : la plus large fait LARGEUR_PX.
        largeur_max_pt = max(taille_pdf_pt(p)[0] for p in pdfs.values())
        ppp = int(LARGEUR_PX / (largeur_max_pt / 72))
        for nom, pdf in pdfs.items():
            subprocess.run([PDFTOCAIRO, '-png', '-r', str(ppp), '-singlefile', pdf.name, str(sortie / nom)],
                           cwd=build, check=True)
            print(f'{nom}.png', f'{ppp} ppp')
    try:
        from PIL import Image
        for png in sorted(sortie.glob('*.png')):
            im = Image.open(png)
            im.convert('RGB').save(png, optimize=True)
            print(png.name, im.size, f'{png.stat().st_size // 1024} Ko')
    except ImportError:
        pass


if __name__ == '__main__':
    main()
