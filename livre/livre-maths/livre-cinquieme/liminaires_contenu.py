from modele import CHAPITRES
SOURCES=[
('Arrêté et calendrier','BO n° 10 du 5 mars 2026, arrêté du 18 février 2026 (NOR MENE2602912A), article 3 : application en Cinquième à la rentrée 2026-2027.','https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A'),
('Programme officiel de mathématiques','Annexe 2 du BO : rubriques de Cinquième, automatismes et objectifs en nombres, algèbre, géométrie, données, proportionnalité et pensée informatique.','https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf'),
('Exemples pour la mise en œuvre','Éduscol, mars 2026 : « Mathématiques. Exemples pour la mise en œuvre des programmes 2026. Cycle 4 », exemples de réussite et conseils pour chaque objectif de Cinquième.','https://eduscol.education.gouv.fr/sites/default/files/document/exemple-mise-en-oeuvre-c4-mathematiques0pdf-126080.pdf'),
('Ressources d’accompagnement','Éduscol : page des ressources d’accompagnement du programme de mathématiques du cycle 4.','https://eduscol.education.gouv.fr/5736/ressources-d-accompagnement-du-programme-de-mathematiques-au-cycle-4'),
]
def front(titre,sous,body,label):
    return r'\clearpage\thispagestyle{otFront}\phantomsection\label{'+label+r'}\pdfbookmark[0]{'+titre+'}{bm-'+label+r'}\otPageTitre{'+titre+'}{'+sous+r'}\fontsize{11}{15}\selectfont'+'\n'+body+'\n'+r'\clearpage'+'\n'
def documents():
    docs={}
    docs['copyright']=r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{128mm}\fontsize{9}{13}\selectfont\color{otMuted}
{\otSemi\color{otInk}Mathématiques · Cinquième · France}\par\medskip
Conception et mise en page : collection OptiTAB.\par
300 exercices de chapitre, 20 défis et deux bilans annuels originaux, corrigés.\par
Édition revue le 23 octobre 2026 · Année scolaire 2026-2027.\par\bigskip
Cette édition suit le nouveau programme de mathématiques publié au BO
du 5 mars 2026 et applicable en Cinquième depuis la rentrée 2026-2027.
Les rubriques de Cinquième du texte officiel ont guidé le périmètre.\par\bigskip
L’ordre des chapitres, les situations et les barèmes sont des choix éditoriaux.
Les défis sont facultatifs. Les bilans sont des entraînements originaux,
sans statut d’examen officiel.\par\bigskip
Les données numériques des problèmes sont construites pour apprendre.
Les dessins géométriques de principe ne sont pas à mesurer sauf consigne
explicite. Les graduations et coordonnées des graphiques font foi.\par\bigskip
Les réponses ajoutées en vert aux figures corrigées ne sont pas des données
de l’énoncé. Conserver les valeurs exactes jusqu’à l’arrondi demandé.\par\bigskip
© OptiTAB, 2026.\par\otSite
\end{minipage}\clearpage
'''
    docs['avant-propos']=front('Apprendre et comprendre','Un livre pour toute la Cinquième',r'''
