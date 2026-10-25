"""Cours, activités et exercices originaux : matière et Système solaire."""
from programme_complet import *

C3=Chapitre(3,'Pourquoi la glace fond-elle sans que l’eau disparaisse ?',[
    'Nommer les changements d’état et distinguer état et changement d’état.',
    'Mesurer une température et lire une courbe de changement d’état.',
    'Distinguer conservation de la masse et variation du volume.'
],[
Lecon('Passer d’un état à un autre',
    'Un changement d’état est une transformation physique : la substance reste la même. La fusion transforme un solide en liquide ; la solidification réalise le passage inverse. La vaporisation transforme un liquide en gaz ; la liquéfaction transforme un gaz en liquide. L’évaporation se produit à la surface du liquide, même sans ébullition. L’ébullition se produit dans tout le liquide avec formation de bulles de vapeur.',
    ('pc_changes',None),'Les flèches indiquent les changements, et non le déplacement d’une matière entre deux récipients.',
    'Un glaçon qui fond et de l’eau qui bout restent constitués d’eau. Chauffer ne provoque donc pas toujours une transformation chimique.',
    'Décrire d’abord l’état initial et l’état final. Écrire ensuite le nom du changement : eau liquide → eau gazeuse : vaporisation.'),
Lecon('Température et changement d’état',
    'La température se mesure avec un thermomètre et s’exprime ici en degré Celsius (°C). Lorsqu’on chauffe de la glace d’eau pure sous la pression atmosphérique usuelle, la fusion se déroule autour de 0 °C. Tant que glace et eau liquide coexistent, l’énergie reçue sert au changement d’état et la température reste voisine de 0 °C. Ce palier est un repère expérimental, avec les limites de précision des mesures.',
    ('pc_temperature',None),'Exemple pédagogique de chauffage de glace d’eau pure ; pression atmosphérique usuelle.',
    'Un palier correspond à plusieurs mesures successives de température presque égale. Un simple point ne constitue pas un palier. L’eau pure bout vers 100 °C à la pression atmosphérique normale.',
    'Lire le titre des axes, leurs unités et leurs graduations. Décrire séparément les portions qui montent et la portion horizontale.'),
Lecon('Même masse, volume parfois différent',
    'Lors d’un changement d’état, la masse se conserve si aucune matière n’entre ni ne sort du système étudié. Le volume peut changer. Pour l’eau, la glace occupe davantage de place que la même masse d’eau liquide. Une bouteille pleine et fermée peut donc être endommagée par le gel. Le modèle particulaire conserve les mêmes particules, tout en modifiant leur organisation et leurs mouvements.',
    ('pc_freeze_mass',None),'La masse affichée inclut le récipient fermé. Schéma qualitatif : le volume augmente lors du gel de l’eau.',
    'Conserver la masse ne signifie pas conserver le volume. Si de la vapeur s’échappe d’un récipient ouvert, la masse de ce qui reste dans le récipient diminue.',
    'Préciser les limites du système pesé : eau seule, ou eau et récipient. Comparer les mesures sur le même ensemble et dans les mêmes conditions.')
],Activite('Suivre la fusion de la glace',
    'Exploiter des mesures de température pour repérer la fusion de l’eau pure.',[
    'En classe : placer un thermomètre adapté dans un mélange de glace pilée et d’un peu d’eau. Éviter le contact du capteur avec la paroi.',
    'Relever la température à intervalles réguliers pendant un réchauffement doux choisi par le professeur. Noter si de la glace reste visible.',
    'Tracer la courbe avec les valeurs réellement mesurées. Pour s’entraîner, utiliser la série pédagogique du schéma.'
],('pc_temperature',{'t':[0,1,2,3,4,5,6],'v':[-5,0,0,0,0,5,10],'min':-10,'max':10}),
    'Données d’entraînement : temps en min ; température en °C. Le réchauffement et la durée du palier dépendent du montage.',[
    'Entre quelles dates observe-t-on un palier ? Quel changement d’état est compatible avec ce palier ?',
    'Pourquoi faut-il aussi observer le contenu du récipient ?',
    'Rédige une conclusion qui associe les mesures et l’observation de la glace.'
], 'Le palier s’étend de 1 à 4 min à 0 °C. Si l’on observe simultanément de la glace et de l’eau liquide, il correspond à la fusion. La courbe seule ne décrit pas tout le contenu du récipient. Après disparition de la glace, l’eau liquide peut se réchauffer : la température augmente. Les mesures expérimentales peuvent osciller légèrement autour de 0 °C.'),[
    'Un changement d’état conserve la nature de la substance.',
    'Fusion, solidification, vaporisation et liquéfaction décrivent des passages précis.',
    'Une température se mesure et se donne avec son unité.',
    'Un corps pur peut présenter un palier lors d’un changement d’état à pression fixée.',
    'Dans un système fermé, la masse se conserve ; le volume peut varier.'
], '« L’eau s’évapore, donc elle n’existe plus. » Elle devient gazeuse et peut quitter le récipient ; elle ne disparaît pas.',[
E(1,'Nommer les passages',['Un glaçon devient liquide. Quel changement d’état se produit ?','L’eau liquide devient de la glace. Quel est le changement inverse ?'],'La glace subit une fusion. Le passage de l’eau liquide à la glace est une solidification. On donne le nom du passage, et non seulement le nom de l’état final.'),
E(2,'La buée sur une vitre',['De la vapeur d’eau forme des gouttelettes sur une vitre froide. Nomme le changement.','Quel est l’état physique de ces gouttelettes ?'],'La vapeur d’eau se liquéfie : c’est une liquéfaction. Les gouttelettes sont liquides. La vapeur invisible présente dans l’air ne doit pas être confondue avec la buée visible.'),
E(3,'Lire une température',['Quelle grandeur porte l’axe vertical ? Quelle est son unité ?','À quelle température se situe le palier ?'],'L’axe vertical porte la température θ, en °C. Le palier est situé à 0 °C. On lit la valeur sur l’axe vertical, et non une durée sur l’axe horizontal.',figure=('pc_temperature',None)),
E(4,'Évaporation ou ébullition ?',['Du linge sèche à 20 °C. L’eau a-t-elle nécessairement bouilli ?','Une casserole d’eau forme des bulles de vapeur dans tout le liquide. Comment nommer cette vaporisation ?'],'Le linge sèche par évaporation ; l’eau n’a pas besoin d’atteindre 100 °C. Une vaporisation avec des bulles de vapeur dans tout le liquide est une ébullition.'),
E(5,'Choisir la bonne unité',['Complète : la température du mélange vaut 0 … .','Pourquoi « 0 min » ne convient-il pas ?'],'La température vaut 0 °C. La minute est une unité de durée et ne mesure pas une température. Même lorsque la valeur numérique est nulle, l’unité est indispensable.'),
E(6,'Peser pendant la fusion',['Quelle masse doit-on retrouver après fusion complète ?','Cite la condition indispensable à cette prévision.'],'On doit retrouver 180,0 g pour l’ensemble fermé. Il ne faut ni fuite, ni ajout, ni perte de matière. La masse de l’ensemble se conserve pendant cette transformation physique.',document='Un récipient fermé contenant de la glace a une masse totale de 180,0 g. Il reste fermé pendant la fusion.'),
E(7,'Deux grandeurs à distinguer',['Le niveau augmente lors du gel. Peut-on conclure que la masse d’eau augmente ?','Explique en distinguant masse et volume.'],'Non. L’eau solide occupe davantage de volume que l’eau liquide de même masse. Le niveau renseigne sur le volume occupé ; il ne démontre pas une augmentation de masse.',figure=('pc_freeze_mass',None)),
E(8,'Durée du palier',['Le palier commence à 3 min et finit à 8 min. Quelle est sa durée ?','Que peut-on observer dans le récipient pendant ce palier de fusion ?'],'La durée est 8 - 3 = 5 min. Pour de l’eau pure en fusion, on peut observer simultanément de la glace et de l’eau liquide. La durée n’est pas la température du changement.',check='8-3==5'),
E(9,'Dessiner une courbe',['Trace la courbe des températures en fonction du temps.','Repère la portion correspondant à la fusion.'],'Placer les points (0 ; -5), (1 ; 0), (2 ; 0), (3 ; 0), (4 ; 5), puis les relier dans l’ordre. La portion horizontale de 1 à 3 min est compatible avec une fusion à 0 °C si glace et eau liquide coexistent.',document='Eau pure, pression usuelle. Temps : 0, 1, 2, 3, 4 min. Température : -5, 0, 0, 0, 5 °C.'),
E(10,'Le récipient ouvert',['La masse mesurée passe de 250 g à 242 g. Quelle masse a quitté le récipient ?','Pourquoi cela ne contredit-il pas la conservation de la masse ?'],'250 - 242 = 8 g ont quitté l’ensemble pesé, si aucune autre perte n’a eu lieu. La vapeur d’eau s’est dispersée dans l’air. Le récipient ouvert n’est pas un système fermé : il faut compter aussi l’eau partie dans l’environnement.',document='On chauffe doucement de l’eau dans un récipient ouvert. Aucune éclaboussure n’est observée.',check='250-242==8'),
E(11,'Le bon placement du thermomètre',['Pourquoi éviter d’appuyer le capteur sur le fond chauffé ?','Quelle information supplémentaire faut-il noter à chaque mesure ?'],'Le fond peut être plus chaud que le contenu et fausser la température recherchée. Le capteur doit mesurer le milieu étudié selon les consignes du matériel. Noter aussi la date et la présence des différents états, par exemple glace et eau liquide.'),
E(12,'Un glaçon dans un sachet',['Propose une expérience pour tester la conservation de la masse pendant la fusion.','Indique une observation qui invaliderait le protocole.'],'Peser un sachet fermé et étanche contenant un glaçon, le laisser fondre, sécher son extérieur et repeser le même ensemble. Une fuite ou de l’eau ajoutée à l’extérieur invalide la comparaison. On compare les masses avec la précision de la balance.'),
E(13,'Une eau qui bout à 94 °C',['Un document donne une pression atmosphérique plus faible qu’au niveau de la mer. Le thermomètre est-il forcément défectueux ?','Quelle condition faut-il préciser lorsqu’on annonce « l’eau bout à 100 °C » ?'],'Le thermomètre n’est pas forcément défectueux : la température d’ébullition dépend de la pression. Il faut préciser la pression, notamment la pression atmosphérique normale pour la valeur voisine de 100 °C. Une vérification de l’instrument reste possible.'),
E(14,'Un palier trop vite annoncé',['Une élève mesure une seule fois 0 °C puis écrit « il y a un palier ». Pourquoi sa conclusion est-elle insuffisante ?','Quelles mesures et observations compléter ?'],'Un point ne suffit pas à montrer une température stable pendant une durée. Il faut plusieurs mesures successives à intervalles réguliers et l’observation des états présents. Un palier de fusion est étayé par une température presque constante et la coexistence du solide et du liquide.'),
E(15,'Interpréter le modèle',['Les particules d’eau deviennent-elles plus grosses quand la glace fond ?','Que conserve-t-on et que modifie-t-on dans un modèle simple ?'],'On ne fait pas grossir les particules. Dans un modèle simple de changement d’état, la nature et le nombre des particules d’eau sont conservés. Leur organisation et leurs possibilités de mouvement changent. Le modèle n’est pas une photographie.')
],Defi('Enquêter sur une bouteille déformée',
    'Une bouteille presque pleine d’eau a été oubliée au congélateur. Après gel, elle est déformée. Un camarade affirme : « La glace pèse plus lourd, donc elle pousse la bouteille. » Construis une explication scientifique sans refaire cette manipulation.',
    ('pc_freeze_mass',None),['Identifie les deux grandeurs confondues.','Propose une vérification sûre de la conservation de la masse.','Explique la déformation avec la propriété de l’eau lors du gel.'],
    'Comparer une même masse d’eau sous deux états et distinguer l’espace occupé de la masse.',
    'Le camarade confond masse et volume. À quantité d’eau conservée, la masse reste identique, mais la glace occupe davantage de volume. La place disponible dans une bouteille presque pleine devient insuffisante. Pour vérifier la masse, utiliser une expérience de fusion dans un récipient adapté, fermé et étanche ; ne pas congeler une bouteille pleine et rigide.'))

