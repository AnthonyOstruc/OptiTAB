from donnees import E,SOURCES

BILANS=[
('B1','Matière et transformations',E('Une enquête sur les matériaux',
r'Un bloc de $54\unite g$ déplace $20\unite{mL}$ d’eau. Calculer sa masse volumique et comparer à $2{,}70\unite{g/cm^3}$ pour l’aluminium.@@Une solution a un pH de 4. La classer et expliquer pourquoi sa transparence ne prouve pas sa pureté.@@Dans $3\,\ce{CO2}$, compter C et O. Comparer cet inventaire à $3\,\ce C+3\,\ce{O2}$.@@Une réaction fermée consomme $6\unite g$ et $16\unite g$ de réactifs. Quelle masse totale de produits ? Justifier pourquoi une pesée ouverte peut différer.@@À l’échelle $1\unite{cm}$ pour $25$ millions de kilomètres, placer une distance de $150$ millions de kilomètres et préciser une limite du dessin.',
r'$\rho=54/20=2{,}70\unite{g/cm^3}$ : compatible avec de l’aluminium compact, sans preuve unique. 2 points pour le calcul, 2 pour la conclusion limitée.@@Solution acide vers 25 °C. Un mélange homogène peut être transparent. 2 points pour le classement, 2 pour l’explication.@@Trois C et six O dans chaque inventaire ; les assemblages et espèces diffèrent. 2 points pour le comptage, 2 pour la distinction.@@$22\unite g$ par conservation. Un système ouvert peut échanger des gaz. 2 points pour le calcul, 2 pour l’argument.@@$150/25=6\unite{cm}$. Les diamètres ou les positions orbitales ne sont pas nécessairement à l’échelle. 2 points pour la position, 2 pour la limite.',calculs=[('54/20',2.7),('6+16',22),('150/25',6)])),
('B2','Mouvements et interactions',E('Le chariot du laboratoire',
r'Un chariot parcourt $2{,}4\unite m$ en $3\unite s$. Calculer sa vitesse moyenne en m/s puis en km/h.@@Les positions, relevées toutes les $0{,}5\unite s$, sont régulièrement espacées sur une droite. Décrire le mouvement et préciser le référentiel.@@Un objet suspendu est immobile. Identifier deux interactions et les distinguer en contact ou distance.@@Avec $m=250\unite g$ et $g=10\unite{N/kg}$, calculer P et tracer sa flèche à $1\unite{cm}$ pour $1\unite N$.@@Sur la Lune avec $g=1{,}6\unite{N/kg}$, que deviennent masse et poids ? Expliquer sans parler de perte de matière.',
r'$v=2{,}4/3=0{,}80\unite{m/s}=2{,}88\unite{km/h}$. 2 points par unité et calcul.@@Rectiligne uniforme dans le référentiel de la table, si la mesure et l’échelle sont fiables. 2 points pour la trajectoire, 2 pour vitesse et référence.@@Terre : distance ; fil : contact. 2 points par interaction classée.@@$m=0{,}250\unite{kg}$ ; $P=2{,}5\unite N$, flèche verticale vers le bas de $2{,}5\unite{cm}$. 2 points pour conversion et calcul, 2 pour la flèche.@@Masse $0{,}250\unite{kg}$ inchangée ; poids $0{,}40\unite N$. 2 points pour les valeurs, 2 pour le rôle du lieu.',calculs=[('2.4/3',.8),('.8*3.6',2.88),('.25*10',2.5),('.25*1.6',.4)])),
('B3','Énergie et électricité',E('Éclairer en maîtrisant les mesures',
r'Deux lampes en dérivation doivent être commandées séparément. Décrire le placement de deux interrupteurs et des nœuds.@@Le courant principal vaut $0{,}50\unite A$ ; une branche vaut $180\unite{mA}$. Calculer l’autre intensité et indiquer le branchement de l’ampèremètre.@@Les deux branches sont reliées directement à une source idéale de $6\unite V$. Donner leurs tensions et placer un voltmètre.@@Une résistance de $200\unite\Omega$ est soumise à $6\unite V$. Calculer I et vérifier l’unité.@@Approfondissement : une lampe de $6\unite W$ fonctionne $2\unite h$. Calculer l’énergie en Wh, kWh et J, puis nommer une sortie non utile à l’éclairage.',
r'Chaque lampe et son interrupteur en série occupent une branche entre les deux mêmes nœuds. 2 points pour la dérivation, 2 pour les commandes.@@$I_2=0{,}50-0{,}180=0{,}320\unite A$. Ampèremètre en série dans la branche étudiée. 2 points pour le calcul, 2 pour le montage.@@$U_1=U_2=6\unite V$ ; voltmètre en dérivation aux bornes d’une lampe. 2 points par élément.@@$I=U/R=6/200=0{,}030\unite A=30\unite{mA}$. 2 points pour la relation, 2 pour calcul et unités.@@$12\unite{Wh}=0{,}012\unite{kWh}=43\,200\unite J$. Transfert thermique vers l’environnement. 3 points pour les conversions, 1 pour la sortie.',calculs=[('.5-.18',.32),('6/200',.03),('6*2*3600',43200)])),
('B4','Signaux et information',E('Communiquer et mesurer à distance',
r'Un signal lumineux parcourt $300\,000\unite{km}$ dans le vide. Estimer la durée et distinguer source primaire et objet diffusant.@@Un écho sonore revient après $0{,}60\unite s$ dans l’air, à $340\unite{m/s}$. Calculer la distance de l’obstacle et justifier le facteur 2.@@Un tracé présente 10 motifs en $0{,}025\unite s$. Calculer la fréquence et préciser si elle appartient à la plage audible humaine usuelle.@@Une télécommande utilise un signal infrarouge. Est-ce un son ? Identifier émetteur, récepteur et information possible.@@Un code associe A = 00, B = 01, C = 10, D = 11. Décoder 10 01 11 et expliquer pourquoi un début de message doit être défini.',
r'$\Delta t=300\,000/300\,000=1\unite s$. Une source primaire émet ; un diffuseur renvoie de la lumière reçue. 2 points pour le calcul, 2 pour la distinction.@@$d=340\times0{,}60/2=102\unite m$. Le son parcourt l’aller-retour. 2 points pour calcul, 2 pour trajet et unité.@@$f=10/0{,}025=400\unite{Hz}$, dans la plage usuelle 20 à 20 000 Hz. 2 points par réponse.@@Non : c’est un rayonnement. Télécommande émettrice, capteur récepteur, commande codée. 1 point par élément.@@C B D. Le début et les séparations évitent de confondre les groupes ou un zéro avec une absence de message. 2 points pour le décodage, 2 pour la limite.',calculs=[('340*.6/2',102),('10/.025',400)])),
]

