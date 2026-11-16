# -*- coding: utf-8 -*-
"""Opérations posées en TikZ (rubrique « Poser les opérations »).

Module partagé par les figures/figures.py de contenu/operations/<page>/ :

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from poser import *

Tous les résultats, retenues, restes et quotients sont CALCULÉS ici (jamais
écrits à la main) puis contrôlés par des assert : une figure ne peut pas
afficher un calcul faux.

Écriture des nombres : chaînes « 2748 », « 34,8 » ; un « o » est un zéro
ajouté (écrit en gris) : « 12,5o ».
Couleurs : nombres de l'énoncé en encre, retenues et emprunts en orange,
résultat en vert foncé, étape en cours en bleu marine, aides en gris.
"""
from fractions import Fraction

VERT = "otGreenDark"
NAVY = "otNavy"
INK = "otInk"
ORANGE = "otOrange!90!black"
MUET = "otMuted!65"
GRIS = "otMuted"

PREAMBULE_EXTRA = r"""
\tikzset{
  ch/.style={anchor=base,inner sep=0pt,font=\fontsize{12.5}{15}\selectfont},
  ret/.style={anchor=base,inner sep=0pt,font=\fontsize{8.6}{10}\selectfont,text=otOrange!90!black},
  note/.style={anchor=base west,inner sep=1pt,font=\otRegular\fontsize{8.4}{10}\selectfont,text=otMuted},
  noteE/.style={anchor=base east,inner sep=1pt,font=\otRegular\fontsize{8.4}{10}\selectfont,text=otMuted},
  ent/.style={anchor=base,inner sep=0pt,font=\otRegular\fontsize{7.8}{9}\selectfont,text=otMuted},
  titreF/.style={anchor=base,inner sep=1pt,font=\otMedium\fontsize{8.8}{10}\selectfont,text=otNavy},
  filet/.style={otMuted,line width=.7pt},
  potence/.style={otNavy,line width=.9pt},
  barre/.style={otOrange!90!black,line width=.7pt},
  descend/.style={otOrange!90!black,line width=.7pt,dash pattern=on 2.2pt off 1.6pt,-{Stealth[length=1.7mm]}},
  fl/.style={otMuted,line width=.6pt,-{Stealth[length=1.6mm]}},
  accol/.style={line width=.7pt,decorate,decoration={brace,amplitude=4.5pt}},
}
"""

FIGURES = {}


def f(v):
    return ("%.4f" % float(v)).rstrip("0").rstrip(".")


def tikz(lignes):
    return "\\begin{tikzpicture}\n" + "\n".join(lignes) + "\n\\end{tikzpicture}"


def valeur(s):
    """« 34,8o » -> Fraction(348, 10)."""
    s = s.replace("o", "0")
    if "," in s:
        e, d = s.split(",")
        return Fraction(int(e + d), 10 ** len(d))
    return Fraction(int(s))


def ecrire(v, decimales=0):
    """Fraction -> chaîne avec virgule et `decimales` chiffres après la virgule."""
    n = v * 10 ** decimales
    assert n.denominator == 1, (v, decimales)
    n = int(n)
    s = str(n).rjust(decimales + 1, "0")
    return s if decimales == 0 else s[:-decimales] + "," + s[-decimales:]


def rangs(s):
    """« 34,8o » -> {rang: (chiffre, muet)} ; rang 0 = unités, -1 = dixièmes…"""
    ent, dec = (s.split(",") + [""])[:2]
    out = {}
    for i, c in enumerate(ent):
        out[len(ent) - 1 - i] = ("0" if c == "o" else c, c == "o")
    for j, c in enumerate(dec):
        out[-(j + 1)] = ("0" if c == "o" else c, c == "o")
    return out


def nb_dec(s):
    return len(s.split(",")[1]) if "," in s else 0


def milliers(n):
    """1234567 -> « 1\\,234\\,567 » (formules)."""
    s = str(n)
    g = []
    while len(s) > 3:
        g.insert(0, s[-3:])
        s = s[:-3]
    g.insert(0, s)
    return "\\,".join(g)


def nombre_tex(s):
    """« 1234,5 » -> « 1\\,234{,}5 »."""
    s = s.replace("o", "0")
    ent, dec = (s.split(",") + [""])[:2]
    t = milliers(int(ent)) if ent else "0"
    return t + ("{,}" + dec if dec else "")


