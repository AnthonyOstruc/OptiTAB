"""Situations complémentaires pour couvrir les méthodes et varier les problèmes."""
from fractions import Fraction as F
from math import gcd,lcm
from modele_5e import ex,q,n,m


def bouteilles(i,l):
    unite=F([25,50,75][l],100)
    pleines=8+i
    reste=F(1,10)
    volume=pleines*unite+reste
    return ex('Remplir des bouteilles sans gaspiller',f'On dispose de {m(n(volume))} L de jus. Chaque bouteille peut contenir {m(n(unite))} L. On remplit les bouteilles une par une.',[
        q('Quelle opération donne le nombre théorique de bouteilles ?', 'On cherche combien de fois une capacité est contenue dans le volume disponible : il s’agit d’une division.', m(f'{n(volume)}\\div {n(unite)}')+'.'),
        q('Transformer cette division pour obtenir un diviseur entier.', 'Multiplier dividende et diviseur par 100 conserve le quotient. Ne pas multiplier seulement le diviseur.', m(f'{n(volume*100)}\\div {n(unite*100)}')+'.'),
        q('Combien de bouteilles peut-on remplir entièrement ?', 'Chercher le plus grand nombre entier de bouteilles dont le volume total ne dépasse pas le volume disponible.', f'{pleines} bouteilles.', m(f'{pleines}\\times {n(unite)}={n(pleines*unite)}'), f'F("{unite}")*{pleines} <= F("{volume}") < F("{unite}")*{pleines+1}'),
        q('Quel volume reste-t-il après ce remplissage ?', 'Soustraire le volume utilisé du volume initial. Le reste doit être plus petit que la capacité d’une bouteille.', '0,1 L, soit 100 mL.', m(f'{n(volume)}-{n(pleines*unite)}=0{{,}}1')),
        q('Combien de bouteilles faut-il pour emporter tout le jus ?', 'Même partiellement remplie, la dernière bouteille est nécessaire pour le reste.', f'{pleines+1} bouteilles.'),
        q('Quel volume manque-t-il pour remplir aussi la dernière bouteille ?', 'Compléter le reste jusqu’à la capacité de la bouteille. Contrôler en ajoutant le volume manquant au volume disponible.', m(n(unite-reste))+' L.', m(f'{n(unite)}-0{{,}}1={n(unite-reste)}'))],
        'Un quotient exact, un nombre de contenants pleins et un nombre de contenants nécessaires ne répondent pas à la même question.',
        dict(type='flow',labels=[f'{float(volume):g} L',f'÷ {float(unite):g} L','Bouteilles ?']))


def lots(i,l):
    k=2+l+i%3
    rouges,bleues=12*k,18*k
    communs=[d for d in range(1,min(rouges,bleues)+1) if rouges%d==bleues%d==0]
    maxi=gcd(rouges,bleues)
    return ex('Des lots identiques pour la fête',f'Le club possède {rouges} cartes rouges et {bleues} cartes bleues. Il veut fabriquer des lots identiques contenant les deux couleurs, sans laisser de carte.',[
        q(f'Vérifier que {rouges} est divisible par 2 et par 3.', 'Pour 2, regarder le chiffre des unités ; pour 3, additionner les chiffres. Contrôler ensuite les quotients entiers.', f'Oui : il est pair et sa somme de chiffres vaut {sum(map(int,str(rouges)))} ; les quotients sont {rouges//2} et {rouges//3}.'),
        q('Peut-on fabriquer six lots identiques ? Donner leur composition.', 'Le nombre de lots doit diviser chacun des effectifs. Diviser chaque couleur séparément par 6.', f'Oui : {rouges//6} cartes rouges et {bleues//6} cartes bleues par lot.'),
        q('Lister tous les nombres de lots possibles.', 'Chercher les diviseurs de chaque effectif puis conserver les diviseurs communs ; tester de manière organisée.', ', '.join(map(str,communs))+'.', controle=f'all({rouges}%d==0 and {bleues}%d==0 for d in {communs})'),
        q('Quel est le plus grand nombre de lots possible ?', 'La liste organisée permet de choisir le plus grand diviseur commun ; aucun algorithme de PGCD n’est nécessaire.', f'{maxi} lots.'),
        q('Quelle sera alors la composition d’un lot ?', 'Partager chaque couleur entre le nombre maximal de lots trouvé.', f'{rouges//maxi} cartes rouges et {bleues//maxi} cartes bleues.', m(f'{rouges}\\div {maxi}={rouges//maxi} \\ ;\\ {bleues}\\div {maxi}={bleues//maxi}')),
        q('Pourquoi ne peut-on pas choisir un nombre de lots plus grand simplement en partageant le total des cartes ?', 'Les lots doivent avoir la même composition en couleurs, et non seulement le même nombre total de cartes.', 'Il faut diviser séparément chaque effectif : un diviseur du total peut ne pas diviser le nombre de cartes rouges ou bleues.')],
        '« Identiques » impose une contrainte pour chaque catégorie. Tester seulement le total oublie la composition des lots.',
        dict(type='table',headers=['Couleur','Rouges','Bleues'],rows=[['Cartes',rouges,bleues]]))