EVALUATIONS=[
('E1','Une station d’observation',E('Mesurer sur le terrain',
r'Un objet de $81\unite g$ déplace $30\unite{mL}$ d’eau. Calculer sa masse volumique ; donner un contrôle du protocole.@@Un chariot parcourt $90\unite m$ en $45\unite s$. Calculer la vitesse moyenne en m/s et km/h ; dire pourquoi elle ne prouve pas un mouvement uniforme.@@Une caisse de $1{,}2\unite{kg}$ est posée sur le sol. Avec $g=10\unite{N/kg}$, calculer le poids et nommer une autre force qui peut le compenser.@@Une résistance sous 6 V est traversée par 40 mA. Trouver sa résistance et décrire le placement des deux appareils de mesure.@@Un signal sonore revient après $0{,}080\unite s$ dans l’air. Estimer la distance de la paroi et nommer une source possible d’erreur.',
r'$\rho=81/30=2{,}70\unite{g/cm^3}$. Contrôler immersion complète et bulles, ou tare et lecture. 3 points pour calcul et unités, 1 pour contrôle.@@$2\unite{m/s}=7{,}2\unite{km/h}$. La moyenne peut masquer des variations. 3 points pour calculs, 1 pour la limite.@@$P=12\unite N$ vers le bas ; l’action du support peut compenser vers le haut dans le modèle immobile. 2 points par force correctement décrite.@@$R=6/0{,}040=150\unite\Omega$. Ampèremètre en série, voltmètre en dérivation. 2 points pour R, 1 par montage.@@$d=340\times0{,}080/2=13{,}6\unite m$. Température, retard du capteur ou obstacle mal identifié peuvent affecter le résultat. 3 points pour le calcul, 1 pour la limite.',calculs=[('81/30',2.7),('90/45',2),('2*3.6',7.2),('1.2*10',12),('6/.04',150),('340*.08/2',13.6)])),
('E2','L’atelier scientifique',E('Relier plusieurs modèles',
r'Une réaction fermée transforme entièrement 4 g de carbone avec une masse de dioxygène fournie de $32/3\unite g$. Calculer la masse de produit en gardant une valeur exacte, puis un arrondi au dixième.@@Écrire les inventaires d’atomes de $\ce{CH4 + 2O2 -> CO2 + 2H2O}$ ; expliquer ce qui change et ce qui se conserve.@@Deux branches d’un circuit fournissent 0,12 et 0,18 A sous la même tension de 6 V. Calculer le courant principal et, en approfondissement, la puissance totale reçue.@@Cette puissance totale reste constante pendant 10 min. Calculer l’énergie en J et Wh ; identifier une hypothèse du calcul.@@Une étoile est à 5 années-lumière. Expliquer le délai d’observation et pourquoi cela ne suffit pas à prouver qu’elle a disparu.',
r'$m=4+32/3=44/3\unite g\approx14{,}7\unite g$. 2 points pour conservation et exact, 2 pour arrondi et unité.@@Un C, quatre H et quatre O de chaque côté. Les assemblages et espèces changent ; les atomes de chaque élément se conservent. 2 points pour inventaire, 2 pour explication.@@$I_G=0{,}30\unite A$ ; $P=6\times0{,}30=1{,}8\unite W$ en courant continu. 2 points par calcul.@@$10\unite{min}=600\unite s=1/6\unite h$ ; $E=1\,080\unite J=0{,}30\unite{Wh}$. Puissance supposée constante. 3 points pour calculs, 1 pour hypothèse.@@On reçoit une lumière émise environ 5 ans auparavant. Son état actuel dépend de son évolution ; la distance ne prouve pas une disparition. 2 points pour délai, 2 pour limite.',calculs=[('4+32/3',44/3),('.12+.18',.3),('6*.3',1.8),('1.8*600',1080),('1.8/6',.3)])),
]

