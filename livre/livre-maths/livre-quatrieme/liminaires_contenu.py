from modele import CHAPITRES
SOURCES=[
('Programme applicable','Bulletin officiel du 30 juillet 2020 : programme du cycle 4, encore applicable en Quatrième en 2026-2027.','https://www.education.gouv.fr/bo/20/Hebdo31/MENE2018714A.htm'),
('Attendus de fin de Quatrième','Éduscol : document complet de 12 pages, connaissances et exemples de réussite, y compris programmation de niveaux 1 et 2.','https://eduscol.education.gouv.fr/sites/default/files/document/16-maths-4e-attendus-eduscol1114746pdf-74682.pdf'),
('Repères annuels du cycle 4','Éduscol : progression par niveau, limites du formalisme, géométrie et programmation.','https://eduscol.education.gouv.fr/sites/default/files/document/26-maths-c4-reperes-eduscol1114756pdf-74694.pdf'),
('Calendrier du nouveau programme','BO du 5 mars 2026, article 3 : nouveau programme applicable en Quatrième à la rentrée 2027-2028.','https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A'),
('Validité des attendus en 2026-2027','Éduscol, repères et attendus annuels : calendrier de leur remplacement progressif.','https://eduscol.education.gouv.fr/6910/reperes-annuels-de-progression-et-attendus-de-fin-d-annee-du-cp-la-troisieme'),
]
def front(titre,sous,body,label):
    return r'\clearpage\thispagestyle{otFront}\phantomsection\label{'+label+r'}\pdfbookmark[0]{'+titre+'}{bm-'+label+r'}\otPageTitre{'+titre+'}{'+sous+r'}\fontsize{11}{15}\selectfont'+'\n'+body+'\n'+r'\clearpage'+'\n'

def documents():
    docs={}
    docs['copyright']=r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{128mm}\fontsize{9}{13}\selectfont\color{otMuted}
{\otSemi\color{otInk}Mathématiques · Quatrième · France}\par\medskip
Conception et mise en page : collection OptiTAB.\par
270 exercices de chapitre, 18 défis et deux bilans annuels originaux, corrigés.\par
Charte graphique de la collection OptiTAB, du collège au lycée.\par\bigskip
Édition du 22 octobre 2026 · Année scolaire 2026-2027.\par\bigskip
Cette édition suit les attendus de Quatrième applicables en 2026-2027.
Le nouveau programme publié en mars 2026 ne s’appliquera en Quatrième
qu’à la rentrée 2027-2028. Les repères de Cinquième nécessaires sont réactivés
au fil des chapitres.\par\bigskip
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
    docs['avant-propos']=front('Apprendre et comprendre','Un livre pour toute la Quatrième',r'''
Ce livre accompagne une année de mathématiques en Quatrième : consolider
les calculs, découvrir les outils géométriques et résoudre des problèmes
qui demandent de relier plusieurs idées. Il peut être suivi dans l’ordre
ou utilisé pour reprendre une difficulté précise.\par\medskip
\begin{savoirfaire}[Une progression régulière]Chaque chapitre contient des objectifs, des prérequis, deux pages de cours et quinze exercices : cinq pour découvrir, cinq pour s’entraîner et cinq problèmes. Les corrections expliquent le choix de méthode, les étapes et l’interprétation du résultat.\end{savoirfaire}
\begin{savoirfaire}[Des représentations pour penser]Les figures de géométrie, tableaux, graphiques, patrons et blocs de programmation accompagnent les questions qui en ont besoin. Les constructions cherchées et les réponses graphiques sont ajoutées au corrigé. Le dessin sert à comprendre et à chercher ; les données restent la base des preuves.\end{savoirfaire}
\begin{savoirfaire}[Chercher davantage]Dix-huit défis facultatifs proposent une recherche plus longue, avec deux indications séparées et une solution. Deux bilans annuels permettent de mélanger les notions. Les fiches outils et le repérage final orientent les révisions.\end{savoirfaire}
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
Calculer & Chapitres 1 à 4 : relatifs, fractions, puissances et racines.\\[3mm]
Modéliser & Chapitres 5 à 9 : algèbre, équations, proportionnalité, unités et graphiques.\\[3mm]
Interpréter & Chapitres 10 et 11 : données, médiane et probabilités.\\[3mm]
Démontrer & Chapitres 12 à 17 : triangles, Pythagore, Thalès, cosinus, translations et espace.\\[3mm]
Programmer & Chapitre 18, à reprendre pendant l’année avec les autres thèmes.\\\bottomrule
\end{tabularx}
\begin{savoirfaire}[Une séance de 35 à 50 minutes]Relire une propriété et son exemple. Chercher deux exercices sans correction. Comparer les démarches et refaire une question ratée. Terminer par une phrase : « La prochaine fois, je dois penser à… ».\end{savoirfaire}
\begin{savoirfaire}[Revenir et mélanger]Reprendre une notion quelques jours plus tard, puis quelques semaines après. Mélanger un calcul, une lecture graphique et une preuve évite de dépendre seulement du titre d’un chapitre.\end{savoirfaire}
Pour un défi, prévoir 30 à 60 minutes, éventuellement en plusieurs séances.
Pour un bilan, respecter le temps choisi puis classer les erreurs par notion.
Le tableau de bord aide à décider ce qui doit être refait seul ou avec aide.
''','parcours')
    docs['sommaire']=r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Quatrième · France · Année 2026-2027}
