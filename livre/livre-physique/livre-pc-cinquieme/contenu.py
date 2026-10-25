"""Plan du manuel et énoncés/corrigés originaux des deux chapitres pilotes."""
from dataclasses import dataclass

PLAN=[
('A','Organisation et transformations de la matière',[
('La matière et ses états','Observer, décrire et utiliser un premier modèle.'),
('Mesurer une masse et un volume','Choisir un instrument, lire, convertir et comparer.'),
('Les changements d’état de l’eau','Température, conservation de la masse et variation du volume.'),
('Corps purs, mélanges et composition de l’air','Distinguer les constituants et décrire un mélange.'),
('Dissolution et miscibilité','Expérimenter, comparer et comprendre une saturation.'),
('Séparer les constituants d’un mélange','Décantation, filtration et évaporation.'),
('Reconnaître une transformation chimique','Premiers exemples expérimentaux et tests fournis.'),
('La Terre dans le Système solaire','Objets célestes et premières échelles de distance.')]),
('B','Mouvement et interactions',[
('Décrire un mouvement','Observateur, trajectoire, direction et sens.'),
('Mesurer et calculer une vitesse','Distance, durée, vitesse et lecture de documents.'),
('Décrire des actions et des interactions','Actions de contact et à distance, approche qualitative.')]),
('C','L’énergie, ses transferts et ses conversions',[
('Sources, formes et conversions d’énergie','Suivre l’énergie dans des objets du quotidien.'),
('Réaliser et schématiser un circuit','Générateur, récepteur, interrupteur et boucle fermée.'),
('Conducteurs, isolants et sécurité électrique','Tester un matériau et reconnaître un court-circuit.'),
('Circuits en série et en dérivation','Comparer les montages et prévoir leur fonctionnement.'),
('Énergie et choix responsables','Ressources, ordres de grandeur et économies d’énergie.')]),
('D','Des signaux pour observer et communiquer',[
('Sources de lumière et vision','Sources primaires, objets diffusants et trajet vers l’œil.'),
('Propagation de la lumière et ombres','Rayons lumineux, écrans et zones d’ombre.'),
('Produire et transmettre un son','Vibrations, milieux de propagation et protection auditive.'),
('Un signal pour transmettre une information','Émetteur, récepteur, code lumineux ou sonore.')])]

SOURCES=[
('Programme du cycle 4','BO n° 31 du 30 juillet 2020, rubrique physique-chimie, pages 96 à 105 de la version Éduscol.','https://eduscol.education.fr/document/621/download'),
('Programmes applicables en 2026-2027','Éduscol, « Enseigner au cycle 4 » : confirmation du texte de référence pour la 5e.','https://eduscol.education.gouv.fr/4362/enseigner-au-cycle-4'),
('Ressources de physique-chimie au cycle 4','Éduscol, page actualisée en mars 2026 : programme, progressions et démarches pédagogiques.','https://eduscol.education.gouv.fr/5739/ressources-d-accompagnement-du-programme-de-physique-chimie-au-cycle-4'),
('Construire une progression au cycle 4','Éduscol, 2016 : repères de progressivité et exemples non prescriptifs.','https://eduscol.education.fr/document/17731/download'),
('Le Système international d’unités','BIPM, 9e édition, mise à jour 2026 : kilogramme, unités de volume et usage du litre.','https://www.bipm.org/fr/publications/si-brochure/'),
('Lire un volume','Collège Carnot, ENT Occitanie : position de l’œil et lecture du bas du ménisque.','https://carnot.mon-ent-occitanie.fr/espaces-pedagogiques/socle-commun/activites-d-accompagnement/comment-mesurer-un-volume--14816.htm')]

@dataclass
class Exo:
    n:int
    titre:str
    questions:list[str]
    reponse:str
    document:str=''
    figure:tuple|None=None
    hauteur:float=0
    caption:str=''
    check:str=''

