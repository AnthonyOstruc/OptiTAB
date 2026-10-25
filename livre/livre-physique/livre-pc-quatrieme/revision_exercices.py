"""Audit des figures utiles et compléments pédagogiques, exercice par exercice."""
ILLUSTRATIONS={}
def I(ids,enonce='',corrige='',legende='',solution='',exact=False,exact_correction=False):
    for ident in ids.split():
        assert ident not in ILLUSTRATIONS,ident
        ILLUSTRATIONS[ident]=dict(figure=enonce,figure_correction=corrige,legende_figure=legende,legende_correction=solution,figure_exacte=exact,correction_exacte=exact_correction)

I('1.3',enonce='ex-immersion',corrige='cor-immersion',legende='Lecture de deux volumes ; solide entièrement immergé.',solution='Le volume du solide est la différence des deux lectures, pas le volume final seul.')
I('1.8',enonce='ex-rho-points',corrige='cor-rho-points',solution='La droite passe par l’origine et les trois quotients sont identiques.')
I('1.11',corrige='cor-bulle',solution='La bulle augmente le volume apparent déplacé ; la masse du solide reste la même.')
I('1.12',corrige='cor-coque',solution='Le volume extérieur comprend la cavité ; il diffère du volume de métal.')
I('1.13',enonce='ex-tare-graphe',corrige='cor-tare-graphe',legende='Exemple de données illustrant une pesée sans tare.',solution='Soustraire la même masse de récipient à chaque mesure déplace toute la droite vers le bas.')
I('2.3',enonce='ex-compression',corrige='cor-compression',solution='Le récipient est étanche : le nombre de particules reste le même.')
I('2.10',enonce='ex-detente',corrige='cor-detente',legende='À droite, compléter le modèle après détente sans fuite.',solution='Même nombre et mêmes types de particules ; elles se répartissent dans un volume plus grand.')
I('2.15',enonce='ex-air-incorrect',corrige='cor-air',legende='Modèle proposé par l’élève, à critiquer.',solution='Schéma qualitatif : un gaz occupe tout le récipient et ses particules sont en mouvement ; les couleurs codent des espèces.')
I('3.6',enonce='ex-fusion',corrige='cor-fusion',solution='Au palier, deux états coexistent : le chauffage peut continuer sans hausse de température.')
I('3.8',enonce='ex-ebullition',corrige='cor-ebullition',solution='La première partie correspond au chauffage du liquide ; le palier à la vaporisation dans les conditions annoncées.')
I('3.10',enonce='ex-deux-courbes',corrige='cor-deux-courbes',legende='Deux mesures à pression constante ; la précision reste limitée.',solution='A est compatible avec un corps pur ; une courbe seule ne prouve pas l’identité et la pureté exactes.')
I('3.12',corrige='cor-glaces',solution='La glace continentale apporte de l’eau à l’océan lorsqu’elle fond et s’y écoule ; la banquise flottait déjà.')
I('3.13',enonce='ex-particules-grosses',corrige='cor-particules-chaudes',legende='Représentation de l’élève : les particules sont dessinées plus grosses après chauffage.',solution='Le modèle conserve les entités ; le chauffage modifie notamment leur agitation, sans les transformer en grosses molécules.')
I('4.2',enonce='ex-eau-huile',solution='Deux phases visibles après repos.')
I('4.4',corrige='cor-filtration',solution='Le filtre retient les grains de sable ; les espèces dissoutes traversent le filtre ordinaire avec l’eau.')
I('4.10',corrige='cor-distillation',solution='Vaporiser puis liquéfier pour recueillir l’eau ; une évaporation peut laisser le sel, sans recueillir l’eau.')
I('5.8',enonce='ex-case-aluminium',legende='Extrait de repérage du tableau périodique.')
I('5.9',enonce='ex-melange-molecules',corrige='cor-melange-molecules',solution='Chaque boule est un atome ; les boules liées forment une molécule. Compter séparément les deux espèces.')
I('5.10',enonce='ex-eau-modele',corrige='cor-eau-formule',legende='Les lettres identifient les atomes du modèle.',solution='L’indice 2 doit porter sur H : il y a deux H et un O.')
I('5.11',enonce='ex-inventaires',corrige='cor-inventaires',solution='Même inventaire de quatre H et deux O ; assemblages et espèces différents.')
I('5.12',corrige='cor-methane-jetons',solution='Le carbone permettrait six modèles ; l’hydrogène n’en permet que cinq : il limite la construction.')
I('6.7 6.11',corrige='cor-reaction-eau',solution='Les coefficients multiplient des molécules entières ; les indices des espèces restent inchangés.')
I('6.8',enonce='ex-temoin',corrige='cor-temoin',legende='Un seul tube reçoit le gaz étudié ; les autres conditions sont comparables.',solution='Le témoin recherche une cause de trouble indépendante de l’ajout de gaz.')
I('7.6',corrige='cor-reaction-methane',solution='Un C, quatre H et quatre O se retrouvent de chaque côté ; le nombre de molécules n’est pas imposé constant.')
I('7.9',corrige='cor-bougie-ouverte',solution='Le bilan doit inclure le dioxygène entrant et les produits gazeux sortants.')
I('7.13',corrige='cor-bilan-carbone-6',solution='Séparer matière transformée et réactif restant ; la masse finale totale comprend les deux.')
I('D7',corrige='cor-bilan-carbone-9',solution='Le dioxygène disponible limite ici le modèle de transformation complète ; inclure le carbone restant dans la masse finale.')
I('8.5',corrige='cor-echelle-astronomie',solution='Schéma réduit : les longueurs indiquées sont à reporter sur la frise. L’échelle relie chaque centimètre à dix millions de kilomètres ; les diamètres ne sont pas à l’échelle.')
I('8.10',corrige='cor-frise-750',solution='On divise la distance réelle par la distance représentée par un centimètre.')
I('D8',corrige='cor-frise-salle',solution='Une longueur totale de 900 cm représente 4 500 millions de kilomètres ; la Terre est à 30 cm du Soleil.')
I('9.1',corrige='cor-referentiels',solution='Le mouvement d’un même objet peut être décrit différemment selon le référentiel.')
I('9.3',enonce='ex-chronophoto',corrige='cor-chronophoto',legende='Les prises de vue sont séparées par une même durée.',solution='Comparer les distances entre positions successives, mesurées pour des durées égales.')
I('9.8',enonce='ex-position',corrige='cor-position',solution='Des distances de 3 m sont parcourues en 2 s ; la pente traduit une vitesse constante de 1,5 m/s.')
I('9.9',corrige='cor-manege',solution='Les flèches de vitesse sont tangentes au cercle : leur direction change même si leur valeur reste la même.')
I('9.14',enonce='ex-position-retour',corrige='cor-position-retour',legende='Exemple de position décroissant linéairement.',solution='Une position décroissante indique un sens de déplacement ; la valeur de la vitesse peut rester constante.')
I('10.5',corrige='cor-direction-sens',solution='Même direction verticale ; sens opposés. Les flèches représentent ici deux forces de même valeur, à titre d’exemple.')
I('10.6',corrige='cor-forces-echelle',solution='Longueurs à mesurer du point d’application à la pointe. Échelle conservée pour une impression à 100 %.',exact_correction=True)
I('10.7',enonce='ex-force-4cm',corrige='cor-force-4cm',legende='Flèche de 4 cm à l’impression à 100 % ; échelle : 1 cm pour 0,5 N.',solution='Quatre segments de 1 cm représentent chacun 0,5 N.',exact=True,exact_correction=True)
I('10.9',corrige='cor-livre-forces',solution='Le diagramme recense les partenaires ; les flèches représentent les actions sur le livre, dans le modèle immobile à deux forces.')
I('10.11',corrige='cor-main-boite',solution='Les deux actions de l’interaction s’appliquent à deux systèmes différents : elles ne se compensent pas sur la seule boîte.')
I('10.12',enonce='ex-suspension-incomplete',corrige='cor-suspension',legende='Bilan de forces proposé par l’élève, incomplet.',solution='Il faut ajouter le poids ; dans le modèle immobile à deux forces, les valeurs sont égales et les sens opposés.')
I('10.15',corrige='cor-systemes',solution='Une action devient interne quand les deux partenaires sont inclus dans le système choisi.')
I('D10',enonce='ex-objet-suspendu',corrige='cor-suspension-3N',solution='Chaque flèche mesure 2 cm à l’impression à 100 %. Les deux forces s’appliquent au même objet et se compensent dans ce modèle.',exact_correction=True)
I('11.4',corrige='cor-poids-20N',solution='Poids de 20 N, vertical vers le bas ; schéma qualitatif sans échelle de longueur.')
I('11.9',corrige='cor-terre-lune-5kg',solution='Même masse de 5 kg ; poids de 50 N et 8 N. Les longueurs des flèches respectent le même rapport.')
I('11.10',enonce='ex-poids-graphe',corrige='cor-poids-graphe',solution='Le quotient P/m vaut 10 N/kg ; le point prévu pour 0,45 kg est sur la même droite.')
I('11.13',enonce='ex-poids-decale',corrige='cor-poids-decale',legende='Exemple de relevé expérimental présentant un décalage de zéro.',solution='Un décalage constant de 0,3 N peut provenir de l’appareil ; contrôler le zéro avant de modifier le modèle.')
I('D11',corrige='cor-colis-lunaire',solution='Comparer deux poids ne change pas la masse ; les calibres doivent couvrir la force mesurée.')
I('12.6',corrige='cor-energie-lampe',solution='Sans stockage, la somme des transferts sortants égale le transfert entrant.')
I('12.7',corrige='cor-energie-moteur',solution='Le transfert mécanique peut être utile ; le transfert thermique ne disparaît pas du bilan.')
I('12.8',corrige='cor-energie-stockage',solution='Entrée − sorties = variation de stockage : entrée et sortie ne sont pas égales si le stockage change.')
I('12.9',corrige='cor-photovoltaique',solution='La lumière apporte de l’énergie par rayonnement ; la sortie électrique n’est pas la seule sortie réelle.')
I('D12',corrige='cor-convertisseur',solution='Le stockage de 80 J est déduit seulement si les transferts indiqués sont complets ; une sortie oubliée reste une autre hypothèse.')
I('13.1',enonce='ex-circuit-ouvert',corrige='cor-circuit-ouvert',solution='L’ouverture interrompt l’unique boucle ; on ne dessine pas un courant permanent à travers l’espace ouvert.')
I('13.2',corrige='cor-sens-courant',solution='Les flèches indiquent le sens conventionnel dans le circuit extérieur : de + vers −.')
I('13.3',enonce='ex-circuit-serie',corrige='cor-serie-ouverte',solution='Une ouverture dans la seule boucle interrompt le courant dans les deux lampes.')
I('13.4 13.6',enonce='ex-circuit-parallele',corrige='cor-branches',solution='Entre les mêmes deux nœuds : une branche de générateur et deux branches de lampes.')
I('13.7',corrige='cor-commandes',solution='Un interrupteur dans la branche L1 commande seulement L1 ; un interrupteur dans le trajet commun peut commander les deux.')
I('D13',corrige='cor-refuge',solution='L1 est directement alimentée ; seul l’interrupteur de la branche L2 commande L2.')
I('13.8 13.11',corrige='cor-branche-ouverte',solution='La branche L1 est ouverte ; L2 garde un trajet fermé vers la source, supposée adaptée et stable.')
I('13.9',enonce='ex-circuits-equivalents',corrige='cor-circuits-equivalents',solution='La position sur la feuille change, mais la même succession de dipôles relie les bornes de la source.')
I('13.10',enonce='ex-lampe-court-circuitee',corrige='cor-lampe-court-circuitee',legende='Schéma à analyser, sans réaliser le défaut.',solution='Le fil ajouté relie directement les bornes de L1 ; ne pas tester ce défaut sur une pile.')
I('13.14',corrige='cor-fil-commun',solution='L’indépendance des branches suppose que le générateur et les connexions communes fonctionnent.')
I('13.15',enonce='ex-circuit-parallele',corrige='cor-courants-paralleles',solution='Le courant principal se partage au nœud ; les lampes ne sont pas traversées successivement par le même courant.')
I('14.2',corrige='cor-amperemetre',solution='L’ampèremètre est inséré dans la branche étudiée ; couper l’alimentation avant de modifier le montage.')
I('14.4',corrige='cor-serie-012',solution='En régime permanent, même intensité avant et après la lampe dans cette unique branche.')
I('14.5',enonce='ex-noeud',corrige='cor-noeud',solution='La somme des courants entrants est égale à la somme des courants sortants.')
I('14.6',enonce='ex-courants-050',corrige='cor-courants-050',solution='Les intensités sont exprimées dans la même unité avant la soustraction.')
I('14.9',corrige='cor-amperemetre-inverse',solution='Le signe négatif provient de l’orientation de connexion retenue ; la valeur absolue est 0,15 A.')
I('14.12',enonce='ex-amperemetre-danger',corrige='cor-amperemetre',legende='Montage incorrect à analyser ; ne pas le réaliser.',solution='L’ampèremètre doit mesurer le courant d’une branche contenant le récepteur, pas relier seul les bornes de la pile.')
I('14.14',corrige='cor-courant-branche-ouverte',solution='La branche ouverte a une intensité nulle ; le courant principal est celui de la seule branche encore fermée.')
I('14.15',enonce='ex-trois-courants',corrige='cor-trois-courants',solution='Convertir 220 mA en 0,220 A ; soustraire les deux branches connues du courant principal.')
I('D14',enonce='ex-bilan-intensites',corrige='cor-bilan-intensites',solution='Le schéma relie chaque valeur à sa branche ; les mesures fournies ne respectent pas l’additivité dans leurs conditions affichées.')
I('15.2',corrige='cor-voltmetre',solution='Les deux bornes du voltmètre sont reliées aux deux bornes de la lampe : on n’ouvre pas la branche principale.')
I('15.3',corrige='cor-pile-isolee',solution='Une tension peut exister sans courant dans un circuit extérieur fermé.')
I('15.5',enonce='ex-tensions-45',corrige='cor-tensions-45',solution='Les lampes sont reliées aux mêmes deux nœuds : on ne divise pas la tension par le nombre de branches.')
I('15.6',enonce='ex-tensions-serie',corrige='cor-tensions-serie',solution='Dans cette boucle, les tensions des récepteurs se somment pour retrouver celle de la source.')
I('15.8',corrige='cor-voltmetre-inverse',solution='Inverser les pointes inverse le signe de la différence de potentiel mesurée, sans modifier sa valeur absolue.')
I('15.9',corrige='cor-interrupteur-ferme',solution='Dans le modèle idéal, un interrupteur fermé a une tension nulle et peut laisser passer un courant.')
I('15.11',corrige='cor-tensions-18-42',solution='La somme vaut 6 V ; la loi ne demande pas que deux récepteurs différents se partagent la tension à parts égales.')
I('15.12',enonce='ex-voltmetre-meme-noeud',corrige='cor-voltmetre-meme-noeud',solution='Les deux pointes sont sur le même conducteur idéal ; elles ne sont pas aux deux bornes de la lampe.')
I('15.14',enonce='ex-amperemetre-danger',corrige='cor-voltmetre',legende='Mode ampèremètre directement aux bornes de la source : montage à ne pas réaliser.',solution='Vérifier mode tension, bornes V/COM et calibre avant de relier le voltmètre en dérivation.')
I('15.15',corrige='cor-serie-derivation-6V',solution='Deux tensions positives de 6 V ne peuvent pas s’ajouter pour donner une source de 6 V ; la dérivation directe est compatible.')
I('D15',corrige='cor-serie-derivation-9V',solution='En A : 3 V + 6 V = 9 V ; en B, chaque récepteur reçoit les 9 V de la source.')
I('16.5',enonce='ex-ohm-modele',corrige='cor-ohm-modele',legende='Repère à compléter qualitativement ; aucune valeur de résistance n’est imposée.',solution='La proportionnalité se reconnaît à la droite passant par l’origine, dans les conditions du modèle.')
I('16.8',enonce='ex-ohm-150',corrige='cor-ohm-150',solution='Les points donnent 150 ohms ; le point prévu pour 0,040 A correspond à 6,0 V.')
I('16.11',enonce='ex-lampe-courbe',corrige='cor-lampe-courbe',legende='Exemple de caractéristique non linéaire dans une plage donnée.',solution='La pente globale n’est pas constante ; utiliser le point de fonctionnement, sans imposer une résistance constante.')
I('16.12',enonce='ex-ohm-point-suspect',corrige='cor-ohm-point-suspect',legende='Droite : modèle de 100 ohms ; croix rouge : relevé à vérifier.',solution='La valeur de 5 V à 0,030 A est comparée à la prévision du modèle de 100 ohms, pas effacée sans enquête.')
I('16.13',corrige='cor-ohmmetre',solution='Résistance déconnectée de toute alimentation ; isoler si nécessaire le dipôle des autres branches.')
I('D16',enonce='ex-ohm-boite',corrige='cor-ohm-boite',solution='La prévision à 5 V reste dans la plage mesurée ; elle ne justifie pas une extrapolation à 100 V.')
I('17.11',corrige='cor-puissance-duree',solution='Comparer des énergies exige de tenir compte à la fois de la puissance et de la durée.')
I('18.2',enonce='ex-vision',corrige='cor-vision',legende='Orienter le segment entre feuille et œil.',solution='La lumière reçue par l’œil vient de la feuille éclairée ; l’œil n’émet pas le rayon nécessaire à cette vision.')
I('18.5',corrige='cor-ombre',solution='L’objet opaque intercepte une partie des rayons issus de la source ponctuelle du modèle.')
I('18.8',corrige='cor-lune-trajets',solution='L’aller-retour parcourt deux fois la distance Terre-Lune.')
I('18.11',enonce='ex-echo-lumineux',corrige='cor-echo-lumineux',solution='La durée mesurée couvre deux trajets de longueur d : d = cΔt/2.')
I('18.12',enonce='ex-ecrans',corrige='cor-ecrans',legende='Même source et même objet ; deux positions possibles de l’écran.',solution='Prolonger les rayons passant par les bords de l’objet : l’ombre grandit quand l’écran s’éloigne.')
I('18.13',corrige='cor-diffusion',solution='Voir le trajet de côté demande que de la lumière soit diffusée vers l’œil.')
I('D18',corrige='cor-miroir-spatial',solution='720 000 km est la longueur totale ; la séparation est la moitié.')
I('19.7',enonce='ex-echo-sonore',corrige='cor-echo-sonore',solution='Le son parcourt 170 m au total ; la paroi est à 85 m.')
I('19.8',enonce='ex-huit-motifs',corrige='cor-huit-motifs',solution='On compte huit motifs complets dans 20 ms, soit 0,020 s ; ne pas confondre nombre de crêtes et nombre d’intervalles.')
I('19.10',enonce='ex-sonar',corrige='cor-sonar',solution='La durée est celle d’un aller-retour dans l’eau : la vitesse fournie est 1 500 m/s.')
I('19.11',enonce='ex-meme-periode',corrige='cor-meme-periode',solution='Même durée d’un motif, donc même fréquence et même hauteur pour ces sons simples ; amplitudes différentes.')
I('19.13',corrige='cor-echo-030',solution='102 m représente le trajet aller-retour ; la distance à la paroi est 51 m.')
I('19.14',corrige='cor-echo-retard',solution='Retirer le retard instrumental d’abord ; seule la durée de propagation corrigée sert à calculer la distance.')
I('D19',corrige='cor-deux-milieux',solution='Même durée d’aller-retour, vitesses différentes : les deux distances ne sont pas égales.')
I('20.9',enonce='ex-etalonnage',corrige='cor-etalonnage',solution='Une droite qui ne passe pas par l’origine n’exprime pas une proportionnalité entre U et T.')
I('20.10',corrige='cor-etalonnage-lecture',solution='Enlever d’abord la tension de décalage, puis diviser par le coefficient 0,020 V/°C.')
I('20.13',enonce='ex-hors-plage',corrige='cor-hors-plage',legende='La zone colorée correspond au seul domaine étalonné.',solution='125 °C est un résultat d’extrapolation, pas une mesure validée par l’étalonnage 0–50 °C.')
I('20.15',corrige='cor-analogique-numerique',solution='L’exemple montre des prélèvements et des arrondis prévus par le dispositif, pas des fautes humaines.')
I('D20',corrige='cor-protocole-phare',solution='Un début plus long et une séparation convenue distinguent le silence d’un message 00 ; ici, un exemple avec le message 01.')