class Pose:
    """Grille d'une opération posée en colonnes (unités alignées).

    x(r) : abscisse de la colonne de rang r ; les décimales sont décalées de
    `gap` pour laisser la place à la virgule.
    """

    def __init__(self, cw=.5, rh=.66, gap=.14, virgule=False):
        self.cw, self.rh, self.gap, self.virgule = cw, rh, gap, virgule
        self.L = []

    def x(self, r):
        return -r * self.cw + (self.gap if (self.virgule and r < 0) else 0)

    def chiffre(self, r, y, c, coul=INK, gras=False):
        g = r",font=\fontsize{12.5}{15}\selectfont\bfseries" if gras else ""
        self.L.append(r"\node[ch,text=%s%s] at (%s,%s) {$%s$};" % (coul, g, f(self.x(r)), f(y), c))

    def nombre(self, s, y, coul=INK, gras=False):
        rg = rangs(s)
        for r, (c, muet) in rg.items():
            self.chiffre(r, y, c, MUET if muet else coul, gras)
        if "," in s:
            self.virg(y, coul)
        return rg

    def virg(self, y, coul=INK):
        xv = self.x(0) + self.cw / 2 + self.gap / 2 - .03
        self.L.append(r"\node[ch,text=%s] at (%s,%s) {$,$};" % (coul, f(xv), f(y)))

    def petit(self, x, y, t, coul=ORANGE):
        self.L.append(r"\node[ret,text=%s] at (%s,%s) {$%s$};" % (coul, f(x), f(y), t))

    def filet(self, r_gauche, r_droite, y, marge=.42):
        x1 = self.x(r_gauche) - self.cw * marge - .3
        x2 = self.x(r_droite) + self.cw * .5
        self.L.append(r"\draw[filet] (%s,%s) -- (%s,%s);" % (f(x1), f(y), f(x2), f(y)))

    def signe(self, r_gauche, y, s, decal=1.0):
        self.L.append(r"\node[ch] at (%s,%s) {$%s$};" % (f(self.x(r_gauche) - self.cw * decal - .12), f(y), s))

    def note(self, r_droite, y, t, dx=.55):
        self.L.append(r"\node[note] at (%s,%s) {%s};" % (f(self.x(r_droite) + self.cw * .5 + dx), f(y), t))

    def code(self):
        return tikz(self.L)


ENTETES = {3: "m", 2: "c", 1: "d", 0: "u"}


# ===================================================================== addition
def addition(termes, entetes=False, retenues=True, notes=None, titre=None):
    """Addition posée ; retenues et résultat calculés. notes : {indice_ligne: texte}."""
    total = sum(valeur(t) for t in termes)
    dmax = max(nb_dec(t) for t in termes)
    res = ecrire(total, dmax)
    virgule = dmax > 0
    P = Pose(cw=.5, virgule=virgule)
    rgs = [rangs(t) for t in termes]
    rmax = max(max(r) for r in rgs + [rangs(res)])
    rmin = -dmax
    # retenues (colonne par colonne, de droite à gauche)
    ret = {}
    c = 0
    for r in range(rmin, rmax + 1):
        s = sum(int(g[r][0]) for g in rgs if r in g) + c
        c = s // 10
        if c:
            ret[r + 1] = c
    assert valeur(res) == total
    y0 = 0
    if retenues and ret:
        for r, v in ret.items():
            P.petit(P.x(r), .5, str(v))
    if entetes:
        yh = 1.0 if (retenues and ret) else .62
        for r in range(rmin, rmax + 1):
            if r in ENTETES:
                P.L.append(r"\node[ent] at (%s,%s) {%s};" % (f(P.x(r)), f(yh), ENTETES[r]))
    for i, t in enumerate(termes):
        P.nombre(t, y0 - i * P.rh)
        if notes and i in notes:
            P.note(rmin, y0 - i * P.rh, notes[i])
    yb = y0 - (len(termes) - 1) * P.rh
    P.signe(max(max(g) for g in rgs[1:]), yb, "+")
    P.filet(rmax, rmin, yb - .24)
    yr = yb - P.rh - .06
    P.nombre(res, yr, VERT, gras=False)
    if notes and "res" in notes:
        P.note(rmin, yr, notes["res"])
    if titre:
        P.L.append(r"\node[titreF] at (%s,%s) {%s};" % (f((P.x(rmax) + P.x(rmin)) / 2), f(1.05 if not entetes else 1.45), titre))
    return P.code()


