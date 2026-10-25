"""Documents lisibles et corrections illustrées des dix sujets, question par question."""
# Énoncés : numéro de partie. Corrigés : numéro global de question (1 à 7).
ENONCES={
1:{2:('rev-bb1-comparaison','Données fictives pour le même trajet et le seul indicateur fourni.')},
2:{1:('rev-bb2-masse-ex','Distinguer récipient rempli et liquide seul.'),2:('rev-bb2-tests-ex','Utiliser les observations et la banque de tests du document.')},
3:{1:('rev-bb3-ex','Deux commandes indépendantes ; interrupteurs fermés pour les mesures.')},
6:{1:('rev-bb6-sonar-ex','Le délai de 0,080 s comprend les deux trajets dans l’eau.')},
7:{1:('rev-bb7-enonce','Les lectures de 30,0 et 50,0 mL correspondent au déplacement de 20,0 mL annoncé.')},
8:{1:('rev-bb8-solaire-ex','Repérer les instants de changement de puissance.')},
9:{2:('rev-bb9-grav-ex','Distance entre centres ; aucune taille n’est à l’échelle.')},
10:{2:('rev-bb10-transfos-ex','Deux transformations différentes peuvent produire des bulles.')},
}
CORRIGES={
1:{2:('rev-bb1-corrige','La pente représente la distance parcourue par unité de temps.'),5:('cor-reaction-methane','Quatre atomes d’oxygène de chaque côté.')},
2:{2:('rev-bb2-masse-cor','Soustraire la masse du récipient avant le quotient.'),7:('rev-bb2-tests-cor','Un test négatif ne prouve pas une absence absolue.')},
3:{3:('rev-bb3-cor','V aux bornes de L1 ; A dans la branche de L2. Chaque interrupteur reste en série avec sa lampe.'),6:('rev-bb3-batterie','Comparer réserve et consommation dans la même unité.')},
4:{3:('rev-bb4-forces','Deux forces de 19,2 N appliquées à l’équipement ; dessin sans échelle.'),6:('rev-bb4-radio-cor','Chaque trajet mesure 384 000 km ; durée totale : 2,56 s.')},
5:{3:('rev-cor-corrosion','La présence de rouille ne donne pas à elle seule une vitesse.'),5:('rev-cor-atome-fe2','26 protons et 24 électrons : charge +2.'),7:('rev-bb5-reaction','Les ions H+ sont consommés ; le pH augmente sans atteindre la neutralité.')},
6:{3:('rev-bb6-sonar-cor','120 m parcourus au total ; profondeur : 60 m.'),6:('rev-bb6-energie','Convertir la durée avant le produit avec la puissance.')},
7:{1:('rev-bb7-corrige','50 − 30 = 20 cm³ ; 54 / 20 = 2,70 g/cm³.'),3:('rev-bb7-atome','Inventaire symbolique des constituants de l’atome neutre décrit ; aucune échelle de taille.'),5:('rev-bb7-bilan','5,0 MJ = 3,5 MJ utiles + 1,5 MJ vers le milieu.')},
8:{3:('rev-bb8-solaire-cor','L’aire du rectangle donne l’énergie : W × h = Wh.'),6:('rev-bb8-lampes','Chaque lampe fonctionne 500 h ; économie : 16 kWh.')},
9:{3:('rev-bb9-lumiere','La distance en années-lumière indique le retard en années.'),7:('rev-bb9-grav-cor','Chaque corps subit 1,334 × 10⁸ N à la distance initiale ; les deux forces s’appliquent à deux systèmes différents.')},
10:{3:('rev-bb10-ohm-cor','R = 200 ohms ; P = 0,080 W, inférieure à 0,25 W.'),7:('rev-bb10-transfos-cor','Le test au CO2 renforce l’interprétation chimique de B ; les bulles seules ne suffisent pas.')},
}
DEMARCHES={
1:[
r'Comparer les déplacements sur des durées égales, dans le référentiel de la route annoncé.',
r'Lire les extrémités : $\Delta x=200-0\unite m$ et $\Delta t=40-0\unite s$ ; le quotient donne des m/s.',
r'Employer kg et m/s ; mettre 5 au carré avant le produit. Doubler v multiplie son carré par quatre.',
r'Le méthane est le combustible ; le dioxygène joue ici le rôle de comburant.',
r'Le coefficient multiplie toute la molécule : $2\,\ce{O2}$ contient $2\times2$ atomes O ; $2\,\ce{H2O}$ en contient $2\times1$.',
r'kWh × g/kWh donne g ; diviser ensuite par 1 000 pour obtenir kg.',
r'Commencer par 1,0 kg contre 4,0 kg, puis préciser le périmètre et un impact que l’indicateur ne mesure pas.'],
2:[
r'La balance a pesé le récipient et le liquide : soustraire la masse du récipient.',
r'Former $\rho=m/V$ avec la masse du liquide seul ; g et mL donnent g/mL.',
r'Les espèces dissoutes concernent la pureté ; les critères sanitaires concernent la potabilité. Donner les deux arguments.',
r'Comparer 6 à 7 ; la proximité avec 7 ne suffit pas à conclure à la neutralité.',
r'Croiser réactif et couleur du précipité avec la banque de tests ; la couleur initiale du liquide ne remplace pas le test.',
r'Cl⁻ conserve le même noyau que Cl et gagne un électron : $17+1=18$.',
r'Prévoir prélèvements séparés, témoin et conditions comparables ; conclure en tenant compte de la limite de détection.'],
3:[
r'Repérer les deux nœuds communs ; chaque lampe est directement reliée à la source par des interrupteurs fermés supposés idéaux.',
r'Les courants sont déjà en ampères : appliquer l’additivité des intensités au nœud.',
r'Insérer A dans la branche de L2 hors tension ; relier les deux bornes de V aux deux bornes de L1. A ne se branche pas seul aux bornes de la source.',
r'Avec W et h, $E=P\Delta t$ donne des Wh.',
r'Multiplier par $3\,600\unite{J/Wh}$ ; on retrouve le résultat avec $6\times(4\times3\,600)$.',
r'Isoler $\Delta t=E/P$ ; Wh divisés par W donnent h. Contrôler $6\times6=36\unite{Wh}$.',
r'Associer une limite à une hypothèse du modèle, puis une économie à $E=P\Delta t$ ; réduire la durée est aussi pertinent.'],
4:[
r'La masse caractérise l’équipement ; g et le poids changent avec le lieu.',
r'Choisir $g_L$ ; kg × N/kg donne N. La valeur terrestre ne convient pas ici.',
r'Nommer les auteurs des actions sur l’équipement : Lune et sol. Dans ce modèle d’équilibre à deux forces, valeurs égales et sens opposés.',
r'Le signal radio est un rayonnement électromagnétique ; un son demande un milieu matériel.',
r'Écrire $\Delta t=d/c$ ; les puissances $10^8$ se simplifient et l’unité obtenue est s.',
r'Additionner deux trajets de 1,28 s ; ne pas diviser de nouveau une durée calculée pour un aller simple.',
r'Expliquer la chute commune ; remplacer ensuite d par 2d : $(2d)^2=4d^2$, donc F est divisée par quatre.'],
5:[
r'La formation de nouvelles espèces distingue cette transformation chimique d’un changement d’état.',
r'B et D contiennent de l’eau ; le facteur comparé est la disponibilité du dioxygène.',
r'Une observation oui/non ne quantifie pas « deux fois plus vite ». Mesurer une quantité sur une durée avec répétitions et contrôles.',
r'Lire les produits à droite de l’équation : H₂ désigne le dihydrogène.',
r'La charge $2+$ signifie deux électrons en moins que l’atome neutre ; Z ne change pas.',
r'Le pH augmente, mais sa valeur finale 4 reste inférieure à 7.',
r'Relier les observations aux espèces de l’équation, puis distinguer cette réaction de la formation de rouille dans l’air humide.'],
6:[
r'Kilo signifie mille. Le classement ultrasonore porte sur la fréquence, sans renseigner un niveau en décibels.',
r'Utiliser la vitesse dans l’eau et la durée totale de 0,080 s pour la longueur totale parcourue.',
r'Écrire $2h=v\Delta t$ ; les deux trajets ont la même longueur dans le modèle annoncé.',
r'En courant continu, $P=UI$ : V × A donne W.',
r'Multiplier par 60 : chaque minute contient 60 secondes.',
r'W × s donne J ; ne pas conserver 20 minutes comme si c’étaient 20 secondes.',
r'Distinguer hauteur, niveau et durée ; justifier les mesures par la réduction du niveau reçu ou du temps d’exposition.'],
7:[
r'$V=50-30=20\unite{mL}=20\unite{cm^3}$. Diviser 54 g par ce volume pour obtenir 2,70 g/cm³.',
r'Comparer dans la même unité et à température comparable ; formuler une compatibilité, pas une preuve absolue d’identité.',
r'Z compte les protons, A les protons et neutrons. Dans l’atome neutre demandé, le nombre d’électrons égale Z.',
r'Le document exclut toute nouvelle espèce : la fusion est physique dans ce modèle.',
r'Sans stockage ni autre sortie, soustraire l’énergie utile de l’entrée. Vérifier $3{,}5+1{,}5=5{,}0\unite{MJ}$.',
r'Un changement d’état sans perte ni réaction conserve la masse.',
r'Préciser où l’énergie est transférée, puis citer un besoin concret du recyclage. Un transfert thermique ne disparaît pas.'],
8:[
r'Distinguer apport par rayonnement et sortie électrique ; les autres transferts réels restent dans le bilan.',
r'Lire la largeur du palier : $14-10=4\unite h$ ; 14 h est l’heure de fin, pas la durée.',
r'La puissance constante permet $E=P\Delta t$. Diviser les Wh par 1 000 pour obtenir les kWh.',
r'Soustraire les puissances pour le même service : $\Delta P=40-8=32\unite W$.',
r'La durée vaut $5\times100=500\unite h$ ; convertir 32 W en 0,032 kW avant le produit en kWh.',
r'kWh × euros/kWh donne des euros ; ce coût concerne le seul poste fourni.',
r'Relier éclairement et puissance disponible, puis ajouter un critère comme durée de vie ou qualité de lumière.'],
9:[
r'L’année-lumière est la distance parcourue par la lumière en un an ; elle reste une unité de distance.',
r'Multiplier la distance d’une année-lumière par quatre ; conserver puissance de dix et unité km.',
r'La planète diffuse la lumière reçue. Les quatre ans de retard concernent la distance étoile-observateur fournie.',
r'La force sur chaque corps est dirigée vers l’autre corps : l’interaction est attractive.',
r'Les données sont en SI ; mettre la distance au carré avec sa puissance de dix : $(10^6)^2=10^{12}$.',
r'Remplacer d par 3d donne F/9 ; utiliser la valeur non arrondie avant de diviser.',
r'Identifier le corps qui reçoit chaque force ; une compensation demanderait des forces appliquées au même système.'],
10:[
r'Il faut une droite et le passage par l’origine ; une droite décalée ne suffit pas pour une proportionnalité.',
r'Choisir un point hors origine, avec I en A ; le quotient U/I donne des ohms.',
r'Calculer P au même point de fonctionnement ; comparer 0,080 W à 0,25 W dans la même unité.',
r'Nommer le passage liquide vers gaz ; l’ébullition se produit dans le volume du liquide.',
r'La conclusion vient du test à l’eau de chaux, pas des seules bulles.',
r'La masse sortie vaut masse initiale moins masse finale dans les hypothèses du système ouvert.',
r'Comparer les espèces avant et après ; proposer un témoin sans gaz ajouté et des conditions de test comparables.'],
}
METHODES={(n,j):t for n,ts in DEMARCHES.items() for j,t in enumerate(ts,1)}
assert len(METHODES)==70 and all(len(ts)==7 for ts in DEMARCHES.values())

def enrichir(sujets):
    for s in sujets:
        for k,p in enumerate(s.parties,1):
            if k in ENONCES.get(s.numero,{}):p.exercice.figure,p.exercice.legende_figure=ENONCES[s.numero][k]
    sujets[6].parties[0].exercice.document+=r' Les lectures sont 30,0 mL avant et 50,0 mL après immersion.'
