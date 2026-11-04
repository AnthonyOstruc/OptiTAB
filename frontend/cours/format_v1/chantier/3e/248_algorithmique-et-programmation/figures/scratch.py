# -*- coding: utf-8 -*-
r"""Blocs Scratch 3 dessinés en TikZ (style des livres OptiTAB) + traduction Python exécutable.

Module réutilisable (notion 248 « Algorithmique et programmation », sujets type brevet…).
Un script est décrit UNE fois, par des objets Python ; le même objet sert à :

  - dessiner les blocs (formes et couleurs officielles des familles, encoches,
    chapeaux, blocs C imbriqués, menus, ovales, hexagones), texte mesuré avec les
    métriques réelles de la police (Montserrat Medium) : aucun texte coupé ;
  - TRADUIRE le script en Python (`traduire`) et l'EXÉCUTER (`executer`) :
    valeurs dites, variables, positions et tracés du lutin.

Utilisation (dans figures.py, compilé par outils/figures_livre.py) :

    from scratch import *
    S = [Drapeau(), Mettre("x", 3), Repeter(4, [Ajouter("x", 3)]), Dire(V("x"))]
    FIGURES["mon_script"] = figure_scripts([("", S)])
    r = executer({"Lutin": [S]});  r.dits  ->  [12]

Familles (couleurs Scratch 3) : evenement (jaune), controle (orange), operateur (vert),
variable (orange foncé), mouvement (bleu), apparence (violet, « dire »), capteur
(bleu clair, « demander », « réponse »), stylo (vert foncé), perso (rose, blocs personnalisés).

Trous (scripts à compléter) : Trou("A", solution) ; dans l'énoncé, case blanche
pointillée marquée A ; avec corrige=True, la solution est écrite en vert (cadre vert).
Bloc surligné (ajouté ou modifié dans un corrigé) : argument hl=True → contour vert épais
(seulement si corrige=True).

PREAMBULE_EXTRA (couleurs des familles) : à ajouter au PREAMBULE_EXTRA de figures.py.
Contrôle des chevauchements : les textes sont écrits sur le fond coloré des blocs (le
détecteur de figures_livre.py les prend pour des traits) ; la variable d'environnement
SCRATCH_CONTROLE=1 produit une version « fonds blancs, texte noir » dans laquelle le
détecteur vérifie réellement qu'aucun texte ne touche un contour (script controle_scratch.py).
"""
import math
import os
import random
import subprocess

# ---------------------------------------------------------------- couleurs Scratch 3
FAMILLES = {
    # nom : (fond, contour, menu)
    "evenement": ("FFBF00", "CC9900", "E6AC00"),
    "controle": ("FFAB19", "CF8B17", "EC9C13"),
    "operateur": ("59C059", "389438", "46B946"),
    "variable": ("FF8C1A", "DB6E00", "E87D17"),
    "mouvement": ("4C97FF", "3373CC", "4280D7"),
    "apparence": ("9966FF", "774DCB", "855CD6"),
    "capteur": ("5CB1D6", "2E8EB8", "47A8D1"),
    "stylo": ("0FBD8C", "0B8E69", "0DA57A"),
    "perso": ("FF6680", "FF3355", "FF4D6A"),
}
PREAMBULE_SCRATCH = "\n".join(
    r"\definecolor{scr%s}{HTML}{%s}\definecolor{scr%sB}{HTML}{%s}\definecolor{scr%sM}{HTML}{%s}"
    % (k, f, k, b, k, m) for k, (f, b, m) in FAMILLES.items()) + r"""
\definecolor{scrTexteEntree}{HTML}{575E75}
\definecolor{scrDrapeau}{HTML}{4CBF56}\definecolor{scrDrapeauB}{HTML}{45993D}
\newcommand{\scrF}{\otMedium\fontsize{9}{11}\selectfont}
\newcommand{\scrT}{\otMedium\bfseries\fontsize{8.5}{10}\selectfont}
"""
CONTROLE = os.environ.get("SCRATCH_CONTROLE") == "1"

# ---------------------------------------------------------------- dimensions (pt)
F = 9.0            # taille du texte des blocs
H_LIGNE = 24.0     # hauteur minimale d'une ligne de bloc
VPAD = 4.0         # marge verticale autour de l'élément le plus haut
PADL, PADR, GAP = 7.0, 7.0, 4.0
H_ENT = 16.0       # hauteur d'une case (entrée, menu, variable)
NX, NW, ND = 9.0, 20.0, 3.5     # encoche : décalage, largeur, profondeur
ARM = 13.0         # bras gauche d'un bloc C
HB = 13.0          # bras inférieur d'un bloc C
H_VIDE = 16.0      # intérieur vide d'un bloc C
CAP = 11.0         # hauteur du chapeau (événements)
HW = 70.0          # largeur de la bosse du chapeau
RC = 2.6           # arrondi des coins
BASE = 0.35 * F    # du milieu de la ligne à la ligne de base du texte

_CORR = [False]    # mode corrigé pendant la construction d'une figure


def _n(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def _pt(x, y):
    return "(%s,%s)" % (_n(x), _n(y))


# ---------------------------------------------------------------- mesure des textes
_POLICES = {}


def _police(graisse="Medium"):
    if graisse not in _POLICES:
        from fontTools.ttLib import TTFont
        nom = "Montserrat-%s.otf" % graisse
        try:
            chemin = subprocess.run(["kpsewhich", nom], capture_output=True, text=True).stdout.strip()
        except OSError:
            chemin = ""
        if not chemin:
            chemin = r"C:/Users/SWEELCO-AT/AppData/Local/Programs/MiKTeX/fonts/opentype/public/montserrat/" + nom
        f = TTFont(chemin)
        _POLICES[graisse] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    return _POLICES[graisse]


def largeur(txt, taille=F, graisse="Medium"):
    cmap, hmtx, upem = _police(graisse)
    tot = 0
    for c in txt:
        g = cmap.get(ord(c))
        if g is None:
            raise ValueError("caractère absent de Montserrat : %r dans %r" % (c, txt))
        tot += hmtx[g][0]
    return tot / upem * taille * 1.02 + 0.4   # petite marge (crénage, arrondis)


def _tex(s):
    s = str(s).replace("'", "’")
    for a, b in (("\\", r"\textbackslash{}"), ("{", r"\{"), ("}", r"\}"), ("%", r"\%"), ("#", r"\#"),
                 ("&", r"\&"), ("_", r"\_"), ("$", r"\$"), ("~", r"\textasciitilde{}"), ("^", r"\^{}")):
        s = s.replace(a, b)
    return s


def nombre_fr(v):
    """3 -> '3' ; 0.5 -> '0,5' ; -4 -> '−4' (texte affiché dans une case)."""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int, float)):
        if isinstance(v, float) and v.is_integer():
            v = int(v)
        s = str(v).replace(".", ",")
        return s.replace("-", "−")
    return str(v)


