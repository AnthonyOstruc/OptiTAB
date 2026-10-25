from modele import CHAPITRES
SOURCES=[
('Arrêté et calendrier',r'« Programmes d’enseignement de français et de mathématiques du cycle des approfondissements (cycle 4) » : arrêté du 18 février 2026, Bulletin officiel n\textsuperscript{o} 10 du 5 mars 2026 (NOR MENE2602912A). Le nouveau programme s’applique en Quatrième à la rentrée 2027-2028.','https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A'),
('Programme de mathématiques du cycle 4','Annexe 2 de l’arrêté, rubriques « Quatrième » : automatismes et objectifs d’apprentissage en nombres et calculs, espace et géométrie, données et probabilités, proportionnalité et fonctions, pensée informatique.','https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf'),
('Exemples pour la mise en œuvre','Éduscol, « Mathématiques. Exemples pour la mise en œuvre des programmes 2026. Cycle 4 » : exemples de réussite et conseils de mise en œuvre pour la Quatrième.','https://eduscol.education.gouv.fr/sites/default/files/document/exemple-mise-en-oeuvre-c4-mathematiques0pdf-126080.pdf'),
('Ressources d’accompagnement','Éduscol : ressources d’accompagnement du programme de mathématiques au cycle 4.','https://eduscol.education.gouv.fr/5736/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-4'),
]
def front(titre,sous,body,label):
    return r'\clearpage\thispagestyle{otFront}\phantomsection\label{'+label+r'}\pdfbookmark[0]{'+titre+'}{bm-'+label+r'}\otPageTitre{'+titre+'}{'+sous+r'}\fontsize{11}{15}\selectfont'+'\n'+body+'\n'+r'\clearpage'+'\n'

def documents():
    docs={}
    docs['copyright']=r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{128mm}\fontsize{9}{13}\selectfont\color{otMuted}
{\otSemi\color{otInk}Mathématiques · Quatrième · France}\par
{\otSemi\color{otGreenDark}Édition 2027-2028 · Nouveau programme}\par\medskip
Conception et mise en page : collection OptiTAB.\par
270 exercices de chapitre, 18 défis et deux bilans annuels originaux, corrigés.\par
Charte graphique de la collection OptiTAB, du collège au lycée.\par\bigskip
Édition du 23 octobre 2026 · Année scolaire 2027-2028.\par\bigskip
Cette édition suit le nouveau programme de mathématiques du cycle 4
(arrêté du 18 février 2026, Bulletin officiel n\textsuperscript{o} 10 du 5 mars 2026),
applicable en Quatrième à partir de la rentrée 2027. Elle remplace, pour
cette rentrée, l’édition 2026-2027, conforme au programme de 2020.\par\bigskip
L’ordre, les exercices et les barèmes sont des choix éditoriaux. Les défis sont
facultatifs. Les deux bilans sont des évaluations d’entraînement originales,
sans statut d’examen officiel.\par\bigskip
Les données des situations sont construites pour apprendre ; ce ne sont pas
des relevés économiques ou scientifiques. Sauf mention contraire, les
schémas de principe ne sont pas à mesurer. Les coordonnées et graduations
explicites font foi dans les graphiques.\par\bigskip
Conserver les résultats exacts, sauf demande d’arrondi. Les réponses ajoutées
en vert dans les figures corrigées ne sont pas des données de l’énoncé.\par\bigskip
© OptiTAB, 2026.\par\otSite
\end{minipage}\clearpage
'''
    docs['avant-propos']=front('Apprendre et comprendre','Un livre pour toute la Quatrième · Nouveau programme',r'''