CONCORDANCE=[
('M1','Masse, volume, masse volumique et température',1,'3, 5, 8, 14, 15','Approfondissement de 4e'),
('M2','Air, mélange de gaz, pression et modèle particulaire',2,'1, 6, 10, 11, 15','Consolidation et approfondissement'),
('M3','États, changements d’état, masse conservée et volume variable',3,'1, 4, 6, 10, 12','Interprétation microscopique'),
('M4','Dissolution, miscibilité, solubilité et séparation',4,'1, 2, 4, 6, 8, 10','Réinvestissement quantitatif'),
('M5','pH, ions et réactions acide-base',4,'3, 11, 14','pH introduit ; modèle ionique approfondi en 3e'),
('M6','Symboles, tableau périodique et formules usuelles',5,'1, 6, 7, 8, 12, 13','Atomes et molécules ; noyau réservé à la 3e'),
('M7','Tests, réactifs, produits, transformations physiques et chimiques',6,'3, 5, 6, 8, 12, 15','Identifier et argumenter'),
('M8','Redistribution des atomes et équations fournies',6,'6, 7, 11','Initiation aux bilans de réaction'),
('M9','Combustions, masse, corrosion et gaz à effet de serre',7,'6, 8, 11, 13, 14','Corrosion au chapitre 6 ; émissions discutées'),
('M10','Organisation, évolution et éléments de l’Univers',8,'1, 2, 7, 8, 12, 15','Échelles, histoire et ressources'),
('V1','Référentiel, trajectoire et variation de vitesse',9,'1, 3, 8, 9, 13, 14','Direction, sens et valeur'),
('V2','Distance, durée, vitesse et conversions',9,'4, 5, 6, 7, 10, 11, 12','Calculer et discuter une moyenne'),
('V3','Interactions, forces et représentations',10,'2, 3, 6, 9, 11, 15','Modélisation dès la 4e'),
('V4','Poids, masse et gravitation',11,'4, 6, 8, 9, 14, 15','P = mg accompagné ; loi de gravitation fournie en 3e'),
('E1','Sources, formes, transferts, conversions et conservation',12,'1, 2, 6, 7, 8, 15','Bilan qualitatif et quantitatif simple'),
('E2','Rayonnement, climat et ressources',12,'5, 9, 10, 14, 15','Terre-atmosphère ; liens avec combustions'),
('E3','Circuits série/dérivation, réalisation et sécurité',13,'3, 4, 6, 7, 11, 15','Cahier des charges et défauts'),
('E4','Intensité : mesure, unicité et additivité',14,'2, 4, 6, 7, 11, 15','Lois de l’électricité en 4e'),
('E5','Tension : mesure, additivité et unicité',15,'2, 3, 5, 6, 11, 13','Polarité et hypothèses'),
('E6','Conducteur ohmique et relation tension-courant',16,'4, 6, 7, 8, 11, 15','Caractéristique et domaine du modèle'),
('E7','Puissance, énergie, durée et consommation',17,'2, 6, 7, 8, 11, 14','Approfondissement de fin de cycle ; calendrier adaptable'),
('S1','Sources, vision, rayons, ombres et propagation',18,'1, 2, 3, 5, 12, 13','Approfondissement des bases de 5e'),
('S2','Vitesse de la lumière et année-lumière',18,'6, 7, 8, 9, 10, 11, 14','Applications astronomiques'),
('S3','Son, milieu, fréquence et risques auditifs',19,'1, 3, 4, 5, 8, 11, 12','Fréquence : première maîtrise accompagnée'),
('S4','Trajets simples et aller-retour',19,'6, 7, 9, 10, 13, 14, 15','Lien entre signaux et mouvement'),
('S5','Signal, information, radio et capteurs',20,'1, 2, 6, 8, 10, 11, 13, 15','Codes, analogique/numérique et limites'),
]