Ce livre accompagne une année de mathématiques : calculer, représenter,
raisonner et expliquer. Il propose une progression complète tout en permettant
de revenir directement sur une difficulté grâce au sommaire et aux liens.\par\medskip
\begin{savoirfaire}[Du simple au problème]Chaque chapitre présente les objectifs,
les prérequis, le cours et quinze exercices : cinq de découverte, cinq
d’entraînement et cinq problèmes. Les corrections expliquent la méthode,
les étapes et le sens du résultat.\end{savoirfaire}
\begin{savoirfaire}[Des figures pour chercher]Quadrillages, constructions,
diagrammes, patrons et blocs accompagnent les tâches qui en ont besoin.
Les triangles et les solides disposent de plus d’espace de cours.
Les constructions cherchées apparaissent dans les corrigés.\end{savoirfaire}
\begin{savoirfaire}[Prendre de l’initiative]Vingt défis facultatifs proposent
deux indications séparées et une solution expliquée. Deux bilans mélangent
les chapitres. Les fiches outils et les repères de fin de livre guident les
révisions.\end{savoirfaire}
Les six compétences sont travaillées : chercher, modéliser, représenter,
raisonner, calculer et communiquer. Chercher sans réussir immédiatement
fait partie du travail : garder les essais utiles et expliquer ce qui bloque.
''','avant-propos')
    docs['mode-emploi']=front('Mode d’emploi','Des repères pour travailler seul',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Une pastille & Découverte : vocabulaire, lecture, calcul direct.\\[3mm]
Deux pastilles & Entraînement : choisir une méthode, organiser des étapes.\\[3mm]
Trois pastilles & Problèmes : relier les notions, justifier et interpréter.\\\bottomrule
\end{tabularx}\par\medskip
Ces indications décrivent les tâches ; elles ne classent pas les élèves.\par\medskip
\begin{exemple}[Lire une correction]Pour $5x=18$, on cherche le nombre
qui, multiplié par 5, donne 18. Donc $x=18:5=3{,}6$.
Le contrôle $5\times3{,}6=18$ confirme le résultat.
Refaire cette explication aide davantage que recopier seulement la réponse.\end{exemple}
\begin{attention}Lire les unités, les hypothèses et les mots « au moins »,
« strictement » ou « total ». Une figure ne donne pas à elle seule les
propriétés d’un objet. Une probabilité décrit un modèle de hasard,
pas une prédiction certaine du prochain résultat.\end{attention}
Chercher avant d’ouvrir le corrigé. Après lecture, fermer le livre et refaire
le passage décisif sur une feuille vierge. Les liens permettent de passer
de l’énoncé à sa correction puis de revenir.
''','mode-emploi')
    docs['parcours']=front('Construire son parcours','Une année avec des retours réguliers',r'''
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Calculer & 1 à 7 : opérations, divisibilité, relatifs, fractions, carrés et cubes.\\[3mm]
Modéliser & 8 à 12 : formules, distributivité, équations simples, proportionnalité, repérage et dépendance.\\[3mm]
Construire & 13 à 17 : angles, triangles, symétries, parallélogrammes, solides et volumes.\\[3mm]
Interpréter & 18 et 19 : données, moyenne simple et probabilités.\\[3mm]
Programmer & 20 : séquences, expressions et répétitions, à reprendre pendant l’année.\\\bottomrule
\end{tabularx}
\begin{savoirfaire}[Une séance régulière]Relire un exemple, chercher deux
exercices sans correction, puis comparer les démarches. Refaire une
question manquée et noter la notion à revoir.\end{savoirfaire}
\begin{savoirfaire}[Revenir et mélanger]Reprendre les notions quelques jours
puis quelques semaines après. Mélanger calcul, graphique et justification
pour apprendre à choisir un outil sans dépendre du titre du chapitre.\end{savoirfaire}
Les défis demandent environ 30 à 60 minutes, éventuellement en plusieurs
séances. Les bilans sont prévus pour deux heures. Adapter le temps à
l’objectif de travail ; le tableau de bord sert à suivre les reprises.
''','parcours')
    docs['sommaire']=r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Cinquième · France · Programme 2026}
\vspace{-4mm}\sommaire\clearpage
\thispagestyle{otFront}\otPageTitre{Parcours et ressources}{Cours, recherches et corrections}
\ligneSommaire{Vingt défis d’approfondissement}{defis-debut}
\ligneSommaire{Indications progressives}{indices-debut}
\ligneSommaire{Organisation des deux bilans}{bilans-guide}
\ligneSommaire{Bilan A}{bilan-A-auto}
\ligneSommaire{Bilan B}{bilan-B-auto}
\ligneSommaire{Comprendre les preuves}{preuves-debut}
\ligneSommaire{Corrigés des 300 exercices}{corriges-debut}
\ligneSommaire{Corrigés des 20 défis}{defi-cor-1}
\ligneSommaire{Corrigés des bilans}{bilan-A-cor-auto}
\ligneSommaire{Fiches outils}{outils-debut}
\ligneSommaire{Repérage du programme dans le livre}{couverture-programme}
\ligneSommaire{Sources officielles et périmètre}{references}\clearpage
'''
    body=''
    for i,(title,desc,url) in enumerate(SOURCES,1):
        body+=r'\par\medskip\textbf{'+str(i)+'. '+title+r'}\par '+desc+r'\par\href{'+url+r'}{\textcolor{otGreenDark}{Consulter la source officielle}}\par'+'\n'
    body+=r'''\par\bigskip Sources consultées le 22 octobre 2026 ; audit de conformité