Ce livre accompagne une année de mathématiques en Quatrième, selon le
programme du cycle 4 publié en mars 2026 : calculer avec les relatifs et les
fractions, découvrir les puissances, raisonner en géométrie et résoudre des
problèmes qui relient plusieurs idées. Il peut être suivi dans l’ordre ou
utilisé pour reprendre une difficulté précise.\par\medskip
\begin{savoirfaire}[Une progression régulière]Chaque chapitre contient des objectifs, des prérequis, deux pages de cours et quinze exercices : cinq pour découvrir, cinq pour s’entraîner et cinq problèmes. Les corrections expliquent le choix de méthode, les étapes et l’interprétation du résultat.\end{savoirfaire}
\begin{savoirfaire}[Raisonner et démontrer]Le programme met l’accent sur la preuve : définition, propriété, réciproque et contraposée sont distinguées ; les théorèmes de la droite des milieux, de Pythagore et du cercle circonscrit sont démontrés ou expliqués. Le dessin aide à chercher ; les données et les propriétés fondent la preuve.\end{savoirfaire}
\begin{savoirfaire}[Chercher davantage]Dix-huit défis facultatifs proposent une recherche plus longue, avec deux indications séparées et une solution. Deux bilans annuels mélangent les notions. Les fiches outils et le repérage final orientent les révisions.\end{savoirfaire}
Les six compétences sont travaillées : chercher, modéliser, représenter,
raisonner, calculer et communiquer. Le progrès se mesure aussi à la capacité
d’expliquer une démarche et de corriger une erreur.
''','avant-propos')
    docs['mode-emploi']=front('Mode d’emploi','Des repères stables pour travailler seul',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Une pastille & Découvrir : calcul direct, vocabulaire, lecture d’une figure ou première application.\\[3mm]
Deux pastilles & S’entraîner : choisir un outil, combiner des étapes et vérifier.\\[3mm]
Trois pastilles & Résoudre : organiser une recherche, justifier, interpréter et contrôler.\\\bottomrule
\end{tabularx}\par\medskip
Ces niveaux sont des indications sur les tâches, pas des étiquettes sur les
élèves. Revenir à une question simple peut aider à débloquer un problème.\par\medskip
\begin{exemple}[Lire une correction]Pour $3(x-2)=x+8$, on développe : $3x-6=x+8$. On obtient $2x=14$, donc $x=7$. Le contrôle donne $3(7-2)=15=7+8$. Le résultat est utile parce que chaque étape peut être expliquée et refaite.\end{exemple}
\begin{attention}Lire les unités, les hypothèses, les mots « strictement », « au moins » et l’arrondi demandé. Une figure ressemblant à un triangle rectangle ne prouve pas qu’il l’est. Un modèle de hasard doit préciser les chances des issues.\end{attention}
Les liens du sommaire et des corrections permettent de naviguer. Pour les
scripts, les indentations et les lignes « fin » délimitent les blocs.
Après une correction, fermer le livre et refaire le passage décisif.
''','mode-emploi')
    docs['parcours']=front('Construire son parcours','Une année avec des retours réguliers',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Étape & Travail conseillé\\\midrule
Calculer & Chapitres 1 à 4 : relatifs, nombres rationnels, puissances et racines carrées.\\[3mm]
Modéliser & Chapitres 5 à 9 : calcul littéral, équations, ratios, pourcentages, grandeurs quotients et programmes de calcul.\\[3mm]
Interpréter & Chapitres 10 et 11 : moyenne, médiane, étendue, probabilités et fréquences.\\[3mm]
Démontrer & Chapitres 12 à 17 : droites remarquables et logique, translations, droite des milieux, Pythagore, cercle circonscrit, pyramides et cônes.\\[3mm]
Programmer & Chapitre 18, à reprendre pendant l’année avec les autres thèmes.\\\bottomrule
\end{tabularx}
\begin{savoirfaire}[Une séance de 35 à 50 minutes]Relire une propriété et son exemple. Chercher deux exercices sans correction. Comparer les démarches et refaire une question ratée. Terminer par une phrase : « La prochaine fois, je dois penser à… ».\end{savoirfaire}
\begin{savoirfaire}[Revenir et mélanger]Reprendre une notion quelques jours plus tard, puis quelques semaines après. Mélanger un calcul, une lecture graphique et une preuve évite de dépendre seulement du titre d’un chapitre.\end{savoirfaire}
Pour un défi, prévoir 30 à 60 minutes, éventuellement en plusieurs séances.
Pour un bilan, respecter le temps choisi puis classer les erreurs par notion.
Le tableau de bord aide à décider ce qui doit être refait seul ou avec aide.
''','parcours')
    docs['nouveautes']=front('Ce qui change','Nouveau programme de Quatrième · Rentrée 2027',r'''
Le programme de mathématiques du cycle 4 publié au Bulletin officiel du 5 mars
2026 entre en vigueur en Quatrième à la rentrée 2027. Cette édition a été
entièrement reprise pour le suivre.\par\medskip
\begin{savoirfaire}[Ce qui entre en Quatrième]Nombres rationnels : définition, inverse, fraction d’une fraction. Puissances : $a^m\times a^n=a^{m+n}$ et $a^n\times b^n=(ab)^n$. Ratios et partages proportionnels ; coefficient multiplicateur ; programmes de calcul que l’on remonte et notation $P(t)$. Étendue, effet d’une valeur extrême et tableur. Notations ensemblistes $\overline A$, $A\cap B$, $A\cup B$, $\varnothing$ ; expériences à deux épreuves ; fluctuation des fréquences. Droites remarquables, réciproque, contraposée et raisonnement par l’absurde ; droite des milieux ; triangle rectangle et cercle circonscrit ; rectangles sans équerre. Conditions avec $<$, $>$, $=$ et une variable.\end{savoirfaire}
\begin{attention}[Ce qui passe en Troisième]Théorème de Thalès ; cosinus, sinus et tangente ; puissances d’exposant négatif et écriture scientifique ; décomposition en facteurs premiers et fractions irréductibles ; conditions composées, boucles « répéter jusqu’à » et programmes à plusieurs variables.\end{attention}
\begin{exemple}[Ce qui n’est plus au programme de Quatrième]Cas d’égalité des triangles ; agrandissements et réductions avec leurs effets sur les aires et les volumes ; repérage dans un pavé droit ; grandeurs produits ; probabilités calculées par des rapports d’aires. Les sommes de fractions de dénominateurs quelconques, les diagrammes circulaires et les volumes du prisme et du cylindre relèvent de la Cinquième dans le programme 2026 : ils sont réactivés ici comme automatismes.\end{exemple}
Le repérage détaillé, objectif par objectif, figure à la fin du livre.
''','nouveautes')
    docs['sommaire']=r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Quatrième · Édition 2027-2028 · Nouveau programme}
\vspace{-4mm}\sommaire\clearpage
\thispagestyle{otFront}\otPageTitre{Parcours et ressources}{Cours, défis, bilans et corrections}
\ligneSommaire{Ce qui change avec le nouveau programme}{nouveautes}
\ligneSommaire{Dix-huit défis d’approfondissement}{defis-debut}
\ligneSommaire{Indications progressives}{indices-debut}
\ligneSommaire{Organisation des deux bilans annuels}{bilans-guide}
\ligneSommaire{Bilan A}{bilan-A-auto}
\ligneSommaire{Bilan B}{bilan-B-auto}
\ligneSommaire{Comprendre quelques démonstrations}{preuves-debut}
\ligneSommaire{Corrigés des 270 exercices}{corriges-debut}
\ligneSommaire{Corrigés des 18 défis}{defi-cor-1}
\ligneSommaire{Corrigés des bilans}{bilan-A-cor-auto}
\ligneSommaire{Fiches outils}{outils-debut}
\ligneSommaire{Le programme dans le livre}{couverture-programme}
\ligneSommaire{Objectifs officiels et chapitres}{matrice-objectifs}
\ligneSommaire{Sources officielles et périmètre de l’édition}{references}
\clearpage
'''
    body=''
    for i,(title,desc,url) in enumerate(SOURCES,1):
        body+=r'\par\medskip\textbf{'+str(i)+'. '+title+r'}\par '+desc+r'\par\href{'+url+r'}{\textcolor{otGreenDark}{Consulter la source officielle}}\par'+'\n'
    body+=r'''\par\bigskip Sources consultées le 23 octobre 2026. Les cours sont rédigés pour ce
livre ; les exercices, défis et bilans sont originaux, sans reproduction des
exemples officiels.\par\medskip
Périmètre de Quatrième : produits et quotients de relatifs ; opérations sur les
rationnels ; puissances d’exposant positif ; racine carrée et encadrement ;
distributivité simple et preuves littérales ; équations $ax+b=cx+d$ ; ratios,
pourcentages et grandeurs quotients ; programmes de calcul et dépendance ;
moyenne pondérée, médiane et étendue ; probabilités avec notations ensemblistes
et deux épreuves ; droites remarquables et logique ; translations ; droite des
milieux ; Pythagore, réciproque et contraposée ; cercle circonscrit au triangle
rectangle ; pyramides et cônes ; conditions et variable en programmation.
Les défis approfondissent ces outils sans ajouter d’exigence officielle.
'''
    docs['references']=front('Sources et édition','Références officielles · France',body,'references')
    return docs

# Chaque repère renvoie à un groupe précis d'exercices du chapitre.
EXEMPLES=[
[[1,2,4,6,14],[3,9,13],[7,8,10,15],[5,11,12]],
[[1,2,4],[3,7,8,14],[5,6,12,13],[9,10,11,15]],
[[1,2,4],[3,5,13],[6,7,8,9,10],[11,12,14,15]],
[[1,2],[3,5,9],[4,6,8,10,14],[7,11,12,13,15]],
[[1,2,3,10],[4,6,7,11],[5,8,13],[9,12,14,15]],
[[1,9],[2,3,4,6,7,8],[5,11,12,13,14],[10,15]],
[[1,2,3,6,11],[4,5,15],[9,10,12,14],[7,8,13]],
[[1,2,3,6,7,13],[11,12],[4,5,8,14],[9,10,15]],
[[1,2,11],[3,11],[4,10,12,13,15],[5,6,7,8,9,14]],
[[1,2,5,6,11],[3,7,8,12,15],[4,9,13],[10,14]],
[[1,3,4,10,14],[2,5,6,15],[7,8,9],[11,12,13]],
[[1,5,10,11],[2,4,9],[6,8,12,14],[3,7,13,15]],
[[1,2,3,10,11],[4,9,14,15],[6,7,12],[5,8,13]],
[[2,5,8,10],[1,3,6,9],[4,7,12],[11,13,14,15]],
[[1,3,7,9],[2,4,8,12],[5,6,10],[11,13,14,15]],
[[1,4,13],[2,6],[3,5,7,9,10,15],[8,11,12,14]],
[[1,5,6],[9,10,11],[2,3,4,7,8,12],[13,14,15]],
[[1,2,5,13],[4,6,9,15],[3,7,8,11],[10,12,14]]
]

# Matrice : objectifs du programme de Quatrième (annexe 2) et chapitres du livre.
OBJECTIFS=[
('Nombres et calculs',[
('Multiplier deux relatifs, d’abord avec un seul facteur négatif, puis deux, grâce à la distributivité',[1]),
('Diviser deux relatifs ; calculer un enchaînement d’opérations',[1]),
(r'Utiliser le vocabulaire (somme, quotient\ldots) d’un programme de calcul et inversement',[1,9]),
('Simplifier une fraction ; définir un nombre rationnel et exprimer son opposé',[2]),
('Produit de rationnels ; fraction d’une fraction, d’un nombre, d’une quantité',[2]),
('Inverse d’un nombre et d’une fraction ; division de fractions ; expressions et problèmes',[2]),
('Puissances d’exposant positif ; produits de puissances d’un même nombre ou de même exposant ; problèmes',[3]),
('Définition de la racine carrée ; encadrement par deux entiers consécutifs',[4]),
('Produire des formules et tester leur vraisemblance ; démontrer par le calcul algébrique',[5,9]),
('Distributivité simple pour développer et factoriser',[5]),
('Résoudre $ax+b=c$ ; mettre en équation avec $ax+b=cx+d$ ; conjecturer avec un tableur ou un algorithme',[6]),
]),
('Proportionnalité, fonctions',[
('Grandeurs quotients, avec ou sans unités',[7,8]),
('Comparer par un rapport ou un ratio ; égalités de rapports ; quatrième proportionnelle',[7]),
('Calculer avec des pourcentages ; coefficient multiplicateur',[8]),
('Résoudre des problèmes de partage proportionnel',[7]),
('Appliquer un programme de calcul à un nombre puis à une variable ; le remonter',[9]),
('Formule littérale, graphique et dépendance d’une grandeur en fonction d’une autre',[9]),
]),
('Organisation et gestion de données, probabilités',[
('Moyenne pondérée d’une série de petit effectif',[10]),
('Médiane et étendue ; effet d’une valeur extrême ; problèmes et comparaison de séries',[10]),
('Utiliser le tableur pour la moyenne, la médiane et l’étendue',[10]),
('Vocabulaire et notations ensemblistes ; complémentaire, réunion, intersection, ensemble vide',[11]),
('Probabilité d’un événement et de l’événement contraire ; expériences à deux épreuves',[11]),
('Distributions fréquentielle et probabiliste ; fluctuation des fréquences',[11]),
]),
('Espace et géométrie',[
('Droites remarquables (automatismes) ; réciproque, contraposée et raisonnement par l’absurde',[12,15]),
('Effet d’une translation ; lien avec les parallélogrammes et les angles ; conservations',[13]),
('Symétrie axiale, demi-tour, parallélogrammes particuliers (automatismes)',[13]),
('Les trois théorèmes relatifs à la droite des milieux',[14]),
('Théorème de Pythagore, réciproque et contraposée',[15]),
('Triangle rectangle et cercle circonscrit ; centre ; rectangles sans équerre',[16]),
('Pyramide et cône de révolution : reconnaître, représenter, calculer le volume',[17]),
('Repérage sur une droite graduée et dans un repère (automatismes)',[1,9,13]),
]),
('Pensée informatique',[
('Représenter des conditions simples ; écrire des instructions conditionnelles',[18]),
('Manipuler une variable ; écrire un programme simple ; modifier un programme donné',[18]),
]),
]

def matrice():
    def refs(ch):
        return ', '.join(r'\hyperref[chap-'+str(c)+']{ch. '+str(c)+'}' for c in ch)
    pages=[OBJECTIFS[:2],OBJECTIFS[2:]]
    text=''
    for k,groupe in enumerate(pages):
        if k==0:text+=r'\clearpage\phantomsection\label{matrice-objectifs}\pdfbookmark[1]{Objectifs officiels et chapitres}{bm-matrice-objectifs}'
        else:text+=r'\clearpage'
        text+=r'\otPageTitre{Objectifs officiels et chapitres}{Annexe 2 du programme 2026 · rubriques de Quatrième}\fontsize{9.5}{12.5}\selectfont'+'\n'
        for domaine,lignes in groupe:
            text+=r'\otIntertitre{'+domaine+r'}\begin{tabularx}{\linewidth}{@{}Yr@{}}\toprule'+'\n'
            for obj,ch in lignes:text+=obj+' & '+refs(ch)+r'\\[1.2mm]'+'\n'
            text+=r'\bottomrule\end{tabularx}\par\vspace{3mm}'+'\n'
    text+=r'\clearpage'+'\n'
    return text

def couverture_programme():
    text=r'\clearpage\phantomsection\label{couverture-programme}\pdfbookmark[0]{Le programme dans le livre}{bm-couverture-programme}'
    text+=r'''\gdef\otChapNum{0}\pagestyle{otFront}\otPageTitre{Le programme dans le livre}{Quatrième · Nouveau programme 2026 · Lecture par notions}
Cette annexe relie le programme officiel au livre. Les pages suivantes
associent d’abord les quatre repères de chaque chapitre à des exercices
précis, puis chaque objectif d’apprentissage de l’annexe 2 du programme
aux chapitres qui le travaillent. Les séries indiquées ne sont pas
exhaustives ; les cours et les défis complètent ce parcours.\par\bigskip
Points à retrouver : multiplication des relatifs justifiée par la distributivité (1),
inverse et fraction d’une fraction (2), produits de puissances (3), encadrement
d’une racine (4), preuves littérales (5), conjectures au tableur (6), ratios et
partages (7), coefficient multiplicateur (8), programmes remontés et notation
$P(t)$ (9), étendue et valeur extrême (10), deux épreuves et fluctuation (11),
réciproque et contraposée (12), translations (13), droite des milieux (14),
Pythagore (15), cercle circonscrit (16), pyramides et cônes (17), conditions
et variable (18).\par\bigskip
\begin{attention}Les exercices à trois pastilles et les défis sont des choix d’entraînement. Ils ne changent pas le programme officiel et ne constituent pas une liste d’exigences supplémentaires.\end{attention}
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
    text+=matrice()
    return text
