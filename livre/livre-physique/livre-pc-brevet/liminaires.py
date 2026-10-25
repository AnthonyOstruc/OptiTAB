from donnees import THEMES
COUVERTURE=r'''\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]\begin{scope}[shift={(current page.south west)}]
\fill[otNavy] (0,0) rectangle (210mm,297mm);
\shade[bottom color=otNavyDark,top color=otNavy] (0,0) rectangle (210mm,165mm);
\draw[white,opacity=.045,step=8mm] (0,0) grid (210mm,297mm);
\node[anchor=north west,inner sep=0pt] at (22mm,279mm){\includegraphics[width=60mm]{logo-blanc}};
\node[anchor=west,text=otGreen,font=\otSemi\fontsize{11}{14}\selectfont] at (24mm,242mm){\otCaps[15]{Troisième · Série générale}};
\node[anchor=west,text=white,font=\otBold\fontsize{36}{42}\selectfont] at (22mm,217mm){Physique-chimie};
\node[anchor=west,text=white,font=\otLight\fontsize{32}{38}\selectfont] at (23mm,194mm){Objectif Brevet 2027};
\fill[otGreen] (24mm,180mm) rectangle (64mm,181.4mm);
\node[anchor=north west,text=white,text width=151mm,font=\otRegular\fontsize{11}{16}\selectfont] at (24mm,166mm)
{Tout le parcours pour comprendre, s’entraîner\\et rédiger une réponse scientifique solide.};
\node[anchor=north west,text=white,text width=151mm,font=\otRegular\fontsize{10.5}{15}\selectfont] at (24mm,132mm)
{\otCheck\hspace{3mm}18 chapitres · 270 exercices corrigés\\[3mm]
\otCheck\hspace{3mm}Énoncés et corrigés illustrés\\[3mm]
\otCheck\hspace{3mm}15 sujets de physique-chimie · format Brevet\\[3mm]
\otCheck\hspace{3mm}Barèmes, méthodes et révisions du cycle 4};
\draw[otGreen,line width=2pt] (24mm,49mm)--(60mm,49mm);
\node[anchor=west,text=white,font=\otSemi\fontsize{9}{12}\selectfont] at (24mm,39mm){France · Édition 2026-2027 · Manuel complet};
\node[anchor=west,text=white,opacity=.7,font=\otLight\fontsize{8}{11}\selectfont] at (24mm,29mm){Fondé sur le programme français et les modalités du DNB 2027};
\node[anchor=west,text=white,font=\otMedium\fontsize{10}{12}\selectfont] at (24mm,15mm){optitab.net};
\end{scope}\end{tikzpicture}\null\clearpage
'''
DIAGNOSTIC=[
r'Convertir $0{,}25\unite L$ en mL et $350\unite g$ en kg.',
'Un liquide transparent est-il forcément un corps pur ? Justifier.',
r'Compter les atomes H et O dans $2\,\ce{H2O}$.',
'Un atome neutre a Z = 11. Combien possède-t-il d’électrons ?',
'Classer une solution de pH 4 vers 25 °C.',
r'Un vélo parcourt 120 m en 30 s. Calculer sa vitesse moyenne.',
'Nommer l’unité du poids et la distinguer de celle de la masse.',
'Indiquer le branchement d’un ampèremètre et d’un voltmètre.',
r'Convertir 20 mA en A et 15 min en secondes.',
'Un écho a fait un aller-retour : pourquoi diviser la distance totale par deux ?',
]
def debut(chs):
    from construire import box,qs
    s=r'''\pagestyle{otFront}
\otPageTitre{Comprendre, puis réussir}{Un cours de Troisième et une préparation au Brevet}
Ce manuel réunit les apprentissages de fin de cycle et les révisions nécessaires de Cinquième et de Quatrième. Il s’adresse à l’élève qui veut construire ses raisonnements, à la famille qui l’accompagne et à l’enseignant qui cherche un parcours structuré.
\begin{pcEncadre}{method}{Quatre étapes pour apprendre}
\textbf{Comprendre.} Lire le cours et décrire les schémas à voix haute ; refaire l’exemple sans le regarder.\par
\textbf{Essayer.} Chercher un exercice avec le cours fermé et conserver les essais, même incomplets.\par
\textbf{Corriger.} Comparer méthode, conversions et conclusion, puis écrire la cause de l’erreur.\par
\textbf{Reprendre.} Refaire une question quelques jours plus tard, puis composer un sujet blanc en temps limité.
\end{pcEncadre}
\pcSousTitre{Un parcours progressif}
\otDots{1}\quad\textbf{Je démarre} : reconnaître, nommer et appliquer directement.\par
\otDots{2}\quad\textbf{Je m’entraîne} : calculer, représenter et relier les notions.\par
\otDots{3}\quad\textbf{Je raisonne} : choisir, croiser les données et argumenter.
\pcSousTitre{Ce que contient le manuel}
18 cours illustrés, 18 investigations et 18 défis ; 270 exercices avec réponses détaillées ; quinze sujets originaux de physique-chimie avec documents, points et remédiation, dont cinq dossiers supplémentaires au format des annales. Les liens internes permettent de passer de l’énoncé à la solution. Les fiches finales réunissent méthodes, unités, tests et concordance du programme.
\vfill
{\small OptiTAB · Octobre 2026. Manuel indépendant du ministère. Cours et exercices originaux ; certains parcours de révision reprennent des activités de la collection OptiTAB. Aucune homologation ni aucun numéro ISBN fictif n’est revendiqué.}
\clearpage\otPageTitre{Sommaire}{Le programme, puis les entraînements au Brevet}
\begingroup\setlength{\parskip}{0pt}
'''
    for k,(a,b,title) in enumerate(THEMES,1):
        s+=rf'\pcSomPartie{{{k}}}{{{title}}}'+'\n'
        for c in chs[a-1:b]:s+=rf'\pcSomLigne{{{c.numero:02}}}{{{c.titre}}}{{chap-{c.numero}}}'+'\n'
    s+=r'''\vspace{2mm}
\pcSomLigne{C}{Corrigés des exercices, investigations et défis}{corriges-debut}
\pcSomLigne{B}{Dix brevets blancs · Énoncés et documents}{brevets}
\pcSomLigne{S}{Corrigés, barèmes et reprise des sujets}{cor-brevets}
\pcSomLigne{A}{Cinq sujets supplémentaires au format des annales}{annales-originales}
\pcSomLigne{C}{Corrigés pédagogiques des sujets 11 à 15}{cor-annales-originales}
\pcSomLigne{M}{Méthodes, formules, unités et lexique}{methodes}
\pcSomLigne{P}{Concordance du programme et références}{programme}
\endgroup
\clearpage\otPageTitre{Le cadre de cette édition}{France · Cycle 4 · Année scolaire 2026-2027}
Le programme en application en physique-chimie est celui du cycle 4 publié au BO du 30 juillet 2020. Il fixe un ensemble pour les trois années du collège ; l’organisation annuelle de ce manuel est un choix éditorial. Les notions déjà rencontrées sont reprises pour préparer l’ensemble du cycle.
\begin{pcEncadre}{definition}{Le Brevet 2027 : le volet sciences}
L’épreuve de sciences dure une heure et porte sur deux disciplines retenues parmi physique-chimie, SVT et technologie. La durée indicative est de 30 minutes par discipline. La note totale est sur 20, soit 10 par discipline, dont 1 point pour la maîtrise de la langue. Les disciplines retenues sont annoncées deux mois avant l’épreuve ; le présent livre ne présume pas ce choix.
\end{pcEncadre}
\pcSousTitre{Des brevets blancs au bon périmètre}
Les quinze sujets sont des \textbf{volets de physique-chimie}, chacun prévu pour 30 minutes et noté sur 10. Ils constituent une préparation à cette discipline ; l’autre volet de l’épreuve de sciences n’est pas traité ici. Les exercices et documents sont créés pour le manuel et ne portent pas le statut de sujets ministériels.
\pcSousTitre{Rédiger fait partie des apprentissages}
Nommer les grandeurs, écrire les relations, convertir avant de calculer, puis conclure dans le contexte. Une question ouverte peut admettre plusieurs démarches cohérentes. La précision du vocabulaire et l’organisation d’une réponse sont travaillées dans les cours et dans chaque sujet blanc.
\pcRepere{programme}{Concordance et textes de référence, vérifiés le 24 octobre 2026}
\clearpage\otPageTitre{Expérimenter et raisonner}{Un cadre pour les investigations en classe}
\begin{pcEncadre}{attention}{Un protocole validé par le professeur}
Les activités de chimie, chauffage, électricité et tests de gaz nécessitent du matériel adapté et un encadrement. Les données et documents peuvent être étudiés sans reproduire une manipulation à domicile.
\end{pcEncadre}
\begin{questions}
\item Lire le protocole, identifier le système étudié et les risques, puis faire vérifier le matériel et le montage.
\item Ne pas goûter ni sentir directement un produit. Employer les protections prescrites, prélever de petites quantités et gérer les déchets selon la consigne.
\item Ne pas mélanger des produits ménagers. Ne pas fermer un dégagement gazeux dans un récipient rigide improvisé. Les tests à la flamme restent encadrés.
\item Couper l’alimentation avant de modifier un circuit ; utiliser seulement l’alimentation scolaire autorisée, sans manipuler le secteur domestique.
\item Ne pas regarder le Soleil ou une source intense ; ne pas augmenter le niveau sonore pour tester son audition.
\end{questions}
\begin{pcEncadre}{method}{La trace d’une démarche scientifique}
Question $\rightarrow$ hypothèse $\rightarrow$ protocole avec témoin $\rightarrow$ résultats et unités $\rightarrow$ interprétation $\rightarrow$ conclusion limitée aux conditions. Distinguer ce qui est observé, calculé et supposé.
\end{pcEncadre}
\pcSousTitre{Pourquoi répéter une mesure ?}
Des répétitions permettent de repérer la dispersion ; elles ne corrigent pas automatiquement un appareil décalé ou une méthode inadaptée. Annoncer la précision utile, comparer les résultats et signaler les limites avant de généraliser.
\clearpage\otPageTitre{Diagnostic de départ}{Dix questions pour choisir ses premières révisions}
Répondre sans le cours. Le diagnostic sert à repérer les besoins ; il ne remplace pas une évaluation de toutes les compétences.\par
'''+qs(DIAGNOSTIC)+r'''\pcRepere{cor-diagnostic}{Vérifier les réponses et choisir un chapitre}
\begin{pcEncadre}{method}{Un objectif réaliste}
Choisir deux priorités, refaire quelques exercices de niveau 1 et revenir au diagnostic après la correction. Une erreur de conversion appelle un entraînement différent d’une confusion entre force et énergie.
\end{pcEncadre}
\clearpage\otPageTitre{Organiser sa préparation}{Un rythme régulier avant les sujets blancs}
\pcSousTitre{Pendant l’année}
Après chaque cours : refaire l’exemple, chercher cinq exercices puis reprendre les erreurs. Chaque semaine : un court calcul, une lecture de graphique et une réponse rédigée. Conserver une page « mes erreurs fréquentes » avec un exemple corrigé.
\pcSousTitre{Un parcours de six semaines adaptable}
\begin{questions}
\item Matière et transformations : chapitres 1 à 6 ; sujet 2 puis reprise des questions manquées.
\item Atomes, ions et métaux : chapitres 2, 4 et 5 ; sujets 5 et 7.
\item Mouvements, forces et énergie : chapitres 8 à 11 ; sujet 1 et questions mécaniques du sujet 4.
\item Électricité et bilans : chapitres 12 à 15 ; sujets 3 et 8.
\item Univers et signaux : chapitres 7 et 16 à 18 ; sujets 6 et 9.
\item Synthèse : sujets 4 et 10 sans aide ; refaire deux questions mal réussies et une réponse ouverte.
\end{questions}
\begin{pcEncadre}{definition}{Avant de rendre la copie}
Ai-je traité toutes les questions accessibles ? Mes unités sont-elles cohérentes ? Les axes et les flèches ont-ils une légende ? La conclusion répond-elle à la question ? Ai-je écrit une démarche même si le calcul n’est pas terminé ?
\end{pcEncadre}
\pcRepere{brevets}{Accéder aux dix sujets blancs}
'''
    return s