def periodes(i,l):
    a,b=4+i,6+2*l
    rencontre=lcm(a,b)
    return ex('Quand les deux signaux se retrouveront-ils ?',f'Deux signaux lumineux s’allument ensemble à l’instant 0. Le premier se rallume toutes les {a} secondes et le second toutes les {b} secondes.',[
        q('Donner les cinq premiers instants strictement positifs du premier signal.', 'Les instants sont les multiples positifs de sa période.', ', '.join(str(a*k) for k in range(1,6))+' secondes.'),
        q('Donner les cinq premiers instants strictement positifs du second signal.', 'Appliquer la même méthode à sa propre période, sans additionner les deux périodes.', ', '.join(str(b*k) for k in range(1,6))+' secondes.'),
        q('Déterminer le premier instant positif où les signaux s’allument ensemble.', 'Continuer si nécessaire les deux listes de multiples jusqu’au premier nombre commun strictement positif.', f'{rencontre} secondes.', controle=f'{rencontre}%{a} == 0 and {rencontre}%{b} == 0 and not any(t%{a}==0 and t%{b}==0 for t in range(1,{rencontre}))'),
        q('Combien de périodes de chaque signal se sont écoulées à cet instant ?', 'Diviser l’instant commun par chacune des périodes.', f'{rencontre//a} périodes du premier ; {rencontre//b} du second.'),
        q('Donner les deux instants communs suivants.', 'Une fois les signaux réunis, le même cycle recommence ; ajouter la durée de ce cycle.', f'{2*rencontre} s et {3*rencontre} s.'),
        q('Pourquoi la somme des deux périodes ne donne-t-elle pas toujours une rencontre ?', 'Un instant de rencontre doit être multiple des deux périodes. Une somme n’a pas forcément cette propriété.', f'Il faut que l’instant soit divisible à la fois par {a} et par {b}, ce que la somme seule ne garantit pas.')],
        'Un problème de rendez-vous utilise des multiples communs ; un problème de lots identiques utilise des diviseurs communs.',
        dict(type='table',headers=['Signal','Période (s)'],rows=[['Premier',a],['Second',b]]))


