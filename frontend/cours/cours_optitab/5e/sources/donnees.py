"""Données, hasard et pensée informatique : interpréter avant de calculer."""
from fractions import Fraction as F
from modele_5e import ex,q,n,m


def statistiques(i,niveau):
    if i%2:
        valeurs=[2+i,3+i,4+i,5+i,6+i]
        moyenne=4+i
        ajout=2+niveau
        return ex('Le suivi des lectures',
            'Cinq élèves ont lu respectivement '+', '.join(map(str,valeurs))+f' livres ce trimestre. On veut décrire cette petite série et comprendre l’effet d’une modification des données.', [
            q('Quelle est la population étudiée ? Quel caractère mesure-t-on ?', 'La population est le groupe observé ; le caractère est la quantité relevée pour chaque individu.', 'Les cinq élèves ; le nombre de livres lus par élève.'),
            q('Quel est l’effectif total et quelle est la somme des valeurs ?', 'L’effectif compte les élèves, la somme additionne les livres ; ce ne sont pas les mêmes grandeurs.', f'5 élèves ; {sum(valeurs)} livres au total.', controle=f'sum({valeurs}) == {sum(valeurs)}'),
            q('Calculer la moyenne du nombre de livres lus.', 'Répartir équitablement la somme des valeurs entre les cinq élèves : moyenne = somme / effectif.', f'{moyenne} livres par élève.', m(f'{sum(valeurs)}\\div5={moyenne}'), f'F(sum({valeurs}),5) == {moyenne}'),
            q('La moyenne doit-elle être une valeur effectivement observée ?', 'Une moyenne décrit une répartition théorique. Ici elle figure dans la série, mais ce n’est pas une obligation générale.', f'Non. Ici {moyenne} est observé ; pour 1 et 2 livres, la moyenne serait 1,5 livre, sans être observée.'),
            q(f'Si chaque élève lit {ajout} livres supplémentaires, quelle devient la moyenne ?', 'La somme augmente de cinq fois le même ajout ; en divisant par cinq, la moyenne augmente de cet ajout.', f'{moyenne+ajout} livres par élève.', m(f'({sum(valeurs)}+5\\times {ajout})\\div5={moyenne+ajout}')),
            q('Une autre classe de 20 élèves a la même moyenne initiale. A-t-elle lu le même nombre total de livres ?', 'Une moyenne égale n’impose pas un total égal lorsque les effectifs diffèrent. Multiplier la moyenne par le nombre d’élèves.', f'Non : {20*moyenne} livres contre {sum(valeurs)} ; elle en a lu quatre fois plus.')],
            'Toujours préciser ce qu’on compte. Une moyenne est un indicateur ; elle ne décrit pas à elle seule la répartition des données.',
            dict(type='bars',labels=['A','B','C','D','E'],values=valeurs,ylabel='Livres lus'),True)
    a,b,c=4+i+2*niveau,6+i+2*niveau,10+2*i+4*niveau
    total=a+b+c
    return ex('L’enquête sur les trajets',
        f'Une classe a demandé à chaque élève son mode principal de trajet. On obtient {a} réponses « marche », {b} réponses « vélo » et {c} réponses « bus ». Chaque élève donne une seule réponse.', [
        q('Quel est l’effectif total de l’enquête ?', 'Les trois catégories sont exclusives et couvrent toutes les réponses : additionner leurs effectifs.', f'{total} élèves.', m(f'{a}+{b}+{c}={total}'), f'{a}+{b}+{c} == {total}'),
        q('Quel mode est le plus fréquent ? Quelle est sa fréquence ?', 'Repérer le plus grand effectif puis le diviser par l’effectif total. Une fréquence n’est pas un effectif.', f'Le bus : '+m(n(F(c,total)))+', soit 50 %.'),
        q('Donner la fréquence des élèves qui viennent à pied.', 'Le numérateur est le nombre de réponses « marche », le dénominateur le nombre total de réponses.', m(rf'\frac{{{a}}}{{{total}}}='+n(F(a,total)))+'.'),
        q('Quelle fraction des élèves vient à pied ou à vélo ?', 'Les catégories sont disjointes : additionner leurs effectifs avant de diviser par le total.', m(rf'\frac{{{a+b}}}{{{total}}}=\frac12')+', soit 50 %.'),
        q('Quel angle représente la catégorie « bus » dans un diagramme circulaire ?', 'Le disque entier mesure 360° ; prendre la même fraction de 360° que la fréquence des réponses.', '180°.', m(r'\frac12\times360=180')),
        q('Une autre classe compte deux fois plus d’élèves et 50 % de réponses « bus ». Combien prennent le bus ? Peut-on comparer les classes avec les seuls secteurs ?', 'Une proportion doit être associée à un effectif total pour retrouver un nombre d’élèves. Des secteurs de même angle peuvent représenter des effectifs différents.', f'{2*c} élèves prennent le bus. Non : les secteurs seuls ne donnent pas les effectifs des deux classes.')],
        'Dans un diagramme circulaire, un angle représente une proportion. Comparer les nombres de personnes nécessite de connaître les effectifs totaux.',
        dict(type='bars',labels=['Marche','Vélo','Bus'],values=[a,b,c],ylabel='Nombre d’élèves'),True)


