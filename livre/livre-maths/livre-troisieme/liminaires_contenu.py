from modele import CHAPITRES

SOURCES=[
('Programme actuellement applicable','Bulletin officiel du 30 juillet 2020, programme du cycle 4.','https://www.education.gouv.fr/bo/20/Hebdo31/MENE2018714A.htm'),
('Attendus de fin de Troisième','Éduscol, attendus annuels de mathématiques, document de 11 pages.','https://eduscol.education.gouv.fr/sites/default/files/document/18-maths-3e-attendus-eduscol1114748pdf-74688.pdf'),
('Repères annuels du cycle 4','Éduscol, progression annuelle et programmation par blocs.','https://eduscol.education.gouv.fr/sites/default/files/document/26-maths-c4-reperes-eduscol1114756pdf-74694.pdf'),
('Calendrier des nouveaux programmes','Éduscol : nouveau programme de 2026 en Troisième à la rentrée 2028.','https://eduscol.education.gouv.fr/5736/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-4'),
('Définition du brevet à compter de 2027','Note du 11 septembre 2026, BO spécial n° 4 du 17 septembre 2026.','https://www.education.gouv.fr/bo/2026/Hebdo4/MENE2623228N'),
('Différencier les entraînements','Éduscol : accompagnement en mathématiques en 4e, 3e et 2de.','https://eduscol.education.gouv.fr/6858/accompagner-les-eleves-en-mathematiques-4e-3e-et-2de'),
('Validité des repères en 2026-2027','Éduscol : repères et attendus annuels, mise à jour de septembre 2026.','https://eduscol.education.gouv.fr/6910/reperes-annuels-de-progression-et-attendus-de-fin-d-annee-du-cp-la-troisieme'),
]

def front(titre,sous,body,label):
    return r'\clearpage\thispagestyle{otFront}\phantomsection\label{'+label+r'}\pdfbookmark[0]{'+titre+'}{bm-'+label+r'}\otPageTitre{'+titre+'}{'+sous+r'}\fontsize{11}{15}\selectfont'+'\n'+body+'\n'+r'\clearpage'+'\n'

def documents():
    docs={}
    docs['copyright']=r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{128mm}\fontsize{9}{13}\selectfont\color{otMuted}
{\otSemi\color{otInk}Mathématiques · Troisième · Brevet 2027}\par\medskip
Conception et mise en page : collection OptiTAB.\par
270 exercices de chapitre, 18 défis et deux brevets blancs originaux, corrigés.\par
Charte graphique de la collection OptiTAB de Terminale, Première et Seconde.\par\bigskip
Édition du 21 octobre 2026 · France · Année scolaire 2026-2027.\par\bigskip
Le livre suit les attendus de Troisième actuellement applicables et réactive
les connaissances du cycle 4 nécessaires. Le nouveau programme publié en 2026
ne s’appliquera en Troisième qu’en 2028-2029. Le format des brevets blancs
s’appuie sur la définition officielle de septembre 2026, applicable à compter
de la session 2027.\par\bigskip
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
    docs['avant-propos']=front('Apprendre et comprendre','Un livre pour toute l’année',r'''
Ce livre accompagne la classe de Troisième et la préparation du brevet :
consolider les calculs, comprendre les nouvelles notions, puis résoudre des
problèmes en reliant plusieurs outils. Il est conçu pour être utilisé en
complément du travail de classe, dans l’ordre adapté aux besoins.\par\medskip
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
\begin{attention}Lire tout l’énoncé, y compris les unités, les mots « exactement », « au moins », « sans remise » et la précision demandée. En géométrie, un angle droit dessiné sans hypothèse n’est pas une preuve.\end{attention}
Les liens du sommaire et les numéros de page conduisent aux chapitres et
aux corrigés. Le tableau de bord permet de noter ce qui est réussi seul,
réussi avec aide ou à reprendre. Pour les scripts, les blocs indentés
appartiennent au bloc qui les contient ; les lignes « fin » en indiquent la fermeture.
''','mode-emploi')
    docs['parcours']=front('Construire son parcours','Avancer avec des retours réguliers',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Étape & Travail conseillé\\\midrule
Consolider & Chapitres 1 à 7 : nombres, calculs, équations, proportionnalité et unités.\\[3mm]
Modéliser & Chapitres 8 à 11 : fonctions, statistiques, expériences aléatoires.\\[3mm]
Démontrer & Chapitres 12 à 16 : théorèmes, transformations, mesures et espace.\\[3mm]
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
    docs['sommaire']=r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Troisième · France · Brevet 2027}