CH1=[
Exo(1,'Associer une matière à son état',[
 'Indique l’état physique de chaque matière à température ambiante : acier d’une règle, lait, air, huile.',
 'Indique l’état de l’eau dans un glaçon et celui de la vapeur d’eau présente dans l’air.'
], 'L’acier de la règle est solide ; le lait et l’huile sont liquides ; l’air est gazeux. Le glaçon est de l’eau solide. La vapeur d’eau est de l’eau à l’état gazeux, invisible. L’état dépend des conditions, notamment de la température.'),
Exo(2,'Les bons mots',[
 'Complète : un solide compact conserve sa … et son … lorsqu’on le change de récipient.',
 'Complète : un liquide possède un … propre, mais il prend la … du récipient.',
 'Complète : un gaz occupe tout l’espace qui lui est … .'
], 'Forme ; volume. Un liquide possède un volume propre mais prend la forme de la partie du récipient qu’il occupe. Un gaz occupe tout l’espace qui lui est accessible. On compare ici les récipients sans changer la température ni comprimer la matière.'),
Exo(3,'Dessiner une surface libre',[
 'Recopie les deux récipients et dessine la surface libre de l’eau, au repos et loin des parois.',
 'Ajoute une légende qui explique l’orientation de cette surface.'
], 'Dans les deux récipients, la surface libre étendue est horizontale. Elle ne reste pas parallèle au bord du récipient incliné. On trace un trait horizontal et on le légende « surface libre de l’eau au repos ». La courbure près des parois n’est pas étudiée ici.',figure=('tilt',True),hauteur=50,caption='Les deux récipients sont immobiles. Dessine dans ton cahier.'),
Exo(4,'De l’air dans une seringue',[
 'Décris ce qui change lorsqu’on pousse doucement le piston.',
 'L’air s’est-il échappé ? Quelle propriété du gaz cette observation met-elle en évidence ?'
], 'Le volume occupé par l’air passe de 50 mL à 30 mL. L’embout est fermé et ne laisse pas fuir l’air : la même quantité d’air occupe moins de place. Le gaz est compressible. La diminution de volume ne signifie pas que l’air a disparu.',document='La seringue ne contient que de l’air. Son embout est fermé de façon étanche.',figure=('syringes',[50,30]),hauteur=48,check='50>30'),
Exo(5,'Vrai ou faux ? Justifier',[
 '« Un gaz est toujours visible. »',
 '« La vapeur d’eau est constituée de petites gouttes liquides. »',
 '« Un liquide au repos peut avoir une surface libre horizontale. »'
], 'Faux : l’air et la vapeur d’eau sont invisibles. Faux : la vapeur d’eau est gazeuse ; le brouillard visible contient de fines gouttelettes liquides. Vrai : une surface libre suffisamment étendue est plane et horizontale au repos, loin des parois.'),
Exo(6,'Peut-on reconnaître un liquide à sa forme ?',[
 'Le sable et l’eau prennent tous les deux la forme du récipient. Ce critère suffit-il pour les classer comme liquides ?',
 'Observe un grain de sable : quelle propriété permet de préciser son état ?'
], 'Non. Un ensemble de grains peut s’écouler et épouser la forme du récipient. Chaque grain de sable est pourtant solide et conserve sa propre forme. Il faut préciser l’objet observé et combiner plusieurs critères.',figure=('powder',None),hauteur=45),
Exo(7,'Le papier reste sec',[
 'Nomme la matière présente entre le papier et l’eau à l’intérieur du verre.',
 'Explique pourquoi l’eau n’atteint pas immédiatement le papier.',
 'Que peut-on observer si l’on incline le verre sous l’eau ?'
], 'De l’air est piégé dans le verre. Il occupe une partie du volume intérieur et empêche l’eau de remplir immédiatement tout le verre. Si l’on incline suffisamment le verre, l’air peut sortir sous forme de bulles ; l’eau prend alors davantage de place dans le verre et peut mouiller le papier.',document='Observe de nouveau le schéma de l’activité « Le verre protège-t-il le papier ? ».'),
Exo(8,'Changer de récipient',[
 'On transvase 120 mL d’eau d’un récipient étroit dans un récipient large, sans perte. Quel est le volume final ?',
 'Explique pourquoi la hauteur d’eau peut diminuer sans que le volume diminue.'
], 'Le volume final est de 120 mL. Dans le récipient large, l’eau s’étale davantage et la hauteur peut être plus faible. La hauteur seule ne mesure pas le volume : la forme et les dimensions du récipient interviennent.',check='120==120'),
Exo(9,'Observation ou interprétation ?',[
 'Classe ces phrases : « Des bulles quittent le verre » ; « L’air occupait une partie du verre » ; « Le papier est sec ».',
 'Rédige une courte conclusion à partir de ces observations.'
], '« Des bulles quittent le verre » et « Le papier est sec » décrivent des observations. « L’air occupait une partie du verre » est une interprétation. Une conclusion possible : l’air est une matière invisible qui occupe une place ; il peut être déplacé et remplacé par de l’eau.'),
Exo(10,'Lire un modèle',[
 'Quel état correspond à des particules proches les unes des autres et capables de se déplacer les unes par rapport aux autres ?',
 'Dans le modèle du gaz, les particules sont-elles plus grosses ou plus espacées ?',
 'Ce schéma est-il une photographie de la matière ?'
], 'L’état liquide. Dans le modèle du gaz, les particules sont plus espacées ; leur taille n’a pas augmenté. Ce n’est pas une photographie, mais une représentation simplifiée qui aide à expliquer les propriétés observées. Les points ne représentent pas des grains de sable visibles.',figure=('particles',None),hauteur=49),
Exo(11,'Tester une idée correctement',[
 'Lina veut comparer la compressibilité de l’air et de l’eau. Elle utilise une seringue ouverte pour l’air et une seringue fermée pour l’eau. Son test est-il convaincant ?',
 'Propose les conditions à garder identiques et une précaution pour la seringue contenant de l’eau.'
], 'Le test n’est pas convaincant : dans la seringue ouverte, l’air peut sortir. Utiliser deux seringues adaptées, sans aiguille, de même taille et fermées, avec une poussée douce comparable. L’eau doit être sans bulle d’air, sinon on comprimerait surtout la bulle. L’expérience est réalisée avec le professeur, sans forcer.'),
Exo(12,'L’air possède-t-il une masse ?',[
 'Calcule l’augmentation de masse du récipient.',
 'Que permettent de conclure ces mesures à propos de l’air ?'
], '239,6 g - 238,4 g = 1,2 g. La masse a augmenté après l’admission d’air. Si seul le contenu en air a changé, cette augmentation montre que l’air possède une masse. Être invisible ne signifie pas être dépourvu de matière.',document='Un dispositif de laboratoire permet de peser le même récipient rigide fermé. Avec très peu d’air : 238,4 g. Après admission d’air, sans autre modification : 239,6 g. Données pédagogiques.',check='2396-2384==12'),
Exo(13,'Une légende scientifique',[
 'Une image de brouillard porte la légende : « On voit la vapeur d’eau dans l’air ». Explique ce qui pose problème.',
 'Propose une légende scientifiquement correcte et compréhensible.'
], 'La vapeur d’eau est invisible. Le brouillard visible contient des gouttelettes d’eau liquide en suspension dans l’air. Une légende correcte serait : « De fines gouttelettes d’eau liquide rendent le brouillard visible. L’air contient aussi de la vapeur d’eau invisible. »'),
Exo(14,'Le sable met la règle à l’épreuve',[
 'Noé affirme : « Tout ce qui s’écoule est liquide. » Utilise un contre-exemple pour discuter son affirmation.',
 'Écris une description qui distingue le comportement de l’ensemble et l’état de chaque grain.'
], 'Le sable est un contre-exemple : on peut le verser, pourtant chaque grain est solide. L’ensemble change de forme quand les grains se déplacent les uns par rapport aux autres. Une description rigoureuse précise donc « un ensemble de grains solides » plutôt que « un liquide ».'),
Exo(15,'Identifier trois échantillons',[
 'Associe A, B et C à un état physique en citant à chaque fois deux propriétés.',
 'Explique pourquoi une seule propriété peut parfois être insuffisante.'
], 'A est un solide compact : forme et volume propres. B est un liquide : il change de forme, conserve son volume et se comprime très peu dans les conditions du test. C est un gaz : il occupe tout l’espace accessible et son volume diminue lorsqu’on le comprime. Un ensemble de grains montre qu’un seul critère, comme prendre la forme d’un récipient, peut tromper.',document='A : forme conservée lors d’un transfert, volume conservé. B : forme modifiée lors d’un transfert, volume conservé, très peu compressible. C : tout l’espace accessible est occupé ; une compression réduit son volume.')
]