METHODES={
'1.3':r'On mesure le volume \emph{ajouté} par le solide : $V=V_f-V_i=57-42=15\unite{mL}=15\unite{cm^3}$. Vérifier immersion complète, absence de bulle et insolubilité.',
'1.5':r'Commencer par $\rho=m/V$ ; avec g et mL, on obtient g/mL. $32/40=0{,}80\unite{g/mL}$ ; comparer ensuite à $1{,}00\unite{g/mL}$ pour l’eau dans les conditions usuelles.',
'1.6':r'Isoler la masse : $m=\rho V=2{,}7\times30=81\unite g$. À même matériau et même température, doubler V double m ; le quotient m/V ne change pas.',
'1.7':r'Partir de $m=\rho V$, donc $V=m/\rho$. Les unités g et g/cm³ donnent cm³ : $79/7{,}9=10\unite{cm^3}=10\unite{mL}$.',
'1.8':r'Calculer les trois quotients : $9/10=18/20=27/30=0{,}90$. Leur unité est g/mL. L’alignement sur une droite passant par l’origine est une autre lecture de la même proportionnalité.',
'1.10':r'$0{,}85\unite{g/mL}=850\unite{kg/m^3}$. Convertir aussi le volume : $2\unite L=2\,000\unite{mL}$, puis $m=0{,}85\times2\,000=1\,700\unite g=1{,}7\unite{kg}$.',
'1.11':r'La masse mesurée séparément ne change pas. Si le dénominateur V est trop grand, le quotient m/V est trop petit : la masse volumique est sous-estimée.',
'1.13':r'Le modèle d’une pesée sans tare est $m_{\text{mesurée}}=m_{\text{récipient}}+\rho V$. À V nul, l’ordonnée n’est donc pas nulle. Soustraire $m_{\text{récipient}}$ rétablit la masse du liquide.',
'1.14':r'Une même erreur de lecture représente une plus petite fraction d’un grand volume déplacé. Pour dix billes identiques : $V_{\text{bille}}=40/10=4\unite{mL}$. Vérifier que toutes sont immergées et sans bulle.',
'1.15':r'Avant : $\rho_1=200/200=1{,}00\unite{g/mL}$. Après : $\rho_2=200/204\approx0{,}980\unite{g/mL}$. La masse est conservée mais un volume plus grand diminue le quotient.',
'2.6':r'Une proportion de 21 % signifie $21/100$ du volume total : $2\times21/100=0{,}42\unite L$. Pour le diazote : $2\times78/100=1{,}56\unite L$.',
'2.9':r'Soustraire les masses du même ballon : $425{,}6-423{,}2=2{,}4\unite g$. Puis $V=m/\rho=2{,}4/1{,}2=2\unite L$, avec les conditions de température et de pression annoncées.',
'3.6':r'Le palier ne signifie pas arrêt du transfert d’énergie : l’énergie reçue permet la fusion pendant la coexistence solide-liquide. La pression et la précision de la mesure font partie de l’interprétation.',
'3.8':r'Lire successivement les portions de la courbe : température croissante, puis constante. Un palier vers 100 °C est compatible avec l’ébullition de l’eau pure à pression usuelle ; la valeur seule ne suffit pas sans les conditions.',
'4.6':r'À température et solvant identiques, la limite fournie donne $20\times250/100=50\unite g$. Sur les 60 g ajoutés, au plus 50 g se dissolvent ; un dépôt d’environ 10 g persiste dans ce modèle.',
'4.8':r'La masse maximale est au moins 14 g, mais strictement inférieure à 16 g dans les conditions de l’essai. Pour un volume d’eau double : au moins 28 g et moins de 32 g. Les essais ne donnent pas une valeur exacte à eux seuls.',
'5.6':r'Le coefficient 5 multiplie toute la formule CO2 : $5\times1=5$ atomes C et $5\times2=10$ atomes O, donc 15 atomes au total.',
'5.7':r'Une molécule N2O contient deux N et un O. Trois molécules contiennent $3\times2=6$ N et $3\times1=3$ O. L’indice ne doit pas être confondu avec le coefficient.',
'5.12':r'Chaque modèle CH4 demande un C et quatre H. Les maxima sont $6/1=6$ et $20/4=5$ ; retenir le plus petit. Cinq modèles utilisent 5 C et 20 H : il reste un C.',
'6.11':r'Changer H2O en H2O2 change le produit : on obtient une autre espèce. Il faut modifier les coefficients : deux H2 et un O2 donnent deux H2O, soit quatre H et deux O de chaque côté.',
'7.7':r'Conservation de masse dans le bilan complet : $m_1+m_2=m_{\text{produit}}$. D’où $m_2=22-6=16\unite g$. Le calcul suppose les deux réactifs entièrement consommés et aucun échange non compté.',
'7.8':r'$m_{\text{dioxygène}}=44-12=32\unite g$. Le produit est plus lourd que le carbone seul parce qu’il contient aussi la matière apportée par le dioxygène.',
'7.10':r'Passer de 3 g à 9 g de carbone multiplie les masses du bilan par trois : 24 g de dioxygène et 33 g de produit. Le bilan chimique utilise O2 ; l’air contient aussi d’autres gaz.',
'7.13':r'Les 6 g de carbone demandent $6\times8/3=16\unite g$ de dioxygène. Sur 24 g, il en reste 8 g ; le produit formé pèse $6+16=22\unite g$. Contrôle : $22+8=6+24=30\unite g$.',
'9.4':r'Choisir $v=d/\Delta t$ avec d en m et la durée en s : $v=40/8=5\unite{m/s}$. Il s’agit de la moyenne sur le trajet, sauf information supplémentaire.',
'9.5':r'$1\unite{m/s}=3{,}6\unite{km/h}$. Multiplier par 3,6 vers km/h et diviser vers m/s : 36 km/h et 20 m/s.',
'9.7':r'Pour une vitesse moyenne fournie, $\Delta t=d/v=1{,}8/6=0{,}30\unite h$. Puis $0{,}30\times60=18\unite{min}$ ; 0,30 h ne signifie pas 30 min.',
'9.11':r'Additionner d’abord distances et durées : $v_{\text{moy}}=(60+60)/(1+2)=40\unite{km/h}$. La moyenne arithmétique de 60 et 30 km/h ne convient pas car les durées sont différentes.',
'9.12':r'La durée totale vaut $30\unite{min}=0{,}50\unite h$ ; $v_{\text{moy}}=12/0{,}50=24\unite{km/h}$. La vitesse pendant les dix minutes d’arrêt vaut zéro.',
'9.14':r'La pente est négative parce que le mobile se déplace vers des positions plus petites. La droite a une pente de valeur constante : dans cet exemple rectiligne, cela ne traduit pas un ralentissement.',
'10.6':r'Chaque segment de 1 cm représente 2 N. La longueur vaut donc $\ell=F/2$ en cm : 3 cm pour 6 N et 0,5 cm pour 1 N. Mesurer du point de départ à la pointe, sans changer l’échelle entre les deux flèches.',
'10.7':r'Chaque centimètre vaut 0,5 N, donc $F=4\times0{,}5=2\unite N$. Une autre échelle change le dessin, pas la force physique représentée.',
'10.9':r'Choisir d’abord le livre comme système. Le diagramme recense Terre et table. Le bilan des forces garde seulement les actions \emph{sur le livre}, et non celles exercées par le livre sur ses partenaires.',
'10.11':r'La main agit sur la boîte et la boîte agit sur la main. Les receveurs diffèrent : le bilan mécanique de la boîte contient l’action de la main, mais pas l’action reçue par la main.',
'10.12':r'Le poids n’est pas supprimé par l’immobilité. Dans le modèle à deux forces, la tension du fil compense le poids : même direction et même valeur, sens opposés.',
'11.6':r'Convertir d’abord $80\unite g=0{,}080\unite{kg}$. Alors $P=mg=0{,}080\times10=0{,}80\unite N$. Employer 80 à la place de 0,080 produirait une valeur 1 000 fois trop grande.',
'11.7':r'De $P=mg$, déduire $m=P/g=35/10=3{,}5\unite{kg}$ ; puis convertir en 3 500 g. Le poids en N n’est pas une masse en kg.',
'11.8':r'La relation donne $g=P/m=4{,}9/0{,}50=9{,}8\unite{N/kg}$. Le quotient compare des newtons à des kilogrammes ; son unité n’est pas N seule.',
'11.10':r'Les trois quotients P/m valent 10 N/kg. Le modèle est donc $P=10m$ dans la plage étudiée ; pour 0,45 kg, on obtient 4,5 N.',
'12.6':r'Écrire le bilan avant de soustraire : $E_{\text{entrée}}=E_{\text{utile}}+E_{\text{autres}}$ sans stockage. Les autres transferts valent $200-60=140\unite J$. Contrôle : $60+140=200\unite J$.',
'12.8':r'La conservation s’écrit ici $\Delta E_{\text{stockée}}=E_{\text{entrée}}-E_{\text{sortie}}=80-30=50\unite J$. Ce n’est pas une disparition des 50 J : le système les stocke en plus.',
'13.7':r'Suivre un trajet fermé pour chaque lampe. Placer l’interrupteur dans le trajet propre à L1 ne coupe pas celui de L2 ; le placer dans le fil commun interrompt les deux trajets.',
'13.9':r'La forme du fil peut être déformée sans changer le circuit tant que ses connexions restent les mêmes. Repérer les bornes de chaque dipôle puis suivre la boucle dans les deux dessins.',
'14.6':r'Au nœud, $I_G=I_1+I_2$. Isoler $I_2=I_G-I_1=0{,}50-0{,}18=0{,}32\unite A$. Contrôle : $0{,}18+0{,}32=0{,}50\unite A$.',
'14.7':r'Employer une seule unité : $0{,}25\unite A=250\unite{mA}$. Puis $I_2=600-250=350\unite{mA}=0{,}350\unite A$.',
'14.11':r'La somme mesurée vaut $0{,}122+0{,}176=0{,}298\unite A$ ; l’écart à 0,300 A est 0,002 A, soit 2 mA. Comparer cet écart à la précision et à la stabilité des mesures avant de conclure.',
'14.15':r'Convertir $220\unite{mA}=0{,}220\unite A$. $I_3=0{,}80-0{,}220-0{,}35=0{,}23\unite A$ ; contrôle : $0{,}220+0{,}35+0{,}23=0{,}80\unite A$.',
'15.6':r'Dans la boucle étudiée, $U_G=U_1+U_2$. Donc $U_2=9-4=5\unite V$ ; on retrouve bien 9 V en additionnant les tensions des récepteurs.',
'15.11':r'En série, la loi impose la somme : $1{,}8+4{,}2=6{,}0\unite V$. Un partage égal ne peut être ajouté sans hypothèse supplémentaire sur les dipôles.',
'15.13':r'$U_1+U_2=2{,}51+3{,}49=6{,}00\unite V$, soit un écart de 0,02 V à la source mesurée. Cet écart se discute avec l’appareil et les conditions, pas avec le seul nombre de décimales affiché.',
'16.6':r'De $U=RI$, isoler $I=U/R=6/200=0{,}030\unite A=30\unite{mA}$. Vérifier : $200\times0{,}030=6\unite V$.',
'16.7':r'Convertir $20\unite{mA}=0{,}020\unite A$, puis $R=U/I=4{,}0/0{,}020=200\unite\Omega$. Le calcul 4/20 oublie le changement d’unité et donne un résultat 1 000 fois trop petit.',
'16.8':r'Les quotients $1{,}5/0{,}01$, $3/0{,}02$ et $4{,}5/0{,}03$ valent tous 150 ohms. Prévoir ensuite $U=150\times0{,}04=6\unite V$, sans confondre lecture d’un point et coefficient de la droite.',
'16.11':r'Pour l’exemple dessiné, U/I vaut 10 ohms au point (0,050 A ; 0,50 V), mais 25 ohms au point (0,200 A ; 5,0 V). Ce quotient variable interdit de décrire toute la courbe par une unique résistance constante.',
'16.12':r'Le modèle de 100 ohms prévoit $U=100\times0{,}030=3\unite V$. Le relevé 5 V est à vérifier : appareil, unité, transcription ou conditions de température peuvent être en cause.',
'17.2':r'À puissance constante, $E=P\Delta t=5\times1=5\unite{Wh}$. Puis $1\unite{Wh}=3\,600\unite J$ : $E=5\times3\,600=18\,000\unite J$.',
'17.7':r'Convertir d’abord 30 min en 0,50 h : $E=60\times0{,}50=30\unite{Wh}=0{,}030\unite{kWh}$. En SI, 30 min = 1 800 s et $E=60\times1\,800=108\,000\unite J$.',
'17.8':r'Isoler la durée : $\Delta t=E/P=180/6=30\unite s$. L’unité J/W donne des secondes ; le contrôle $6\times30=180\unite J$ retrouve l’énergie reçue.',
'17.11':r'Convertir les durées avant de comparer : 1 min = 60 s et 20 min = 1 200 s. A reçoit 6 000 J, B 12 000 J. La plus grande puissance ne suffit donc pas à désigner la plus grande énergie.',
'17.13':r'Calculer successivement $I=U/R=5/100=0{,}050\unite A$, puis $P=UI=5\times0{,}050=0{,}25\unite W$. La limite 0,125 W est dépassée d’un facteur deux : ne pas réaliser ce fonctionnement.',
'18.7':r'$\Delta t=d/c=150\,000\,000/300\,000=500\unite s$. Comme $500=8\times60+20$, cela représente 8 min 20 s. Il s’agit d’un trajet simple Soleil-Terre.',
'18.11':r'Distance totale : $c\Delta t=300\,000\times0{,}004=1\,200\unite{km}$. Le réflecteur est à la moitié : $d=600\unite{km}$. Les unités km/s et s donnent des km.',
'19.7':r'Le produit $340\times0{,}50=170\unite m$ donne le trajet complet. La paroi est à $d=170/2=85\unite m$. Écrire le facteur deux avant d’effectuer le calcul évite de confondre les deux distances.',
'19.8':r'Convertir 20 ms en 0,020 s puis $f=N/\Delta t=8/0{,}020=400\unite{Hz}$. Le nombre de motifs est un comptage, pas une durée. À 400 Hz, le son simple est plus aigu qu’à 200 Hz.',
'19.10':r'Utiliser la vitesse dans l’eau, puis le trajet double : $d=v\Delta t/2=1\,500\times0{,}20/2=150\unite m$. Employer la vitesse dans l’air changerait le modèle physique.',
'19.14':r'Durée réelle de propagation : $0{,}210-0{,}010=0{,}200\unite s$. Distance : $d=340\times0{,}200/2=34\unite m$. Le retard électronique n’est pas un temps passé à parcourir l’aller-retour.',
'19.15':r'Un écho de 2 s correspondrait à $340\times2/2=340\unite m$, pas 3,4 m. Pour 3,4 m : $\Delta t=2d/v=6{,}8/340=0{,}020\unite s$.',
'20.8':r'Pour x = 12, $U=0{,}10\times12=1{,}2\unite V$. Dans l’autre sens, $x=U/0{,}10=0{,}8/0{,}10=8$ dans l’unité de x. Vérifier le domaine d’étalonnage avant d’interpréter.',
'20.9':r'À 20 °C : $U=0{,}020\times20+0{,}50=0{,}90\unite V$. À 0 °C, U vaut déjà 0,50 V ; la droite ne passe donc pas par l’origine : la relation est affine, pas proportionnelle.',
'20.10':r'De $U=0{,}020T+0{,}50$, déduire $T=(U-0{,}50)/0{,}020$. Pour 1,30 V, $T=0{,}80/0{,}020=40\,^{\circ}\mathrm C$, dans la plage 0–50 °C.',
'20.13':r'Le calcul donne $T=(3-0{,}50)/0{,}020=125\,^{\circ}\mathrm C$. Le modèle n’est validé que de 0 à 50 °C : l’extrapolation ne suffit pas à annoncer une température mesurée fiable.',
}