# ================================================================ éléments de ligne
class Elem:
    """Élément d'une ligne : mesure() -> (largeur, hauteur) ; dessin(x, ym) -> commandes TikZ."""
    forme = "rond"   # forme du bord (pour l'espacement intérieur d'un reporter)

    def py(self):
        raise NotImplementedError


class Texte(Elem):
    forme = "texte"

    def __init__(self, s, couleur="white", taille=F):
        self.s, self.couleur, self.taille = s, couleur, taille

    def py(self):
        return repr(self.s)

    def mesure(self):
        return largeur(self.s.replace("'", "’"), self.taille), F * 0.75

    def dessin(self, x, ym):
        coul = "black" if CONTROLE else self.couleur
        if self.taille == F:
            police, dy = r"\scrF", BASE
        else:
            police = r"\otMedium\fontsize{%s}{%s}\selectfont" % (_n(self.taille), _n(self.taille + 2))
            dy = 0.35 * self.taille
        return [r"\node[anchor=base west,inner sep=0pt,text=%s,font=%s] at %s {%s};"
                % (coul, police, _pt(x, ym - dy), _tex(self.s))]


class Icone(Elem):
    """Drapeau vert, flèches de rotation (gauche = ↺, droite = ↻)."""
    forme = "texte"

    def __init__(self, nom):
        self.nom = nom

    def mesure(self):
        return (12.0, 12.0) if self.nom == "drapeau" else (10.0, 10.0)

    def dessin(self, x, ym):
        if self.nom == "drapeau":
            return [r"\draw[scrDrapeauB,line width=1.1pt,line cap=round] %s -- %s;" % (_pt(x + 1.5, ym - 6), _pt(x + 1.5, ym + 5.5)),
                    r"\draw[scrDrapeauB,fill=scrDrapeau,line width=.6pt,line join=round] %s .. controls %s and %s .. %s"
                    r" -- %s .. controls %s and %s .. %s -- cycle;"
                    % (_pt(x + 1.5, ym + 5.5), _pt(x + 5, ym + 7.5), _pt(x + 7.5, ym + 3.5), _pt(x + 11.5, ym + 5.5),
                       _pt(x + 11.5, ym - 0.5), _pt(x + 7.5, ym - 2.5), _pt(x + 5, ym + 1.5), _pt(x + 1.5, ym - 0.5))]
        coul = "black" if CONTROLE else "white"
        cx, r = x + 5, 3.8
        if self.nom == "gauche":   # ↺ : flèche dans le sens inverse des aiguilles d'une montre
            return [r"\draw[%s,line width=1.15pt,-{Stealth[length=2.6pt,width=3.4pt]}] %s arc[start angle=-60,end angle=200,radius=%s];"
                    % (coul, _pt(cx + r * math.cos(math.radians(-60)), ym + r * math.sin(math.radians(-60))), _n(r))]
        return [r"\draw[%s,line width=1.15pt,-{Stealth[length=2.6pt,width=3.4pt]}] %s arc[start angle=240,end angle=-20,radius=%s];"
                % (coul, _pt(cx + r * math.cos(math.radians(240)), ym + r * math.sin(math.radians(240))), _n(r))]

    def py(self):
        return ""


def _el(e):
    """Conversion automatique : nombre -> case nombre, chaîne -> case texte."""
    if isinstance(e, Elem):
        return e
    if isinstance(e, (int, float)):
        return Entree(e)
    return Entree(e, texte=True)


class Entree(Elem):
    """Case blanche (nombre ou texte)."""

    def __init__(self, v, texte=False):
        self.v, self.texte = v, texte or not isinstance(v, (int, float))

    def libelle(self):
        return self.v if self.texte else nombre_fr(self.v)

    def mesure(self):
        w = largeur(self.libelle()) + 2 * 5.0
        return max(w, 14.0 if self.texte else 20.0), H_ENT

    def dessin(self, x, ym, couleur_texte="scrTexteEntree", contour="black!18", epais=".5pt"):
        w, h = self.mesure()
        if CONTROLE:
            contour = "black!70"
        s = [r"\draw[%s,line width=%s,fill=white,rounded corners=%spt] %s rectangle %s;"
             % (contour, epais, _n(h / 2 - .01), _pt(x, ym - h / 2), _pt(x + w, ym + h / 2))]
        coul = "black" if CONTROLE else couleur_texte
        s.append(r"\node[anchor=base,inner sep=0pt,text=%s,font=\scrF] at %s {%s};"
                 % (coul, _pt(x + w / 2, ym - BASE), _tex(self.libelle())))
        return s

    def py(self):
        if self.texte:
            return repr(self.v)
        return repr(self.v)


