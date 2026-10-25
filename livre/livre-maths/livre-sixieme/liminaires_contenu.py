from modele import CHAPITRES
SOURCES=[
('Arrêté et calendrier','Arrêté du 10 avril 2025 publié au BO n° 16 du 17 avril 2025 : le programme de mathématiques du cycle 3 s’applique en classe de Sixième depuis la rentrée de l’année scolaire 2025-2026.','https://www.education.gouv.fr/bo/2025/Hebdo16/MENE2504620A'),
('Programme officiel de mathématiques du cycle 3','Rubriques « Sixième » : nombres entiers et décimaux, fractions, algèbre ; grandeurs et mesures ; espace et géométrie ; organisation et gestion de données et probabilités ; proportionnalité ; initiation à la pensée informatique.','https://www.education.gouv.fr/sites/default/files/programme-de-math-matiques-pour-le-cycle-3-439827.pdf'),
('Accompagnement du programme','Éduscol : ressources d’accompagnement du programme de mathématiques au cycle 3, dont les exemples de réussite en Sixième, les schémas en barres et la résolution de problèmes.','https://eduscol.education.gouv.fr/5712/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-3'),
]
def front(titre,sous,body,label):
    return r'\clearpage\thispagestyle{otFront}\phantomsection\label{'+label+r'}\pdfbookmark[0]{'+titre+'}{bm-'+label+r'}\otPageTitre{'+titre+'}{'+sous+r'}\fontsize{11}{15}\selectfont'+'\n'+body+'\n'+r'\clearpage'+'\n'
def documents():
    docs={}
    docs['copyright']=r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{128mm}\fontsize{9}{13}\selectfont\color{otMuted}
{\otSemi\color{otInk}Mathématiques · Sixième · France}\par\medskip
Conception et mise en page : collection OptiTAB.\par
315 exercices de chapitre, 21 défis et deux bilans originaux, tous corrigés.\par
Édition du 23 octobre 2026 · Année scolaire 2026-2027.\par\bigskip
Cette édition suit le programme de mathématiques du cycle 3 publié au
BO n° 16 du 17 avril 2025, applicable en Sixième depuis la rentrée 2025.
Les rubriques « Sixième » de chaque domaine ont guidé le périmètre.\par\bigskip
L’ordre des chapitres, les situations et les personnages sont des choix
éditoriaux. Les défis sont facultatifs. Les bilans sont des entraînements
originaux, sans statut d’examen officiel.\par\bigskip
Les données numériques des problèmes sont construites pour apprendre ;
les données réelles citées (population mondiale, distances dans le
système solaire, calendriers) sont arrondies. Les figures de principe ne
sont pas à mesurer, sauf consigne explicite ; graduations et quadrillages
font foi.\par\bigskip
Les réponses ajoutées en vert aux figures corrigées ne sont pas des données
de l’énoncé. Les calculs du livre se font sans calculatrice, sauf mention
contraire dans un défi.\par\bigskip
© OptiTAB, 2026.\par\otSite
\end{minipage}\clearpage
'''
    docs['avant-propos']=front('Apprendre et comprendre','Un livre pour toute l’année de Sixième',r'''
