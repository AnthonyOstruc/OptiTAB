from modele import CHAPITRES

BO10='https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2010%20du%205%20mars%202026-480719.pdf'
BOS4='https://www.education.gouv.fr/sites/default/files/document/bulletin-officiel-special-ndeg-4-du-17-septembre-2026-521113.pdf'
SOURCES=[
('Arrêté du 18 février 2026 : calendrier','« Programmes d’enseignement de français et de mathématiques du cycle des approfondissements (cycle 4) », arrêté du 18-2-2026, JO du 4-3-2026, NOR MENE2602912A, Bulletin officiel n° 10 du 5 mars 2026. Article 3 : application en classe de troisième à la rentrée de l’année scolaire 2028-2029.',BO10),
('Programme de mathématiques du cycle 4','Annexe 2 de cet arrêté, « Programme de mathématiques pour le cycle 4 » : principes, puis rubriques de Troisième (automatismes, objectifs d’apprentissage et prolongements possibles).','https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf'),
('Exemples pour la mise en œuvre','Éduscol, « Mathématiques. Exemples pour la mise en œuvre des programmes 2026. Cycle 4 » : exemples de réussite et conseils de mise en œuvre pour chaque objectif de Troisième.','https://eduscol.education.gouv.fr/sites/default/files/document/exemple-mise-en-oeuvre-c4-mathematiques0pdf-126080.pdf'),
('Définition de l’épreuve du brevet','Note de service du 11-9-2026, NOR MENE2623228N, « Définition des épreuves de l’examen du diplôme national du brevet à compter de la session 2027 », Bulletin officiel spécial n° 4 du 17 septembre 2026 ; partie 2 : épreuve écrite de mathématiques.',BOS4),
('Maîtrise de la langue aux examens','Note de service du 11-9-2026, NOR MENE2623195N, « Exigences en matière de maîtrise de la langue à tous les examens à compter de la session 2027 », même Bulletin officiel spécial n° 4.',BOS4),
]

def front(titre,sous,body,label):
    return r'\clearpage\thispagestyle{otFront}\phantomsection\label{'+label+r'}\pdfbookmark[0]{'+titre+'}{bm-'+label+r'}\otPageTitre{'+titre+'}{'+sous+r'}\fontsize{11}{15}\selectfont'+'\n'+body+'\n'+r'\clearpage'+'\n'

def documents():
    docs={}
    docs['copyright']=r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{128mm}\fontsize{9}{13}\selectfont\color{otMuted}
{\otSemi\color{otInk}Mathématiques · Troisième\par Édition 2028-2029 · Nouveau programme · Brevet 2029}\par\medskip
Conception et mise en page : collection OptiTAB.\par
270 exercices de chapitre, 18 défis et deux brevets blancs originaux, corrigés.\par
Charte graphique de la collection OptiTAB.\par\bigskip
Édition du 23 octobre 2026 · France · Année scolaire 2028-2029.\par\bigskip
Cette édition suit le programme de mathématiques du cycle 4 fixé par l’arrêté
du 18 février 2026 (BO n° 10 du 5 mars 2026), applicable en Troisième à la
rentrée 2028. Elle prépare la session 2029 du diplôme national du brevet.\par\bigskip
Au 23 octobre 2026, aucun texte propre à la session 2029 n’était publié. Les
brevets blancs suivent la définition de l’épreuve de mathématiques en vigueur
à compter de la session 2027 (note de service du 11 septembre 2026, BO spécial
n° 4 du 17 septembre 2026). Vérifier avant l’examen qu’aucun texte plus récent
ne l’a modifiée.\par\bigskip
L’ordre des chapitres, les exercices et les barèmes d’entraînement sont des
choix éditoriaux. Les défis sont facultatifs. Les situations et données
numériques sont construites pour l’apprentissage ; elles ne constituent pas
des données économiques ou scientifiques relevées.\par\bigskip
Les schémas de principe ne permettent pas de mesurer une longueur inconnue.
Les coordonnées et graduations explicites font foi pour les graphiques.
Sauf demande d’arrondi, conserver les résultats exacts.\par\bigskip
© OptiTAB, 2026.\par\otSite
\end{minipage}\clearpage
'''
    docs['avant-propos']=front('Apprendre et comprendre','Un livre pour toute l’année de Troisième',r'''