# ===================================================================== soustraction
def soustraction(a, b, methode="compensation", notes=None, titre=None, entetes=False):
    """Soustraction posée a - b.

    methode = « cassage » (on casse une dizaine du haut : chiffre barré, nouvelle
    valeur au-dessus) ou « compensation » (on ajoute 10 en haut et 1 en bas).
    """
    da, db = nb_dec(a), nb_dec(b)
    dmax = max(da, db)
    diff = valeur(a) - valeur(b)
    assert diff >= 0
    res = ecrire(diff, dmax)
    virgule = dmax > 0
    P = Pose(cw=.7, virgule=virgule, gap=.3)
    A, B = rangs(a), rangs(b)
    rmax, rmin = max(A), -dmax
    top = {r: int(A[r][0]) if r in A else 0 for r in range(rmin, rmax + 1)}
    bot = {r: int(B[r][0]) if r in B else 0 for r in range(rmin, rmax + 1)}
    dessus, barre, dix, ret_bas = {}, set(), set(), set()
    if methode == "cassage":
        t = dict(top)
        for r in range(rmin, rmax + 1):
            if t[r] < bot[r]:
                j = r + 1
                while t[j] == 0:
                    j += 1
                t[j] -= 1
                barre.add(j)
                for k in range(r + 1, j):
                    t[k] = 9 if k not in barre else t[k] + 9
                    barre.add(k)
                t[r] += 10
                if r in barre:
                    pass
                else:
                    dix.add(r)
            out = t[r] - bot[r]
            assert 0 <= out <= 9
        for r in barre:
            dessus[r] = t[r]
        chiffres_res = {r: t[r] - bot[r] for r in t}
    else:
        c = 0
        chiffres_res = {}
        for r in range(rmin, rmax + 1):
            if top[r] < bot[r] + c:
                dix.add(r)
                chiffres_res[r] = top[r] + 10 - bot[r] - c
                c2 = 1
            else:
                chiffres_res[r] = top[r] - bot[r] - c
                c2 = 0
            if c2:
                ret_bas.add(r + 1)
            c = c2
        assert c == 0
    # contrôle : les chiffres trouvés font bien la différence
    tot = sum(Fraction(d) * Fraction(10) ** r for r, d in chiffres_res.items())
    assert tot == diff, (a, b, chiffres_res)
    # dessin
    y1, y2 = 0, -P.rh
    for r, (ch, muet) in A.items():
        P.chiffre(r, y1, ch, MUET if muet else INK)
    if "," in a or virgule:
        P.virg(y1)
    for r, (ch, muet) in B.items():
        P.chiffre(r, y2, ch, MUET if muet else INK)
    if "," in b or virgule:
        P.virg(y2)
    for r in dix:
        P.petit(P.x(r) - .3, y1 + .14, "1")
    for r in barre:
        x = P.x(r)
        P.L.append(r"\draw[barre] (%s,%s) -- (%s,%s);" % (f(x - .15), f(y1 - .07), f(x + .15), f(y1 + .36)))
    for r, v in dessus.items():
        P.petit(P.x(r), y1 + .52, str(v))
    for r in ret_bas:
        # retenue ajoutée au chiffre du bas ; colonne vide en bas : elle prend la place du chiffre
        P.petit(P.x(r) - (.3 if r in B else 0), y2 - .1, "1")
    rgauche = rmax
    P.signe(rgauche, y2, "-", decal=1.05)
    P.filet(rgauche, rmin, y2 - .26, marge=.6)
    yr = y2 - P.rh - .06
    P.nombre(res if not res.startswith("0") or len(res.split(",")[0]) == 1 else res, yr, VERT)
    if notes:
        for i, t in notes.items():
            y = {0: y1, 1: y2, "res": yr}[i]
            P.note(rmin, y, t)
    if titre:
        haut = .95 if (barre or not dix) else .7
        P.L.append(r"\node[titreF] at (%s,%s) {%s};" % (f((P.x(rmax) + P.x(rmin)) / 2), f(haut + .2), titre))
    if entetes:
        yh = .95 if barre else .62
        for r in range(rmin, rmax + 1):
            if r in ENTETES:
                P.L.append(r"\node[ent] at (%s,%s) {%s};" % (f(P.x(r)), f(yh), ENTETES[r]))
    return P.code()