class Menu(Elem):
    """Menu déroulant dans un bloc (nom de variable, message, touche)."""
    forme = "carre"

    def __init__(self, s, fam):
        self.s, self.fam = s, fam

    def mesure(self):
        return largeur(self.s) + 6 + 13, H_ENT

    def dessin(self, x, ym):
        w, h = self.mesure()
        fond = "white" if CONTROLE else "scr%sM" % self.fam
        coul = "black" if CONTROLE else "white"
        s = [r"\draw[scr%sB,line width=.5pt,fill=%s,rounded corners=3pt] %s rectangle %s;"
             % (self.fam, fond, _pt(x, ym - h / 2), _pt(x + w, ym + h / 2)),
             r"\node[anchor=base west,inner sep=0pt,text=%s,font=\scrF] at %s {%s};" % (coul, _pt(x + 6, ym - BASE), _tex(self.s)),
             r"\fill[%s] %s -- %s -- %s -- cycle;" % (coul, _pt(x + w - 10.5, ym + 1.6), _pt(x + w - 4.5, ym + 1.6), _pt(x + w - 7.5, ym - 2))]
        return s

    def py(self):
        return repr(self.s)


class Reporter(Elem):
    """Ovale coloré (variable, opérateur, réponse…) ; bool=True : hexagone (condition)."""

    def __init__(self, fam, items, code, bool_=False):
        self.fam, self.items, self.code, self.bool = fam, [_el(i) for i in items], code, bool_

    def _contenu(self):
        dims = [i.mesure() for i in self.items]
        w = sum(d[0] for d in dims) + GAP * 0.8 * (len(dims) - 1)
        hmax = max(d[1] for d in dims)
        texte_seul = all(isinstance(i, Texte) for i in self.items)
        h = H_ENT if texte_seul else max(H_ENT, hmax + 4.0)
        return dims, w, h

    def mesure(self):
        dims, w, h = self._contenu()
        if self.bool:
            pad = h / 2 + 2.0
        elif all(isinstance(i, Texte) for i in self.items):
            pad = 7.0
        else:
            pad = 3.0 if not isinstance(self.items[0], Texte) else 5.5
        return w + 2 * pad, h

    def dessin(self, x, ym, hl=False):
        dims, wc, h = self._contenu()
        w, _ = self.mesure()
        fond = "white" if CONTROLE else "scr%s" % self.fam
        bord = "scr%sB" % self.fam
        ep = ".5pt"
        if hl and _CORR[0]:
            bord, ep = "otGreenDark", "1.6pt"
        if self.bool:
            p = h / 2
            s = [r"\draw[%s,line width=%s,fill=%s,line join=round] %s -- %s -- %s -- %s -- %s -- %s -- cycle;"
                 % (bord, ep, fond, _pt(x, ym), _pt(x + p, ym + h / 2), _pt(x + w - p, ym + h / 2), _pt(x + w, ym),
                    _pt(x + w - p, ym - h / 2), _pt(x + p, ym - h / 2))]
        else:
            s = [r"\draw[%s,line width=%s,fill=%s,rounded corners=%spt] %s rectangle %s;"
                 % (bord, ep, fond, _n(h / 2 - .01), _pt(x, ym - h / 2), _pt(x + w, ym + h / 2))]
        cx = x + (w - wc) / 2
        for it, (iw, ih) in zip(self.items, dims):
            s += it.dessin(cx, ym)
            cx += iw + GAP * 0.8
        return s

    def py(self):
        return self.code(*[i.py() for i in self.items])


class Trou(Elem):
    """Case à compléter : lettre dans l'énoncé, solution en vert dans le corrigé."""

    def __init__(self, lettre, solution):
        self.lettre, self.sol = lettre, _el(solution)

    def mesure(self):
        if _CORR[0]:
            w, h = self.sol.mesure()
            return w + (0 if isinstance(self.sol, Reporter) else 4), h
        return max(largeur(self.lettre, graisse="SemiBold") + 14, 24.0), H_ENT

    def dessin(self, x, ym):
        if _CORR[0]:
            if isinstance(self.sol, Reporter):
                return self.sol.dessin(x, ym, hl=True)
            w, h = self.mesure()
            e = self.sol
            s = [r"\draw[otGreenDark,line width=1.3pt,fill=white,rounded corners=%spt] %s rectangle %s;"
                 % (_n(h / 2 - .01), _pt(x, ym - h / 2), _pt(x + w, ym + h / 2)),
                 r"\node[anchor=base,inner sep=0pt,text=%s,font=\otMedium\bfseries\fontsize{9}{11}\selectfont] at %s {%s};"
                 % ("black" if CONTROLE else "otGreenDark", _pt(x + w / 2, ym - BASE), _tex(e.libelle()))]
            return s
        w, h = self.mesure()
        return [r"\draw[otNavy,line width=.8pt,dash pattern=on 2pt off 1.4pt,fill=white,rounded corners=%spt] %s rectangle %s;"
                % (_n(h / 2 - .01), _pt(x, ym - h / 2), _pt(x + w, ym + h / 2)),
                r"\node[anchor=base,inner sep=0pt,text=%s,font=\otMedium\bfseries\fontsize{9}{11}\selectfont] at %s {%s};"
                % ("black" if CONTROLE else "otNavy", _pt(x + w / 2, ym - BASE), _tex(self.lettre))]

    def py(self):
        return self.sol.py()


# ---------------------------------------------------------------- reporters usuels
def _id(nom):
    """Nom de variable Scratch -> identifiant Python (les accents sont permis en Python)."""
    return nom.replace(" ", "_").replace("-", "_")


def V(nom):
    return Reporter("variable", [Texte(nom)], lambda *a: _id(nom))


def Param(nom):
    return Reporter("perso", [Texte(nom)], lambda *a: _id(nom))


def Reponse():
    return Reporter("capteur", [Texte("réponse")], lambda *a: "réponse")


def AbsX():
    return Reporter("mouvement", [Texte("abscisse x")], lambda *a: "lutin.x")


def OrdY():
    return Reporter("mouvement", [Texte("ordonnée y")], lambda *a: "lutin.y")


_PYOP = {"+": "+", "-": "-", "*": "*", "/": "/"}
_SYM = {"-": "−"}   # affichage : vrai signe moins