def qs(a):return '\\begin{questions}\n'+''.join('\\item '+s+'\n' for s in a)+'\\end{questions}\n'
def page(a,b='',label=''):
    return rf'\pcAnnexe{{{a}}}{{{b}}}'+ ('\n'+rf'\phantomsection\label{{{label}}}' if label else '')+'\n'
def box(a,b,kind='method'):return rf'\begin{{pcEncadre}}{{{kind}}}{{{a}}}'+b+'\\end{pcEncadre}\n'

def documents(chs):
    from revision_exercices import ANNEXES,DEMARCHES_ANNEXES
    from construire import figure_ex
    s=page('Bilans des quatre thèmes','Quatre bilans sur 20 points · 30 à 45 minutes chacun','bilans')
    s+=box('Une étape de consolidation','Chaque bilan comporte cinq questions de 4 points. Chercher sans les solutions, conserver les essais et conclure avec les unités. Le professeur peut adapter la durée et réserver les questions d’approfondissement à la suite du cycle.')
    for code,title,e in BILANS+EVALUATIONS:
        if code=='E1':
            s+=page('Évaluations de synthèse','Deux sujets inédits sur 20 points · Environ 45 minutes','evaluations')
            s+=box('Le cadre','Ces évaluations sont des propositions de travail de Quatrième, sans format d’examen national revendiqué. Chaque question vaut 4 points ; les relations de fin de cycle sont signalées. Calculatrice autorisée dans cette proposition.')
        s+=page(code+' · '+title,'Cinq questions · 4 points chacune','sujet-'+code)
        s+=r'\pdfbookmark[1]{'+code+' · '+title+'}{bm-'+code+'}\n'
        s+=r'\pcSousTitre{'+e.titre+'}\n'
        for j,q in enumerate(e.questions,1):
            s+=r'\par\noindent\begin{minipage}{\linewidth}\pcSousTitre{Question '+str(j)+r' · 4 points}'+'\n'+q+r'\par'+'\n'
            if j in ANNEXES.get(code,{}).get('enonce',{}):s+=figure_ex(*ANNEXES[code]['enonce'][j])
            s+=r'\end{minipage}\par'+'\n'
        s+=r'\pcRepere{cor-'+code+r'}{Corrigé et barème}'+('\\pcGrilleCourte' if code in ['B3','B4'] else '\\pcGrille')
    for code,title,e in BILANS+EVALUATIONS:
        s+=page('Corrigé '+code,title,'cor-'+code)
        if code=='B1':s+=r'\phantomsection\label{cor-bilans}\pdfbookmark[0]{Corrigés des bilans et évaluations}{bm-cor-bilans}'+'\n'
        for j,a in enumerate(e.reponses,1):
            s+=r'\par\noindent\begin{minipage}{\linewidth}\pcSousTitre{Question '+str(j)+r' · 4 points}'+'\n'+a+r'\par'+'\n'
            if (code,j) in DEMARCHES_ANNEXES:s+=r'\smallskip\textbf{Pour comprendre.}\enspace '+DEMARCHES_ANNEXES[(code,j)]+r'\par'+'\n'
            if j in ANNEXES.get(code,{}).get('corrige',{}):s+=figure_ex(*ANNEXES[code]['corrige'][j])
            s+=r'\end{minipage}\par'+'\n'
        s+=r'\pcRepere{sujet-'+code+'}{Revenir au sujet}\n'
    s+=page('Fiches méthodes','Des gestes réutilisables dans tout le manuel','methodes')
    s+=r'''\pcSousTitre{1 · Faire un calcul scientifique}
\begin{questions}
\item Identifier la grandeur demandée et les données utiles. Écrire les symboles et les unités.
\item Choisir une relation et vérifier ses hypothèses : mouvement uniforme, dipôle ohmique, puissance constante, trajet aller-retour, etc.
\item Convertir avant de remplacer les symboles par les valeurs. Garder une valeur non arrondie pendant les étapes.
\item Calculer, puis donner un résultat arrondi cohérent avec les données et une unité.
\item Contrôler l’ordre de grandeur et conclure dans le contexte.
\end{questions}
\begin{pcEncadre}{definition}{Exemple}
Pour parcourir 150 m à 5 m/s de façon uniforme : $\Delta t=d/v=150/5=30\unite s$. Une réponse de 30 h est incompatible avec les unités ; une réponse négative n’a pas de sens pour cette durée.
\end{pcEncadre}
\pcSousTitre{2 · Mesurer et discuter}
Choisir le calibre, vérifier le zéro, placer correctement la sonde ou l’appareil, noter la résolution et les conditions. Répéter si utile. Un écart entre deux valeurs ne prouve pas automatiquement une différence physique : comparer à la dispersion et à la précision. Dire « environ » n’autorise pas une valeur arbitraire.
\pcAnnexe{Lire et construire un graphique}{Une méthode en six gestes}
\begin{questions}
\item Nommer les grandeurs des axes et leurs unités. Identifier la variable réglée et la grandeur mesurée.
\item Choisir une échelle régulière utilisant une bonne partie du cadre. Une graduation ne change pas de valeur en cours d’axe.
\item Placer les points avec des croix fines et donner un titre précisant les conditions.
\item Ne pas imposer une droite : comparer d’abord les données au modèle attendu.
\item Pour une proportionnalité, chercher une droite passant près de l’origine et des quotients compatibles.
\item Lire une valeur avec sa précision ; éviter une extrapolation hors de la plage étudiée sans justification.
\end{questions}
\begin{pcEncadre}{method}{Un exemple de contrôle}
Pour une résistance, les points $(I;U)=(0{,}01;2)$, $(0{,}02;4)$ et $(0{,}03;6)$ en A et V donnent un quotient de $200\unite\Omega$. Le point $(0{,}02;5)$ s’écarterait de ce modèle : vérifier mesure, transcription et température avant de conclure.
\end{pcEncadre}
\pcAnnexe{Concevoir une investigation}{Faire correspondre question et protocole}
\begin{questions}
\item Formuler une question testable et une hypothèse distincte du résultat attendu.
\item Faire varier le paramètre étudié et garder comparables les autres conditions pertinentes.
\item Prévoir un témoin et, lorsque cela aide, un essai de référence ou une répétition.
\item Faire valider les risques, les quantités et le montage. Définir les grandeurs réellement mesurées.
\item Séparer faits, calculs et interprétations dans le compte rendu.
\item Dire ce que les résultats permettent de conclure et ce qu’ils ne permettent pas encore de prouver.
\end{questions}
\begin{pcEncadre}{definition}{Des verbes à distinguer}
\textbf{Décrire} : rendre compte des faits. \textbf{Identifier} : attribuer un nom avec un critère. \textbf{Calculer} : utiliser données, relation et unités. \textbf{Justifier} : relier la réponse à un argument. \textbf{Comparer} : utiliser des conditions et critères communs. \textbf{Conclure} : répondre à la question avec les limites utiles.
\end{pcEncadre}
\pcAnnexe{Mesurer en électricité}{Des branchements à retenir}
\begin{tabularx}{\linewidth}{@{}p{28mm}YYY@{}}\toprule
& Grandeur et unité & Branchement & Contrôle\\\midrule
Ampèremètre & Intensité I, en A & En série dans la branche & Fonction A, bornes, calibre et fusible\\[3mm]
Voltmètre & Tension U, en V & En dérivation entre deux points & Fonction V, polarité, calibre\\[3mm]
Ohmmètre & Résistance R, en $\Omega$ & Composant hors alimentation & Déconnexion et trajets parasites\\\bottomrule
\end{tabularx}
\begin{pcEncadre}{attention}{Une règle de montage}
Couper la source avant de modifier les connexions. Un ampèremètre directement entre les bornes d’une source peut la court-circuiter. Tous les montages du manuel sont limités au matériel scolaire autorisé et vérifiés par le professeur.
\end{pcEncadre}
\pcSousTitre{Les quatre relations de la progression}
Série : même intensité dans la branche et addition des tensions des récepteurs. Dérivation : même tension entre les mêmes nœuds et addition des intensités avec les sens définis. Conducteur ohmique : $U=RI$ dans sa plage. Énergie à puissance constante : $E=P\Delta t$.
\pcAnnexe{Tests et modèles de chimie}{Utiliser une banque fournie}
\begin{tabularx}{\linewidth}{@{}p{29mm}YY@{}}\toprule
Espèce & Test de la banque & Limite à retenir\\\midrule
Dioxyde de carbone & Eau de chaux troublée & Témoin et quantité détectable\\[3mm]
Dioxygène & Bûchette incandescente ravivée & Démonstration du professeur\\[3mm]
Dihydrogène & Très petit prélèvement : petite détonation avec flamme & Exclusivement sous conduite du professeur\\[3mm]
Eau & Sulfate de cuivre anhydre blanc qui bleuit & Réactif et échantillon non contaminés\\\bottomrule
\end{tabularx}
\pcSousTitre{Lire avant et après}
Une nouvelle espèce et la consommation de réactifs permettent d’identifier une réaction. Un test positif prouve une présence détectable dans ses conditions ; il ne donne pas automatiquement une quantité, une pureté ni un mécanisme. Une formule conserve ses indices dans un équilibrage ; les coefficients changent les nombres d’entités.
\pcSousTitre{L’inventaire qui vérifie}
Pour $\ce{CH4 + 2O2 -> CO2 + 2H2O}$ : un C, quatre H et quatre O de chaque côté. L’inventaire ne signifie pas que toutes les espèces ont la même masse, ni que les molécules sont conservées.
\pcAnnexe{Grandeurs et conversions}{Choisir les unités avant de calculer}
\begin{tabularx}{\linewidth}{@{}p{26mm}p{16mm}YY@{}}\toprule
Grandeur & Symbole & Unités usuelles & Relation utile\\\midrule
Masse & m & kg, g & 1 kg = 1 000 g\\[2mm]
Volume & V & m$^3$, L, mL & 1 mL = 1 cm$^3$\\[2mm]
Masse volumique & $\rho$ & kg/m$^3$, g/mL & $\rho=m/V$\\[2mm]
Durée & $\Delta t$ & s, min, h & 1 h = 3 600 s\\[2mm]
Vitesse & v & m/s, km/h & 1 m/s = 3,6 km/h\\[2mm]
Force, poids & F, P & N & $P=mg$\\[2mm]
Intensité & I & A, mA & 1 A = 1 000 mA\\[2mm]
Tension & U & V, mV & 1 V = 1 000 mV\\[2mm]
Résistance & R & $\Omega$, k$\Omega$ & $U=RI$\\[2mm]
Puissance & P & W, kW & $P=UI$ en continu\\[2mm]
Énergie & E & J, Wh, kWh & $E=P\Delta t$ à P constante\\[2mm]
Fréquence & f & Hz, kHz & 1 kHz = 1 000 Hz\\\bottomrule
\end{tabularx}
\begin{pcEncadre}{definition}{Égalités de référence}
$1\unite L=1\unite{dm^3}$ ; $1\unite{m^3}=1\,000\unite L$ ; $1\unite{g/mL}=1\,000\unite{kg/m^3}$ ; $1\unite{Wh}=3\,600\unite J$ ; $1\unite{kWh}=3{,}6\times10^6\unite J$.
\end{pcEncadre}
\pcAnnexe{Diagnostic : corrigé}{Comprendre les bases avant de poursuivre}
\phantomsection\label{cor-diagnostic}
'''+qs([
r'$0{,}5\unite L=500\unite{mL}$ ; $200\unite g=0{,}200\unite{kg}$.',
r'$V=42-30=12\unite{mL}=12\unite{cm^3}$, si le solide est totalement immergé, insoluble et sans bulle.',
'Non : elle contient plusieurs espèces, même si elle est homogène et transparente.',
'Non : les molécules restent celles de l’eau ; c’est une fusion, donc une transformation physique.',
r'$v=12/4=3\unite{m/s}$.',
'Le siège ou le train pour dire qu’il est immobile ; le quai ou le sol pour décrire son déplacement.',
'Dans l’unique boucle ouverte, le courant permanent devient nul dans le modèle.',
'Le son ne se propage pas dans le vide ; la fréquence se mesure en hertz, Hz.',
])
    s+=page('Repères des éléments','Nom, symbole et numéro atomique','elements')
    s+=r'''Ce répertoire reprend les vingt premiers éléments et trois métaux usuels. C’est une sélection de repérage, et non le tableau périodique complet. Le numéro atomique identifie l’élément ; la structure interne de l’atome sera étudiée en Troisième.
\begin{center}\begingroup\fontsize{10.5}{13}\selectfont\renewcommand{\arraystretch}{1.12}
\begin{tabularx}{.85\linewidth}{@{}p{20mm}Yp{25mm}@{}}\toprule
Z & Élément & Symbole\\\midrule
'''
    elements=[(1,'Hydrogène','H'),(2,'Hélium','He'),(3,'Lithium','Li'),(4,'Béryllium','Be'),(5,'Bore','B'),(6,'Carbone','C'),(7,'Azote','N'),(8,'Oxygène','O'),(9,'Fluor','F'),(10,'Néon','Ne'),(11,'Sodium','Na'),(12,'Magnésium','Mg'),(13,'Aluminium','Al'),(14,'Silicium','Si'),(15,'Phosphore','P'),(16,'Soufre','S'),(17,'Chlore','Cl'),(18,'Argon','Ar'),(19,'Potassium','K'),(20,'Calcium','Ca'),(26,'Fer','Fe'),(29,'Cuivre','Cu'),(30,'Zinc','Zn')]
    for z,name,symbol in elements:s+=rf'{z} & {name} & {symbol} \\'+'\n'
    s+=r'''\bottomrule\end{tabularx}\endgroup\end{center}
\pcSousTitre{Ne pas confondre symbole et formule}
N est le symbole de l’azote ; $\ce{N2}$ est le diazote. O est le symbole de l’oxygène ; $\ce{O2}$ est le dioxygène. $\ce{CO2}$ contient C et O, tandis que Co est le symbole du cobalt. Les majuscules et minuscules portent une information.
'''
    s+=page('Lexique scientifique','Des mots à utiliser avec leur contexte','lexique')
    lex=[('Atome','Entité constitutive de la matière ; son élément est repéré par un symbole.'),('Coefficient','Nombre placé devant une formule et multipliant toute sa composition.'),('Comburant','Réactif permettant une combustion, souvent le dioxygène.'),('Combustible','Réactif consommé comme source d’énergie dans une combustion.'),('Corps pur','Substance constituée d’une seule espèce dans le modèle annoncé.'),('Dérivation','Association de dipôles entre les mêmes deux nœuds.'),('Espèce chimique','Ensemble d’entités chimiques identiques.'),('Étalonnage','Correspondance établie entre des références et le signal d’un appareil.'),('Force','Modèle d’une action, avec point, direction, sens et valeur.'),('Fréquence','Nombre de répétitions périodiques par seconde.'),('Hypothèse','Proposition que l’on confronte à des observations ou des expériences.'),('Intensité','Grandeur caractérisant le courant, mesurée en ampères.'),('Masse volumique','Quotient de la masse par le volume dans des conditions précisées.'),('Mélange','Ensemble contenant plusieurs espèces chimiques.'),('Molécule','Assemblage neutre d’atomes liés.'),('Nœud','Point de connexion de plusieurs branches dans le modèle du circuit.'),('Poids','Force de pesanteur exercée sur un objet.'),('Produit','Espèce formée au cours d’une réaction.'),('Puissance','Énergie transférée par unité de durée.'),('Réactif','Espèce consommée au cours d’une réaction.'),('Référentiel','Référence spatiale et temporelle choisie pour décrire un mouvement.'),('Résistance','Grandeur d’un conducteur ohmique, exprimée en ohms ; aussi nom du dipôle.'),('Signal','Phénomène physique détectable pouvant transporter une information.'),('Solubilité','Limite de dissolution définie pour un soluté, un solvant et une température.'),('Tension','Grandeur électrique entre deux points, mesurée en volts.'),('Trajectoire','Ensemble des positions successives d’un point dans un référentiel.'),('Transfert','Passage d’énergie entre systèmes.'),('Vitesse moyenne','Distance totale parcourue divisée par la durée totale.')]
    s+=r'\begingroup\fontsize{10.5}{13.5}\selectfont\begin{multicols}{2}'+'\n'
    for term,definition in lex:
        s+=r'\par\addvspace{2mm}\noindent\begin{minipage}{\linewidth}\textbf{'+term+r'}\enspace '+definition+r'\par\end{minipage}\par'+'\n'
    s+=r'\end{multicols}\endgroup'+'\n'
    s+=page('Programme et progression','Concordance des apprentissages de cette édition','programme')
    s+=r'''\pdfbookmark[0]{Programme et références}{bm-programme}
Référence vérifiée le 24 octobre 2026 : BO du 30 juillet 2020, programme de physique-chimie du cycle 4. La répartition annuelle ci-dessous est éditoriale ; elle ne transforme pas tous les attendus de fin de cycle en obligations de Quatrième. Les repères de 3e sont annoncés dans les cours.\par\vspace{3mm}
'''
    for code,title,ch,ex,mode in CONCORDANCE:
        s+=rf'\noindent\textbf{{{code}}} · {title}. \hyperref[chap-{ch}]{{Chapitre {ch}}}, exercices {ex}. \emph{{{mode}.}}\par\vspace{{2mm}}'+'\n'
    s+=page('Compétences et numérique','Des capacités travaillées tout au long de l’année')
    s+=qs(['Pratiquer une démarche : hypothèse, témoin et conclusion, notamment chapitres 1, 4 et 6.','Concevoir et réaliser : montages et cahiers des charges aux chapitres 10, 13 à 16.','S’approprier des méthodes : mesures et conversions aux chapitres 1, 9, 11, 14 à 19.','Pratiquer des langages : formules, schémas, graphiques et argumentation dans tous les chapitres.','Mobiliser le numérique : vidéo au chapitre 9, graphique au tableur aux chapitres 1, 11 et 16, enregistrement au chapitre 19, étalonnage au chapitre 20.','Adopter une attitude responsable : eau et déchets aux chapitres 4 et 6, climat aux chapitres 7 et 12, électricité et audition aux chapitres 13 et 19.','Se situer dans le temps et l’espace : histoire de la matière et échelles astronomiques aux chapitres 8 et 18.'])
    s+=box('Atelier tableur','Saisir une colonne I en A et une colonne U en V pour la résistance du chapitre 16. Ajouter une colonne U/I seulement pour I non nul. Créer un nuage de points, et non un graphique de catégories. Vérifier les axes et comparer l’ajustement à la dispersion. Conserver le tableau d’origine pour pouvoir contrôler les modifications.')
    s+=page('Références et choix éditoriaux','Sources consultées le 24 octobre 2026','references')
    refs=SOURCES+[
('Constantes et unités','BIPM : définition du SI et valeur exacte de la vitesse de la lumière dans le vide.','https://www.bipm.org/fr/measurement-units/si-defining-constants'),
('Formation du Système solaire','Agence spatiale canadienne : formation à partir de gaz et de poussières, âge approximatif.','https://www.asc-csa.gc.ca/fra/blogue/2021/08/06/comment-se-forment-les-systemes-solaires.asp'),
('Risque électrique','INRS : risques de contact, échauffement et court-circuit.','https://www.inrs.fr/risques/electriques/risques-electricite.html'),
('Monoxyde de carbone','Santé publique France : formation par combustion incomplète et caractère imperceptible.','https://inpes.santepubliquefrance.fr/monoxyde-de-carbone/quest-ce-que-le-monoxyde-de-carbone-et-comment-se-forme-t-il'),
('Fréquence et audition','Éduscol : ressource sur sons graves, sons aigus et prévention auditive.','https://eduscol.education.gouv.fr/sites/default/files/document/ra19lyceetechnost2s1rephysiquechimiesante-songravesonaigu1188251pdf-82632.pdf')]
    refs.append(('Éléments chimiques','IUPAC : symboles et numéros atomiques de référence ; sélection du répertoire adaptée au collège.','https://iupac.org/what-we-do/periodic-table-of-elements/'))
    for i,(title,desc,url) in enumerate(refs):
        if i==5:s+=page('Références scientifiques','Comprendre les phénomènes et les risques')
        s+=r'\par\noindent\begin{minipage}{\linewidth}\pcSousTitre{'+title+'}\n'+desc+r'\par{\fontsize{8.5}{11}\selectfont\raggedright\url{'+url+r'}\par}\end{minipage}\par'+'\n'
    s+=r'''\pcSousTitre{Ce qui relève du manuel}
Les activités et exercices sont des créations originales, construites à partir des notions du programme. Ils ne reproduisent pas une banque commerciale ou un sujet officiel. Les expériences proposées sont des supports pour l’enseignant, qui adapte produits, quantités, matériel et calendrier. Les valeurs arrondies servent la progression ; les constantes exactes sont identifiées quand elles sont utiles.
'''
    return s
