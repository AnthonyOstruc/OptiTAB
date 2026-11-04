"""Problèmes de modélisation : lettres, équations, proportionnalité, repérage."""
from fractions import Fraction as F
from modele_5e import ex, q, n, m


def formules(i, niveau):
    a, b, rang = 2+i%3, 1+niveau, 4+i+niveau
    def f(x): return a*x+b
    return ex(['Les allumettes du motif', 'La frise du collège', 'Une construction par étapes'][i%3],
        f'Une frise est construite par étapes. Au rang 1, elle utilise {f(1)} allumettes. Chaque rang supplémentaire ajoute {a} allumettes. Le rang n est un entier positif.', [
        q('Calculer le nombre d’allumettes aux rangs 2 et 3.', 'Passer au rang suivant revient à ajouter la même quantité ; poursuivre la construction deux fois.', f'Rang 2 : {f(2)} ; rang 3 : {f(3)}.', m(f'{f(1)}+{a}={f(2)} \\ ;\\ {f(2)}+{a}={f(3)}')),
        q('Proposer une formule donnant le nombre d’allumettes au rang n.', 'On peut partir du premier rang et ajouter a allumettes n−1 fois, ou isoler un bloc fixe et n blocs identiques.', m(f'{a}(n-1)+{f(1)}={a}n+{b}')+' allumettes.'),
        q(f'Utiliser cette formule au rang {rang}.', 'Remplacer la lettre n par le rang demandé ; effectuer la multiplication avant l’addition.', f'{f(rang)} allumettes.', m(f'{a}\\times {rang}+{b}={f(rang)}'), f'{a}*{rang}+{b} == {f(rang)}'),
        q('La formule proposée correspond-elle aux trois premiers rangs ?', 'Un contrôle vérifie des cas connus ; il aide à détecter une erreur de formule.', f'Oui : elle donne {f(1)}, {f(2)} et {f(3)} pour n égal à 1, 2 et 3.'),
        q(f'À quel rang obtient-on {f(rang+2)} allumettes ?', 'Enlever la partie fixe puis chercher combien de blocs identiques restent. Vérifier en remplaçant dans la formule.', f'Au rang {rang+2}.', m(f'({f(rang+2)}-{b})\\div {a}={rang+2}')),
        q('Doubler le rang double-t-il le nombre d’allumettes ? Justifier.', 'Comparer le nombre au rang 2n et le double du nombre au rang n. La partie fixe n’est comptée qu’une fois dans la construction.', f'Non : au rang {2*rang}, on a {f(2*rang)} allumettes ; le double de {f(rang)} vaut {2*f(rang)}.', m(f'{f(2*rang)}\\ne {2*f(rang)}'), f'({a}*{2*rang}+{b}) != 2*({a}*{rang}+{b})')],
        'Une lettre peut représenter un rang variable. Tester des valeurs vérifie une formule sur ces cas ; expliquer la construction justifie la formule pour tous les rangs.',
        dict(type='table', headers=['Rang',1,2,3], rows=[['Allumettes',f(1),f(2),f(3)]]), True)


