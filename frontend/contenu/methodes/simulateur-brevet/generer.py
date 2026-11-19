# -*- coding: utf-8 -*-
"""Page « Simulateur du brevet » (methodes/simulateur-brevet) : contrôles et texte.

    python -X utf8 generer.py

1. Contrôle : le calcul écrit ici (Python) donne les mêmes résultats que celui du
   site, côté page (scripts/ressources/brevet.mjs) et côté saisie
   (scripts/ressources/outils/brevet.js), sur 5 000 cas tirés au hasard.
2. Calcule les exemples de la page et écrit formulaire.md (ne pas le modifier à
   la main : modifier ce script et le relancer).

Règles officielles (lues dans les textes le 19/11/2026) :
- arrêté du 10 avril 2025 modifiant l'arrêté du 31 décembre 2015 relatif aux
  modalités d'attribution du DNB (JO du 12 avril 2025, NOR MENE2415613A) :
  note finale = 40 % contrôle continu + 60 % épreuves ; admis si ≥ 10/20 ;
  coefficients français 2, mathématiques 2, histoire-géographie 1,5, EMC 0,5,
  sciences 2, oral 2 ; mentions 12, 14, 16, 18 (félicitations du jury) ;
- mémento Éduscol « Évaluer les élèves de 3e… » (décembre 2025) : les points
  au-dessus de 10 d'un seul enseignement facultatif s'ajoutent à la SOMME des
  moyennes annuelles ; liste des 12 enseignements obligatoires ;
- session 2027 : mêmes règles (BO spécial n° 4 du 17 septembre 2026), épreuves
  sur les programmes de 3e, oral de 15 minutes, 20 min d'automatismes en maths.
"""
import json
import math
import random
import re
import subprocess
from pathlib import Path

ICI = Path(__file__).resolve().parent
FRONT = ICI.parents[2]
NBSP, NNBSP = chr(0xA0), chr(0x202F)

COEF = {"francais": 2, "maths": 2, "hg": 1.5, "emc": 0.5, "sciences": 2, "oral": 2}


def controle_continu(moyennes, option=None):
    notes = [m for m in moyennes if m is not None]
    if not notes:
        return None
    bonus = option - 10 if option is not None and option > 10 else 0
    return min(20, (sum(notes) + bonus) / len(notes))


def moyenne_epreuves(notes):
    return sum(COEF[k] * notes[k] for k in COEF) / 10


def note_finale(cc, ep):
    return 0.4 * cc + 0.6 * ep


def a_viser(cc, seuil):
    return (seuil - 0.4 * cc) / 0.6


def arrondi(x):
    """Note finale au centième, comme le site (le verdict suit le nombre affiché)."""
    return math.floor(x * 100 + 1e-7 + 0.5) / 100


def plafond(x):
    """Note à viser au centième supérieur, comme le site : l'obtenir suffit toujours."""
    return math.ceil(x * 100 - 1e-7) / 100


def g(x):
    """Valeur exacte au centième, sans zéros inutiles : 13,5 ; 14 ; 13,25."""
    assert abs(x * 100 - round(x * 100)) < 1e-6, x
    return f(x).rstrip("0").rstrip(",")


def f(x):
    """2 décimales, virgule (affichage de la page)."""
    return f"{x:.2f}".replace(".", ",")