def probabilites(i,niveau):
    rouge,bleu,vert=2+i,3+niveau,1+i%2
    total=rouge+bleu+vert
    return ex('Un tirage dans le sac',
        f'Un sac opaque contient {rouge} jetons rouges, {bleu} jetons bleus et {vert} jeton(s) vert(s). Les jetons ont même forme et même masse. On mélange puis on tire un jeton sans regarder. Chaque jeton a la même chance d’être tiré.', [
        q('Combien de jetons le sac contient-il ? Les couleurs sont-elles nécessairement équiprobables ?', 'Les issues élémentaires sont les jetons individuels. Des couleurs ne sont équiprobables que si elles ont le même nombre de jetons.', f'{total} jetons. Les couleurs ne sont pas nécessairement équiprobables : leurs effectifs sont à comparer.'),
        q('Calculer la probabilité de tirer un jeton rouge.', 'Dans une situation d’équiprobabilité des jetons, diviser le nombre de jetons favorables par le nombre total.', m(rf'\frac{{{rouge}}}{{{total}}}='+n(F(rouge,total)))+'.', controle=f'0 <= F({rouge},{total}) <= 1'),
        q('Calculer la probabilité de tirer un jeton bleu ou vert.', 'Un jeton ne peut pas être bleu et vert à la fois ; additionner les effectifs favorables.', m(rf'\frac{{{bleu+vert}}}{{{total}}}='+n(F(bleu+vert,total)))+'.'),
        q('Quelle relation relie les probabilités des deux questions précédentes ?', '« Rouge » et « pas rouge » sont des événements contraires : ils couvrent tous les jetons sans chevauchement.', 'Leur somme est égale à 1.', m(rf'\frac{{{rouge}}}{{{total}}}+\frac{{{bleu+vert}}}{{{total}}}=1'), f'F({rouge},{total})+F({bleu+vert},{total}) == 1'),
        q('Donner un événement impossible puis un événement certain.', 'Un événement impossible ne contient aucune issue ; un événement certain contient toutes les issues possibles.', 'Impossible : tirer un jeton jaune (probabilité 0). Certain : tirer un jeton rouge, bleu ou vert (probabilité 1).'),
        q('Après avoir tiré un jeton rouge puis l’avoir remis dans le sac, est-on certain de tirer une autre couleur au tirage suivant ?', 'La remise rétablit exactement la composition initiale. Un résultat passé n’oblige pas le hasard à compenser.', 'Non. Après mélange, la probabilité de rouge reste '+m(n(F(rouge,total)))+' ; deux rouges successifs restent possibles.')],
        'La formule « favorables / possibles » suppose l’équiprobabilité des issues élémentaires. Une probabilité ne prédit pas avec certitude un tirage particulier.',
        dict(type='urn',red=rouge,blue=bleu,green=vert),True)


