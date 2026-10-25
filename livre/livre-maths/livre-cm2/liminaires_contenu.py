from modele import CHAPITRES
SOURCES=[
('Arrêté et calendrier','Arrêté du 10 avril 2025 publié au BO n° 16 du 17 avril 2025, article 3 : le programme de mathématiques du cycle 3 s’applique en CM2 à la rentrée de l’année scolaire 2026-2027.','https://www.education.gouv.fr/bo/2025/Hebdo16/MENE2504620A'),
('Programme officiel de mathématiques du cycle 3','Rubriques « Cours moyen deuxième année » : nombres, calcul et résolution de problèmes ; grandeurs et mesures ; espace et géométrie ; données et probabilités ; proportionnalité ; initiation à la pensée informatique.','https://www.education.gouv.fr/sites/default/files/programme-de-math-matiques-pour-le-cycle-3-439827.pdf'),
('Accompagnement du programme','Éduscol : ressources d’accompagnement du programme de mathématiques au cycle 3, dont la résolution de problèmes en quatre phases et les schémas en barres.','https://eduscol.education.gouv.fr/5712/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-3'),
]
def front(titre,sous,body,label):
    return r'\clearpage\thispagestyle{otFront}\phantomsection\label{'+label+r'}\pdfbookmark[0]{'+titre+'}{bm-'+label+r'}\otPageTitre{'+titre+'}{'+sous+r'}\fontsize{11}{15}\selectfont'+'\n'+body+'\n'+r'\clearpage'+'\n'
def documents():
    docs={}
    docs['copyright']=r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{128mm}\fontsize{9}{13}\selectfont\color{otMuted}
{\otSemi\color{otInk}Mathématiques · CM2 · France}\par\medskip
Conception et mise en page : collection OptiTAB.\par
315 exercices de chapitre, 21 défis et deux bilans originaux, tous corrigés.\par
Édition du 23 octobre 2026 · Année scolaire 2026-2027.\par\bigskip
Cette édition suit le programme de mathématiques du cycle 3 publié au
BO n° 16 du 17 avril 2025, applicable en CM2 depuis la rentrée 2026.
Les rubriques « cours moyen deuxième année » ont guidé le périmètre.\par\bigskip
L’ordre des chapitres, les situations et les personnages sont des choix
éditoriaux. Les défis sont facultatifs. Les bilans sont des entraînements
originaux, sans statut d’examen officiel.\par\bigskip
Les données numériques des problèmes sont construites pour apprendre.
Les dessins géométriques de principe ne sont pas à mesurer sauf consigne
explicite. Les graduations et quadrillages des figures font foi.\par\bigskip
Les réponses ajoutées en vert aux figures corrigées ne sont pas des données
de l’énoncé. Conformément au programme, la calculatrice n’est pas utilisée.\par\bigskip
© OptiTAB, 2026.\par\otSite
\end{minipage}\clearpage
'''
    docs['avant-propos']=front('Apprendre et comprendre','Un livre pour toute l’année de CM2',r'''