Ce livre accompagne l’entrée au collège : nombres décimaux et fractions,
calcul, proportionnalité, grandeurs, géométrie des distances et des angles,
données, hasard et premiers pas en programmation. Il consolide les acquis
de l’école et prépare le cycle 4, en développant le raisonnement.\par\medskip
\begin{savoirfaire}[Du simple au problème]Chaque chapitre propose ses objectifs,
ses prérequis, deux pages de cours en quatre sections et quinze exercices :
cinq de découverte, cinq d’entraînement et cinq problèmes. Chaque correction
explique la méthode et le sens du résultat.\end{savoirfaire}
\begin{savoirfaire}[Des figures pour comprendre]Demi-droites graduées, bandes,
schémas en barres, rapporteurs, constructions au compas, symétries,
assemblages de cubes, diagrammes et programmes par blocs accompagnent les
notions. Les constructions demandées apparaissent en vert dans les corrigés.\end{savoirfaire}
\begin{savoirfaire}[Chercher et oser]Vingt-et-un défis facultatifs offrent deux
indications séparées et une solution expliquée. Deux bilans mélangent les
chapitres pour apprendre à choisir ses outils.\end{savoirfaire}
Chercher sans réussir du premier coup fait partie des mathématiques :
garder ses essais, les expliquer, puis comparer avec la méthode proposée.
''','avant-propos')
    docs['mode-emploi']=front('Mode d’emploi','Des repères pour travailler seul ou accompagné',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Une pastille & Découverte : appliquer directement le cours.\\[3mm]
Deux pastilles & Entraînement : choisir une méthode, organiser ses étapes.\\[3mm]
Trois pastilles & Problèmes : comprendre, modéliser, calculer, répondre.\\\bottomrule
\end{tabularx}\par\medskip
Ces pastilles décrivent les tâches ; elles ne classent pas les élèves.\par\medskip
\begin{exemple}[Lire une correction]Pour « $7\times\square=3$ », on utilise la
définition du quotient : le nombre caché est $\frac37$. Contrôle :
$7\times\frac37=3$. Refaire ensuite le raisonnement sans regarder aide
plus que recopier la réponse.\end{exemple}
\begin{attention}Lire l’énoncé en entier avant de calculer. Un mot comme
« plus » ou « moins » ne décide pas de l’opération : c’est la situation
qui la choisit. En géométrie, les consignes nomment toujours les objets :
la droite (AB), le segment [AB], la demi-droite [AB).\end{attention}
Chercher d’abord, ouvrir le corrigé ensuite. Après lecture, refaire le
passage difficile sur une feuille : c’est là que l’on apprend.
''','mode-emploi')
    docs['parcours']=front('Construire son parcours','Une année avec des retours réguliers',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Nombres & 1 à 6 : milliards, décimaux, arrondis, produits, divisions, fractions quotients et calculs de fractions.\\[3mm]
Modéliser & 7 à 9 : pourcentages, schémas en barres, motifs, proportionnalité et échelles.\\[3mm]
Mesurer & 10 à 12 : longueurs et nombre $\pi$, aires et conversions, durées et heures décimales.\\[3mm]
Construire & 13 à 18 : distances, cercles, médiatrice, angles, triangles, symétrie axiale, solides et volumes.\\[3mm]
Organiser & 19 à 21 : enquêtes et données, probabilités, instructions et répétitions.\\\bottomrule
\end{tabularx}
\begin{savoirfaire}[Une séance qui fonctionne]Relire un exemple du cours,
chercher deux exercices sans corrigé, comparer, puis refaire la question
manquée. Vingt minutes régulières valent mieux qu’une longue séance
isolée.\end{savoirfaire}
\begin{savoirfaire}[Revenir et mélanger]Reprendre une notion quelques jours
plus tard, puis au moment des bilans. Les problèmes mélangent
volontairement les chapitres : c’est ainsi qu’on apprend à choisir.\end{savoirfaire}
Les défis demandent de 20 à 45 minutes, parfois en plusieurs fois.
Le tableau de bord suit les réussites et les reprises au fil de l’année.
''','parcours')
    docs['sommaire']=r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Sixième · France · Programme 2025}
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
Périmètre de la Sixième : entiers jusqu’aux milliards ; écritures d’un
décimal (virgule, fraction décimale, nombre mixte, pourcentage) ; arrondis
à l’unité, au dixième et au centième, y compris de nombres non décimaux ;
produit de deux décimaux ; division euclidienne par un entier inférieur à
100 et division décimale par un entier inférieur à 10 ; fraction quotient,
égalités à trous, graduation d’un segment ; égalités, comparaisons,
sommes et différences de fractions, produit par un entier ; pourcentages ;
schémas en barres et motifs évolutifs, sans lettres formelles ;
périmètre du disque, conversions d’aires entre m$^2$, dm$^2$ et cm$^2$,
aires du carré et du rectangle, cm$^3$ ; durées en base soixante et en
heures décimales ; distances, milieu, cercle et disque, médiatrice,
angles, bissectrice, triangles, somme des angles, cercle circonscrit ;
symétrie axiale sur quadrillage, papier pointé et papier uni ; assemblages
de cubes ; enquêtes, tableaux et filtrage ; probabilités entre 0 et 1 et
fréquences ; instructions, séquences, entrées, sorties et répétitions.\par\medskip
La proportionnalité est traitée dans le cadre des grandeurs, par la
linéarité et le retour à l’unité, avec tableaux et échelles ; conformément
au programme, le produit en croix n’est pas enseigné. L’ordre des
chapitres est une proposition de progression.
'''
    docs['references']=front('Sources et édition','Références officielles · France',body,'references')
    return docs

# Chaque repère renvoie à un groupe précis d'exercices du chapitre.
EXEMPLES=[
[[1,2,10,11,12],[3,6,15],[4,5,9,13],[7,8,14]],
[[1,2,8],[3,4,11,15],[6,7,13],[5,9,10,12,14]],
[[1,2,11,14],[3,4],[5,6,7,9,12],[8,10,13,15]],
[[1,13],[2,3,6,10,15],[4,5,12],[7,8,9,11,14]],
[[1,2,5,13],[4,6,9],[3,7,12,15],[8,10,11,14]],
[[1,2,10],[3,6,9],[4,7,11],[5,8,12,13,14,15]],
[[1,15],[2,3],[4,6,8,9,10,14],[5,7,11,12,13]],
[[2,11],[1,5,6,7],[4,10,14],[3,8,9,12,13,15]],
[[1,8,15],[2,4,7,10,12],[3,6,13],[5,9,11,14]],
[[1,2,5,13],[3,8,12,15],[4,9,11,14],[6,7,10]],
[[1,7,8],[2,3],[5,6,11,14],[4,9,10,12,13,15]],
[[1,2,3,10],[4,5,9,11,12],[6,13,14],[7,8,15]],
[[1,2],[3,8,14,15],[4,5,6,9],[7,10,11,12,13]],
[[1,2],[3,6],[4,5,7,8,14,15],[9,10,11,12,13]],
[[1,2,5,15],[3,4,6,12],[7,8,9,11],[10,13,14]],
[[5,6,7,8],[2,3,4,9],[1,13,14,15],[10,11,12]],
[[1,14,15],[2,3,4,5,9],[6,7,8,10,13],[11,12]],
[[1,2],[4,7,14],[3,5,6,8,10,12,13],[9,11,15]],
[[1,14],[2,6,7,10],[3,4,5,13],[8,9,11,12,15]],
[[1,5,10],[2,4,6,7,11],[3,9,12,14,15],[8,13]],
[[1,3],[2,5,9],[6,7,10,12,13,14],[4,8,11,15]],
]
assert all(sorted(sum(r,[]))==list(range(1,16)) for r in EXEMPLES)
def couverture_programme():
    text=r'\clearpage\phantomsection\label{couverture-programme}\pdfbookmark[0]{Repérage du programme}{bm-couverture-programme}'
    text+=r'''\gdef\otChapNum{0}\pagestyle{otFront}
\otPageTitre{Repérage du programme}{Sixième · Programme 2025 du cycle 3}
Cette matrice relie les objectifs d’apprentissage du programme aux
exercices du livre. Les cours complètent ces repères, notamment pour
le vocabulaire, les représentations et les méthodes de construction.\par\bigskip
Les six domaines du programme sont couverts : nombres, calcul et
résolution de problèmes, y compris l’algèbre (chapitres 1 à 8) ;
grandeurs et mesures (10 à 12, et les volumes au chapitre 18) ; espace et
géométrie (13 à 18) ; organisation et gestion de données et probabilités
(19 et 20) ; proportionnalité (9, avec les échelles) ; initiation à la
pensée informatique (21, et plusieurs défis).\par\bigskip
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