def controler_avec_le_site():
    random.seed(2027)
    cas = []
    for _ in range(5000):
        moy = [None if random.random() < 0.08 else round(random.uniform(0, 20), 2) for _ in range(12)]
        opt = None if random.random() < 0.6 else round(random.uniform(0, 20), 2)
        notes = {k: round(random.uniform(0, 20), 2) for k in COEF}
        cas.append({"moy": moy, "opt": opt, "notes": notes})
    attendu = []
    for c in cas:
        cc = controle_continu(c["moy"], c["opt"])
        ep = moyenne_epreuves(c["notes"])
        attendu.append([cc, ep, arrondi(note_finale(cc, ep)) if cc is not None else None,
                        plafond(a_viser(cc, 12)) if cc is not None else None])
    entree = json.dumps(cas)
    js = FRONT / "scripts" / "ressources" / "outils" / "brevet.js"
    mjs = (FRONT / "scripts" / "ressources" / "brevet.mjs").as_uri()
    code = ("const vm=require('vm'),fs=require('fs');const c={window:{},document:{querySelector:()=>null}};"
            "vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),c);const B=c.window.OTBrevet;"
            "const cas=JSON.parse(fs.readFileSync(0,'utf8'));"
            "import(process.argv[2]).then((M)=>{const r=cas.map((x)=>{"
            "const cc=B.controleContinu(x.moy,x.opt),ep=B.moyenneEpreuves(x.notes);"
            "const cc2=M.controleContinu(x.moy,x.opt),ep2=M.moyenneEpreuves(x.notes);"
            "if(Math.abs((cc??0)-(cc2??0))>1e-12||Math.abs(ep-ep2)>1e-12)throw new Error('page et saisie differentes');"
            "if(cc!=null&&(M.arrondi(M.noteFinale(cc,ep))!==B.arrondi(B.noteFinale(cc,ep))||M.plafond(M.aViser(cc,12))!==B.plafond(B.aViser(cc,12))))throw new Error('arrondis differents');"
            "return [cc,ep,cc==null?null:B.arrondi(B.noteFinale(cc,ep)),cc==null?null:B.plafond(B.aViser(cc,12))]});"
            "process.stdout.write(JSON.stringify(r))})")
    sortie = subprocess.run(["node", "-e", code, str(js), mjs], input=entree, capture_output=True, text=True,
                            encoding="utf-8", check=True).stdout
    site = json.loads(sortie)
    for a, b in zip(attendu, site):
        for x, y in zip(a, b):
            assert (x is None and y is None) or abs(x - y) < 1e-9, (a, b)
    # Règles vérifiées à la main
    assert controle_continu([12] * 12) == 12
    assert controle_continu([12] * 12, 16) == 12.5            # 6 points ajoutés à la somme, divisés par 12
    assert controle_continu([20] * 12, 20) == 20              # plafond de 20
    assert controle_continu([12, None, 14]) == 13             # matière vide (dispense) non comptée
    assert moyenne_epreuves({k: 10 for k in COEF}) == 10
    assert abs(a_viser(11, 10) - 9.3333333) < 1e-6
    assert plafond(a_viser(11, 10)) == 9.34 and note_finale(11, 9.34) >= 10 and note_finale(11, 9.33) < 10
    assert plafond(a_viser(13, 10)) == 8 and plafond(a_viser(11, 12)) == 12.67
    # avec la note à viser affichée, l'objectif est toujours atteint
    for c in cas[:2000]:
        cc = controle_continu(c["moy"], c["opt"])
        for s in (10, 12, 14, 16, 18):
            if cc is not None and 0 < a_viser(cc, s) <= 20:
                assert arrondi(note_finale(cc, plafond(a_viser(cc, s)))) >= s
    print("calcul identique au site (page et saisie) sur 5 000 cas")


# ---------------------------------------------------------------- exemples de la page
SOMME_EX, OPTION_EX = 162, 16
CC_SANS = SOMME_EX / 12
CC_AVEC = controle_continu([SOMME_EX / 12] * 12, OPTION_EX)
NOTES_EX = {"francais": 12, "maths": 14, "hg": 11, "emc": 16, "sciences": 13, "oral": 15}
EP_EX = moyenne_epreuves(NOTES_EX)
FIN_EX = note_finale(CC_AVEC, EP_EX)
assert (round(CC_SANS, 2), round(CC_AVEC, 2), EP_EX, round(FIN_EX, 2)) == (13.5, 14.0, 13.25, 13.55)


def remplacer(texte):
    valeurs = {
        "CC_SANS": g(CC_SANS), "CC_AVEC": g(CC_AVEC), "EP_EX": g(EP_EX), "FIN_EX": g(FIN_EX),
        "PART_CC": g(0.4 * CC_AVEC), "EP_X10": g(10 * EP_EX), "PART_EP": g(0.6 * EP_EX),
        "VISER_10": f(a_viser(11, 10)), "VISER_12": f(a_viser(11, 12)),
        "VISER_10_HAUT": g(plafond(a_viser(11, 10))), "VISER_13_10": g(plafond(a_viser(13, 10))),
    }
    for k, v in valeurs.items():
        texte = texte.replace("{" + k + "}", v)
    assert not re.search(r"\{[A-Z][A-Z0-9_]+\}", texte), "valeur non remplacée"
    return texte