def comparaison(i,l):
    den=6+2*i
    a,b=2+l,3+l
    f,g=F(a,den),F(b,den*2)
    return ex('Comparer deux portions de ruban',f'Deux rubans ont la même longueur initiale. Alice en utilise {m(rf"\frac{{{a}}}{{{den}}}")} et Bilal {m(rf"\frac{{{b}}}{{{2*den}}}")}. On compare les portions, sans mesurer le dessin.',[
        q('Pourquoi est-il nécessaire que les rubans aient la même longueur initiale ?', 'Deux fractions ne comparent les quantités utilisées directement que si leurs unités de référence sont identiques.', 'Une même fraction de deux longueurs différentes peut donner deux portions de longueurs différentes.'),
        q('Écrire la fraction d’Alice au dénominateur de celle de Bilal.', 'Doubler les deux termes conserve la fraction et donne des parts de même taille.', m(rf'\frac{{{a}}}{{{den}}}=\frac{{{2*a}}}{{{2*den}}}')+'.'),
        q('Qui utilise la plus grande portion ? Justifier.', 'À dénominateur commun, comparer les numérateurs ; le plus grand compte davantage de parts identiques.', f'Alice, car {2*a} > {b}.'),
        q('Quelle fraction de la longueur initiale représente l’écart ?', 'Soustraire les fractions écrites au même dénominateur.', m(n(f-g))+'.', m(rf'\frac{{{2*a}-{b}}}{{{2*den}}}='+n(f-g)), f'F({a},{den})-F({b},{2*den}) == F("{f-g}")'),
        q(f'Chaque ruban mesurait {2*den} cm. Calculer les deux longueurs utilisées.', 'Diviser la longueur initiale par le dénominateur puis multiplier par le numérateur pour chaque personne.', f'Alice : {2*a} cm ; Bilal : {b} cm.'),
        q('Une fraction avec un dénominateur plus grand est-elle toujours plus grande ?', 'Un contre-exemple suffit à réfuter « toujours ». Pour un même numérateur positif, un partage en plus de parts donne des parts plus petites.', 'Non : 1/4 est plus petit que 1/2, bien que 4 soit plus grand que 2.')],
        'Ne comparer ni les numérateurs seuls ni les dénominateurs seuls : rendre d’abord les parts comparables.',
        dict(type='fraction',denominator=2*den,numerator=2*a,total=2*den),True)


def fraction_reste(i,l):
    total=24+12*i
    d=3+l
    # Le total est choisi comme multiple des deux dénominateurs pour garder des quantités concrètes entières.
    total=4*d*(3+i)
    premiere=F(1,d)
    reste=total*(1-premiere)
    seconde=reste/4
    return ex('Une fraction du reste',f'La bibliothèque possède {total} livres à ranger. Le matin, on range un livre sur {d}. L’après-midi, on range le quart des livres qui restaient après le matin.',[
        q('Combien de livres sont rangés le matin ?', 'Prendre un d-ième de la quantité initiale en divisant par d.', f'{total//d} livres.'),
        q('Combien de livres restent après le matin ?', 'Soustraire la quantité rangée à la quantité initiale avant d’appliquer la fraction de l’après-midi.', f'{n(reste)} livres.', m(f'{total}-{total//d}={n(reste)}')),
        q('Combien de livres sont rangés l’après-midi ?', 'Le quart concerne le reste calculé, pas le nombre initial de livres.', f'{n(seconde)} livres.', m(f'{n(reste)}\\div4={n(seconde)}')),
        q('Combien de livres sont rangés dans la journée ?', 'Additionner les deux quantités de livres, car elles sont maintenant exprimées dans la même unité.', f'{n(total//d+seconde)} livres.', controle=f'F({total},{d})+F("{reste}")/4 == F("{total//d+seconde}")'),
        q('Combien reste-t-il de livres à ranger en fin de journée ?', 'On peut enlever le total rangé de la réserve initiale, ou enlever l’après-midi du reste du matin.', f'{n(reste-seconde)} livres.'),
        q('Pourquoi additionner directement 1/d et 1/4 donnerait-il ici une mauvaise fraction ?', 'Les deux fractions ne portent pas sur le même ensemble de livres. La seconde doit d’abord être ramenée à la réserve initiale.', f'Le quart porte sur {n(reste)} livres, pas sur {total} ; les références ont changé.')],
        'Lire « du total » et « du reste » : avant d’additionner des fractions dans un problème, vérifier leur unité de référence.',
        dict(type='flow',labels=[f'{total} livres','Après le matin','Quart du reste']),True)