\vspace{-4mm}\sommaire\clearpage
\thispagestyle{otFront}\otPageTitre{Parcours et ressources}{Cours, défis, bilans et corrections}
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
\ligneSommaire{Repérage des attendus dans le livre}{couverture-programme}
\ligneSommaire{Sources officielles et périmètre de l’édition}{references}
\clearpage
'''
    body=''
    for i,(title,desc,url) in enumerate(SOURCES,1):
        body+=r'\par\medskip\textbf{'+str(i)+'. '+title+r'}\par '+desc+r'\par\href{'+url+r'}{\textcolor{otGreenDark}{Consulter la source officielle}}\par'+'\n'
    body+=r'''\par\bigskip Sources consultées le 22 octobre 2026. Les exercices et bilans
sont originaux, sans reproduction des exemples officiels.\par\medskip
Périmètre : Thalès dans les triangles emboîtés, cosinus seul en trigonométrie,
translations sans calcul vectoriel formel, dépendance de grandeurs sans
notations de fonctions, probabilités à une épreuve, programmation de niveaux
1 et 2. Les défis approfondissent ces outils sans ajouter d’exigence officielle.
Le programme nouveau de 2027-2028 en Quatrième demandera une édition adaptée.
'''
    docs['references']=front('Sources et édition','Références officielles · France',body,'references')
    return docs

EXEMPLES=[
[[1,2,3,5],[4,6,14],[7,8,9,10,15],[11,12,13]],
[[1,2,10],[3,4,5,8,9],[6,7,12],[11,13,14,15]],
[[1,2,14],[3,7,9,10],[4,6,8,13,15],[5,11,12]],
[[1,2,3],[4,5,8],[6,10,14],[7,9,11,12,13,15]],
[[1,2,3,10],[4,6,7],[5,8,13],[9,11,12,14,15]],
[[1,5],[2,3,4,6,7,8],[11,12,13,14,15],[9,10]],
[[1,2,6],[3,4,7,11,13,15],[5,10,12,14],[8,9]],
[[1,2,3,6,11,14],[4,5,7,8,13,15],[9,12],[10]],
[[1,2,9],[3,4,7],[5,6,8],[10,11,12,13,14,15]],
[[1,2,6,11],[3,4,7,12,15],[5,8,9],[10,13,14]],
[[1,2,3],[4,6,7],[5,8,11,13],[9,10,12,14,15]],
[[1,2,3,4,14],[5,6,7,8],[9,10,11,13],[12,15]],
[[1,3,7,9],[2,4,8,12],[5,6,10],[11,13,14,15]],
[[1,2,3,7,8,10,12],[4,5,6,13],[9,14],[11,15]],
[[1,2,3,10],[4,5,6,9],[7,8],[11,12,13,14,15]],
[[1,2,3,13],[4,6],[5,15],[7,8,9,10,11,12,14]],
[[1,2,3,4],[5,6],[9,10],[7,8,11,12,13,14,15]],
[[1,2,3,5,6],[4,9,15],[7,8,11,13],[10,12,14]]
]
def couverture_programme():
    text=r'\clearpage\phantomsection\label{couverture-programme}\pdfbookmark[0]{Repérage des attendus}{bm-couverture-programme}'
    text+=r'''\gdef\otChapNum{0}\pagestyle{otFront}\otPageTitre{Repérage des attendus}{Quatrième 2026-2027 · Lecture par notions}
Cette matrice relie les connaissances des attendus annuels et les acquis
réactivés à des exercices précis. Les quatre repères de chaque chapitre
permettent de retrouver un travail ciblé. Les séries indiquées ne sont pas
exhaustives ; les cours et les défis complètent ce parcours.\par\bigskip
Points à retrouver : préfixes de nano à giga (3), carrés jusqu’à 144 et
racines en contexte (4), équations du premier degré (6), grandeurs composées
(8), graphiques sans formalisme de fonctions (9), médiane sur de petits
effectifs et diagrammes circulaires (10), événement contraire (11),
cas d’égalité des triangles (12), Pythagore et réciproque (13),
Thalès emboîté et réciproque (14), cosinus (15), translations et effets
sur les grandeurs (16), patrons et repérage dans le pavé (17),
programmation de niveaux 1 et 2 (18).\par\bigskip
\begin{attention}Les difficultés signalées par trois pastilles et les défis sont des choix d’entraînement. Ils ne changent pas le programme officiel et ne constituent pas une liste d’exigences supplémentaires pour un examen.\end{attention}
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
