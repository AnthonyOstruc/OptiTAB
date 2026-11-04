"""Situations de Sixième : pourcentages, régularités et mesures."""
from fractions import Fraction as F
from modele_6e import ex,q,n,m


def pourcentages(i,l):
    total=100+100*l+20*i
    # Un multiple de 20 rend les pourcentages usuels exacts en nombres d'élèves.
    taux=[10,25,50,20,75,5,100][i]
    total=20*(5+l+i)
    part=F(total*taux,100)
    return ex('Une enquête à traduire en pourcentages',f'Une enquête porte sur {total} élèves. Parmi eux, {taux} % choisissent un atelier de dessin ; les autres choisissent un autre atelier. Chaque élève choisit exactement un atelier.',[
        q('Que représentent 100 % dans cette enquête ?', 'Le tout de référence est l’ensemble des élèves interrogés ; un pourcentage exprime des parts de ce tout.', f'Les {total} élèves interrogés.'),
        q('Écrire le pourcentage sous forme de fraction de dénominateur 100.', 'Le mot pour cent signifie pour cent parts égales.', m(rf'\frac{{{taux}}}{{100}}')+'.'),
        q('Donner aussi son écriture décimale.', 'Un centième vaut 0,01 ; écrire la fraction décimale avec une virgule.', m(n(F(taux,100)))+'.'),
        q('Combien d’élèves choisissent le dessin ?', 'Calculer une part sur cent puis prendre autant de parts que le taux. Pour 50 %, on peut aussi prendre la moitié ; pour 25 %, le quart.', f'{n(part)} élèves.', m(f'{total}\\div100\\times {taux}={n(part)}'), f'F({total}*{taux},100) == F("{part}")'),
        q('Quel pourcentage et combien d’élèves choisissent un autre atelier ?', 'Enlever du tout la part déjà comptée, en pourcentage puis en effectif.', f'{100-taux} %, soit {n(total-part)} élèves.'),
        q('Une seconde enquête porte sur deux fois plus d’élèves avec le même pourcentage. Combien choisissent le dessin ?', 'Le pourcentage reste identique mais le tout double ; la quantité correspondante double elle aussi.', f'{n(2*part)} élèves. Le même pourcentage ne signifie donc pas le même effectif.')],
        'Nommer le tout de référence avant tout calcul. Pourcentage, écriture décimale et fraction peuvent représenter le même nombre.',
        dict(type='percent',rate=taux,total=total),True)


