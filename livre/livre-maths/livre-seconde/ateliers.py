FIGURES_ATELIERS={'atelier-nuage':'stats-nuage'}

ATELIERS=[
('atelier-debut','Atelier numérique','Balayer pour proposer un maximum',r'''\editionEtape{Un calcul sur une grille}
Pour $f(x)=4-(x-1{,}3)^2$ sur $[0;3]$, on découpe l’intervalle en $n$ morceaux égaux. La fonction suivante garde la meilleure valeur de la grille.
\begin{python}
def balayage(n):
    xbest, vbest = 0, 4 - 1.3**2
    for k in range(1, n + 1):
        x = 3 * k / n
        v = 4 - (x - 1.3)**2
        if v > vbest:
            xbest, vbest = x, v
    return xbest, vbest
\end{python}
\editionEtape{Lire la sortie et contrôler}
Le domaine est $n\ge1$ entier. Pour $n=3$, la grille contient 0, 1, 2 et 3 ; le programme renvoie 1 et 3,91. Pour $n=30$, 1,3 appartient à la grille et la valeur 4 est obtenue. On sait algébriquement que $4-(x-1{,}3)^2\le4$ : l’optimum peut être démontré.
\editionEtape{Tableur et géométrie dynamique}
Dans un tableur, préparer les abscisses et les images puis rechercher la plus grande valeur. Dans un logiciel de géométrie, déplacer un point sur la courbe. Comparer les observations à la preuve algébrique.
\editionRetenir{Un outil numérique aide à chercher. Pour annoncer un optimum exact et global, préciser le raisonnement qui le garantit.}'''),
('atelier-filtres','Atelier numérique','Deux listes, des filtres et un tableau croisé',r'''\editionEtape{Lire un format fourni}
Deux listes décrivent huit individus : l’individu numéro $i$ a le groupe \code{groupe[i]} et la réponse \code{reponse[i]}. Les listes sont fournies ; il suffit de lire le rôle du programme.
\begin{python}
groupe  = ["A", "B", "A", "A", "B", "B", "A", "B"]
reponse = ["O", "N", "N", "O", "O", "N", "N", "O"]

def compter(g, r):
    total = 0
    for i in range(8):
        if groupe[i] == g and reponse[i] == r:
            total = total + 1
    return total

def freq_cond(r, g):
    return compter(g, r) / (compter(g, "O") + compter(g, "N"))
\end{python}
\editionEtape{Comprendre et modifier}
\code{compter("A", "O")} renvoie 2 : les quatre appels pour $A/B$ et $O/N$ remplissent le tableau croisé, dont les quatre cases valent 2 et les marges 4. \code{freq\_cond("O", "A")} renvoie 0,5, fréquence conditionnelle de O parmi A ; la fréquence marginale de O vaut $4/8=0{,}5$. Remplacer \code{and} par \code{or} compte « A OU O » : six individus. Le filtre \code{not reponse[i] == "O"} (NON O) retient quatre réponses N.
\editionEtape{Avec un tableur}
Saisir les deux colonnes et filtrer. Un tableau croisé compte chaque combinaison ; contrôler que les marges retrouvent 8. Ces données sont construites pour l’activité.
\editionRetenir{Les effectifs retenus dépendent du connecteur logique ; une ligne doit être comptée une seule fois.}'''),
('atelier-nuage','Lecture graphique','Lire et commenter un nuage de points',r'''\editionEtape{Lire les deux axes}
Les six points représentent six trajets à vélo. L’abscisse est la durée en minutes et l’ordonnée la distance en kilomètres. Les données sont construites pour l’activité.
\par\medskip
\textbf{Questions.} Lire les deux distances observées pour 20 minutes. Quelle proportion des trajets atteint au moins 6 km ? Une durée détermine-t-elle toujours une seule distance ? La distance est-elle proportionnelle à la durée ?
@@FIGURE@@
\editionEtape{Corrigé expliqué}
À l’abscisse 20, les deux ordonnées sont \res{3\text{ km et }5\text{ km}}. Trois points sur six ont une ordonnée supérieure ou égale à 6 : la proportion vaut \res{3/6=50\,\%}.
\par\medskip
La durée 20 donne deux distances : ce nuage ne représente donc pas une fonction de la durée. Il n’y a pas non plus de proportionnalité : les rapports $2/10=0{,}2$ et $3/20=0{,}15$ diffèrent.
\par\medskip
Le nuage suggère une tendance croissante d’ensemble. Il ne permet pas de connaître exactement une distance pour 35 minutes : cette durée n’a pas été observée.
\editionRetenir{Lire les unités et les échelles avant de commenter. Chaque point est une observation ; relier les points ou interpoler demande une hypothèse supplémentaire.}'''),
('culture-debut','Culture mathématique','Des idées à relier au cours',r'''\editionEtape{Des nombres aux preuves}
L’arithmétique et l’irrationalité relient la manipulation des nombres à la nécessité de démontrer. Les preuves sur $1/3$ et $\sqrt2$ montrent qu’une longue observation ne remplace pas une justification générale.
\editionEtape{Des calculs aux équations}
Les travaux d’auteurs comme Al-Khwarizmi, puis l’évolution du symbolisme algébrique, mettent en perspective la puissance des lettres : une seule transformation traite une famille de calculs. Reconstruire une identité illustre ce gain de généralité.
\editionEtape{Des figures aux coordonnées}
La méthode des coordonnées associée à Descartes relie une figure à des équations. Les chapitres de droites et les défis de lieux donnent des exemples de ce passage entre registres.
\editionEtape{Des jeux au hasard mathématisé}
Les problèmes étudiés dans les échanges de Pascal et Fermat, ainsi que les jeux de dés, montrent l’importance du modèle et du dénombrement. D16 travaille le choix des issues équiprobables avant le calcul d’une probabilité.
\editionRetenir{Pour une présentation orale, distinguer le contexte historique, la question mathématique et la solution moderne.}''')
]
