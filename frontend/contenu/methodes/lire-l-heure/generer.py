# -*- coding: utf-8 -*-
"""Page « Lire l'heure » (methodes/lire-l-heure) : texte, fiches PDF et contrôles.

    python -I -X utf8 generer.py

1. Contrôle : la lecture de l'heure en mots écrite ici (corrigés des fiches) et
   celle de l'horloge du site (scripts/ressources/outils/horloge.js) donnent le
   même texte pour les 1 440 minutes de la journée.
2. Écrit formulaire.md (ne pas le modifier à la main : modifier ce script).
3. Écrit les fiches PDF CP, CE1, CE2 et leurs corrigés dans
   public/ressources-gratuites/methodes/lire-l-heure/ (LuaLaTeX + TikZ).
Programme du cycle 2 (2025) : CP heures entières ; CE1 demi-heures, quarts
d'heure, matin et après-midi (14 h 15 = 2 heures et quart) ; CE2 heures et minutes.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
FRONT = ICI.parents[2]
sys.path.insert(0, str(FRONT / "cours" / "format_v1" / "outils"))
sys.path.insert(0, str(ICI))
from figures_livre import PREAMBULE  # noqa: E402
from horloge_tikz import BS, horloge  # noqa: E402

NBSP, NNBSP = chr(0xA0), chr(0x202F)
URL = "/ressources-gratuites/methodes/lire-l-heure/"
SORTIE_PDF = FRONT / "public" / URL.strip("/")
BUILD = ICI / "build"

# ---------------------------------------------------------------- lecture de l'heure
NB = ["zéro", "une", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze",
      "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
DIZ = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante"}


def nombre(n):
    if n < 20:
        return NB[n]
    d, u = divmod(n, 10)
    if u == 0:
        return DIZ[d]
    if u == 1:
        return DIZ[d] + " et une"
    return DIZ[d] + "-" + NB[u]


def chiffres(h, m):
    return f"{h}{NBSP}h{NBSP}{m:02d}"


def vingt_quatre(h, m):
    heures = "zéro heure" if h == 0 else "une heure" if h == 1 else nombre(h) + " heures"
    return heures + (" " + nombre(m) if m else "")


def nom_heure(h):
    if h % 24 == 0:
        return "minuit"
    if h == 12:
        return "midi"
    k = h % 12
    return "une heure" if k == 1 else nombre(k) + " heures"


def moment(h):
    if h in (0, 12):
        return ""
    return " du matin" if h < 12 else " de l’après-midi" if h < 18 else " du soir"


def parle(h, m):
    if m == 0:
        return nom_heure(h) + moment(h)
    if m == 15:
        return nom_heure(h) + " et quart" + moment(h)
    if m == 30:
        return nom_heure(h) + (" et demi" if h % 12 == 0 else " et demie") + moment(h)
    if m >= 35 and m % 5 == 0:
        h2 = (h + 1) % 24
        return nom_heure(h2) + (" moins le quart" if m == 45 else " moins " + nombre(60 - m)) + moment(h2)
    return nom_heure(h) + " " + nombre(m) + moment(h)


def sans_moment(texte):
    return re.sub(r" (du matin|de l’après-midi|du soir)$", "", texte)


def controler_avec_le_site():
    js = FRONT / "scripts" / "ressources" / "outils" / "horloge.js"
    code = ("const vm=require('vm'),fs=require('fs');const c={window:{},document:{querySelector:()=>null}};"
            "vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),c);const L=c.window.OTHeure,r=[];"
            "for(let t=0;t<1440;t++){const h=Math.floor(t/60),m=t%60;r.push([L.parle(h,m),L.vingtQuatre(h,m),L.chiffres(h,m)])}"
            "process.stdout.write(JSON.stringify(r))")
    sortie = subprocess.run(["node", "-e", code, str(js)], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    site = json.loads(sortie)
    for t, (p, v, c) in enumerate(site):
        h, m = divmod(t, 60)
        assert (p, v, c) == (parle(h, m), vingt_quatre(h, m), chiffres(h, m)), (h, m, p, parle(h, m))
    # Quelques lectures vérifiées à la main
    assert parle(14, 15) == "deux heures et quart de l’après-midi"
    assert parle(11, 45) == "midi moins le quart" and parle(12, 30) == "midi et demi"
    assert parle(8, 40) == "neuf heures moins vingt du matin" and parle(23, 55) == "minuit moins cinq"
    assert vingt_quatre(21, 31) == "vingt et une heures trente et une" and vingt_quatre(0, 5) == "zéro heure cinq"
    print("lecture de l’heure : identique au site pour les 1 440 minutes de la journée")


# ---------------------------------------------------------------- fiches PDF
FICHES = [
    {
        "niveau": "cp", "classe": "CP", "titre": "Les heures entières",
        "consigne": "A. Écris l’heure. Quand la grande aiguille est sur le 12, il est une heure entière : la petite aiguille montre l’heure. B. Dessine la petite aiguille.",
        "lire": [(3, 0), (7, 0), (12, 0), (5, 0), (9, 0), (1, 0), (10, 0), (6, 0), (11, 0)],
        "dessiner": [(4, 0, "4 heures"), (8, 0, "8 heures"), (2, 0, "2 heures")],
        "note": "Sur une horloge à aiguilles, 3 h peut aussi être 15 h, l’après-midi.",
    },
    {
        "niveau": "ce1", "classe": "CE1", "titre": "Demi-heures et quarts d’heure",
        "consigne": "A. Écris l’heure. Grande aiguille sur le 3 : et quart ; sur le 6 : et demie ; sur le 9 : moins le quart. B. Dessine les deux aiguilles.",
        "lire": [(2, 0), (4, 30), (7, 15), (9, 45), (11, 30), (6, 15), (1, 45), (3, 30), (12, 15)],
        "dessiner": [(5, 30, "5 h 30"), (8, 15, "huit heures et quart"), (15, 45, "15 h 45")],
        "note": "Sur une horloge à aiguilles, 7 h 15 peut aussi être 19 h 15 : l’après-midi et le soir, on ajoute 12 heures.",
    },
    {
        "niveau": "ce2", "classe": "CE2", "titre": "Heures et minutes",
        "consigne": "A. Écris l’heure en heures et minutes : compte les minutes de 5 en 5 à partir du 12, puis une par une. B. Dessine les deux aiguilles.",
        "lire": [(2, 5), (4, 20), (7, 35), (9, 50), (11, 10), (6, 25), (1, 40), (8, 12), (10, 47)],
        "dessiner": [(3, 25, "3 h 25"), (9, 50, "dix heures moins dix"), (17, 40, "17 h 40")],
        "note": "Sur une horloge à aiguilles, 4 h 20 peut aussi être 16 h 20 : l’après-midi, on ajoute 12 heures.",
    },
]

LARGEUR, HAUTEUR, R = 19.0, 27.4, 1.5
COLS = [LARGEUR / 6, LARGEUR / 2, 5 * LARGEUR / 6]
LIGNES_A = [-6.2, -10.9, -15.6]   # 4,7 cm par rangée : la réponse en mots du corrigé tient sous l’horloge
LIGNE_B = -21.6
LETTRES = "abcdefghijkl"


def page(fiche, corrige):
    vert = "otGreenDark"
    L = [rf"{BS}path (0,0) rectangle ({LARGEUR},{-HAUTEUR});"]
    L.append(rf"{BS}node[anchor=north west,inner sep=0pt,font={BS}otMedium{BS}fontsize{{11}}{{13}}{BS}selectfont{BS}bfseries,text=otNavy] at (0,0) {{OptiTAB}};")
    L.append(rf"{BS}node[anchor=north west,inner sep=0pt,font={BS}otRegular{BS}fontsize{{8.5}}{{10}}{BS}selectfont,text=otMuted] at (1.75,-.06) {{Fiche gratuite à imprimer}};")
    L.append(rf"{BS}node[anchor=north east,inner sep=4pt,font={BS}otMedium{BS}fontsize{{10}}{{12}}{BS}selectfont{BS}bfseries,text=white,fill=otNavy,rounded corners=3pt] at ({LARGEUR},.06) {{{fiche['classe']}}};")
    titre = f"Lire l’heure · {fiche['titre']}" + (" · Corrigé" if corrige else "")
    L.append(rf"{BS}node[anchor=north west,inner sep=0pt,font={BS}otMedium{BS}fontsize{{17}}{{20}}{BS}selectfont{BS}bfseries,text=otInk] at (0,-.85) {{{titre}}};")
    if corrige:
        L.append(rf"{BS}node[anchor=north west,inner sep=0pt,font={BS}otRegular{BS}fontsize{{10}}{{13}}{BS}selectfont,text=otInk,text width={LARGEUR}cm] at (0,-1.95) {{Réponses en vert. {fiche['note']}}};")
    else:
        L.append(rf"{BS}node[anchor=north west,inner sep=0pt,font={BS}otRegular{BS}fontsize{{10.5}}{{13}}{BS}selectfont,text=otInk] at (0,-1.95) {{Prénom : {BS}rule[-1pt]{{5.2cm}}{{.4pt}}{BS}qquad Date : {BS}rule[-1pt]{{3cm}}{{.4pt}}{BS}qquad Score : {BS}rule[-1pt]{{1.1cm}}{{.4pt}} / 12}};")
        L.append(rf"{BS}node[anchor=north west,inner sep=6pt,font={BS}otRegular{BS}fontsize{{10}}{{13}}{BS}selectfont,text=otInk,fill=otSky,rounded corners=4pt,text width={LARGEUR - 0.25}cm] at (0,-2.7) {{{fiche['consigne']}}};")
    section = rf"{BS}otMedium{BS}fontsize{{12.5}}{{15}}{BS}selectfont{BS}bfseries"
    L.append(rf"{BS}node[anchor=west,inner sep=0pt,font={section},text=otNavy] at (0,-4.25) {{A. Quelle heure est-il ?}};")
    for i, (h, m) in enumerate(fiche["lire"]):
        x, y = COLS[i % 3], LIGNES_A[i // 3]
        L.append(horloge(x, y, R, h, m))
        L.append(rf"{BS}node[anchor=north west,inner sep=0pt,font={BS}otMedium{BS}bfseries{BS}fontsize{{11}}{{13}}{BS}selectfont,text=otNavy] at ({x - R - 0.95},{y + R}) {{{LETTRES[i]})}};")
        bas = y - R - 0.42
        if corrige:
            reponse = f"{h} h" if fiche["niveau"] == "cp" else chiffres(h, m).replace(NBSP, " ")
            L.append(rf"{BS}node[anchor=north,inner sep=0pt,font={BS}otMedium{BS}bfseries{BS}fontsize{{13}}{{15}}{BS}selectfont,text={vert}] at ({x},{bas}) {{{reponse}}};")
            L.append(rf"{BS}node[anchor=north,inner sep=0pt,font={BS}otRegular{BS}fontsize{{9}}{{11}}{BS}selectfont,text={vert}] at ({x},{bas - 0.55}) {{{sans_moment(parle(h, m))}}};")
        elif fiche["niveau"] == "cp":
            L.append(rf"{BS}node[anchor=north,inner sep=0pt,font={BS}otRegular{BS}fontsize{{12}}{{14}}{BS}selectfont,text=otInk] at ({x},{bas}) {{{BS}rule[-1pt]{{1.6cm}}{{.5pt}} heures}};")
        else:
            L.append(rf"{BS}node[anchor=north,inner sep=0pt,font={BS}otRegular{BS}fontsize{{12}}{{14}}{BS}selectfont,text=otInk] at ({x},{bas}) {{{BS}rule[-1pt]{{1.2cm}}{{.5pt}} h {BS}rule[-1pt]{{1.2cm}}{{.5pt}}}};")
    consigne_b = "B. Dessine la petite aiguille." if fiche["niveau"] == "cp" else "B. Dessine les deux aiguilles."
    L.append(rf"{BS}node[anchor=west,inner sep=0pt,font={section},text=otNavy] at (0,{LIGNE_B + R + 1.0}) {{{consigne_b}}};")
    for i, (h, m, texte) in enumerate(fiche["dessiner"]):
        x = COLS[i]
        L.append(horloge(x, LIGNE_B, R, h if corrige else None, m if corrige else None))
        L.append(rf"{BS}node[anchor=north west,inner sep=0pt,font={BS}otMedium{BS}bfseries{BS}fontsize{{11}}{{13}}{BS}selectfont,text=otNavy] at ({x - R - 0.95},{LIGNE_B + R}) {{{LETTRES[9 + i]})}};")
        L.append(rf"{BS}node[anchor=north,inner sep=0pt,font={BS}otMedium{BS}fontsize{{12.5}}{{15}}{BS}selectfont,text=otInk] at ({x},{LIGNE_B - R - 0.42}) {{{texte}}};")
    L.append(rf"{BS}node[anchor=south,inner sep=0pt,font={BS}otRegular{BS}fontsize{{8}}{{10}}{BS}selectfont,text=otMuted] at ({LARGEUR / 2},{-HAUTEUR}) {{Fiche gratuite OptiTAB · Lire l’heure · {fiche['classe']} · www.optitab.net{URL}}};")
    return BS + "begin{tikzpicture}\n" + "\n".join(L) + "\n" + BS + "end{tikzpicture}"


def document(tikz):
    tete = PREAMBULE.replace(BS + "documentclass[border=6pt]{standalone}",
                             BS + "documentclass[11pt]{article}\n" + BS + "usepackage[a4paper,margin=10mm,top=11mm]{geometry}")
    return (tete + "\n" + BS + "pagestyle{empty}\n" + BS + "setlength{" + BS + "parindent}{0pt}\n"
            + BS + "hyphenpenalty=10000\n" + BS + "exhyphenpenalty=10000\n" + BS + "begin{document}\n"
            + tikz + "\n" + BS + "end{document}\n")


def compiler(nom, tex):
    BUILD.mkdir(exist_ok=True)
    (BUILD / f"{nom}.tex").write_text(tex, encoding="utf-8")
    r = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", f"{nom}.tex"],
                       cwd=BUILD, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode or not (BUILD / f"{nom}.pdf").exists():
        erreurs = [l for l in r.stdout.splitlines() if l.startswith("!")]
        raise SystemExit(f"{nom} : échec LuaLaTeX {erreurs[:3]}")
    SORTIE_PDF.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BUILD / f"{nom}.pdf", SORTIE_PDF / f"{nom}.pdf")


def ecrire_fiches():
    for fiche in FICHES:
        for corrige in (False, True):
            nom = f"lire-l-heure-{fiche['niveau']}-{'corrige' if corrige else 'fiche'}"
            compiler(nom, document(page(fiche, corrige)))
    shutil.rmtree(BUILD, ignore_errors=True)
    print(f"fiches : {len(FICHES) * 2} PDF dans {SORTIE_PDF}")


# ---------------------------------------------------------------- page
def tableau_apres_midi():
    lignes = ["| L’horloge indique | L’après-midi ou le soir | On dit |", "|---|---|---|"]
    for h in range(1, 12):
        lignes.append(f"| {h} h | {h + 12} h | {parle(h + 12, 0)} |")
    return "\n".join(lignes)


INFOS = {
    "slug": "lire-l-heure",
    "titre": "Lire l’heure : méthode, horloge interactive et exercices",
    "titreCourt": "Lire l’heure",
    "titreSeo": "Lire l’heure : horloge interactive, méthode et exercices",
    "description": "Apprendre à lire l’heure du CP au CE2 : horloge interactive, méthode pas à pas (quarts d’heure, minutes, après-midi) et fiches à imprimer avec corrigé.",
    "chapo": "Une horloge à manipuler pour apprendre à lire l’heure, la méthode pas à pas du CP au CE2 (heures entières, quarts d’heure, minutes, après-midi) et des fiches d’exercices à imprimer avec leur corrigé.",
    "resume": "Horloge interactive, quarts d’heure, minutes, fiches à imprimer",
    "vignette": "horloge_annotee",
    "niveaux": ["Primaire"],
    "ordre": 3.5,
    "publie": "2026-11-19",
    "modifie": "2026-11-19",
    "outil": "horloge",
    "motsCles": ["lire l'heure", "apprendre à lire l'heure", "horloge interactive", "horloge pour apprendre l'heure",
                 "exercices lire l'heure", "lire l'heure CP", "lire l'heure CE1", "lire l'heure CE2",
                 "fiche lire l'heure à imprimer", "quart d'heure", "et quart", "moins le quart", "demi-heure",
                 "heures de l'après-midi", "heure sur 24 heures", "petite aiguille", "grande aiguille"],
    "figures": [
        {"nom": "horloge_annotee", "alt": "Une horloge à aiguilles qui indique 10 h 08 : la petite aiguille, bleue, montre les heures ; la grande aiguille, orange, montre les minutes ; autour du cadran, les minutes de 5 en 5 : 05, 10, 15 jusqu’à 55."}
    ],
    "telechargements": [
        {"titre": "CP : les heures entières", "libelle": "Fiche", "pdf": f"{URL}lire-l-heure-cp-fiche.pdf", "corrige": f"{URL}lire-l-heure-cp-corrige.pdf"},
        {"titre": "CE1 : demi-heures et quarts d’heure", "libelle": "Fiche", "pdf": f"{URL}lire-l-heure-ce1-fiche.pdf", "corrige": f"{URL}lire-l-heure-ce1-corrige.pdf"},
        {"titre": "CE2 : heures et minutes", "libelle": "Fiche", "pdf": f"{URL}lire-l-heure-ce2-fiche.pdf", "corrige": f"{URL}lire-l-heure-ce2-corrige.pdf"}
    ],
    "chapitresLies": [
        "cp/le-reperage-dans-le-temps-les-heures-entieres",
        "ce1/lire-les-heures-et-les-quarts-d-heure",
        "ce2/lire-l-heure-a-la-minute",
        "cm2/lire-l-heure-et-calculer-des-durees"
    ],
    "liees": ["methodes/calculer-une-duree", "tables/tableau-de-conversion"],
    "faq": [
        ["À quel âge apprend-on à lire l’heure ?", "À l’école, au CP (6 ans), on lit les heures entières. Au CE1 (7 ans), on apprend les demi-heures, les quarts d’heure et les heures de l’après-midi. Au CE2 (8 ans), on lit l’heure à la minute près. Chaque enfant avance à son rythme : l’horloge de cette page permet de s’entraîner niveau par niveau."],
        ["Quelle aiguille indique les heures ?", "La petite aiguille indique les heures, la grande aiguille indique les minutes. En une heure, la grande aiguille fait un tour complet du cadran, pendant que la petite passe d’un nombre au suivant."],
        ["Comment dit-on 14 h 45 ?", "On dit « trois heures moins le quart » (de l’après-midi) ou, en lisant sur 24 heures, « quatorze heures quarante-cinq ». Sur une horloge à aiguilles, la petite aiguille est presque sur le 3 et la grande aiguille est sur le 9."],
        ["Comment apprendre l’heure à un enfant ?", "Commencez par les heures entières : la grande aiguille est sur le 12 et la petite montre l’heure. Passez ensuite aux demi-heures et aux quarts d’heure, puis aux minutes en comptant de 5 en 5. Faites-lui lire l’heure plusieurs fois par jour (repas, sortie de l’école) et laissez-le manipuler une horloge, comme celle de cette page."],
        ["Que signifient midi et minuit ?", "Midi, c’est 12 h, au milieu de la journée. Minuit, c’est 0 h (ou 24 h), au milieu de la nuit : une nouvelle journée commence."],
        ["Pourquoi dit-on « moins le quart » ?", "Quand la grande aiguille est sur le 9, il reste un quart d’heure, soit 15 minutes, avant l’heure suivante. À 3 h 45, on dit donc « quatre heures moins le quart ». Une erreur fréquente est de dire « trois heures moins le quart »."]
    ]
}

TEXTE = r"""<!-- optitab:1 -->
[OUTIL]