C4=Chapitre(4,'Un liquide transparent est-il forcément de l’eau pure ?',[
    'Distinguer corps pur, mélange homogène et mélange hétérogène.',
    'Relier un modèle particulaire à la présence d’une ou plusieurs espèces.',
    'Décrire la composition approximative de l’air sec.'
],[
Lecon('Une seule espèce ou plusieurs ?',
    'Une espèce chimique désigne une catégorie de constituants identiques du point de vue chimique. Un corps pur ne contient qu’une seule espèce ; un mélange en contient plusieurs. Une eau minérale contient de l’eau et des substances dissoutes : c’est un mélange. L’eau distillée est considérée comme un corps pur dans le modèle scolaire si les impuretés sont négligées. L’aspect seul ne permet pas de compter les espèces présentes.',
    ('pc_particles_mix',None),'Modèles simplifiés : les couleurs représentent des espèces différentes, sans représenter leur couleur réelle.',
    '« Pur » a un sens scientifique précis. Une eau potable n’est pas nécessairement un corps pur ; une eau chimiquement pure n’est pas automatiquement garantie potable.',
    'Pour classer un échantillon, rechercher sa composition. Une couleur, une étiquette publicitaire ou la transparence ne remplacent pas cette information.'),
Lecon('Homogène ou hétérogène ?',
    'À l’œil nu, on distingue plusieurs constituants ou plusieurs phases d’un mélange hétérogène. Dans un mélange homogène, on ne distingue qu’une seule phase à cette échelle d’observation. L’eau salée est homogène lorsque le sel est entièrement dissous. L’eau et l’huile forment après repos deux phases visibles. Le classement dépend des conditions et de l’échelle d’observation ; une agitation peut produire une dispersion temporaire.',
    ('pc_mixtures',None),'À gauche, une solution homogène ; à droite, deux phases liquides après repos.',
    'Une seule phase visible n’implique pas une seule espèce chimique. Un mélange homogène peut être incolore, transparent ou coloré.',
    'Observer après agitation puis après repos. Écrire « je distingue… » avant de conclure « le mélange est… ». Ne jamais goûter un produit pour l’identifier.'),
Lecon('L’air, un mélange de gaz',
    'L’air qui nous entoure est un mélange. Pour l’air sec, on retient environ 78 % de diazote et 21 % de dioxygène en volume. Le pour cent restant rassemble d’autres gaz, notamment l’argon et le dioxyde de carbone. L’air ambiant contient aussi une quantité variable de vapeur d’eau. Ces proportions ne signifient pas qu’un petit récipient contient des couches de gaz séparées.',
    ('pc_air',None),'Cent points représentent cent parts égales de volume d’air sec ; valeurs arrondies.',
    'L’air n’est pas du dioxygène pur. Les mots « gaz », « air » et « dioxygène » n’ont pas le même sens.',
    'Sur 100 parts d’air sec, environ 21 correspondent au dioxygène. Pour 200 parts, toutes les valeurs sont multipliées par 2 ; la proportion reste la même.')
],Activite('Classer sans se fier à la couleur',
    'Construire un classement à partir d’observations et de compositions fournies.',[
    'Préparer avec le professeur de l’eau salée sans cristaux visibles, de l’eau et de l’huile, puis de l’eau distillée de laboratoire.',
    'Observer les récipients, les laisser reposer et noter le nombre de phases visibles. Ne goûter aucun échantillon.',
    'Comparer l’observation aux compositions connues : eau seule dans le modèle ; eau et sel ; eau et huile.'
],('pc_mixtures',None),'Deux aspects possibles ne suffisent pas à distinguer un corps pur d’un mélange homogène.',[
    'Quel échantillon est un corps pur dans le modèle ? Lesquels sont des mélanges ?',
    'Pourquoi l’œil ne permet-il pas de distinguer eau distillée et eau salée ?',
    'Rédige une phrase qui utilise correctement « transparent » et « homogène ».'
], 'L’eau distillée est le corps pur dans le modèle annoncé. L’eau salée est un mélange homogène ; l’eau et l’huile forment un mélange hétérogène après repos. L’eau distillée et l’eau salée peuvent toutes deux être transparentes : la transparence ne révèle pas le nombre d’espèces. Il faut utiliser la composition connue ou réaliser des tests adaptés.'),[
    'Un corps pur contient une seule espèce chimique ; un mélange en contient plusieurs.',
    'Homogène : une seule phase visible à l’échelle considérée.',
    'Hétérogène : plusieurs phases ou constituants visibles.',
    'L’aspect transparent ne prouve pas la pureté.',
    'L’air sec contient environ 78 % de diazote et 21 % de dioxygène en volume.'
], '« Je ne vois pas le sel, donc il n’y en a plus. » Une substance dissoute reste présente même si elle n’est plus visible.',[
E(1,'Corps pur ou mélange ?',['Classe : eau seule, eau salée, air sec.','Quel critère utilises-tu ?'],'L’eau seule est un corps pur dans le modèle ; l’eau salée et l’air sec sont des mélanges. Le critère est le nombre d’espèces chimiques présentes, pas le nombre d’états physiques.'),
E(2,'Nommer l’aspect',['On distingue de la pulpe dans un jus. Le mélange est-il homogène ou hétérogène ?','Une eau salée sans cristaux visibles présente une seule phase. Comment la classer ?'],'Le jus avec pulpe est hétérogène à l’œil nu. L’eau salée sans cristaux visibles est homogène à cette échelle. Dans les deux cas, plusieurs espèces sont présentes.'),
E(3,'Les deux gaz principaux',['Nomme les deux principaux gaz de l’air sec.','Donne leurs proportions approximatives en volume.'],'Le diazote représente environ 78 % et le dioxygène environ 21 % du volume de l’air sec. Les autres gaz représentent ensemble environ 1 %.'),
E(4,'Lire un modèle',['Quel dessin représente un corps pur ?','Que représente le changement de couleur des points ?'],'Le dessin avec une seule couleur représente un corps pur ; celui à deux couleurs représente un mélange. Chaque couleur code une espèce chimique, et non la couleur visible réelle du gaz ou du liquide.',figure=('pc_particles_mix',None)),
E(5,'Déjouer une affirmation',['« Un liquide incolore est pur. » Vrai ou faux ? Donne un contre-exemple.'],'Faux. De l’eau contenant du sel entièrement dissous peut être incolore et transparente tout en contenant plusieurs espèces. L’aspect ne suffit pas pour établir la pureté.'),
E(6,'Lire une étiquette',['Une eau contient des ions calcium, magnésium et des hydrogénocarbonates en plus de l’eau. Est-ce un mélange ?','Peut-elle être potable tout en étant un mélange ?'],'Oui : la composition mentionne plusieurs espèces. Une eau peut respecter les critères de potabilité tout en étant un mélange ; la potabilité et la pureté chimique répondent à des questions différentes.'),
E(7,'Air sec dans une seringue',['Dans 100 mL d’air sec, quel volume correspond approximativement au dioxygène ?','Quel volume correspond au diazote ?'],'Environ 21 mL correspondent au dioxygène et 78 mL au diazote, à conditions de mesure identiques. Il s’agit d’une description en proportions de volumes ; les gaz ne forment pas des couches distinctes.'),
E(8,'Changer de quantité',['Calcule les parts de dioxygène et de diazote correspondant à 200 mL d’air sec.','Les pourcentages ont-ils doublé ?'],'Les volumes correspondants sont environ 42 mL de dioxygène et 156 mL de diazote. Les pourcentages restent 21 % et 78 % : c’est la quantité totale qui a doublé.',check='21*2==42 and 78*2==156'),
E(9,'Agiter puis laisser reposer',['Après agitation, eau et huile semblent dispersées. Après repos, deux couches apparaissent. Quelle observation est décisive ?','Comment classer le mélange après repos ?'],'L’apparition durable de deux phases après repos est décisive. Le mélange est alors hétérogène. Une dispersion temporaire de petites gouttes ne prouve pas que les deux liquides sont miscibles.'),
E(10,'Faire le total',['Calcule la part des autres gaz.','Pourquoi ne peut-on pas attribuer tout ce reste au dioxyde de carbone ?'],'100 - 78 - 21 = 1 %. Ce reste comprend plusieurs gaz, dont l’argon et le dioxyde de carbone. Le dioxyde de carbone n’en représente qu’une partie.',document='Air sec : 78 % de diazote et 21 % de dioxygène, valeurs arrondies.',check='100-78-21==1'),
E(11,'Préciser l’échelle',['Un lait paraît uniforme à l’œil nu, mais contient de minuscules gouttes de matière grasse dispersées. Que faut-il préciser dans sa description ?','Pourquoi les observations au microscope et à l’œil nu peuvent-elles différer ?'],'Il faut préciser l’échelle d’observation. Un aspect uniforme à l’œil nu peut masquer une dispersion visible à une autre échelle. Les deux descriptions ne sont pas contradictoires si leurs conditions sont annoncées.'),
E(12,'Deux flacons identiques',['Un flacon contient de l’eau pure, l’autre de l’eau salée. Tous deux sont limpides. Propose une méthode pour les distinguer sans goûter.','Quelle limite faut-il garder en tête ?'],'Sur de petits échantillons, le professeur peut faire évaporer l’eau : un résidu solide est attendu pour l’eau salée. L’absence de résidu visible ne prouve pas à elle seule une pureté parfaite ; la quantité et la sensibilité de la méthode comptent.'),
E(13,'Un modèle à corriger',['Un dessin représente l’air par une seule sorte de points. Est-ce cohérent avec sa composition ?','Comment améliorer la légende et le dessin ?'],'Le dessin ne représente pas sa composition de mélange s’il annonce une seule espèce. Utiliser plusieurs sortes de points avec une légende, en respectant approximativement les proportions pour un échantillon assez grand. Ne pas confondre la taille des points et la proportion.'),
E(14,'Passer à un litre',['Détermine les volumes correspondant aux deux gaz principaux dans 1 L d’air sec.','Exprime les résultats en mL.'],'1 L = 1 000 mL, soit dix fois 100 mL. Environ 780 mL correspondent au diazote et 210 mL au dioxygène. Les 10 mL restants correspondent à d’autres gaz, selon les valeurs arrondies retenues.',check='78*10==780 and 21*10==210'),
E(15,'Argumenter avec deux indices',['Un liquide transparent laisse un dépôt après évaporation. Que peut-on en conclure ?','Peut-on identifier précisément la substance du dépôt par cette seule observation ?'],'Le liquide contenait au moins une substance non volatile dans les conditions de l’expérience : il n’était pas constitué seulement d’eau. On ne peut pas identifier précisément le dépôt par sa seule présence. Il faut d’autres informations ou des tests adaptés.')
],Defi('Préparer un modèle de l’air',
    'Tu disposes de 100 jetons de même taille pour représenter l’air sec. Construis une affiche qui explique à un élève de 6e ce que représente chaque jeton et ce que le modèle ne montre pas.',
    ('pc_air',None),['Répartis les jetons et prépare une légende.','Explique pourquoi ce modèle ne représente pas des couches de gaz.','Adapte la répartition à 200 jetons.'],
    'Garder les proportions, et préciser que l’air réel contient des constituants en mouvement.',
    'Utiliser 78 jetons pour le diazote, 21 pour le dioxygène et 1 pour les autres gaz. Mélanger les jetons dans la représentation, avec une légende. Le modèle code des proportions arrondies en volume ; il ne montre ni les tailles réelles ni les mouvements. Avec 200 jetons : 156, 42 et 2.'))

