"""Scénarios communs au collège, adaptés au périmètre de Sixième."""

from fractions import Fraction as F

from modele_6e import ex,q,n,m



def operations(i, niveau):
    a, b, groupes = 3+i, 2+niveau, 4+niveau
    prix = F(25+5*i+3*niveau, 10)
    budget = groupes*(a+b)*prix + 20 + i
    total = groupes*(a+b)*prix
    return ex(['Les fournitures des ateliers', 'Une commande de carnets', 'Le budget du club'][i%3],
        f'Un club prépare {groupes} ateliers. Chaque atelier reçoit {a} carnets bleus et {b} carnets verts. Chaque carnet coûte {m(n(prix))} €. Le club dispose de {m(n(budget))} €. Les frais de livraison pour toute la commande sont de 6 €.', [
        q('Combien de carnets faut-il pour un atelier ?', 'Les deux couleurs se complètent : on additionne leurs effectifs.', f'{a+b} carnets.', m(f'{a}+{b}={a+b}'), f'{a}+{b} == {a+b}'),
        q('Combien de carnets faut-il pour tous les ateliers ?', 'Chaque atelier reçoit le même nombre : on multiplie le nombre d’ateliers par les besoins d’un atelier.', f'{groupes*(a+b)} carnets.', m(f'{groupes}\\times({a}+{b})={groupes*(a+b)}')),
        q('Écrire une seule expression pour le prix des carnets, puis la calculer.', 'Les parenthèses regroupent les carnets d’un atelier ; le prix unitaire multiplie le nombre total.', m(n(total))+' €.', m(f'{groupes}\\times({a}+{b})\\times {n(prix)}={n(total)}'), f'{groupes}*({a}+{b})*F("{prix}") == F("{total}")'),
        q('Calculer le coût de la commande, livraison comprise.', 'Les frais concernent toute la commande ; on les ajoute une seule fois après le prix des carnets.', m(n(total+6))+' €.', m(f'{n(total)}+6={n(total+6)}')),
        q('Quelle somme restera-t-il au club ?', 'On soustrait la dépense totale au budget disponible et on vérifie que le reste est positif.', m(n(budget-total-6))+' €.', m(f'{n(budget)}-({n(total)}+6)={n(budget-total-6)}')),
        q('Un élève multiplie aussi les 6 € de livraison par le nombre d’ateliers. De combien surestime-t-il la dépense ?', 'Comparer la livraison facturée une fois à la livraison comptée une fois par atelier : seules les copies supplémentaires sont en trop.', f'{6*(groupes-1)} € de trop.', m(f'6\\times {groupes}-6={6*(groupes-1)}'), f'6*{groupes}-6 == {6*(groupes-1)}')],
        'Lire « pour chaque » et « pour toute la commande » avant de poser un calcul ; une parenthèse indique une quantité regroupée.',
        dict(type='table', headers=['Pour un atelier', 'Carnets bleus', 'Carnets verts'], rows=[['Quantités', a, b], ['Prix par carnet', n(prix)+' €', n(prix)+' €']]))

def divisibilite(i, niveau):
    capacite = 4+i
    quotient = 5+2*niveau+i
    reste = 1+i%3
    total = capacite*quotient+reste
    return ex(['Des places pour une sortie', 'Ranger la collection', 'Préparer les colis'][i%3],
        f'Une association doit ranger {total} objets dans des boîtes qui contiennent chacune au maximum {capacite} objets. Les objets ne peuvent pas être découpés.', [
        q(f'Encadrer {total} par deux multiples consécutifs de {capacite}.', 'Chercher deux produits consécutifs entre lesquels se trouve le nombre d’objets.', m(f'{capacite*quotient}\\le {total}<{capacite*(quotient+1)}'), m(f'{capacite}\\times {quotient}={capacite*quotient} \\ ;\\ {capacite}\\times {quotient+1}={capacite*(quotient+1)}')),
        q('Effectuer la division euclidienne : donner quotient et reste.', 'Le quotient compte les boîtes pleines ; le reste compte les objets qui ne remplissent pas une boîte.', f'Quotient {quotient} ; reste {reste}.', m(f'{total}={capacite}\\times {quotient}+{reste}'), f'divmod({total},{capacite}) == ({quotient},{reste})'),
        q('Vérifier que le reste est autorisé.', 'Dans une division euclidienne, le reste est positif ou nul et strictement inférieur au diviseur.', m(f'0\\le {reste}<{capacite}')+' : le reste convient.'),
        q('Combien de boîtes faut-il pour ranger tous les objets ?', 'Le reste est non nul : une boîte supplémentaire est nécessaire pour les derniers objets.', f'{quotient+1} boîtes.', m(f'{quotient}+1={quotient+1}')),
        q('Combien de places resteront vides dans la dernière boîte ?', 'La dernière boîte reçoit le reste ; on soustrait ce reste à sa capacité.', f'{capacite-reste} places.', m(f'{capacite}-{reste}={capacite-reste}'), f'{capacite}*({quotient}+1)-{total} == {capacite-reste}'),
        q(f'{capacite} est-il un diviseur de {total} ? Quel nombre minimal d’objets faudrait-il ajouter pour obtenir des boîtes toutes pleines ?', 'Un diviseur donne un reste nul. Compléter la dernière boîte supprime le reste.', f'Non ; il faut ajouter {capacite-reste} objets pour obtenir {capacite*(quotient+1)} objets.')],
        'Le quotient entier, le reste et le nombre de boîtes nécessaires sont trois informations différentes. Toujours interpréter le résultat.',
        dict(type='boxes', total=total, capacity=capacite, quotient=quotient, remainder=reste))

