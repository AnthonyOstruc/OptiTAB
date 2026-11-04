"""Enquêtes, probabilités et instructions sans notion hors programme."""
from fractions import Fraction as F
from modele_6e import ex,q,n,m


def donnees(i,l):
    if i%2:
        a,b,c,d=7+i,3+l,6+i,4+l
        total=a+b+c+d
        return ex('Lire un tableau à double entrée',f'Deux classes ont répondu à une enquête sur le trajet. En 6e A, {a} élèves viennent à pied et {b} en bus. En 6e B, {c} élèves viennent à pied et {d} en bus. Pour cette enquête, tous les élèves choisissent exactement l’un de ces deux modes.',[
            q('Combien d’élèves de 6e A ont répondu ?', 'Additionner les effectifs de la ligne 6e A ; les deux réponses sont exclusives et couvrent toute la classe.', f'{a+b} élèves.'),
            q('Combien d’élèves de 6e B ont répondu ?', 'Appliquer le même comptage à la seconde ligne.', f'{c+d} élèves.'),
            q('Combien d’élèves viennent à pied dans les deux classes ?', 'Additionner cette fois la colonne à pied ; ne pas confondre le total d’une ligne et celui d’une colonne.', f'{a+c} élèves.'),
            q('Combien d’élèves viennent en bus dans les deux classes ?', 'Additionner la colonne bus pour réunir les deux classes.', f'{b+d} élèves.'),
            q('Déterminer l’effectif total et le vérifier de deux façons.', 'Le total des lignes doit être égal au total des colonnes ; ce contrôle détecte une omission ou un double comptage.', f'{total} élèves.', m(f'{a+b}+{c+d}={a+c}+{b+d}={total}'), f'({a}+{b})+({c}+{d}) == ({a}+{c})+({b}+{d}) == {total}'),
            q('Quelle classe a la plus grande proportion de marcheurs ? Justifier par des fractions.', f'Ici les deux classes comptent {a+b} élèves. Les fractions ont donc le même dénominateur avant simplification : comparer leurs numérateurs.', '6e A : '+m(rf'\frac{{{a}}}{{{a+b}}}')+' ; 6e B : '+m(rf'\frac{{{c}}}{{{c+d}}}')+f'. La 6e A a la plus grande proportion, car {a} > {c}.')],
            'Une ligne répond à une catégorie, une colonne à une autre. Le double total permet de contrôler un tableau.',
            dict(type='table',headers=['Classe','À pied','Bus','Total'],rows=[['6e A',a,b,'?'],['6e B',c,d,'?'],['Total','?','?','?']]),True)
    values=[8+i+2*l,12+i+2*l,16+2*i+4*l]
    total=sum(values)
    return ex('Choisir une représentation pour l’enquête',f'Pour une sortie, {values[0]} élèves choisissent le musée, {values[1]} le parc et {values[2]} le stade. Chaque élève ne choisit qu’une sortie. Le diagramme représente cette enquête.',[
        q('Comment peut-on recueillir ces données ?', 'Une préférence est déclarée par la personne interrogée ; il faut poser la même question à tous.', 'Par un questionnaire avec une seule réponse demandée à chaque élève.'),
        q('Combien d’élèves ont répondu en tout ?', 'Les catégories ne se recouvrent pas ; additionner les trois effectifs.', f'{total} élèves.', controle=f'sum({values}) == {total}'),
        q('Quelle sortie a reçu le plus de réponses ? Quel est son effectif ?', 'La plus haute barre correspond au plus grand effectif ; lire la légende avant de conclure.', f'Le stade : {values[2]} élèves.'),
        q('Combien d’élèves de plus ont choisi le stade que le musée ?', 'Un écart se calcule en soustrayant le plus petit effectif du plus grand.', f'{values[2]-values[0]} élèves.'),
        q('Donner la fraction des élèves qui choisissent le stade.', 'La part d’une catégorie est son effectif divisé par l’effectif total.', m(n(F(values[2],total)))+'.'),
        q('Un diagramme circulaire peut-il représenter cette enquête ? Que faut-il conserver ?', 'Un diagramme circulaire montre les parts d’un tout ; les catégories doivent rester les mêmes et leurs parts doivent remplir tout le disque.', 'Oui. Conserver les trois catégories et leurs proportions ; indiquer aussi l’effectif total pour interpréter les nombres d’élèves.')],
        'Lire le titre, les catégories, l’unité et l’origine de l’axe avant de comparer les barres ; une représentation doit permettre une interprétation fidèle.',
        dict(type='bars',labels=['Musée','Parc','Stade'],values=values,ylabel='Nombre d’élèves'),True)


def probabilites(i,l):
    from scenarios_communs import probabilites as sac,de
    return de(i,l) if i%2 else sac(i,l)


def instructions(i,l):
    from scenarios_communs import programmation
    if i%3!=2:return programmation(i,l)
    marches=3+l+i%3
    return ex('Coder un escalier avec une répétition',f'Un robot part du point D, dirigé vers la droite. Il répète {marches} fois : « avancer de 1 case ; tourner à gauche d’un quart de tour ; avancer de 1 case ; tourner à droite d’un quart de tour ».',[
        q('Combien d’instructions avancer y a-t-il dans une répétition ?', 'Une répétition contient toute la séquence située après répéter ; lire chaque instruction dans l’ordre.', 'Deux instructions avancer.'),
        q('Décrire la première marche.', 'Le robot avance d’abord à droite, puis tourne et avance vers le haut ; la dernière rotation prépare la marche suivante.', 'Une case à droite puis une case vers le haut ; il est de nouveau dirigé vers la droite.'),
        q('Combien de cases le robot parcourt-il en tout ?', 'Chaque marche comprend deux déplacements d’une case ; multiplier par le nombre de marches.', f'{2*marches} cases.', m(f'2\\times{marches}={2*marches}'), f'2*{marches} == {2*marches}'),
        q('Où arrive-t-il par rapport à son point de départ ?', 'Chaque marche ajoute une case horizontalement et une verticalement ; compter les deux directions séparément.', f'{marches} cases à droite et {marches} cases au-dessus de D.'),
        q('Quelle est son orientation finale ?', 'Dans une marche, les quarts de tour à gauche puis à droite se compensent ; chaque marche se termine dans l’orientation initiale.', 'Vers la droite.'),
        q('Que changer pour obtenir deux marches supplémentaires ?', 'Le dessin d’une marche reste identique ; seul le nombre de répétitions doit augmenter.', f'Remplacer {marches} répétitions par {marches+2} répétitions ; le robot parcourra {2*(marches+2)} cases.')],
        'Décrire le chemin, la position finale et l’orientation séparément. Une rotation seule ne fait pas avancer le robot.',
        dict(type='staircase',steps=marches),True)


BUILDERS={'donnees':donnees,'probabilites':probabilites,'instructions':instructions}