# Numéros de questions à partir de 1 ; chaque illustration est placée au bon endroit.
ANNEXES={
'B1':{'enonce':{},'corrige':{5:('cor-distance-bilan','Segment de 6 cm à l’impression à 100 % ; les diamètres ne sont pas représentés.',True)}},
'B2':{'enonce':{},'corrige':{3:('cor-suspension','Interactions et forces distinguées.',False),4:('cor-poids-25N','Flèche de 2,5 cm à l’impression à 100 % ; échelle 1 cm pour 1 N.',True)}},
'B3':{'enonce':{1:('ex-circuit-parallele','Recopier et compléter le schéma pour placer les commandes.',False)},'corrige':{1:('cor-commandes-independantes','Une commande propre à chaque branche.',False),2:('cor-amperemetre-branche','Convertir puis soustraire ; l’ampèremètre mesure le courant de sa propre branche.',False),3:('cor-voltmetre-6V','Le voltmètre se branche aux bornes de la lampe étudiée.',False)}},
'B4':{'enonce':{3:('ex-dix-motifs','Compter des motifs complets sur toute la durée indiquée.',False)},'corrige':{2:('cor-echo-060','Deux trajets de 102 m ; durée totale de 0,60 s.',False),3:('cor-dix-motifs','25 ms = 0,025 s ; fréquence = 10 / 0,025 = 400 Hz.',False)}},
'E1':{'enonce':{},'corrige':{3:('cor-caisse-12N','Deux forces de même valeur sur la caisse immobile, dans ce modèle.',False),4:('cor-montage-150','A en série ; V en dérivation aux bornes de la résistance.',False),5:('cor-echo-0080','Le délai de 0,080 s correspond à l’aller-retour.',False)}},
'E2':{'enonce':{},'corrige':{2:('cor-reaction-methane','Les atomes sont conservés ; les assemblages changent.',False),3:('cor-circuit-evaluation','Deux branches sous 6 V ; courants de 0,12 A et 0,18 A.',False)}},
}