Ce livre accompagne la classe de Troisième et la préparation du brevet 2029,
avec le nouveau programme de mathématiques du cycle 4. Il aide à consolider les
calculs, à comprendre les nouvelles notions, puis à résoudre des problèmes en
reliant plusieurs outils. Il complète le travail de classe, dans l’ordre adapté aux besoins.\par\medskip
\begin{savoirfaire}[Une progression en trois temps]Chaque chapitre propose deux pages de cours, cinq exercices de découverte, cinq d’entraînement et cinq problèmes. Les corrections explicitent la méthode, les calculs et l’interprétation. Une figure utile est reprise avec le corrigé ; une construction cherchée n’apparaît qu’à cet endroit.\end{savoirfaire}
\begin{savoirfaire}[Chercher avant de consulter]Écrire une première démarche même incomplète. Après correction, fermer le livre et refaire les étapes décisives. Quelques jours plus tard, reprendre un exercice proche sans aide : reconnaître un résultat n’est pas encore savoir le retrouver.\end{savoirfaire}
\begin{savoirfaire}[Aller plus loin]Les dix-huit défis demandent une initiative supplémentaire, avec deux indications séparées et une solution rédigée. Deux brevets blancs permettent un entraînement chronométré. Les fiches et la matrice finale aident à repérer la notion à revoir.\end{savoirfaire}
Les six compétences travaillées sont chercher, modéliser, représenter,
raisonner, calculer et communiquer. Un dessin, un tableau ou un script sont
des moyens de penser autant que des supports de réponse.
''','avant-propos')
    docs['mode-emploi']=front('Mode d’emploi','Des repères stables dans tout le livre',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Une pastille & Découvrir : appliquer une propriété, lire une représentation ou faire un calcul direct.\\[3mm]
Deux pastilles & S’entraîner : choisir une méthode, combiner deux étapes ou interpréter un résultat.\\[3mm]
Trois pastilles & Résoudre : organiser une démarche plus longue, justifier et contrôler.\\\bottomrule
\end{tabularx}\par\medskip
Ces niveaux sont des repères pédagogiques, pas un classement des élèves.
Un exercice simple peut révéler une notion à consolider ; un problème peut
être réussi avec une représentation bien choisie.\par\medskip
\begin{exemple}[Une correction utile]Pour résoudre $3(x-2)=x+4$, on développe : $3x-6=x+4$, puis $2x=10$, donc $x=5$. Le contrôle dans l’énoncé donne $3(5-2)=9=5+4$. L’égalité obtenue vérifie la solution.\end{exemple}
\begin{attention}Lire tout l’énoncé, y compris les unités, les mots « exactement », « au moins », « et », « ou » et la précision demandée. En géométrie, un angle droit dessiné sans hypothèse n’est pas une preuve.\end{attention}
Les liens du sommaire et les numéros de page conduisent aux chapitres et
aux corrigés. Le tableau de bord permet de noter ce qui est réussi seul,
réussi avec aide ou à reprendre. Pour les scripts, les blocs indentés
appartiennent au bloc qui les contient ; les lignes « fin » en indiquent la fermeture.
''','mode-emploi')
    docs['parcours']=front('Construire son parcours','Avancer avec des retours réguliers',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Étape & Travail conseillé\\\midrule
Consolider & Chapitres 1 à 5 : nombres, puissances, calcul littéral, équations et inéquations.\\[3mm]
Modéliser & Chapitres 6 à 11 : proportionnalité, fonctions, statistiques et probabilités.\\[3mm]
Démontrer & Chapitres 12 à 16 : théorèmes du triangle, vecteurs, espace.\\[3mm]
Programmer & Chapitre 17, à reprendre pendant toute l’année.\\[3mm]
Synthétiser & Chapitre 18, défis et brevets blancs.\\\bottomrule
\end{tabularx}
\begin{savoirfaire}[Une séance autonome de 35 à 50 minutes]Relire une propriété et son exemple ; traiter deux exercices sans correction ; comparer la démarche ; refaire une question ratée. Terminer par une phrase : « La prochaine fois, je dois penser à… ».\end{savoirfaire}
\begin{savoirfaire}[Une révision espacée]Revenir sur une notion quelques jours après, puis quelques semaines plus tard. Mélanger un calcul, une lecture graphique et une justification géométrique évite de dépendre seulement de l’ordre du chapitre.\end{savoirfaire}
Pour un défi, prévoir 30 à 60 minutes, éventuellement en deux séances.
Pour un brevet blanc, utiliser deux copies et respecter la remise de la
première au bout de 20 minutes. Refaire ensuite les erreurs par notion,
sans attendre le prochain sujet complet.
''','parcours')
    docs['nouveautes']=front('Nouveau programme','Ce qui change en Troisième à la rentrée 2028',r'''
Le programme de mathématiques du cycle 4 publié en 2026 s’applique en Troisième
à la rentrée 2028. Cette édition a été réécrite en conséquence ; voici les
principaux changements par rapport au programme précédent.\par\medskip
\fontsize{10}{13.5}\selectfont
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{27mm}Y@{}}\toprule
Nouveau en Troisième & Translations et vecteurs : vecteurs égaux, somme, relation de Chasles (ch. 15). Effectifs cumulés, quartiles et boîtes à moustaches (ch. 10). Réunion, intersection et relation $P(A\cup B)+P(A\cap B)=P(A)+P(B)$ (ch. 11). Inéquations $ax\ge b$ par le calcul et graphiquement (ch. 5 et 9). Trois identités remarquables et raisonnement par analyse-synthèse (ch. 4 et 5). Fonction carré et équation $x^2=a$ (ch. 2 et 8). Sphère, boule, grands cercles et sections (ch. 16). Conditions composées, boucles conditionnelles et blocs personnalisés (ch. 17).\\[3mm]
Prolongements & Notations $\mathbb N$, $\mathbb Z$, $\mathbb D$, $\mathbb Q$ (ch. 1) ; préfixes de nano à giga (ch. 2) ; identité de Sophie Germain et cylindre d’Archimède (défis et ch. 16).\\[3mm]
Réactivé & Pythagore, sa réciproque et sa contraposée, cercle circonscrit au triangle rectangle, droite des milieux, grandeurs quotients et expériences à deux épreuves : étudiés en Quatrième, ils sont attendus en automatismes et dans les problèmes (ch. 7, 11 et 12).\\[3mm]
Retiré & Homothéties et rotations, triangles semblables, effet d’un agrandissement sur les aires et les volumes, repérage sur la sphère et dans un pavé, histogrammes : ces notions ne figurent plus dans le programme du cycle 4 et ne sont plus traitées.\\\bottomrule
\end{tabularx}
\par\medskip\fontsize{11}{15}\selectfont
Le vocabulaire suit le programme : quotient, fraction et nombre rationnel ;
demi-tour pour la symétrie centrale ; théorème, réciproque et contraposée ;
évènement, réunion et intersection. La notation $x\mapsto f(x)$ est utilisée
pour les fonctions. La matrice de fin de livre relie chaque rubrique du
programme aux chapitres et aux exercices.
''','nouveautes')
    docs['sommaire']=r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Troisième · Nouveau programme · Brevet 2029}
\vspace{-4mm}\sommaire\clearpage
\thispagestyle{otFront}\otPageTitre{Parcours et ressources}{Cours, défis, sujets et corrections}
\ligneSommaire{Nouveau programme : ce qui change}{nouveautes}
\ligneSommaire{Dix-huit défis d’approfondissement}{defis-debut}
\ligneSommaire{Indications progressives}{indices-debut}
\ligneSommaire{Organisation des deux brevets blancs}{bilans-guide}
\ligneSommaire{Brevet blanc A}{bilan-A-auto}
\ligneSommaire{Brevet blanc B}{bilan-B-auto}
\ligneSommaire{Comprendre quelques démonstrations}{preuves-debut}
\ligneSommaire{Corrigés des 270 exercices}{corriges-debut}
\ligneSommaire{Corrigés des 18 défis}{defi-cor-1}
\ligneSommaire{Corrigés des brevets blancs}{bilan-A-cor-auto}
\ligneSommaire{Fiches outils}{outils-debut}
\ligneSommaire{Correspondance avec le programme}{couverture-programme}
\ligneSommaire{Sources officielles et périmètre de l’édition}{references}
\clearpage
'''
    body=''
    for i,(titre,desc,url) in enumerate(SOURCES,1):
        body+=r'\par\medskip\textbf{'+str(i)+'. '+titre+r'}\par '+desc+r'\par\href{'+url.replace('%',r'\%')+r'}{\textcolor{otGreenDark}{Consulter la source officielle}}\par'+'\n'
    body+=r'''\par\bigskip Sources consultées le 23 octobre 2026. Le programme et les exemples
de mise en œuvre ont guidé le périmètre et la matrice de correspondance. Les
exercices sont originaux, non reproduits des documents officiels. Les défis et
les sujets du livre ne sont pas des sujets officiels.\par\medskip
À cette date, aucun texte propre à la session 2029 du brevet n’était publié.
La note du 11 septembre 2026 s’applique « à compter de la session 2027 » et
précise que les sujets portent sur le programme de Troisième s’il est en vigueur :
c’est la définition retenue pour les brevets blancs. Un texte ultérieur pourrait
la modifier.
'''
    docs['references']=front('Sources et édition','Références officielles · France',body,'references')
    return docs