# ===================================================================== multiplication
def multiplication(a, b, retenues=None, notes=True, decalage="0", comptes=None):
    """Multiplication posée a × b (nombres alignés à droite, sans tenir compte
    des virgules). Produits partiels décalés (zéros gris), notes à droite.

    retenues : True pour écrire les retenues du produit par un chiffre (b à un
    chiffre seulement). comptes : notes « chiffres après la virgule » (décimaux).
    """
    ea, eb = int(a.replace(",", "")), int(b.replace(",", ""))
    da, db = nb_dec(a), nb_dec(b)
    prod = ea * eb
    assert valeur(a) * valeur(b) == Fraction(prod, 10 ** (da + db))
    res = ecrire(Fraction(prod, 10 ** (da + db)), da + db)
    P = Pose(cw=.5)
    sa, sb = a.replace(",", ""), b.replace(",", "")
    # position = index depuis la droite (rang « fictif ») ; virgules dessinées entre deux colonnes
    def place(s_avec_virgule, y, coul=INK, muets=0):
        s = s_avec_virgule.replace(",", "")
        n = len(s)
        for i, c in enumerate(s):
            r = n - 1 - i
            P.chiffre(r, y, c, MUET if r < muets else coul)
        if "," in s_avec_virgule:
            k = nb_dec(s_avec_virgule)
            xv = P.x(k) + P.cw / 2 - .04
            P.L.append(r"\node[ch,text=%s] at (%s,%s) {$,$};" % (coul, f(xv), f(y)))
        return n

    rows = []
    y = 0
    if retenues and len(sb) == 1:
        c, rr = 0, {}
        for i in range(len(sa)):
            d = int(sa[len(sa) - 1 - i])
            p = d * int(sb) + c
            c = p // 10
            if c and i + 1 < len(sa):
                rr[i + 1] = c
        for r, v in rr.items():
            P.petit(P.x(r), .5, str(v))
    na = place(a, 0)
    nb = place(b, -P.rh)
    larg = len(str(prod))
    P.signe(max(na, nb) - 1, -P.rh, r"\times")
    P.filet(max(larg, na, nb) - 1, 0, -P.rh - .24)
    yl = -2 * P.rh - .06
    lignes = []
    if len(sb) > 1:
        for i in range(len(sb)):
            d = int(sb[len(sb) - 1 - i])
            part = ea * d
            txt = str(part) + "0" * i
            lignes.append((txt, i, d))
        for txt, i, d in lignes:
            n = len(txt)
            for j, c in enumerate(txt):
                r = n - 1 - j
                if r < i:
                    if decalage == "0":
                        P.chiffre(r, yl, "0", MUET)
                    else:
                        P.chiffre(r, yl, r"\cdot", MUET)
                else:
                    P.chiffre(r, yl, c, INK)
            if notes and not comptes:
                mult = d * 10 ** i
                P.note(0, yl, r"$%s \times %s$" % (milliers(ea), milliers(mult)) if i else r"$%s \times %d$" % (milliers(ea), d))
            yl -= P.rh
        assert sum(int(t) for t, _, _ in lignes) == prod
        P.signe(len(lignes[-1][0]) - 1, yl + P.rh, "+")
        P.filet(larg - 1, 0, yl + P.rh - .24)
        yl -= .06
    # résultat
    if da + db:
        place(res if not res.startswith("0,") else res, yl, VERT)
    else:
        place(str(prod), yl, VERT)
    if comptes:
        P.note(0, 0, comptes[0])
        P.note(0, -P.rh, comptes[1])
        P.note(0, yl, comptes[2], dx=.55)
    return P.code(), res


# ===================================================================== division
def analyse(dividende, b, zeros=0):
    """Division posée de `dividende` (chaîne, éventuellement décimale) par b
    (entier), avec `zeros` zéros ajoutés après la virgule.

    Renvoie (ch, k, nz, etapes, quotient_txt, reste) ; etapes = [(e, partiel,
    qd, r)] avec e = indice du dernier chiffre du dividende utilisé.
    """
    s = dividende
    ent, dec = (s.split(",") + [""])[:2]
    ch = [int(c) for c in ent + dec] + [0] * zeros
    k = len(ent)                     # indice du premier chiffre après la virgule
    nz = zeros
    e = 0
    partiel = ch[0]
    while partiel < b and e < k - 1:
        e += 1
        partiel = partiel * 10 + ch[e]
    et = []
    while True:
        qd = partiel // b
        r = partiel - qd * b
        et.append((e, partiel, qd, r))
        e += 1
        if e >= len(ch):
            break
        partiel = r * 10 + ch[e]
    e0 = et[0][0]
    qch = [str(x[2]) for x in et]
    # virgule du quotient : avant le chiffre obtenu en abaissant ch[k]
    if len(ch) > k:
        avant = k - e0          # nombre de chiffres de la partie entière du quotient
        if avant <= 0:
            qtxt = "0{,}" + "0" * (-avant) + "".join(qch)
        else:
            qtxt = "".join(qch[:avant]) + "{,}" + "".join(qch[avant:])
    else:
        qtxt = "".join(qch)
    ndec = max(0, len(ch) - k)
    reste = Fraction(et[-1][3], 10 ** ndec)
    q = Fraction(int(qtxt.replace("{,}", "")), 10 ** (len(ch) - max(k, e0 + 1) if len(ch) > k else 0))
    assert valeur(s) == b * q + reste, (s, b, qtxt, reste)
    return ch, k, nz, et, q, qtxt, reste


