# -*- coding: utf-8 -*-
"""Figures du site dans le style des livres OptiTAB (LuaLaTeX + TikZ/pgfplots).

Chaque notion du chantier a son fichier <dossier_notion>/figures/figures.py qui
définit au minimum :

    FIGURES = {"nom": r"\\begin{tikzpicture} … \\end{tikzpicture}", …}

et, facultativement :

    XLAB = {"nom": [(x, "g"|"d"|"c"|"h", r"\\frac{\\pi}{2}"), …]}  # graduations x placées à la main
    PREAMBULE_EXTRA = r"…"                                          # macros propres à la notion

Compilation (depuis n'importe où) :

    python figures_livre.py <dossier_notion> [nom …] [--planche] [--jobs 3]

Sortie : <dossier_notion>/figures/images/<nom>.png à 240 ppp, fond blanc,
affichées sur le site à la MOITIÉ de leur taille en pixels (l'importeur règle
width/height) : le texte des figures a alors la taille du texte courant.
--planche compose figures/planche_nouvelles_NN.png pour la relecture (outil Read).

Réglages communs : Libertinus (texte, formules), Montserrat (graduations,
notes), palette du logo. Styles TikZ : voir PREAMBULE ci-dessous (courbe,
courbe2, pale, seuil, asymptote, guide, etiq, note ; geoTrait, geoAide,
geoVecteur, geoReponse, geoLabel, geoRemplissage, cote ; \\pnt, \\pntv,
\\guides, \\guidev, \\sol, \\borneF, \\borneO, \\angledroit, \\codage, \\cote).
Les livres de collège ont des générateurs Python de figures TikZ réutilisables :
livre/livre-maths/livre-sixieme/generer_figures.py (géométrie, solides, droites
graduées, diagrammes, horloges…) — importer ses fonctions ou les recopier.
"""
import importlib.util
import re
import struct
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PREAMBULE = r"""
\documentclass[border=6pt]{standalone}
\usepackage{amsmath}
\usepackage{unicode-math}
\setmainfont{LibertinusSerif}[Extension=.otf, UprightFont=*-Regular, ItalicFont=*-Italic,
  BoldFont=*-Semibold, BoldItalicFont=*-SemiboldItalic]
\setmathfont{LibertinusMath-Regular.otf}
\newfontfamily\otRegular{Montserrat}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-SemiBold]
\newfontfamily\otMedium{Montserrat}[Extension=.otf, UprightFont=*-Medium, BoldFont=*-SemiBold]
\usepackage{xcolor}
\definecolor{otNavy}{HTML}{1B3C8E}
\definecolor{otGreen}{HTML}{5FAC60}
\definecolor{otGreenDark}{HTML}{3B8544}
\definecolor{otInk}{HTML}{1C2130}
\definecolor{otMuted}{HTML}{6B7385}
\definecolor{otRule}{HTML}{D5DAE3}
\definecolor{otOrange}{HTML}{F0A23B}
\definecolor{otRed}{HTML}{E0574C}
\definecolor{otSky}{HTML}{EAF0FA}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,angles,quotes,decorations.pathreplacing,decorations.markings,patterns,positioning,shapes.geometric,3d,intersections}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{fillbetween}
% ---------------------------------------------------------------- repères
\pgfplotsset{otWeb/.style={
  axis lines=middle,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
  grid=major, grid style={otRule!75,line width=0.35pt},
  xlabel={$x$}, ylabel={$y$},
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,font=\normalsize,text=otMuted},
  every axis y label/.style={at={(current axis.above origin)},anchor=south,font=\normalsize,text=otMuted},
  clip=false, scale only axis, axis on top=false,
  yticklabel style={anchor=south east,inner sep=1.2pt,xshift=-1pt,yshift=1pt},
  xticklabel style={anchor=north,yshift=-2.5pt},
  samples=240,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
\pgfplotsset{otTrig/.style={otWeb, trig format plots=rad}}
% diagrammes en barres / statistiques
\pgfplotsset{otBarres/.style={
  axis lines*=left, ymajorgrids, grid style={otRule!75,line width=0.35pt},
  axis line style={otMuted,line width=0.6pt}, tick style={otMuted,line width=0.5pt},
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  label style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  ybar, bar width=16pt, enlarge x limits=0.15, ymin=0,
  cycle list={{fill=otNavy!60,draw=otNavy},{fill=otGreen!70,draw=otGreenDark},{fill=otOrange!75,draw=otOrange!80!black},{fill=otMuted!45,draw=otMuted}},
  nodes near coords style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otInk},
  scale only axis,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
\tikzset{
  courbe/.style={otNavy,line width=1.35pt},
  courbe2/.style={otGreen,line width=1.35pt},
  pale/.style={otNavy!35,line width=1.1pt},
  seuil/.style={otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt},
  asymptote/.style={otRed!85,line width=0.75pt,dash pattern=on 4pt off 2.5pt},
  guide/.style={otMuted,line width=0.5pt,dash pattern=on 2pt off 1.6pt},
  etiq/.style={fill=white,inner sep=1.4pt,font=\normalsize},
  note/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,fill=white,inner sep=1.2pt},
  % géométrie (styles des livres de collège)
  geoTrait/.style={otNavy,line width=.9pt,line join=round},
  geoAide/.style={otGreenDark,line width=.75pt,dashed},
  geoVecteur/.style={otNavy,line width=.9pt,-{Stealth[length=2mm]}},
  geoReponse/.style={otGreenDark,line width=1pt},
  geoLabel/.style={fill=white,inner sep=1pt,text=otInk},
  geoRemplissage/.style={fill=otSky},
  geoPoint/.style={circle,fill=otNavy,inner sep=0pt,minimum size=3.6pt},
  cote/.style={otMuted,line width=.55pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}},
  coteTexte/.style={fill=white,inner sep=1.2pt,text=otInk,font=\normalsize},
}
% points : plein, vide ; repères en pointillés ; solution sur l'axe des abscisses
\newcommand{\pnt}[3][otNavy]{\fill[#1] (axis cs:#2,#3) circle (2.1pt);}
\newcommand{\pntv}[3][otNavy]{\draw[#1,fill=white,line width=0.9pt] (axis cs:#2,#3) circle (2.3pt);}
\newcommand{\guides}[2]{\draw[guide] (axis cs:#1,0) -- (axis cs:#1,#2) -- (axis cs:0,#2);}
\newcommand{\guidev}[2]{\draw[guide] (axis cs:#1,0) -- (axis cs:#1,#2);}
\newcommand{\sol}[2]{\draw[otGreen,line width=3pt,line cap=butt,opacity=0.9] (axis cs:#1,0) -- (axis cs:#2,0);}
\newcommand{\borneF}[1]{\fill[otGreenDark] (axis cs:#1,0) circle (2.5pt);}
\newcommand{\borneO}[1]{\draw[otGreenDark,fill=white,line width=1pt] (axis cs:#1,0) circle (2.5pt);}
% \angledroit{A}{B}{C} : angle droit en B (coordonnées nommées)
\newcommand{\angledroit}[4][0.22]{\draw[otNavy,line width=.6pt] ($(#3)!#1cm!(#2)$) -- ($($(#3)!#1cm!(#2)$)+($(#3)!#1cm!(#4)$)-(#3)$) -- ($(#3)!#1cm!(#4)$);}
% \codage[n]{A}{B} : n petits traits au milieu de [AB] (longueurs égales)
\newcommand{\codage}[3][1]{\path[postaction={decorate,decoration={markings,mark=at position 0.5 with
  {\foreach \k in {1,...,#1}{\draw[otNavy,line width=.7pt] ({(\k-(#1+1)/2)*2.4pt},-3.2pt) -- ++(0,6.4pt);}}}}] (#2) -- (#3);}
% \cote[décalage]{A}{B}{texte} : flèche de cote parallèle à [AB], décalée vers la gauche de A→B
\newcommand{\cote}[4][0.35]{\draw[cote] ($(#2)!#1cm!90:(#3)$) -- ($(#3)!#1cm!-90:(#2)$) node[midway,coteTexte]{#4};
  \draw[otMuted!70,line width=.4pt] (#2) -- ($(#2)!#1cm+2pt!90:(#3)$) (#3) -- ($(#3)!#1cm+2pt!-90:(#2)$);}
\newif\ifotGeoCorrige
\newcommand{\geoSolution}[1]{\ifotGeoCorrige #1\fi}
\newcommand{\geoEnonce}[1]{\ifotGeoCorrige\else #1\fi}
\newcommand{\stevin}[1]{\tikz[baseline=(s.base)]\node[circle,draw=otNavy,line width=.4pt,inner sep=.7pt,font=\scriptsize](s){#1};}
"""

