"""Matrice de correspondance : édition 2026-2027 (programme 2020) -> programme 2026 de Quatrième -> édition 2027-2028.

Écrit build/matrice-programme.md, repris dans le rapport de livraison.
"""
from pathlib import Path
from liminaires_contenu import OBJECTIFS

ROOT = Path(__file__).resolve().parent

ANCIEN = [
    ('1 · Calculer avec les nombres relatifs', 'Opérations sur les relatifs : produit d’abord avec un facteur négatif, puis deux grâce à la distributivité ; quotient ; enchaînements ; vocabulaire d’un programme de calcul.', 'Conservé et recentré : construction du produit par l’addition itérée et la distributivité, multiplications à trou, nommer un calcul, programme de calcul (ch. 1).'),
    ('2 · Fractions et nombres premiers', 'Nombres rationnels : simplifier, définir un rationnel, opposé, produit, fraction d’une fraction, inverse et notation 1/a, division, enchaînements, problèmes. Nombres premiers, décomposition et fraction irréductible : Troisième (« Multiples et diviseurs »).', 'Réécrit (ch. 2). Nombres premiers et décomposition retirés ; fraction d’une fraction illustrée ; problèmes de partage conservés.'),
    ('3 · Puissances et notation scientifique', 'Puissances d’exposant positif ; a^m × a^n = a^(m+n) ; a^n × b^n = (ab)^n ; problèmes ; a^0 = 1. Exposants négatifs, division de puissances et notation scientifique : Troisième.', 'Réécrit (ch. 3) : produits de puissances ; préfixes kilo, méga, giga, milli, micro, nano sans exposant négatif.'),
    ('4 · Carrés et racines carrées', 'Définition de la racine carrée d’un nombre positif ; encadrement par deux entiers consécutifs ; prolongement : √2 n’est pas décimal. Équations x² = a : Troisième.', 'Conservé (ch. 4), vocabulaire ajusté ; repère historique ; défi D04 « √2 n’est pas décimal ».'),
    ('5 · Expressions et distributivité', 'Produire des formules, distributivité simple, démonstrations par le calcul ; nombres pairs 2n et impairs 2n + 1 ; rôle du facteur −1.', 'Conservé (ch. 5) avec pairs/impairs, opposé d’une expression, somme de trois entiers consécutifs.'),
    ('6 · Équations', 'ax + b = c ; mise en équation avec ax + b = cx + d ; conjectures avec un tableur ou un algorithme.', 'Conservé (ch. 6) ; exercice de conjecture au tableur ajouté.'),
    ('7 · Proportionnalité et pourcentages', 'Grandeurs quotients ; rapports et ratios ; égalités de rapports et produit en croix ; quatrième proportionnelle ; pourcentages ; coefficient multiplicateur ; partage proportionnel.', 'Scindé : ch. 7 (rapports, ratios, partages) et ch. 8 (pourcentages, coefficient multiplicateur).'),
    ('8 · Grandeurs composées et unités', 'Grandeurs quotients avec ou sans unités. Les grandeurs produits ne figurent plus au programme de Quatrième.', 'Fusionné dans le ch. 8 ; énergie en kWh retirée.'),
    ('9 · Relier des grandeurs et lire des graphiques', 'Programmes de calcul appliqués à un nombre puis à une variable ; les remonter ; formule, tableau, graphique ; notations P(t) utilisées progressivement.', 'Réécrit (ch. 9) : programmes de calcul, notation P(t), A(c), V(t).'),
    ('10 · Statistiques et diagrammes', 'Moyenne pondérée ; médiane (« toute valeur » qui partage la série) ; étendue ; effet d’une valeur extrême ; comparaison de séries ; tableur. Construction de diagrammes circulaires : Cinquième.', 'Réécrit (ch. 10) : étendue, valeur extrême, fonctions MOYENNE, MEDIANE, MAX, MIN, NB.'),
    ('11 · Probabilités (une épreuve)', 'Vocabulaire et notations ensemblistes ; contraire, réunion, intersection, ensemble vide ; deux épreuves ; distributions fréquentielle et probabiliste ; fluctuation.', 'Réécrit (ch. 11) : univers, Ā, A ∩ B, A ∪ B, ∅, arbres et tableaux, fluctuation. Probabilités par aires retirées.'),
    ('12 · Construire et comparer des triangles (cas d’égalité)', 'Les cas d’égalité ne figurent pas dans le programme 2026. Nouveau : droites remarquables (automatismes), réciproque, contraposée, raisonnement par l’absurde.', 'Remplacé par le ch. 12 « Droites remarquables et raisonnement ».'),
    ('13 · Le théorème de Pythagore', 'Théorème, réciproque et contraposée ; travail de logique ; le mot « contraposée » est attendu.', 'Conservé (ch. 15) ; contraposée explicitée.'),
    ('14 · Thalès : triangles emboîtés', 'Passe en Troisième (emboîtés et papillon). Nouveau en Quatrième : les trois théorèmes de la droite des milieux.', 'Remplacé par le ch. 14 « La droite des milieux » ; Varignon et centre de gravité en problèmes.'),
    ('15 · Le cosinus', 'Passe en Troisième (cosinus, sinus, tangente). Nouveau : triangle rectangle et cercle circonscrit, centre, rectangles sans équerre.', 'Remplacé par le ch. 16 « Triangle rectangle et cercle circonscrit ».'),
    ('16 · Translations, agrandissements et réductions', 'Effet d’une translation, lien avec les parallélogrammes et les angles, conservations ; reconnaissance de symétries et demi-tours. Agrandissements et réductions non repris.', 'Réécrit (ch. 13 « Translations et parallélogrammes »).'),
    ('17 · Espace, pyramides et cônes', 'Reconnaître pyramide et cône, représentations, volumes. Repérage dans un pavé non repris.', 'Conservé (ch. 17) : reconnaissance des solides et cône de révolution par rotation ajoutés ; repérage dans le pavé retiré.'),
    ('18 · Algorithmique et programmation', 'Conditions simples (<, >, =), instructions conditionnelles, une variable, écrire et modifier un programme. Conditions composées, boucles conditionnelles, plusieurs variables, blocs personnalisés : Troisième.', 'Adapté (ch. 18) : chaque script n’utilise qu’une variable (contrôle automatique).'),
]

