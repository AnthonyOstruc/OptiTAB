"""Pages de navigation et références de l'édition enrichie."""
TEXTES={
'parcours':r'''
\thispagestyle{otFront}
\phantomsection\pdfbookmark[0]{Parcours de travail}{bm-parcours}
\otPageTitre{Parcours de travail}{Des bases aux problèmes de recherche}
\fontsize{11}{15}\selectfont
\otIntertitre{Un livre de Première générale, spécialité mathématiques}
Les chapitres 1 à 11 développent l'algèbre, l'analyse, la géométrie, les probabilités
et les statistiques. Les chapitres 12 à 14 donnent les outils transversaux : Python,
raisonnement et automatismes. Ces derniers sont à reprendre au fil de l'année.
L'ordre des thèmes peut être adapté à la progression du professeur.\par\vspace{5mm}
\otIntertitre{Choisir le bon point de départ}
\begin{tabularx}{\linewidth}{@{}p{38mm}Y@{}}\toprule
\textbf{Parcours} & \textbf{Objectif}\\\midrule
Découverte, 1 à 5 & Vérifier les bases avec des applications directes.\\[2mm]
Entraînement, 6 à 11 & Installer les méthodes, puis choisir une démarche.\\[2mm]
Problèmes, 12 à 15 & Relier les notions, modéliser et rédiger.\\[2mm]
Défis D01 à D14 & Prendre des initiatives et traiter des discussions exigeantes.\\[2mm]
Sujets blancs A et B & Travailler en temps limité, sans calculatrice.\\\bottomrule
\end{tabularx}
\vspace{6mm}
\otIntertitre{Une méthode de travail en quatre temps}
\begin{questions}
\item Lire les objectifs et le cours. Reformuler une propriété avec ses hypothèses.
\item Chercher sans corrigé. Écrire les données, un schéma utile et les premières relations.
\item Comparer la démarche à la correction. Repérer précisément l'étape qui manquait.
\item Refaire quelques jours plus tard, puis expliquer la solution à voix haute.
\end{questions}
\vspace{4mm}
\otIntertitre{Se repérer et mesurer ses progrès}
Le tableau de bord suit les 210 exercices des chapitres. Pour les 14 défis,
noter dans son cahier : réussi seul, réussi avec un indice, ou à reprendre.
Les indications sont séparées des énoncés et des corrigés.
Les démonstrations de référence et les repères du programme servent de points d'appui.
\editionRetenir{La difficulté augmente par les choix de méthode et le raisonnement.
Un défi facultatif peut demander du temps, tout en restant fondé sur les outils de Première.}
\clearpage
''',
'sommaire':r'''
\thispagestyle{otFront}
\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Première générale · Spécialité mathématiques}
\vspace{-4mm}\sommaire\clearpage
\thispagestyle{otFront}
\otPageTitre{Parcours et ressources}{Compléments, entraînements et outils de révision}
\fontsize{11}{16}\selectfont
\newcommand{\editionSomLigne}[2]{\hyperref[#1]{\textcolor{otNavy}{#2}}\hfill p.~\pageref*{#1}\par\vspace{4mm}}
\otIntertitre{Approfondir}
\editionSomLigne{defis-debut}{14 défis d'approfondissement}
\editionSomLigne{indices-defis}{Indications progressives pour les défis}
\otIntertitre{Préparer l'épreuve anticipée}
\editionSomLigne{epreuve-guide}{Format, conseils et barème d'entraînement}
\editionSomLigne{sujet-A}{Sujet blanc A : automatismes, analyse, probabilités}
\editionSomLigne{sujet-B}{Sujet blanc B : automatismes, suites, géométrie}
\otIntertitre{Comprendre et corriger}
\editionSomLigne{demonstrations-debut}{Démonstrations de référence}
\editionSomLigne{corriges-debut}{Corrigés des 210 exercices de chapitre}
\editionSomLigne{defi-cor-1-1}{Corrigés détaillés des 14 défis}
\editionSomLigne{sujet-A-cor-auto}{Corrigés des deux sujets blancs}
\otIntertitre{Vérifier sa couverture du programme}
\editionSomLigne{couverture-programme}{Repères du programme : contenus, méthodes, preuves}
\clearpage
''',
'references':r'''
\thispagestyle{otFront}
\phantomsection\pdfbookmark[0]{Références et repères éditoriaux}{bm-references}
\otPageTitre{Références}{France · Première générale · Spécialité mathématiques}
\fontsize{10.5}{14.5}\selectfont
\otIntertitre{Le programme de référence}
Le livre s'appuie sur le programme publié au \textbf{BO n° 14 du 2 avril 2026}
(arrêté du 26 février 2026, NOR MENE2602917A), applicable à la rentrée 2026-2027.
Les repères de l'annexe relient ses contenus aux cours et exercices du livre.
Les approfondissements facultatifs sont sélectionnés, sans prétendre les reproduire tous.\par\vspace{3mm}
\href{https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A}{\textcolor{otNavy}{Programme officiel et annexe sur education.gouv.fr}}\par\vspace{5mm}
\otIntertitre{L'épreuve anticipée}
La préparation suit la \textbf{note de service du 11 septembre 2026}, NOR MENE2622640N,
publiée au BO spécial n° 4 du 17 septembre 2026. Elle s'applique en 2026-2027 aux
épreuves présentées au titre du baccalauréat session 2028 et remplace la note de service
du 10 juin 2025 (NOR MENE2515469N). Les automatismes y prennent la forme de réponses
courtes. Le programme de Première précise que sa liste d'automatismes s'ajoute à celle
de Seconde, à entretenir en Première. Le guide du livre distingue ce cadre officiel du barème
choisi pour ses sujets d'entraînement.\par\vspace{3mm}
\href{https://www.education.gouv.fr/bo/2026/Special4/MENE2622640N}{\textcolor{otNavy}{Définition officielle de l'épreuve anticipée}}\par\vspace{2mm}
\href{https://eduscol.education.gouv.fr/5688/epreuve-anticipee-de-mathematiques-aux-baccalaureats-general-et-technologique}{\textcolor{otNavy}{Présentation et ressources de préparation sur Éduscol}}\par\vspace{5mm}
\otIntertitre{Les choix pédagogiques}
Les 210 exercices de chapitre, 14 défis et deux sujets blancs sont des créations pour ce livre.
Les sujets blancs ne reproduisent pas un sujet officiel. Les défis très exigeants sont
facultatifs et explicitent leurs prérequis ; ils ne nécessitent pas de cours de Terminale.
L'ordre du livre peut être adapté par le professeur.\par\vspace{3mm}
Les figures, courbes, arbres et tableaux sont vectoriels. Les schémas sans échelle
imposée sont signalés. Les programmes Python peuvent être exécutés séparément.
Les résultats numériques illustrent les calculs théoriques ; les arrondis et les
hypothèses d'indépendance sont précisés lorsqu'ils interviennent.\par\vspace{5mm}
{\fontsize{9}{12}\selectfont\color{otMuted}Sources officielles consultées le 23 octobre 2026.
La charte reprend le modèle OptiTAB de Terminale : couleurs, typographie et repères de difficulté.}
\clearpage
'''}

def ecrire_liminaires(root):
    for name,text in TEXTES.items():
        (root/'liminaires'/f'{name}.tex').write_text(text.strip()+'\n',encoding='utf-8')
