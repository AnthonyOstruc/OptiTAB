# -*- coding: utf-8 -*-
"""Vérification mathématique de la notion 273 (5e : angles et droites parallèles).

    python verif_273.py

1. Figures : chaque arc qui porte une mesure (enregistré par figures/figures.py dans
   DONNEES) est recalculé avec sympy à partir des points réellement dessinés ; les
   droites annoncées parallèles ont la même direction, les autres non.
2. Positions : les paires annoncées « alternes-internes », « correspondants »,
   « opposés par le sommet » sont reconnues géométriquement sur les figures.
3. Réponses : chaque calcul des exercices, du cours et de la fiche (valeurs exactes).
4. Contrôle automatique : toute égalité numérique écrite entre $…$ (mesures en degrés,
   chaînes « a = b = c », « ≠ ») est recalculée exactement.
5. Structure : 10 exercices + 11 retirés = 21 Id, progression, corrigés complets
   (étapes, résultat par question, erreur fréquente), solutions numérotées, images
   déclarées, aucune mention du brevet.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
ok, ko = 0, []


def check(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        ko.append(msg)


spec = importlib.util.spec_from_file_location("fig273", ICI / "figures" / "figures.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)


# ===================================================================== 1. angles dessinés
def mesure(o, p, q):
    """Angle (en degrés, sympy) de [op) à [oq) dans le sens direct."""
    o, p, q = [tuple(sp.Float(c, 30) for c in v) for v in (o, p, q)]
    a1 = sp.atan2(p[1] - o[1], p[0] - o[0])
    a2 = sp.atan2(q[1] - o[1], q[0] - o[0])
    d = sp.N((a2 - a1) * 180 / sp.pi, 25) % 360
    return d


n_arcs = 0
for nom, d in F.DONNEES.items():
    for (o, p, q, val) in d["angles"]:
        m = mesure(o, p, q)
        n_arcs += 1
        check(abs(m - val) < 1e-6, f"{nom} : arc annoncé {val}°, dessiné {float(m):.4f}°")
    for (t1, t2, noms) in d["paralleles"]:
        check(abs(((t1 - t2) % 180)) < 1e-9 or abs(((t1 - t2) % 180) - 180) < 1e-9, f"{nom} : {noms} non parallèles")
    for (t1, t2, noms) in d["secantes"]:
        check(abs((t1 - t2) % 180) > 0.5, f"{nom} : {noms} devraient être sécantes")
check(n_arcs >= 60, f"trop peu d'arcs contrôlés ({n_arcs})")

# toutes les figures déclarées existent et sont appelées
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
utilisees = {v["fichier"] for sec in corr.values() for doc in sec.values() for v in doc.values()}
check(utilisees == {n + ".png" for n in F.FIGURES}, "figures définies ≠ figures utilisées : %s"
      % (utilisees ^ {n + ".png" for n in F.FIGURES}))
for fch in utilisees:
    check((ICI / "figures" / "images" / fch).exists(), f"image absente : {fch}")
for sec in corr.values():
    for doc in sec.values():
        for v in doc.values():
            check(len(v["alt"]) >= 15, f"alt trop court : {v}")


# ===================================================================== 2. positions des angles
def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


class Config:
    """Droites (d) par A (direction td) et (e) par B (direction te), sécante (AB)."""

    def __init__(self, A, td, B, te):
        self.A, self.td, self.B, self.te = A, td, B, te
        self.ts = F.direc(B, A)

    def point(self, som, pos):
        P, t = (self.A, self.td) if som == "A" else (self.B, self.te)
        p, q = F.secteur(P, t, self.ts, pos)
        a1, a2 = F.direc(P, p), F.direc(P, q)
        sw = (a2 - a1) % 360
        return P, t, F.pol(P, 0.3, a1 + sw / 2), sw

    def info(self, som, pos):
        P, t, X, sw = self.point(som, pos)
        u_d = (sp.cos(sp.rad(self.td)), sp.sin(sp.rad(self.td)))
        u_e = (sp.cos(sp.rad(self.te)), sp.sin(sp.rad(self.te)))
        u_s = (sp.cos(sp.rad(self.ts)), sp.sin(sp.rad(self.ts)))
        cote_d = sp.sign(cross(u_d, sub(X, self.A)))
        cote_e = sp.sign(cross(u_e, sub(X, self.B)))
        interne = (cote_d == sp.sign(cross(u_d, sub(self.B, self.A)))) and \
                  (cote_e == sp.sign(cross(u_e, sub(self.A, self.B))))
        u_t = u_d if som == "A" else u_e
        return {"som": som, "interne": interne, "cote_s": sp.sign(cross(u_s, sub(X, self.B))),
                "dessus": sp.sign(cross(u_t, sub(X, P))), "mesure": sw}


def alternes_internes(c, a, b):
    i, j = c.info(*a), c.info(*b)
    return i["som"] != j["som"] and i["interne"] and j["interne"] and i["cote_s"] != j["cote_s"]


def correspondants(c, a, b):
    i, j = c.info(*a), c.info(*b)
    return i["som"] != j["som"] and i["cote_s"] == j["cote_s"] and i["dessus"] == j["dessus"]


POS = ("hd", "hg", "bg", "bd")

# --- 2958 : droites non parallèles, angles numérotés 1-4 (A) et 5-8 (B)
B58 = (0.0, 0.0)
A58 = F.pol(B58, 2.9, F.TS58)
c58 = Config(A58, F.TD58, B58, 0)
num = {k + 1: ("A", POS[k]) for k in range(4)}
num.update({k + 5: ("B", POS[k]) for k in range(4)})
internes = sorted(k for k in num if c58.info(*num[k])["interne"])
check(internes == [3, 4, 5, 6], f"2958 : angles internes {internes}")
ai = sorted(tuple(sorted((a, b))) for a in num for b in num if a < b and alternes_internes(c58, num[a], num[b]))
check(ai == [(3, 5), (4, 6)], f"2958 : alternes-internes {ai}")
co = sorted(tuple(sorted((a, b))) for a in num for b in num if a < b and correspondants(c58, num[a], num[b]))
check(co == [(1, 5), (2, 6), (3, 7), (4, 8)], f"2958 : correspondants {co}")
mes = {k: round(float(c58.info(*num[k])["mesure"]), 6) for k in num}
check(mes[1] == 64 and mes[5] == 52, f"2958 : angles 1 et 5 dessinés {mes[1]}, {mes[5]}")
check(mes[3] == mes[1] == 64, "2958 : angle 3 = angle 1 (opposés)")
check(mes[6] == 180 - 52 == 128, "2958 : angle 6 = 128")
for a, b in ((1, 3), (2, 4), (5, 7), (6, 8)):
    check(mes[a] == mes[b], f"2958 : opposés {a}, {b}")
check(mes[3] != mes[5], "2958 : alternes-internes inégaux (non parallèles)")

# --- cours_secante : paires de la figure (orange = alternes-internes, vert = correspondants)
Bc = (0.0, 0.0)
cS = Config(F.pol(Bc, 2.5, 56), -9, Bc, 0)
check(alternes_internes(cS, ("A", "bg"), ("B", "hd")), "cours : paire alternes-internes")
check(correspondants(cS, ("A", "hd"), ("B", "hd")), "cours : paire correspondants")

# --- 2962 : (d) // (e), ts = 62
B62 = (0.0, 0.0)
A62 = (2.5 / F.math.tan(F.math.radians(62)), 2.5)
c62 = Config(A62, 0, B62, 0)
noms62 = {"MAS": ("A", "hg"), "NAS": ("A", "hd"), "NAB": ("A", "bd"), "MAB": ("A", "bg"),
          "PBA": ("B", "hg"), "ABQ": ("B", "hd"), "QBT": ("B", "bd"), "PBT": ("B", "bg")}
val62 = {"MAS": 118, "NAS": 62, "NAB": 118, "MAB": 62, "PBA": 118, "ABQ": 62, "QBT": 118, "PBT": 62}
for k, v in noms62.items():
    check(round(float(c62.info(*v)["mesure"]), 6) == val62[k], f"2962 : {k}")
check(alternes_internes(c62, noms62["MAB"], noms62["ABQ"]), "2962 : MAB / ABQ alternes-internes")
check(correspondants(c62, noms62["MAS"], noms62["PBA"]), "2962 : MAS / PBA correspondants")
check(180 - 118 == 62 and len(set(val62.values())) == 2 and 62 + 118 == 180, "2962 : calculs")

# --- 2961 : figure 1 alternes-internes 58/58 ; figure 2 correspondants 73/75
B61 = (0.0, 0.0)
c61 = Config((2.2 / F.math.tan(F.math.radians(58)), 2.2), 0, B61, 0)
check(alternes_internes(c61, ("A", "bg"), ("B", "hd")), "2961 : figure 1 alternes-internes")
D61 = (0.0, -4.9)
c61b = Config(F.pol(D61, 2.4, 75), 2, D61, 0)
check(correspondants(c61b, ("A", "hd"), ("B", "hd")), "2961 : figure 2 correspondants")
check(round(float(c61b.info("A", "hd")["mesure"]), 6) == 73 and round(float(c61b.info("B", "hd")["mesure"]), 6) == 75,
      "2961 : 73° et 75° dessinés")
check(73 != 75 and (75 - 73) == 2, "2961 : directions différentes de 2°")

# --- 2974 : intérieurs du même côté 112 / 68
B74 = (0.0, 0.0)
c74 = Config((2.4 / F.math.tan(F.math.radians(68)), 2.4), 0, B74, 0)
i1, i2 = c74.info("A", "bd"), c74.info("B", "hd")
check(i1["interne"] and i2["interne"] and i1["cote_s"] == i2["cote_s"], "2974 : même côté, internes")
check(not alternes_internes(c74, ("A", "bd"), ("B", "hd")) and not correspondants(c74, ("A", "bd"), ("B", "hd")),
      "2974 : ni alternes-internes ni correspondants")
check(alternes_internes(c74, ("A", "bg"), ("B", "hd")), "2974 : angle trouvé alterne-interne")
check(180 - 112 == 68 and 112 + 68 == 180 and 68 != 70, "2974 : calculs")

# --- 2965 : poteaux // , rampe sécante
d65 = F.DONNEES["ex2965_corrige"]
A65, B65 = (0.0, 1.0), (3.6, 1.0 + 3.6 * F.math.tan(F.math.radians(34)))
u_r, u_p = (F.math.cos(F.math.radians(34)), F.math.sin(F.math.radians(34))), (0.0, 1.0)


def bis(o, a1, a2):
    return F.pol(o, 0.3, (a1 + a2) / 2)


X_DAB, X_EBR = bis(A65, 34, 90), bis(B65, 34, 90)          # angles DAB et EBR
X_ABE = bis(B65, 90, 214)                                   # angle ABE
X_P, X_Q = bis((0.0, 0.0), 0, 90), bis((3.6, 0.0), 0, 90)   # angles droits en P et Q
# correspondants pour la rampe : même côté de la rampe, même côté de leur poteau
check(cross(u_r, sub(X_DAB, A65)) * cross(u_r, sub(X_EBR, A65)) > 0
      and cross(u_p, sub(X_DAB, A65)) * cross(u_p, sub(X_EBR, B65)) > 0, "2965 : DAB / EBR correspondants")
# correspondants pour le sol : au-dessus du sol, à droite de chaque poteau
check(X_P[1] > 0 and X_Q[1] > 0 and X_P[0] > 0 and X_Q[0] > 3.6, "2965 : angles droits correspondants")
check(cross(u_r, sub(X_ABE, A65)) * cross(u_r, sub(X_EBR, A65)) > 0, "2965 : ABE et EBR du même côté de la rampe")
check(90 - 56 == 34 and 180 - 56 == 124, "2965 : calculs")
check(any(v == 34 for (_, _, _, v) in d65["angles"]) and any(v == 124 for (_, _, _, v) in d65["angles"]),
      "2965 : 34° et 124° dessinés")

# --- 2971 : triangle 48 / 67
check(180 - 48 - 67 == 65 and 48 + 67 + 65 == 180, "2971 : calculs")
# --- 2972 : point entre deux parallèles
check(42 + 31 == 73 and 180 - 73 == 107 and 90 - 42 == 48, "2972 : calculs")
# --- 2959, 2957, 2960
check(90 - 34 == 56 and 180 - 34 == 146 and 34 + 56 == 90 and 34 + 146 == 180, "2959 : calculs")
check(90 - 72 == 18 and 180 - 72 == 108 and 35 + 55 == 90 and 120 + 70 == 190, "2959 : complément, supplément")
check(180 - 38 == 142 and 38 + 142 + 38 + 142 == 360 and 180 / 2 == 90, "2957 : calculs")
check(180 - 147 == 33 and 180 - 70 == 110, "2960 : calculs")
# rapporteur : la graduation intérieure vaut 180 − t, l'extérieure t (t = direction de [Oy))
check((128, 180 - 128) == (128, 52), "cours : lecture 128° / piège 52°")
check(180 - 147 == 33, "2960 : lecture intérieure 33° (extérieure 147°)")
# cours
check(90 - 28 == 62 and 180 - 28 == 152 and 180 - 40 == 140 and 180 - 50 == 130, "cours : calculs")

# ===================================================================== 3. égalités écrites
FICHIERS = [ICI / "cours_268.txt", ICI / "fiche_188.txt", ICI / "exercices.txt"]


def num_expr(s):
    """Expression purement numérique (degrés retirés) ou None."""
    s = s.replace(r"^\circ", "").replace(r"^{\circ}", "").replace("°", "").replace(r"\,", "")
    s = s.replace(r"\times", "*").replace(r"\div", "/").replace("{,}", ".").replace(" ", "")
    s = s.replace(r"\left", "").replace(r"\right", "")
    if not s or not re.fullmatch(r"[0-9.+\-*/()]+", s) or not re.search(r"\d", s):
        return None
    try:
        return sp.nsimplify(s)
    except Exception:
        return None


n_eg = 0
for fch in FICHIERS:
    texte = fch.read_text(encoding="utf-8")
    for m in re.finditer(r"\$\$(.+?)\$\$|\$(.+?)\$", texte, re.S):
        f_ = m.group(1) or m.group(2)
        for morceau in re.split(r"\\\\", f_):
            morceau = morceau.replace("&", "")
            if r"\neq" in morceau:
                g, d = morceau.split(r"\neq", 1)
                vg, vd = num_expr(g), num_expr(d)
                if vg is not None and vd is not None:
                    n_eg += 1
                    check(vg != vd, f"{fch.name} : « {morceau.strip()} » est une égalité")
                continue
            parts = morceau.split("=")
            if len(parts) < 2:
                continue
            vals = [num_expr(p) for p in parts]
            nums = [v for v in vals if v is not None]
            if len(nums) >= 2:
                n_eg += 1
                check(len(set(nums)) == 1, f"{fch.name} : « {morceau.strip()} » faux ({nums})")
            
# ===================================================================== 4. structure
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b for b in re.split(r"^===\s*$", ex, flags=re.M) if b.strip()]
GARDES = [2959, 2957, 2958, 2962, 2961, 2960, 2974, 2965, 2971, 2972]
ids = [int(re.search(r"^Id: (\d+)", b, re.M).group(1)) for b in blocs]
check(ids == GARDES, f"Id des exercices : {ids}")
retires = [int(l.split("#")[0]) for l in (ICI / "exercices_retires.txt").read_text(encoding="utf-8").splitlines()
           if l.strip() and not l.startswith("#")]
src = (ICI / "source_en_ligne" / "exercices.txt").read_text(encoding="utf-8")
ids_src = [int(x) for x in re.findall(r"^Id: (\d+)", src, re.M)]
check(sorted(ids + retires) == sorted(ids_src) and len(ids_src) == 21, "Id gardés + retirés ≠ Id en ligne")
types = [re.search(r"^=== (\w+)", b.strip(), re.M).group(1) for b in blocs]
check(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"],
      f"progression : {types}")
titres = [re.search(r"^=== (.+)$", b.strip(), re.M).group(1) for b in blocs]
check(len(set(titres)) == 10, "titres en double")
diff = {"Découverte": "easy", "Entraînement": "medium", "Problème": "hard", "Synthèse": "hard"}
for b, t, i in zip(blocs, types, ids):
    check(re.search(r"^Difficulté: (\w+)", b, re.M).group(1) == diff[t], f"{i} : difficulté")
    enonce = b.split("Énoncé:")[1].split("Étapes:")[0]
    etapes = b.split("Étapes:")[1].split("Solution:")[0]
    solution = b.split("Solution:")[1]
    nq = len(re.findall(r"^\d+\. ", enonce, re.M))
    qs = re.split(r"^## Question \d+", etapes, flags=re.M)[1:]
    check(len(qs) == nq, f"{i} : {nq} questions, {len(qs)} corrigées")
    for k, q in enumerate(qs, 1):
        check(q.count("::: resultat") == 1, f"{i} Q{k} : un résultat")
        check("::: etape" in q, f"{i} Q{k} : au moins une étape")
    check("::: attention" in etapes, f"{i} : erreur fréquente")
    check(len(re.findall(r"^\d+\. ", solution, re.M)) == nq, f"{i} : solution incomplète")
    imgs = set(re.findall(r"\[IMAGE_(\d+)\]", b))
    decl = set(corr["exercices"].get(str(i), {}).keys())
    check(imgs == decl and imgs, f"{i} : images {imgs} / déclarées {decl}")
    check(enonce.count("[IMAGE_") >= 1 and etapes.count("[IMAGE_") >= 1, f"{i} : figure énoncé + corrigé")
for nomf, cle, idd in (("cours_268.txt", "cours", "268"), ("fiche_188.txt", "fiches", "188")):
    t = (ICI / nomf).read_text(encoding="utf-8")
    check(set(re.findall(r"\[IMAGE_(\d+)\]", t)) == set(corr[cle][idd].keys()), f"{nomf} : images")
for fch in FICHIERS:
    check("brevet" not in fch.read_text(encoding="utf-8").lower(), f"{fch.name} : mention du brevet")

# « \widehat{XYZ} = a - b = c » : la partie numérique doit être cohérente
check(n_eg >= 30, f"trop peu d'égalités numériques contrôlées ({n_eg})")

# « \widehat{XYZ} = … = N° » : la mesure écrite est celle de la figure de l'exercice
VALEURS = {
    2959: {"AOB": 34, "BOC": 56, "BOD": 146, "AOC": 90, "AOD": 180},
    2957: {"AOC": 38, "BOD": 38, "AOD": 142, "BOC": 142},
    2962: val62,
    2960: {"xOy": 33},
    2965: {"DAB": 56, "EBR": 56, "ABE": 124},
    2971: {"ABC": 48, "ACB": 67, "DAB": 48, "EAC": 67, "CAE": 67, "BAC": 65, "DAE": 180},
    2972: {"DAM": 42, "EBM": 31, "AMN": 42, "NMB": 31, "AMB": 73, "BMK": 107},
}
# situations hypothétiques annoncées comme telles dans les énoncés (questions « Si … »)
HYPOTHESES = {(2957, "AOC", 90), (2972, "EBM", 48), (2972, "AMB", 90)}


def cle(n):
    return n[1] + "".join(sorted(n[0] + n[2]))


n_noms = 0
for b, i in zip(blocs, ids):
    if i not in VALEURS:
        continue
    table = {cle(k): v for k, v in VALEURS[i].items()}
    for m in re.finditer(r"\$\$(.+?)\$\$|\$(.+?)\$", b, re.S):
        f_ = m.group(1) or m.group(2)
        parts = [p.replace("&", "").strip() for p in re.split(r"=|\\\\", f_)]
        nums = [num_expr(p) for p in parts]
        nums = [v for v in nums if v is not None]
        if not nums:
            continue
        val = nums[-1]
        for p in parts:
            mm = re.fullmatch(r"\\widehat\{(\w)(\w)(\w)\}", p)
            if mm and "=" in f_:
                n = "".join(mm.groups())
                if (i, n, val) in HYPOTHESES:
                    continue
                n_noms += 1
                check(table.get(cle(n)) == val, f"{i} : $\\widehat{{{n}}}$ écrit {val}, figure {table.get(cle(n))}")
check(n_noms >= 25, f"trop peu de mesures nommées contrôlées ({n_noms})")

print(f"verif_273 : {ok} contrôles OK, {len(ko)} erreur(s) ; {n_arcs} arcs de figures, {n_eg} égalités écrites, {n_noms} mesures nommées.")
for m in ko:
    print("  ✗", m)
sys.exit(1 if ko else 0)