CH2=[
Exo(1,'Choisir la grandeur et l’instrument',[
 'Pour connaître la masse d’une trousse, choisis : balance ou éprouvette graduée ? Propose une unité.',
 'Pour connaître le volume d’un peu d’eau, choisis un instrument et une unité adaptés.',
 'Que mesure une valeur exprimée en cm³ ?'
], 'Une balance, avec une masse en g ou en kg. Pour un peu d’eau, une éprouvette graduée et une lecture en mL conviennent. Le cm³ est une unité de volume : il ne mesure pas une masse.'),
Exo(2,'Lire une pesée',[
 'Après la tare avec le récipient vide, la balance affiche 37,6 g quand on ajoute le liquide. Quelle est la masse du liquide ?',
 'Pourquoi ne faut-il pas ajouter à nouveau la masse du récipient ?'
], 'La masse du liquide est de 37,6 g. La tare a remis l’affichage à zéro avec le récipient déjà posé : sa masse a été prise en compte par la balance. L’affichage représente donc uniquement la masse ajoutée.'),
Exo(3,'Lire une éprouvette',[
 'Détermine le volume correspondant à une petite division.',
 'Lis le volume au bas du ménisque et écris le résultat avec son unité.'
], 'Entre 20 mL et 30 mL, il y a 5 intervalles égaux : une petite division vaut 2 mL. Le bas du ménisque atteint 24 mL. On écrit V = 24 mL, et non 24 g.',figure=('cylinders',[[24],50,2]),hauteur=67,check='10/5==2'),
Exo(4,'Convertir sans confondre',[
 'Convertis : 1,25 kg en g ; 750 g en kg.',
 'Convertis : 2,4 L en mL ; 350 mL en L.',
 'Complète : 18 mL = … cm³ ; 3 L = … dm³.'
], '1,25 kg = 1 250 g ; 750 g = 0,750 kg. 2,4 L = 2 400 mL ; 350 mL = 0,350 L. 18 mL = 18 cm³ ; 3 L = 3 dm³. La grandeur ne change pas pendant une conversion.',check='1.25*1000==1250 and 750/1000==0.75 and 2.4*1000==2400 and 350/1000==0.35'),
Exo(5,'Corriger l’unité',[
 'Lina lit 35 mL dans une éprouvette et écrit : « La masse du liquide est 35 g ». Explique son erreur.',
 'Écris ce que cette mesure permet réellement de connaître.'
], 'L’éprouvette fournit un volume, pas une masse. On peut écrire : « Le volume du liquide est V = 35 mL. » Pour sa masse, il faut une pesée. Une égalité numérique entre mL et g n’est pas une règle générale.'),
Exo(6,'Peser sans utiliser la tare',[
 'Calcule la masse du liquide.',
 'Explique l’opération à l’aide des grandeurs qui interviennent.'
], 'La masse totale réunit le récipient et le liquide. Masse du liquide = masse totale - masse du récipient = 187,3 g - 62,8 g = 124,5 g. On soustrait des masses exprimées dans la même unité.',document='Récipient vide : 62,8 g. Même récipient contenant un liquide : 187,3 g.',check='1873-628==1245'),
Exo(7,'Deux méthodes, un même résultat',[
 'Méthode A : récipient vide 45,2 g ; récipient et liquide 118,7 g. Détermine la masse du liquide.',
 'Méthode B : après tare avec le même récipient vide, on verse le même liquide. Quelle valeur devrait s’afficher ?'
], 'Méthode A : 118,7 g - 45,2 g = 73,5 g. Méthode B : environ 73,5 g, si la même quantité de liquide est versée et si les mesures sont réalisées dans les mêmes conditions. Les deux méthodes retirent l’effet de la masse du récipient.',check='1187-452==735'),
Exo(8,'Mesurer un petit solide',[
 'Lis le volume avant et après immersion.',
 'Détermine le volume du solide et exprime-le en cm³.'
], 'Avant : 32 mL. Après : 46 mL. Le solide déplace 46 mL - 32 mL = 14 mL d’eau. Son volume vaut donc 14 cm³. L’eau et l’objet occupent ensemble le volume final ; ce volume final n’est pas celui du solide seul.',document='Solide entièrement immergé, insoluble et non absorbant. Aucune bulle n’est accrochée.',figure=('displacement',[[32,46],50,2]),hauteur=50,check='46-32==14'),
Exo(9,'Un repère pour l’eau',[
 'À température ambiante, quelle masse approximative correspond à 250 mL d’eau ?',
 'Une huile de même volume a-t-elle nécessairement cette masse ? Justifie.'
], 'Environ 250 g, car pour l’eau usuelle à température ambiante, 1 mL correspond approximativement à 1 g. Ce repère ne s’applique pas à tous les liquides. La masse de 250 mL d’huile doit être mesurée ou déterminée à partir de données propres à cette huile.'),
Exo(10,'Exploiter une proportionnalité',[
 'Complète les masses correspondant à 60 mL et 80 mL.',
 'Explique comment tu passes de 20 mL à 80 mL.',
 'Quelle condition faut-il conserver pour comparer ces mesures ?'
], 'Les masses sont approximativement 60 g et 80 g. Le volume est multiplié par 4 entre 20 mL et 80 mL ; la masse l’est aussi : 20 g × 4 = 80 g. Il faut garder la même substance, ici l’eau, et la même température. Ces valeurs pédagogiques sont arrondies.',document='Eau à température ambiante, données arrondies : 20 mL → 20 g ; 40 mL → 40 g.',check='20*4==80'),
Exo(11,'Choisir une verrerie adaptée',[
 'Pour mesurer environ 38 mL, choisis entre une éprouvette de 50 mL graduée tous les 1 mL et une éprouvette de 1 L graduée tous les 20 mL.',
 'Justifie ton choix avec la capacité et la graduation.'
], 'L’éprouvette de 50 mL convient : sa capacité suffit pour 38 mL et ses divisions de 1 mL permettent une lecture plus fine. Celle de 1 L possède une capacité inutilement grande ici et des divisions trop larges pour distinguer facilement 38 mL.'),
Exo(12,'Comparer sans mélanger les grandeurs',[
 'Quel échantillon possède le plus grand volume ? Lequel possède la plus grande masse ?',
 'Explique pourquoi « le plus volumineux est toujours le plus lourd » n’est pas une conclusion générale.'
], 'A a le plus grand volume : 45 mL contre 30 mL. B a la plus grande masse : 60 g contre 40 g. Les substances sont différentes ; un plus grand volume ne garantit donc pas une plus grande masse. Le mot « lourd » doit ici être remplacé par une comparaison précise des masses.',document='Échantillon A : volume 45 mL, masse 40 g. Échantillon B, constitué d’une autre matière : volume 30 mL, masse 60 g.'),
Exo(13,'Un protocole à discuter',[
 'Le morceau de bois flotte et dépasse de l’eau. La différence des deux lectures donne-t-elle son volume total ?',
 'Indique une condition qui n’est pas respectée et propose une façon de poursuivre l’étude.'
], 'Non. Une partie du bois dépasse de l’eau ; seule la partie immergée déplace de l’eau. Le protocole simple exige un objet entièrement immergé. On peut choisir un solide compact qui s’immerge complètement, ou faire adapter le protocole par le professeur. On ne compte pas le volume d’un doigt ajouté pour maintenir l’objet.',figure=('floating',None),hauteur=59),
Exo(14,'Une identification prudente',[
 'Un liquide inconnu a une masse de 45 g pour 50 mL. Est-ce compatible avec le liquide de référence ?',
 'Ces seules mesures permettent-elles de prouver l’identité du liquide ?'
], 'Oui. Doubler 25 mL donne 50 mL et doubler 22,5 g donne 45 g : les données sont compatibles avec la même proportionnalité. Cela ne prouve pas l’identité du liquide : plusieurs substances peuvent présenter des valeurs voisines et toute mesure possède une précision limitée. D’autres observations ou tests seraient nécessaires.',document='Pour un liquide de référence, dans les conditions de l’étude : 25 mL ont une masse de 22,5 g. Pour l’échantillon inconnu : 50 mL ont une masse de 45 g.',check='22.5*2==45 and 25*2==50'),
Exo(15,'Réunir deux mesures indépendantes',[
 'Calcule la masse du solide.',
 'Calcule son volume en mL, puis en cm³.',
 'L’affirmation « sa masse en g est forcément égale à son volume en mL » est-elle vérifiée ? Rédige une conclusion.'
], 'Masse du solide : 125,6 g - 91,4 g = 34,2 g. Volume : 52 mL - 38 mL = 14 mL, soit 14 cm³. Les valeurs 34,2 et 14 sont différentes : il n’existe pas de correspondance universelle 1 mL = 1 g. On a mesuré deux grandeurs distinctes sur le même échantillon.',document='Coupelle vide : 91,4 g ; avec le solide : 125,6 g. L’expérience ci-dessous concerne ce même solide, entièrement immergé, non absorbant, sans bulle et sans réaction avec l’eau.',figure=('displacement',[[38,52],100,2]),hauteur=58,check='1256-914==342 and 52-38==14')
]

assert [e.n for e in CH1]==list(range(1,16))
assert [e.n for e in CH2]==list(range(1,16))