INFOS = {
    "slug": "simulateur-brevet",
    "titre": "Simulateur du brevet : calculer sa note et sa mention",
    "titreCourt": "Simulateur du brevet",
    "titreSeo": "Simulateur brevet 2027 : calcul de la note et de la mention",
    "description": "Calculez votre note au brevet 2027 : contrôle continu (40 %), épreuves (60 %), coefficients officiels, mention et note à viser. Gratuit, avec exemples.",
    "chapo": "Le calcul officiel de la note du brevet, en vigueur depuis la session 2026 : entrez vos moyennes de 3e et vos notes, le simulateur donne la note finale, la mention et la note à viser aux épreuves. Avec la méthode pas à pas et des exemples.",
    "resume": "Contrôle continu, épreuves, mention et note à viser",
    "vignette": "poids_notes_brevet",
    "theme": "Brevet",
    "niveaux": ["Collège"],
    "ordre": 2.5,
    "publie": "2026-11-19",
    "modifie": "2026-11-19",
    "outil": "brevet",
    "motsCles": ["simulateur brevet", "simulateur brevet 2027", "simulateur brevet 2026", "calcul note brevet", "calculer sa note au brevet",
                 "calcul moyenne brevet", "note brevet sur 20", "contrôle continu brevet", "coefficient brevet",
                 "coefficients épreuves brevet", "mention brevet", "points brevet", "brevet 40 % 60 %",
                 "note pour avoir le brevet", "latin points brevet", "félicitations du jury brevet"],
    "figures": [
        {"nom": "poids_notes_brevet", "alt": "Part de chaque note dans la note finale du brevet : contrôle continu 40 % ; épreuves 60 %, soit français 12 %, mathématiques 12 %, sciences 12 %, oral 12 %, histoire-géographie 9 % et enseignement moral et civique 3 %."}
    ],
    "liees": ["methodes/calculer-une-moyenne", "physique-chimie/formules-physique-chimie-brevet"],
    "faq": [
        ["Comment est calculée la note du brevet ?", "Depuis la session 2026, la note finale est sur 20 : 40 % pour le contrôle continu (la moyenne des moyennes annuelles de 3e) et 60 % pour les épreuves terminales. Note finale = 0,4 × contrôle continu + 0,6 × moyenne des épreuves. Le brevet est obtenu à partir de 10 sur 20."],
        ["Quelle moyenne faut-il pour avoir le brevet ?", "Une note finale d’au moins 10 sur 20. Avec un contrôle continu de 11, il faut au moins {VISER_10_HAUT} de moyenne aux épreuves ; avec un contrôle continu de 13, il suffit de {VISER_13_10}."],
        ["Quels sont les coefficients des épreuves du brevet ?", "Français 2, mathématiques 2, sciences 2, oral 2, histoire-géographie 1,5 et enseignement moral et civique 0,5, soit 10 au total. Chaque épreuve est notée sur 20."],
        ["Comment se calcule le contrôle continu du brevet ?", "C’est la moyenne des moyennes annuelles de 3e de tous les enseignements obligatoires, 12 pour la plupart des élèves, qui ont tous le même coefficient. Une matière dont l’élève est dispensé n’est pas comptée."],
        ["Le latin rapporte-t-il des points au brevet ?", "Oui. Les points au-dessus de 10 sur 20 de la moyenne d’un enseignement facultatif (latin, grec, langues et cultures européennes, langue régionale, chant choral) ou de la langue des signes française s’ajoutent à la somme des moyennes du contrôle continu. Avec 16 en latin, on ajoute 6 points à la somme. Une seule option est prise en compte et le contrôle continu ne peut pas dépasser 20."],
        ["Quelles sont les mentions au brevet ?", "Assez bien à partir de 12 sur 20, bien à partir de 14, très bien à partir de 16, et très bien avec les félicitations du jury à partir de 18."]
    ]
}