def programmation(i,niveau):
    if i%3==1:
        pas=10+5*niveau
        tours=4
        return ex('Programmer le tracé d’un carré',
            f'Un lutin part d’un point A, orienté vers la droite, stylo baissé. Il exécute : « répéter {tours} fois : avancer de {pas} pas ; tourner à gauche de 90° ». Un pas est une unité de longueur.', [
            q('Combien de déplacements le programme exécute-t-il ?', 'La boucle répète son contenu quatre fois ; il y a une instruction avancer par tour.', '4 déplacements.'),
            q('Quelle distance totale le lutin parcourt-il ?', 'Additionner les quatre déplacements de même longueur. Cette distance est le périmètre du tracé.', f'{4*pas} pas.', m(f'4\\times {pas}={4*pas}'), f'4*{pas} == {4*pas}'),
            q('Quel angle total a-t-il tourné ?', 'Une rotation de 90° est exécutée à chaque tour de boucle, y compris le dernier.', '360°, soit un tour complet.', m(r'4\times90=360')),
            q('Quelle figure obtient-on ? Justifier.', 'Quatre côtés égaux sont tracés avec quatre angles droits. Après quatre déplacements, le lutin revient au point de départ.', f'Un carré de côté {pas} pas.'),
            q('Quelle est la position et l’orientation finales du lutin ?', 'Suivre les déplacements droite, haut, gauche, bas ; la quatrième rotation ramène l’orientation initiale.', 'Au point A, orienté vers la droite.'),
            q('On enlève la dernière rotation seulement. Le dessin change-t-il ? L’état final change-t-il ?', 'Une rotation sans déplacement ne dessine pas de segment ; elle modifie seulement l’orientation du lutin.', 'Le carré reste identique, mais le lutin termine orienté vers le bas : il lui manque le dernier quart de tour.')],
            'Distinguer le dessin, la position et l’orientation. Une boucle compacte plusieurs instructions, mais chaque instruction est exécutée dans l’ordre.',
            dict(type='program',lines=['Quand le drapeau est cliqué','Stylo en position écriture','Répéter 4 fois',f'    avancer de {pas} pas','    tourner à gauche de 90°']),True)
    entree=2+i
    facteur=2+niveau
    ajout=3+i
    final=facteur*entree+ajout
    return ex('Lire une donnée et prévoir une sortie',
        f'Le programme demande un nombre, puis affiche le résultat de « {facteur} × réponse + {ajout} ». Le bloc « réponse » lit la donnée saisie ; cette donnée n’est pas modifiée.', [
        q('Quelle est l’entrée du programme ? Quelle est sa sortie ?', 'L’entrée est la donnée demandée ; la sortie est le résultat affiché après le calcul.', f'Entrée : le nombre saisi. Sortie : {facteur} fois ce nombre, plus {ajout}.'),
        q(f'Quel calcul est effectué pour l’entrée {entree} ?', 'Remplacer le bloc réponse par la donnée saisie, sans changer les opérations.', m(f'{facteur}\\times {entree}+{ajout}')+'.'),
        q('Prévoir le nombre affiché pour cette entrée.', 'Effectuer la multiplication avant l’addition ; la donnée saisie reste inchangée.', str(final)+'.', m(f'{facteur}\\times {entree}+{ajout}={final}'), f'{facteur}*{entree}+{ajout} == {final}'),
        q('Quel nombre est affiché si on saisit 0 ?', 'Remplacer réponse par zéro ; seul le terme ajouté subsiste.', str(ajout)+'.', m(f'{facteur}\\times0+{ajout}={ajout}')),
        q(f'On imbrique autrement les blocs pour calculer {facteur} × (réponse + {ajout}). Quel résultat obtient-on pour l’entrée {entree} ?', 'Les blocs imbriqués imposent les parenthèses : additionner avant de multiplier change le programme.', str(facteur*(entree+ajout))+'.', m(f'{facteur}({entree}+{ajout})={facteur*(entree+ajout)}')),
        q('Les deux organisations de blocs représentent-elles la même formule ? Justifier.', 'Développer la formule avec parenthèses : l’ajout est alors multiplié par le facteur. Un exemple de résultats différents suffit aussi à distinguer les programmes.', f'Non : le premier affiche {final}, le second {facteur*(entree+ajout)} pour la même entrée.')],
        'En 5e, on lit une donnée saisie pour calculer une formule. Prévoir la sortie avant d’exécuter et contrôler l’imbrication des blocs.',
        dict(type='program',lines=['Quand le drapeau est cliqué','Demander un nombre',f'Dire ({facteur} × réponse + {ajout})']),True)


BUILDERS={'statistiques':statistiques,'probabilites':probabilites,'programmation':programmation}