def Op(a, sym, b):
    return Reporter("operateur", [a, Texte(_SYM.get(sym, sym), taille=11.5), b],
                    lambda x, s, y: "(%s %s %s)" % (x, _PYOP[sym], y))


def Mod(a, b):
    return Reporter("operateur", [a, Texte("modulo"), b], lambda x, s, y: "(%s %% %s)" % (x, y))


def Alea(a, b):
    return Reporter("operateur", [Texte("nombre aléatoire entre"), a, Texte("et"), b],
                    lambda s1, x, s2, y: "random.randint(%s, %s)" % (x, y))


_PYCMP = {"<": "<", ">": ">", "=": "=="}


def Cmp(a, sym, b):
    return Reporter("operateur", [a, Texte(sym, taille=11.5), b], lambda x, s, y: "%s %s %s" % (x, _PYCMP[sym], y),
                    bool_=True)


def Et(a, b):
    return Reporter("operateur", [a, Texte("et"), b], lambda x, s, y: "(%s) and (%s)" % (x, y), bool_=True)


def Ou(a, b):
    return Reporter("operateur", [a, Texte("ou"), b], lambda x, s, y: "(%s) or (%s)" % (x, y), bool_=True)


def Non(a):
    return Reporter("operateur", [Texte("non"), a], lambda s, x: "not (%s)" % x, bool_=True)


def ToucheP(k):
    return Reporter("capteur", [Texte("touche"), Menu(k, "capteur"), Texte("pressée ?")],
                    lambda s, m, s2: "touche_pressee(%s)" % m, bool_=True)


# ================================================================ blocs (instructions)
class Bloc:
    """Instruction. genre : pile | chapeau | definir | C."""

    def __init__(self, fam, items, genre="pile", code=None, branches=None, hl=False):
        self.fam, self.genre = fam, genre
        self.items = [Texte(i) if isinstance(i, str) else _el(i) for i in items]
        self.code, self.branches, self.hl = code, branches or [], hl

    # ---- mesures
    def ligne(self, items=None):
        items = self.items if items is None else items
        dims = [i.mesure() for i in items]
        w = PADL + sum(d[0] for d in dims) + GAP * (len(dims) - 1) + PADR
        h = max(H_LIGNE, max(d[1] for d in dims) + 2 * VPAD)
        return dims, w, h

    def _proto(self):
        """Bloc « définir » : mesures du prototype (nom + paramètres)."""
        dims = [i.mesure() for i in self.items]
        wp = 6 + sum(d[0] for d in dims) + GAP * (len(dims) - 1) + 6
        hp = max(H_LIGNE - 4, max(d[1] for d in dims) + 6)
        return dims, wp, hp

    def hauteur(self):
        if self.genre == "seul":
            return self.items[0].mesure()[1]
        if self.genre == "definir":
            return self._proto()[2] + 16
        _, _, h = self.ligne()
        if self.genre == "chapeau":
            return h + CAP
        if self.genre == "C":
            tot = h
            for k, (lab, corps) in enumerate(self.branches):
                if k > 0:
                    tot += self.ligne([Texte(lab)])[2] - 4
                tot += hauteur_pile(corps) if corps else H_VIDE
            return tot + HB
        return h

    def largeur(self):
        if self.genre == "seul":
            return self.items[0].mesure()[0]
        if self.genre == "definir":
            return PADL + largeur("définir") + GAP + self._proto()[1] + PADR
        _, w, _ = self.ligne()
        if self.genre == "chapeau":
            w = max(w, HW + 12)
        if self.genre == "C":
            for lab, corps in self.branches:
                if corps:
                    w = max(w, ARM + largeur_pile(corps))
        return max(w, 44.0)

    # ---- dessin
    def _texte_ligne(self, items, dims, x0, ym):
        s, cx = [], x0
        for it, (iw, ih) in zip(items, dims):
            s += it.dessin(cx, ym)
            cx += iw + GAP
        return s

    def dessin(self, x, y):
        """(x, y) : coin haut-gauche de la partie rectangulaire (sous le chapeau éventuel)."""
        fond = "white" if CONTROLE else "scr%s" % self.fam
        bord = "scr%sB" % self.fam
        ep = ".6pt"
        if self.hl and _CORR[0]:
            bord, ep = "otGreenDark", "1.8pt"
        st = r"\draw[%s,line width=%s,fill=%s,line join=round" % (bord, ep, fond)

        def encoche_haut(x0, yy):   # de gauche à droite : creux vers le bas
            return [(x0 + NX, yy), (x0 + NX + ND, yy - ND), (x0 + NX + NW - ND, yy - ND), (x0 + NX + NW, yy)]

        def bosse_bas(x0, yy):      # de droite à gauche : bosse vers le bas
            return [(x0 + NX + NW, yy), (x0 + NX + NW - ND, yy - ND), (x0 + NX + ND, yy - ND), (x0 + NX, yy)]

        def chemin(pts):
            return st + ",rounded corners=%spt] " % _n(RC) + " -- ".join(_pt(*p) for p in _nettoie(pts)) + " -- cycle;"

        if self.genre == "seul":
            h = self.hauteur()
            return self.items[0].dessin(x, y - h / 2)
        if self.genre == "definir":
            dims, wp, hp = self._proto()
            W, H, R = self.largeur(), self.hauteur(), 10.0
            bas = [(x + W, y - H)] + bosse_bas(x, y - H) + [(x, y - H)]
            s = [st + "] %s arc[start angle=180,end angle=90,radius=%s] -- %s arc[start angle=90,end angle=0,radius=%s] -- %s -- cycle;"
                 % (_pt(x, y - R), _n(R), _pt(x + W - R, y), _n(R), " -- ".join(_pt(*p) for p in bas))]
            ym = y - 8 - hp / 2
            s += Texte("définir").dessin(x + PADL, ym)
            px = x + PADL + largeur("définir") + GAP
            s.append(r"\draw[scrpersoB,line width=.6pt,fill=%s,rounded corners=3pt] %s rectangle %s;"
                     % ("white" if CONTROLE else "scrperso", _pt(px, ym - hp / 2), _pt(px + wp, ym + hp / 2)))
            s += self._texte_ligne(self.items, dims, px + 6, ym)
            return s

        dims, w, h = self.ligne()
        if self.genre == "pile":
            W = self.largeur()
            pts = [(x, y)] + encoche_haut(x, y) + [(x + W, y), (x + W, y - h)] + bosse_bas(x, y - h) + [(x, y - h)]
            return [chemin(pts)] + self._texte_ligne(self.items, dims, x + PADL, y - h / 2)

        if self.genre == "chapeau":
            W = self.largeur()
            k = CAP * 4 / 3
            bas = [(x + W, y), (x + W, y - h)] + bosse_bas(x, y - h) + [(x, y - h)]
            s = [st + ",rounded corners=%spt] %s .. controls %s and %s .. %s -- %s -- cycle;"
                 % (_n(RC), _pt(x, y), _pt(x + HW * 0.3, y + k), _pt(x + HW * 0.7, y + k), _pt(x + HW, y),
                    " -- ".join(_pt(*p) for p in bas))]
            return s + self._texte_ligne(self.items, dims, x + PADL, y - h / 2)

        # ---------------- bloc C (répéter, si … alors [sinon])
        wh = max(w, 44.0)
        pts = [(x, y)] + encoche_haut(x, y) + [(x + wh, y), (x + wh, y - h)]
        textes = self._texte_ligne(self.items, dims, x + PADL, y - h / 2)
        interieur = []
        cy = y - h
        for k, (lab, corps) in enumerate(self.branches):
            if k > 0:   # ligne intermédiaire « sinon »
                it = [Texte(lab)]
                d2, w2, h2 = self.ligne(it)
                h2 -= 4
                w2 = max(w2, 44.0)
                pts += encoche_haut(x + ARM, cy) + [(x + w2, cy), (x + w2, cy - h2)]
                textes += self._texte_ligne(it, d2, x + PADL, cy - h2 / 2)
                cy -= h2
            hi = hauteur_pile(corps) if corps else H_VIDE
            pts += bosse_bas(x + ARM, cy) + [(x + ARM, cy), (x + ARM, cy - hi)]
            interieur += dessin_pile(corps, x + ARM, cy) if corps else []
            cy -= hi
        wb = max(44.0, min(wh, 56.0))
        pts += encoche_haut(x + ARM, cy) + [(x + wb, cy), (x + wb, cy - HB)] + bosse_bas(x, cy - HB) + [(x, cy - HB)]
        return [chemin(pts)] + textes + interieur

    def py(self, ind):
        return self.code(self, ind)