def distributivite(i, niveau):
    k, ajout, x = 2+niveau, 2+i, 3+i+niveau
    return ex(['Les rectangles découpés', 'La banderole de l’atelier', 'Deux méthodes pour une aire'][i%3],
        f'Un rectangle a une hauteur de {k} cm et une largeur de x + {ajout} cm, avec x positif. On le partage en deux rectangles de largeurs x cm et {ajout} cm.', [
        q('Exprimer l’aire du grand rectangle avec des parenthèses.', 'L’aire d’un rectangle est largeur fois hauteur. Toute la largeur doit être multipliée par la hauteur.', m(f'{k}(x+{ajout})')+' cm².'),
        q('Exprimer séparément les aires des deux petits rectangles.', 'Chaque petit rectangle garde la même hauteur ; on calcule son aire avec sa propre largeur.', m(f'{k}x')+' cm² et '+m(str(k*ajout))+' cm².'),
        q('En déduire une expression développée de l’aire totale.', 'Les deux petits rectangles recouvrent exactement le grand, sans chevauchement : on additionne leurs aires.', m(f'{k}(x+{ajout})={k}x+{k*ajout}')+'.'),
        q(f'Calculer l’aire lorsque x = {x} cm, avec les deux expressions.', 'La formule avec parenthèses et sa forme développée doivent donner la même valeur après remplacement de x.', f'{k*(x+ajout)} cm².', m(f'{k}({x}+{ajout})={k*(x+ajout)} \\ ;\\ {k}\\times {x}+{k*ajout}={k*(x+ajout)}'), f'{k}*({x}+{ajout}) == {k}*{x}+{k*ajout} == {k*(x+ajout)}'),
        q(f'Un élève propose {k}x + {ajout}. Expliquer son erreur.', 'Le facteur devant une parenthèse multiplie chacun des termes. Le petit rectangle fixe a pour aire hauteur fois largeur.', f'Il a oublié de multiplier {ajout} par {k}. Le terme fixe doit être {k*ajout}.'),
        q('Si x augmente de 1 cm, de combien l’aire augmente-t-elle ? Justifier pour toute valeur de x.', 'Une bande de largeur 1 cm et de hauteur k cm est ajoutée. On peut aussi soustraire les deux expressions développées.', f'De {k} cm².', m(f'[{k}(x+1)+{k*ajout}]-({k}x+{k*ajout})={k}'))],
        'Distribuer signifie multiplier tous les termes de la parenthèse. Une lettre désigne un nombre ; on ne mélange pas des longueurs et des aires.',
        dict(type='rectangle', width=x, extension=ajout, height=k), True)


def equations(i, niveau):
    a, x, b = 2+i%3, 4+i+niveau, (0 if i==6 else 2+niveau)
    total=a*x+b
    return ex(['Les pochettes surprises', 'Le prix des places', 'Une commande à retrouver'][i%3],
        f'On achète {a} pochettes identiques et un emballage à {b} €. La facture totale est de {total} €. On appelle x le prix, en euros, d’une pochette.', [
        q('Que représente l’inconnue x ? Quelle unité utilise-t-on ?', 'Nommer précisément la quantité cherchée évite de résoudre une autre question.', 'x est le prix d’une seule pochette, en euros.'),
        q('Écrire l’équation traduisant la facture.', 'Le prix des pochettes est leur nombre multiplié par le prix unitaire ; on ajoute le seul emballage.', m(f'{a}x+{b}={total}')+'.'),
        q('Quel est le prix total des seules pochettes ?', 'L’emballage est connu : on le retire du total, ce qui revient à soustraire la même quantité aux deux membres.', f'{total-b} €.', m(f'{total}-{b}={total-b}')),
        q('Résoudre l’équation et donner le prix d’une pochette.', 'Partager le prix total des pochettes entre les pochettes identiques ; le coefficient de x est non nul.', f'x = {x} ; une pochette coûte {x} €.', m(f'x=({total}-{b})\\div {a}={x}'), f'F({total}-{b},{a}) == {x}'),
        q('Vérifier la solution dans la facture de départ.', 'Remplacer x par le prix trouvé et recalculer le membre de gauche. Il doit être égal au total annoncé.', m(f'{a}\\times {x}+{b}={total}')+' : la facture est vérifiée.', controle=f'{a}*{x}+{b} == {total}'),
        q('Si la facture augmente de 6 € avec le même emballage et le même nombre de pochettes, de combien le prix unitaire augmente-t-il ?', 'Toute l’augmentation concerne les pochettes : partager 6 € entre elles. On ne rajoute pas 6 € à chaque pochette.', m(n(F(6,a)))+' € par pochette ; nouveau prix '+m(n(x+F(6,a)))+' €.')],
        'Résoudre une équation consiste à trouver la valeur qui rend l’égalité vraie. Une vérification remplace l’inconnue dans l’égalité initiale.',
        dict(type='flow', labels=[f'{a} pochettes à x €', f'+ {b} €', f'= {total} €']), True)