def division(dividende, b, zeros=0, noms=False, courte=False, jusqua=None, actif=None,
             abaisse=None, slots=None, egalite=None, suite=False, mode="cours",
             style="france", accolade=None, extra=None, cadre=False):
    """Division posée.

    style   : « france » (potence) ou « anglais » (diviseur à gauche, quotient
              au-dessus du dividende, pays anglophones).
    courte  : méthode courte, les soustractions sont faites de tête (seuls les
              restes sont écrits).
    jusqua  : n'afficher que les étapes 0..jusqua (déroulé pas à pas ; -1 =
              préparation seule) ; actif = étape écrite en bleu.
    abaisse : étape dont le chiffre abaissé est montré par une flèche.
    slots   : lettres sous les chiffres attendus du quotient (« cdu ») + points.
    accolade: texte sous l'accolade du premier « morceau » du dividende.
    egalite : texte sous la figure (None = égalité de la division euclidienne
              si la division est finie et entière ; '' = rien).
    suite   : division qui ne s'arrête pas (« … », restes répétés en orange).
    extra   : lignes TikZ ajoutées (table des multiples…).
    cadre   : même cadre que la division complète (potence pleine hauteur) :
              les figures d'un déroulé pas à pas ont toutes la même taille.
    """
    ch, k, nz, et, q, qtxt, reste = analyse(dividende, b, zeros)
    n = len(ch)
    virgule = ("," in dividende) or zeros > 0
    CW, RH, GAP = .36, .62, .12
    L = []
    prepa = jusqua == -1
    nmax = len(et) - 1 if jusqua is None else jusqua
    cres = VERT if mode == "corrige" else NAVY

    def X(i):
        return i * CW + (GAP if (virgule and i >= k) else 0)

    def coul_etape(j, defaut=INK):
        return NAVY if (actif is not None and j == actif) else defaut

    def nombre(valeur_, fin, y, coul, gras=False):
        s = str(valeur_)
        g = r",font=\fontsize{12.5}{15}\selectfont\bfseries" if gras else ""
        for j, c in enumerate(s):
            i = fin - (len(s) - 1) + j
            L.append(r"\node[ch,text=%s%s] at (%s,%s) {$%s$};" % (coul, g, f(X(i)), f(y), c))
        return fin - (len(s) - 1)

    # dividende (zéros ajoutés en gris)
    for i, c in enumerate(ch):
        coul = MUET if i >= n - nz else INK
        L.append(r"\node[ch,text=%s] at (%s,0) {$%d$};" % (coul, f(X(i)), c))
    if virgule:
        L.append(r"\node[ch] at (%s,0) {$,$};" % f(X(k - 1) + CW / 2 + GAP / 2 - .02))

    # Lignes de calcul. Méthode longue : une étape où le diviseur « ne va pas »
    # (chiffre 0 au quotient) n'écrit rien, le chiffre suivant est abaissé à côté.
    row = 0
    vus = set()
    y_partiel = {}
    for j, (e, partiel, qd, r) in enumerate(et):
        if j > nmax:
            break
        c_et = coul_etape(j)
        if courte:
            if j > 0:
                row += 1
                nombre(partiel, e, -row * RH, ORANGE if (suite and partiel in vus) else c_et)
                y_partiel[j] = -row * RH
            vus.add(partiel)
        elif qd > 0:
            if j > 0:
                row += 1
                nombre(partiel, e, -row * RH, ORANGE if (suite and partiel in vus) else c_et)
                y_partiel[j] = -row * RH
            vus.add(partiel)
            row += 1
            y = -row * RH
            debut = nombre(qd * b, e, y, c_et)
            L.append(r"\node[ch,text=%s] at (%s,%s) {$-$};" % (c_et, f(X(debut) - CW * .95), f(y)))
            L.append(r"\draw[filet] (%s,%s) -- (%s,%s);" % (f(X(debut) - CW * 1.35), f(y - .24), f(X(e) + CW * .45), f(y - .24)))

    if prepa:
        fini = False
        jfin = -1
        yr = -2 * RH
        xr = 0
    else:
        jfin = min(nmax, len(et) - 1)
        e_f, _, _, r_f = et[jfin]
        fini = jfin == len(et) - 1
        row += 1
        yr = -row * RH
        if suite and fini:
            coul = ORANGE
        elif actif is not None:
            coul = coul_etape(jfin)
        else:
            coul = cres if fini else INK
        xr = nombre(r_f, e_f, yr, coul, gras=fini and mode == "corrige")

    if cadre:
        # nombre de lignes de la division complète
        if courte:
            total = len(et)
        else:
            total = sum((1 if (j > 0 and x[2] > 0) else 0) + (1 if x[2] > 0 else 0) for j, x in enumerate(et)) + 1
        yr = -total * RH

    # flèche du chiffre abaissé
    if abaisse is not None and abaisse in y_partiel:
        xa = X(et[abaisse][0])
        L.append(r"\draw[descend] (%s,%s) -- (%s,%s);" % (f(xa), f(-.14), f(xa), f(y_partiel[abaisse] + .4)))

    # accolade sous le premier morceau du dividende (préparation)
    if accolade:
        e0 = et[0][0]
        L.append(r"\draw[accol,%s] (%s,-.2) -- (%s,-.2);" % (NAVY, f(X(e0) + .16), f(X(0) - .16)))
        L.append(r"\node[note,anchor=north,text=%s] at (%s,-.42) {%s};" % (NAVY, f((X(0) + X(e0)) / 2), accolade))

    qch = [str(x[2]) for x in et[:jfin + 1]]
    if style == "anglais":
        # ) et barre au-dessus du dividende, diviseur à gauche, quotient en haut
        x0 = X(0) - .3
        L.append(r"\draw[potence] (%s,.46) .. controls (%s,.2) and (%s,-.02) .. (%s,-.26);" % (
            f(x0), f(x0 + .17), f(x0 + .17), f(x0 - .02)))
        L.append(r"\draw[potence] (%s,.46) -- (%s,.46);" % (f(x0), f(X(n - 1) + .3)))
        L.append(r"\node[ch,anchor=base east] at (%s,0) {$%d$};" % (f(x0 - .12), b))
        for j, (e, _, qd, _) in enumerate(et[:jfin + 1]):
            L.append(r"\node[ch,text=%s] at (%s,.66) {$%d$};" % (cres if actif is None else coul_etape(j), f(X(e)), qd))
        if fini and reste and not virgule:
            L.append(r"\node[note,text=%s] at (%s,.66) {r %d};" % (cres, f(X(n - 1) + .3), int(reste)))
        xg, xd = x0 - .5, X(n - 1) + .3
        ybas = yr - .3
    else:
        xb = X(n - 1) + CW * .5 + .22
        ybas = yr - .3
        L.append(r"\draw[potence] (%s,.5) -- (%s,%s);" % (f(xb), f(xb), f(ybas)))
        if fini:
            qaff = qtxt + (r"\ldots" if suite else "")
        else:
            avant = k - et[0][0]
            qs = "".join(qch)
            qaff = qs[:avant] + "{,}" + qs[avant:] if (len(ch) > k and len(qs) > avant > 0) else qs
        nq = len(qtxt.replace("{,}", "")) + (1 if "{,}" in qtxt else 0)
        larg = max(len(str(b)) * .25, nq * .235 + (.35 if suite else 0), (len(slots) * .3 if slots else 0)) + .55
        L.append(r"\draw[potence] (%s,-.22) -- (%s,-.22);" % (f(xb), f(xb + larg)))
        L.append(r"\node[ch,anchor=base west] (dv) at (%s,0) {$%d$};" % (f(xb + .22), b))
        if slots:
            for i, lettre in enumerate(slots):
                xs = xb + .22 + .125 + i * .3
                L.append(r"\node[ent] at (%s,%s) {%s};" % (f(xs), f(-RH - .5), lettre))
                if i >= len(qch):
                    L.append(r"\node[ch,text=%s] at (%s,%s) {$\cdot$};" % (MUET, f(xs), f(-RH)))
            for i, c in enumerate(qch):
                xs = xb + .22 + .125 + i * .3
                coul = coul_etape(i) if actif is not None else cres
                L.append(r"\node[ch,text=%s] at (%s,%s) {$%s$};" % (coul, f(xs), f(-RH), c))
        elif qaff:
            L.append(r"\node[ch,text=%s,font=\fontsize{12.5}{15}\selectfont\bfseries,anchor=base west] (qt) at (%s,%s) {$%s$};" % (
                cres, f(xb + .22), f(-RH), qaff))
        if noms:
            cl = NAVY
            L.append(r"\node[anchor=east,text=%s] (ld) at (%s,.1) {dividende};" % (cl, f(X(0) - .75)))
            L.append(r"\draw[fl,%s] (ld.east) -- (%s,.1);" % (cl, f(X(0) - .2)))
            L.append(r"\node[anchor=east,text=%s] (lr) at (%s,%s) {reste};" % (cl, f(X(0) - .75), f(yr + .1)))
            L.append(r"\draw[fl,%s] (lr.east) -- (%s,%s);" % (cl, f(X(xr) - .2), f(yr + .1)))
            xd_ = xb + larg + .45
            L.append(r"\node[anchor=west,text=%s] (lb) at (%s,.1) {diviseur};" % (cl, f(xd_)))
            L.append(r"\draw[fl,%s] (lb.west) -- ([xshift=1.5mm]dv.east);" % cl)
            L.append(r"\node[anchor=west,text=%s] (lq) at (%s,%s) {quotient};" % (cl, f(xd_), f(-RH + .1)))
            L.append(r"\draw[fl,%s] (lq.west) -- ([xshift=1.5mm]qt.east);" % cl)
        xg, xd = X(0), xb + larg
    if egalite is None and fini and not suite and not virgule:
        r_ = int(reste)
        egalite = r"$%s = %d \times %s + %s$ \quad avec \quad $%s < %d$" % (
            nombre_tex(dividende), b, nombre_tex(qtxt.replace("{,}", ",")), r_, r_, b)
    if egalite:
        L.append(r"\node[anchor=north,text=%s,align=center] at (%s,%s) {%s};" % (
            NAVY, f((xg + xd) / 2), f(ybas - .25), egalite))
    if cadre:
        L.append(r"\path (%s,%s) rectangle (%s,.7);" % (f(X(0) - 1.0), f(ybas - .05), f(xd + .1)))
    return tikz(L + list(extra or [])), qtxt, reste