::: conseil Par où commencer ?
- **Au CP** : parties I et II (les aiguilles, les heures entières).
- **Au CE1** : parties III et V (demi-heures, quarts d’heure, après-midi).
- **Au CE2** : partie IV (les minutes) et partie VI (les durées).
- **Pour s’entraîner sur papier** : les fiches à imprimer de la partie VII.
:::

## I. La petite et la grande aiguille {Primaire}

[IMAGE_1]

- La **petite aiguille** indique les **heures**.
- La **grande aiguille** indique les **minutes**.
- En une heure, la grande aiguille fait un tour complet du cadran : il y a 60 minutes dans une heure. Pendant ce temps, la petite aiguille passe d’un nombre au suivant.
- Entre deux nombres du cadran, il y a 5 petits traits : 5 minutes.

## II. Lire les heures entières {Primaire}

*Programme de CP.*

Quand la grande aiguille est sur le 12, il est une **heure entière** (on dit aussi « heure pile ») : la petite aiguille montre l’heure.

::: exemple
La grande aiguille est sur le 12 et la petite aiguille sur le 3 : il est **3 heures**, que l’on écrit 3 h ou 3 h 00.
:::

Quand les deux aiguilles sont sur le 12, il est **midi** (au milieu de la journée) ou **minuit** (au milieu de la nuit).