def prealgebre(i,l):
    if i%2:
        premier=4+l
        ajout=2+i%3
        rang=4+i+l
        final=premier+(rang-1)*ajout
        return ex('Poursuivre une frise de perles',f'Une frise utilise {premier} perles au rang 1. Pour passer au rang suivant, on ajoute toujours {ajout} perles, sans en enlever.',[
            q('Combien de perles utilise le rang 2 ?', 'Un passage au rang suivant ajoute une fois la quantité donnée.', f'{premier+ajout} perles.'),
            q('Combien de perles utilisent les rangs 3 et 4 ?', 'Continuer les ajouts réguliers et conserver le rang de chaque résultat.', f'Rang 3 : {premier+2*ajout} ; rang 4 : {premier+3*ajout}.'),
            q(f'Combien de passages faut-il du rang 1 au rang {rang} ?', 'Compter les intervalles entre les rangs, et non le nombre de rangs : du rang 1 au rang 2, il n’y a qu’un passage.', f'{rang-1} passages.'),
            q(f'Calculer le nombre de perles du rang {rang}.', 'Ajouter au premier rang autant d’ajouts qu’il y a de passages. Un produit remplace les additions répétées.', f'{final} perles.', m(f'{premier}+{rang-1}\\times {ajout}={final}'), f'{premier}+({rang}-1)*{ajout} == {final}'),
            q(f'Un rang utilise {final+2*ajout} perles. Quel est son numéro ?', 'Retirer les perles du premier rang, diviser par l’ajout pour trouver le nombre de passages, puis ajouter 1 pour le numéro du rang.', f'Le rang {rang+2}.'),
            q('Pourquoi multiplier directement le numéro du rang par l’ajout ne suffit-il pas toujours ?', 'Il faut tenir compte de la construction du premier rang et compter les passages à partir de ce rang.', f'Au rang 1 il y a {premier} perles ; on part de cette réserve puis on ajoute {ajout} par passage.')],
            'Un motif évolutif peut se décrire avec des mots, un tableau et des opérations ; aucune lettre inconnue n’est nécessaire ici.',
            dict(type='table',headers=['Rang',1,2,3,4],rows=[['Perles',premier,premier+ajout,premier+2*ajout,premier+3*ajout]]),True)
    boites=3+l
    parboite=5+i
    isoles=4+l+i
    total=boites*parboite+isoles
    return ex('Retrouver le contenu de boîtes identiques',f'On compte {total} crayons : {boites} boîtes identiques et {isoles} crayons isolés. Les boîtes contiennent toutes le même nombre de crayons. On cherche leur contenu sans les ouvrir.',[
        q('Quelles quantités sont connues ? Quelle quantité cherche-t-on ?', 'Séparer les données du nombre inconnu avant de choisir une opération.', f'On connaît {total} crayons, {boites} boîtes et {isoles} crayons isolés ; on cherche les crayons d’une boîte.'),
        q('Combien de crayons sont rangés dans les boîtes ?', 'Enlever les crayons isolés du total pour conserver seulement la partie répartie entre les boîtes.', f'{boites*parboite} crayons.', m(f'{total}-{isoles}={boites*parboite}')),
        q('Combien de crayons contient une boîte ?', 'Les boîtes sont identiques : partager également le nombre de crayons rangés entre les boîtes.', f'{parboite} crayons.', m(f'{boites*parboite}\\div {boites}={parboite}'), f'F({total}-{isoles},{boites}) == {parboite}'),
        q('Compléter puis vérifier le calcul à trou : nombre de boîtes × □ + crayons isolés = total.', 'Remplacer la case par le résultat trouvé et refaire le calcul dans l’ordre de départ.', m(f'{boites}\\times {parboite}+{isoles}={total}')+'.'),
        q('Combien y aurait-il de crayons avec une boîte identique de plus ?', 'Le contenu d’une boîte ne change pas ; ajouter ce contenu au total initial.', f'{total+parboite} crayons.'),
        q('Un élève divise le total directement par le nombre de boîtes. Pourquoi sa méthode ne convient-elle pas ?', 'Les crayons isolés ne sont dans aucune boîte ; ils ne doivent pas être répartis dans le calcul du contenu d’une boîte.', 'Il faut d’abord retirer les crayons isolés, puis diviser le reste entre les boîtes.')],
        'Un schéma en barres aide à isoler la partie inconnue ; défaire les opérations dans l’ordre inverse.',
        dict(type='flow',labels=[f'{boites} boîtes identiques',f'+ {isoles} crayons',f'{total} crayons']),True)


def proportionnalite(i,l):
    from scenarios_communs import proportionnalite as recette
    if i%2==0:return recette(i,l)
    echelle=100+100*l
    plan=3+i
    reel=plan*echelle
    return ex('Passer du plan à la réalité',f'Un jardin est dessiné à l’échelle 1/{echelle}. Sur le plan, la longueur d’une allée est {plan} cm et la largeur d’un massif est 2 cm.',[
        q('Que représente 1 cm sur ce plan ?', 'L’échelle indique que toutes les longueurs du plan sont multipliées par le même nombre pour retrouver les longueurs réelles.', f'{echelle} cm dans la réalité, soit {echelle//100} m.'),
        q('Calculer la longueur réelle de l’allée en centimètres.', 'Multiplier la longueur mesurée sur le plan par le coefficient commun.', f'{reel} cm.', m(f'{plan}\\times {echelle}={reel}')),
        q('Convertir cette longueur réelle en mètres.', 'Cent centimètres forment un mètre ; diviser le nombre de centimètres par 100.', m(n(F(reel,100)))+' m.', controle=f'F({plan}*{echelle},100) == F("{F(reel,100)}")'),
        q('Calculer la largeur réelle du massif en mètres.', 'Appliquer le même coefficient à une autre longueur du plan puis convertir dans l’unité demandée.', f'{2*echelle//100} m.'),
        q(f'Une clôture mesure {5*echelle//100} m dans la réalité. Quelle longueur doit-elle avoir sur le plan ?', 'Revenir d’abord aux centimètres puis partager par le coefficient d’agrandissement ; on effectue le passage inverse.', '5 cm.'),
        q('Si on photocopie ce plan en doublant toutes ses longueurs, que représente désormais 1 cm de la copie ?', 'Une longueur du dessin double pour une même longueur réelle : chaque centimètre de la copie représente deux fois moins.', f'{echelle//2} cm dans la réalité. L’échelle de la copie est 1/{echelle//2}.')],
        'Les deux longueurs d’une échelle doivent être exprimées dans la même unité. Utiliser le passage à l’unité ou un coefficient, sans produit en croix.',
        dict(type='table',headers=['Longueur','Plan (cm)','Réalité (cm)'],rows=[['Unité',1,echelle],['Allée',plan,'?'],['Massif',2,'?']]),True)