def _nettoie(pts):
    out = []
    for p in pts:
        if not out or (abs(out[-1][0] - p[0]) > 1e-6 or abs(out[-1][1] - p[1]) > 1e-6):
            out.append(p)
    return out


def hauteur_pile(blocs):
    return sum(b.hauteur() for b in blocs)


def largeur_pile(blocs):
    return max(b.largeur() for b in blocs) if blocs else 0


def dessin_pile(blocs, x, y):
    s = []
    for b in blocs:
        if b.genre == "chapeau":
            s += b.dessin(x, y - CAP)
            y -= b.hauteur()
        else:
            s += b.dessin(x, y)
            y -= b.hauteur()
    return s


# ---------------------------------------------------------------- traduction Python
def _ind(n):
    return "    " * n


def _corps_py(corps, ind):
    if not corps:
        return [_ind(ind) + "pass"]
    out = []
    for b in corps:
        out += b.py(ind)
    return out


def _simple(fmt):
    return lambda b, ind: [_ind(ind) + fmt(*[i.py() for i in b.items if not isinstance(i, (Texte, Icone))])]


# chapeaux
def Drapeau():
    return Bloc("evenement", ["quand", Icone("drapeau"), "est cliqué"], "chapeau", code=lambda b, i: [])


def Recoit(msg):
    b = Bloc("evenement", ["quand je reçois", Menu(msg, "evenement")], "chapeau", code=lambda b, i: [])
    b.message = msg
    return b


def ToucheHat(k):
    b = Bloc("evenement", ["quand la touche", Menu(k, "evenement"), "est pressée"], "chapeau", code=lambda b, i: [])
    b.touche = k
    return b


def Definir(nom, params):
    items = [Texte(nom)] + [Param(p) for p in params]
    b = Bloc("perso", items, "definir", code=lambda b, i: [])
    b.nom, b.params = nom, params
    return b


# variables, entrées, sorties
def Mettre(var, val, hl=False):
    return Bloc("variable", ["mettre", Menu(var, "variable"), "à", _el(val)], code=lambda b, ind: [
        _ind(ind) + "%s = %s" % (_id(var), _el(val).py())], hl=hl)


def Ajouter(var, val, hl=False):
    return Bloc("variable", ["ajouter", _el(val), "à", Menu(var, "variable")], code=lambda b, ind: [
        _ind(ind) + "%s = %s + %s" % (_id(var), _id(var), _el(val).py())], hl=hl)


def Demander(question, hl=False):
    return Bloc("capteur", ["demander", Entree(question, texte=True), "et attendre"], code=lambda b, ind: [
        _ind(ind) + "réponse = demander(%r)" % question], hl=hl)


def Dire(val, secondes=None, hl=False):
    if secondes is None:
        return Bloc("apparence", ["dire", _el(val)], code=lambda b, ind: [_ind(ind) + "lutin.dire(%s)" % _el(val).py()], hl=hl)
    return Bloc("apparence", ["dire", _el(val), "pendant", _el(secondes), "secondes"],
                code=lambda b, ind: [_ind(ind) + "lutin.dire(%s)" % _el(val).py()], hl=hl)


def Attendre(sec, hl=False):
    return Bloc("controle", ["attendre", _el(sec), "secondes"], code=lambda b, ind: [_ind(ind) + "pass  # attendre"], hl=hl)