Ce livre accompagne la dernière année de l’école élémentaire : grands
nombres, fractions et décimaux, mesures, constructions, données et hasard.
Il prépare l’entrée en Sixième en consolidant les méthodes et en
développant le raisonnement.\par\medskip
\begin{savoirfaire}[Du simple au problème]Chaque chapitre propose les objectifs,
les prérequis, deux à quatre pages de cours et quinze exercices : cinq
de découverte, cinq d’entraînement et cinq problèmes. Chaque correction
explique la méthode et le sens du résultat.\end{savoirfaire}
\begin{savoirfaire}[Des figures pour comprendre]Demi-droites graduées, bandes
de fractions, quadrillages, horloges, angles, patrons, arbres et diagrammes
accompagnent les notions qui en ont besoin. Les constructions demandées
apparaissent en vert dans les corrigés.\end{savoirfaire}
\begin{savoirfaire}[Chercher et oser]Vingt-et-un défis facultatifs offrent deux
indications séparées et une solution expliquée. Deux bilans mélangent
les chapitres pour apprendre à choisir ses outils.\end{savoirfaire}
Chercher sans réussir du premier coup fait partie des mathématiques :
garder ses essais, les raconter, puis comparer avec la méthode proposée.
''','avant-propos')
    docs['mode-emploi']=front('Mode d’emploi','Des repères pour travailler seul ou accompagné',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Une pastille & Découverte : lire, écrire, calculer directement.\\[3mm]
Deux pastilles & Entraînement : choisir une méthode, organiser ses étapes.\\[3mm]
Trois pastilles & Problèmes : raconter, modéliser, calculer et répondre.\\\bottomrule
\end{tabularx}\par\medskip
Ces pastilles décrivent les tâches ; elles ne classent pas les élèves.\par\medskip
\begin{exemple}[Lire une correction]Pour « $178-\square=6\times8$ », on calcule
d’abord le côté connu : $6\times8=48$. Le nombre caché vaut alors
$178-48=130$, et le contrôle $178-130=48$ confirme. Refaire ensuite
le calcul sans regarder aide plus que recopier la réponse.\end{exemple}
\begin{attention}Lire l’énoncé en entier avant de calculer. Un mot comme
« plus » ou « de moins » ne décide pas de l’opération : c’est l’histoire
du problème qui la choisit. Toujours écrire l’unité dans la réponse.\end{attention}
Chercher d’abord, ouvrir le corrigé ensuite. Après lecture, refaire le
passage difficile sur une feuille : c’est là que l’on apprend.
''','mode-emploi')
    docs['parcours']=front('Construire son parcours','Une année avec des retours réguliers',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Calculer & 1 à 5 : nombres jusqu’au milliard, opérations, diviseurs, divisions, programmes et suites.\\[3mm]
Partager & 6 à 10 : fractions, sommes de fractions, fraction d’une quantité, décimaux jusqu’aux millièmes.\\[3mm]
Mesurer & 11 à 14 : longueurs, masses, contenances, aires, angles et durées en secondes.\\[3mm]
Construire & 15 à 18 : programmes de construction, polygones, symétrie et solides.\\[3mm]
Modéliser & 19 à 21 : proportionnalité, données et probabilités « a chances sur b ».\\\bottomrule
\end{tabularx}
\begin{savoirfaire}[Une séance qui fonctionne]Relire un exemple du cours,
chercher deux exercices sans corrigé, comparer, puis refaire la question
manquée. Quinze minutes régulières valent mieux qu’une longue séance
isolée.\end{savoirfaire}
\begin{savoirfaire}[Revenir et mélanger]Reprendre une notion quelques jours
plus tard, puis au moment des bilans. Les problèmes mélangent
volontairement les chapitres : c’est ainsi qu’on apprend à choisir.\end{savoirfaire}
Les défis demandent entre 20 et 45 minutes, parfois en plusieurs fois.
Le tableau de bord suit les réussites et les reprises au fil de l’année.
''','parcours')
    docs['sommaire']=r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{CM2 · France · Programme 2025}
\vspace{-4mm}\sommaire\clearpage
\thispagestyle{otFront}\otPageTitre{Parcours et ressources}{Cours, recherches et corrections}
\ligneSommaire{Vingt-et-un défis d’approfondissement}{defis-debut}
\ligneSommaire{Indications progressives}{indices-debut}
\ligneSommaire{Organisation des deux bilans}{bilans-guide}
\ligneSommaire{Bilan A}{bilan-A-auto}
\ligneSommaire{Bilan B}{bilan-B-auto}
\ligneSommaire{Comprendre pourquoi}{preuves-debut}
\ligneSommaire{Corrigés des 315 exercices}{corriges-debut}
\ligneSommaire{Corrigés des 21 défis}{defi-cor-1}
\ligneSommaire{Corrigés des bilans}{bilan-A-cor-auto}
\ligneSommaire{Fiches outils}{outils-debut}
\ligneSommaire{Repérage du programme dans le livre}{couverture-programme}
\ligneSommaire{Sources officielles et périmètre}{references}\clearpage
'''
    body=''
    for i,(title,desc,url) in enumerate(SOURCES,1):
        body+=r'\par\medskip\textbf{'+str(i)+'. '+title+r'}\par '+desc+r'\par\href{'+url+r'}{\textcolor{otGreenDark}{Consulter la source officielle}}\par'+'\n'
    body+=r'''\par\bigskip Sources consultées le 23 octobre 2026.
Les cours sont rédigés pour ce livre ; les exercices, défis et bilans
sont originaux.\par\medskip
Périmètre du CM2 : nombres entiers jusqu’à 999 999 999 ; diviseurs
d’un nombre jusqu’à 100, liste complète jusqu’à 30, diviseurs et
multiples communs ; fractions de dénominateur au plus 60 et fractions
décimales jusqu’aux millièmes ; produit d’un entier par une fraction ;
divisions décimales par un diviseur à un chiffre ; programmes de calcul
jusqu’à trois instructions ; unités d’aire cm², dm², m² et aires du carré
et du rectangle ; angle droit de 90 degrés, sans rapporteur ; durées en
heures, minutes et secondes ; trapèzes, pentagones et hexagones ;
symétrie sur quadrillage, y compris le long d’une diagonale ; patrons du
cube et du pavé ; diagrammes circulaires ; probabilités « a chances
sur b », arbres et tableaux pour deux étapes.\par\medskip
La proportionnalité se traite par des raisonnements en langage naturel
(« trois fois plus, trois fois moins », addition de situations), sans
tableau de proportionnalité, sans coefficient ni produit en croix,
conformément au programme du cours moyen. Les défis approfondissent les
outils du livre et restent facultatifs. L’ordre des chapitres est une
proposition de progression.
'''
    docs['references']=front('Sources et édition','Références officielles · France',body,'references')
    return docs

# Chaque repère renvoie à un groupe précis d'exercices du chapitre.
EXEMPLES=[
[[1,2,13],[3,4,6,12],[5,8,9,10,14,15],[7,11]],
[[1,2,5,10],[3,4,15],[6,7,8,9,14],[11,12,13]],
[[1,2,5,8,10,15],[3,4,9,14],[6,7],[11,12,13]],
[[1,2,7,9],[3,4,5,8,10],[6,12,15],[11,13,14]],
[[1,7,10,15],[2,3,4,8,13],[5,6,9,14],[11,12]],
[[1,2,15],[3,4,9,13],[6,7,8],[5,10,11,12,14]],
[[1,2,5],[3,4,14],[6,7,8,9,10,15],[11,12,13]],
[[1,2,5,8],[3,4,9,14],[7,15],[6,10,11,12,13]],
[[1,2,3,4,13],[5,6,11,12,15],[7,8,10],[9,14]],
[[1,2,9,10],[3,15],[4,5,6,7,8],[11,12,13,14]],
[[1,2,3,15],[4,8],[5,6,7,13],[9,10,11,12,14]],
[[4,5,8],[1,2,6,10],[7,12],[3,9,11,13,14,15]],
[[1,2,10,14],[3,15],[6,7,8,9],[4,5,11,12,13]],
[[1,2,3,9],[4,11,15],[6,7,8,14],[5,10,12,13]],
[[1,2,3],[4,8,12],[5,6,14],[7,9,10,11,13,15]],
[[2,3],[4,5,7,8,11,13],[1,9,10,12,14],[6,15]],
[[1,8,13],[2,3,9,14],[4,5,6,7,11],[10,12,15]],
[[1,2,3,4],[5,6,8],[7,9],[10,11,12,13,14,15]],
[[1,9,15],[2,3,7],[4,5,6,11,12],[8,10,13,14]],
[[1,2,7,12],[3,4,6,8],[5,9],[10,11,13,14,15]],
[[1,2,3,13],[4,5,10,12,14,15],[6],[7,8,9,11]],
]
def couverture_programme():
    text=r'\clearpage\phantomsection\label{couverture-programme}\pdfbookmark[0]{Repérage du programme}{bm-couverture-programme}'
    text+=r'''\gdef\otChapNum{0}\pagestyle{otFront}
\otPageTitre{Repérage du programme}{CM2 · Programme 2025 du cycle 3}
Cette matrice relie les objectifs d’apprentissage du programme aux
exercices du livre. Les cours complètent ces repères, notamment pour
le vocabulaire, les représentations et les méthodes de construction.\par\bigskip
Les six domaines du programme sont couverts : nombres, calcul et
résolution de problèmes ; grandeurs et mesures ; espace et géométrie ;
organisation et gestion de données et probabilités ; proportionnalité ;
initiation à la pensée informatique, travaillée dans les chapitres 5,
15 et 18 ainsi que dans plusieurs défis.\par\bigskip
\begin{attention}Les niveaux de difficulté et les défis sont des choix
d’entraînement. Ils ne constituent pas une liste d’obligations
supplémentaires au programme officiel.\end{attention}\clearpage
'''
    for start in range(0,21,3):
        text+=r'\otPageTitre{Repères et exercices}{'+f'Chapitres {start+1} à {min(start+3,21)}'+r'}\fontsize{10}{13}\selectfont'+'\n'
        for c,rows in zip(CHAPITRES[start:start+3],EXEMPLES[start:start+3]):
            text+=r'\otIntertitre{'+str(c.numero)+'. '+c.titre+r'}\begin{tabularx}{\linewidth}{@{}Yl@{}}\toprule'+'\n'
            for rep,idxs in zip(c.reperes,rows):
                refs=', '.join(r'\hyperref[exo-'+f'{c.numero}-{j}'+']{'+f'{c.numero}.{j}'+'}' for j in idxs)
                text+=rep+' & '+refs+r'\\[2mm]'+'\n'
            text+=r'\bottomrule\end{tabularx}\par\vspace{4mm}'+'\n'
        text+=r'\clearpage'+'\n'
    return text