ANCRES = {"g": "north east", "d": "north west", "c": "north", "h": "south"}
DECALAGES = {"g": "xshift=-1.5pt,yshift=-2pt", "d": "xshift=1.5pt,yshift=-2pt", "c": "yshift=-2.5pt", "h": "yshift=2.5pt"}

# Largeur en pixels à 240 ppp (affichée à moitié) : au-delà de 900 px la figure
# est rétrécie sur téléphone et son texte devient petit ; au-delà de 1100 px, refus.
LARGEUR_CONSEILLEE_PX = 900
LARGEUR_MAX_PX = 1100
LARGEUR_MIN_PX = 240

# Version « sans texte » d'une figure (contrôle des chevauchements) : les nœuds
# gardent leur place mais deviennent invisibles.
SANS_TEXTE = r"""
\tikzset{every node/.append style={text opacity=0,fill opacity=0},
  geoPoint/.append style={fill opacity=1}}
\pgfplotsset{every axis/.append style={every tick label/.append style={text opacity=0,fill opacity=0},
  every axis label/.append style={text opacity=0,fill opacity=0},
  every axis title/.append style={text opacity=0,fill opacity=0},
  every node near coord/.append style={text opacity=0}}}
"""

VERROUS = Path(__file__).resolve().parent / ".verrous"
LUALATEX_SIMULTANES = 8   # pour toute la machine (tous agents confondus)


