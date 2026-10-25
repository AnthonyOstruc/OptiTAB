from modele import CHAPITRES

PROGRAMME='https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602914A'
EDUSCOL='https://eduscol.education.gouv.fr/6858/accompagner-les-eleves-en-mathematiques-4e-3e-et-2de'

EXEMPLES_PAR_REPERE={
    1:[1,4,6,8], 2:[1,4,6,10], 3:[2,5,7,9], 4:[6,3,8,14],
    5:[4,6,9,12], 6:[1,8,7,9], 7:[6,7,11,10], 8:[5,14,7,13],
    9:[2,5,8,9], 10:[7,6,13,9], 11:[6,4,7,14], 12:[2,7,10,14],
    13:[5,1,2,10], 14:[1,11,7,14], 15:[2,3,12,15], 16:[2,4,8,11],
}

def documents():
    return {
'copyright':r'''\thispagestyle{empty}\vspace*{\fill}
{\otSemi\fontsize{10}{13}\selectfont Mathématiques · Seconde · Livre complet}\par\medskip
{\fontsize{9}{12}\selectfont\color{otMuted}
Collection OptiTAB. Conception, exercices et corrigés originaux.\par
256 exercices : 240 exercices de chapitre et 16 défis facultatifs. Quarante questions flash d’automatismes et deux bilans corrigés complètent l’entraînement.\par\medskip
Édition du 23 octobre 2026, après audit de conformité au programme de Seconde générale et technologique applicable à la rentrée 2026-2027, publié au BO du 2 avril 2026 (NOR MENE2602914A).\par\medskip
La charte reprend le livre OptiTAB de Première : typographie, couleurs, repères de difficulté et liens entre énoncés et corrigés. Les données sont construites pour l’apprentissage, sauf source explicitement indiquée.\par\medskip
Les figures sont vectorielles. Les repères orthonormés et les schémas sans échelle sont identifiés. Une lecture graphique est approchée, sauf indication de points ou d’une construction exacte.\par\medskip
Les programmes utilisent Python 3 et les modules standards. Les scripts de vérification et les sources modifiables sont fournis séparément.\par\medskip
© OptiTAB, 2026\par optitab.net}
\clearpage''',
'avant-propos':r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Avant-propos}{bm-avant-propos}
\otPageTitre{Avant-propos}{Comprendre, chercher et progresser pendant toute la Seconde}
{\large\itshape\color{otNavy}Ce livre accompagne ton année de Seconde générale et technologique, depuis les applications directes jusqu’aux problèmes qui demandent de prendre des initiatives.}\par\bigskip
Les 16 chapitres couvrent les nombres et le calcul, les fonctions, la géométrie, les statistiques et les probabilités. Python, la logique et les automatismes se travaillent tout au long de l’année : les chapitres 15 et 16 et quatre séries de questions flash corrigées servent de ressources à reprendre au moment utile.\par\medskip
Chaque chapitre propose un cours de référence, des méthodes et 15 exercices en trois étapes : \textbf{Découverte}, \textbf{Entraînement}, \textbf{Problèmes}. Les corrigés expliquent pourquoi la méthode convient, déroulent les calculs et interprètent les résultats. Les figures utiles restent avec le texte correspondant.\par\medskip
Un parcours de \textbf{16 défis facultatifs}, avec deux indications progressives pour chacun, permet d’approfondir. Il traite toutes les pistes d’approfondissement citées dans le programme, dont les barycentres, les concours de droites, les identités et les lieux géométriques. Les notions supplémentaires sont définies sur place.\par\medskip
Les démonstrations de référence, deux bilans de fin d’année, un atelier numérique et une matrice de couverture du programme complètent le livre. Les bilans sont des entraînements éditoriaux : ils ne représentent pas une épreuve nationale de Seconde.\par\medskip
Prends le temps de chercher avant de consulter une solution. Après lecture, ferme le corrigé et refais l’exercice : expliquer la démarche avec tes propres mots permet de mesurer ce qui est acquis.\par\bigskip
{\otMedium Bon travail et bonne année de Seconde !}\par\medskip
\includegraphics[width=10mm]{icone-couleur}\clearpage''',
'parcours':r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Parcours de travail}{bm-parcours}
\otPageTitre{Parcours de travail}{Des bases à la recherche, à ton rythme}
\otIntertitre{Choisir le bon niveau}
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
Exercices 1 à 5 & Appliquer une notion et vérifier les bases.\\[2mm]
Exercices 6 à 10 & Installer les méthodes, changer de représentation.\\[2mm]
Exercices 11 à 15 & Relier les notions et rédiger une démarche.\\[2mm]
Questions flash & Entretenir les automatismes, quelques minutes à chaque séance.\\[2mm]
Défis D01 à D16 & Chercher plus longtemps, avec des indications séparées.\\[2mm]
Bilans A et B & Mobiliser plusieurs chapitres en temps limité.\\\bottomrule
\end{tabularx}\par\bigskip
\otIntertitre{Une méthode en quatre temps}
\otConseil{1}{Lire les objectifs et le cours ; reformuler la propriété à utiliser.}
\otConseil{2}{Chercher sans corrigé, en dessinant et en nommant les inconnues.}
\otConseil{3}{Comparer les démarches ; repérer précisément la première difficulté.}
\otConseil{4}{Refaire l’exercice quelques jours plus tard, puis expliquer la solution à voix haute.}
\par\medskip\otIntertitre{Un travail réparti sur l’année}
L’ordre des chapitres est un choix éditorial, adaptable par le professeur. Les automatismes, le raisonnement et Python doivent être réinvestis dès les premiers thèmes, même si leurs pages de ressources sont regroupées à la fin.\par\medskip
Une séance courte peut réunir un calcul mental, un exercice direct et une question d’explication. Une séance longue peut être réservée à un problème ou à un défi ; note alors ce que tu as essayé, même si la recherche n’aboutit pas.\par\medskip
\begin{savoirfaire}[Suivre ses progrès]Le tableau de bord suit les 240 exercices de chapitre. Pour les défis et les bilans, noter séparément : réussi seul, avec une indication, ou à reprendre. Une correction comprise devient un objectif de révision, pas une simple page à cocher.\end{savoirfaire}
\clearpage''',
'sommaire':r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Seconde générale et technologique · Programme 2026-2027}
\sommaire\clearpage
\thispagestyle{otFront}\otPageTitre{Parcours et ressources}{Approfondir, s’entraîner et vérifier ses acquis}
\otIntertitre{Entretenir les automatismes}
\ligneSommaire{Quatre séries de questions flash}{automatismes-1}
\par\vspace{6mm}\otIntertitre{Chercher plus loin}
\ligneSommaire{16 défis d’approfondissement}{defis-debut}
\ligneSommaire{Indications progressives pour les défis}{indices-debut}
\par\vspace{6mm}\otIntertitre{Faire le point}
\ligneSommaire{Comment travailler les deux bilans}{bilans-guide}
\ligneSommaire{Bilan A : fonctions, géométrie et conditionnement}{bilan-A-auto}
\ligneSommaire{Bilan B : statistiques, configurations et tirages}{bilan-B-auto}
\par\vspace{6mm}\otIntertitre{Comprendre les preuves et les corrigés}
\ligneSommaire{Démonstrations de référence}{preuves-debut}
\ligneSommaire{Corrigés des 240 exercices de chapitre}{corriges-debut}
\ligneSommaire{Corrigés des questions flash}{automatismes-cor-1}
\ligneSommaire{Corrigés des 16 défis}{defi-cor-1-1}
\ligneSommaire{Corrigés des deux bilans}{bilan-A-cor-auto}
\par\vspace{6mm}\otIntertitre{Utiliser et situer les outils}
\ligneSommaire{Atelier numérique : balayage, listes et filtres}{atelier-debut}
\ligneSommaire{Lecture graphique : nuage de points}{atelier-nuage}
\ligneSommaire{Repères de culture mathématique}{culture-debut}
\ligneSommaire{Couverture du programme et approfondissements}{couverture-programme}
\ligneSommaire{Références et choix de l’édition}{references}
\clearpage''',
'references':r'''\thispagestyle{otFront}\gdef\otChapNum{0}\phantomsection\label{references}\pdfbookmark[0]{Références}{bm-references}
\otPageTitre{Références}{France · Seconde générale et technologique}
\otIntertitre{Le programme de référence}
Le livre s’appuie sur l’arrêté du 26 février 2026, publié au BO n° 14 du 2 avril 2026 (NOR MENE2602914A), applicable à la rentrée 2026-2027. Son annexe (pages 333 à 345 du BO) a été relue intégralement lors de l’audit du 23 octobre 2026. La matrice précédente repère les contenus, les capacités, les démonstrations, les exemples algorithmiques, les automatismes et les approfondissements dans le livre.\par\smallskip
\href{https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602914A}{Programme et annexe sur education.gouv.fr}\par\bigskip
\otIntertitre{Ressources pédagogiques consultées}
Les ressources Éduscol « Accompagner les élèves en mathématiques - 4e, 3e et 2de » et « Raisonner et démontrer en Seconde » ont servi à vérifier la variété des tâches et l’importance de l’argumentation. Les exercices de ce livre sont originaux ; ils ne reproduisent pas ces fiches.\par\smallskip
\href{https://eduscol.education.gouv.fr/6858/accompagner-les-eleves-en-mathematiques-4e-3e-et-2de}{Ressources Éduscol et fiches par domaines}\par\bigskip
\otIntertitre{Données réelles}
Deux exercices utilisent des données identifiées : Insee Focus n° 374, décembre 2025, pour les populations de Nantes et Bordeaux en 2023 ; dossier complet France, POP T4, édition du 27 août 2026, pour des croisements âge et sexe au RP2023. Le champ France hors Mayotte est précisé dans l’exercice concerné. Les autres enquêtes et modèles numériques sont construits à des fins pédagogiques.\par\smallskip
\href{https://www.insee.fr/fr/statistiques/8682718}{Insee Focus 374}\quad
\href{https://www.insee.fr/fr/statistiques/2011101?geo=FRANCE-1}{Dossier France, données 2023}\par\bigskip
\otIntertitre{Choix et vérifications}
Les calculs exacts, cas limites, énumérations et programmes ont été contrôlés avec les scripts fournis. Les preuves ont été relues ; les contrôles numériques finis ne remplacent pas une démonstration générale. Toutes les pages sont rendues et contrôlées avant livraison.\par\medskip
{\small\color{otMuted}Sources consultées le 21 octobre 2026 ; programme relu le 23 octobre 2026. Charte de la collection OptiTAB. Les deux bilans, leur barème et les séries de questions flash sont des choix pédagogiques.}\clearpage'''
}

def couverture_programme():
    rows=[]
    for c in CHAPITRES:
        rows.append(r'\multicolumn{2}{@{}l}{\otSemi\color{otNavy}'+str(c.numero)+'. '+c.titre+r'}\\[2mm]')
        for i,topic in enumerate(c.reperes):
            ex=EXEMPLES_PAR_REPERE[c.numero][i]
            rows.append(topic+r' & \hyperref[ess-'+str(c.numero)+r']{Cours p.\,\pageref*{ess-'+str(c.numero)+r'}} ; \hyperref[exo-'+str(c.numero)+'-'+str(ex)+r']{ex. '+str(ex)+r'}\\[2mm]')
    return r'''\clearpage\gdef\otChapNum{0}\pagestyle{otFront}\phantomsection\label{couverture-programme}\pdfbookmark[0]{Couverture du programme}{bm-programme}
\otPageTitre{Repères du programme}{Contenus, méthodes et exercices correspondants}
Le découpage ci-dessous est celui du livre. Les trois ressources transversales se réinvestissent dans tous les thèmes ; leur regroupement n’impose pas d’attendre la fin de l’année. Les références renvoient à un cours et à un exemple d’exercice, sans limiter les notions à ces seules pages.\par\medskip
\begingroup\fontsize{9.5}{12}\selectfont\renewcommand{\arraystretch}{1.2}
\begin{longtable}{@{}p{106mm}p{53mm}@{}}\toprule
Contenu ou capacité travaillé & Où le retrouver\\\midrule\endhead
'''+ '\n'.join(rows)+r'''\bottomrule\end{longtable}\endgroup
\par\medskip\otIntertitre{Les trois parties transversales}
{\fontsize{9.5}{12}\selectfont\renewcommand{\arraystretch}{1.2}\begin{tabularx}{\linewidth}{@{}Yl@{}}\toprule
Vocabulaire ensembliste et logique : opérations sur les ensembles, cardinal, propositions et raisonnements & \hyperref[ess-16]{Cours p.\,\pageref*{ess-16}} ; \hyperref[exo-16-1]{ex. 1}\\[1mm]
Algorithmique : affectation notée $\leftarrow$, langage naturel et Python, fonctions, hasard & \hyperref[ess-15]{Cours p.\,\pageref*{ess-15}} ; \hyperref[exo-15-1]{ex. 1}\\[1mm]
Automatismes : 30 capacités du programme, 40 questions flash corrigées & \hyperref[automatismes-1]{Séries p.\,\pageref*{automatismes-1}}\\\bottomrule
\end{tabularx}}\par\smallskip
{\fontsize{9.5}{12}\selectfont Nuage de points : atelier de lecture graphique, p.\,\pageref{atelier-nuage}. Signe d’une fonction affine et taux d’accroissement : cours du chapitre~6.}
\clearpage\otPageTitre{Preuves et prolongements}{Un périmètre explicite}
\otIntertitre{Les démonstrations identifiées dans le programme}
Somme de multiples et carré impair ; non-décimalité de $1/3$ et irrationalité de $\sqrt2$ ; racine d’un produit ; critère de colinéarité ; équation cartésienne de droite ; variations des affines ; position de $x$ et $x^2$ ; variations du carré et de l’inverse. Elles sont rassemblées dans les 13 démonstrations de référence, avec deux compléments.\par\medskip
\otIntertitre{Toutes les pistes d’approfondissement proposées}
\begin{tabularx}{\linewidth}{@{}Yl@{}}\toprule
Écritures décimales illimitées ; périodicité rationnelle & D01\\[1.5mm]
Carré de trois termes ; cube d’une somme & D02\\[1.5mm]
Moyennes arithmétique et géométrique & D03\\[1.5mm]
Barycentres de deux et trois points & D04\\[1.5mm]
Formule des coordonnées du milieu, démontrée & Preuve 12\\[1.5mm]
Concours des hauteurs & D06\\[1.5mm]
Aire $ab\sin C/2$ & D07\\[1.5mm]
Isobarycentre et concours des médianes & D05\\[1.5mm]
Médiatrices et cercle circonscrit & D08\\[1.5mm]
Équidistance d’un point et de l’axe horizontal & D09\\[1.5mm]
Régions décrites par des inégalités & D10\\[1.5mm]
Lien entre courbes carré et racine sur les positifs & D11\\\bottomrule
\end{tabularx}\par\medskip
Les défis D12 à D16 ajoutent d’autres recherches : paramètre, dispersion, marges d’un tableau, contrôle et dénombrement. Le caractère facultatif est indiqué dans le parcours.\par\medskip
\otIntertitre{Les exemples d’algorithmes}
Divisibilité et dernier multiple : 1.8 et 1.9. Encadrement de racine : 2.15 et 15.7. Première puissance au-delà ou en deçà d’un seuil : 11.13 et 15.6. Alignement et équation de droite : 15.8 et 15.9. Balayage et dichotomie d’un extrémum : 7.10, 15.15 et atelier. Longueur approchée de courbe : 15.14. Filtres ET, OU, NON sur deux listes, tableau croisé et fréquences conditionnelles : 13.7, 13.8 et atelier. Simulation et loi des grands nombres : 15.10 à 15.12.
\clearpage'''