TEXTE = r"""<!-- optitab:1 -->
[OUTIL]

::: conseil Comment utiliser le simulateur
1. Entrez vos **moyennes annuelles de 3e** (sur vos bulletins). En cours d’année, la moyenne des trimestres déjà passés donne une bonne estimation.
2. Entrez vos **notes aux épreuves** : vos notes au brevet blanc ou celles que vous visez.
3. Lisez la note finale, la mention et, en bas, la **note à obtenir aux épreuves** pour chaque objectif.
:::

## I. Le calcul de la note du brevet {Collège}

Depuis la session 2026, le brevet est noté **sur 20** (il n’y a plus de total sur 800 points) :

::: formule Note finale du brevet
$$N = 0{,}4 \times C + 0{,}6 \times E$$
:::

| Lettre | Ce que c’est |
|---|---|
| $N$ | la note finale, sur 20 |
| $C$ | la moyenne du contrôle continu, sur 20 : 40 % de la note |
| $E$ | la moyenne des épreuves terminales, sur 20 : 60 % de la note |

Le diplôme est obtenu quand la note finale est au moins égale à **10 sur 20**.

[IMAGE_1]

::: attention Les anciens calculs sur 800 points
Avant 2026, le brevet se comptait sur 800 points, avec 400 points pour la maîtrise du socle commun. Ce calcul n’existe plus : le socle ne rapporte plus de points, et un simulateur sur 800 points donne un résultat faux.
:::

## II. Le contrôle continu : 40 % de la note {Collège}

C’est la moyenne des **moyennes annuelles de 3e** de tous les enseignements obligatoires, qui ont **tous le même coefficient** : français, mathématiques, langue vivante 1, langue vivante 2, histoire-géographie, enseignement moral et civique, sciences de la vie et de la Terre, physique-chimie, technologie, éducation physique et sportive, arts plastiques et éducation musicale. Une matière dont l’élève est dispensé n’est pas comptée.

::: retenir Le bonus d’une option
Les points au-dessus de 10 sur 20 de la moyenne d’un enseignement facultatif (latin ou grec, langues et cultures européennes, langue et culture régionales, chant choral) ou de l’enseignement en langue des signes française s’ajoutent à la **somme** des moyennes annuelles. Un seul enseignement facultatif est pris en compte, et le contrôle continu ne peut pas dépasser 20.
:::

::: exemple
La somme des 12 moyennes annuelles vaut 162 : sans option, $C = 162 \div 12 = {CC_SANS}$. Avec 16 de moyenne en latin, on ajoute $16 - 10 = 6$ points à la somme : $C = (162 + 6) \div 12 = {CC_AVEC}$.
:::

Une commission académique peut harmoniser les moyennes d’un collège, à la hausse ou à la baisse, si elles s’écartent nettement de celles de l’académie.

## III. Les épreuves terminales : 60 % de la note {Collège}

Chaque épreuve est notée sur 20 :

| Épreuve | Coefficient |
|---|---|
| Français | 2, soit 12 % de la note finale |
| Mathématiques | 2, soit 12 % de la note finale |
| Sciences | 2, soit 12 % de la note finale |
| Oral de soutenance | 2, soit 12 % de la note finale |
| Histoire-géographie | 1,5, soit 9 % de la note finale |
| Enseignement moral et civique | 0,5, soit 3 % de la note finale |

- **Mathématiques** : l’épreuve commence par une partie d’automatismes, 20 minutes sans calculatrice, notée sur 6 points.
- **Sciences** : deux disciplines parmi physique-chimie, sciences de la vie et de la Terre et technologie.
- **Histoire-géographie et EMC** : une seule épreuve écrite en deux parties, chacune avec sa note et son coefficient.
- **Oral** : une soutenance de 15 minutes, organisée par le collège.

::: formule Moyenne des épreuves
$$\begin{aligned}
10\,E &= 2F + 2M + 2S + 2O \\
&\quad + 1{,}5\,HG + 0{,}5\,EMC
\end{aligned}$$
:::

On additionne les six notes multipliées par leur coefficient, puis on divise par 10, la somme des coefficients.

::: exemple
Avec 12 en français, 14 en mathématiques, 13 en sciences, 15 à l’oral, 11 en histoire-géographie et 16 en EMC :

$$\begin{aligned}
10\,E &= 24 + 28 + 26 + 30 \\
&\quad + 16{,}5 + 8 = {EP_X10}
\end{aligned}$$

donc $E = {EP_X10} \div 10 = {EP_EX}$.
:::

## IV. Les mentions {Collège}

| Note finale | Résultat |
|---|---|
| moins de 10 | non admis |
| de 10 à moins de 12 | admis |
| à partir de 12 | mention assez bien |
| à partir de 14 | mention bien |
| à partir de 16 | mention très bien |
| à partir de 18 | très bien avec les félicitations du jury |

## V. Un exemple complet {Collège}

::: exemple
Contrôle continu $C = {CC_AVEC}$ (avec le latin) et moyenne des épreuves $E = {EP_EX}$ :

$$\begin{aligned}
N &= 0{,}4 \times {CC_AVEC} + 0{,}6 \times {EP_EX} \\
&= {PART_CC} + {PART_EP} = {FIN_EX}
\end{aligned}$$

L’élève obtient le brevet avec la **mention assez bien**.
:::

## VI. Quelle note viser aux épreuves ? {Collège}

En connaissant son contrôle continu, on peut calculer la moyenne à obtenir aux épreuves pour atteindre un objectif $S$ (10 pour le diplôme, 12, 14, 16 ou 18 pour une mention) :

::: formule Moyenne à obtenir aux épreuves
$$E = \dfrac{S - 0{,}4 \times C}{0{,}6}$$
:::

::: exemple
Avec un contrôle continu de 11, il faut $E \geq (10 - 0{,}4 \times 11) \div 0{,}6 \approx {VISER_10}$ aux épreuves pour obtenir le brevet, et $E \geq (12 - 0{,}4 \times 11) \div 0{,}6 \approx {VISER_12}$ pour la mention assez bien.

Le simulateur arrondit ce résultat au centième supérieur, {VISER_10_HAUT} au lieu de {VISER_10} : avec cette note, l’objectif est atteint à coup sûr.
:::

## VII. Les candidats individuels {Collège}

Les candidats qui ne sont pas scolarisés dans un collège n’ont pas de contrôle continu. Leur note est la moyenne de cinq épreuves écrites : les quatre épreuves écrites des autres candidats, avec les mêmes coefficients, et une épreuve de langue vivante étrangère (coefficient 2, 1 h 30). Ils ne passent pas d’oral.

::: remarque Les textes officiels
Arrêté du 10 avril 2025 modifiant l’arrêté du 31 décembre 2015 relatif aux modalités d’attribution du diplôme national du brevet (Journal officiel du 12 avril 2025, NOR MENE2415613A), en vigueur depuis la session 2026 ; mêmes règles pour la session 2027 (Bulletin officiel spécial n° 4 du 17 septembre 2026). Le simulateur donne une estimation : seul le relevé de notes officiel fait foi.
:::
"""