# Quatre points de repère par chapitre, associés à des exercices identifiables.
EXEMPLES=[
[[1,2,10],[3,4,5,6,8],[7,9,15],[11,12,13,14]],
[[1,2,3,11],[4,6,7,8,12,13],[5,9,10,15],[11,12,13,14,15]],
[[1,2,5,6,7,10],[3,4,8,9],[11,13],[12,14,15]],
[[1,2,3],[4,6,8,12],[5,7,9,10],[11,13,14,15]],
[[1,2,3,4,6,7],[5,10,13],[8,9,15],[11,12,13,14,15]],
[[1,2,15],[5,8,9,10],[3,4,6,7],[11,12,13,14]],
[[1,2,13,15],[3,4,6,7,11],[5,8,12,14,15],[9,10,13,14]],
[[1,3,5,6],[2,4,7,9,14],[8,10,12],[11,13,14,15]],
[[1,2,4,6,13],[5,10,12,14],[3,7,8,9],[11,13,15]],
[[1,2,4,10,11],[3,6,7,9],[5,8,12],[12,13,14,15]],
[[1,2,3,4,13],[6,9,10,14],[7,8,10,11,14],[5,12,15]],
[[1,2,3,4,11,14],[6,7,10],[5,12,13],[8,9,15]],
[[1,2,3,4,5,8,9,13],[6,10,14],[7,15],[11,12,14]],
[[1,2,3,4,15],[5,6,7,13,14],[8,9,12],[10,11,14]],
[[1,4,10,14],[2,3,5,12],[4,6,7,11,15],[8,9,10,11,13]],
[[1,2,3,4,5,7],[5,6,10],[8,9,10,13,14],[11,12,13,15]],
[[1,2,6,10],[4,8,9,14],[3,5,7,10,11],[12,13,14,15]],
[[1,2,6,8,10],[3,5,7],[11,12,13,14],[4,9,15]]
]