\vspace{-4mm}\sommaire\clearpage
\thispagestyle{otFront}\otPageTitre{Parcours et ressources}{Cours, défis, sujets et corrections}
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
\ligneSommaire{Repérage des attendus dans le livre}{couverture-programme}
\ligneSommaire{Sources officielles et périmètre de l’édition}{references}
\clearpage
'''
    body=''
    for i,(titre,desc,url) in enumerate(SOURCES,1):
        body+=r'\par\medskip\textbf{'+str(i)+'. '+titre+r'}\par '+desc+r'\par\href{'+url+r'}{\textcolor{otGreenDark}{Consulter la source officielle}}\par'+'\n'
    body+=r'''\par\bigskip Sources consultées le 21 octobre 2026. Les attendus annuels et les
repères du cycle 4 ont guidé la correspondance finale. Les exercices sont
originaux, non reproduits des documents officiels. Les défis et les sujets
du livre ne sont pas des sujets officiels.\par\medskip
Le calendrier publié en 2026 est essentiel : programme nouveau en 5e dès
2026, en 4e dès 2027, en 3e dès 2028. Cette édition prépare la Troisième
2026-2027 et la session 2027 du DNB, série générale.
'''
    docs['references']=front('Sources et édition','Références officielles · France',body,'references')
    return docs

# Quatre points de repère par chapitre, associés à des exercices identifiables.
EXEMPLES=[
[[1,2],[3,4,5,7,8],[6,10,15],[9,11,12,13,14]],
[[1,2,3,11],[4,6,7,12,13],[5,8,9,10,14],[11,12,13,14,15]],
[[1,2,5,6,7],[3,4,8,9],[10,11,13],[12,14,15]],
[[1,2,3],[4,7],[5,6,8,9],[10,11,12,13,14,15]],
[[1,2,3,4,5,6],[8,9,10,15],[7,10],[11,12,13,14,15]],
[[1,2,10],[5,8,9],[3,4,6,7,14,15],[11,12,13]],
[[1,2,3],[4,6,7,11],[5,8,10,12],[9,13,14,15]],
[[1,3,4,6],[2,5,7,8,10,15],[9],[11,12,13,14]],
[[1,2,4,6],[3,5,7,8],[3,7,8,9],[10,11,12,13,14,15]],
[[1,2],[3,6,10,11,12],[4,5,7,13,14],[8,9,15]],
[[1,2,3,5,10],[6,7,14],[8,9,11,13],[4,15]],
[[1,2,3,4],[5,6,10],[9],[7,8,11,12,13,14,15]],
[[1,2,3,4,5,8,9],[6,7,14],[10,12],[11,13,15]],
[[1,2,3,4],[5,6,7,13,15],[8,9,10,12],[11,12,13,14,15]],
[[1,2,3,4,5],[6,7,8,13],[9,10,14,15],[11,12]],
[[6,7,8,13],[1,2,3,4,5,11,12,14,15],[9],[10]],
[[1,2,4,5,6,9,10],[3,7,11],[8,12,13,14],[15]],
[[1,2,6,8,10],[3,4,5,7,9],[11,12,13,14],[15]]
]
def couverture_programme():
    text=r'\clearpage\phantomsection\label{couverture-programme}\pdfbookmark[0]{Repérage des attendus}{bm-couverture-programme}'+'\n'
    text+=r'''\gdef\otChapNum{0}\pagestyle{otFront}\otPageTitre{Repérage des attendus}{Troisième 2026-2027 · Lecture par notions}
Cette matrice rassemble les attendus annuels, avec les acquis du cycle 4
réactivés pour les utiliser. Les quatre repères de chaque chapitre renvoient
à des exercices précis ; les séries citées ne sont pas exhaustives.
Les dix-huit défis prolongent ces notions sans ajouter d’exigence à l’examen.\par\bigskip
Points à retrouver : puissances négatives (2), différence de carrés et
produits nuls (4-5), histogrammes de même amplitude (10), arbres à deux
étapes (11), Thalès en papillon (13), homothéties négatives (15), sections,
assemblages et repérage sur la sphère (16), scripts parallèles (17).\par\bigskip
\begin{attention}La précision perdue par un regroupement statistique en classes est signalée :
les valeurs extrêmes exactes et la médiane exacte ne se déduisent pas toujours
d’un histogramme. La programmation est abordée par blocs, comme au collège.\end{attention}
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