au programme et aux exemples de mise en œuvre le 23 octobre 2026.
Les cours sont rédigés pour ce livre ; les exercices, défis et bilans
sont originaux.\par\medskip
Périmètre de Cinquième : sommes et différences de relatifs et de fractions ;
valeur absolue vue comme distance à zéro, sans notation exigible ;
carrés et cubes ; distributivité simple avec lettres ; équations $x+b=c$
et $ax=c$ par opérations inverses ; dépendance de grandeurs ; moyenne
simple ; probabilités en équiprobabilité ; données saisies lues et boucles
inconditionnelles simples. Les cours signalent les propriétés admises
en Cinquième : propriétés du demi-tour, réciproque des angles alternes
internes et correspondants, concours des hauteurs et des médianes, cercle
circonscrit du triangle rectangle.\par\medskip
Les nombres premiers sont présentés comme prolongement facultatif,
conformément à la rubrique « Prolongements possibles » du programme. Les défis
approfondissent les outils du cours et ne créent pas d’exigences d’examen.
L’ordre des chapitres est une proposition de progression.
'''
    docs['references']=front('Sources et édition','Références officielles · France',body,'references')
    return docs

# Chaque repère renvoie à un groupe précis d'exercices du chapitre.
EXEMPLES=[
[[1,2,3,11],[4,9,12],[5,6,7,10],[8,13,14,15]],
[[1,5,11],[2,3,4,6,7],[8,9,14],[10,12,13,15]],
[[1,2,8],[3,4,10],[5,6,7,12,13],[9,11,14,15]],
[[1,2,3,5,6],[4,10],[7,8,9],[11,12,13,14,15]],
[[1,3],[2,7,9,10],[4,5,6,8,11,12,14],[13,15]],
[[1,2,3,4],[6,7,8,9,10],[5,11,12],[13,14,15]],
[[1,2,5],[3,4],[6,7,8,9],[10,11,12,13,14,15]],
[[1,2,4,7,9],[3,6],[8,10,11,14],[5,12,13,15]],
[[1,2,6],[3,4,5,7,8],[9,11,12,13,14],[10,15]],
[[4,5],[1,6,8],[2,3,7,9,10],[11,12,13,14,15]],
[[1,2,5,6],[3,4,7,12,13],[8,9,14,15],[5,10,11]],
[[1,2,3,4,8,11],[6,7,12,13,15],[5,9,14],[10,13,15]],
[[1,2,3,4,5,6,12],[2,3,4,5,6,13],[7,8,11,15],[9,10,14]],
[[1,2,3,6,7,14],[9,12,13],[8,12,13],[4,5,10,11,15]],
[[1,2,6,11],[3,4,7,8],[5,9,10,12],[13,14,15]],
[[1,2,6,7],[8,9,14],[3,5,8,9,10],[4,11,12,13,15]],
[[1,11,14],[9,10,15],[2,3,5,6,12],[4,7,8,13]],
[[1,2,6,12,15],[4,5,7,8,15],[3,9,10,11,13],[10,12,13,14,15]],
[[1,6,9],[2,3,4,5],[6,7,8,9,12,13],[10,11,14,15]],
[[1,5,10],[2,3,4,14,15],[6,10,13],[7,8,9,11,12,13]]
]
def couverture_programme():
    text=r'\clearpage\phantomsection\label{couverture-programme}\pdfbookmark[0]{Repérage du programme}{bm-couverture-programme}'
    text+=r'''\gdef\otChapNum{0}\pagestyle{otFront}
\otPageTitre{Repérage du programme}{Cinquième · Nouveau programme 2026}
Cette matrice relie les notions et les automatismes du programme aux
exercices du livre. Les cours complètent ces repères, notamment pour les
définitions, démonstrations et constructions.\par\bigskip
Les objectifs nouveaux sont intégrés : fractions de dénominateurs
quelconques, carrés et cubes, distributivité littérale, équations simples,
parallélisme et angles, hauteurs et médianes, cercle circonscrit, y compris
celui du triangle rectangle, caractérisations des parallélogrammes,
perspectives et patrons de prismes et de cylindres, moyenne simple, échelle
de probabilité, lecture de dépendances et répétitions inconditionnelles.\par\bigskip
\begin{attention}Les niveaux de difficulté et les défis sont des choix
d’entraînement. Ils ne constituent pas une liste d’obligations
supplémentaires au programme officiel.\end{attention}\clearpage
'''
    for start in range(0,20,3):
        text+=r'\otPageTitre{Repères et exercices}{'+f'Chapitres {start+1} à {min(start+3,20)}'+r'}\fontsize{10}{13}\selectfont'+'\n'
        for c,rows in zip(CHAPITRES[start:start+3],EXEMPLES[start:start+3]):
            text+=r'\otIntertitre{'+str(c.numero)+'. '+c.titre+r'}\begin{tabularx}{\linewidth}{@{}Yl@{}}\toprule'+'\n'
            for rep,idxs in zip(c.reperes,rows):
                refs=', '.join(r'\hyperref[exo-'+f'{c.numero}-{j}'+']{'+f'{c.numero}.{j}'+'}' for j in idxs)
                text+=rep+' & '+refs+r'\\[2mm]'+'\n'
            text+=r'\bottomrule\end{tabularx}\par\vspace{4mm}'+'\n'
        text+=r'\clearpage'+'\n'
    return text
