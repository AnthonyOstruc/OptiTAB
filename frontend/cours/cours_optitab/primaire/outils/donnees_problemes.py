"""Problèmes suivis, données et hasard : formulations propres à chaque âge."""
from fractions import Fraction as F
from config import GRADE
from modele_site import ex,m
from nombres import a,c,f,frac,NOMS,OBJETS,lit

def proportionnalite(i,l):
    base=2+i%3;price=base*(2+l);multiple=2+l;more=base+1
    return ex('Le stand de cahiers',f'Au stand, {base} cahiers identiques coûtent {price} €. Chaque cahier a le même prix ; il n’y a ni remise ni frais supplémentaires.',[
        a('Le prix est-il proportionnel au nombre de cahiers ? Justifie.','Je teste si deux fois plus de cahiers coûtent deux fois plus.','Oui : chaque cahier a le même prix. Acheter plusieurs fois la même quantité multiplie le prix de la même façon.'),
        c(f'Combien coûtent {base*2} cahiers ?','Deux fois plus de cahiers coûtent deux fois plus.',f'{price}*2',2*price,'€'),
        c(f'Combien coûtent {base*multiple} cahiers ?','Je multiplie le prix par le même nombre que la quantité.',f'{price}*{multiple}',price*multiple,'€'),
        c('Combien coûte un seul cahier ?','Un seul cahier représente une part du lot de départ.',f'{price}//{base}',price//base,'€'),
        c(f'Combien coûtent {more} cahiers ?','Je réunis le lot de départ et un cahier.',f'{price}+{price//base}',price+price//base,'€'),
        a('Un autre stand facture aussi 3 € de livraison par commande. Le prix total y reste-t-il proportionnel ?','Je compare deux commandes avec le même frais fixe.',f'Non. Une commande de {base} cahiers coûterait {price+3} €, et le double de cahiers coûterait {2*price+3} €, au lieu du double {2*(price+3)} €. Le frais fixe est payé une seule fois.',f'{2*price+3}!=2*{price+3}')],
        'J’explique « fois plus », « fois moins » et les assemblages en phrases avant de calculer.',dict(type='prices',labels=[f'{base} cahiers','1 cahier'],values=[str(price),'?']),True)

def donnees(i,l):
    vs=[4+i+l,7+i*2+l,3+i+l];labels=['À pied','Vélo','Bus'];total=sum(vs)
    return ex('L’enquête sur les trajets', 'Chaque élève interrogé a choisi son moyen principal pour venir à l’école. Une personne ne compte que dans une seule catégorie. Lis le graphique et indique l’unité utilisée.',[
        a('Que représentent les catégories et les hauteurs ?','Je lis les noms sous les barres puis le titre de l’axe vertical.','Les catégories sont les moyens de transport ; les hauteurs comptent les élèves.'),
        c('Combien d’élèves viennent à vélo ?','Je suis la barre Vélo jusqu’à son sommet, puis je lis l’effectif.',str(vs[1]),vs[1],'élèves'),
        a('Quel moyen de transport est le plus fréquent ?','Je compare les hauteurs dans la même unité.',f'Le vélo, avec {vs[1]} élèves.',f'{vs[1]}==max({vs})'),
        c('Combien d’élèves ont été interrogés ?','Je réunis les effectifs de toutes les catégories, sans compter deux fois un élève.', '+'.join(map(str,vs)),total,'élèves'),
        c('Combien d’élèves de plus viennent à vélo qu’en bus ?','Je cherche l’écart entre les deux effectifs.',f'{vs[1]}-{vs[2]}',vs[1]-vs[2],'élèves'),
        c('Deux élèves du bus choisissent maintenant de venir à pied. Quel est le nouvel effectif à pied ? Le total change-t-il ?','Je déplace deux personnes d’une catégorie à l’autre sans ajouter de personnes.',f'{vs[0]}+2',vs[0]+2,'élèves à pied ; le total reste '+str(total)+'.')],
        'Je lis le titre, les catégories et l’échelle avant de calculer avec les données.',dict(type='bars',labels=labels,values=vs),True)

def hasard(i,l):
    red=2+i%4;blue=red+1+l;green=1;total=red+blue+green;numeric=GRADE=='cm2'
    return ex('Le sac de jetons',f'Un sac contient {red} jetons rouges, {blue} bleus et {green} vert. Les jetons ont la même taille et sont bien mélangés. On en prend un sans regarder.',[
        c('Combien de jetons contient le sac ?','Je réunis les trois couleurs pour connaître toutes les possibilités.',f'{red}+{blue}+{green}',total,'jetons'),
        a('Peut-on savoir à l’avance la couleur qui sortira ?','Je distingue un résultat possible d’un résultat certain.','Non. Plusieurs couleurs sont possibles : le tirage est une expérience aléatoire.'),
        a('Peut-on tirer un jeton jaune ?','Je regarde si cette couleur existe dans le sac.','Non : c’est impossible, aucun jeton n’est jaune.'),
        a('Quelle couleur a le plus de chances de sortir ? Justifie.','Chaque jeton a la même chance ; une couleur plus nombreuse a davantage de possibilités.',f'Le bleu : il y a {blue} jetons bleus, plus que de rouges ou de verts.',f'{blue}>{red} and {blue}>{green}'),
        a('Indique les chances de tirer rouge sous la forme « a chances sur b ».' if numeric else 'Est-il certain de tirer un jeton rouge ?','Je compte les jetons favorables parmi tous les jetons.' if numeric else 'Pour être certain, tous les jetons devraient être rouges.',f'{red} chances sur {total}.' if numeric else 'Non. Des jetons bleus et verts peuvent aussi sortir.'),
        a('Un jeton rouge a été tiré, puis REMIS dans le sac. Les chances ont-elles changé au tirage suivant ?','Après remise et mélange, le sac possède de nouveau exactement la même composition.','Non : les chances sont les mêmes, car aucun jeton n’a été retiré du sac.')],
        'Possible ne veut pas dire certain. Après remise, la composition du sac reste identique.',dict(type='tokens',counts=[red,blue,green]),True)

def parties_tout(i,l,compare=False,mixed=False):
    small=GRADE=='ce1';base=36+i*7+l*18 if small else 136+i*17+l*107;delta=12+i*3;give=7+i
    second=base+delta;total=base+second
    intro=f'{NOMS[i]} possède {base} cartes. Son ami en possède {delta} de plus.'
    return ex('Deux collections réunies',intro,[
        a('Qui possède le plus de cartes ?','« De plus » compare les deux collections en ajoutant un écart.','L’ami possède plus de cartes.'),
        c('Combien de cartes possède l’ami ?','Je pars de la collection connue et j’ajoute l’écart.',f'{base}+{delta}',second,'cartes'),
        c('Combien de cartes ont-ils ensemble ?','Je réunis les deux collections ; je compte bien la collection entière de chacun.',f'{base}+{second}',total,'cartes'),
        c(f'Ils donnent ensemble {give} cartes. Combien leur en reste-t-il en tout ?','Je retire le don du total, une seule fois.',f'{total}-{give}',total-give,'cartes'),
        c('Combien de cartes faut-il rendre à l’ami pour qu’il possède sa collection de départ si on lui a pris tout le don ?','Je retrouve sa quantité en ajoutant les cartes données à ce qui lui reste.',f'{second-give}+{give}',second,'cartes'),
        a(f'Un élève calcule seulement {base} + {delta} pour trouver le total des deux collections. A-t-il raison ?','Je précise ce que représente le résultat de son calcul.',f'Non. {base} + {delta} = {second} est seulement la collection de l’ami. Pour le total, il faut encore ajouter les {base} cartes de {NOMS[i]}.')],
        'Je donne un nom à chaque résultat intermédiaire : une collection, un écart ou un total.',dict(type='comparison',a=base,difference=delta),True)

def choix(i,l):
    colors=2+i%2;shapes=2+l;decor=2
    return ex('Inventer tous les badges',f'Pour créer un badge, on choisit une couleur parmi {colors}, une forme parmi {shapes}, puis un décor parmi {decor}. On utilise exactement un choix de chaque sorte.',[
        c('Pour une couleur fixée, combien de formes peut-on choisir ?','Je laisse varier seulement la forme.',str(shapes),shapes,'formes'),
        c('Combien de couples couleur-forme existe-t-il ?','Pour chaque couleur, les mêmes formes sont possibles.',f'{colors}*{shapes}',colors*shapes,'couples'),
        c('Pour un couple fixé, combien de décors peut-on ajouter ?','Je garde la couleur et la forme et je fais varier le décor.',str(decor),decor,'décors'),
        c('Combien de badges différents peut-on fabriquer ?','Chaque couple couleur-forme se décline avec les deux décors.',f'{colors*shapes}*{decor}',colors*shapes*decor,'badges'),
        c('Si une couleur est supprimée, combien de badges différents reste-t-il ?','Je refais le compte avec une couleur de moins.',f'({colors}-1)*{shapes}*{decor}',(colors-1)*shapes*decor,'badges'),
        a('Comment vérifier que tu n’as oublié aucun badge ?','J’organise la recherche dans un ordre régulier.','Choisir une première couleur, lister toutes les formes et les deux décors pour chacune, puis recommencer pour les autres couleurs. Un arbre de choix évite les oublis et les doublons.')],
        'Je fixe un choix, je liste les suivants dans un ordre régulier, puis je recommence.',dict(type='choices',colors=colors,shapes=shapes),True)

def monnaie(i,l):
    cents=205+i*25+l*31;other=125+i*10;budget=1000 if cents+other>500 else 500
    def prix(v):return f'{v//100},{v%100:02} €'
    return ex('Au petit magasin',f'Un carnet coûte {prix(cents)} et une gomme {prix(other)}. {NOMS[i]} donne {budget//100} € pour acheter un carnet et une gomme.',[
        a('Lis le prix du carnet en euros et centimes.','Les deux rangs à droite de la virgule indiquent les centimes.',f'{cents//100} euros et {cents%100} centimes.'),
        c('Combien de centimes coûte le carnet ?','Chaque euro vaut 100 centimes.',f'{cents//100}*100+{cents%100}',cents,'centimes'),
        c('Combien de centimes coûtent les deux objets ensemble ?','Je réunis les deux prix dans une même unité.',f'{cents}+{other}',cents+other,'centimes'),
        a('Écris le total avec une virgule et le symbole €.','Je regroupe 100 centimes en 1 euro et je garde deux chiffres pour les centimes.',prix(cents+other)+'.'),
        c('Combien de centimes doit-on rendre ?','Je complète le prix jusqu’à la somme donnée ou je soustrais les deux montants.',f'{budget}-{cents+other}',budget-cents-other,'centimes'),
        a('Exprime cette monnaie en euros et centimes, puis vérifie le paiement.','Achats et monnaie doivent reconstituer exactement la somme donnée.',f'{prix(budget-cents-other)}. Vérification : {cents+other} + {budget-cents-other} = {budget} centimes.',f'{cents+other}+{budget-cents-other}=={budget}')],
        'La virgule des prix sépare euros et parties d’euro : 2,05 € signifie 2 € et 5 centimes.',dict(type='prices',labels=['Carnet','Gomme'],values=[prix(cents),prix(other)]),True)

def fraction_unite(i,l):
    d=4 if l==0 else 3 if l==1 else 6;unit=d*2;whole=1+i%3;parts=d-1;length=whole*unit+parts*2
    return ex('Mesurer avec une unité choisie',f'Une bande de référence, appelée unité u, mesure {unit} cm. On la partage en {d} parts égales. On veut tracer une longueur de {whole} u et {parts}/{d} u.',[
        c('Combien de centimètres mesure une petite part de l’unité ?','Je partage la longueur de référence en parts égales.',f'{unit}//{d}',2,'cm'),
        c('Combien de centimètres représentent les unités entières ?','Chaque unité entière a la même longueur de référence.',f'{whole}*{unit}',whole*unit,'cm'),
        c('Combien de centimètres représentent les parts supplémentaires ?','Je compte autant de petites parts que le numérateur.',f'{parts}*2',parts*2,'cm'),
        c('Quelle longueur totale faut-il tracer ?','Je réunis les unités entières et les parts supplémentaires.',f'{whole*unit}+{parts*2}',length,'cm'),
        a('Comment vérifier ton tracé sans recommencer toute la mesure ?','Je reporte d’abord la bande unité puis ses parts égales.',f'On doit pouvoir reporter {whole} fois u puis {parts} petites parts sur le segment.'),
        c('Combien manque-t-il de centimètres pour atteindre l’unité entière suivante ?','Il reste une petite part avant de compléter une unité.',f'{(whole+1)*unit}-{length}',2,'cm')],
        'Une fraction de longueur dépend de l’unité choisie ; je fixe cette unité avant de mesurer.',dict(type='unitlength',denominator=d,whole=whole,parts=parts),True)

def rangs(i,l):
    rank=12+i*7+l*10;step=2+l
    return ex('Une file et une suite',f'{NOMS[i]} occupe la {rank}e place dans une file. Pour une activité, les élèves récitent ensuite une suite qui commence à {rank} et avance de {step} en {step}.',[
        c(f'Combien de personnes sont devant {NOMS[i]} ?','Le rang compte aussi la personne elle-même.',f'{rank}-1',rank-1,'personnes'),
        c('Quel rang occupe la personne juste après ?','La place suivante augmente le rang d’une unité.',f'{rank}+1',rank+1),
        c('Quel est le deuxième nombre de la suite ?','J’ajoute une fois le pas annoncé.',f'{rank}+{step}',rank+step),
        c('Quel est le troisième nombre de la suite ?','Je repars du deuxième nombre et j’ajoute le même pas.',f'{rank+step}+{step}',rank+2*step),
        c('Quel est le quatrième nombre de la suite ?','L’écart entre deux termes voisins reste le même.',f'{rank+2*step}+{step}',rank+3*step),
        a('Comment distinguer le rang d’un élève et le nombre de personnes devant lui ?','Je vérifie qui est compté par chaque expression.',f'Le rang est {rank}, mais il y a {rank-1} personnes devant : on ne compte pas {NOMS[i]} parmi celles qui sont devant.')],
        'Un rang donne une position. Dans une suite régulière, je repère le pas avant de continuer.',dict(type='numberline',start=rank,step=step),True)
