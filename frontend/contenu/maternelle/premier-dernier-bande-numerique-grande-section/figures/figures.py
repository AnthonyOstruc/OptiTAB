# -*- coding: utf-8 -*-
"""Figures de la page « Premier, dernier et bande numérique en grande section » (ressources gratuites, maternelle).

    python frontend/contenu/maternelle/premier-dernier-bande-numerique-grande-section/figures/figures.py

Les dessins viennent tels quels du cahier OptiTAB de Grande Section
(livre/livre-maths/livre-maternelle/gs.py, lu sans être modifié) : même
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
    'canards': 'a_canards_rang',   # Premier, deuxième, avant-dernier, dernier
    'cartes': 'a_rang_dix',        # Changer de point de départ
    'oie': 'a_oie_gs',             # Avancer, reculer sur la bande numérique
}

# Retouches pour l'écran (le cahier A4 n'est pas modifié) :
#  - canards : le bec du premier canard mordait sur la mare (mare décalée) ;
#    étiquettes de 10-12 pt illisibles sur téléphone (16-17 pt, légende sur deux lignes) ;
#  - cartes : étiquettes « départ » agrandies (sur deux lignes) ; l'ellipse
#    « entourée » du cahier débordait sur les cartes voisines : le contour vert
#    suit désormais le bord de la carte.
def _legende(couleur, x, mot, x2, y2):
    """Une pastille de la légende des canards : (x, 1.6) en 12 pt -> (x2, y2) en 17 pt."""
    avant = (rf'\fill[{couleur}] ({x:g},1.6) circle (0.32);\node[anchor=west,font=\otMedium\fontsize{{12}}{{14}}\selectfont,'
             rf'text=otMuted] at ({x + 0.5:g},1.6) {{{mot}}};')
    # Ancre sur la ligne de base : « premier » et « deuxième » restent alignés malgré l'accent.
    apres = (rf'\fill[{couleur}] ({x2:g},{y2:g}) circle (0.36);\node[anchor=base west,font=\otMedium\fontsize{{17}}{{20}}\selectfont,'
             rf'text=otMuted] at ({x2 + 0.6:g},{y2 - 0.21:g}) {{{mot}}};')
    return avant, apres


RETOUCHES = {
    'canards': [
        (r'\draw[mat contour,fill=matCiel] (15.6,5.6) ellipse (1.3 and 0.8);',
         r'\draw[mat contour,fill=matCiel] (16.1,5.6) ellipse (1.15 and 0.8);'),
        (r'\fontsize{10}{12}\selectfont,text=otMuted] at (15.6,4.2) {la mare};',
         r'\fontsize{17}{20}\selectfont,text=otMuted] at (16.1,4.15) {la mare};'),
        _legende('matRouge', 1.4, 'premier', 2.0, 2.6),
        _legende('matJaune', 5, 'deuxième', 9.0, 2.6),
        _legende('otGreen', 8.8, 'avant-dernier', 2.0, 1.2),
        _legende('matBleu', 13.4, 'dernier', 9.0, 1.2),
    ],
    'cartes': [
        (r'\node[anchor=center,font=\otMedium\fontsize{10}{12}\selectfont,text=otMuted] at (0.7,4.4) {départ bleu};',
         r'\node[anchor=north,align=center,font=\otMedium\fontsize{17}{20}\selectfont,text=otMuted] at (0.7,4.55) {départ\\bleu};'),
        (r'\node[anchor=center,font=\otMedium\fontsize{10}{12}\selectfont,text=otMuted] at (16.3,4.4) {départ rouge};',
         r'\node[anchor=north,align=center,font=\otMedium\fontsize{17}{20}\selectfont,text=otMuted] at (16.3,4.55) {départ\\rouge};'),
        (r'\draw[sol entoure] (12.04,6) ellipse (0.95 and 1.4);',
         r'\draw[sol entoure,line width=3.2pt,rounded corners=4pt] (11.44,5.0) rectangle (12.64,7.0);'),
    ],
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
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,shapes.geometric}
\usepackage{objets}
\colorlet{matAccent}{matViolet}
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
ESPACEMENT = {'modele': 1.22}


def activites():
    sys.path.insert(0, str(LIVRE))
    import gs  # noqa: E402  (module du cahier, lu seulement)
    import outils  # noqa: E402
    origine = outils.positions
    sortie = {}
    for nom, fonction in ACTIVITES.items():
        k = ESPACEMENT.get(nom, 1.0)
        outils.positions = lambda n, kind, cx, cy, w, h, d=1.0, graine=0: origine(
            n, kind, cx, cy, w, h, d * k if kind == 'vrac' else d, graine)
        a = getattr(gs, fonction)()
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