DEMARCHES_ANNEXES={
('B3',4):r'On choisit $U=RI$ et on isole l’intensité : $I=U/R$. Avec U en V et R en ohms, I est en A. Multiplier 0,030 A par 1 000 donne 30 mA. Le contrôle $200\times0{,}030=6\unite V$ retrouve la tension fournie.',
('B3',5):r'On applique $E=P\Delta t$. Avec 6 W et 2 h, on obtient 12 Wh, puis $12/1\,000=0{,}012\unite{kWh}$. Pour calculer en joules, convertir $2\unite h=7\,200\unite s$ : $E=6\times7\,200=43\,200\unite J$. La sortie thermique reste dans le bilan de conservation, même si elle n’est pas utile à l’éclairage.',
('E1',5):r'La durée mesurée couvre l’aller et le retour : $2d=v\Delta t$, donc $d=340\times0{,}080/2=13{,}6\unite m$. Le produit sans division, 27,2 m, est le trajet total. Si un retard électronique est présent, il faut le retrancher de la durée mesurée avant ce calcul.',
}

def appliquer(ex,ident):
    for key,val in ILLUSTRATIONS.get(ident,{}).items():setattr(ex,key,val)
    ex.methode=METHODES.get(ident,'')
    if ident=='10.9':ex.questions[0]='Construire le diagramme des interactions du livre, en négligeant l’air.'
    if ident=='D10':ex.questions[1]=r'Tracer les forces à l’échelle $1\unite{cm}$ pour $1{,}5\unite N$.'
    if ident=='16.5':ex.questions[0]='Tracer qualitativement U en fonction de I pour un conducteur ohmique idéal.'
def enrichir(chs):
    for c in chs:
        for j,ex in enumerate(c.exercices,1):appliquer(ex,f'{c.numero}.{j}')
        appliquer(c.defi,f'D{c.numero}')