def equations_particulieres(i,l):
    d=3+l+i
    cible=0 if i==6 else 1+l
    x=d*cible
    return ex('Retrouver le nombre partagé',f'Un programme demande un nombre x, le partage en {d} parts égales et affiche {cible}. On cherche le nombre choisi au départ.',[
        q('Écrire l’équation du programme.', 'Le nombre affiché est le quotient du nombre choisi par le nombre de parts.', m(rf'\frac{{x}}{{{d}}}={cible}')+'.'),
        q('Quelle opération permet de retrouver x ?', 'L’opération inverse d’une division par un nombre non nul est une multiplication par ce nombre.', f'Multiplier {cible} par {d}.'),
        q('Résoudre l’équation.', 'Faire la même multiplication sur les deux membres de l’égalité conserve son équilibre.', f'x = {x}.', m(f'x={d}\\times {cible}={x}'), f'F({x},{d}) == {cible}'),
        q('Vérifier la solution dans le programme.', 'Remplacer x par la valeur trouvée et exécuter la division de départ.', m(rf'\frac{{{x}}}{{{d}}}={cible}')+' : le résultat affiché est correct.'),
        q(f'Un autre programme multiplie x par {d} et affiche 0. Quelle est sa solution ?', 'Le coefficient est non nul : seul zéro donne un produit nul en le multipliant par ce coefficient.', 'x = 0.', m(f'{d}\\times0=0')),
        q('Une équation demande-t-elle toujours un nombre strictement positif ?', 'Les solutions dépendent de l’égalité et du contexte. Le nombre zéro est autorisé ici car aucun énoncé ne l’interdit.', 'Non. Le second programme a pour solution zéro ; vérifier le contexte avant de refuser une valeur.')],
        'Diviser x par 3 et multiplier x par 3 sont deux programmes différents. Une division par zéro reste interdite.',
        dict(type='flow',labels=['Nombre x',f'÷ {d}',f'Affiche {cible}']),True)


def prisme(i,l):
    b,h,long=4+2*i,3+l,5+l
    aire=F(b*h,2);volume=aire*long
    return ex('Une boîte en prisme triangulaire',f'Une boîte est un prisme droit de longueur {long} cm. Ses deux bases sont des triangles rectangles dont les côtés perpendiculaires mesurent {b} cm et {h} cm.',[
        q('Combien cette boîte a-t-elle de bases ? Quelle est leur forme ?', 'Un prisme droit possède deux bases parallèles et superposables ; ici il ne s’agit pas de rectangles.', 'Deux bases triangulaires rectangles.'),
        q('Décrire les faces latérales et compter les faces de la boîte.', 'Un rectangle latéral correspond à chaque côté du triangle de base.', 'Trois rectangles latéraux et deux triangles, soit cinq faces.'),
        q('Calculer l’aire d’une base.', 'La base du solide est elle-même un triangle : calculer d’abord son aire en divisant le produit des côtés perpendiculaires par 2.', m(n(aire))+' cm².', m(rf'\frac{{{b}\times {h}}}{{2}}={n(aire)}')),
        q('Calculer le volume du prisme.', 'Multiplier l’aire d’une base par la distance entre les deux bases, qui est la hauteur du solide.', m(n(volume))+' cm³.', m(f'{n(aire)}\\times {long}={n(volume)}'), f'F({b}*{h},2)*{long} == F("{volume}")'),
        q('Convertir ce volume en mL.', 'Un volume de 1 cm³ correspond à une capacité de 1 mL.', m(n(volume))+' mL.'),
        q('Si on double seulement la distance entre les bases, que devient le volume ?', 'Les bases sont inchangées : le produit aire de base × hauteur double seulement par son second facteur.', m(n(2*volume))+' cm³, soit le double.')],
        'La hauteur du triangle sert à calculer l’aire de base ; la hauteur du prisme est la distance entre ses deux bases. Ne pas les confondre.',
        dict(type='prism',base=b,height=h,length=long),True)