# mouvement
def Avancer(n, hl=False):
    return Bloc("mouvement", ["avancer de", _el(n), "pas"], code=lambda b, ind: [_ind(ind) + "lutin.avancer(%s)" % _el(n).py()], hl=hl)


def TournerG(a, hl=False):
    return Bloc("mouvement", ["tourner", Icone("gauche"), "de", _el(a), "degrés"],
                code=lambda b, ind: [_ind(ind) + "lutin.tourner_gauche(%s)" % _el(a).py()], hl=hl)


def TournerD(a, hl=False):
    return Bloc("mouvement", ["tourner", Icone("droite"), "de", _el(a), "degrés"],
                code=lambda b, ind: [_ind(ind) + "lutin.tourner_droite(%s)" % _el(a).py()], hl=hl)


def AllerA(x, y, hl=False):
    return Bloc("mouvement", ["aller à x :", _el(x), "y :", _el(y)],
                code=lambda b, ind: [_ind(ind) + "lutin.aller_a(%s, %s)" % (_el(x).py(), _el(y).py())], hl=hl)


def Orienter(a, hl=False):
    return Bloc("mouvement", ["s'orienter à", _el(a)], code=lambda b, ind: [_ind(ind) + "lutin.orienter(%s)" % _el(a).py()], hl=hl)


def AjouterX(n, hl=False):
    return Bloc("mouvement", ["ajouter", _el(n), "à x"], code=lambda b, ind: [_ind(ind) + "lutin.ajouter_x(%s)" % _el(n).py()], hl=hl)


def AjouterY(n, hl=False):
    return Bloc("mouvement", ["ajouter", _el(n), "à y"], code=lambda b, ind: [_ind(ind) + "lutin.ajouter_y(%s)" % _el(n).py()], hl=hl)


# stylo
def EffacerTout(hl=False):
    return Bloc("stylo", ["effacer tout"], code=lambda b, ind: [_ind(ind) + "lutin.effacer_tout()"], hl=hl)


def StyloBas(hl=False):
    return Bloc("stylo", ["stylo en position d'écriture"], code=lambda b, ind: [_ind(ind) + "lutin.stylo_bas()"], hl=hl)


def StyloHaut(hl=False):
    return Bloc("stylo", ["relever le stylo"], code=lambda b, ind: [_ind(ind) + "lutin.stylo_haut()"], hl=hl)


# messages
def Envoyer(msg, attendre=False, hl=False):
    items = ["envoyer à tous", Menu(msg, "evenement")] + (["et attendre"] if attendre else [])
    return Bloc("evenement", items, code=lambda b, ind: [_ind(ind) + "envoyer_a_tous(%r)" % msg], hl=hl)


def Seul(reporter):
    """Reporter ou condition dessiné seul (palette du cours)."""
    return Bloc(reporter.fam, [reporter], "seul", code=lambda b, ind: [])


# bloc personnalisé (appel)
def Appel(nom, args, hl=False):
    return Bloc("perso", [nom] + [_el(a) for a in args], code=lambda b, ind: [
        _ind(ind) + "%s(%s)" % (_id(nom), ", ".join(_el(a).py() for a in args))], hl=hl)


# contrôle
def Repeter(n, corps, hl=False):
    return Bloc("controle", ["répéter", _el(n), "fois"], "C", branches=[(None, corps)], hl=hl, code=lambda b, ind: [
        _ind(ind) + "for _ in range(%s):" % _el(n).py(), _ind(ind + 1) + "pas()"] + _corps_py(corps, ind + 1))


def JusquA(cond, corps, hl=False):
    return Bloc("controle", ["répéter jusqu'à", cond], "C", branches=[(None, corps)], hl=hl, code=lambda b, ind: [
        _ind(ind) + "while not (%s):" % cond.py(), _ind(ind + 1) + "pas()"] + _corps_py(corps, ind + 1))


def Indefiniment(corps, hl=False):
    return Bloc("controle", ["répéter indéfiniment"], "C", branches=[(None, corps)], hl=hl, code=lambda b, ind: [
        _ind(ind) + "while True:", _ind(ind + 1) + "pas()"] + _corps_py(corps, ind + 1))


def Si(cond, corps, sinon=None, hl=False):
    br = [(None, corps)] + ([("sinon", sinon)] if sinon is not None else [])

    def code(b, ind):
        out = [_ind(ind) + "if %s:" % cond.py()] + _corps_py(corps, ind + 1)
        if sinon is not None:
            out += [_ind(ind) + "else:"] + _corps_py(sinon, ind + 1)
        return out
    return Bloc("controle", ["si", cond, "alors"], "C", branches=br, hl=hl, code=code)


# ================================================================ figures de scripts
def _titre(x, y, txt):
    return [r"\node[anchor=north west,inner sep=0pt,text=%s,font=\scrT] at %s {%s};"
            % ("black" if CONTROLE else "otNavy", _pt(x, y), _tex(txt))]


def mesure_script(script):
    """(largeur, hauteur) en pt d'une pile de blocs (chapeau compris)."""
    return largeur_pile(script), hauteur_pile(script)


def figure_scripts(scripts, corrige=False, disposition="colonne", ecart=16.0, largeur_max=262.0):
    """scripts : liste de (titre, pile de blocs). disposition : colonne (les uns sous les autres)
    ou ligne (côte à côte). Renvoie le code tikzpicture (unités : pt)."""
    _CORR[0] = corrige
    try:
        s = []
        x = y = 0.0
        largeur_tot = 0.0
        for titre, pile in scripts:
            w, h = mesure_script(pile)
            ys = y
            if titre:
                s += _titre(x, y, titre)
                ys = y - 15.0
            s += dessin_pile(pile, x, ys)
            if disposition == "colonne":
                y = ys - h - ecart
                largeur_tot = max(largeur_tot, w)
            else:
                x += w + ecart
                largeur_tot = x - ecart
        if largeur_tot > largeur_max:
            print("  [scratch] attention : figure large (%.0f pt > %.0f pt)" % (largeur_tot, largeur_max))
        return "\n".join([r"\begin{tikzpicture}[x=1pt,y=1pt,line cap=round]"] + s + [r"\end{tikzpicture}"])
    finally:
        _CORR[0] = False