class Place:
    """Sémaphore inter-processus par fichiers : limite les compilations simultanées."""

    def __init__(self, nom, n):
        self.nom, self.n, self.fichier = nom, n, None

    def __enter__(self):
        import os
        import time
        VERROUS.mkdir(exist_ok=True)
        while True:
            for k in range(self.n):
                f = VERROUS / f"{self.nom}_{k}.lock"
                try:
                    if f.exists() and time.time() - f.stat().st_mtime > 600:
                        f.unlink()  # verrou abandonné
                    fd = os.open(f, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.write(fd, str(os.getpid()).encode())
                    os.close(fd)
                    self.fichier = f
                    return self
                except (FileExistsError, PermissionError):
                    continue
                except FileNotFoundError:
                    continue
            time.sleep(0.4)

    def __exit__(self, *exc):
        try:
            self.fichier.unlink()
        except OSError:
            pass


def lualatex(build, tex_name):
    with Place("lualatex", LUALATEX_SIMULTANES):
        return subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", tex_name],
                              cwd=build, capture_output=True, text=True, encoding="utf-8", errors="replace")


def chevauchements(png_complet, png_sans_texte):
    """Textes posés sur un trait.

    Compare la figure complète et la même figure sans texte : chaque groupe de
    pixels qui diffère est un texte (ou son fond blanc). Erreur si, dans le
    cadre d'un texte, un trait foncé reste VISIBLE (texte écrit par-dessus) ;
    avertissement si le fond blanc d'une étiquette masque un trait (étiquette
    posée sur une ligne : normal pour une cote ou une graduation, à vérifier sinon).
    """
    import numpy as np
    from PIL import Image
    from scipy import ndimage

    a = np.asarray(Image.open(png_complet).convert("L"), dtype=np.int16)
    b = np.asarray(Image.open(png_sans_texte).convert("L"), dtype=np.int16)
    if a.shape != b.shape:
        return [f"contrôle impossible (tailles {a.shape} / {b.shape})"], []
    diff = np.abs(a - b) > 40
    groupes, n = ndimage.label(ndimage.binary_dilation(diff, iterations=3))
    erreurs, avert = [], []
    h_img = a.shape[0]
    for k, tranche in enumerate(ndimage.find_objects(groupes), start=1):
        if tranche is None:
            continue
        masque = (groupes[tranche] == k) & diff[tranche]
        ys, xs = np.nonzero(masque)
        if not len(xs):
            continue
        y0, y1 = tranche[0].start + ys.min(), tranche[0].start + ys.max()
        x0, x1 = tranche[1].start + xs.min(), tranche[1].start + xs.max()
        if (x1 - x0) <= 15 and (y1 - y0) <= 15:
            continue  # point, petite marque
        sa = a[y0 + 2:y1 - 1, x0 + 2:x1 - 1]
        sb = b[y0 + 2:y1 - 1, x0 + 2:x1 - 1]
        trait = sb < 200
        visible = int((trait & (np.abs(sa - sb) <= 25)).sum())
        masque_blanc = int((trait & (sa > 235)).sum())
        ou = f"vers ({(x0 + x1) / 2 / 240 * 2.54:.1f} cm ; {(h_img - (y0 + y1) / 2) / 240 * 2.54:.1f} cm) depuis le coin bas-gauche"
        if visible > 18:
            erreurs.append(f"texte écrit sur un trait {ou} ({visible} px de trait visibles sous le texte)")
        elif masque_blanc > 40:
            avert.append(f"étiquette posée sur un trait, qu'elle coupe grâce à son fond blanc {ou} "
                         "(normal pour une cote ou une graduation ; sinon la déplacer)")
    return erreurs, avert