VOCABULAIRE = [
    ('Quotient, fraction, rationnel', 'Définitions du programme : la fraction est à la fois un nombre et une écriture ; un rationnel est le quotient de deux entiers relatifs.'),
    ('Inverse', 'Notation 1/a ; inverse de a/b égal à b/a ; zéro n’a pas d’inverse.'),
    ('Puissances', 'a^n pour n entier naturel, a^0 = 1 pour a non nul.'),
    ('Dépendance', 'Notations P(t), A(c), V(t), T(2) utilisées comme « valeur pour », sans le vocabulaire image et antécédent (Troisième).'),
    ('Ratio', 'Notation a : b et a : b : c ; « proportionnels à 2, 3, 7 ».'),
    ('Pourcentages', 'Coefficient multiplicateur 1 + t/100 et 1 − t/100.'),
    ('Statistiques', 'Médiane : toute valeur qui partage la série ordonnée en deux parties de même effectif ; étendue.'),
    ('Probabilités', 'Univers, événement, Ā (contraire, complémentaire), A ∩ B, A ∪ B, ∅ ; fréquence, fluctuation.'),
    ('Logique', 'Hypothèse, conclusion, théorème, réciproque, contraposée, propriété caractéristique, contre-exemple, raisonnement par l’absurde.'),
    ('Transformations', '« Demi-tour » ou symétrie centrale ; translation décrite par son effet, sans définition ponctuelle (Troisième).'),
    ('Programmation', 'Condition construite avec <, > ou = ; variable associée à un espace de mémoire.'),
]


def ecrire():
    lignes = ['## Matrice de correspondance : édition 2026-2027 → programme 2026 → édition 2027-2028', '',
              '| Chapitre de l’édition 2026-2027 | Programme 2026 de Quatrième (annexe 2) | Décision dans l’édition 2027-2028 |',
              '|---|---|---|']
    lignes += [f'| {a} | {b} | {c} |' for a, b, c in ANCIEN]
    lignes += ['', '## Objectifs d’apprentissage de Quatrième et chapitres', '', '| Domaine | Objectif (annexe 2) | Chapitres |', '|---|---|---|']
    for domaine, objectifs in OBJECTIFS:
        for obj, ch in objectifs:
            texte = obj.replace('$', '').replace('\\ldots', '…')
            lignes.append(f'| {domaine} | {texte} | {", ".join(str(c) for c in ch)} |')
    lignes += ['', '## Vocabulaire et notations', '', '| Notion | Usage dans l’édition 2027-2028 |', '|---|---|']
    lignes += [f'| {a} | {b} |' for a, b in VOCABULAIRE]
    lignes += ['', '## Repères de progressivité', '',
               'Aucun document de « repères annuels » ou d’« attendus de fin d’année » propre au programme 2026 n’a été trouvé sur Éduscol au 23 octobre 2026 ; '
               'les documents de 2019-2020 accompagnent l’ancien programme. La progression suit donc l’annexe 2 (automatismes et objectifs de la rubrique « Quatrième ») '
               'et les « Exemples pour la mise en œuvre des programmes 2026 · Cycle 4 » (exemples de réussite), en réactivant comme automatismes les notions de Cinquième '
               '(sommes de fractions, diagrammes circulaires, demi-tour, parallélogrammes, volumes du prisme et du cylindre).', '']
    (ROOT / 'build').mkdir(exist_ok=True)
    (ROOT / 'build/matrice-programme.md').write_text('\n'.join(lignes), encoding='utf8')
    print('matrice :', len(ANCIEN), 'chapitres,', sum(len(o) for _, o in OBJECTIFS), 'objectifs')


if __name__ == '__main__':
    ecrire()
