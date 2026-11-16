# -*- coding: utf-8 -*-
"""Fiches de calcul à imprimer (PDF) avec leur corrigé posé.

Pour chaque fiche de FICHES :
  - public/ressources-gratuites/fiches-a-imprimer/<slug>/<slug>-fiche-<k>.pdf
    et <slug>-corrige-<k>.pdf (A4, LuaLaTeX + TikZ, polices des livres) ;
  - contenu/fiches/<slug>/formulaire.md (page de la rubrique, générée ici) ;
  - contenu/fiches/<slug>/figures/images/ : aperçu de la fiche et du corrigé,
    vignette de la carte.

Les nombres sont tirés au hasard (graine fixe : mêmes fiches à chaque
lancement) dans les limites du programme de la classe ; résultats, retenues,
quotients et restes sont calculés par contenu/operations/poser.py, qui vérifie
chaque calcul.

    python contenu/fiches/generer_fiches.py [slug …]
"""
import json
import random
import re
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ICI = Path(__file__).resolve().parent
FRONT = ICI.parents[1]
sys.path.insert(0, str(ICI.parent / "operations"))
sys.path.insert(0, str(FRONT / "cours" / "format_v1" / "outils"))
import poser  # noqa: E402
from figures_livre import PREAMBULE  # noqa: E402

PUBLIC = FRONT / "public" / "ressources-gratuites" / "fiches-a-imprimer"
URL = "/ressources-gratuites/fiches-a-imprimer"
BUILD = ICI / "_build"
DATE = "2026-11-16"

LARGEUR, HAUTEUR = 19.0, 27.2          # zone utile de la page (cm)
HAUT_TETE = 4.1                         # en-tête (titre, nom, consigne)
PIED = .7
LETTRES = "abcdefghijklmnop"


# --------------------------------------------------------------- tirages
def colonnes(n):
    return [int(c) for c in str(n)][::-1]


def retenue_addition(termes):
    c, out = 0, False
    for r in range(max(len(str(t)) for t in termes)):
        s = sum(colonnes(t)[r] if r < len(str(t)) else 0 for t in termes) + c
        c = s // 10
        out = out or c > 0
    return out


def emprunt(a, b):
    A, B = colonnes(a), colonnes(b)
    return any(A[r] < (B[r] if r < len(B) else 0) for r in range(len(A)))


def tirer(rng, n, fabrique, ok):
    out, essais = [], 0
    while len(out) < n:
        essais += 1
        assert essais < 100000
        x = fabrique(rng)
        if ok(x) and x not in out:
            out.append(x)
    return out


def additions(rng, n, plages, total_max, trois=0):
    def fab(r):
        nb = 3 if len(out_trois) < trois else 2
        return tuple(r.randint(*plages[i % len(plages)]) for i in range(nb))
    out_trois = []
    res = []
    while len(res) < n:
        t = tirer(rng, 1, fab, lambda t: sum(t) <= total_max and retenue_addition(t) and t not in res)[0]
        if len(t) == 3:
            out_trois.append(t)
        res.append(t)
    rng.shuffle(res)
    return res


def soustractions(rng, n, plage_a, plage_b, zeros=2):
    def a_zero(a):
        return "0" in str(a)[1:]
    res = tirer(rng, zeros, lambda r: (r.randint(*plage_a), r.randint(*plage_b)),
                lambda t: t[0] > t[1] and emprunt(*t) and a_zero(t[0]))
    res += tirer(rng, n - zeros, lambda r: (r.randint(*plage_a), r.randint(*plage_b)),
                 lambda t: t[0] > t[1] and emprunt(*t) and not a_zero(t[0]) and t not in res)
    rng.shuffle(res)
    return res


def multiplications(rng, n, plage_a, plage_b):
    def ok(t):
        a, b = t
        return b % 10 != 0 and str(b).count("1") == 0 and any(int(c) * (b % 10) >= 10 for c in str(a))
    return tirer(rng, n, lambda r: (r.randint(*plage_a), r.randint(*plage_b)), ok)