## III. Les demi-heures et les quarts d’heure {Primaire}

*Programme de CE1.*

La grande aiguille partage le cadran en quatre quarts : chaque quart dure 15 minutes.

| Grande aiguille sur | On dit | On écrit |
|---|---|---|
| le 12 | trois heures | 3 h 00 |
| le 3 | trois heures et quart | 3 h 15 |
| le 6 | trois heures et demie | 3 h 30 |
| le 9 | quatre heures moins le quart | 3 h 45 |

::: attention Le piège de « moins le quart »
À 3 h 45, la petite aiguille est presque sur le 4 : il reste un quart d’heure avant 4 heures. On dit donc « **quatre** heures moins le quart », mais on écrit 3 h 45.
:::

## IV. Lire l’heure à la minute près {Primaire}

*Programme de CE2.*

1. On lit l’heure avec la **petite aiguille** : c’est le dernier nombre qu’elle a dépassé.
2. On compte les minutes avec la **grande aiguille**, de 5 en 5 à partir du 12 : 5, 10, 15, 20… puis une par une avec les petits traits.

::: exemple
La petite aiguille a dépassé le 7 et la grande est sur le 4 : il est 7 h 20 (sept heures vingt). La grande aiguille est sur le 8 et la petite presque sur le 9 : il est 8 h 40, que l’on dit aussi « neuf heures moins vingt ».
:::

