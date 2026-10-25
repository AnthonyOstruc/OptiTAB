from donnees import THEMES

COUVERTURE=r'''\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]\begin{scope}[shift={(current page.south west)}]
\fill[otNavy] (0,0) rectangle (210mm,297mm);
\shade[bottom color=otNavyDark,top color=otNavy] (0,0) rectangle (210mm,155mm);
\draw[white,opacity=.05,step=8mm] (0,0) grid (210mm,297mm);
\node[anchor=north west,inner sep=0pt] at (22mm,279mm){\includegraphics[width=60mm]{logo-blanc}};
\node[anchor=west,text=otGreen,font=\otSemi\fontsize{11}{14}\selectfont] at (23mm,239mm){\otCaps[18]{Quatrième · Collège}};
\node[anchor=west,text=white,font=\otBold\fontsize{36}{42}\selectfont] at (21mm,215mm){Physique-chimie};
\node[anchor=west,text=white,font=\otLight\fontsize{27}{33}\selectfont] at (22mm,195mm){Comprendre et réussir};
\fill[otGreen] (24mm,182mm) rectangle (54mm,183.4mm);
\node[anchor=north west,text=white,text width=156mm,font=\otRegular\fontsize{11}{16}\selectfont] at (24mm,169mm)
{Le cours expliqué et illustré\\Des expériences pour raisonner\\Des exercices progressifs et leurs corrigés};
\node[anchor=north west,text=white,text width=151mm,font=\otRegular\fontsize{10.5}{15}\selectfont] at (24mm,130mm)
{\otCheck\hspace{3mm}20 chapitres · 300 exercices corrigés\\[3mm]
\otCheck\hspace{3mm}20 investigations · 20 défis\\[3mm]
\otCheck\hspace{3mm}Schémas et graphiques vectoriels\\[3mm]
\otCheck\hspace{3mm}Bilans, évaluations et fiches méthodes};
\draw[otGreen,line width=2pt] (24mm,49mm)--(60mm,49mm);
\node[anchor=west,text=white,font=\otSemi\fontsize{9}{12}\selectfont] at (24mm,39mm){France · Cycle 4 · Édition 2026-2027};
\node[anchor=west,text=white,opacity=.7,font=\otLight\fontsize{8}{11}\selectfont] at (24mm,29mm){Manuel indépendant fondé sur les textes du Bulletin officiel};
\node[anchor=west,text=white,font=\otMedium\fontsize{10}{12}\selectfont] at (24mm,15mm){optitab.net};
\end{scope}\end{tikzpicture}\null\clearpage
'''