# Rubriques de Troisième du programme (annexe 2) et chapitres correspondants.
CORRESPONDANCE=[
('Nombres et calculs','Nombres rationnels : forme irréductible, problèmes ; notation des ensembles de nombres (prolongement)','1'),
('','Puissances : exposants négatifs, produits et quotients, notation scientifique','2, 7'),
('','Racine carrée : équations $x^2=a$, résolution par le calcul et graphique, problèmes','2, 5, 8'),
('','Multiples et diviseurs : décomposition, critères de divisibilité, fractions (automatismes)','3, 1'),
('',r'Calcul littéral : produits et rapports, double distributivité, identités remarquables, produit nul, inéquation $ax\ge b$, analyse-synthèse','4, 5'),
('Espace et géométrie','Repérage sur une droite graduée et dans le plan (automatismes)','5, 6, 8, 9'),
('','Représentation de l’espace : solides et volumes, boule, sphère, grands cercles, sections planes','16'),
('','Triangles : Thalès, réciproque et contraposée ; cosinus, sinus, tangente ; Pythagore, cercle circonscrit et droite des milieux (automatismes)','12, 13, 14'),
('','Translations et vecteurs : vecteurs égaux, nul, opposé, somme, relation de Chasles','15'),
('Données et probabilités','Statistiques : effectifs cumulés, médiane, quartiles, boîtes à moustaches, tableur','10'),
('',r'Probabilités : relation $P(A\cup B)+P(A\cap B)=P(A)+P(B)$, expériences indépendantes, simulation et stabilisation des fréquences','11, 17'),
('Proportionnalité, fonctions','Proportionnalité : ratios, pourcentages, échelles, coefficient multiplicateur, lien avec Thalès, fonctions linéaires','6, 7, 9'),
('','Fonctions : représentations, image et antécédents, fonctions linéaires et affines, inéquations, fonction carré','8, 9'),
('Pensée informatique','Variables, conditions composées, boucle conditionnelle, blocs personnalisés, écriture de programmes','17'),
('Principes du programme','Raisonnement : conjecture, preuve, contre-exemple, réciproque, contraposée, absurde ; automatismes et résolution de problèmes','18 et tous'),
]