def longueurs(i,l):
    if i%3==2:
        rayon=2+i+l
        diam=2*rayon
        per=F(314,100)*diam
        return ex('Faire le tour d’un bassin rond',f'Un bassin circulaire a un rayon de {rayon} m. On utilise π ≈ 3,14 pour estimer la longueur de sa bordure.',[
            q('Décrire le rayon du cercle.', 'Un rayon relie le centre à un point du cercle ; tous les rayons ont la même longueur.', f'Un segment du centre au bord du bassin ; longueur {rayon} m.'),
            q('Calculer le diamètre.', 'Un diamètre passe par le centre et relie deux points du cercle ; il mesure deux rayons.', f'{diam} m.'),
            q('Écrire le périmètre du cercle avec π.', 'Le tour du cercle est π fois le diamètre ; ne pas utiliser une formule d’aire.', m(f'{diam}\\pi')+' m.'),
            q('Calculer une valeur approchée du périmètre.', 'Remplacer π par 3,14 seulement pour l’approximation.', m(n(per))+' m environ.', m(f'{diam}\\times3{{,}}14={n(per)}'), f'{diam}*F(314,100) == F("{per}")'),
            q('Exprimer cette approximation en centimètres.', 'Un mètre vaut cent centimètres : multiplier la valeur en mètres par 100.', f'{int(per*100)} cm environ.'),
            q('Si le diamètre double, que devient le périmètre ?', 'Le même nombre π multiplie le diamètre ; doubler ce diamètre double donc le produit.', 'Il double : '+m(n(2*per))+' m environ.')],
            'Pour le contour d’un disque, utiliser π × diamètre. Le résultat est une longueur, exprimée dans une unité simple.',
            dict(type='circle_measure',radius=rayon),True)
    longueur=5+i+l
    largeur=2+l
    tour=2*(longueur+largeur)
    return ex('Clôturer un potager',f'Un potager rectangulaire mesure {longueur} m de long et {largeur} m de large. On veut entourer son contour avec un grillage ; une ouverture de 1 m doit rester libre.',[
        q('Convertir les deux dimensions en centimètres.', 'Multiplier les mètres par 100 ; les deux dimensions doivent être dans la même unité.', f'{100*longueur} cm et {100*largeur} cm.'),
        q('Nommer la grandeur nécessaire pour connaître la longueur du contour.', 'Le contour est une longueur totale : on cherche le périmètre, et non la surface occupée.', 'Le périmètre du rectangle.'),
        q('Calculer le périmètre complet.', 'Les côtés opposés sont égaux : additionner longueur et largeur, puis doubler.', f'{tour} m.', m(f'2\\times({longueur}+{largeur})={tour}'), f'2*({longueur}+{largeur}) == {tour}'),
        q('Quelle longueur de grillage faut-il avec l’ouverture ?', 'Retirer du contour la partie laissée libre.', f'{tour-1} m.'),
        q('Le grillage est vendu en rouleaux de 5 m. Combien de rouleaux faut-il acheter ?', 'Chercher le plus petit nombre entier de rouleaux couvrant la longueur nécessaire ; un rouleau partiel compte pour un achat entier.', f'{(tour-1+4)//5} rouleaux.'),
        q('Quelle longueur de grillage restera-t-il ?', 'Calculer la longueur achetée puis soustraire la longueur utilisée, sans retirer à nouveau l’ouverture.', f'{5*((tour-1+4)//5)-(tour-1)} m.')],
        'Un périmètre se calcule en additionnant des longueurs. Distinguer la quantité à utiliser de la quantité à acheter.',
        dict(type='rectangle_measure',length=longueur,width=largeur),True)