C5=Chapitre(5,'Le sucre a-t-il disparu lorsqu’on ne le voit plus ?',[
    'Identifier solvant, soluté et solution.',
    'Tester une dissolution et reconnaître une saturation.',
    'Distinguer dissolution d’un solide et miscibilité de deux liquides.'
],[
Lecon('Dissoudre sans faire disparaître',
    'Lorsqu’un solide se dissout dans un liquide, ses constituants se dispersent dans le liquide. Le liquide qui dissout est le solvant ; la substance dissoute est le soluté. Le mélange homogène obtenu est une solution. Avec de l’eau comme solvant, on parle de solution aqueuse. Le soluté ne devient pas nécessairement liquide et ne disparaît pas : une dissolution n’est pas une fusion.',
    ('pc_dissolve',None),'Les points colorés symbolisent le soluté réparti dans l’eau ; ils ne représentent pas des grains visibles.',
    'Si tout le sel est dissous, il reste présent dans la solution. Dans un système sans perte, masse de solution = masse de solvant + masse de soluté ajouté.',
    'Pour préparer une solution, peser le soluté et le solvant séparément, puis mélanger sans perte. Ne pas additionner automatiquement les volumes.'),
Lecon('Il existe une limite à la dissolution',
    'Un solide est soluble dans un solvant s’il peut s’y dissoudre dans les conditions étudiées. Si l’on ajoute progressivement trop de soluté, un dépôt peut persister malgré une agitation suffisante : la solution est saturée. La quantité maximale dissoute dépend notamment du soluté, du solvant et de la température. Agiter facilite le contact et accélère souvent la dissolution, sans garantir que toute quantité pourra se dissoudre.',
    ('pc_dissolve',None),'Dans le dernier récipient, une partie du solide reste au fond : la solution au-dessus est saturée.',
    'Un dépôt juste après l’ajout n’est pas à lui seul la preuve d’une saturation. Laisser assez de temps et agiter selon le protocole avant de conclure.',
    'Comparer des essais avec la même quantité de solvant à la même température. Modifier une seule variable à la fois.'),
Lecon('Mélanger deux liquides',
    'Deux liquides miscibles forment un mélange homogène lorsqu’on les mélange dans les proportions étudiées. L’eau et l’éthanol sont miscibles ; leur manipulation éventuelle reste encadrée en classe. L’eau et l’huile sont non miscibles : après agitation puis repos, elles forment des phases distinctes. Une dispersion temporaire de gouttelettes ne constitue pas une preuve de miscibilité.',
    ('pc_mixtures',None),'Une phase visible après mélange ; deux phases après repos dans le cas de liquides non miscibles.',
    'On parle ici de dissolution pour un solide dans un liquide, et de miscibilité pour comparer deux liquides. Toujours nommer les substances et les conditions.',
    'Agiter doucement les deux liquides dans un récipient adapté, puis observer après repos. Décrire les phases avant d’utiliser le mot miscible.')
],Activite('Chercher une limite expérimentale',
    'Déterminer entre quelles masses se situe une limite de dissolution.',[
    'Le professeur fournit trois essais réalisés avec 50 g d’eau à la même température et un solide X : 10 g entièrement dissous ; 15 g entièrement dissous ; 20 g avec dépôt persistant.',
    'Comparer les essais après une même durée d’agitation et de repos. Les données sont pédagogiques et ne décrivent pas une substance à identifier.',
    'Proposer une nouvelle masse à tester entre les deux essais qui encadrent la limite.'
],('pc_dissolve',None),'L’encadrement suppose une agitation suffisante et une température constante.',[
    'Que peut-on affirmer de la masse maximale qui se dissout dans 50 g d’eau ?',
    'Quel nouvel essai permettrait de préciser l’encadrement ?',
    'Pourquoi ne faut-il pas changer la température pendant la comparaison ?'
], 'La masse maximale dissoute est au moins égale à 15 g et inférieure à 20 g, dans les conditions données. Tester par exemple 17 g ou 18 g avec 50 g d’eau à la même température précise l’encadrement. Changer la température modifierait une autre variable susceptible de changer la limite ; la comparaison ne porterait plus seulement sur la masse ajoutée.'),[
    'Une solution contient un solvant et un ou plusieurs solutés.',
    'Dissolution et fusion sont deux phénomènes différents.',
    'La masse se conserve pendant une dissolution sans perte de matière.',
    'Une solution saturée ne peut plus dissoudre davantage de soluté dans les conditions données.',
    'Deux liquides non miscibles forment des phases distinctes après repos.'
], '« Agiter plus fort permet de dissoudre une quantité illimitée. » L’agitation peut accélérer la dissolution, mais ne supprime pas la saturation.',[
E(1,'Le vocabulaire de la solution',['On dissout du sucre dans l’eau. Nomme le solvant et le soluté.','Comment nomme-t-on le mélange homogène obtenu ?'],'L’eau est le solvant ; le sucre est le soluté. On obtient une solution aqueuse de sucre. Le mot aqueuse précise que le solvant est l’eau.'),
E(2,'Dissoudre ou fondre ?',['Un glaçon devient liquide au-dessus de 0 °C. Est-ce une dissolution ?','Du sel se disperse dans l’eau sans rester visible. Quel phénomène se produit ?'],'Le glaçon subit une fusion, changement d’état de l’eau. Le sel subit une dissolution dans l’eau, qui joue le rôle de solvant. Une dissolution n’est pas définie par le passage du solide au liquide.'),
E(3,'Lire les récipients',['Quel récipient montre un dépôt persistant ?','Que signifie « solution saturée » ?'],'Le dernier récipient montre un dépôt. Une solution saturée contient la quantité maximale de soluté qui peut être dissoute dans les conditions étudiées, après un temps et une agitation suffisants.',figure=('pc_dissolve',None)),
E(4,'Deux liquides au repos',['Eau et huile donnent deux couches après repos. Sont-elles miscibles ?','Le mélange est-il homogène ou hétérogène à l’œil nu ?'],'Elles sont non miscibles dans ces conditions. Le mélange est hétérogène, car on distingue deux phases liquides.'),
E(5,'La substance invisible',['« Le sel n’est plus visible, donc la solution ne contient que de l’eau. » Corrige cette phrase.'],'Le sel reste présent sous forme dissoute, même si ses cristaux ne sont plus visibles. La solution contient de l’eau et du sel : c’est un mélange homogène.'),
E(6,'Conserver la masse',['On mélange 80 g d’eau et 12 g de sucre sans perte. Calcule la masse de solution.','Quel type de grandeur additionnes-tu ?'],'La masse de solution est 80 + 12 = 92 g. On additionne des masses exprimées dans la même unité, pas des volumes.',check='80+12==92'),
E(7,'Retrouver la masse du soluté',['Une solution a une masse de 125 g. Elle a été préparée avec 110 g d’eau. Quelle masse de soluté a été ajoutée ?','Quelle hypothèse utilises-tu ?'],'125 - 110 = 15 g de soluté ont été ajoutés. On suppose qu’il n’y a eu aucune perte ni aucun autre ajout et que le mélange ne contient que ces constituants.',check='125-110==15'),
E(8,'Ne changer qu’un facteur',['Pour comparer l’effet de l’agitation, Léa utilise 50 mL d’eau froide et 100 mL d’eau chaude. Son protocole convient-il ?','Propose une correction.'],'Non : volume et température changent en plus de l’agitation. Utiliser la même substance, la même masse de solide, le même volume d’eau, la même température et des récipients comparables ; seul le mode d’agitation diffère.'),
E(9,'Encadrer une limite',['Quelle masse maximale dissoute peut-on encadrer ?','Propose un quatrième essai utile.'],'La limite est au moins 12 g et inférieure à 16 g pour 40 g d’eau, à cette température. Tester par exemple 14 g, avec les mêmes conditions, affine l’encadrement.',document='Pour 40 g d’eau à température fixée : 8 g dissous ; 12 g dissous ; 16 g avec un dépôt persistant après agitation suffisante.'),
E(10,'Une masse totale avec un dépôt',['On ajoute 25 g d’un solide à 60 g d’eau. Une partie reste au fond. Quelle masse totale contient le récipient, sans perte ?','Cette masse est-elle celle de la seule phase liquide ?'],'La masse totale du contenu est 85 g. Elle inclut la solution et le dépôt. La masse de la seule phase liquide ne peut pas être obtenue en affirmant que les 25 g se sont tous dissous.',check='60+25==85'),
E(11,'Comparer deux volumes de solvant',['Une substance peut se dissoudre jusqu’à 18 g dans 50 g d’eau. Dans les mêmes conditions, quelle masse correspond à 100 g d’eau ?','Quelle hypothèse permet ce calcul ?'],'100 g d’eau représentent deux fois 50 g : la masse maximale correspondante est 36 g. On suppose que les conditions sont identiques et que la limite dissoute est proportionnelle à la quantité de solvant, pour cette substance.',check='18*2==36'),
E(12,'Le dépôt disparaît lentement',['Juste après ajout du sucre, un dépôt est visible. Dix minutes plus tard, il a disparu. Pouvait-on conclure immédiatement à la saturation ?','Quelle précaution de langage adopter ?'],'Non. Le dépôt pouvait seulement traduire une dissolution inachevée. Il faut observer après une durée et une agitation suffisantes. On écrit « un dépôt est encore visible à cet instant », puis on conclut avec les observations finales.'),
E(13,'Choisir le mot précis',['Une élève écrit « l’huile est insoluble, donc l’eau est un mauvais liquide ». Reformule scientifiquement.','Pourquoi doit-on nommer les deux liquides ?'],'On dit que l’eau et l’huile sont non miscibles dans les conditions de l’essai. La propriété concerne un couple de substances, pas une qualité générale de l’eau. Un même liquide peut se mélanger différemment avec des liquides différents.'),
E(14,'Calculer la masse dissoute',['On ajoute 22 g de X à 50 g d’eau. Après saturation, 4 g de solide sec restent non dissous. Quelle masse a été dissoute ?','Quelle est la masse de la solution séparée du dépôt, sans perte ?'],'22 - 4 = 18 g ont été dissous. La phase liquide contient 50 + 18 = 68 g. Le système entier contenait 72 g avant séparation ; les 4 g restants appartiennent au dépôt.',check='22-4==18 and 50+18==68'),
E(15,'Le volume ne s’additionne pas toujours',['Deux liquides miscibles de volumes 50 mL et 50 mL donnent 97 mL de mélange. Y a-t-il forcément eu une perte de matière ?','Quelle mesure permettrait de contrôler une éventuelle perte ?'],'Non : le volume du mélange n’est pas toujours la somme des volumes initiaux. Une pesée avant et après mélange dans un système adapté permet de contrôler la conservation de la masse. On ne déduit pas une perte de matière de la seule baisse de volume.')
],Defi('Obtenir une solution sans dépôt',
    'À température fixée, au maximum 12 g d’un solide X se dissolvent dans 40 g d’eau. On a versé 18 g de X dans 40 g d’eau. Sans chauffer ni retirer de solide, quelle quantité minimale d’eau faut-il ajouter pour pouvoir tout dissoudre ?',
    ('pc_dissolve',None),['Calcule la masse d’eau nécessaire pour 18 g de X.','Déduis la masse d’eau à ajouter.','Explique comment vérifier le résultat expérimentalement.'],
    '18 g représentent une fois et demie 12 g ; garder la même proportion entre soluté et eau.',
    'Il faut 40 × 1,5 = 60 g d’eau au total. Ajouter au minimum 20 g d’eau aux 40 g initiaux. Agiter suffisamment à température constante et vérifier la disparition du dépôt. La valeur théorique est une limite ; les mesures ont une précision finie.'))