# ================================================================ exécution (traduction Python)
class BoucleInfinie(Exception):
    pass


class Lutin:
    def __init__(self, nom):
        self.nom = nom
        self.x, self.y, self.direction = 0.0, 0.0, 90.0
        self.ecrit = False
        self.segments = []      # ((x1, y1), (x2, y2))
        self.positions = [(0.0, 0.0)]
        self.dits = []

    def _va(self, x, y):
        x, y = round(x, 9), round(y, 9)
        if self.ecrit and (x, y) != (self.x, self.y):
            self.segments.append(((self.x, self.y), (x, y)))
        self.x, self.y = x, y
        self.positions.append((x, y))

    def avancer(self, d):
        a = math.radians(self.direction)
        self._va(self.x + d * math.sin(a), self.y + d * math.cos(a))

    def tourner_gauche(self, a):
        self.direction = _dir(self.direction - a)

    def tourner_droite(self, a):
        self.direction = _dir(self.direction + a)

    def orienter(self, a):
        self.direction = _dir(a)

    def aller_a(self, x, y):
        self._va(x, y)

    def ajouter_x(self, d):
        self._va(self.x + d, self.y)

    def ajouter_y(self, d):
        self._va(self.x, self.y + d)

    def effacer_tout(self):
        self.segments = []

    def stylo_bas(self):
        self.ecrit = True

    def stylo_haut(self):
        self.ecrit = False

    def dire(self, v):
        self.dits.append(v)


def _dir(a):
    """Orientation Scratch dans ]-180 ; 180]."""
    a = (a + 180) % 360 - 180
    return 180.0 if a == -180 else a


def _nom_fonction(b, k, lutin):
    if b.genre == "definir":
        return _id(b.nom)
    base = {"drapeau": "quand_drapeau_clique"}
    if hasattr(b, "message"):
        n = "quand_je_recois_" + _id(b.message)
    elif hasattr(b, "touche"):
        n = "quand_touche_" + _id(b.touche)
    else:
        n = base["drapeau"]
    return "%s_%s_%d" % (_id(lutin).lower(), n, k)


def _variables(projet):
    noms = set()

    def visite(blocs):
        for b in blocs:
            for it in b.items:
                if isinstance(it, Menu) and b.fam == "variable":
                    noms.add(_id(it.s))
            for _, corps in b.branches:
                visite(corps)
    for scripts in projet.values():
        for sc in scripts:
            visite(sc)
    return sorted(noms)


def traduire(projet, instrumente=False):
    """projet : {nom_lutin: [script, …]} (variables communes à tous les lutins).
    Renvoie le texte Python ; chaque script devient une fonction."""
    glob = _variables(projet)
    lignes = ["import random", ""]
    if glob:
        lignes += ["%s = 0" % g for g in glob] + [""]
    for lutin, scripts in projet.items():
        lignes.append("# ----- lutin %s" % lutin)
        lignes.append("%s = Lutin(%r)" % ("lutin_" + _id(lutin).lower(), lutin))
        for k, sc in enumerate(scripts):
            tete = sc[0]
            nom = _nom_fonction(tete, k, lutin)
            params = ", ".join(_id(p) for p in getattr(tete, "params", []))
            lignes.append("def %s(%s):" % (nom, params))
            if glob:
                lignes.append("    global %s, réponse" % ", ".join(glob))
            else:
                lignes.append("    global réponse")
            lignes.append("    lutin = %s" % ("lutin_" + _id(lutin).lower()))
            corps = _corps_py(sc[1:], 1)
            lignes += corps
            if hasattr(tete, "message"):
                lignes.append("MESSAGES.setdefault(%r, []).append(%s)" % (tete.message, nom))
            elif hasattr(tete, "touche"):
                lignes.append("TOUCHES.setdefault(%r, []).append(%s)" % (tete.touche, nom))
            elif tete.genre == "chapeau":
                lignes.append("DRAPEAU.append(%s)" % nom)
            lignes.append("")
    texte = "\n".join(lignes)
    if not instrumente:
        texte = "\n".join(l for l in texte.splitlines() if l.strip() != "pas()")
    return texte


class Resultat:
    pass


class _Impose:
    """Générateur « aléatoire » qui renvoie des tirages imposés (puis le hasard)."""

    def __init__(self, tirages, graine):
        self.tirages, self.rnd = list(tirages), random.Random(graine)

    def randint(self, a, b):
        if self.tirages:
            v = self.tirages.pop(0)
            assert a <= v <= b
            return v
        return self.rnd.randint(a, b)


def executer(projet, entrees=(), touches=(), graine=0, max_pas=2_000_000, tirages=()):
    """Traduit le projet en Python et l'exécute (drapeau, puis touches pressées dans l'ordre).
    entrees : réponses successives aux blocs « demander » ; tirages : résultats imposés des
    « nombre aléatoire » (ensuite : hasard reproductible, graine).
    Renvoie un objet : dits (toutes les valeurs dites, dans l'ordre), vars (variables
    globales), lutins (objets Lutin : segments, positions, direction), infinie (boucle infinie)."""
    code = traduire(projet, instrumente=True)
    entrees = list(entrees)
    rnd = _Impose(tirages, graine)
    compteur = [0]
    ns = {}

    def pas():
        compteur[0] += 1
        if compteur[0] > max_pas:
            raise BoucleInfinie()

    def demander(q):
        return entrees.pop(0)

    def envoyer_a_tous(msg):
        for f in ns["MESSAGES"].get(msg, []):
            f()

    ns.update(Lutin=Lutin, DRAPEAU=[], MESSAGES={}, TOUCHES={}, pas=pas, demander=demander,
              envoyer_a_tous=envoyer_a_tous, réponse="", touche_pressee=lambda k: False)
    exec(code, ns)
    ns["random"] = rnd   # hasard reproductible
    r = Resultat()
    r.infinie = False
    try:
        for f in ns["DRAPEAU"]:
            f()
        for t in touches:
            for f in ns["TOUCHES"].get(t, []):
                f()
    except BoucleInfinie:
        r.infinie = True
    r.lutins = {k[len("lutin_"):]: v for k, v in ns.items() if k.startswith("lutin_") and isinstance(v, Lutin)}
    r.dits = [d for l in r.lutins.values() for d in l.dits]
    r.vars = {g: ns[g] for g in _variables(projet)}
    r.code = traduire(projet)
    r.pas = compteur[0]
    return r


