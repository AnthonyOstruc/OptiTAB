from structure import write

def produire_liminaires(ch):
    write('adaptations.tex',r'''
% Bandeau des corrigés : trois zones distinctes, titre susceptible de revenir à la ligne.
\newcommand{\caseSuivi}{\tikz[baseline=-.2ex]\draw[otMuted,line width=.4pt](0,0)rectangle(2.4mm,2.4mm);}
\renewcommand{\corrigesChapitre}[2]{%
 \gdef\otChapNum{#1}\gdef\otChapTitle{#2}\gdef\otHeadTag{\otTwoDigits{#1}}%
 \global\otCorrigestrue\gdef\otAccent{otGreenDark}\global\otSouplefalse
 \markboth{Corrigés · #2}{Corrigés · #2}\phantomsection\label{corchap-#1}%
 \pdfbookmark[1]{\otTwoDigits{#1} · #2}{bm-corchap-#1}%
 \begin{tikzpicture}
 \fill[otGreenTint,rounded corners=2mm] (0,0) rectangle (\linewidth,18mm);
 \node[fill=otGreenDark,rounded corners=1mm,text=white,minimum height=8mm,
 font=\otBold\fontsize{11}{12}\selectfont]at(8mm,9mm){\otTwoDigits{#1}};
 \node[anchor=west,text width=102mm,align=left,font=\otSemi\fontsize{12}{14}\selectfont]
 at(17mm,9mm){#2};
 \node[anchor=east,font=\otMedium\fontsize{7}{9}\selectfont,text=otMuted]
 at([xshift=-4mm]\linewidth,9mm){\otRenvoi{Énoncés}{chap-#1}};
 \end{tikzpicture}\par\vspace{3mm}}
% Les liens pointent vers le site de la collection, sans promettre une ressource particulière.
\renewcommand{\otQRCours}{\begin{minipage}{30mm}\centering
 {\color{otNavy}\qrcode[height=18mm,nolink]{\otURL}}\par\smallskip
 {\otLight\fontsize{7}{9}\selectfont\otSite}\end{minipage}}
''')
    write('liminaires/copyright.tex',r'''\thispagestyle{empty}\vspace*{\fill}
\begin{minipage}{135mm}\fontsize{9.5}{14}\selectfont\color{otMuted}
{\otSemi\color{otInk}Physique-chimie · Seconde générale et technologique}\par\medskip
Collection OptiTAB. Édition du 25 octobre 2026.\par
240 exercices de chapitre, 20 défis et six évaluations originales corrigées.\par\medskip
Référence : programme français de physique-chimie de Seconde générale et technologique,
BO spécial n° 1 du 22 janvier 2019, arrêté du 17 janvier 2019, NOR MENE1901634A.
Programme signalé en vigueur sur Éduscol lors de la vérification du 25 octobre 2026.
L'ordre des chapitres et les formats d'évaluation sont des choix de la collection.\par\medskip
Ce manuel indépendant n'est pas une publication du ministère de l'Éducation nationale.
Les cours, situations d'entraînement et figures ont été rédigés pour cet ouvrage ; aucune
annale ni aucun exercice d'éditeur n'est reproduit. Les mesures des exercices sont construites
ou idéalisées pour l'entraînement. Les constantes et les références sont indiquées dans les annexes.\par\medskip
Les schémas sont vectoriels. Les échelles utiles à une construction ou une lecture sont précisées ;
les autres dessins sont des schémas de principe. Les activités expérimentales se réalisent
avec l'encadrement et le matériel adaptés au laboratoire scolaire.\par\medskip
© OptiTAB, 2026.\quad\otSite
\end{minipage}\clearpage''')
    write('liminaires/mode-emploi.tex',r'''\editionPage{mode-emploi}{Apprendre avec ce livre}{Comprendre, chercher, vérifier, recommencer}{Un parcours complet pour l'année de Seconde}
\editionEtape{Le cours donne du sens}
Les définitions, lois et méthodes précisent les conditions d'application. Les exemples montrent comment passer du texte à un calcul ; les schémas accompagnent les phénomènes, les montages et les modèles. Les activités expérimentales proposent une démarche à discuter avec l'enseignant.
\editionEtape{Douze exercices par chapitre}
Les exercices 1 à 4 installent les bases, les 5 à 8 consolident les méthodes et les 9 à 12 demandent davantage de raisonnement. Les points de difficulté sont indiqués dans les en-têtes. Chercher avant de lire la solution : une correction comprise se vérifie en refaisant l'exercice sans aide.
\editionEtape{Des figures dans les deux sens}
Quand un tracé est demandé, l'énoncé fournit les données et le support utiles. La version corrigée ajoute les vecteurs, rayons ou projections nécessaires. Les légendes distinguent les schémas de principe des dessins à l'échelle. Les unités et les échelles font partie de la réponse.
\editionEtape{Approfondir et s'évaluer}
Vingt défis mobilisent plusieurs idées de chaque chapitre. Des indications progressives précèdent leurs corrigés. Six évaluations de 90 minutes, notées sur 20, permettent de travailler sans le cours ; les barèmes valorisent les étapes de raisonnement. Ce format est pédagogique : il n'existe pas d'épreuve nationale unique de Seconde.
\editionRetenir{Une bonne réponse associe une idée physique, une relation justifiée, un calcul avec unités et une conclusion liée à la question.}
\clearpage''')
    write('liminaires/sommaire.tex',r'''\thispagestyle{otFront}\phantomsection\pdfbookmark[0]{Sommaire}{bm-sommaire}
\otPageTitre{Sommaire}{Seconde générale et technologique · Physique-chimie}
\vspace{-6mm}\sommaire\clearpage
\editionPage{ressources}{Parcours et ressources}{Naviguer dans le manuel}{Les numéros de page sont cliquables.}
\otLigneRessource{defis-debut}{20 défis d'approfondissement}
\otLigneRessource{indices-defis}{Indications progressives}
\otLigneRessource{methodes-devoir}{Préparer une évaluation}
\otLigneRessource{fiches-experimentales}{Fiches pratiques de laboratoire}
\otLigneRessource{ateliers-python}{Ateliers numériques : graphiques, vecteurs et étalonnage}
\otLigneRessource{devoir-1}{Six évaluations corrigées et notées sur 20}
\otLigneRessource{corriges-debut}{Corrigés des 240 exercices de chapitre}
\otLigneRessource{defi-cor-1-1}{Solutions des 20 défis}
\otLigneRessource{devoir-1-cor}{Corrigés et barèmes des évaluations}
\otLigneRessource{donnees-utiles}{Constantes, unités et formules utiles}
\otLigneRessource{couverture-programme}{Correspondance avec le programme}
\otLigneRessource{references}{Références officielles}
\clearpage''')
    rows=''
    for i,c in enumerate(ch,1):
        rows+=f'{i:02d} & {c["titre"]} & \\caseSuivi & \\caseSuivi & \\caseSuivi \\\\\n'
    write('liminaires/parcours.tex',r'''\editionPage{progression}{Suivre ses progrès}{Un bilan utile après chaque chapitre}{Cocher après avoir travaillé sans le corrigé.}
\begin{tabularx}{\linewidth}{@{}rYccc@{}}\toprule
N° & Chapitre & Cours & Exos & Défi\\\midrule
'''+rows+r'''\bottomrule\end{tabularx}\par\medskip
\small Une case cochée signifie « je sais expliquer et refaire ». Si une méthode reste fragile, noter un exercice à reprendre puis le refaire quelques jours plus tard. Les erreurs de conversion, de signe et de légende méritent une attention particulière.
\clearpage''')
    write('annexes/methodes-devoir.tex',r'''\editionPage{methodes-devoir}{Réussir une évaluation}{Six devoirs originaux de 90 minutes}{Calculatrice autorisée ; documents et données intégrés.}
\editionEtape{Avant de commencer}
Lire les trois exercices et repérer les points. Réserver environ dix minutes à la lecture et à la relecture finale ; répartir le reste selon les barèmes. Les exercices sont indépendants. S'assurer que chaque feuille porte les références de l'exercice et des questions.
\editionEtape{Pendant la recherche}
Souligner ce qui est demandé. Recopier les données utiles avec unités, définir les grandeurs et citer la loi. Pour un problème ouvert, présenter une hypothèse raisonnable, une démarche et ses limites ; une tentative justifiée peut être valorisée même si elle n'aboutit pas.
\editionEtape{Avant de rendre}
Vérifier les conversions, le signe des vecteurs et tensions, le sens des rayons, les coefficients des équations et le nombre de chiffres significatifs. Donner une phrase de conclusion, pas seulement le résultat de la calculatrice.
\editionEtape{Se corriger}
Le corrigé associe une réponse à chaque question et indique ses points. Accorder des points aux étapes correctement réalisées, sans compter deux fois la même compétence. Une erreur numérique isolée ne doit pas annuler un raisonnement ensuite cohérent. Noter la cause de l'erreur puis reprendre un exercice du chapitre correspondant.
\editionRetenir{Les barèmes sont des propositions de correction pédagogique ; l'enseignant peut adapter les critères à son évaluation.}
\editionPage{fiches-experimentales}{Fiche pratique · Chimie}{Préparer, transformer, identifier}{Repères à utiliser avec un protocole encadré.}
\editionEtape{Avant la manipulation}
Lire les dangers, préparer blouse et lunettes, attacher les cheveux et identifier les déchets. Choisir la verrerie selon le besoin : manipuler, mesurer approximativement, prélever précisément ou fixer un volume final. Étiqueter les récipients.
\editionEtape{Préparer une solution}
Pour dissoudre : pesée, dissolution, transfert quantitatif et rinçages, ajustement puis homogénéisation. Pour diluer : calcul du prélèvement, pipette et propipette, fiole jaugée, ajustement puis homogénéisation. Lire le ménisque à hauteur des yeux.
\schema{dilution}
\editionEtape{Chauffer et identifier}
Au reflux, l'eau entre en bas du réfrigérant et sort en haut ; le système communique avec l'atmosphère. En CCM, placer les dépôts au-dessus du bain, repérer le front et comparer des pistes développées ensemble. Un réfrigérant condense ; une CCM aide à identifier : les fonctions ne se confondent pas.
\editionPage{fiche-physique}{Fiche pratique · Physique}{Mesurer sans confondre les grandeurs}{Un schéma du montage fait partie du compte rendu.}
\editionEtape{Mouvement et son}
Étalonner l'espace et le temps, pointer un même point et citer le référentiel. Distinguer distance de déplacement et longueur d'un vecteur vitesse. Pour le son, distinguer retard entre deux capteurs et période du motif. Contrôler les éventuels trajets aller-retour.
\editionEtape{Optique}
Construire la normale avant de mesurer des angles. Pour une lentille, indiquer axe, O, foyers, échelles, objet et sens de propagation. Une image réelle nette se forme dans un plan précis ; déplacer l'écran jusqu'à ce plan.
\editionEtape{Électricité et capteurs}
Couper l'alimentation avant de modifier un branchement. Ampèremètre en série, voltmètre en dérivation ; vérifier entrées et calibres. Pour un capteur, étalonner avec une référence et vérifier le domaine de validité. Les exemples numériques de convertisseur du livre sont fictifs : utiliser la documentation de la carte réelle.
\schema[corrige]{mesures-circuit}
\editionRetenir{Un compte rendu distingue observation, modèle et conclusion. Il indique les limites de mesure, les unités et les hypothèses.}
\input{annexes/ateliers-python}
''')
    write('annexes/ateliers-python.tex',r'''\editionPage{ateliers-python}{Atelier numérique 1}{Positions et vecteurs vitesse}{Python · Matplotlib · Données construites en mètres et secondes}
\begin{python}
import matplotlib.pyplot as plt
t = [0, .2, .4, .6, .8]
x = [0, .2, .8, 1.8, 3.2]
y = [0, .1, .2, .3, .4]
vx = []; vy = []
for i in range(len(t)-1):
    dt = t[i+1] - t[i]
    vx.append((x[i+1]-x[i])/dt)
    vy.append((y[i+1]-y[i])/dt)
fig, ax = plt.subplots()
ax.plot(x, y, 'o', label='Positions')
ax.quiver(x[:-1], y[:-1], vx, vy,
          angles='xy', scale_units='xy', scale=5,
          color='green', label='Vitesses approchees')
ax.set(xlabel='x (m)', ylabel='y (m)')
ax.set_aspect('equal', adjustable='box')
ax.grid(); ax.legend(); plt.show()
print(vx, vy)
\end{python}
\editionEtape{Chercher et vérifier}
Pourquoi quatre vecteurs pour cinq positions ? Que représente le facteur \texttt{scale=5} ? Changer les données pour un mouvement rectiligne uniforme.
\editionRetenir{Le programme affiche $v_x=[1;3;5;7]$ et $v_y=[0,5;0,5;0,5;0,5]$ en m/s. Chaque vecteur utilise deux positions. Ici 1 m/s produit une flèche de 0,2 unité de l'axe spatial : c'est une échelle de représentation, pas une durée de déplacement.}
\editionPage{atelier-ohm}{Atelier numérique 2}{Caractéristique d'un conducteur}{Python · NumPy et Matplotlib · Courant converti en ampères}
\begin{python}
import numpy as np
import matplotlib.pyplot as plt
i_ma = np.array([0, 10, 20, 30, 40])
u = np.array([0.01, 2.00, 4.02, 5.99, 8.01])
i = i_ma / 1000
a, b = np.polyfit(i, u, 1)
print('Pente en ohms :', a)
print('Decalage en volts :', b)
plt.scatter(i, u, label='Mesures')
plt.plot(i, a*i+b, label='Ajustement affine')
plt.xlabel('I (A)'); plt.ylabel('U (V)')
plt.grid(); plt.legend(); plt.show()
\end{python}
\editionEtape{Chercher et vérifier}
Pourquoi convertir l'intensité ? La pente donne environ 199,9 ohms et le décalage environ 0,008 V. Discuter ce décalage à l'échelle d'une incertitude de lecture de 0,03 V. Estimer le point de fonctionnement sous 6,0 V avec un modèle ohmique de 200 ohms.
\editionRetenir{La pente dépend des unités des axes. Le petit décalage est inférieur à l'incertitude annoncée ; un modèle passant par l'origine paraît ici acceptable. Sous 6,0 V, $I\simeq30$ mA.}
\editionPage{atelier-statistique}{Atelier numérique 3}{Variabilité et histogramme}{Tableur ou Python · Mesures indépendantes d'un volume}
\begin{python}
import numpy as np
import matplotlib.pyplot as plt
v = np.array([9.8, 9.9, 10.0, 10.0, 10.1, 10.2])
moyenne = v.mean()
s = v.std(ddof=1)  # ecart-type d'echantillon
u = s / np.sqrt(len(v))
print(moyenne, s, u)
classes = [9.75, 9.95, 10.15, 10.35]
plt.hist(v, bins=classes, edgecolor='white')
plt.xlabel('Volume (mL)'); plt.ylabel('Effectif')
plt.show()
\end{python}
\editionEtape{Transposer dans un tableur}
Placer les six valeurs dans une colonne. Calculer leur moyenne et l'écart-type d'échantillon avec les fonctions adaptées du logiciel ; construire des classes de largeur 0,20 mL. Comparer les effectifs à ceux du programme.
\editionRetenir{On obtient une moyenne de 10,0 mL, $s\simeq0,141$ mL et $u(\bar V)\simeq0,058$ mL. Les classes ont pour effectifs 2, 3 et 1. L'écart-type des valeurs individuelles et l'incertitude sur la moyenne sont différents.}
\editionPage{atelier-microcontroleur}{Atelier numérique 4}{Commander et acquérir}{Algorithmes à adapter au matériel réellement utilisé}
\editionEtape{Produire un son}
Une sortie numérique peut commander un transducteur adapté. Pour un signal carré de fréquence 500 Hz, la période vaut 2 ms : maintenir l'état haut pendant 1 ms, puis l'état bas pendant 1 ms, et répéter. La durée d'exécution et les temporisations de la carte doivent être prises en compte ; une fonction de génération dédiée est préférable quand elle est disponible.
\begin{docu}{1}{Pseudocode de production}
Choisir la sortie et le transducteur selon la documentation.\par
Répéter pendant la durée choisie : état haut ; attendre $T/2$ ; état bas ; attendre $T/2$.\par
Vérifier la fréquence avec un microphone ou un dispositif d'acquisition.\end{docu}
\editionEtape{Acquérir un capteur}
Lire le code ; le convertir en tension avec la référence et la résolution de la carte ; retrouver la résistance du capteur ; appliquer l'étalonnage ; vérifier les domaines avant affichage. Utiliser la même référence électrique que le circuit et respecter les tensions admissibles.
\editionRetenir{Le programme traite un modèle de mesure. Changer de carte, de capteur ou de tension de référence demande de revoir les paramètres et de vérifier la chaîne avec une mesure connue.}
''')
    write('annexes/donnees-programme.tex',r'''\editionPage{donnees-utiles}{Données et relations utiles}{Toujours vérifier les unités et les conditions}{Valeurs arrondies pour les exercices, sauf indication contraire.}
\begin{tabularx}{\linewidth}{@{}YY@{}}\toprule
Constante ou grandeur & Valeur utilisée\\\midrule
Constante d'Avogadro & $N_A\simeq6,02\times10^{23}\unit{mol^{-1}}$\\
Charge élémentaire & $e\simeq1,60\times10^{-19}\unit{C}$\\
Masse d'un nucléon & $m_n\simeq1,67\times10^{-27}\unit{kg}$\\
Masse d'un électron & $m_e\simeq9,11\times10^{-31}\unit{kg}$\\
Constante de gravitation & $G\simeq6,67\times10^{-11}\unit{N.m^2.kg^{-2}}$\\
Pesanteur terrestre usuelle & $g\simeq9,8\unit{N.kg^{-1}}$ (ou 10 si fourni)\\
Lumière dans le vide ou l'air & $c\simeq3,00\times10^8\unit{m.s^{-1}}$\\
Son dans l'air ambiant & $v\simeq340\unit{m.s^{-1}}$\\
Eau liquide vers 20 °C & $\rho\simeq1,00\unit{g.mL^{-1}}$\\
Énergie massique de fusion de l'eau & $L_f\simeq334\unit{kJ.kg^{-1}}$\\\bottomrule
\end{tabularx}
\editionEtape{Conversions fréquentes}
$1\unit{L}=10^{-3}\unit{m^3}$ ; $1\unit{mL}=1\unit{cm^3}$ ; $1\unit{g}=10^{-3}\unit{kg}$ ; $1\unit{ms}=10^{-3}\unit{s}$ ; $1\unit{nm}=10^{-9}\unit{m}$. Pour passer de km/h à m/s, diviser par 3,6.
\editionEtape{Relations à retrouver avec leur sens}
$\rho=m/V$ ; $c_m=m_s/V_s$ ; $c_{m,m}V_p=c_{m,f}V_f$ ; $N=m/m_{\mathrm{entité}}$ ; $n=N/N_A$ ; $E=mL$ ; $P=mg$ ; $F=Gm_Am_B/d^2$ ; $v=d/\Delta t$ ; $f=1/T$ ; $n_1\sin i=n_2\sin r$ ; $U=RI$.
\editionRetenir{Une formule seule ne suffit pas : définir les symboles et vérifier le système, les hypothèses et les unités avant de l'appliquer.}
\editionPage{couverture-programme}{Correspondance avec le programme}{Repères de lecture et d'entraînement}{Le découpage du livre respecte les trois thèmes du BO et les compétences transversales.}
'''+''.join(f'\\editionEtape{{{i:02d} · {c["titre"]}}}\n'+ '; '.join(c['capacites']).replace('_',r'\_')+'. '+f'Cours et exercices du chapitre {i}, défi D{i:02d}.\n' for i,c in enumerate(ch,1)))
    write('liminaires/references.tex',r'''\editionPage{references}{Références officielles}{Recherche documentaire du 25 octobre 2026}{Sources de cadrage ; exercices et figures rédigés pour ce manuel.}
\editionEtape{Programme français}
Ministère de l'Éducation nationale, programme de physique-chimie de Seconde générale et technologique, arrêté du 17 janvier 2019, BO spécial n° 1 du 22 janvier 2019, NOR MENE1901634A. Annexe de 13 pages.\par\smallskip
\url{https://www.education.gouv.fr/bo/19/Special1/MENE1901634A.htm}
\editionEtape{Vérification du programme en vigueur}
Éduscol, « Programmes et ressources en physique-chimie - voie GT », page mise à jour en mars 2026, consultée le 25 octobre 2026. Le programme de Seconde y est référencé sous le BO de janvier 2019.\par\smallskip
\href{https://eduscol.education.gouv.fr/5829/programmes-et-ressources-en-physique-chimie-voie-gt}{Éduscol : programmes et ressources en physique-chimie, voie GT.}
\editionEtape{Ressources d'accompagnement consultées}
Ressources Éduscol sur le cortège électronique, le dénombrement des entités et les signaux électriques en Seconde ; fiches d'accompagnement pour Python : positions, vecteurs déplacement et vitesse, graphiques et variabilité des volumes. Elles éclairent le niveau attendu et la démarche de modélisation.
\editionEtape{Méthode éditoriale}
Le programme a été lu dans son intégralité pour établir la correspondance des notions et des capacités. Les activités du livre sont originales et leurs données sont adaptées à l'apprentissage. Les six devoirs ne sont pas des sujets nationaux : il s'agit d'évaluations de la collection, avec corrigés et barèmes proposés.
''')
