"""Vérification du chapitre 19 (Couleurs et vision) et du défi D19.

Lancer : python -I -X utf8 verifications/chapitre_19.py
Modèle trichrome : une lumière ou une couleur est représentée par l'ensemble de ses composantes R, V, B.
"""
import io
import math
from contextlib import redirect_stdout

ECHECS = []
R, V, B = 'rouge', 'vert', 'bleu'
NOMS = {frozenset(): 'noir', frozenset({R}): 'rouge', frozenset({V}): 'vert', frozenset({B}): 'bleu',
        frozenset({R, V}): 'jaune', frozenset({V, B}): 'cyan', frozenset({R, B}): 'magenta',
        frozenset({R, V, B}): 'blanc'}
COUL = {nom: set(e) for e, nom in NOMS.items()}


def nom(ensemble):
    return NOMS[frozenset(ensemble)]


def attendu(etiquette, obtenu, prevu):
    ok = obtenu == prevu
    print(f"{'ok ' if ok else 'ÉCHEC'} {etiquette:60s} obtenu {obtenu}  publié {prevu}")
    if not ok:
        ECHECS.append(etiquette)


def verifie(etiquette, calcule, publie, tol_rel=0.006):
    ok = abs(calcule - publie) <= tol_rel * abs(publie) + 1e-12
    print(f"{'ok ' if ok else 'ÉCHEC'} {etiquette:60s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(etiquette)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


# Synthèse additive (union) et soustractive (intersection)
attendu("additive rouge + vert", nom({R} | {V}), 'jaune')
attendu("additive vert + bleu", nom({V} | {B}), 'cyan')
attendu("additive rouge + bleu", nom({R} | {B}), 'magenta')
attendu("additive rouge + vert + bleu", nom({R, V, B}), 'blanc')
attendu("soustractive cyan + magenta", nom(COUL['cyan'] & COUL['magenta']), 'bleu')
attendu("soustractive cyan + jaune", nom(COUL['cyan'] & COUL['jaune']), 'vert')
attendu("soustractive magenta + jaune", nom(COUL['magenta'] & COUL['jaune']), 'rouge')
attendu("soustractive cyan + magenta + jaune", nom(COUL['cyan'] & COUL['magenta'] & COUL['jaune']), 'noir')
for a, b in [('rouge', 'cyan'), ('vert', 'magenta'), ('bleu', 'jaune')]:
    attendu(f"complémentaires {a} + {b}", nom(COUL[a] | COUL[b]), 'blanc')


def programme():
    blanche = {'rouge', 'vert', 'bleu'}
    filtre_jaune = {'rouge', 'vert'}
    filtre_cyan = {'vert', 'bleu'}
    print(sorted(blanche & filtre_jaune))
    print(sorted(blanche & filtre_jaune & filtre_cyan))


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != "['rouge', 'vert']\n['vert']":
    ECHECS.append('cours programme')
# Exercice 3 : tomate (diffuse le rouge)
tomate = COUL['rouge']
attendu("ex3 tomate en lumière blanche", nom(COUL['blanc'] & tomate), 'rouge')
attendu("ex3 tomate en lumière verte", nom(COUL['vert'] & tomate), 'noir')
attendu("ex3 tomate en lumière jaune", nom(COUL['jaune'] & tomate), 'rouge')
attendu("ex3 tomate en lumière cyan", nom(COUL['cyan'] & tomate), 'noir')
# Exercice 4 : filtres
attendu("ex4 blanc, jaune puis cyan", nom(COUL['blanc'] & COUL['jaune'] & COUL['cyan']), 'vert')
attendu("ex4 blanc, rouge puis cyan", nom(COUL['blanc'] & COUL['rouge'] & COUL['cyan']), 'noir')
attendu("ex4 blanc, magenta puis jaune", nom(COUL['blanc'] & COUL['magenta'] & COUL['jaune']), 'rouge')
attendu("ex4 lumière magenta, filtre cyan", nom(COUL['magenta'] & COUL['cyan']), 'bleu')


# Exercice 6 : programme
def programme6():
    couleurs = {'rouge': {'R'}, 'vert': {'V'}, 'bleu': {'B'}, 'jaune': {'R', 'V'},
                'cyan': {'V', 'B'}, 'magenta': {'R', 'B'}, 'blanc': {'R', 'V', 'B'}}
    lumiere = couleurs['jaune']
    for objet in ['blanc', 'rouge', 'cyan', 'bleu']:
        vu = lumiere & couleurs[objet]
        nom_vu = [n for n in couleurs if couleurs[n] == vu]
        print(objet, '->', nom_vu[0] if nom_vu else 'noir')


s6 = sortie_de(programme6)
print('   ex6 programme :', s6.replace('\n', ' | '))
if s6 != 'blanc -> jaune\nrouge -> rouge\ncyan -> vert\nbleu -> noir':
    ECHECS.append('ex6 programme')
# Exercice 7 : écran RVB
verifie("ex7 nombre de couleurs", 256 ** 3, 16777216)
verifie("ex7 nombre de niveaux par sous-pixel", 2 ** 8, 256)
# Exercice 8 : spectacle
attendu("ex8 costume blanc, projecteurs rouge et bleu", nom(COUL['blanc'] & (COUL['rouge'] | COUL['bleu'])), 'magenta')
attendu("ex8 costume blanc, projecteur vert", nom(COUL['blanc'] & COUL['vert']), 'vert')
attendu("ex8 costume rouge, projecteur bleu", nom(COUL['rouge'] & COUL['bleu']), 'noir')
attendu("ex8 costume jaune, projecteurs rouge et bleu", nom(COUL['jaune'] & (COUL['rouge'] | COUL['bleu'])), 'rouge')
# Exercice 11 : capteur de Bayer
verifie("ex11 photosites verts sur 12 millions", 12e6 / 2, 6e6)
verifie("ex11 photosites rouges", 12e6 / 4, 3e6)
# Exercice 12 : imprimante
attendu("ex12 encre cyan sous lumière rouge", nom(COUL['rouge'] & COUL['cyan']), 'noir')
attendu("ex12 bleu imprimé = cyan + magenta", nom(COUL['cyan'] & COUL['magenta']), 'bleu')
# Exercice 13 : anaglyphes
attendu("ex13 dessin rouge vu à travers le filtre rouge", nom(COUL['rouge'] & COUL['rouge']), 'rouge')
attendu("ex13 fond blanc vu à travers le filtre rouge", nom(COUL['blanc'] & COUL['rouge']), 'rouge')
attendu("ex13 dessin cyan vu à travers le filtre rouge", nom(COUL['cyan'] & COUL['rouge']), 'noir')
attendu("ex13 dessin rouge vu à travers le filtre cyan", nom(COUL['rouge'] & COUL['cyan']), 'noir')
# Exercice 14 : pixels d'un écran
pas = 25.4 / 400
verifie("ex14 taille d'un pixel à 400 ppp (micrometres)", pas * 1000, 63.5)
verifie("ex14 pouvoir séparateur de l'oeil (rad)", math.radians(1 / 60), 2.9e-4, 0.005)
verifie("ex14 plus petit détail vu à 30 cm (micrometres)", math.radians(1 / 60) * 300 * 1000, 87, 0.005)
verifie("ex14 distance à partir de laquelle les pixels se fondent (cm)", pas / math.radians(1 / 60) / 10, 21.8, 0.004)
verifie("ex14 écran 1920 pixels sur 1,0 m : pas (mm)", 1000 / 1920, 0.52, 0.002)
verifie("ex14 distance minimale pour la télévision (m)", 1 / 1920 / math.radians(1 / 60), 1.79, 0.004)
# Exercice 15 : spectres d'absorption
attendu("ex15 absorbe le vert : couleur perçue", nom(COUL['blanc'] - COUL['vert']), 'magenta')
attendu("ex15 absorbe le bleu : couleur perçue", nom(COUL['blanc'] - COUL['bleu']), 'jaune')

# Défi D19 : le bleu du ciel
verifie("D19 rapport bleu 450 / rouge 700", (700 / 450) ** 4, 5.86, 0.003)
verifie("D19 rapport violet 400 / rouge 700", (700 / 400) ** 4, 9.38, 0.003)
verifie("D19 rapport bleu 450 / vert 550", (550 / 450) ** 4, 2.23, 0.003)


def programme_d19():
    for lam in [400, 450, 500, 550, 600, 650, 700]:
        print(lam, 'nm :', round((700 / lam) ** 4, 2))


s19 = sortie_de(programme_d19)
print('   D19 programme :', s19.replace('\n', ' | '))
if s19 != '400 nm : 9.38\n450 nm : 5.86\n500 nm : 3.84\n550 nm : 2.62\n600 nm : 1.85\n650 nm : 1.35\n700 nm : 1.0':
    ECHECS.append('D19 programme')
verifie("D19 épaisseur d'air traversée au coucher (fois)", 1 / math.cos(math.radians(85)), 11.5, 0.004)
verifie("D19 fraction de bleu restante après 11 couches de 10 %", 0.9 ** 11.5, 0.30, 0.02)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les synthèses, valeurs et sorties du chapitre 19 et du défi D19 sont vérifiées.")