C6=Chapitre(6,'Comment récupérer du sel et de l’eau séparément ?',[
    'Choisir décantation ou filtration pour un mélange hétérogène.',
    'Distinguer évaporation et distillation selon le constituant recherché.',
    'Décrire un protocole et ses limites, notamment pour la potabilité.'
],[
Lecon('Laisser reposer puis séparer',
    'La décantation consiste à laisser un mélange hétérogène au repos pour que les phases se séparent. Des particules solides peuvent se déposer au fond ; des liquides non miscibles peuvent former des couches. On peut ensuite prélever une phase avec précaution. La décantation ne retire pas les substances dissoutes dans l’eau et ne garantit pas l’élimination des particules les plus fines.',
    ('pc_decant',None),'Une partie des particules se dépose pendant le repos ; l’eau surnageante peut rester imparfaitement limpide.',
    'Un liquide plus limpide n’est pas nécessairement pur ni potable. La séparation doit répondre à un objectif annoncé.',
    'Avant de choisir la méthode, repérer le nombre de phases et l’état des constituants. Laisser le dépôt au fond lorsque l’on prélève le liquide.'),
Lecon('Filtrer un mélange hétérogène',
    'Une filtration utilise une barrière poreuse, par exemple un papier-filtre. Les particules suffisamment grosses restent sur le filtre : elles constituent le résidu. Le liquide qui traverse est le filtrat. Le sel dissous traverse un papier-filtre ordinaire avec l’eau ; il ne forme pas des cristaux bloqués dans le filtre. La filtration sépare selon des propriétés et des tailles, pas selon la dangerosité des substances.',
    ('pc_filter',None),'Le liquide recueilli est le filtrat ; les particules retenues forment le résidu.',
    'Filtrer de l’eau salée ne permet pas, à lui seul, de retirer le sel dissous. Un filtre scolaire n’est pas un dispositif garantissant la potabilité.',
    'Nommer les récipients et les produits recueillis. Verser doucement avec un montage stable, sans remplir le filtre au-delà de son bord.'),
Lecon('Récupérer le soluté ou le solvant',
    'Pour récupérer un solide dissous non volatil, on peut laisser évaporer le solvant ; le solide demeure. Pour récupérer aussi le solvant, on utilise une distillation : une partie du liquide se vaporise, puis sa vapeur se liquéfie dans un réfrigérant. Le liquide recueilli est le distillat. Au collège, les montages avec chauffage sont réalisés uniquement selon les consignes du professeur.',
    ('pc_distill',None),'Distillation simplifiée d’eau salée : le sel reste dans le récipient chauffé ; l’eau se vaporise puis se liquéfie.',
    'Évaporer permet de récupérer le sel, mais laisse partir l’eau dans l’air. Distiller organise une récupération de l’eau après deux changements d’état.',
    'Préciser ce que l’on cherche à récupérer. Une méthode de séparation ne prouve pas que l’eau obtenue répond à tous les critères sanitaires.')
],Activite('Séparer un mélange à trois constituants',
    'Proposer un enchaînement pour un mélange d’eau, de sel dissous et de sable.',[
    'Identifier les constituants visibles et ceux qui restent dissous. Préparer un schéma de chaque étape.',
    'Avec le professeur, filtrer pour séparer le sable. Étiqueter résidu et filtrat.',
    'Sur une petite partie du filtrat, observer l’évaporation de l’eau selon le protocole de classe. Ne jamais goûter les produits.'
],('pc_filter',None),'Après filtration, le filtrat contient encore de l’eau et du sel dissous.',[
    'Quel constituant se trouve sur le filtre ?',
    'Quel constituant solide récupère-t-on après évaporation du filtrat ?',
    'Quelle étape remplacer pour récupérer de l’eau liquide au lieu de la laisser partir ?'
], 'Le sable est principalement retenu dans le résidu ; le filtrat est de l’eau salée. L’évaporation du filtrat laisse le sel non volatil. Pour recueillir l’eau liquide, le professeur peut remplacer l’évaporation simple par une distillation avec refroidissement et liquéfaction de la vapeur. Les pertes et les contaminations doivent être prises en compte.'),[
    'La décantation sépare des phases après repos.',
    'La filtration donne un résidu et un filtrat.',
    'Un soluté dissous traverse habituellement le papier-filtre avec le solvant.',
    'L’évaporation laisse un solide dissous non volatil.',
    'La distillation permet de recueillir un liquide après vaporisation puis liquéfaction.'
], '« L’eau est transparente après filtration, donc on peut la boire. » La transparence ne garantit ni la pureté chimique ni la potabilité.',[
E(1,'Choisir une technique',['Pour séparer du sable et de l’eau, propose une méthode utilisant un filtre.','Comment appelle-t-on le liquide recueilli ?'],'On réalise une filtration. Le liquide qui traverse le filtre est le filtrat ; le sable retenu forme le résidu.'),
E(2,'Nommer les produits',['Associe résidu et filtrat aux éléments du schéma.','Quel rôle joue le papier-filtre ?'],'Le résidu solide est sur le papier-filtre ; le filtrat est dans le récipient inférieur. Le papier retient les particules assez grosses pour ne pas traverser ses pores.',figure=('pc_filter',None)),
E(3,'Laisser reposer',['Une eau boueuse devient plus limpide au-dessus d’un dépôt. Quelle méthode commence-t-on à utiliser ?','Le dépôt s’est-il dissous ?'],'On utilise une décantation. Le dépôt provient de particules qui se sont rassemblées au fond ; il ne prouve pas une dissolution.'),
E(4,'Récupérer du sel',['Quelle opération peut laisser le sel après départ de l’eau d’une solution salée ?','L’eau partie dans l’air a-t-elle disparu ?'],'L’évaporation de l’eau laisse le sel non volatil. L’eau est passée dans l’air à l’état gazeux ; elle n’a pas disparu.'),
E(5,'Deux changements successifs',['Dans une distillation, nomme le passage du liquide à la vapeur puis de la vapeur au liquide.'],'Il s’agit d’abord d’une vaporisation, puis d’une liquéfaction. Le réfrigérant favorise le refroidissement et la liquéfaction de la vapeur.'),
E(6,'Un filtre face au sel',['Un élève filtre une eau salée limpide. Le filtrat contient-il encore du sel ?','Explique pourquoi.'],'Oui. Le sel dissous est dispersé dans l’eau et traverse le papier-filtre ordinaire avec elle. La filtration scolaire ne sépare pas les espèces dissoutes de cette manière.'),
E(7,'Comparer deux objectifs',['Tu veux récupérer le sel d’une eau salée. Quelle méthode simple choisir ?','Tu veux récupérer l’eau sous forme liquide. Quelle méthode choisir ?'],'Pour le sel, une évaporation adaptée convient. Pour récupérer l’eau liquide, choisir une distillation, avec liquéfaction de la vapeur et collecte du distillat.'),
E(8,'Lire un montage',['Où le liquide se vaporise-t-il ?','Quel est le rôle du réfrigérant ?'],'Le liquide se vaporise dans le récipient chauffé à gauche. Le réfrigérant retire de l’énergie à la vapeur et permet sa liquéfaction. Le distillat est recueilli à droite.',figure=('pc_distill',None)),
E(9,'Une séparation en deux étapes',['Pour séparer eau, sable et sel dissous, quelle méthode utiliser d’abord ?','Que contient encore le filtrat ?'],'Filtrer d’abord pour retenir le sable. Le filtrat contient l’eau et le sel dissous ; il faut une autre étape, comme l’évaporation ou la distillation, selon le constituant recherché.'),
E(10,'Le résultat de l’évaporation',['Après évaporation complète, on récupère 7,5 g de solide. Quelle masse minimale de substance non volatile était présente dans l’échantillon ?','Quelle hypothèse faut-il faire pour parler de toute la masse initialement dissoute ?'],'Il y avait au moins 7,5 g de substance récupérée. Pour assimiler ce résultat à toute la masse initialement dissoute, il faut supposer une récupération complète, sans perte ni transformation du solide et sans contamination.'),
E(11,'Des volumes de distillat',['Un montage recueille 45 mL d’eau sur les 60 mL initialement présents. Combien de millilitres n’ont pas été recueillis ?','Peut-on affirmer qu’ils ont été détruits ?'],'60 - 45 = 15 mL n’ont pas été recueillis, en comparant les volumes à conditions équivalentes. Ils peuvent rester dans le montage ou être perdus sous forme de vapeur ou de liquide. Rien ne permet d’affirmer une destruction de l’eau.',check='60-45==15'),
E(12,'Filtrer avant ou après ?',['Un filtre est bouché rapidement par beaucoup de boue. Quelle étape préalable peut aider ?','Pourquoi le résultat doit-il encore être contrôlé ?'],'Une décantation peut retirer une grande partie du dépôt avant filtration du liquide surnageant. Des particules fines et des substances dissoutes peuvent néanmoins rester ; le résultat dépend de l’objectif et du filtre.'),
E(13,'Un mot trompeur',['Une publicité nomme « eau pure » une eau simplement filtrée. Quelle question scientifique poser ?','Propose une formulation plus précise.'],'Demander quelles substances et quelles particules ont réellement été retirées, avec quel dispositif et quels contrôles. On peut écrire « eau filtrée avec tel dispositif » sans affirmer une pureté chimique totale.'),
E(14,'Éviter une mauvaise conclusion',['Un filtrat est incolore. Donne deux types de constituants qui peuvent encore être présents.','Pourquoi ne doit-on pas le goûter ?'],'Il peut contenir des espèces dissoutes et des particules ou micro-organismes non retenus par le dispositif. L’aspect ne garantit pas l’absence de danger ; un échantillon de laboratoire ne se goûte jamais.'),
E(15,'Construire un protocole complet',['Décris une suite d’opérations pour obtenir du sable sec et du sel à partir d’eau salée contenant du sable.','Cite une limite de récupération.'],'Filtrer ; récupérer le sable retenu et le sécher selon le protocole. Faire évaporer le filtrat pour obtenir le sel, puis le sécher si nécessaire. Une partie du sel peut rester sur le sable humide, et des pertes peuvent avoir lieu lors des transferts. Les produits ne sont pas déclarés purs sans contrôle.')
],Defi('Une mini-chaîne de séparation',
    'Un mélange contient de l’eau, du sel dissous, du sable et quelques morceaux de liège qui flottent. Tu dois proposer une suite d’étapes pour récupérer séparément le liège, le sable et le sel. Le matériel et le chauffage sont gérés par le professeur.',
    ('pc_filter',None),['Ordonne les opérations en expliquant le rôle de chacune.','Précise ce qui se trouve dans le filtrat.','Propose une adaptation pour récupérer aussi l’eau.'],
    'Commencer par retirer les morceaux faciles à prélever ; séparer ensuite les particules, puis les espèces dissoutes.',
    'Retirer le liège par prélèvement adapté. Filtrer pour retenir le sable, puis sécher les solides selon les consignes. Le filtrat est une solution salée ; son évaporation permet de récupérer le sel. Pour récupérer l’eau, utiliser une distillation plutôt qu’une évaporation simple. Signaler les pertes et les limites de pureté.'))