def de(i,l):
    faces=6
    seuil=2+i%4
    favorables=6-seuil
    return ex('Un dé équilibré et une affirmation',f'On lance un dé équilibré à six faces numérotées de 1 à 6. L’événement A est « obtenir un nombre strictement supérieur à {seuil} ».',[
        q('Lister toutes les issues possibles.', 'Une issue est ici le numéro inscrit sur la face supérieure ; le dé comporte six résultats distincts.', '1, 2, 3, 4, 5 et 6.'),
        q('Pourquoi les issues sont-elles équiprobables ?', 'Le mot équilibré est l’hypothèse qui donne la même chance à chaque face ; le nombre de faces seul ne suffit pas.', 'Parce que le dé est supposé équilibré ; chaque issue a une probabilité de 1/6.'),
        q('Lister les issues favorables à A.', '« Strictement supérieur » exclut la valeur seuil elle-même.', ', '.join(map(str,range(seuil+1,7)))+'.'),
        q('Calculer la probabilité de A.', 'Compter les issues favorables puis diviser par le nombre d’issues équiprobables.', m(n(F(favorables,6)))+'.', controle=f'F({favorables},6)+F({seuil},6) == 1'),
        q('Décrire l’événement contraire de A et calculer sa probabilité.', 'L’événement contraire rassemble toutes les issues qui ne réalisent pas A, y compris la valeur seuil.', f'Obtenir un nombre inférieur ou égal à {seuil} ; probabilité '+m(n(F(seuil,6)))+'.'),
        q('Un élève affirme qu’après six lancers chaque face sera nécessairement sortie une fois. A-t-il raison ?', 'L’équiprobabilité ne fixe pas l’ordre ni la répartition d’une série courte. Des répétitions et des absences restent possibles.', 'Non. On peut obtenir plusieurs fois le même numéro ; aucune face n’est garantie en six lancers.')],
        'Une probabilité donne une chance pour chaque expérience ; elle ne promet pas un résultat exact sur une courte série.',
        dict(type='table',headers=['Issues',1,2,3,4,5,6],rows=[['Probabilité','1/6','1/6','1/6','1/6','1/6','1/6']]))


def sequence(i,l):
    longueur,largeur=30+5*i,15+5*l
    return ex('Répéter une séquence pour tracer un rectangle',f'Un lutin part du point A vers la droite, stylo baissé. Il répète deux fois : « avancer de {longueur} pas ; tourner à gauche de 90° ; avancer de {largeur} pas ; tourner à gauche de 90° ».',[
        q('Combien d’instructions avancer contient la séquence répétée ?', 'Distinguer le contenu d’un tour de boucle du programme complet.', 'Deux instructions avancer par tour.'),
        q('Combien de segments le programme complet trace-t-il ?', 'Le tour contenant deux déplacements est exécuté deux fois.', 'Quatre segments.', m(r'2\times2=4')),
        q('Donner les longueurs des segments dans l’ordre.', 'Lire la séquence de haut en bas, puis recommencer la même séquence sans revenir au point de départ entre les deux tours.', f'{longueur}, {largeur}, {longueur}, {largeur} pas.'),
        q('Quelle figure est tracée ? Justifier.', 'Les côtés opposés ont les mêmes longueurs et les rotations successives donnent des angles droits.', f'Un rectangle de dimensions {longueur} et {largeur} pas.'),
        q('Calculer la distance parcourue et donner la position finale.', 'Additionner les quatre côtés ; les déplacements opposés se compensent deux à deux.', f'{2*(longueur+largeur)} pas ; le lutin revient au point A.', m(f'2({longueur}+{largeur})={2*(longueur+largeur)}'), f'2*({longueur}+{largeur}) == {2*(longueur+largeur)}'),
        q('Comment modifier un seul paramètre pour obtenir un carré ?', 'Pour un carré, les quatre côtés doivent être égaux. Les rotations de 90° et les deux répétitions conviennent déjà.', f'Remplacer la longueur {largeur} par {longueur} dans le second déplacement, ou inversement pour le premier.')],
        'Une boucle peut répéter une séquence de plusieurs instructions. Suivre l’ordre et la direction entre les déplacements pour prévoir la figure.',
        dict(type='program',lines=['Répéter 2 fois',f'    avancer de {longueur} pas','    tourner à gauche de 90°',f'    avancer de {largeur} pas','    tourner à gauche de 90°']),True)


def choisir(slug,i,l,defaut):
    if slug=='operations' and i%2: return bouteilles(i,l)
    if slug=='divisibilite' and i%3==1: return lots(i,l)
    if slug=='divisibilite' and i%3==2: return periodes(i,l)
    if slug=='fractions' and i%2: return comparaison(i,l)
    if slug=='additions-fractions' and i%3==2: return fraction_reste(i,l)
    if slug=='equations' and i in (4,6): return equations_particulieres(i,l)
    if slug=='espace' and i in (2,6): return prisme(i,l)
    if slug=='probabilites' and i%2: return de(i,l)
    if slug=='programmation' and i in (2,5): return sequence(i,l)
    return defaut(i,l)