::: attention Le nombre de la grande aiguille
Grande aiguille sur le 4, ce n’est pas 4 minutes mais 20 minutes : on multiplie par 5 (4 × 5 = 20).
:::

## V. Le matin, l’après-midi et les heures sur 24 heures {Primaire}

*Programme de CE1.*

Une journée dure 24 heures, mais la petite aiguille fait deux tours : un le matin, un l’après-midi et le soir. L’après-midi, on ajoute 12 heures à l’heure de l’horloge.

TABLEAU_APRES_MIDI

::: exemple
Il est deux heures et quart de l’après-midi : on écrit 14 h 15, et une horloge digitale affiche 14:15.
:::

Midi, c’est 12 h. Minuit, c’est 0 h (ou 24 h) : une nouvelle journée commence.

## VI. Les durées à connaître {Primaire}

| Durée | En minutes |
|---|---|
| une heure | 60 minutes |
| une demi-heure | 30 minutes |
| un quart d’heure | 15 minutes |
| trois quarts d’heure | 45 minutes |
| une heure et demie | 90 minutes |

Une minute dure 60 secondes. Pour calculer le temps écoulé entre deux heures, voir la méthode « Calculer une durée » (lien en bas de page).

## VII. Fiches à imprimer {Primaire}

Une fiche par niveau, avec son corrigé : 9 horloges à lire et 3 horloges où dessiner les aiguilles.