def couverture_programme():
    text=r'\clearpage\phantomsection\label{couverture-programme}\pdfbookmark[0]{Correspondance avec le programme}{bm-couverture-programme}'+'\n'
    text+=r'''\gdef\otChapNum{0}\pagestyle{otFront}\otPageTitre{Programme et chapitres}{Troisième · Programme 2026 applicable à la rentrée 2028}
Chaque rubrique de Troisième de l’annexe 2 de l’arrêté du 18 février 2026 est
reliée aux chapitres qui la traitent. Les pages suivantes associent ensuite quatre
repères par chapitre à des exercices précis ; les séries citées ne sont pas exhaustives.\par\medskip
{\fontsize{9.5}{12.5}\selectfont
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{32mm}Yr@{}}\toprule
Domaine & Rubrique de Troisième & Chapitres\\\midrule
'''
    for dom,rub,ch in CORRESPONDANCE:
        text+=dom+' & '+rub+' & '+ch+r'\\[1.6mm]'+'\n'
    text+=r'''\bottomrule\end{tabularx}}\par\medskip
\begin{attention}Les automatismes de Troisième s’appuient sur des notions étudiées en Quatrième sans y être automatisées. L’épreuve évalue les connaissances et compétences attendues en fin de cycle 4, déclinées par le programme de Troisième. Les défis prolongent ces notions sans ajouter d’exigence à l’examen.\end{attention}
\clearpage
'''
    for start in range(0,18,3):
        text+=r'\otPageTitre{Repères et exercices}{'+f'Chapitres {start+1} à {start+3}'+r'}\fontsize{10}{13}\selectfont'+'\n'
        for c,rows in zip(CHAPITRES[start:start+3],EXEMPLES[start:start+3]):
            text+=r'\otIntertitre{'+str(c.numero)+'. '+c.titre+r'}\begin{tabularx}{\linewidth}{@{}Yl@{}}\toprule'+'\n'
            for rep,idxs in zip(c.reperes,rows):
                refs=', '.join(r'\hyperref[exo-'+f'{c.numero}-{j}'+']{'+f'{c.numero}.{j}'+'}' for j in idxs)
                text+=rep+' & '+refs+r'\\[2mm]'+'\n'
            text+=r'\bottomrule\end{tabularx}\par\vspace{4mm}'+'\n'
        text+=r'\clearpage'+'\n'
    return text