def proportionnalite(i, niveau):
    if i%3 == 2:
        prix = 40+20*i+10*niveau
        taux = [10,20,25][niveau]
        reduction = F(prix*taux,100)
        return ex('Une réduction à expliquer', f'Un sac coûte {prix} €. Le magasin annonce une remise de {taux} % sur ce prix initial, sans autres frais.', [
            q('Quelle quantité représente 100 % dans cette situation ?', 'Le pourcentage prend comme référence le prix avant toute remise.', f'Le prix initial : {prix} €.'),
            q('Calculer 1 % du prix initial.', 'Un pour cent est une part sur cent ; diviser le prix de référence par 100.', m(n(F(prix,100)))+' €.'),
            q('Calculer le montant de la remise.', 'Multiplier la valeur de 1 % par le taux de réduction.', m(n(reduction))+' €.', m(rf'{prix}\times \frac{{{taux}}}{{100}}={n(reduction)}'), f'F({prix}*{taux},100) == F("{reduction}")'),
            q('Calculer le prix payé.', 'Une remise est retranchée du prix initial ; son montant n’est pas le prix final.', m(n(prix-reduction))+' €.', m(f'{prix}-{n(reduction)}={n(prix-reduction)}')),
            q('Quel pourcentage du prix initial est payé ?', 'Le prix initial représente 100 % : enlever la part remise.', f'{100-taux} %.'),
            q('Deux sacs identiques bénéficient de la même remise. Calculer la dépense totale et vérifier par une seconde méthode.', 'On peut doubler le prix réduit, ou calculer la remise sur le prix de deux sacs : les deux chemins doivent coïncider.', m(n(2*(prix-reduction)))+' €.', m(f'2\\times {n(prix-reduction)}={n(2*(prix-reduction))}'), f'2*({prix}-F("{reduction}")) == 2*{prix}*(1-F({taux},100))')],
            'Un pourcentage est une fraction d’une référence. Toujours distinguer le montant de la remise et le prix à payer.',
            dict(type='percent', rate=taux, total=prix), True)
    personnes, cible = 4+i%3, 6+i+2*niveau
    farine = personnes*(50+10*niveau)
    par_personne=farine//personnes
    return ex('Adapter la recette', f'Une recette pour {personnes} personnes demande {farine} g de farine. Les quantités sont proportionnelles au nombre de personnes.', [
        q('Quelle quantité faut-il pour une personne ?', 'Revenir à l’unité : diviser la quantité connue par le nombre de personnes.', f'{par_personne} g.', m(f'{farine}\\div {personnes}={par_personne}')),
        q(f'Quelle quantité faut-il pour {cible} personnes ?', 'Chaque personne demande la même quantité ; multiplier le nombre de personnes par la quantité pour une personne.', f'{cible*par_personne} g.', m(f'{cible}\\times {par_personne}={cible*par_personne}'), f'F({farine},{personnes})*{cible} == {cible*par_personne}'),
        q('Donner le coefficient permettant de passer du nombre de personnes à la masse de farine.', 'Le coefficient est la masse divisée par le nombre de personnes ; préciser le sens du passage entre les lignes.', f'{par_personne} g par personne.'),
        q(f'Avec {par_personne*(cible+2)} g, pour combien de personnes peut-on cuisiner ?', 'On connaît la masse : diviser par la masse par personne pour retrouver le nombre de personnes.', f'{cible+2} personnes.', m(f'{par_personne*(cible+2)}\\div {par_personne}={cible+2}')),
        q('Si on double le nombre de personnes, que devient la masse de farine ?', 'Dans une situation proportionnelle, multiplier une grandeur par 2 multiplie aussi l’autre par 2.', f'Elle double : {2*farine} g pour {2*personnes} personnes.'),
        q('Une autre recette contient une base fixe de 100 g puis la même masse par personne. Est-elle proportionnelle au nombre de personnes ?', 'Comparer les masses pour une et deux personnes. Le doublement doit être respecté pour qu’il y ait proportionnalité.', f'Non : {100+par_personne} g pour 1 personne et {100+2*par_personne} g pour 2 ; le second nombre n’est pas le double du premier.')],
        'La proportionnalité se reconnaît à un même coefficient. Deux grandeurs qui augmentent ensemble ne sont pas forcément proportionnelles.',
        dict(type='table', headers=['Personnes',personnes,1,cible], rows=[['Farine (g)',farine,'?','?']]), True)