def ensemble(morceaux, titres=None, ytitre=1.25):
    """Plusieurs figures côte à côte : morceaux = [(code_tikz, decalage_x)]."""
    L = []
    for i, (code, dx) in enumerate(morceaux):
        corps = code.replace("\\begin{tikzpicture}\n", "").replace("\n\\end{tikzpicture}", "")
        L.append(r"\begin{scope}[xshift=%scm]" % f(dx))
        L.append(corps)
        if titres:
            t, xt = titres[i]
            L.append(r"\node[titreF] at (%s,%s) {%s};" % (f(xt), f(ytitre), t))
        L.append(r"\end{scope}")
    return tikz(L)


def multiples(b, n=9, x0=0.0, y0=0.0, surligne=(), RH=.5):
    """Table des multiples de b (1 à n) en deux colonnes « k × b | valeur »."""
    L = []
    L.append(r"\node[titreF,anchor=base west] at (%s,%s) {multiples de %d};" % (f(x0 - .05), f(y0 + .55), b))
    for k in range(1, n + 1):
        y = y0 - (k - 1) * RH
        coul = NAVY if k in surligne else GRIS
        L.append(r"\node[note,anchor=base east,text=%s] at (%s,%s) {%d\,$\times$\,%d};" % (coul, f(x0 + 1.05), f(y), k, b))
        L.append(r"\node[ch,anchor=base east,text=%s,font=\fontsize{11}{13}\selectfont%s] at (%s,%s) {$%s$};" % (
            NAVY if k in surligne else INK, r"\bfseries" if k in surligne else "", f(x0 + 2.05), f(y), milliers(k * b)))
    L.append(r"\draw[filet,otRule] (%s,%s) -- (%s,%s);" % (f(x0 + 1.25), f(y0 + .38), f(x0 + 1.25), f(y0 - (n - 1) * RH - .18)))
    return L