UNITE = r"(?:points|minutes|min|h|%)"
NOMBRE_UNITE = re.compile(r"(\d) (?=" + UNITE + r"(?![A-Za-zÀ-ÿ0-9’]))")
MILLIERS = re.compile(r"(\d) (?=\d{3}(?![\d,]))")
MATHS = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)")


def insecables(texte):
    morceaux = MATHS.split(texte)
    for i in range(0, len(morceaux), 2):
        m = MILLIERS.sub(lambda x: x.group(1) + NNBSP, morceaux[i])
        morceaux[i] = NOMBRE_UNITE.sub(lambda x: x.group(1) + NBSP, m)
    return "".join(morceaux)


def ecrire_formulaire():
    infos = json.loads(remplacer(json.dumps(INFOS, ensure_ascii=False)))
    entete = json.dumps(infos, ensure_ascii=False, indent=2)
    texte = MATHS.sub(lambda m: re.sub(r"(\d),(\d)", r"\1{,}\2", m.group(0)), remplacer(TEXTE))
    (ICI / "formulaire.md").write_text(insecables(f"---\n{entete}\n---\n{texte}"), encoding="utf-8", newline="\n")
    print("formulaire.md écrit")


if __name__ == "__main__":
    controler_avec_le_site()
    ecrire_formulaire()