def aires(i,l):
    longueur,largeur=4+i,2+l
    aire=longueur*largeur
    return ex('Recouvrir une affiche',f'Une affiche rectangulaire mesure {longueur} dm de longueur et {largeur} dm de largeur. On la recouvre avec des carrés de 1 dm de côté, sans chevauchement et sans trou.',[
        q('Combien de carrés de 1 dm de côté place-t-on dans une rangée ?', 'Une rangée suit la longueur ; chaque carré occupe 1 dm de cette longueur.', f'{longueur} carrés.'),
        q('Combien de rangées faut-il ? Combien de carrés en tout ?', 'La largeur donne le nombre de rangées ; multiplier rangées et carrés par rangée.', f'{largeur} rangées, soit {aire} carrés.'),
        q('Donner l’aire de l’affiche en dm².', 'Un carré de 1 dm de côté a une aire de 1 dm² ; l’aire totale est le nombre de ces carrés.', f'{aire} dm².', m(f'{longueur}\\times{largeur}={aire}'), f'{longueur}*{largeur} == {aire}'),
        q('Convertir cette aire en cm².', 'Chaque carré de 1 dm de côté contient 10 × 10 carrés de 1 cm de côté : le facteur est 100.', f'{100*aire} cm².'),
        q('Convertir la même aire en m².', 'Un m² contient 100 dm² ; on partage donc par 100.', m(n(F(aire,100)))+' m².'),
        q('Si on double la longueur en gardant la largeur, que deviennent l’aire et le périmètre ?', 'Deux affiches se placent côte à côte : l’aire double. Pour le contour, les deux largeurs ne doublent pas : recalculer la somme des côtés.', f'Aire : {2*aire} dm². Périmètre : {2*(2*longueur+largeur)} dm ; il n’est pas doublé.')],
        'Une conversion d’aire utilise des facteurs 100 entre m², dm² et cm². Ne pas appliquer le facteur 10 des longueurs.',
        dict(type='area_grid',length=longueur,width=largeur),True)


def durees(i,l):
    depart_h=23 if l==2 and i>=4 else 8+i
    depart_m=35+5*l
    trajet=50+10*i+15*l
    arrivee=depart_h*60+depart_m+trajet
    pause=20+l*5
    def horaire(t):
        return f'{(t//60)%24} h {t%60:02d}'+(' le lendemain' if t>=1440 else '')
    return ex('Organiser le trajet d’une sortie',f'Un autocar part à {depart_h} h {depart_m:02d}. Le trajet dure {trajet} minutes. À l’arrivée, le groupe fait une pause de {pause} minutes avant la visite.',[
        q('Convertir la durée du trajet en heures et minutes.', 'Partager par 60 : le quotient compte les heures complètes et le reste les minutes.', f'{trajet//60} h {trajet%60:02d} min.'),
        q('À quelle heure l’autocar arrive-t-il ?', 'Additionner la durée à l’heure de départ ; dès que les minutes atteignent 60, les échanger contre une heure. Après minuit, les heures repartent de zéro et on précise le lendemain.', horaire(arrivee)+'.', controle=f'{depart_h}*60+{depart_m}+{trajet} == {arrivee}'),
        q('À quelle heure la visite commence-t-elle ?', 'La pause commence à l’arrivée ; ajouter sa durée à l’heure d’arrivée.', horaire(arrivee+pause)+'.'),
        q('Combien de minutes séparent le départ du début de la visite ?', 'Additionner les deux durées successives, sans additionner les horaires eux-mêmes.', f'{trajet+pause} minutes.'),
        q('La visite dure 1 h 30 min. Exprimer cette durée en heures décimales.', '30 minutes représentent 30/60 d’heure, soit une demi-heure ; le système des minutes est en base 60.', '1,5 h, et non 1,30 h.'),
        q('À quelle heure se termine la visite ?', 'Convertir 1 h 30 min en 90 minutes puis les ajouter au début de la visite.', horaire(arrivee+pause+90)+'.')],
        '1 heure contient 60 minutes : les horaires ne se calculent pas comme des décimaux à deux chiffres.',
        dict(type='timeline',labels=['Départ','Arrivée','Visite'],values=[depart_h*60+depart_m,arrivee,arrivee+pause]),True)


BUILDERS={'pourcentages':pourcentages,'prealgebre':prealgebre,'proportionnalite':proportionnalite,
    'longueurs':longueurs,'aires':aires,'durees':durees}
