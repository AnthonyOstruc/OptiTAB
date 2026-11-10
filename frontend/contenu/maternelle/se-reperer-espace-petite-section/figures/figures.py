# -*- coding: utf-8 -*-
"""Figures de la page « Se repérer dans l'espace en petite section » (ressources gratuites, maternelle).

    python frontend/contenu/maternelle/se-reperer-espace-petite-section/figures/figures.py

Les dessins viennent tels quels du cahier OptiTAB de Petite Section
(livre/livre-maths/livre-maternelle/ps.py, lu sans être modifié) : même
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
    'bocal': 'a_bocal',        # Dans le bocal (dans, dehors)
    'table': 'a_table',        # Sur ou sous la table (sur, sous)
    'arbre': 'a_derriere',     # Devant ou derrière (devant, derrière)
}

# Retouches de mise en place (aucun texte dans ces figures) :
# - table : dans le cahier, les pieds de la table s'arrêtent au-dessus du sol ;
#   on remonte le sol jusqu'aux pieds et l'objet posé dessous avec lui, on
#   resserre l'ellipse de la réponse (elle ne touche plus le plateau) et l'on
#   réduit les cadres, trop hauts une fois le sol remonté ;
# - arbre : le tronc s'arrête au-dessus du sol ; on remonte le sol jusqu'au
#   tronc et les lapins avec lui, et l'ellipse de la réponse passe à égale
#   distance de l'oreille du lapin et du feuillage.
RETOUCHES = {
    'table': [(r'(0.3,0.4) rectangle (8.3,12.4)', r'(0.3,2.4) rectangle (8.3,11.4)'),
              (r'(8.7,0.4) rectangle (16.7,12.4)', r'(8.7,2.4) rectangle (16.7,11.4)'),
              (r'(0.5,3.5) -- (8.1,3.5)', r'(0.5,4.17) -- (8.1,4.17)'),
              (r'(8.9,3.5) -- (16.5,3.5)', r'(8.9,4.17) -- (16.5,4.17)'),
              (r'at (4.3,4.65) {ballon}', r'at (4.3,5.32) {ballon}'),
              (r'at (12.7,4.6) {chat}', r'at (12.7,5.27) {chat}'),
              (r'(12.7,4.6) ellipse (1.8 and 1.7)', r'(12.7,5.36) ellipse (1.7 and 1.45)')],
    'arbre': [(r'(0.3,0.4) rectangle (8.3,13)', r'(0.3,1.0) rectangle (8.3,12.4)'),
              (r'(8.7,0.4) rectangle (16.7,13)', r'(8.7,1.0) rectangle (16.7,12.4)'),
              (r'(0.5,2.1) -- (8.1,2.1)', r'(0.5,2.3) -- (8.1,2.3)'),
              (r'(8.9,2.1) -- (16.5,2.1)', r'(8.9,2.3) -- (16.5,2.3)'),
              (r'at (5.05,3.3) {lapin}', r'at (5.05,3.5) {lapin}'),
              (r'at (13.8,3.3) {lapin}', r'at (13.8,3.5) {lapin}'),
              (r'(5.05,3.3) ellipse (1.6 and 1.7)', r'(5.05,3.525) ellipse (1.6 and 1.425)')],
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
\colorlet{matAccent}{otGreen}   % couleur de la Petite Section
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


# Pas de collection « en vrac » dans ces activités : aucun espacement à modifier.
ESPACEMENT = {}


def activites():
    sys.path.insert(0, str(LIVRE))
    import ps  # noqa: E402  (module du cahier, lu seulement)
    import outils  # noqa: E402
    origine = outils.positions
    sortie = {}
    for nom, fonction in ACTIVITES.items():
        k = ESPACEMENT.get(nom, 1.0)
        outils.positions = lambda n, kind, cx, cy, w, h, d=1.0, graine=0: origine(
            n, kind, cx, cy, w, h, d * k if kind == 'vrac' else d, graine)
        a = getattr(ps, fonction)()
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