C7=Chapitre(7,'Toute apparition de bulles révèle-t-elle une réaction chimique ?',[
    'Distinguer mélange, changement d’état et transformation chimique.',
    'Exploiter un test caractéristique fourni avec ses limites.',
    'Raisonner sur la conservation de la masse dans un ensemble fermé.'
],[
Lecon('Reconnaître une nouvelle espèce',
    'Une transformation chimique consomme certaines espèces, les réactifs, et en forme d’autres, les produits. Un changement d’état conserve la nature des espèces ; un mélange n’implique pas à lui seul la formation de nouvelles espèces. Une couleur qui change, une apparition de gaz ou un dépôt constituent des indices à examiner. Ils ne suffisent pas toujours : l’eau qui bout forme des bulles sans devenir une autre substance.',
    ('pc_reaction',None),'Un gaz se forme et peut être recueilli ; son identification apporte une information supplémentaire.',
    'La conclusion doit s’appuyer sur la présence de nouvelles espèces, avec des observations et des tests adaptés. On ne décide pas uniquement à partir d’un effet spectaculaire.',
    'Décrire l’état initial et l’état final, puis comparer les espèces présentes. Écrire « cet indice est compatible avec… » si l’identification reste incomplète.'),
Lecon('Utiliser une banque de tests',
    'Un test caractéristique relie une observation à la présence d’une espèce dans des conditions précisées. Dans les situations de ce livre, de l’eau de chaux initialement limpide se trouble en présence de dioxyde de carbone. Une banque peut aussi indiquer que du sulfate de cuivre anhydre blanc devient bleu en présence d’eau. Ce second test est présenté comme document et manipulé uniquement par le professeur avec les précautions adaptées.',
    ('pc_lime',None),'Test du dioxyde de carbone dans les conditions scolaires fournies : apparition d’un trouble blanc.',
    'Un test positif indique une présence ; il ne démontre pas que l’échantillon est pur. Un résultat négatif s’interprète avec la sensibilité et les conditions du test.',
    'Rédiger trois étapes : j’observe le résultat ; je cite le test de la banque ; j’en déduis la présence de l’espèce recherchée.'),
Lecon('Compter toute la matière',
    'Lors d’une transformation chimique dans un ensemble fermé, la masse totale se conserve. Un gaz formé fait partie des produits et doit être compté. Dans un récipient ouvert, il peut partir dans l’air : la masse du contenu restant diminue sans contredire la conservation. Une combustion est un exemple de transformation chimique qui consomme un combustible et du dioxygène ; certains combustibles produisent notamment du dioxyde de carbone.',
    ('pc_reaction',None),'Le gaz est retenu par un ballon souple adapté, sous le contrôle du professeur. Ne jamais enfermer une production de gaz dans un récipient rigide bouché.',
    'Une conservation de masse ne signifie pas que les espèces restent les mêmes. Une nouvelle espèce peut apparaître tout en conservant la masse totale.',
    'Définir le système pesé et rechercher toute entrée ou sortie de matière. Une combustion utilise aussi un réactif provenant de l’air, le dioxygène.')
],Activite('Une enquête à partir d’un gaz',
    'Comparer deux documents pour identifier une transformation.',[
    'Document A : de l’eau bout ; la vapeur refroidie redonne de l’eau liquide. Document B : du vinaigre réagit avec de l’hydrogénocarbonate de sodium et un gaz se forme.',
    'Dans l’essai B réalisé par le professeur, le gaz mis en contact avec de l’eau de chaux initialement limpide produit un trouble blanc.',
    'Utiliser la banque de tests pour distinguer ce qui est observé, ce qui est identifié et ce qui peut être conclu.'
],('pc_lime',None),'Documents d’expériences encadrées ; aucun test avec une flamme n’est demandé.',[
    'Quel gaz est mis en évidence dans le document B ?',
    'Pourquoi les bulles du document A ne prouvent-elles pas une transformation chimique ?',
    'Rédige une conclusion argumentée sur les deux situations.'
], 'Dans B, le trouble de l’eau de chaux indique la présence de dioxyde de carbone dans le gaz testé. L’apparition de cette espèce, dans la réaction donnée, étaye une transformation chimique. Dans A, l’eau change d’état et redevient liquide au refroidissement : la vaporisation n’est pas une transformation chimique. Des bulles seules ne suffisent donc pas pour trancher.'),[
    'Une transformation chimique forme de nouvelles espèces.',
    'Les espèces consommées sont les réactifs ; les espèces formées sont les produits.',
    'Un test caractéristique s’utilise avec une banque et des conditions données.',
    'Un test positif ne prouve pas la pureté d’un échantillon.',
    'Dans un ensemble fermé, la masse totale se conserve, gaz compris.'
], '« La masse baisse, donc la matière est détruite. » Vérifier d’abord si un gaz ou un liquide a quitté le système pesé.',[
E(1,'Nommer réactif et produit',['Dans une transformation, comment nomme-t-on une espèce consommée ?','Comment nomme-t-on une espèce formée ?'],'Une espèce consommée est un réactif. Une espèce formée est un produit. Une espèce présente avant et après ne doit pas être déclarée consommée sans information supplémentaire.'),
E(2,'Trois situations',['Classe : fusion d’un glaçon ; mélange de sable et d’eau ; formation de rouille sur du fer.'],'La fusion est un changement d’état ; sable et eau forment un mélange ; la formation de rouille correspond à une transformation chimique, car de nouvelles espèces se forment.'),
E(3,'Un test fourni',['L’eau de chaux se trouble au contact d’un gaz. Quelle présence indique la banque de tests du cours ?','Le gaz est-il forcément pur ?'],'Le test indique la présence de dioxyde de carbone dans les conditions fournies. Il ne prouve pas que le gaz est pur : d’autres gaz peuvent être présents.'),
E(4,'Des bulles sans réaction',['Donne un exemple de formation de bulles qui ne constitue pas une transformation chimique.','Explique ton choix.'],'L’ébullition de l’eau est un exemple : les bulles contiennent de la vapeur d’eau. L’espèce eau est conservée ; son état physique change.'),
E(5,'Rendre compte d’un test',['Écris une phrase complète d’identification à partir du schéma.'],'J’observe que l’eau de chaux initialement limpide se trouble. D’après la banque de tests, ce résultat indique que le gaz testé contient du dioxyde de carbone.',figure=('pc_lime',None)),
E(6,'Peser un ensemble fermé',['Avant mélange, l’ensemble fermé pèse 152,0 g. Un gaz se forme sans fuite. Quelle masse attend-on après ?','Que doit-on inclure dans la pesée ?'],'On attend environ 152,0 g, dans la précision de la balance. Il faut peser tout le même ensemble, y compris le récipient et le dispositif qui retient le gaz.'),
E(7,'Un gaz qui part',['Un récipient ouvert passe de 98,4 g à 97,8 g pendant une réaction. Quelle masse a quitté le système si seul le gaz s’échappe ?','Pourquoi cette condition est-elle importante ?'],'98,4 - 97,8 = 0,6 g ont quitté le système sous forme de gaz. Si une éclaboussure ou une autre perte se produit, la baisse ne peut pas être attribuée au seul gaz.',check='984-978==6'),
E(8,'Interpréter un test de l’eau',['Un document indique : poudre anhydre blanche avant le test, bleue après contact avec un liquide. Quelle présence cela met-il en évidence selon la banque ?','Peut-on conclure « ce liquide est uniquement de l’eau » ?'],'Le test fourni met en évidence la présence d’eau. Il ne prouve pas que le liquide est uniquement de l’eau ; une solution contenant d’autres espèces peut aussi donner ce résultat.'),
E(9,'Un ballon qui gonfle',['Pourquoi placer un ballon souple adapté sur le récipient dans une expérience encadrée ?','Quel mauvais montage faut-il éviter ?'],'Le ballon peut recueillir le gaz et permettre d’inclure sa masse dans l’ensemble pesé. Éviter de produire un gaz dans un récipient rigide hermétiquement bouché : la pression pourrait augmenter dangereusement. Le professeur choisit le montage.'),
E(10,'Le rôle de l’air',['Une combustion utilise un combustible. Quel autre réactif de l’air est habituellement nécessaire ?','Pourquoi faut-il en tenir compte dans un bilan de masse ?'],'Le dioxygène de l’air est un réactif de la combustion. Sa masse fait partie de la matière initiale consommée ; ignorer les échanges avec l’air conduit à un bilan incomplet.'),
E(11,'Présence ou absence ?',['Un test ne montre aucun changement visible. Peut-on conclure à une absence absolue de l’espèce ?','Cite une vérification utile.'],'Pas nécessairement : l’espèce peut être trop peu abondante pour la sensibilité du test, ou le protocole peut être inadapté. Vérifier le réactif, les quantités et les conditions, par exemple avec un témoin positif adapté fourni par le professeur.'),
E(12,'Un changement de couleur',['Un colorant rouge se disperse dans l’eau et tout le liquide devient rose. La nouvelle couleur suffit-elle à prouver une réaction ?','Quelle autre interprétation proposer ?'],'Non. La dilution ou la dispersion du colorant peut expliquer l’aspect rose sans nouvelle espèce. Il faut rechercher d’autres indices ou des tests qui montrent une transformation de la composition chimique.'),
E(13,'Une conclusion trop large',['« L’eau de chaux est trouble, donc le flacon ne contient que du dioxyde de carbone. » Corrige la conclusion.','Quelle observation doit précéder la conclusion ?'],'On conclut que le gaz contient du dioxyde de carbone dans les conditions du test. Il faut avoir observé le passage d’une eau de chaux initialement limpide à un trouble, selon le protocole fourni. La pureté n’est pas démontrée.'),
E(14,'Comparer ouvert et fermé',['Dans A, le gaz s’échappe ; dans B, il reste retenu. Quelle masse est conservée dans chaque situation ?','Quelle masse la balance compare-t-elle réellement ?'],'La masse totale de toute la matière se conserve dans les deux situations. Dans A, la balance ne pèse plus le gaz parti dans l’air ; dans B, elle pèse encore l’ensemble fermé. La différence concerne les limites du système mesuré.'),
E(15,'Une preuve construite',['Propose un raisonnement pour distinguer l’ébullition de l’eau et la production de dioxyde de carbone par une réaction.','Pourquoi faut-il éviter le seul critère « je vois des bulles » ?'],'Décrire les substances initiales, recueillir ou analyser le gaz par les tests fournis et comparer les espèces finales. L’eau vaporisée peut redonner de l’eau par liquéfaction ; un gaz contenant du dioxyde de carbone trouble l’eau de chaux. Les bulles indiquent seulement une phase gazeuse, pas son identité ni son mode de formation.')
],Defi('Le mystère des 1,2 gramme',
    'Un document annonce une baisse de 1,2 g dans un récipient ouvert pendant une réaction qui dégage un gaz. Un autre groupe obtient la même masse avant et après avec un dispositif fermé adapté. Les deux groupes s’accusent d’avoir faux.',
    ('pc_reaction',None),['Explique comment les deux résultats peuvent être compatibles.','Précise la masse du gaz parti si aucune autre perte n’a eu lieu.','Propose deux contrôles pour améliorer la comparaison.'],
    'Dessiner la frontière du système réellement posé sur la balance.',
    'Les deux résultats peuvent être cohérents : dans le système ouvert, 1,2 g de gaz ont quitté l’ensemble pesé ; dans le système fermé, le gaz est encore inclus. Contrôler l’absence de fuite ou d’éclaboussure, utiliser le même ensemble avant et après, vérifier la stabilité et la précision de la balance. La matière n’a pas été détruite.'))

