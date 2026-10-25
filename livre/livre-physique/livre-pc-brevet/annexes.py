from donnees import SOURCES
CONCORDANCE=[
('M01','États, changements d’état et interprétation microscopique',1,'1, 3, 10, 14','Cours ; sujet 7'),
('M02','Corps purs, mélanges, espèces et séparation',1,'2, 9, 11, 15','Fiche air ; sujet 2'),
('M03','Masse volumique, mesure, unités et température',1,'5, 6, 7, 8, 12, 13','Sujets 2 et 7'),
('M04','Solubilité, miscibilité et dissolution de gaz',1,'9, 11, 15','Fiche air, solutions et climat'),
('M05','Atomes, molécules, ions, formules et tableau périodique',2,'4, 6, 7, 8, 9, 14','Sujets 2, 5 et 7'),
('M06','Protons, neutrons, électrons et structure du noyau',2,'1, 2, 3, 8, 13, 15','Fiche des éléments ; sujet 7'),
('M07','Tests caractéristiques et transformations physiques/chimiques',3,'1, 3, 11, 12, 14','Sujets 5 et 10'),
('M08','Équation fournie, redistribution des atomes et conservation',3,'4, 5, 7, 8, 9, 10, 13','Sujets 1 et 10'),
('M09','Acidité, basicité, pH et ions H+ ou OH−',4,'1, 3, 6, 7, 10, 14','Sujets 2 et 5'),
('M10','Réactions acide-base et acide-métal',5,'2, 3, 6, 7, 12, 14','Réaction acide-base au chapitre 4'),
('M11','Corrosion, environnement et protections',5,'1, 4, 9, 10, 13, 15','Sujet 5'),
('M12','Air, combustions, gaz à effet de serre et impacts',6,'1, 6, 8, 11, 13, 14','Fiches air/climat ; sujet 1'),
('M13','Univers, Système solaire, évolution, éléments et ressources',7,'1, 2, 7, 8, 12, 15','Année-lumière au chapitre 16 ; sujet 9'),
('V01','Référentiel, relativité du mouvement et trajectoires',8,'1, 3, 8, 9, 13, 14','Sujet 1'),
('V02','Vitesse : valeur, direction, sens ; distance et durée',8,'4, 5, 6, 7, 10, 11, 12','Sujets 1 et 6'),
('V03','Interactions, forces et quatre caractéristiques',9,'1, 4, 9, 10, 13, 14','Sujet 4'),
('V04','Poids, masse et P = mg',9,'5, 6, 7, 8, 11, 15','Sujet 4'),
('V05','Exploitation de la loi fournie de gravitation',10,'5, 6, 8, 9, 10, 11, 14','Sujets 4 et 9'),
('E01','Énergie cinétique et énergie potentielle de position',11,'4, 6, 7, 8, 9, 15','Sujet 1'),
('E02','Sources, formes, transferts, conversions et conservation',12,'1, 2, 6, 7, 8, 15','Sujets 3, 7 et 8'),
('E03','Rayonnement, absorption et système Terre-atmosphère',12,'5, 9, 10, 14, 15','Fiche climat ; sujet 8'),
('E04','Circuits série/dérivation et cahier des charges',13,'3, 4, 8, 10, 13, 15','Sujet 3'),
('E05','Mesures, unicité et additivité des intensités/tensions',13,'1, 6, 7, 8, 11, 12','Sujet 3'),
('E06','Loi d’Ohm et caractéristique',14,'3, 4, 5, 8, 9, 13','Sujet 10'),
('E07','Puissance électrique P = UI',14,'6, 7, 9, 14, 15','Sujets 3, 6 et 10'),
('E08','Énergie, puissance, durée, consommation et stockage',15,'2, 3, 4, 6, 7, 11, 15','Sujets 3, 6 et 8'),
('S01','Sources, diffusion, rayon lumineux et propagation',16,'1, 3, 5, 8, 10, 11','Sujet 9'),
('S02','Vitesse de lumière, distances et année-lumière',16,'4, 6, 7, 12, 13, 15','Sujets 4 et 9'),
('S03','Propagation sonore, fréquence et plages audibles',17,'1, 2, 4, 6, 7, 13','Sujet 6'),
('S04','Écho, sonar, distance et prévention auditive',17,'3, 8, 9, 11, 14, 15','Sujet 6'),
('S05','Signaux, information, codage et mesures',18,'1, 4, 6, 7, 10, 12, 15','Sujets 4 et 6'),
]
def documents(chs):
    from construire import page,box,qs
    from brevets import documents as blancs
    from annales_originales import documents as annales
    s=blancs()+annales()
    s+=r'\pcAnnexe{Méthodes et références utiles}{Des fiches à consulter puis à utiliser sans aide}\phantomsection\label{methodes}\pdfbookmark[0]{Méthodes et outils}{bm-methodes}'+'\n'
    s+=box('Calculer en cinq étapes',r'1. Nommer la grandeur cherchée. 2. Écrire une relation adaptée. 3. Convertir les données. 4. Remplacer les valeurs et calculer. 5. Donner l’unité, un arrondi utile et une conclusion dans le contexte.','method')
    s+=r'''\pcSousTitre{Exemple : une énergie de fonctionnement}
Un appareil de 1,2 kW fonctionne 15 min à puissance constante. En kWh, écrire $\Delta t=15/60=0{,}25\unite h$, puis $E=1{,}2\times0{,}25=0{,}30\unite{kWh}$. En joules, utiliser 1 200 W et 900 s : $E=1\,080\,000\unite J$. Les deux résultats sont cohérents.
\pcSousTitre{Isoler une grandeur}
De $P=mg$ : $m=P/g$ et $g=P/m$, si les dénominateurs sont non nuls. De $E=P\Delta t$ : $P=E/\Delta t$ et $\Delta t=E/P$. Vérifier le sens : à même énergie, une puissance deux fois plus faible demande deux fois plus de temps.
\pcSousTitre{Comparer avant de calculer}
Si $E_c=\tfrac12mv^2$, doubler m double Ec ; doubler v quadruple Ec. Si la gravitation est fournie sous $F=Gm_Am_B/d^2$, doubler d divise F par quatre. Énoncer ce qui reste fixé.
\pcSousTitre{Contrôler un ordre de grandeur}
Une vitesse de vélo de plusieurs milliers de m/s ou une énergie en N signale une erreur probable de conversion ou de grandeur. Le contrôle de plausibilité complète le calcul ; il ne remplace pas les relations.
'''
    s+=page('Les relations de fin de cycle','Grandeurs, unités et conditions d’emploi','formules')
    s+=r'''\begingroup\renewcommand{\arraystretch}{1.5}\fontsize{10.5}{13}\selectfont
\begin{tabularx}{\linewidth}{@{}p{37mm}p{37mm}Y@{}}\toprule
Relation & Unités cohérentes & Conditions et précautions\\\midrule
$\rho=m/V$ & kg ; m³ ; kg/m³ & Matériau et température précisés\\
$v=d/\Delta t$ & m ; s ; m/s & Moyenne sur le trajet ; uniforme si précisé\\
$P=mg$ & kg ; N/kg ; N & g du lieu ; P est ici le poids\\
$F=Gm_Am_B/d^2$ & kg ; m ; N & Loi fournie ; d entre centres ; G en SI\\
$E_c=\tfrac12mv^2$ & kg ; m/s ; J & Référentiel et système indiqués\\
$U=RI$ & V ; A ; $\Omega$ & Conducteur ohmique, conditions fixées\\
$P=UI$ & V ; A ; W & Courant continu dans le cours\\
$E=P\Delta t$ & W ; s ; J & Puissance constante ou moyenne fournie\\
$E=P\Delta t$ & kW ; h ; kWh & Ne pas mélanger W et kW\\
$d=v\Delta t$ & m ; s ; m/s & Distance totale parcourue par le signal\\
$f=N/\Delta t$ & répétitions ; s ; Hz & Signal périodique ; N motifs complets\\\bottomrule
\end{tabularx}\endgroup
\begin{pcEncadre}{attention}{Le contexte détermine les symboles}
P peut désigner un poids en N ou une puissance en W. Lire la légende et l’unité, puis écrire le nom de la grandeur au début de la démarche.
\end{pcEncadre}
\pcSousTitre{Lois des circuits}
En série dans une branche : même I. À un nœud : somme entrante = somme sortante. Dans une boucle source + deux récepteurs avec conventions adaptées : $U_G=U_1+U_2$. En dérivation entre les mêmes nœuds : même U.
'''
    s+=page('Conversions et puissances de dix','Une fiche pour éviter les erreurs d’unité','conversions')
    s+=qs([r'$1\unite{kg}=1\,000\unite g$ ; $1\unite g=10^{-3}\unite{kg}$.',r'$1\unite L=1\unite{dm^3}$ ; $1\unite{mL}=1\unite{cm^3}$ ; $1\unite{m^3}=1\,000\unite L$.',r'$1\unite{g/mL}=1\,000\unite{kg/m^3}$. Un cube de 1 m de côté a un volume de $10^6\unite{cm^3}$.',r'$1\unite h=3\,600\unite s$ ; $1\unite{min}=60\unite s$. 15 min = 0,25 h, et non 0,15 h.',r'De km/h vers m/s : diviser par 3,6. De m/s vers km/h : multiplier par 3,6.',r'$1\unite A=1\,000\unite{mA}$ ; $1\unite{k\Omega}=1\,000\unite\Omega$ ; $1\unite{kW}=1\,000\unite W$.',r'$1\unite{Wh}=3\,600\unite J$ ; $1\unite{kWh}=3{,}6\times10^6\unite J$. Le kWh est une unité d’énergie.',r'$1\unite{kHz}=1\,000\unite{Hz}$ ; $1\unite{al}\approx9{,}46\times10^{15}\unite m$.'])
    s+=box('Le carré concerne toute la valeur',r'$(2\times10^3)^2=4\times10^6$ et non $2\times10^6$. Sur la calculatrice, saisir les parenthèses autour d’une distance écrite avec une puissance de dix avant de la mettre au carré.','method')
    s+=page('Lire un graphique','Exploiter un document et respecter la précision des données','graphiques')
    s+=qs(['Lire le titre, les noms des axes, les unités, l’origine et les graduations. Vérifier si l’axe des intensités est en A ou en mA.','Repérer la série et la légende ; distinguer mesure, modèle tracé et valeur de référence.','Pour une lecture, projeter le point vers les axes. Donner une valeur arrondie compatible avec la graduation.','Une droite ne prouve une proportionnalité que si elle est compatible avec le passage par l’origine et les conditions étudiées.','Pour un tableau, citer au moins une valeur pertinente et son unité avant de comparer.','Identifier l’auteur d’un document, sa date, son périmètre et les éventuelles données fictives. Une image seule n’est pas une mesure.'])
    s+=box('Construire une réponse ouverte','Dire ce que l’on cherche ; choisir les données utiles ; expliquer la relation ; calculer si nécessaire ; comparer ; conclure avec une limite. Si deux options ont des avantages différents, préciser le critère plutôt que proclamer une supériorité absolue.','method')
    s+=r'\pcSousTitre{Exemple de réponse scientifique courte}'+'\n'+r'« Dans le modèle fourni, A émet 1 kg de CO2 et B en émet 4 kg. A a donc des émissions quatre fois plus faibles pour ce trajet. Cette comparaison porte seulement sur le périmètre et l’indicateur fournis ; elle ne décrit pas tous les impacts. »'
    s+=page('Air, solutions et climat','Révisions transversales du cycle 4','air')
    s+=r'''\pcSousTitre{Composition et pression}
L’air sec contient environ 78 % de diazote, 21 % de dioxygène et 1 % d’autres gaz en volume. La vapeur d’eau est variable. Un gaz possède une masse et se comprime : à quantité de gaz conservée et après retour à la même température, un volume plus petit correspond à une pression plus élevée. La pression se mesure en pascals, Pa ; $1\unite{hPa}=100\unite{Pa}$ et $1\unite{bar}=10^5\unite{Pa}$. La pression atmosphérique usuelle est voisine de $10^5\unite{Pa}$.
\pcSousTitre{Dissolution et traitement des eaux}
Des gaz comme CO2 peuvent se dissoudre dans l’eau. Un gaz qui se dégage pouvait être déjà dissous : le dégazage n’est pas toujours une réaction. La miscibilité concerne deux liquides ; la solubilité caractérise une limite de dissolution dans des conditions données. Décantation, filtration et distillation séparent selon des propriétés différentes. Une eau clarifiée n’est pas automatiquement potable.
\pcSousTitre{Gaz à effet de serre}
CO2, vapeur d’eau, méthane et protoxyde d’azote font partie des gaz à effet de serre. Ils absorbent une partie du rayonnement infrarouge terrestre et émettent aussi du rayonnement. Un déséquilibre durable entre énergie reçue et énergie renvoyée peut modifier l’énergie du système Terre-atmosphère et sa température. L’effet de serre naturel est distinct de son renforcement lié aux activités humaines.
\pcSousTitre{Des conclusions qui respectent le périmètre}
Une absence de CO2 au point d’usage ne prouve pas une absence d’émissions sur tout le cycle de vie. L’acidification est une baisse de pH : un océan peut devenir moins basique tout en gardant un pH supérieur à 7. Comparer les émissions exige une même quantité de service et un périmètre annoncé.
\begin{pcEncadre}{method}{Trois questions flash, corrigées}
Dans 100 L d’air sec : environ 21 L de dioxygène. Une solution pH 8,0 reste basique vers 25 °C. Un écart énergétique reçu − renvoyé de 10 J correspond, dans un bilan sans autre échange, à une hausse d’énergie du système de 10 J.
\end{pcEncadre}
'''
    s+=page('Tests et formules usuelles','Une banque à exploiter avec le protocole donné','tests')
    s+=r'''\begingroup\renewcommand{\arraystretch}{1.45}\begin{tabularx}{\linewidth}{@{}p{32mm}p{47mm}Y@{}}\toprule
Espèce recherchée & Test fourni & Résultat positif usuel\\\midrule
CO2 & Eau de chaux & Trouble\\
O2 & Bûchette incandescente & Ravivement, test encadré\\
H2 & Flamme, test sécurisé & Petite détonation, test encadré\\
Eau & Sulfate de cuivre anhydre & Blanc vers bleu\\
Cl− & Nitrate d’argent & Précipité blanc\\
Cu2+ & Soude & Précipité bleu\\
Fe2+ & Soude & Précipité vert\\
Fe3+ & Soude & Précipité brun\\\bottomrule
\end{tabularx}\endgroup
\pcSousTitre{Les formules à reconnaître}
Dihydrogène H2 ; dioxygène O2 ; diazote N2 ; eau H2O ; dioxyde de carbone CO2 ; méthane CH4 ; protoxyde d’azote N2O. Ces écritures décrivent la composition ; les noms ne se remplacent pas par « gaz » sans précision.
\begin{pcEncadre}{attention}{Une banque n’est pas une consigne de manipulation libre}
Utiliser les quantités, protections et traitements des déchets indiqués par le professeur. Un test positif s’interprète dans ses conditions ; un résultat négatif dépend aussi de la sensibilité et de l’état du réactif. Faire les tests sur des prélèvements séparés.
\end{pcEncadre}
'''
    s+=page('Repères des éléments','Z identifie le nombre de protons','elements')
    els=[(1,'Hydrogène','H'),(2,'Hélium','He'),(3,'Lithium','Li'),(4,'Béryllium','Be'),(5,'Bore','B'),(6,'Carbone','C'),(7,'Azote','N'),(8,'Oxygène','O'),(9,'Fluor','F'),(10,'Néon','Ne'),(11,'Sodium','Na'),(12,'Magnésium','Mg'),(13,'Aluminium','Al'),(14,'Silicium','Si'),(15,'Phosphore','P'),(16,'Soufre','S'),(17,'Chlore','Cl'),(18,'Argon','Ar'),(19,'Potassium','K'),(20,'Calcium','Ca'),(26,'Fer','Fe'),(29,'Cuivre','Cu'),(30,'Zinc','Zn')]
    s+=r'Sélection de repérage ; ce tableau ne remplace pas une classification périodique complète. A n’est pas donné ici : on ne déduit pas un nombre précis de neutrons du seul Z.\par\vspace{3mm}'+'\n'
    s+=r'\begingroup\fontsize{10.5}{13}\selectfont\renewcommand{\arraystretch}{1.12}\begin{tabularx}{.85\linewidth}{@{}p{20mm}Yp{25mm}@{}}\toprule Z & Élément & Symbole\\\midrule'+'\n'
    for z,t,sym in els:s+=rf'{z} & {t} & {sym}\\'+'\n'
    s+=r'\bottomrule\end{tabularx}\endgroup'+'\n'
    s+=page('Diagnostic : corrigé','Un repère pour reprendre le bon chapitre','cor-diagnostic')
    s+=qs([r'250 mL et 0,350 kg. Reprendre la fiche conversions.', 'Non : une solution homogène peut contenir plusieurs espèces ; chapitre 1.', 'Quatre H et deux O ; chapitre 2.', '11 électrons, par neutralité ; chapitre 2.', 'Acide, car pH < 7 ; chapitre 4.',r'$v=120/30=4\unite{m/s}$ ; chapitre 8.', 'Poids en N ; masse en kg ; chapitre 9.', 'Ampèremètre en série ; voltmètre en dérivation ; chapitre 13.',r'$0{,}020\unite A$ et $900\unite s$ ; conversions.', 'La distance totale comprend l’aller et le retour ; chapitre 17.'])
    s+=box('Décider de la suite','Si une conversion est erronée, refaire deux exemples avec leurs unités. Si la notion est confuse, relire le cours et expliquer le schéma. Si la réponse est juste mais difficile à suivre, retravailler les phrases et l’organisation.','method')
    s+=page('Lexique scientifique','Des définitions à replacer dans une situation','lexique')
    lex=[('Atome','Entité neutre comportant un noyau et des électrons.'),('Ion','Entité chargée ayant perdu ou gagné des électrons.'),('Nucléon','Proton ou neutron du noyau.'),('Numéro atomique','Z : nombre de protons ; identifie l’élément.'),('Molécule','Assemblage neutre d’atomes liés.'),('Espèce chimique','Ensemble d’entités chimiques identiques.'),('Réactif','Espèce consommée lors d’une réaction.'),('Produit','Espèce formée lors d’une réaction.'),('Corrosion','Transformation d’un métal avec son environnement.'),('Dissolution','Dispersion d’un soluté dans un solvant.'),('Dilution','Ajout de solvant sans ajout de soluté.'),('Masse volumique','Masse divisée par le volume, dans des conditions précisées.'),('Force','Modèle d’une action : point, direction, sens et valeur.'),('Poids','Force de pesanteur exercée sur un objet.'),('Référentiel','Référence choisie pour décrire les positions et leur évolution.'),('Trajectoire','Ensemble des positions successives d’un point.'),('Énergie cinétique','Énergie associée au mouvement dans un référentiel.'),('Transfert','Passage d’énergie entre systèmes.'),('Conversion','Changement de forme d’énergie.'),('Puissance','Énergie transférée par unité de durée.'),('Tension','Grandeur électrique entre deux points, en V.'),('Intensité','Grandeur caractérisant le courant, en A.'),('Résistance','Grandeur d’un conducteur ohmique, en Ω.'),('Fréquence','Nombre de répétitions périodiques par seconde.'),('Signal','Phénomène détectable pouvant transporter de l’information.'),('Année-lumière','Distance parcourue par la lumière dans le vide en un an.'),('Témoin','Comparaison permettant d’examiner une cause possible.'),('Modèle','Représentation simplifiée dont le domaine d’emploi est précisé.')]
    s+=r'\begingroup\fontsize{10.5}{13.5}\selectfont\begin{multicols}{2}'+'\n'
    for term,definition in lex:s+=r'\par\addvspace{2mm}\noindent\begin{minipage}{\linewidth}\textbf{'+term+r'}\enspace '+definition+r'\par\end{minipage}\par'+'\n'
    s+=r'\end{multicols}\endgroup'+'\n'
    s+=page('Programme et concordance','Repérer les apprentissages du cycle 4','programme')
    s+=r'\pdfbookmark[0]{Programme et références}{bm-programme}'+'\n'
    s+=r'Les lignes relient les notions du programme en vigueur aux cours, exercices et sujets blancs. Le découpage annuel reste éditorial. La loi de gravitation est utilisée quand elle est fournie ; la formule de l’énergie potentielle n’est pas un prérequis exigé par ce manuel.\par\vspace{2mm}'+'\n'
    for code,title,ch,ex,mode in CONCORDANCE:
        s+=r'\par\noindent\begin{minipage}{\linewidth}'+rf'\textbf{{{code}}} · {title}. \hyperref[chap-{ch}]{{Chapitre {ch}}}, exercices {ex}. \emph{{{mode}.}}'+r'\par\end{minipage}\par\vspace{2mm}'+'\n'
    s+=page('Compétences et numérique','Pratiquer les démarches, les langages et les outils')
    s+=qs(['Démarche expérimentale : hypothèse, témoin, répétition et conclusion, chapitres 1, 3, 4 et 5.','Concevoir un dispositif : protocole de mesure et montage répondant à une demande, chapitres 9, 13 et 14.','Mobiliser le numérique : nuages de points au tableur, chapitres 1, 10, 11 et 14 ; vidéo au chapitre 8 ; signaux enregistrés aux chapitres 17 et 18.','Pratiquer les langages : équations, forces, circuits et graphiques ; réponses rédigées de tous les sujets blancs.','Adopter une attitude responsable : produits, déchets et ressources ; sécurité électrique ; protection visuelle et auditive.','Se situer dans le temps et l’espace : origine des éléments, évolution de l’Univers et ordres de grandeur, chapitres 2, 7 et 16.'])
    s+=box('Atelier tableur reproductible',r'Saisir v = 0, 2, 4, 6, 8 m/s ; fixer m = 2 kg. Calculer Ec par une formule recopiable. Conserver les données d’origine. Produire un nuage de points Ec(v), puis Ec(v²), avec noms des axes et unités. Expliquer la différence des deux graphes.','method')
    s+=page('Références et choix éditoriaux','Sources primaires vérifiées le 24 octobre 2026','references')
    refs=SOURCES+[
('Ressources pédagogiques','Éduscol : accompagnement du programme de physique-chimie au cycle 4.','https://eduscol.education.gouv.fr/5739/ressources-d-accompagnement-du-programme-de-physique-chimie-au-cycle-4'),
('Prévention électrique','INRS : risques et prévention en électricité.','https://www.inrs.fr/risques/electriques/risques-electricite.html'),
('Éléments et symboles','IUPAC : tableau périodique des éléments.','https://iupac.org/what-we-do/periodic-table-of-elements/'),
('Système solaire','Agence spatiale canadienne : formation des systèmes solaires.','https://www.asc-csa.gc.ca/fra/blogue/2021/08/06/comment-se-forment-les-systemes-solaires.asp')]
    for i,(title,desc,url) in enumerate(refs):
        if i and i%5==0:s+=page('Références complémentaires','Poursuivre la lecture des sources primaires')
        s+=r'\par\noindent\begin{minipage}{\linewidth}\pcSousTitre{'+title+'}\n'+desc+r'\par{\fontsize{8.5}{11}\selectfont\raggedright\url{'+url+r'}\par}\end{minipage}\par'+'\n'
    s+=r'''\pcSousTitre{Création et réutilisation}
Les sujets blancs, documents d’étude, barèmes et schémas sont des créations éditoriales OptiTAB. Les sujets ministériels ont été consultés pour analyser les attendus, sans reproduction de leurs exercices ni de leurs images. Les activités de révision sont harmonisées avec les autres manuels de la collection. Les nombres d’étude, prix et scénarios sont fictifs sauf indication explicite.
'''
    return s