# ================================================================ repère de la scène et tracés
def figure_trace(segments, fenetre, pas, unite, vert=True, points=(), depart=None, fleche=None,
                 autres=(), legende_axes=True, grille=True, pas_lab=None, sans_repere=False):
    """Tracé du lutin sur le repère de la scène.

    segments : [((x1,y1),(x2,y2)), …] (tracé principal : vert si vert=True, sinon bleu marine) ;
    autres : [(segments, style TikZ)] tracés supplémentaires ; fenetre = (xmin, xmax, ymin, ymax) ;
    pas : pas de la grille ; unite : cm par unité Scratch ; points : [(x, y, texte, ancre)] ;
    depart : (x, y) point de départ (« départ ») ; fleche : (x, y, orientation) lutin final.
    """
    xmin, xmax, ymin, ymax = fenetre
    pas_lab = pas_lab or pas
    u = unite

    def P(x, y):
        return "(%s,%s)" % (_n(x * u), _n(y * u))
    s = [r"\begin{tikzpicture}[line cap=round,line join=round]"]
    if not sans_repere:
        if grille:
            k = math.ceil(xmin / pas)
            while k * pas <= xmax + 1e-9:
                s.append(r"\draw[otRule!80,line width=.35pt] %s -- %s;" % (P(k * pas, ymin), P(k * pas, ymax)))
                k += 1
            k = math.ceil(ymin / pas)
            while k * pas <= ymax + 1e-9:
                s.append(r"\draw[otRule!80,line width=.35pt] %s -- %s;" % (P(xmin, k * pas), P(xmax, k * pas)))
                k += 1
        s.append(r"\draw[otRule,line width=.6pt] %s rectangle %s;" % (P(xmin, ymin), P(xmax, ymax)))
        if xmin <= 0 <= xmax:
            s.append(r"\draw[otMuted,line width=.6pt] %s -- %s;" % (P(0, ymin), P(0, ymax)))
        if ymin <= 0 <= ymax:
            s.append(r"\draw[otMuted,line width=.6pt] %s -- %s;" % (P(xmin, 0), P(xmax, 0)))
        lab = r"\node[font=\otRegular\fontsize{8}{9}\selectfont,text=otMuted,inner sep=1pt,anchor=%s] at %s {%s};"
        k = math.ceil(xmin / pas_lab)
        while k * pas_lab <= xmax + 1e-9:
            s.append(lab % ("north", "(%s,%s)" % (_n(k * pas_lab * u), _n(ymin * u - .08)), nombre_fr(k * pas_lab)))
            k += 1
        k = math.ceil(ymin / pas_lab)
        coin = abs(xmin / pas_lab - round(xmin / pas_lab)) < 1e-9   # graduation x dans le coin bas-gauche
        while k * pas_lab <= ymax + 1e-9:
            if not (coin and abs(k * pas_lab - ymin) < 1e-9):   # évite deux nombres qui se touchent au coin
                s.append(lab % ("east", "(%s,%s)" % (_n(xmin * u - .08), _n(k * pas_lab * u)), nombre_fr(k * pas_lab)))
            k += 1
        if legende_axes:   # noms des axes au bout des axes, hors du cadre
            yx = 0 if ymin <= 0 <= ymax else ymin
            xy = 0 if xmin <= 0 <= xmax else xmin
            s.append(r"\node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=west,inner sep=1pt] at (%s,%s) {$x$};"
                     % (_n(xmax * u + .1), _n(yx * u)))
            s.append(r"\node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=south,inner sep=1pt] at (%s,%s) {$y$};"
                     % (_n(xy * u), _n(ymax * u + .08)))
    for segs, style in autres:
        for a, b in segs:
            s.append(r"\draw[%s] %s -- %s;" % (style, P(*a), P(*b)))
    style = "otGreenDark,line width=1.7pt" if vert else "otNavy,line width=1.5pt"
    for a, b in _fusion(segments):
        s.append(r"\draw[%s] %s;" % (style, " -- ".join(P(*p) for p in [a] + b)))
    if depart is not None:
        s.append(r"\fill[otNavy] %s circle (2.4pt);" % P(*depart))
    if fleche is not None:
        x, y, o = fleche
        a = math.radians(o)
        dx, dy = math.sin(a), math.cos(a)
        c = (x * u, y * u)
        L = .26
        tip = (c[0] + dx * L, c[1] + dy * L)
        b1 = (c[0] - dy * .1, c[1] + dx * .1)
        b2 = (c[0] + dy * .1, c[1] - dx * .1)
        s.append(r"\fill[otOrange] (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;" % (_n(tip[0]), _n(tip[1]), _n(b1[0]), _n(b1[1]), _n(b2[0]), _n(b2[1])))
    for (x, y, txt, anc) in points:
        s.append(r"\node[anchor=%s,inner sep=2.6pt,font=\otMedium\fontsize{8.5}{10}\selectfont,text=%s] at %s {%s};"
                 % (anc, "otGreenDark" if vert else "otInk", P(x, y), txt))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


def _fusion(segments):
    """Regroupe les segments consécutifs en lignes brisées (meilleures jonctions)."""
    out = []
    for a, b in segments:
        if out and out[-1][1][-1] == a:
            out[-1][1].append(b)
        else:
            out.append((a, [b]))
    return out


__all__ = [n for n in dir() if not n.startswith("_") or n in ("_CORR",)]
