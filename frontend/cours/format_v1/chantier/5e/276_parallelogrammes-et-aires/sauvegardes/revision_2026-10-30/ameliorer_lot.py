# -*- coding: utf-8 -*-
"""Révision éditoriale reproductible des notions 276 à 280 ; aucun accès base."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DOSSIERS = {int(p.name[:3]): p for p in ROOT.iterdir() if p.name[:3] in {'276','277','278','279','280'}}

COURS = {
276: r'''::: objectifs
Reconnaître, construire et justifier un parallélogramme. Utiliser ses propriétés et calculer une aire en choisissant la hauteur correspondante.
:::

## I. Reconnaître un parallélogramme

::: definition
Un **parallélogramme** est un quadrilatère dont les côtés opposés sont parallèles deux à deux. Pour $ABCD$, nommé dans l'ordre du contour :
$$ (AB)\parallel(CD)\quad\text{et}\quad(AD)\parallel(BC). $$
:::

[IMAGE_1]

::: propriete
Dans un parallélogramme :
- les côtés opposés ont la même longueur : $AB=CD$ et $AD=BC$ ;
- les diagonales se coupent en leur milieu : $AO=OC$ et $BO=OD$ ;
- les angles opposés ont la même mesure.
Le milieu commun $O$ des diagonales est le **centre de symétrie** du parallélogramme.
:::

::: attention
Les diagonales ne sont pas nécessairement de même longueur, ni perpendiculaires. Une figure qui « ressemble » à un parallélogramme ne constitue pas une preuve.
:::

## II. Construire et démontrer

::: propriete Critères pour un quadrilatère non croisé
Il suffit de vérifier **l'un** des critères suivants :
- ses côtés opposés sont parallèles deux à deux ;
- ses côtés opposés ont la même longueur deux à deux ;
- ses diagonales ont le même milieu ;
- deux côtés opposés sont à la fois parallèles et de même longueur.
:::

::: methode Construire le quatrième sommet
On connaît trois sommets consécutifs $A$, $B$ et $C$.
1. Tracer par $A$ la parallèle à $(BC)$.
2. Tracer par $C$ la parallèle à $(AB)$.
3. Leur intersection est $D$.
Autre méthode : construire le milieu $O$ de $[AC]$, puis le symétrique de $B$ par rapport à $O$.
:::

::: demonstration Pourquoi le critère des diagonales fonctionne
Si $[AC]$ et $[BD]$ ont le même milieu $O$, la symétrie centrale de centre $O$ échange $A$ et $C$, puis $B$ et $D$. Elle transforme donc $(AB)$ en $(CD)$ et $(AD)$ en $(CB)$. Une droite et son image sont parallèles : $ABCD$ est un parallélogramme.
:::

## III. Rectangle, losange et carré

| Figure | Définition à partir d'un parallélogramme | Diagonales |
|---|---|---|
| Rectangle | Possède un angle droit | De même longueur |
| Losange | Possède deux côtés consécutifs égaux | Perpendiculaires |
| Carré | Est à la fois rectangle et losange | De même longueur et perpendiculaires |

::: attention
Les critères portant sur les diagonales s'appliquent ici à un **parallélogramme déjà établi**. Deux diagonales de même longueur ne suffisent pas, à elles seules, à prouver qu'un quadrilatère est un rectangle.
:::

## IV. Calculer une aire

::: definition Hauteur relative à une base
La hauteur est la distance **perpendiculaire** entre la droite portant la base et la droite portant le côté opposé. Son pied peut se situer sur le prolongement de la base.
:::

[IMAGE_2]

::: formule
$$\mathcal A_{\text{parallélogramme}}=b\times h$$
$b$ et $h$ doivent être exprimées dans la même unité de longueur.
:::

::: exemple Un terrain
Pour une base de $6\,\mathrm m$, un côté oblique de $4\,\mathrm m$ et une hauteur de $2\,\mathrm m$ :
$$\begin{aligned}
P&=2\times(6+4)=20\,\mathrm m,\\
\mathcal A&=6\times2=12\,\mathrm{m}^2.
\end{aligned}$$
Le côté oblique n'est pas la hauteur. Le périmètre mesure le contour ; l'aire mesure la surface.
:::

::: methode Une figure composée
Découper en rectangles, triangles ou parallélogrammes, puis additionner les aires. On peut aussi soustraire une partie d'une figure plus grande. Pour un triangle, $\mathcal A=b\times h\div2$.
:::

::: retenir
$1\,\mathrm{m}^2=100\,\mathrm{dm}^2=10\,000\,\mathrm{cm}^2$. Convertir toutes les aires dans la même unité avant de les additionner.
:::
''',
277: r'''::: objectifs
Lire une représentation de solide, reconnaître un patron et calculer une aire de disque ou un volume. Passer des unités de volume aux capacités.
:::

## I. Représenter des solides

::: definition
- Un **pavé droit** a six faces rectangulaires, douze arêtes et huit sommets.
- Un **cube** est un pavé droit dont les six faces sont des carrés.
- Un **prisme droit** possède deux bases polygonales superposables et parallèles ; ses faces latérales sont des rectangles.
- Un **cylindre de révolution** possède deux bases en forme de disques et une surface latérale courbe.
:::

[IMAGE_1]

::: methode Lire une perspective cavalière
Les arêtes parallèles restent parallèles sur le dessin ; les arêtes cachées sont en pointillés. Lire les dimensions indiquées : une longueur oblique sur le dessin ne se mesure pas directement à la règle pour retrouver la dimension réelle.
:::

::: attention
Une perspective peut cacher des cubes dans un empilement. Une vue de dessus, une vue de face ou un tableau des hauteurs doit préciser les éléments invisibles.
:::

## II. Passer du solide au patron

::: definition
Un **patron** est une figure plane qui permet de reconstituer la surface d'un solide par pliage, sans chevauchement des faces. Les bords qui se rejoignent doivent avoir la même longueur.
:::

::: exemple
Un prisme droit à base triangulaire a deux triangles identiques et trois rectangles : il possède donc cinq faces. Un cube nécessite six carrés ; leur disposition doit permettre le pliage.
:::

[IMAGE_2]

::: propriete Patron du cylindre fermé
Pour un rayon $r$ et une hauteur $h$, il faut :
- deux disques de rayon $r$ ;
- un rectangle de dimensions $h$ et $2\pi r$.
La longueur du rectangle correspond au tour d'une base.
:::

## III. Calculer un volume

::: formule
$$V_{\text{prisme droit}}=B\times h$$
$B$ est l'**aire** d'une base et $h$ la distance entre les deux bases.
:::

| Solide | Volume |
|---|---|
| Pavé droit | $L\times\ell\times h$ |
| Cube de côté $c$ | $c\times c\times c=c^3$ |

::: exemple Base triangulaire
Un triangle rectangle a deux côtés perpendiculaires de $6\,\mathrm{cm}$ et $4\,\mathrm{cm}$. La distance entre les bases du prisme vaut $10\,\mathrm{cm}$.
$$\begin{aligned}
B&=6\times4\div2=12\,\mathrm{cm}^2,\\
V&=12\times10=120\,\mathrm{cm}^3.
\end{aligned}$$
La hauteur du triangle sert au calcul de $B$ ; la hauteur du solide sert au calcul de $V$.
:::

## IV. Disque et cylindre

[IMAGE_3]

::: formule
$$P_{\text{cercle}}=2\pi r\qquad \mathcal A_{\text{disque}}=\pi r^2$$
$$V_{\text{cylindre}}=\pi r^2\times h$$
Le rayon est la moitié du diamètre : $r=d\div2$.
:::

::: exemple Rayon $3\,\mathrm{cm}$ et hauteur $8\,\mathrm{cm}$
$$\begin{aligned}
B&=\pi\times3^2=9\pi\,\mathrm{cm}^2,\\
V&=9\pi\times8=72\pi\,\mathrm{cm}^3\\
&\approx226\,\mathrm{cm}^3.
\end{aligned}$$
On conserve $\pi$ pour la valeur exacte puis on arrondit à l'unité à la fin.
:::

## V. Convertir un volume ou une capacité

::: propriete
$$1\,\mathrm m^3=1\,000\,\mathrm{dm}^3$$
$$1\,\mathrm{dm}^3=1\,000\,\mathrm{cm}^3$$
Chaque changement vers l'unité de volume immédiatement plus petite multiplie par $1\,000$ : on multiplie les trois dimensions par $10$.
:::

::: retenir
$$1\,\mathrm L=1\,\mathrm{dm}^3\qquad1\,\mathrm{mL}=1\,\mathrm{cm}^3$$
$$1\,\mathrm m^3=1\,000\,\mathrm L$$
$1\,\mathrm L=100\,\mathrm{cL}=1\,000\,\mathrm{mL}$.
:::

::: attention
Pour peindre une surface, on calcule une **aire**, en unités carrées. Pour remplir un récipient, on calcule un **volume**, en unités cubes, puis éventuellement une capacité en litres. Mettre les longueurs dans la même unité avant tout produit.
:::
''',
278: r'''::: objectifs
Organiser un relevé, calculer des effectifs et des fréquences, lire des diagrammes et interpréter une moyenne simple.
:::

## I. Organiser les données

::: definition
La **population** est le groupe étudié ; le **caractère** est l'information relevée pour chaque individu. L'**effectif** d'une valeur ou d'une catégorie est son nombre d'apparitions. L'**effectif total** est la somme des effectifs.
:::

::: exemple Une enquête sur les trajets
Vingt élèves donnent chacun leur mode principal de transport.
| Transport | À pied | Vélo | Bus | Total |
|---|---|---|---|---|
| Effectif | $10$ | $6$ | $4$ | $20$ |
| Fréquence | $50\,\%$ | $30\,\%$ | $20\,\%$ | $100\,\%$ |
La population est la classe ; le caractère est le mode principal de transport.
:::

## II. Calculer une fréquence

::: formule
$$\text{fréquence}=\frac{\text{effectif de la catégorie}}{\text{effectif total}}$$
L'effectif total doit être non nul. Une fréquence s'écrit comme une fraction, un nombre décimal ou un pourcentage.
:::

::: exemple
Pour le vélo :
$$f=\frac6{20}=0{,}3=30\,\%.$$
Les catégories couvrent tous les élèves sans chevauchement : leurs fréquences ont pour somme $1$, soit $100\,\%$.
:::

::: attention
Un effectif compte des personnes ; une fréquence décrit une proportion. $30\,\%$ n'est pas un nombre d'élèves tant qu'on ne connaît pas l'effectif total.
:::

## III. Choisir et lire un diagramme

[IMAGE_1]

| Représentation | Utilité | Points à vérifier |
|---|---|---|
| Diagramme en barres | Comparer les catégories | Hauteur, échelle et unité |
| Diagramme circulaire | Montrer le partage du total | Proportion de chaque secteur |
| Graphique cartésien | Suivre une évolution | Axes, dates et unités |

::: methode Construire un diagramme circulaire
Le disque entier correspond à $360^\circ$.
$$\text{angle du secteur}=\text{fréquence}\times360^\circ.$$
Pour le vélo : $0{,}3\times360^\circ=108^\circ$.
:::

::: attention Lire avec esprit critique
Vérifier les graduations et le début de l'axe. Des secteurs de même angle dans deux diagrammes représentent les mêmes proportions, mais pas forcément les mêmes effectifs.
:::

## IV. Calculer et interpréter une moyenne

::: definition
La **moyenne simple** d'une série numérique est la somme de ses valeurs divisée par leur nombre. Elle correspond à un partage égal du total.
$$\text{moyenne}=\frac{\text{somme des valeurs}}{\text{nombre de valeurs}}.$$
:::

::: exemple
Pour les valeurs $4$ ; $6$ ; $6$ ; $8$ :
$$\overline x=\frac{4+6+6+8}{4}=\frac{24}{4}=6.$$
Le $6$ apparaît deux fois : il faut le compter deux fois. Si chaque valeur augmente de $1$, la somme augmente de $4$ et la moyenne devient $28\div4=7$.
:::

::: methode Utiliser un tableur
Placer une valeur par cellule. La formule `=MOYENNE(A2:A6)` calcule la moyenne de cinq valeurs. Pour une fréquence, diviser l'effectif par le total puis choisir le format pourcentage.
:::

::: retenir
La moyenne n'est pas nécessairement observée : la moyenne de $2$ ; $3$ ; $10$ est $5$. Deux séries peuvent avoir la même moyenne et des répartitions très différentes. Toujours préciser l'unité et la population étudiée.
:::
''',
279: r'''::: objectifs
Décrire une expérience aléatoire, distinguer issues et événements, calculer des probabilités simples et comprendre les limites d'une expérience courte.
:::

## I. Décrire le hasard

::: definition
Une **expérience aléatoire** est une expérience dont on ne peut pas prévoir avec certitude le résultat avant de la réaliser. Une **issue** est un résultat possible. Un **événement** rassemble une ou plusieurs issues.
:::

::: exemple Un dé à six faces
Les issues sont $1$, $2$, $3$, $4$, $5$ et $6$. L'événement « obtenir un nombre pair » rassemble les issues $2$, $4$ et $6$.
:::

::: propriete
Une probabilité est comprise entre $0$ et $1$. Un événement impossible a pour probabilité $0$ ; un événement certain a pour probabilité $1$.
$$\frac14=0{,}25=25\,\%$$
Une chance sur quatre correspond à $25\,\%$.
:::

::: attention
Très peu probable ne signifie pas impossible ; très probable ne signifie pas certain. Le hasard ne permet pas de prévoir chaque résultat individuel.
:::

## II. Compter les issues équiprobables

::: definition
Il y a **équiprobabilité** lorsque toutes les issues retenues ont la même probabilité. Un dé équilibré donne la même chance à chacune des six faces.
:::

::: formule En cas d'équiprobabilité
$$P(\text{événement})=\frac{\text{nombre d'issues favorables}}{\text{nombre total d'issues}}$$
:::

::: methode Calculer une probabilité
1. Décrire les issues et justifier qu'elles ont la même chance.
2. Compter toutes les issues possibles.
3. Compter celles qui réalisent l'événement.
4. Écrire et simplifier la fraction ; vérifier qu'elle est comprise entre $0$ et $1$.
:::

::: exemple Tirer un jeton
Un sac contient trois jetons rouges et deux bleus, indiscernables au toucher. On mélange et on tire sans regarder.
| Couleur | Rouge | Bleu | Total |
|---|---|---|---|
| Nombre de jetons | $3$ | $2$ | $5$ |
| Probabilité | $\frac35$ | $\frac25$ | $1$ |
Les **cinq jetons** ont la même chance d'être tirés. Les deux **couleurs**, elles, ne sont pas équiprobables.
:::

::: exemple Un dé équilibré
« Obtenir plus de $4$ » signifie obtenir $5$ ou $6$ :
$$P=\frac26=\frac13.$$
L'événement contraire est « obtenir au plus $4$ » : $P=\frac46=\frac23$. Les deux probabilités ont pour somme $1$.
:::

## III. Expérimenter et interpréter

::: definition Fréquence observée
$$f=\frac{\text{nombre de réalisations de l'événement}}{\text{nombre d'essais}}.$$
La probabilité décrit le modèle ; la fréquence décrit les résultats effectivement observés.
:::

::: methode Répéter une expérience
Rétablir les mêmes conditions à chaque essai. Pour un tirage avec remise, remettre le jeton et mélanger. Noter les résultats puis calculer les effectifs et les fréquences.
:::

::: retenir
Une fréquence peut différer de la probabilité, surtout sur peu d'essais. Six lancers ne garantissent pas l'apparition de chaque face. Après un tirage rouge avec remise, la composition du sac reste la même : un nouveau rouge est toujours possible.
:::
''',
280: r'''::: objectifs
Lire une suite d'instructions, prévoir une sortie et traduire une formule par des blocs. Comprendre une répétition et suivre un tracé.
:::

## I. Lire un programme dans l'ordre

::: definition
Un **programme** est une suite d'instructions exécutées dans un ordre précis. Une **entrée** est une donnée fournie ; une **sortie** est une information produite. Le bloc `réponse` contient ici la donnée saisie après une question.
:::

::: exemple Demander, calculer, afficher
Transcription textuelle des blocs, dans leur ordre d'exécution :
```console
demander « Choisir un nombre » et attendre
dire ((3 × réponse) + 2)
```
Pour l'entrée $4$, le programme affiche $3\times4+2=14$.
:::

::: methode Prévoir une sortie
Repérer le bloc qui demande une donnée. Remplacer `réponse` par cette donnée dans le calcul. Respecter les parenthèses et les priorités, puis donner ce qui est affiché.
:::

## II. Comprendre les blocs imbriqués

::: exemple Deux organisations différentes
| Expression décrite par les blocs | Pour l'entrée $4$ |
|---|---|
| $(3\times\text{réponse})+2$ | $3\times4+2=14$ |
| $3\times(\text{réponse}+2)$ | $3\times(4+2)=18$ |
Le bloc placé à l'intérieur est calculé en premier : les parenthèses traduisent cette imbrication.
:::

::: attention
Une phrase affichée n'est pas une nouvelle entrée. La donnée saisie n'est pas modifiée par le simple affichage d'un calcul. Ne pas confondre « multiplier puis ajouter » avec « ajouter puis multiplier ».
:::

## III. Répéter une séquence

::: definition
Une **boucle de répétition** exécute un nombre fixé de fois la même suite d'instructions. Toutes les instructions placées à l'intérieur sont répétées, dans l'ordre.
:::

::: exemple Tracer un carré
Le lutin commence au point $A$, dirigé vers la droite.
```console
stylo en position d'écriture
répéter 4 fois :
    avancer de 60 pas
    tourner à gauche de 90°
```
Il trace quatre segments de $60$ pas et effectue quatre quarts de tour. Il revient en $A$, orienté vers la droite.
:::

[IMAGE_1]

::: methode Suivre une boucle
Faire un tableau avec une ligne par répétition. Relever la direction de chaque déplacement, puis la direction obtenue après la rotation. Compter les déplacements et les rotations séparément.
:::

| Répétition | Déplacement | Direction après rotation |
|---|---|---|
| $1$ | Vers la droite | Vers le haut |
| $2$ | Vers le haut | Vers la gauche |
| $3$ | Vers la gauche | Vers le bas |
| $4$ | Vers le bas | Vers la droite |

## IV. Contrôler le résultat

::: attention Dessin et état final
Une rotation sans déplacement ne trace rien. Si on supprime uniquement la dernière rotation du carré, le dessin reste identique, mais le lutin termine orienté vers le bas.
:::

::: retenir
Vérifier le départ, la direction initiale, le stylo et le contenu exact de la boucle. Pour un triangle équilatéral, le changement de direction vaut $120^\circ$, et non l'angle intérieur $60^\circ$. Quatre déplacements quelconques ne suffisent pas à tracer un carré.
:::
'''
}

FICHES = {
276:r'''::: objectifs
Retrouver les critères, les constructions et la formule d'aire.
:::

## I. Reconnaître et justifier
::: definition
Parallélogramme : côtés opposés parallèles deux à deux.
:::
- Côtés opposés égaux ; angles opposés égaux.
- Diagonales de même milieu $O$, centre de symétrie.
- Pour prouver : côtés opposés parallèles deux à deux, ou égaux deux à deux, ou diagonales de même milieu, ou deux côtés opposés à la fois parallèles et égaux.

## II. Construire et calculer
::: methode
Avec $A$, $B$, $C$ consécutifs : tracer par $A$ la parallèle à $(BC)$ et par $C$ celle à $(AB)$. Leur intersection est $D$.
:::
$$\mathcal A=b\times h\qquad P=2\times(a+b)$$
$h$ est perpendiculaire à la base $b$.
Rectangle : un angle droit. Losange : deux côtés consécutifs égaux. Carré : les deux.

::: attention
Un côté oblique n'est pas une hauteur. Aire en unités carrées ; périmètre en unités de longueur. $1\,\mathrm m^2=10\,000\,\mathrm{cm}^2$.
:::
''',
277:r'''::: objectifs
Choisir la formule et l'unité adaptées.
:::

## I. Aires et volumes
| Figure ou solide | Formule |
|---|---|
| Disque de rayon $r$ | $\mathcal A=\pi r^2$ |
| Pavé droit | $V=L\times\ell\times h$ |
| Cube de côté $c$ | $V=c^3$ |
| Prisme droit | $V=B\times h$ |
| Cylindre | $V=\pi r^2\times h$ |
$B$ est l'aire d'une base ; $h$ est la distance entre les bases ; $r=d\div2$.

## II. Patrons et conversions
Un prisme triangulaire : deux triangles et trois rectangles. Un cylindre fermé : deux disques de rayon $r$ et un rectangle de dimensions $2\pi r$ et $h$.
::: retenir
$$1\,\mathrm L=1\,\mathrm{dm}^3\qquad1\,\mathrm{mL}=1\,\mathrm{cm}^3$$
$1\,\mathrm m^3=1\,000\,\mathrm L$ ; d'une unité de volume à la suivante : multiplier ou diviser par $1\,000$.
:::

::: attention
Convertir les longueurs avant de multiplier. Aire : unité carrée ; volume : unité cube. Conserver $\pi$ jusqu'à l'arrondi demandé.
:::
''',
278:r'''::: objectifs
Distinguer effectif, fréquence et moyenne.
:::

## I. Compter et représenter
L'effectif compte les observations. L'effectif total est la somme des effectifs.
$$f=\frac{\text{effectif de la catégorie}}{\text{effectif total}}$$
$\frac6{20}=0{,}3=30\,\%$. Pour toutes les catégories sans chevauchement : somme des fréquences $=1$.
| Diagramme | Pour quoi faire ? |
|---|---|
| Barres | Comparer des catégories |
| Circulaire | Montrer les proportions |
| Cartésien | Suivre une évolution |
Angle d'un secteur : $f\times360^\circ$.

## II. Calculer une moyenne
$$\text{moyenne}=\frac{\text{somme des valeurs}}{\text{nombre de valeurs}}$$
Compter chaque valeur autant de fois qu'elle apparaît. Ajouter $2$ à chaque valeur augmente la moyenne de $2$.

::: attention
Une moyenne n'est pas forcément observée. Deux groupes de même moyenne peuvent avoir des totaux différents. Un secteur donne une proportion : connaître le total est nécessaire pour retrouver un effectif.
:::
''',
279:r'''::: objectifs
Calculer une probabilité et interpréter un tirage.
:::

## I. Décrire
Une issue est un résultat possible. Un événement rassemble des issues. Équiprobabilité : toutes les issues ont la même chance.
$$0\le P\le1$$
Impossible : $P=0$ ; certain : $P=1$.

## II. Calculer
::: formule En cas d'équiprobabilité
$$P=\frac{\text{nombre d'issues favorables}}{\text{nombre total d'issues}}$$
:::
Dé équilibré : obtenir $5$ ou $6$ donne $P=\frac26=\frac13$. Les probabilités d'un événement et de son contraire ont pour somme $1$.

::: attention
Des jetons équiprobables n'impliquent pas des couleurs équiprobables. Après remise et mélange, la composition reste la même. Le hasard ne doit pas « compenser » les tirages précédents.
:::

::: retenir
La fréquence décrit les essais observés ; la probabilité décrit le modèle. Une courte série ne garantit aucun résultat précis.
:::
''',
280:r'''::: objectifs
Prévoir une sortie et suivre une boucle.
:::

## I. Lire un programme
::: methode
Repérer l'entrée, remplacer `réponse` par la valeur saisie, respecter les blocs imbriqués et calculer la sortie affichée.
:::
Pour l'entrée $4$ : $3\times4+2=14$, tandis que $3\times(4+2)=18$.

## II. Répéter et tracer
Une boucle répète **tout son contenu**, dans l'ordre.
```console
répéter 4 fois :
    avancer de 60 pas
    tourner à gauche de 90°
```
Stylo baissé, départ vers la droite : carré de côté $60$ pas ; distance $240$ pas ; retour au départ avec la direction initiale.

::: attention
Une rotation change la direction, sans tracer. Sans la dernière rotation, le carré reste tracé mais la direction finale change. Pour un triangle équilatéral, tourner de $120^\circ$.
:::
'''
}

def run():
    for num,p in DOSSIERS.items():
        (p/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'donnees_espace','maj':'2026-10-28'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        for pattern,body in [('cours_*.txt',COURS[num]),('fiche_*.txt',FICHES[num])]:
            f=next(p.glob(pattern)); title=f.read_text(encoding='utf8').splitlines()[0]
            f.write_text(title+'\n\n<!-- optitab:1 -->\n'+body,encoding='utf8')
        f=p/'exercices.txt'; text=f.read_text(encoding='utf8')
        text=re.sub(r'::: etape (\$[^\n]+\$)\n:::',r'::: etape Calcul détaillé\n$$\n\1\n$$\n:::',text)
        text=text.replace('$$\n$\\displaystyle','$$\n').replace('$\n$$','\n$$')
        text=re.sub(r'\*\*À retenir :\*\* ([^\n]+)',r'::: retenir\n\1\n:::',text)
        # Chaque méthode dispose d'une étape explicite : les ajouts propres aux
        # familles sont réalisés plus bas sans modifier les identifiants.
        blocks=re.split(r'^===[ \t]*$',text,flags=re.M)
        out=[]
        for b in blocks:
            if not b.strip(): continue
            b=ameliorer_exercice(num,b)
            out.append(b.strip())
        f.write_text('\n\n===\n\n'.join(out)+'\n\n===\n',encoding='utf8')

def ameliorer_exercice(num,b):
    # Corps de l'étape : le raisonnement mathématique, pas une étiquette vide.
    avant,steps=b.split('Étapes:',1); steps,solution=steps.split('Solution:',1)
    chunks=re.split(r'(?=^## Question )',steps,flags=re.M)
    additions={}
    if num==276:
        base,cote,h=map(int,re.search(r'AB = (\d+) m, AD = (\d+) m.*?mesure (\d+) m',avant).groups())
        additions={1:f'Les côtés [BC] et [AD] sont opposés ; il en est de même pour [CD] et [AB]. On reporte donc les longueurs données : {cote} m et {base} m.',4:f'Le produit {base} × {cote} utilise le côté oblique. La distance perpendiculaire entre (AB) et (CD) vaut {h} m : c’est cette mesure qui doit multiplier la base.',5:'Par la propriété des diagonales, O partage [AC] en deux segments égaux et partage aussi [BD] en deux segments égaux.'}
        avant=avant.replace('[IMAGE_1]','On note $b=AB$ et $h$ la hauteur donnée. Le schéma de principe n’est pas à l’échelle.\n\n[IMAGE_1]')
    elif num==277:
        avant=avant.replace('[IMAGE_1]','Schéma de principe : les lettres renvoient aux dimensions données dans le texte.\n\n[IMAGE_1]')
        if 'Un aquarium' in avant:
            L,l,h=map(int,re.search(r'de (\d+) dm de longueur, (\d+) dm de largeur et (\d+) dm',avant).groups()); V=L*l*h
            additions={1:'On compte 2 bases et 4 faces latérales. Les deux bases portent 4 sommets chacune ; les arêtes se répartissent en 4 en bas, 4 en haut et 4 entre les bases.',4:f'Le volume vaut {V} dm³. Comme 1 dm³ = 1 L, on obtient la même valeur numérique en litres.',5:f'La hauteur d’eau vaut les trois quarts de {h} dm. La base ne change pas : le volume d’eau vaut donc les trois quarts du volume intérieur.'}
        elif 'cylindrique a un rayon' in avant:
            r,h=map(int,re.search(r'de (\d+) cm et une hauteur intérieure de (\d+) cm',avant).groups()); V=r*r*h
            additions={1:rf'$$d=2\times r=2\times{r}={2*r}\,\mathrm{{cm}}.$$',2:rf'$$P=2\pi r=2\times\pi\times{r}={2*r}\pi\,\mathrm{{cm}}.$$',5:rf'$$\begin{{aligned}}V&={V}\pi\,\mathrm{{cm}}^3\\&={V}\pi\,\mathrm{{mL}}\\&=\frac{{{V}\pi}}{{1\,000}}\,\mathrm L.\end{{aligned}}$$'+'\nOn utilise ensuite la valeur 3,14 demandée pour π.',6:rf'Le rectangle s’enroule autour de la boîte : sa longueur est le périmètre ${2*r}\pi$ cm ; sa hauteur est ${h}$ cm. Les deux disques ferment les deux extrémités.'}
            avant=avant.replace('avec π','avec $\\pi$').replace('π ≈ 3,14',r'$\pi\approx3{,}14$')
        else:
            L,a,h=map(int,re.search(r'longueur (\d+) cm.*?mesurent (\d+) cm et (\d+) cm',avant).groups()); V=a*h*L//2
            additions={1:'Les deux faces triangulaires identiques et parallèles sont les bases du prisme ; ce sont ici des triangles rectangles.',2:'Chaque triangle a trois côtés : il y a donc trois rectangles latéraux. En ajoutant les deux bases, on compte 3 + 2 = 5 faces.',5:rf'$$1\,\mathrm{{cm}}^3=1\,\mathrm{{mL}}\quad\Rightarrow\quad{V}\,\mathrm{{cm}}^3={V}\,\mathrm{{mL}}.$$',6:rf'$$V_{{\text{{nouveau}}}}=B\times(2\times{L})=2\times(B\times{L})=2\times{V}={2*V}\,\mathrm{{cm}}^3.$$'}
    elif num==278:
        if 'Une classe' in avant:
            a,c,d=map(int,re.search(r'(\d+) réponses « marche », (\d+) réponses « vélo » et (\d+) réponses « bus »',avant).groups()); n=a+c+d
            table=f'| Trajet | Marche | Vélo | Bus |\n|---|---|---|---|\n| Effectif | {a} | {c} | {d} |'
            additions={2:rf'Le plus grand effectif est ${d}$. Sa fréquence vaut $\frac{{{d}}}{{{n}}}=\frac12=50\,\%$.',3:rf'Il y a ${a}$ élèves à pied parmi ${n}$ élèves : la fréquence est $\frac{{{a}}}{{{n}}}$.',4:rf'$$f=\frac{{{a}+{c}}}{{{n}}}=\frac{{{a+c}}}{{{n}}}=\frac12.$$',6:rf'La seconde classe a $2\times{n}={2*n}$ élèves. La moitié prend le bus : ${2*n}\div2={n}$. Dans la première classe, ils sont seulement ${d}$.'}
        else:
            vals=list(map(int,re.search(r'respectivement ([\d, ]+) livres',avant).group(1).split(','))); s=sum(vals); m=s//5
            table='| Élève | 1 | 2 | 3 | 4 | 5 |\n|---|---|---|---|---|---|\n| Livres lus | '+' | '.join(map(str,vals))+' |'
            additions={1:'Les individus interrogés sont les cinq élèves. Pour chacun, on relève un nombre de livres : le caractère est numérique.',2:rf'On compte cinq valeurs. Leur somme est ${"+".join(map(str,vals))}={s}$.',4:r'Pour deux valeurs $1$ et $2$, on obtient $(1+2)\div2=1{,}5$. Cette moyenne n’est égale à aucune des deux valeurs.',6:rf'$$\begin{{aligned}}T_1&=5\times{m}={s},\\T_2&=20\times{m}={20*m}.\end{{aligned}}$$'+'\nLe second groupe a quatre fois plus d’élèves : à moyenne égale, il a lu quatre fois plus de livres.'}
        avant=avant.replace('[IMAGE_1]',table); steps=steps.replace('[IMAGE_2]','')
        chunks=re.split(r'(?=^## Question )',steps,flags=re.M)
    elif num==279:
        avant=avant.replace('1 jeton(s) vert(s)','1 jeton vert')
        if 'Un sac' in avant:
            r,c=map(int,re.search(r'contient (\d+) jetons rouges, (\d+) jetons bleus',avant).groups()); n=r+c+1
            table=f'| Couleur | Rouge | Bleu | Vert |\n|---|---|---|---|\n| Nombre | {r} | {c} | 1 |'
            additions={1:rf'Le total vaut ${r}+{c}+1={n}$. Les effectifs des trois couleurs ne sont pas tous égaux ; elles ne sont donc pas équiprobables.',2:rf'Chaque jeton est équiprobable. Sur les ${n}$ jetons, ${r}$ sont rouges : $P(\text{{rouge}})=\frac{{{r}}}{{{n}}}$.',3:rf'Les cas favorables sont les ${c}$ jetons bleus et le jeton vert : $P(\text{{bleu ou vert}})=\frac{{{c}+1}}{{{n}}}=\frac{{{c+1}}}{{{n}}}$.',5:'Aucun jeton n’est jaune, donc cet événement est impossible. Tous les jetons sont rouges, bleus ou verts : cet événement est certain.',6:rf'Après remise, on retrouve exactement ${r}$ jetons rouges sur ${n}$. La probabilité de rouge reste $\frac{{{r}}}{{{n}}}$ : elle n’est pas nulle.'}
            old=f'{n} jetons. Les couleurs ne sont pas nécessairement équiprobables : leurs effectifs sont à comparer.'
            new=f'{n} jetons. Ici, les couleurs ne sont pas équiprobables : leurs effectifs ne sont pas tous égaux.'
            steps=steps.replace(old,new); solution=solution.replace(old,new)
        else:
            k=int(re.search(r'strictement supérieur à (\d+)',avant).group(1)); favorable=list(range(k+1,7))
            table='| Issues possibles | 1 | 2 | 3 | 4 | 5 | 6 |\n|---|---|---|---|---|---|---|\n| Même probabilité | $\\frac16$ | $\\frac16$ | $\\frac16$ | $\\frac16$ | $\\frac16$ | $\\frac16$ |'
            additions={1:'Le résultat est le numéro de la face supérieure. On énumère les six numéros, sans en oublier ni en répéter.',2:'Le dé est supposé équilibré. Ses six faces ont donc la même chance ; leurs probabilités ont pour somme 1, soit 1 ÷ 6 pour chaque face.',3:f'Le seuil {k} est exclu. On garde les nombres '+', '.join(map(str,favorable))+f', soit {6-k} issue(s).',4:rf'$$P(A)=\frac{{{6-k}}}6.$$',5:rf'Le contraire correspond aux numéros de $1$ à ${k}$, seuil inclus. Il contient ${k}$ issues : $P(\text{{contraire de }}A)=\frac{{{k}}}6$.',6:'La suite 1, 1, 1, 1, 1, 1 reste possible. Elle suffit à montrer que six lancers ne garantissent pas les six faces.'}
        avant=avant.replace('[IMAGE_1]',table); steps=steps.replace('[IMAGE_2]',''); chunks=re.split(r'(?=^## Question )',steps,flags=re.M)
    elif num==280:
        if 'Le programme' in avant:
            a,c=map(int,re.search(r'« (\d+) × réponse \+ (\d+) »',avant).groups()); x=int(re.search(r'pour l’entrée (\d+)',avant).group(1))
            code=f'demander « Choisir un nombre » et attendre\ndire (({a} × réponse) + {c})'
            additions={1:'L’instruction demander reçoit le nombre saisi ; l’instruction dire affiche le calcul effectué à partir de cette donnée.',2:rf'La réponse saisie vaut ${x}$ : remplacer uniquement le bloc réponse donne ${a}\times{x}+{c}$.',6:rf'Pour la même entrée ${x}$, les sorties ${a*x+c}$ et ${a*(x+c)}$ sont différentes. Ce contre-exemple suffit à montrer que les deux formules ne sont pas identiques.'}
            steps=steps.replace('[IMAGE_2]','')
        elif 'répéter 4 fois' in avant:
            a=int(re.search(r'avancer de (\d+) pas',avant).group(1)); code=f'répéter 4 fois :\n    avancer de {a} pas\n    tourner à gauche de 90°'
            additions={1:'Une instruction avancer par répétition et quatre répétitions donnent 1 × 4 = 4 déplacements.',4:'Les quatre segments ont la même longueur. Chaque changement de direction de 90° crée un angle droit ; le quatrième segment ferme la figure.',5:'On avance successivement à droite, vers le haut, à gauche et vers le bas. Les déplacements opposés se compensent ; les quatre rotations reconstituent un tour complet.',6:'Le quatrième segment a déjà ramené le lutin en A. Avant la dernière rotation il est dirigé vers le bas ; supprimer cette seule rotation conserve le tracé et la position, mais change la direction finale.'}
        else:
            a,c=map(int,re.search(r'avancer de (\d+) pas.*?avancer de (\d+) pas',avant).groups()); code=f'répéter 2 fois :\n    avancer de {a} pas\n    tourner à gauche de 90°\n    avancer de {c} pas\n    tourner à gauche de 90°'
            additions={1:'À l’intérieur de la boucle, on lit deux instructions avancer, séparées par des rotations.',2:'Deux déplacements par répétition et deux répétitions donnent 2 × 2 = 4 segments.',3:f'Le premier tour trace {a} puis {c} pas. Le second tour reproduit les mêmes longueurs, dans le même ordre.',4:'Les quatre changements de direction sont des angles droits ; les côtés opposés ont la même longueur. Le tracé fermé est donc un rectangle.',5:rf'$$P=2\times({a}+{c})={2*(a+c)}\text{{ pas}}.$$'+'\nLes directions sont droite, haut, gauche et bas : le lutin revient en A.',6:f'Pour obtenir quatre côtés égaux, remplacer partout le paramètre {c} par {a} (ou remplacer {a} par {c}). Modifier un bloc de la boucle agit lors des deux répétitions.'}
        avant=avant.replace('[IMAGE_1]','Transcription textuelle des blocs :\n```console\n'+code+'\n```')
        chunks=re.split(r'(?=^## Question )',steps,flags=re.M)
    for i,chunk in enumerate(chunks):
        m=re.match(r'## Question (\d+)',chunk)
        if m and '::: etape ' not in chunk:
            n=int(m.group(1)); detail=additions.get(n)
            if detail is None:
                detail=re.search(r'::: methode\n(.*?)\n:::',chunk,re.S).group(1)
            pos=chunk.index('::: resultat')
            chunks[i]=chunk[:pos]+'::: etape Appliquer aux données\n'+detail+'\n:::\n\n'+chunk[pos:]
    return avant+'Étapes:'+''.join(chunks)+'Solution:'+solution

if __name__=='__main__': run()