def divisions(rng, n, plage_q, plage_b, zero_interne=2):
    """Dividende = b × q + r ; quelques quotients avec un zéro interne."""
    def fab(r):
        b = r.randint(*plage_b)
        return (b * r.randint(*plage_q) + r.randint(0, b - 1), b)

    def zero(t):
        q = t[0] // t[1]
        return "0" in str(q)[1:-1] or (len(str(q)) == 2 and False)
    res = tirer(rng, zero_interne, fab, lambda t: "0" in str(t[0] // t[1])[1:])
    res += tirer(rng, n - zero_interne, fab, lambda t: "0" not in str(t[0] // t[1]) and t not in res)
    rng.shuffle(res)
    return res


# --------------------------------------------------------------- fiches
# type, classe, titre de l'opération, consigne, colonnes × lignes, tirage
FICHES = [
    {
        "slug": "additions-posees-ce1", "classe": "CE1", "section": "ce1", "op": "addition",
        "nom": "Additions posées", "grille": (3, 4), "ordre": 1,
        "consigne": "Pose chaque addition en colonnes sur le quadrillage, puis calcule-la. Aligne bien les unités sous les unités.",
        "tirage": lambda r: additions(r, 12, [(12, 89), (105, 489)], 999),
        "limites": "nombres jusqu’à 1 000, avec retenues",
        "chapitres": ["ce1/additionner-en-colonnes", "cp/addition-posee-alignement-et-retenue"],
    },
    {
        "slug": "additions-posees-ce2", "classe": "CE2", "section": "ce2", "op": "addition",
        "nom": "Additions posées", "grille": (3, 4), "ordre": 2,
        "consigne": "Pose chaque addition en colonnes sur le quadrillage, puis calcule-la. N’oublie pas les retenues.",
        "tirage": lambda r: additions(r, 12, [(1050, 5890), (248, 3970), (35, 980)], 9999, trois=3),
        "limites": "nombres jusqu’à 10 000, deux ou trois termes",
        "chapitres": ["ce2/additionner-en-colonnes"],
    },
    {
        "slug": "soustractions-posees-ce1", "classe": "CE1", "section": "ce1", "op": "soustraction",
        "nom": "Soustractions posées", "grille": (3, 4), "ordre": 3,
        "consigne": "Pose chaque soustraction en colonnes, le plus grand nombre en haut, puis calcule-la.",
        "tirage": lambda r: soustractions(r, 12, (120, 980), (15, 489)),
        "limites": "nombres jusqu’à 1 000, avec retenues et zéros",
        "chapitres": ["ce1/soustraire-en-colonnes"],
    },
    {
        "slug": "soustractions-posees-ce2", "classe": "CE2", "section": "ce2", "op": "soustraction",
        "nom": "Soustractions posées", "grille": (3, 4), "ordre": 4,
        "consigne": "Pose chaque soustraction en colonnes, le plus grand nombre en haut, puis calcule-la.",
        "tirage": lambda r: soustractions(r, 12, (1200, 9800), (150, 4890), zeros=3),
        "limites": "nombres jusqu’à 10 000, avec retenues et zéros",
        "chapitres": ["ce2/soustraire-en-colonnes"],
    },
    {
        "slug": "multiplications-posees-ce2", "classe": "CE2", "section": "ce2", "op": "multiplication",
        "nom": "Multiplications posées", "grille": (3, 4), "ordre": 5,
        "consigne": "Pose chaque multiplication en colonnes, le plus grand nombre en haut, puis calcule-la avec les retenues.",
        "tirage": lambda r: multiplications(r, 12, (23, 489), (3, 9)),
        "limites": "par un nombre à un chiffre",
        "chapitres": ["ce2/multiplier-en-colonnes-par-un-chiffre"],
    },
    {
        "slug": "multiplications-posees-cm1", "classe": "CM1", "section": "cm1", "op": "multiplication",
        "nom": "Multiplications posées", "grille": (3, 3), "ordre": 6,
        "consigne": "Pose chaque multiplication en colonnes. N’oublie pas le zéro de décalage sur la deuxième ligne.",
        "tirage": lambda r: multiplications(r, 9, (124, 879), (23, 98)),
        "limites": "par un nombre à deux chiffres",
        "chapitres": ["ce2/multiplier-en-colonnes-par-deux-chiffres", "cm1/multiplier-des-entiers"],
    },
    {
        "slug": "divisions-posees-cm1", "classe": "CM1", "section": "cm1", "op": "division",
        "nom": "Divisions posées", "grille": (3, 3), "ordre": 7,
        "consigne": "Pose chaque division dans une potence et écris le quotient q et le reste r. Vérifie : diviseur × quotient + reste = dividende.",
        "tirage": lambda r: divisions(r, 9, (104, 980), (3, 9)),
        "limites": "par un nombre à un chiffre, avec reste",
        "chapitres": ["cm1/diviser-partages-et-restes", "cm2/diviser-et-interpreter-le-quotient"],
    },
    {
        "slug": "divisions-posees-6e", "classe": "6e", "section": "6e", "op": "division",
        "nom": "Divisions posées", "grille": (2, 3), "ordre": 8,
        "consigne": "Pose chaque division dans une potence et écris le quotient q et le reste r. Si tu en as besoin, écris d’abord la table des multiples du diviseur.",
        "tirage": lambda r: divisions(r, 6, (102, 489), (12, 48)),
        "limites": "par un nombre à deux chiffres",
        "chapitres": ["6e/diviser-et-interpreter-un-partage"],
    },
]
NB_FICHES = 2       # fiches par page (graines 1, 2…)


# --------------------------------------------------------------- calculs et dessins
def calcul(op, t):
    """(écriture en ligne, résultat en texte, code TikZ du corrigé posé)."""
    if op == "addition":
        s = sum(t)
        return " + ".join(poser.milliers(x) for x in t), poser.milliers(s), poser.addition([str(x) for x in t])
    if op == "soustraction":
        a, b = t
        return f"{poser.milliers(a)} - {poser.milliers(b)}", poser.milliers(a - b), poser.soustraction(str(a), str(b), methode="cassage")
    if op == "multiplication":
        a, b = t
        code, res = poser.multiplication(str(a), str(b), retenues=b < 10, notes=False)
        assert int(res.replace(",", "")) == a * b
        return f"{poser.milliers(a)} \\times {poser.milliers(b)}", poser.milliers(a * b), code
    a, b = t
    code, qtxt, reste = poser.division(str(a), b, egalite="")
    q = a // b
    assert int(qtxt) == q and reste == a - b * q
    return f"{poser.milliers(a)} \\div {b}", f"q = {poser.milliers(q)}, r = {a - b * q}", code


NOMBRE = re.compile(r"\((-?[\d.]+),(-?[\d.]+)\)")


def boite_englobante(code):
    """Boîte approximative d'un dessin de poser.py (coordonnées écrites dans le code)."""
    xs, ys = [], []
    for m in NOMBRE.finditer(code):
        xs.append(float(m.group(1)))
        ys.append(float(m.group(2)))
    return min(xs) - .2, max(xs) + .25, min(ys) - .2, max(ys) + .35


def place(code, cx, cy, l, h, echelle_max=1.0):
    """Dessin centré dans le rectangle (cx, cy) de taille l × h, réduit si besoin."""
    x0, x1, y0, y1 = boite_englobante(code)
    k = min(echelle_max, l / (x1 - x0), h / (y1 - y0))
    corps = code.replace("\\begin{tikzpicture}\n", "").replace("\n\\end{tikzpicture}", "")
    dx = cx - k * (x0 + x1) / 2
    dy = cy - k * (y0 + y1) / 2
    return [r"\begin{scope}[shift={(%s,%s)},scale=%s,every node/.append style={scale=%s}]" % (
        poser.f(dx), poser.f(dy), poser.f(k), poser.f(k)), corps, r"\end{scope}"]


def quadrillage(x0, y0, l, h, pas=.5):
    """Petits carreaux (tracés un à un depuis le coin : pas de décalage)."""
    L = []
    n, m = int(l / pas + 1e-9), int(h / pas + 1e-9)
    l, h = n * pas, m * pas
    for i in range(n + 1):
        L.append(r"\draw[otNavy!18,line width=.35pt] (%s,%s) -- (%s,%s);" % (poser.f(x0 + i * pas), poser.f(y0), poser.f(x0 + i * pas), poser.f(y0 - h)))
    for j in range(m + 1):
        L.append(r"\draw[otNavy!18,line width=.35pt] (%s,%s) -- (%s,%s);" % (poser.f(x0), poser.f(y0 - j * pas), poser.f(x0 + l), poser.f(y0 - j * pas)))
    return L, l, h


def page(fiche, k, calculs, corrige):
    nc, nl = fiche["grille"]
    L = [r"\path (0,0) rectangle (%s,%s);" % (poser.f(LARGEUR), poser.f(-HAUTEUR))]
    # en-tête
    L.append(r"\node[anchor=north west,inner sep=0pt,font=\otMedium\fontsize{11}{13}\selectfont\bfseries,text=otNavy] at (0,0) {OptiTAB};")
    L.append(r"\node[anchor=north west,inner sep=0pt,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted] at (1.75,-.06) {Fiche de calcul gratuite};")
    L.append(r"\node[anchor=north east,inner sep=4pt,font=\otMedium\fontsize{10}{12}\selectfont\bfseries,text=white,fill=otNavy,rounded corners=3pt] at (%s,.06) {%s};" % (poser.f(LARGEUR), fiche["classe"]))
    titre = "%s · Fiche %d%s" % (fiche["nom"], k, " · Corrigé" if corrige else "")
    L.append(r"\node[anchor=north west,inner sep=0pt,font=\otMedium\fontsize{17}{20}\selectfont\bfseries,text=otInk] at (0,-.85) {%s};" % titre)
    if corrige:
        L.append(r"\node[anchor=north west,inner sep=0pt,font=\otRegular\fontsize{10}{13}\selectfont,text=otInk,text width=%scm] at (0,-1.95) {Les calculs posés et leurs résultats en vert. %s};" % (
            poser.f(LARGEUR), "Les soustractions sont posées par cassage (méthode par échanges) ; la méthode par compensation donne les mêmes résultats." if fiche["op"] == "soustraction" else
            "On vérifie chaque division : diviseur × quotient + reste = dividende, et le reste est plus petit que le diviseur." if fiche["op"] == "division" else
            "Pense à vérifier avec un ordre de grandeur."))
    else:
        L.append(r"\node[anchor=north west,inner sep=0pt,font=\otRegular\fontsize{10.5}{13}\selectfont,text=otInk] at (0,-1.95) {Prénom : \rule[-1pt]{5.2cm}{.4pt}\qquad Date : \rule[-1pt]{3cm}{.4pt}\qquad Score : \rule[-1pt]{1.1cm}{.4pt} / %d};" % len(calculs))
        L.append(r"\node[anchor=north west,inner sep=6pt,font=\otRegular\fontsize{10}{13}\selectfont,text=otInk,fill=otSky,rounded corners=4pt,text width=%scm] at (0,-2.75) {%s};" % (poser.f(LARGEUR - .25), fiche["consigne"]))
    # cases
    ecart = .35
    lc = (LARGEUR - (nc - 1) * ecart) / nc
    hc = (HAUTEUR - HAUT_TETE - PIED - (nl - 1) * ecart) / nl
    for i, (enligne, res, code) in enumerate(calculs):
        c, li = i % nc, i // nc
        x, y = c * (lc + ecart), -HAUT_TETE - li * (hc + ecart)
        L.append(r"\draw[otNavy!45,line width=.6pt,rounded corners=4pt] (%s,%s) rectangle (%s,%s);" % (poser.f(x), poser.f(y), poser.f(x + lc), poser.f(y - hc)))
        lettre = LETTRES[i]
        texte = r"$%s = %s$" % (enligne, r"\textcolor{otGreenDark}{%s}" % res if corrige else r"\ldots\ldots")
        if fiche["op"] == "division":
            a, b = calculs_bruts[i]
            if corrige:
                texte = r"$%s$ : \textcolor{otGreenDark}{$q = %s$ ; $r = %d$}" % (enligne, poser.milliers(a // b), a % b)
            else:
                texte = r"$%s$ : $q = \ldots\ldots$ ; $r = \ldots$" % enligne
        L.append(r"\node[anchor=north west,inner sep=0pt,font=\fontsize{12}{14}\selectfont] at (%s,%s) {\textcolor{otNavy}{\otMedium\bfseries %s)}\enspace %s};" % (
            poser.f(x + .3), poser.f(y - .3), lettre, texte))
        zone_y = y - 1.0
        zone_h = hc - 1.25
        if corrige:
            L += place(code, x + lc / 2, zone_y - zone_h / 2, lc - .6, zone_h - .2)
            if fiche["op"] == "division":
                a, b = calculs_bruts[i]
                L.append(r"\node[anchor=south,inner sep=0pt,font=\fontsize{9.5}{11}\selectfont,text=otNavy] at (%s,%s) {$%s = %d \times %s + %d$};" % (
                    poser.f(x + lc / 2), poser.f(y - hc + .2), poser.milliers(a), b, poser.milliers(a // b), a % b))
        else:
            q, ql, qh = quadrillage(x + .3, zone_y, lc - .6, zone_h - .1)
            L += q
    # pied
    L.append(r"\node[anchor=south,inner sep=0pt,font=\otRegular\fontsize{8}{10}\selectfont,text=otMuted] at (%s,%s) {Fiche gratuite OptiTAB · %s · www.optitab.net%s/%s/};" % (
        poser.f(LARGEUR / 2), poser.f(-HAUTEUR), fiche["limites"], URL, fiche["slug"]))
    return "\\begin{tikzpicture}\n" + "\n".join(L) + "\n\\end{tikzpicture}"


calculs_bruts = []


def document(pages):
    tete = PREAMBULE.replace(r"\documentclass[border=6pt]{standalone}",
                             "\\documentclass[11pt]{article}\n\\usepackage[a4paper,margin=10mm,top=11mm]{geometry}")
    # Aucun mot coupé en fin de ligne (fiches pour enfants).
    return (tete + poser.PREAMBULE_EXTRA + "\n\\pagestyle{empty}\n\\setlength{\\parindent}{0pt}\n\\hyphenpenalty=10000\n\\exhyphenpenalty=10000\n\\begin{document}\n"
            + "\n\\newpage\n".join(pages) + "\n\\end{document}\n")


def compiler(nom, tex, sortie):
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / f"{nom}.tex").write_text(tex, encoding="utf-8")
    r = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", f"{nom}.tex"],
                       cwd=BUILD, capture_output=True, text=True, encoding="utf-8", errors="replace")
    pdf = BUILD / f"{nom}.pdf"
    if r.returncode != 0 or not pdf.exists():
        log = (BUILD / f"{nom}.log").read_text(encoding="utf-8", errors="replace")
        erreurs = [l for l in log.splitlines() if l.startswith("!")]
        raise SystemExit(f"{nom} : échec LuaLaTeX {erreurs[:3]}")
    sortie.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, sortie)
    return sortie


def png(pdf, sortie, largeur=900):
    sortie.parent.mkdir(parents=True, exist_ok=True)
    base = str(sortie.with_suffix(""))
    subprocess.run(["pdftocairo", "-png", "-singlefile", "-f", "1", "-l", "1", "-scale-to-x", str(largeur), "-scale-to-y", "-1", str(pdf), base], check=True)
    return sortie


def carte(apercu, sortie):
    from PIL import Image
    im = Image.open(apercu).convert("RGB")
    w = im.size[0]
    h = int(w * 10 / 16)
    im.crop((0, 0, w, h)).resize((720, 450), Image.LANCZOS).save(sortie, optimize=True)


# --------------------------------------------------------------- page de la rubrique
def ecrire_page(fiche, series):
    slug = fiche["slug"]
    classe = fiche["classe"]
    nom = fiche["nom"]
    nom_min = nom[0].lower() + nom[1:]
    op = fiche["op"]
    n = len(series[0])
    figs = [
        {"nom": "apercu_fiche_1", "alt": f"Aperçu de la fiche 1 « {nom} {classe} » : {n} calculs à poser sur des quadrillages, avec prénom, date et score."},
        {"nom": "apercu_corrige_1", "alt": f"Aperçu du corrigé de la fiche 1 : les {n} calculs posés avec leurs résultats en vert."},
        {"nom": f"carte_{slug}", "alt": f"Aperçu : haut de la fiche « {nom} {classe} » à imprimer.", "carte": True},
    ]
    tel = []
    for k in range(1, len(series) + 1):
        tel.append({"titre": f"Fiche {k}", "pdf": f"{URL}/{slug}/{slug}-fiche-{k}.pdf", "corrige": f"{URL}/{slug}/{slug}-corrige-{k}.pdf"})
    info = {
        "slug": slug,
        "titre": f"{nom} {classe} : fiches à imprimer avec corrigé",
        "titreCourt": f"{nom} {classe}",
        "titreSeo": f"{nom} {classe} à imprimer (PDF) avec corrigé",
        "description": f"Fiches gratuites de {nom_min} {classe} à imprimer en PDF ({fiche['limites']}), avec le corrigé posé de chaque calcul.",
        "chapo": f"Des fiches de {nom_min} pour le {classe}, prêtes à imprimer : {n} calculs par fiche ({fiche['limites']}), un quadrillage pour poser chaque calcul, et un corrigé où chaque opération est posée en entier.",
        "resume": f"{len(series)} fiches PDF et leurs corrigés",
        "vignette": f"carte_{slug}",
        "theme": nom,
        "niveaux": ["Collège" if classe == "6e" else "Primaire"],
        "section": fiche["section"],
        "ordre": fiche["ordre"],
        "publie": DATE,
        "modifie": DATE,
        "motsCles": [f"{nom_min} {classe}", f"{nom_min} {classe} à imprimer", f"fiche {nom_min} {classe}", f"exercices {nom_min} {classe}", f"{nom_min} {classe} pdf", f"{nom_min} avec corrigé", f"fiche de calcul {classe}"],
        "figures": figs,
        "telechargements": tel,
        "liees": [f"operations/{op}-posee"],
        "chapitresLies": fiche["chapitres"],
        "faq": [
            [f"Les fiches de {nom_min} {classe} sont-elles gratuites ?", "Oui. Les fiches et leurs corrigés sont gratuits, sans inscription : il suffit de télécharger le PDF et de l’imprimer."],
            ["Comment imprimer la fiche ?", "Cliquez sur « Fiche » pour ouvrir le PDF, puis imprimez-le en A4, à 100 % (taille réelle), pour que les carreaux mesurent 5 mm. Le corrigé est un PDF séparé, à garder pour la correction."],
            [f"Que contient une fiche de {nom_min} {classe} ?", f"{n} calculs ({fiche['limites']}), adaptés au programme du {classe}, avec un quadrillage pour poser chaque opération, une ligne pour le prénom, la date et le score."],
            ["Comment utiliser le corrigé ?", "Le corrigé montre chaque calcul posé en entier, avec les retenues et le résultat en vert. Comparez colonne par colonne pour trouver où se trouve une erreur, plutôt que de regarder seulement le résultat."],
        ],
    }
    assert len(info["description"]) <= 160, (slug, len(info["description"]))
    L = ["<!-- optitab:1 -->", "[TELECHARGEMENTS]", "",
         f"## I. Ce que contiennent les fiches {{{info['niveaux'][0]}}}", "",
         f"Chaque fiche propose **{n} {nom_min}** ({fiche['limites']}), choisies pour le niveau **{classe}**. "
         "Chaque calcul a son quadrillage à petits carreaux pour être posé proprement, et le corrigé montre toutes les étapes.", "",
         "[IMAGE_1]", "",
         "::: conseil Bien imprimer",
         "Imprimez en A4, à **100 %** (taille réelle) : les carreaux mesurent alors $5$ mm, comme dans un cahier.",
         ":::", ""]
    for k, serie in enumerate(series, 1):
        L += [f"## {['II', 'III', 'IV', 'V'][k - 1]}. Le corrigé de la fiche {k} {{{info['niveaux'][0]}}}", ""]
        if k == 1:
            L += ["[IMAGE_2]", ""]
        if op == "division":
            L += ["| Calcul | Quotient | Reste |", "|---|---|---|"]
            for i, (a, b) in enumerate(serie):
                L.append(f"| {LETTRES[i]}) ${poser.milliers(a)} \\div {b}$ | ${poser.milliers(a // b)}$ | ${a % b}$ |")
        else:
            L += ["| Calcul | Résultat |", "|---|---|"]
            for i, t in enumerate(serie):
                enligne, res, _ = calcul(op, t)
                L.append(f"| {LETTRES[i]}) ${enligne}$ | ${res}$ |")
        L.append("")
    L += [f"## {['II', 'III', 'IV', 'V'][len(series)]}. Pour réussir {{{info['niveaux'][0]}}}", "",
          {"addition": "::: retenir Les points clés\n- Aligner les unités sous les unités.\n- Commencer par la colonne des unités, à droite.\n- Écrire la retenue en haut de la colonne suivante.\n- Vérifier avec un ordre de grandeur.\n:::",
           "soustraction": "::: retenir Les points clés\n- Le plus grand nombre en haut, unités sous unités.\n- Si le chiffre du haut est trop petit, utiliser une retenue (cassage ou compensation).\n- Vérifier : résultat + nombre retiré = nombre de départ.\n:::",
           "multiplication": "::: retenir Les points clés\n- Le nombre le plus long en haut, alignés à droite.\n- Multiplier, puis ajouter la retenue.\n- Pour le chiffre des dizaines, écrire d’abord le zéro de décalage.\n- Vérifier avec un ordre de grandeur.\n:::",
           "division": "::: retenir Les points clés\n- Prendre le premier morceau du dividende qui contient le diviseur et compter les chiffres du quotient.\n- Chaque reste doit être plus petit que le diviseur.\n- Ne pas oublier les zéros au quotient.\n- Vérifier : diviseur × quotient + reste = dividende.\n:::"}[op], "",
          "La méthode complète, avec des schémas étape par étape, est dans la page liée en bas de page."]
    d = ICI / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "formulaire.md").write_bytes(("---\n" + json.dumps(info, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L) + "\n").encode("utf-8"))


def generer(fiche):
    global calculs_bruts
    slug = fiche["slug"]
    series = []
    images = ICI / slug / "figures" / "images"
    for k in range(1, NB_FICHES + 1):
        rng = random.Random(f"{slug}-{k}")
        serie = fiche["tirage"](rng)
        nc, nl = fiche["grille"]
        assert len(serie) == nc * nl, (slug, len(serie))
        series.append(serie)
        calculs_bruts = serie
        calculs = [calcul(fiche["op"], t) for t in serie]
        for corrige in (False, True):
            nom = f"{slug}-{'corrige' if corrige else 'fiche'}-{k}"
            pdf = compiler(nom, document([page(fiche, k, calculs, corrige)]), PUBLIC / slug / f"{nom}.pdf")
            if k == 1:
                png(pdf, images / f"apercu_{'corrige' if corrige else 'fiche'}_1.png")
    carte(images / "apercu_fiche_1.png", images / f"carte_{slug}.png")
    ecrire_page(fiche, series)
    print(f"{slug} : {NB_FICHES} fiches, {NB_FICHES} corrigés")


if __name__ == "__main__":
    choix = sys.argv[1:]
    for fiche in FICHES:
        if not choix or fiche["slug"] in choix:
            generer(fiche)
    shutil.rmtree(BUILD, ignore_errors=True)