def fractions(i, niveau):
    d = [4,5,6,8,10,12,20][i]
    a = 1+niveau
    quantite = d*(4+i+niveau)
    part = F(a,d)
    return ex(['La réserve de jus', 'Les rubans de l’atelier', 'Une collection à partager'][i%3],
        f'Un atelier possède {quantite} L de jus. Il en réserve {m(rf"\frac{{{a}}}{{{d}}}")} pour le matin. Toutes les fractions de cet exercice concernent cette réserve initiale, sauf indication contraire.', [
        q('Que représentent le numérateur et le dénominateur de la fraction réservée ?', 'Le dénominateur donne le nombre de parts égales de l’unité ; le numérateur indique combien de ces parts sont prises.', f'{d} parts égales, dont {a} sont réservées.'),
        q('Écrire une fraction égale en doublant numérateur et dénominateur.', 'Multiplier les deux termes d’une fraction par un même nombre non nul conserve le quotient.', m(rf'\frac{{{2*a}}}{{{2*d}}}='+n(part)), controle=f'F({2*a},{2*d}) == F({a},{d})'),
        q('Quelle quantité représente une seule part ?', 'Partager d’abord la quantité initiale par le dénominateur.', f'{quantite//d} L.', m(f'{quantite}\\div {d}={quantite//d}')),
        q('Quelle quantité est réservée pour le matin ?', 'Multiplier la valeur d’une part par le numérateur. C’est prendre une fraction d’une quantité.', f'{quantite*a//d} L.', m(f'{quantite}\\div {d}\\times {a}={quantite*a//d}'), f'F({a},{d})*{quantite} == {quantite*a//d}'),
        q('Quelle fraction de la réserve initiale reste-t-il ?', 'Une unité entière vaut dénominateur sur lui-même ; on enlève les parts réservées.', m(n(1-part))+'.', m(rf'\frac{{{d}}}{{{d}}}-\frac{{{a}}}{{{d}}}=\frac{{{d-a}}}{{{d}}}')),
        q('La quantité réservée dépasse-t-elle la moitié ? Justifier sans approximation.', 'Mettre la fraction et un demi au même dénominateur, ou comparer le double du numérateur au dénominateur.', ('Oui' if 2*a>d else 'Non')+f' : le double du numérateur vaut {2*a}, '+('supérieur à' if 2*a>d else 'inférieur ou égal à')+f' {d}.')],
        'Une fraction se réfère toujours à une unité précise. Pour calculer une part, diviser par le dénominateur puis multiplier par le numérateur.',
        dict(type='fraction', denominator=d, numerator=a, total=quantite), True)

def additions_fractions(i, niveau):
    d = [6,8,10,12,14,16,18][i]
    a, b = 1+niveau, 1
    matin, apres = F(a,d), F(b,d//2)
    total = matin+apres
    quantite = d*10
    return ex(['Le réservoir du jardin', 'L’eau des serres', 'Le suivi de l’arrosage'][i%3],
        f'Un réservoir contient {quantite} L. On utilise {m(rf"\frac{{{a}}}{{{d}}}")} du volume initial le matin et {m(rf"\frac{{{b}}}{{{d//2}}}")} du volume initial l’après-midi. On ne remplit pas le réservoir entre les deux.', [
        q('Pourquoi peut-on additionner les deux fractions ?', 'On additionne des parts comparables parce que les deux fractions portent explicitement sur le même volume initial.', 'Les deux fractions ont la même unité de référence : le réservoir initial.'),
        q('Écrire la fraction de l’après-midi avec le même dénominateur que celle du matin.', 'Multiplier le numérateur et le dénominateur par 2 pour obtenir des parts de même taille.', m(rf'\frac{{1}}{{{d//2}}}=\frac{{2}}{{{d}}}'), controle=f'F(1,{d//2}) == F(2,{d})'),
        q('Quelle fraction du volume initial a été utilisée en tout ?', 'Additionner les nombres de parts en conservant leur taille : le dénominateur reste inchangé.', m(n(total))+'.', m(rf'\frac{{{a}}}{{{d}}}+\frac{{2}}{{{d}}}=\frac{{{a+2}}}{{{d}}}='+n(total)), f'F({a},{d})+F(1,{d//2}) == F("{total}")'),
        q('Quelle fraction du volume initial reste-t-il ?', 'Écrire le réservoir entier sous la forme d/d puis soustraire la fraction utilisée.', m(n(1-total))+'.', m(rf'1-\frac{{{a+2}}}{{{d}}}=\frac{{{d-a-2}}}{{{d}}}')),
        q('Calculer le nombre de litres utilisés et le nombre de litres restants.', 'Appliquer chaque fraction au volume initial. Leur somme doit redonner la capacité initiale.', f'{n(total*quantite)} L utilisés ; {n((1-total)*quantite)} L restants.', m(f'{quantite}\\times {n(total)}={n(total*quantite)}')),
        q('L’après-midi a-t-on utilisé plus d’eau que le matin ? Donner l’écart en litres.', 'Les fractions sont au même dénominateur : comparer les numérateurs, puis calculer la différence entre les volumes.', ('Plus' if apres>matin else 'Autant' if apres==matin else 'Moins')+f' d’eau l’après-midi ; écart de {n(abs(apres-matin)*quantite)} L.', controle=f'F("{total*quantite}")+F("{(1-total)*quantite}") == {quantite}')],
        'On n’additionne pas les dénominateurs. Si la seconde fraction concernait seulement le reste, il faudrait changer le modèle.',
        dict(type='fraction', denominator=d, numerator=a+2, total=quantite), True)

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
        'En 6e, on lit une donnée saisie pour calculer une formule. Prévoir la sortie avant d’exécuter et contrôler l’imbrication des blocs.',
        dict(type='program',lines=['Quand le drapeau est cliqué','Demander un nombre',f'Dire ({facteur} × réponse + {ajout})']),True)

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