[TELECHARGEMENTS]
"""

UNITE = r"(?:h|min|minutes|secondes|ans)"
NOMBRE_UNITE = re.compile(r"(\d) (?=" + UNITE + r"(?![A-Za-zÀ-ÿ0-9’]))")
HEURE = re.compile(r"(\d) h (\d\d)")
MATHS = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)")


def insecables(texte):
    morceaux = MATHS.split(texte)
    for i in range(0, len(morceaux), 2):
        m = HEURE.sub(lambda x: x.group(1) + NBSP + "h" + NBSP + x.group(2), morceaux[i])
        morceaux[i] = NOMBRE_UNITE.sub(lambda x: x.group(1) + NBSP, m)
    return "".join(morceaux)


def ecrire_formulaire():
    texte = TEXTE.replace("TABLEAU_APRES_MIDI", tableau_apres_midi())
    entete = json.dumps(INFOS, ensure_ascii=False, indent=2)
    (ICI / "formulaire.md").write_text(insecables(f"---\n{entete}\n---\n{texte}"), encoding="utf-8", newline="\n")
    print("formulaire.md écrit")


if __name__ == "__main__":
    controler_avec_le_site()
    ecrire_formulaire()
    if "--sans-pdf" not in sys.argv:
        ecrire_fiches()