def graduations_x(code, nom, xlab):
    """Graduations de l'axe des abscisses placées à la main, du côté libre de la courbe.

    « g » sous l'axe à gauche du trait, « d » à droite, « c » centrée dessous,
    « h » au-dessus de l'axe ; leur fond blanc efface asymptotes et pointillés.
    """
    if not xlab or nom not in xlab:
        return code
    code = re.sub(r"xticklabels=\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}", "xticklabels={}", code)
    nodes = "".join(
        f"  \\node[anchor={ANCRES[cote]},{DECALAGES[cote]},font=\\otRegular\\fontsize{{9}}{{10}}\\selectfont,"
        f"text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:{x},0) {{$\\displaystyle {tex}$}};\n"
        for x, cote, tex in xlab[nom]
    )
    return code.replace("\\end{axis}", nodes + "\\end{axis}", 1)


def taille_png(png):
    with open(png, "rb") as fh:
        tete = fh.read(24)
    return struct.unpack(">II", tete[16:24])


def charger(dossier_notion):
    chemin = Path(dossier_notion) / "figures" / "figures.py"
    spec = importlib.util.spec_from_file_location("figures_notion", chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(chemin.parent))
    spec.loader.exec_module(mod)
    return mod


def compiler_un(nom, code, build, sortie, xlab=None, extra="", tolere=None):
    build.mkdir(parents=True, exist_ok=True)
    sortie.mkdir(parents=True, exist_ok=True)
    tex = build / f"{nom}.tex"
    corps = graduations_x(code, nom, xlab)
    tex.write_text(PREAMBULE + extra + "\n\\begin{document}\n" + corps + "\n\\end{document}\n", encoding="utf-8")
    r = lualatex(build, tex.name)
    pdf = build / f"{nom}.pdf"
    if r.returncode != 0 or not pdf.exists():
        log = (build / f"{nom}.log").read_text(encoding="utf-8", errors="replace") if (build / f"{nom}.log").exists() else r.stdout
        lignes = log.splitlines()
        erreurs = []
        for k, l in enumerate(lignes):
            if l.startswith("!"):
                erreurs.append(" ".join(x.strip() for x in lignes[k:k + 3]))
        return nom, False, erreurs[:4] or [r.stdout[-300:]]
    png = sortie / f"{nom}.png"
    subprocess.run(["pdftocairo", "-png", "-r", "240", "-singlefile", pdf.name, str(sortie / nom)],
                   cwd=build, check=True)
    w, h = taille_png(png)
    erreurs, avert = [], []
    if w > LARGEUR_MAX_PX:
        erreurs.append(f"trop large ({w} px > {LARGEUR_MAX_PX}) : sur téléphone elle serait rétrécie et son texte illisible")
    elif w > LARGEUR_CONSEILLEE_PX:
        avert.append(f"large ({w} px, conseillé ≤ {LARGEUR_CONSEILLEE_PX})")
    if w < LARGEUR_MIN_PX:
        avert.append(f"très étroite ({w} px)")
    # même figure sans texte → chevauchements texte / traits
    tex2 = build / f"{nom}__sans_texte.tex"
    tex2.write_text(PREAMBULE + extra + SANS_TEXTE + "\n\\begin{document}\n" + corps + "\n\\end{document}\n", encoding="utf-8")
    r2 = lualatex(build, tex2.name)
    if r2.returncode == 0:
        subprocess.run(["pdftocairo", "-png", "-r", "240", "-singlefile", f"{nom}__sans_texte.pdf", str(build / f"{nom}__sans_texte")],
                       cwd=build, check=True)
        e2, a2 = chevauchements(png, build / f"{nom}__sans_texte.png")
        if tolere and nom in tolere:
            avert += [f"toléré ({tolere[nom]}) : {x}" for x in e2]
        else:
            erreurs += e2
        avert += a2
    else:
        avert.append("contrôle des chevauchements impossible (version sans texte non compilée)")
    if erreurs:
        return nom, False, erreurs + [f"(avertissement) {x}" for x in avert]
    return nom, True, avert