def reperage(i, niveau):
    if i%2:
        coeff, fixe = 2+niveau, 1+i
        x=3+i
        return ex('Le tarif du parcours', f'Un parcours de loisirs coûte {fixe} € de droit d’entrée, puis {coeff} € par activité. On note n le nombre d’activités et P le prix total en euros.', [
            q('Écrire une formule pour P en fonction de n.', 'Additionner la partie fixe et la partie qui dépend du nombre d’activités.', m(f'P={coeff}n+{fixe}')+'.'),
            q('Compléter les prix pour n = 0, 1 et 2.', 'Remplacer n par chaque valeur ; même avec zéro activité, le droit d’entrée est payé.', f'{fixe} €, {fixe+coeff} €, {fixe+2*coeff} €.'),
            q(f'Calculer le prix de {x} activités.', 'La multiplication du nombre d’activités par le tarif variable précède l’addition de la partie fixe.', f'{coeff*x+fixe} €.', m(f'{coeff}\\times {x}+{fixe}={coeff*x+fixe}'), f'{coeff}*{x}+{fixe} == {coeff*x+fixe}'),
            q('Quelles coordonnées placer pour représenter deux activités ?', 'L’abscisse désigne le nombre d’activités, l’ordonnée le prix ; l’ordre des coordonnées est imposé par les axes.', m(f'(2\\ ;\\ {fixe+2*coeff})')+'.'),
            q('La relation est-elle proportionnelle ?', 'Tester le prix pour zéro activité et le doublement : une situation proportionnelle doit passer par l’origine.', f'Non : pour zéro activité, le prix est {fixe} €, différent de zéro.'),
            q(f'Combien d’activités peut-on faire avec {coeff*(x+1)+fixe} € ?', 'Retirer le droit d’entrée, puis diviser le reste par le prix d’une activité.', f'{x+1} activités.', m(f'({coeff*(x+1)+fixe}-{fixe})\\div {coeff}={x+1}'))],
            'Les axes doivent indiquer leur grandeur et leur unité. Lire une ordonnée et lire une abscisse ne répondent pas à la même question.',
            dict(type='graph', coefficient=coeff, fixed=fixe, max_x=x), True)
    x,y=2+i+niveau,3+niveau
    return ex('Le plan du jardin', f'Sur un plan muni d’un repère orthogonal, une unité vaut 1 m. Les points A({-x} ; {y}), B({x} ; {y}), C({x} ; {-y}) et D({-x} ; {-y}) sont les sommets d’un jardin rectangulaire.', [
        q('Donner l’abscisse et l’ordonnée de A.', 'La première coordonnée se lit sur l’axe horizontal et la seconde sur l’axe vertical.', f'Abscisse : {-x} ; ordonnée : {y}.'),
        q('Quels points sont au-dessus de l’axe horizontal ?', 'Au-dessus de cet axe, l’ordonnée est strictement positive.', 'A et B.'),
        q('Pourquoi le segment AB est-il horizontal ?', 'Deux points distincts ayant la même ordonnée sont sur une droite parallèle à l’axe horizontal.', f'A et B ont la même ordonnée {y}.'),
        q('Calculer la longueur AB.', 'Sur une horizontale, compter l’écart des abscisses ; les points sont de part et d’autre de l’axe vertical.', f'{2*x} m.', m(f'{x}-({-x})={2*x}'), f'{x}-({-x}) == {2*x}'),
        q('Calculer la longueur BC, puis l’aire du jardin.', 'Sur une verticale, la distance est l’écart des ordonnées. L’aire du rectangle est le produit de ses deux dimensions.', f'BC = {2*y} m ; aire = {4*x*y} m².', m(f'{2*x}\\times {2*y}={4*x*y}')),
        q('Donner les coordonnées du centre du jardin et justifier.', 'Les sommets opposés ont des coordonnées opposées. Leurs milieux sont à l’origine ; le centre est à mi-distance des côtés opposés.', 'O(0 ; 0), milieu de chacune des deux diagonales.')],
        'Lire d’abord horizontalement puis verticalement. Une distance est positive ; une coordonnée peut être négative.',
        dict(type='coordinates', x=x,y=y), True)


BUILDERS={'formules':formules,'distributivite':distributivite,'equations':equations,
    'proportionnalite':proportionnalite,'reperage':reperage}