C8=Chapitre(8,'Comment représenter des distances aussi grandes ?',[
    'Distinguer étoile, planète et satellite naturel.',
    'Se repérer dans le Système solaire et distinguer rotation et révolution.',
    'Lire des distances astronomiques et construire une échelle simple.'
],[
Lecon('Notre place dans le Système solaire',
    'Le Soleil est une étoile : il émet sa propre lumière. Les huit planètes tournent autour de lui et diffusent la lumière qu’elles reçoivent. Dans l’ordre d’éloignement moyen : Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus et Neptune. La Lune est un satellite naturel de la Terre. Le Système solaire comprend aussi des planètes naines, des astéroïdes et des comètes ; il appartient à la galaxie appelée Voie lactée.',
    ('pc_solar',None),'Représentation d’ordre : les tailles, les intervalles et les positions ne respectent pas une échelle commune.',
    'Le Soleil n’est pas une planète. La Lune n’est pas une étoile et ne produit pas la lumière visible qu’elle nous renvoie.',
    'Distinguer le nom de l’objet, sa catégorie et l’astre autour duquel il se déplace. Ne pas lire une distance sur une illustration annoncée sans échelle.'),
Lecon('Rotation, révolution et alternance jour-nuit',
    'La Terre tourne sur elle-même : c’est sa rotation. Elle effectue aussi une révolution autour du Soleil en environ une année. L’alternance du jour et de la nuit est liée à la rotation terrestre : à un instant donné, le Soleil éclaire approximativement une moitié de la Terre. Une durée proche de 24 h décrit un jour solaire ; ces ordres de grandeur suffisent ici pour distinguer les mouvements.',
    ('pc_daynight',None),'La moitié tournée vers le Soleil est éclairée ; l’autre est dans la nuit. Les tailles et distances ne sont pas à l’échelle.',
    'Le Soleil ne s’éteint pas chaque soir. Un lieu terrestre passe progressivement de la partie éclairée à la partie non éclairée.',
    'Pour expliquer le jour et la nuit, faire tourner un globe devant une lampe fixe. Ne pas confondre ce mouvement avec la révolution annuelle.'),
Lecon('Choisir une échelle de distance',
    'Les distances du Système solaire s’expriment souvent en millions de kilomètres. La distance moyenne Terre-Soleil est voisine de 150 millions de kilomètres ; elle donne le repère d’environ une unité astronomique (ua). Une représentation à l’échelle utilise le même rapport pour toutes les distances représentées. Une échelle pratique pour les planètes proches devient vite trop grande pour inclure Neptune sur une feuille.',
    ('pc_solar_scale',None),'Distances moyennes arrondies depuis le Soleil : Mercure 58, Vénus 108, Terre 150, Mars 228 millions de km.',
    'Une distance moyenne au Soleil n’est pas une distance fixe entre deux planètes. Leurs positions varient au cours de leurs révolutions.',
    'Si 1 cm représente 50 millions de km, la Terre est placée à 150 ÷ 50 = 3 cm du Soleil. Appliquer le même coefficient à tous les objets du modèle.')
],Activite('Une maquette sur une bande de papier',
    'Placer les quatre planètes internes à une même échelle de distance.',[
    'Utiliser les distances moyennes arrondies : 58, 108, 150 et 228 millions de km pour Mercure, Vénus, Terre et Mars.',
    'Choisir 1 cm pour 50 millions de km et calculer la position de chaque planète depuis le Soleil.',
    'Tracer une ligne, placer le Soleil à l’origine et reporter les distances calculées. Les disques des planètes servent seulement de repères.'
],('pc_solar_scale',None),'Le schéma du livre emploie une échelle graphique ; ta maquette utilise celle annoncée dans l’activité.',[
    'À quelles distances du Soleil places-tu les quatre repères ?',
    'Jupiter est à environ 780 millions de km du Soleil. Tiendrait-il sur une bande de 20 cm ?',
    'Pourquoi faut-il préciser que les diamètres dessinés ne sont pas à cette échelle ?'
], 'Les positions sont 1,16 cm ; 2,16 cm ; 3,00 cm ; 4,56 cm. Jupiter serait à 15,6 cm et tient sur une bande de 20 cm. Les diamètres réels, à cette échelle des distances, seraient trop petits pour être lisibles : les disques sont agrandis pour repérer les planètes. Le modèle ne prétend donc pas respecter simultanément l’échelle des tailles.'),[
    'Le Soleil est l’étoile du Système solaire.',
    'Huit planètes gravitent autour de lui ; la Lune est un satellite de la Terre.',
    'La rotation de la Terre explique l’alternance du jour et de la nuit.',
    'La révolution de la Terre autour du Soleil dure environ une année.',
    'Une échelle doit être annoncée et appliquée de manière identique aux distances.'
], '« Mars est à 228 millions de km de la Terre. » Cette valeur arrondie concerne sa distance moyenne au Soleil, pas sa distance à la Terre.',[
E(1,'Classer les astres',['Classe le Soleil, la Terre et la Lune : étoile, planète ou satellite naturel.'],'Le Soleil est une étoile ; la Terre une planète ; la Lune un satellite naturel de la Terre. Ces catégories n’indiquent pas simplement la taille des objets.'),
E(2,'Retrouver l’ordre',['Nomme les quatre planètes les plus proches du Soleil dans l’ordre.','Quelle planète vient après Mars ?'],'Mercure, Vénus, Terre et Mars. Jupiter vient ensuite. L’ordre est celui des distances moyennes au Soleil.'),
E(3,'Identifier la source de lumière',['Pourquoi voit-on la Lune lorsqu’elle est éclairée ?','Est-elle une source primaire de lumière visible ?'],'La Lune diffuse une partie de la lumière solaire reçue. Elle n’est pas une source primaire de lumière visible dans ce modèle ; c’est un objet diffusant.'),
E(4,'Rotation ou révolution ?',['Quel mouvement explique l’alternance jour-nuit ?','Quel mouvement terrestre dure environ une année ?'],'L’alternance jour-nuit est liée à la rotation terrestre. La révolution de la Terre autour du Soleil dure environ une année.'),
E(5,'Lire une représentation',['Peut-on mesurer une distance réelle avec une règle sur ce dessin ?','Quelle indication l’empêche ?'],'Non. Le dessin indique un ordre et annonce des tailles et distances non à l’échelle. Sans échelle de distance, une mesure sur la page n’est pas convertible en distance réelle.',figure=('pc_solar',None)),
E(6,'Une unité de distance',['Écris 150 millions de km en kilomètres.','Cette valeur mesure-t-elle une durée ?'],'150 millions de km = 150 000 000 km. C’est une distance, pas une durée. Elle sert ici de repère approximatif pour la distance moyenne Terre-Soleil.'),
E(7,'Placer la Terre',['À l’échelle 1 cm pour 50 millions de km, à quelle distance du Soleil placer la Terre ?','Précise l’unité de la mesure sur la feuille.'],'150 ÷ 50 = 3 cm sur la feuille. La valeur 3 n’est pas exprimée en millions de km : elle décrit la maquette.',check='150/50==3'),
E(8,'Placer Mars',['À la même échelle, calcule la position de Mars, située à 228 millions de km du Soleil.','Est-elle plus de quatre fois plus loin que le repère d’un centimètre ?'],'228 ÷ 50 = 4,56 cm. Oui : 4,56 cm dépassent 4 cm, qui représentent 200 millions de km.',check='228/50==4.56'),
E(9,'Jour et nuit',['Explique pourquoi deux lieux très éloignés peuvent être au jour et dans la nuit au même instant.','Faut-il que le Soleil s’éteigne pour produire la nuit ?'],'À un même instant, les lieux peuvent être sur les moitiés éclairée et non éclairée de la Terre. Le Soleil reste lumineux ; c’est l’orientation du lieu terrestre par rapport à lui qui change avec la rotation.',figure=('pc_daynight',None)),
E(10,'Comparer des distances',['La Terre est à environ 150 millions de km du Soleil, Jupiter à 780 millions. Combien de fois la seconde distance représente-t-elle la première ?','Cette comparaison donne-t-elle la distance Terre-Jupiter ?'],'780 ÷ 150 = 5,2 fois. Non : la séparation entre les deux planètes dépend de leurs positions sur leurs orbites. Les distances données sont chacune mesurées depuis le Soleil.',check='780/150==5.2'),
E(11,'Lire un repère en ua',['On donne 1 ua ≈ 150 millions de km. Une distance de 3 ua correspond à combien de millions de km ?','Pourquoi utiliser ce repère ?'],'3 × 150 = 450 millions de km environ. L’unité astronomique permet d’exprimer plus simplement certaines distances dans le Système solaire.',check='3*150==450'),
E(12,'Le modèle trop petit',['Neptune est à environ 4 500 millions de km du Soleil. Quelle longueur faut-il à l’échelle 1 cm pour 50 millions de km ?','Une feuille de 21 cm de large suffit-elle ?'],'4 500 ÷ 50 = 90 cm. Une feuille de 21 cm de large ne suffit pas ; il faut une bande plus longue ou une autre échelle.',check='4500/50==90'),
E(13,'Une échelle incohérente',['Un élève place la Terre à 3 cm pour 150 millions de km et Mars à 3 cm pour 228 millions de km. Pourquoi la maquette est-elle fausse ?','Comment corriger Mars ?'],'Il n’applique pas le même rapport aux distances. Avec 1 cm pour 50 millions de km, Mars doit être à 4,56 cm du Soleil. Une même longueur sur la maquette doit représenter la même distance réelle partout.'),
E(14,'Relier plusieurs mouvements',['Une personne assise dans son jardin semble immobile. Cite deux mouvements qu’elle accompagne à l’échelle astronomique.','Pourquoi faut-il préciser l’observateur ?'],'Elle accompagne la rotation terrestre et la révolution de la Terre autour du Soleil. Son repos est relatif au jardin ; un autre observateur peut décrire d’autres mouvements. La description dépend du repère choisi.'),
E(15,'Évaluer une source',['Un document mélange planètes et étoiles dans une liste sans date ni auteur. Quels contrôles effectuer avant de l’utiliser ?','Cite un organisme pertinent pour vérifier les informations.'],'Vérifier les catégories, l’auteur, la date, les unités et les sources des données ; comparer avec une source reconnue. Le CNES ou un observatoire astronomique peut fournir des repères fiables. Une image attractive ne garantit pas l’exactitude scientifique.')
],Defi('Le Système solaire dans la cour',
    'Tu disposes d’une longueur de 45 m pour placer Neptune, à environ 4 500 millions de km du Soleil. Tu souhaites une seule échelle pour toutes les distances. Terre : 150 millions de km ; Mars : 228 millions de km ; Jupiter : 780 millions de km.',
    ('pc_solar',None),['Quelle distance réelle doit représenter 1 m dans la cour ?','Place la Terre, Mars et Jupiter à cette échelle.','Explique pourquoi les diamètres des planètes devront être traités séparément.'],
    'Diviser la distance de Neptune par 45 ; utiliser ensuite la même proportion pour chaque planète.',
    '1 m représente 100 millions de km. La Terre est à 1,50 m, Mars à 2,28 m et Jupiter à 7,80 m du Soleil. Neptune est à 45 m. Les diamètres des planètes à cette échelle seraient minuscules ; employer des repères agrandis clairement annoncés, sans prétendre respecter l’échelle des tailles.'))

CHAPITRES_MATIERE=[C3,C4,C5,C6,C7,C8]