def compiler(figures, dossier_figures, noms=None, xlab=None, extra="", jobs=3, tolere=None):
    dossier_figures = Path(dossier_figures).resolve()
    build = dossier_figures / "build"
    sortie = dossier_figures / "images"
    noms = noms or list(figures)
    inconnus = [n for n in noms if n not in figures]
    if inconnus:
        raise SystemExit(f"Figures inconnues : {inconnus}")
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        res = list(pool.map(lambda n: compiler_un(n, figures[n], build, sortie, xlab, extra, tolere), noms))
    ok = 0
    for nom, bon, msgs in res:
        ok += bon
        if not bon:
            print(f"✗ {nom} : " + " | ".join(msgs))
        elif msgs:
            print(f"⚠ {nom} : " + " ; ".join(msgs))
    print(f"{ok}/{len(noms)} figure(s) produite(s) dans {sortie}")
    return [n for n, bon, _ in res if bon]


def planche(dossier_figures, noms, par=9):
    """Planches de relecture des figures produites (taille réelle d'affichage ÷ 1)."""
    from PIL import Image, ImageDraw, ImageFont
    dossier_figures = Path(dossier_figures)
    for vieux in dossier_figures.glob("planche_nouvelles_*.png"):
        vieux.unlink()
    try:
        police = ImageFont.truetype("arialbd.ttf", 16)
    except OSError:
        police = ImageFont.load_default()
    imgs = [(n, dossier_figures / "images" / f"{n}.png") for n in noms if (dossier_figures / "images" / f"{n}.png").exists()]
    for k in range(0, len(imgs), par):
        lot = imgs[k:k + par]
        vignettes = []
        for n, p in lot:
            im = Image.open(p).convert("RGB")
            # taille d'affichage sur le site : moitié des pixels
            im = im.resize((max(1, im.width // 2), max(1, im.height // 2)), Image.LANCZOS)
            vignettes.append((n, im))
        cols = 3
        larg = max(v.width for _, v in vignettes) + 24
        haut = max(v.height for _, v in vignettes) + 40
        lignes = (len(vignettes) + cols - 1) // cols
        feuille = Image.new("RGB", (cols * larg + 16, lignes * haut + 16), (226, 230, 238))
        d = ImageDraw.Draw(feuille)
        for i, (n, v) in enumerate(vignettes):
            x = 16 + (i % cols) * larg
            y = 16 + (i // cols) * haut
            d.text((x, y), n, fill=(27, 60, 142), font=police)
            feuille.paste(v, (x, y + 24))
        feuille.save(dossier_figures / f"planche_nouvelles_{k // par + 1:02d}.png")
    print(f"{(len(imgs) + par - 1) // par} planche(s) de relecture dans {dossier_figures}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    jobs = 3
    if "--jobs" in args:
        k = args.index("--jobs")
        jobs = int(args[k + 1])
        del args[k:k + 2]
    avec_planche = "--planche" in args
    args = [a for a in args if a != "--planche"]
    dossier = Path(args[0]).resolve()
    mod = charger(dossier)
    noms = args[1:] or list(mod.FIGURES)
    produits = compiler(mod.FIGURES, dossier / "figures", noms, getattr(mod, "XLAB", None),
                        getattr(mod, "PREAMBULE_EXTRA", ""), jobs, getattr(mod, "TOLERE", None))
    if avec_planche:
        planche(dossier / "figures", produits)
    if len(produits) < len(noms):
        sys.exit(1)


if __name__ == "__main__":
    main()