def debut(chs):
    s=r'''\pagestyle{otFront}
\otPageTitre{Apprendre la physique-chimie}{Observer · Expérimenter · Modéliser · Expliquer}
Ce manuel accompagne une année de Quatrième. Les questions partent de situations concrètes pour construire des modèles et apprendre à les utiliser avec précision.
\begin{pcEncadre}{method}{Un parcours pour progresser}
\textbf{Comprendre.} Lire le cours, commenter le schéma et refaire l’exemple en cachant les calculs.\par
\textbf{Essayer.} Chercher les exercices avant d’ouvrir les solutions ; conserver les essais et les unités.\par
\textbf{Raisonner.} Comparer des résultats, vérifier les hypothèses et expliquer les limites d’une conclusion.\par
\textbf{Consolider.} Corriger une erreur puis refaire la question quelques jours plus tard, sans aide.
\end{pcEncadre}
\pcSousTitre{Trois niveaux, dans chaque chapitre}
\otDots{1}\quad\textbf{Je démarre} : reconnaître, nommer, lire et appliquer directement.\par
\otDots{2}\quad\textbf{Je m’entraîne} : calculer, représenter et relier plusieurs connaissances.\par
\otDots{3}\quad\textbf{Je raisonne} : croiser des données, choisir une méthode et argumenter.
\pcSousTitre{Des outils pour apprendre}
Chaque chapitre propose une investigation encadrée, un exemple résolu et un défi. Les corrigés donnent les démarches et les limites des modèles. Les renvois entre énoncés et solutions sont cliquables.
Les données d’exercices sont choisies pour l’apprentissage, sauf référence explicite. Les prix sont fictifs. Un dessin peut être schématique : sa légende précise les échelles et les conventions.
\vfill
{\small OptiTAB · Octobre 2026. Cours, exercices, corrigés et schémas : création éditoriale originale. Manuel indépendant ; aucune homologation ministérielle revendiquée. Aucun numéro ISBN fictif.}
\clearpage\otPageTitre{Sommaire}{Une progression dans les quatre thèmes du cycle 4}
\begingroup\setlength{\parskip}{0pt}
'''
    for k,(a,b,title) in enumerate(THEMES,1):
        s+=rf'\pcSomPartie{{{k}}}{{{title}}}'+'\n'
        for c in chs[a-1:b]:s+=rf'\pcSomLigne{{{c.numero:02}}}{{{c.titre}}}{{chap-{c.numero}}}'+'\n'
    s+=r'''\vspace{3mm}\pcSomLigne{C}{Corrigés des exercices et des défis}{corriges-debut}
\pcSomLigne{B}{Bilans des quatre thèmes}{bilans}
\pcSomLigne{E}{Deux évaluations de synthèse}{evaluations}
\pcSomLigne{M}{Méthodes, conversions et lexique}{methodes}
\pcSomLigne{P}{Programme, progression et références}{programme}
\endgroup
\clearpage\otPageTitre{Le cadre de cette édition}{Programme français · Année scolaire 2026-2027}
La page Éduscol des programmes en application en 2026-2027 confirme la référence du BO du 30 juillet 2020 pour la physique-chimie du cycle 4. Le texte définit des attendus pour les trois années ; il ne fixe pas un découpage annuel unique.
\begin{pcEncadre}{definition}{La progression choisie en Quatrième}
Le manuel approfondit la masse volumique, les modèles de la matière, les transformations chimiques, les forces et les lois de l’électricité. Il reprend les bases de Cinquième quand elles sont nécessaires, puis applique vitesse, distance et durée aux signaux et à l’Univers.
\end{pcEncadre}
\pcSousTitre{Les repères pour la Troisième}
La structure interne de l’atome, les calculs ioniques détaillés et l’exploitation formelle de la gravitation sont réservés à la suite du cycle. La relation de l’énergie cinétique est seulement exploitée lorsqu’elle est fournie. Le chapitre 17 prépare les relations énergétiques de fin de cycle : le professeur peut adapter son calendrier.
\pcSousTitre{Une couverture vérifiable}
Une concordance en fin de manuel relie les apprentissages aux chapitres et aux exercices. Elle distingue la progression de Quatrième des prolongements de fin de cycle. Les ressources officielles éclairent la construction ; les exercices du manuel sont inédits et ne sont pas présentés comme des sujets officiels.
\pcRepere{programme}{Concordance et références}
\clearpage\otPageTitre{Expérimenter avec soin}{Des habitudes de travail scientifique}
\begin{pcEncadre}{attention}{Avant de manipuler}
Lire tout le protocole, identifier les risques et faire vérifier le montage. Les manipulations de chimie, de chauffage et d’électricité se font en classe avec les produits, protections et appareils choisis par le professeur.
\end{pcEncadre}
\begin{questions}
\item Ne pas goûter les produits ni les sentir directement. Porter les lunettes et protections demandées ; attacher les cheveux lorsque le protocole l’exige.
\item Prélever de petites quantités, étiqueter et trier les déchets selon la consigne. Ne pas mélanger de produits ménagers et ne pas fermer un dégagement gazeux dans un récipient rigide improvisé.
\item Utiliser seulement le matériel électrique scolaire autorisé. Couper l’alimentation avant de modifier les connexions ; ne jamais manipuler le secteur domestique.
\item Ne pas regarder le Soleil, un laser ou une source intense. Ne pas chercher un niveau sonore élevé pour tester l’audition.
\item Garder la paillasse dégagée. Signaler une casse, une fuite ou un fonctionnement anormal et demander avant de poursuivre.
\end{questions}
\begin{pcEncadre}{method}{Une trace utile}
Question $\rightarrow$ hypothèse $\rightarrow$ protocole $\rightarrow$ résultats avec unités $\rightarrow$ interprétation $\rightarrow$ conclusion et limites. Une observation n’est pas une interprétation ; une hypothèse doit pouvoir être confrontée aux faits.
\end{pcEncadre}
\clearpage\otPageTitre{Diagnostic de départ}{À faire sans corrigé, puis à reprendre après révision}
\begin{questions}
\item Convertir 0,5 L en mL, puis 200 g en kg.
\item Une éprouvette passe de 30 à 42 mL après immersion d’un solide insoluble. Calculer son volume.
\item Une eau salée limpide est-elle un corps pur ? Justifier.
\item Une glace fond. Une nouvelle espèce chimique apparaît-elle ?
\item Un mobile parcourt 12 m en 4 s. Calculer sa vitesse moyenne.
\item Nommer un objet de référence pour décrire le mouvement d’un passager assis dans un train.
\item Dans une boucle série, un interrupteur s’ouvre. Que devient le courant ?
\item Un son se propage-t-il dans le vide ? Quelle unité mesure une fréquence ?
\end{questions}
\pcRepere{cor-diagnostic}{Corrigé du diagnostic}
\pcSousTitre{Comment utiliser le résultat}
Une difficulté de conversion invite à retravailler la fiche des unités. Une confusion entre grandeur, appareil et unité doit être corrigée avant d’enchaîner les calculs. Un résultat numérique juste sans unité reste incomplet.
\clearpage\otPageTitre{Mon parcours}{Une case après une réussite autonome}
\begin{tabularx}{\linewidth}{@{}p{7mm}Yccc@{}}\toprule
& Chapitre & Cours & Exercices & Reprise\\\midrule
'''
    for c in chs:s+=rf'{c.numero} & {c.titre} & \pcCase & \pcCase & \pcCase \\[1.7mm]'+'\n'
    s+=r'''\bottomrule\end{tabularx}
\vspace{4mm}Noter la date d’une reprise dans le cahier. Une correction comprise devient un apprentissage durable lorsqu’on réussit ensuite sans regarder la solution.
\clearpage
'''
    return s