# ===================================================================== multiplication par jalousie
def jalousie_calcul(a, b):
    """Bandes diagonales de la multiplication par jalousie (per gelosia).

    Renvoie (cellules, bandes, chiffres, retenues) : bandes[k] = liste des
    chiffres de la bande k (k = 0 en haut à gauche) ; chiffres[k] = chiffre écrit ;
    retenues[k] = retenue reçue de la bande k + 1.
    """
    A, B = [int(c) for c in a], [int(c) for c in b]
    n, m = len(A), len(B)
    cell = {(c, r): divmod(A[c] * B[r], 10) for c in range(n) for r in range(m)}
    bandes = {k: [] for k in range(n + m)}
    for (c, r), (t, u) in cell.items():
        bandes[c + r].append(t)
        bandes[c + r + 1].append(u)
    chiffres, retenues = {}, {}
    ret = 0
    for k in range(n + m - 1, -1, -1):
        retenues[k] = ret
        s = sum(bandes[k]) + ret
        chiffres[k] = s % 10
        ret = s // 10
    assert ret == 0
    total = int("".join(str(chiffres[k]) for k in range(n + m)))
    assert total == int(a) * int(b), (a, b, total)
    return cell, bandes, chiffres, retenues


def jalousie(a, b, s=1.0, retenues=True):
    """Grille de la multiplication par jalousie de a (en haut) par b (à droite)."""
    cell, bandes, chiffres, rets = jalousie_calcul(a, b)
    n, m = len(a), len(b)
    L = []
    # quadrillage
    L.append(r"\fill[otSky] (0,%s) rectangle (%s,0);" % (f(-m * s), f(n * s)))
    for c in range(n + 1):
        L.append(r"\draw[otNavy,line width=.8pt] (%s,0) -- (%s,%s);" % (f(c * s), f(c * s), f(-m * s)))
    for r in range(m + 1):
        L.append(r"\draw[otNavy,line width=.8pt] (0,%s) -- (%s,%s);" % (f(-r * s), f(n * s), f(-r * s)))
    # diagonales (x - y = d), prolongées hors de la grille vers le bas à gauche
    e = .78
    for k in range(1, n + m):
        d = k * s
        x1, y1 = (d, 0) if d <= n * s else (n * s, n * s - d)
        x2, y2 = (0, -d) if d <= m * s else (d - m * s, -m * s)
        L.append(r"\draw[otMuted,line width=.6pt] (%s,%s) -- (%s,%s);" % (f(x1), f(y1), f(x2 - e), f(y2 - e)))
    # chiffres des cases : dizaines en haut à gauche, unités en bas à droite
    for (c, r), (t, u) in cell.items():
        x0, y0 = c * s, -(r + 1) * s
        L.append(r"\node[ch,anchor=center] at (%s,%s) {$%d$};" % (f(x0 + .3 * s), f(y0 + .7 * s), t))
        L.append(r"\node[ch,anchor=center] at (%s,%s) {$%d$};" % (f(x0 + .7 * s), f(y0 + .3 * s), u))
    # facteurs
    for c, ch in enumerate(a):
        L.append(r"\node[ch,anchor=center,text=%s,font=\fontsize{12.5}{15}\selectfont\bfseries] at (%s,.38) {$%s$};" % (NAVY, f((c + .5) * s), ch))
    for r, ch in enumerate(b):
        L.append(r"\node[ch,anchor=center,text=%s,font=\fontsize{12.5}{15}\selectfont\bfseries] at (%s,%s) {$%s$};" % (NAVY, f(n * s + .38), f(-(r + .5) * s), ch))
    L.append(r"\node[ch,anchor=center,text=%s] at (%s,.38) {$\times$};" % (GRIS, f(n * s + .38)))
    # résultat de chaque bande (sorties à gauche puis en bas)
    for k in range(n + m):
        if k < m:
            mx, my = 0, -(k + .5) * s
        else:
            mx, my = (k - m + .5) * s, -m * s
        zero_tete = k == 0 and chiffres[0] == 0
        L.append(r"\node[ch,anchor=center,text=%s] at (%s,%s) {$%d$};" % (
            MUET if zero_tete else VERT, f(mx - .44), f(my - .44), chiffres[k]))
        if retenues and rets[k]:
            L.append(r"\node[ret,anchor=center] at (%s,%s) {$+%d$};" % (f(mx - .2), f(my - .2), rets[k]))
    return tikz(L), chiffres, bandes, rets


# ===================================================================== aperçu des cartes
def apercu(code, larg=6.0, haut=3.75):
    """Figure centrée dans un cadre fixe (16/10) : les cartes de la rubrique
    affichent toutes leurs chiffres à la même taille."""
    corps = code.replace("\\begin{tikzpicture}\n", "").replace("\n\\end{tikzpicture}", "")
    return tikz([
        r"\begin{scope}[local bounding box=F]",
        corps,
        r"\end{scope}",
        r"\pgfresetboundingbox",
        r"\path ($(F.center)+(%s,%s)$) rectangle ($(F.center)+(%s,%s)$);" % (f(-larg / 2), f(-haut / 2), f(larg / 2), f(haut / 2)),
    ])
