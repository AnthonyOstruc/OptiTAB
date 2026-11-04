# -*- coding: utf-8 -*-
"""Révision pédagogique locale : Id conservés, variantes redondantes remplacées."""
from pathlib import Path
from fractions import Fraction
import json
import re

ROOT=Path(__file__).resolve().parent.parent
NEW={}
FIGURES={n:{} for n in range(276,281)}

def question(titre,methode,etapes,resultat):return (titre,methode,etapes,resultat)
def add(num,index,titre,enonce,questions,retenir,images=None,level=None):
    NEW[num,index]={'titre':titre,'enonce':enonce,'questions':questions,'retenir':retenir,'images':images or {},'level':level or ('easy' if index<7 else 'medium' if index<14 else 'hard')}

Q=question
add(276,4,'Diagonales et centre de symétrie',r'''Les diagonales d'un quadrilatère non croisé $ABCD$ se coupent en $O$. On sait que $AO=OC=3\,\mathrm{cm}$ et $BO=OD=2\,\mathrm{cm}$.

1. Que représente $O$ pour chaque diagonale ?
2. Démontrer que $ABCD$ est un parallélogramme.
3. Calculer $AC$ et $BD$.
4. Ce parallélogramme peut-il être un rectangle ?''',[
Q('Identifier les milieux','Utiliser la définition du milieu.', [('Lire les égalités',r'$O$ appartient à $[AC]$ et $AO=OC$ ; il est donc le milieu de $[AC]$. De même, $BO=OD$ montre que $O$ est le milieu de $[BD]$.')],r'$O$ est le milieu des deux diagonales.'),
Q('Reconnaître un parallélogramme','Employer le critère des diagonales.', [('Énoncer le critère','Un quadrilatère dont les diagonales ont le même milieu est un parallélogramme.'),('Vérifier les hypothèses',r'La question 1 montre que les deux milieux sont le même point $O$ ; le critère s’applique à $ABCD$.')],r'$ABCD$ est un parallélogramme.'),
Q('Calculer les diagonales','Additionner les deux moitiés de chaque diagonale.', [('Calculer les longueurs',r'$$\begin{aligned}AC&=AO+OC=3+3=6\,\mathrm{cm},\\BD&=BO+OD=2+2=4\,\mathrm{cm}.\end{aligned}$$')],r'$AC=6\,\mathrm{cm}$ ; $BD=4\,\mathrm{cm}$.'),
Q('Tester le rectangle','Comparer les diagonales du parallélogramme.', [('Utiliser une propriété nécessaire','Les diagonales d’un rectangle ont la même longueur.'),('Comparer',r'Ici $6\ne4$ : cette propriété n’est pas vérifiée.')],r'Non : les diagonales ont des longueurs différentes.')],
'Pour utiliser une réciproque, citer le critère puis vérifier toutes ses hypothèses.')

add(276,6,'Construire le quatrième sommet',r'''Trois points $A$, $B$ et $C$ sont placés dans l'ordre du futur parallélogramme. Le dessin sert de modèle à reproduire ; aucune longueur n'est à mesurer.

[IMAGE_1]

1. Construire $D$ pour que $ABCD$ soit un parallélogramme.
2. Justifier la construction.
3. Tracer les diagonales et placer leur point d'intersection $O$.
4. Décrire une autre construction de $D$ à partir de $O$, milieu de $[AC]$.''',[
Q('Construire le sommet manquant','Tracer deux parallèles.', [('Tracer par deux sommets',r'Tracer par $A$ la parallèle à $(BC)$, puis par $C$ la parallèle à $(AB)$.'),('Placer le point obtenu',r'Leur intersection est $D$. Le sommet et les segments construits sont indiqués en vert.\n\n[IMAGE_2]')],r'$D$ est l’intersection des deux parallèles.'),
Q('Justifier la figure','Vérifier le parallélisme des côtés opposés.', [('Lire la construction',r'On a $(AD)\parallel(BC)$ et $(CD)\parallel(AB)$.'),('Appliquer la définition',r'Les deux paires de côtés opposés sont parallèles : $ABCD$ est un parallélogramme.')],r'La définition du parallélogramme est vérifiée.'),
Q('Placer le centre','Tracer les deux diagonales.', [('Relier les sommets opposés',r'Tracer $[AC]$ et $[BD]$, puis nommer leur intersection $O$.'),('Contrôler la position',r'Les diagonales d’un parallélogramme ont le même milieu : $AO=OC$ et $BO=OD$.\n\n[IMAGE_3]')],r'$O$ est le milieu commun des diagonales.'),
Q('Construire par symétrie','Utiliser le centre de symétrie.', [('Construire le milieu',r'Construire d’abord $O$, milieu de $[AC]$.'),('Reporter la demi-diagonale',r'Sur $(BO)$, placer $D$ de l’autre côté de $O$ avec $OD=OB$. Ainsi $O$ est aussi le milieu de $[BD]$.')],r'$D$ est le symétrique de $B$ par rapport à $O$.')],
'Respecter l’ordre des sommets A, B, C, D : les parallèles se tracent par A et par C.',{1:'construction_depart',2:'construction_fin',3:'construction_diagonales'})

add(276,11,'Choisir une propriété caractéristique',r'''On considère trois quadrilatères non croisés.

| Figure | Informations connues |
|---|---|
| $EFGH$ | $EF=GH$ et $FG=HE$ |
| $IJKL$ | $IJ=KL$ seulement |
| $MNPR$ | $(MN)\parallel(PR)$ et $MN=PR$ |

1. Démontrer que $EFGH$ est un parallélogramme.
2. Peut-on conclure pour $IJKL$ ?
3. Démontrer que $MNPR$ est un parallélogramme.
4. Si les diagonales de $EFGH$ sont en plus perpendiculaires, quelle nature peut-on préciser ?''',[
Q('Étudier EFGH','Repérer les deux paires de côtés opposés.', [('Vérifier les deux égalités',r'$[EF]$ et $[GH]$ sont opposés, de même que $[FG]$ et $[HE]$. Les deux paires ont des longueurs égales.'),('Conclure avec le critère','Un quadrilatère non croisé dont les côtés opposés sont égaux deux à deux est un parallélogramme.')],r'$EFGH$ est un parallélogramme.'),
Q('Étudier IJKL','Distinguer une information utile d’un critère suffisant.', [('Vérifier ce qui manque',r'Une seule paire de côtés opposés égaux est donnée. On ne sait rien sur l’autre paire ni sur le parallélisme.')],r'Non, les données ne permettent pas de conclure.'),
Q('Étudier MNPR','Utiliser un même couple de côtés opposés.', [('Associer parallélisme et égalité',r'Les mêmes côtés $[MN]$ et $[PR]$ sont opposés, parallèles et de même longueur.'),('Appliquer le critère','Cette double propriété suffit pour un quadrilatère non croisé.')],r'$MNPR$ est un parallélogramme.'),
Q('Préciser la nature','Utiliser le parallélogramme déjà démontré.', [('Ajouter l’information nouvelle',r'On sait déjà que $EFGH$ est un parallélogramme. Ses diagonales sont maintenant supposées perpendiculaires.'),('Identifier le cas particulier','Un parallélogramme à diagonales perpendiculaires est un losange.')],r'$EFGH$ est un losange, éventuellement un carré.')],
'Deux côtés égaux ne suffisent pas : vérifier exactement quel critère est disponible.')

add(276,13,'Une parcelle composée de deux figures',r'''La parcelle est formée du parallélogramme $ABCD$ et du triangle $DCE$, sans chevauchement intérieur. On a $AB=DC=6\,\mathrm m$. La hauteur du parallélogramme vaut $2\,\mathrm m$ et la hauteur du triangle relative à $[DC]$ vaut aussi $2\,\mathrm m$.

[IMAGE_1]

1. Calculer l'aire du parallélogramme.
2. Calculer l'aire du triangle.
3. Calculer l'aire totale, puis l'exprimer en $\mathrm{dm}^2$.
4. L'engazonnement coûte $3\,\text{€}$ par $\mathrm m^2$. Calculer le coût total.''',[
Q('Calculer la première aire','Multiplier la base par la hauteur correspondante.', [('Choisir les mesures',r'La base vaut $6\,\mathrm m$ et la hauteur perpendiculaire vaut $2\,\mathrm m$.'),('Multiplier',r'$$\mathcal A_1=6\times2=12\,\mathrm m^2.$$')],r'$12\,\mathrm m^2$.'),
Q('Calculer l’aire du triangle','Diviser le produit base-hauteur par deux.', [('Utiliser la base commune',r'Le triangle a pour base $DC=6\,\mathrm m$ et pour hauteur $2\,\mathrm m$.'),('Calculer',r'$$\mathcal A_2=\frac{6\times2}{2}=6\,\mathrm m^2.$$')],r'$6\,\mathrm m^2$.'),
Q('Assembler et convertir','Additionner les aires puis convertir.', [('Additionner sans chevauchement',r'$$\mathcal A=12+6=18\,\mathrm m^2.$$\n\n[IMAGE_2]'),('Changer d’unité',r'Comme $1\,\mathrm m^2=100\,\mathrm{dm}^2$, on obtient $18\times100=1\,800\,\mathrm{dm}^2$.')],r'$18\,\mathrm m^2=1\,800\,\mathrm{dm}^2$.'),
Q('Calculer le prix','Multiplier la surface par le prix unitaire.', [('Vérifier l’unité du tarif',r'Le tarif est par $\mathrm m^2$ : on utilise donc $18$, et non $1\,800$.'),('Calculer',r'$$18\times3=54\,\text{€}.$$')],r'$54\,\text{€}$.')],
'Le parallélogramme et le triangle ont ici la même base et la même hauteur, mais le triangle a une aire deux fois plus petite.',{1:'parcelle',2:'parcelle_corrige'})

add(276,18,'Même périmètre, surfaces différentes',r'''Deux projets rectangulaires doivent utiliser $24\,\mathrm m$ de bordure. Le projet A mesure $8\,\mathrm m$ sur $4\,\mathrm m$ ; le projet B mesure $6\,\mathrm m$ sur $6\,\mathrm m$.

1. Vérifier le périmètre de chaque projet.
2. Calculer leurs aires et la différence de surface.
3. Le projet B est-il un parallélogramme ? Préciser sa nature.
4. Expliquer pourquoi « même périmètre » n'entraîne pas « même aire ».''',[
Q('Vérifier les bordures','Calculer deux périmètres.', [('Projet A',r'$$P_A=2\times(8+4)=24\,\mathrm m.$$'),('Projet B',r'$$P_B=4\times6=24\,\mathrm m.$$')],r'Les deux projets utilisent $24\,\mathrm m$ de bordure.'),
Q('Comparer les surfaces','Calculer les aires avant de les soustraire.', [('Calculer chaque aire',r'$$\begin{aligned}\mathcal A_A&=8\times4=32\,\mathrm m^2,\\\mathcal A_B&=6\times6=36\,\mathrm m^2.\end{aligned}$$'),('Calculer le gain',r'$$36-32=4\,\mathrm m^2.$$')],r'Le projet B offre $4\,\mathrm m^2$ de plus.'),
Q('Nommer le projet B','Reconnaître un carré.', [('Examiner les côtés et les angles','Le projet B est rectangulaire et ses quatre côtés ont la même longueur : c’est un carré.'),('Relier les familles','Un carré est un rectangle et un losange ; c’est donc aussi un parallélogramme.')],r'Oui : B est un carré, donc un parallélogramme.'),
Q('Interpréter la comparaison','Utiliser les deux projets comme contre-exemple.', [('Comparer deux grandeurs',r'Les périmètres sont égaux à $24\,\mathrm m$, alors que les aires valent $32$ et $36\,\mathrm m^2$.')],r'Une même longueur de contour peut entourer des surfaces différentes.')],
'Le périmètre mesure un contour ; l’aire mesure une surface. Une égalité de l’un ne fixe pas l’autre.')

add(276,20,'Choisir la quantité de dalles',r'''Une terrasse rectangulaire mesure $6\,\mathrm m$ sur $4\,\mathrm m$. Un massif en parallélogramme, de base $3\,\mathrm m$ et de hauteur $2\,\mathrm m$, occupe une partie de la terrasse. Il ne sera pas dallé. Les dalles sont des carrés de côté $50\,\mathrm{cm}$. On prévoit $10\,\%$ de dalles supplémentaires pour les découpes. Chaque dalle coûte $2{,}50\,\text{€}$.

[IMAGE_1]

1. Calculer la surface à daller.
2. Calculer l'aire d'une dalle en $\mathrm m^2$.
3. Calculer le nombre de dalles sans marge, puis le nombre à acheter avec la marge prévue.
4. Calculer le prix des dalles achetées.''',[
Q('Retirer le massif','Soustraire deux aires exprimées dans la même unité.', [('Calculer les deux surfaces',r'$$\begin{aligned}\mathcal A_{\text{terrasse}}&=6\times4=24\,\mathrm m^2,\\\mathcal A_{\text{massif}}&=3\times2=6\,\mathrm m^2.\end{aligned}$$'),('Retirer la partie non dallée',r'$$24-6=18\,\mathrm m^2.$$\n\n[IMAGE_2]')],r'$18\,\mathrm m^2$ à daller.'),
Q('Calculer la surface d’une dalle','Convertir le côté avant de calculer son carré.', [('Convertir une longueur',r'$50\,\mathrm{cm}=0{,}5\,\mathrm m$.'),('Calculer le carré',r'$$\mathcal A_{\text{dalle}}=0{,}5\times0{,}5=0{,}25\,\mathrm m^2.$$')],r'$0{,}25\,\mathrm m^2$ par dalle.'),
Q('Prévoir la quantité','Diviser par l’aire d’une dalle puis prévoir la marge.', [('Calculer sans marge',r'$$18\div0{,}25=72.$$'),('Ajouter la marge et arrondir au-dessus',r'$$\begin{aligned}10\,\%\text{ de }72&=7{,}2,\\72+7{,}2&=79{,}2.\end{aligned}$$\nOn achète des dalles entières : il en faut au moins $80$.')],r'$72$ sans marge ; $80$ dalles à acheter.'),
Q('Calculer le budget','Utiliser le nombre effectivement acheté.', [('Choisir la bonne quantité','Le prix se calcule sur les 80 dalles achetées, y compris la marge.'),('Multiplier',r'$$80\times2{,}50=200\,\text{€}.$$')],r'$200\,\text{€}$.')],
'Un besoin de 79,2 dalles impose d’en acheter 80. Arrondir à l’entier le plus proche peut laisser un manque.',{1:'terrasse',2:'terrasse_corrige'})

# ---------- Solides, patrons, unités et problèmes de capacité ----------
add(277,4,'Relier volumes et capacités',r'''On dispose de trois mesures : $0{,}45\,\mathrm m^3$ ; $2\,500\,\mathrm{cm}^3$ ; $3{,}2\,\mathrm L$.

1. Exprimer $0{,}45\,\mathrm m^3$ en litres.
2. Exprimer $2\,500\,\mathrm{cm}^3$ en mL puis en L.
3. Exprimer $3{,}2\,\mathrm L$ en $\mathrm{dm}^3$ puis en $\mathrm{cm}^3$.
4. Ranger les trois volumes dans l'ordre croissant.''',[
Q('Passer des mètres cubes aux litres','Utiliser le lien entre mètre cube et litre.', [('Choisir le facteur',r'$1\,\mathrm m^3=1\,000\,\mathrm L$.'),('Multiplier',r'$$0{,}45\times1\,000=450\,\mathrm L.$$')],r'$450\,\mathrm L$.'),
Q('Convertir les centimètres cubes','Passer par les millilitres.', [('Relier les unités',r'$1\,\mathrm{cm}^3=1\,\mathrm{mL}$, donc le volume vaut $2\,500\,\mathrm{mL}$.'),('Passer aux litres',r'$$2\,500\div1\,000=2{,}5\,\mathrm L.$$')],r'$2\,500\,\mathrm{mL}=2{,}5\,\mathrm L$.'),
Q('Retrouver des unités de volume','Passer des litres aux décimètres cubes.', [('Première correspondance',r'$3{,}2\,\mathrm L=3{,}2\,\mathrm{dm}^3$.'),('Changer d’unité cube',r'$$3{,}2\times1\,000=3\,200\,\mathrm{cm}^3.$$')],r'$3{,}2\,\mathrm{dm}^3=3\,200\,\mathrm{cm}^3$.'),
Q('Comparer les volumes','Tout exprimer dans la même unité.', [('Comparer en litres',r'$2{,}5\lt3{,}2\lt450$.' )],r'$2\,500\,\mathrm{cm}^3\lt3{,}2\,\mathrm L\lt0{,}45\,\mathrm m^3$.')],
'Un nombre écrit plus grand peut représenter un volume plus petit : comparer après conversion.')

add(277,6,'Reconnaître un patron de cube',r'''Chaque petit carré a un côté de $2\,\mathrm{cm}$. Les assemblages A et B contiennent six carrés.

[IMAGE_1]

1. Le nombre de carrés suffit-il pour reconnaître un patron de cube ?
2. Choisir l'assemblage qui est un patron de cube et expliquer le pliage.
3. Expliquer pourquoi l'autre assemblage ne convient pas.
4. Calculer l'aire totale des faces du cube obtenu.''',[
Q('Compter ne suffit pas','Distinguer nombre de faces et disposition.', [('Identifier la condition nécessaire','Un cube possède six faces carrées : il faut donc six carrés.'),('Identifier la condition supplémentaire','Ces carrés doivent se rejoindre au pliage sans recouvrement des faces.')],r'Non : la disposition des six carrés compte aussi.'),
Q('Choisir le patron','Imaginer le pliage autour d’une face.', [('Fixer la face centrale','Dans A, le carré central peut être la face du dessous ; les quatre carrés voisins deviennent les faces latérales.'),('Fermer le cube','Le sixième carré ferme le dessus. Toutes les faces occupent des positions différentes.\n\n[IMAGE_2]')],r'A est un patron de cube.'),
Q('Écarter l’autre assemblage','Examiner le bloc de quatre carrés.', [('Repérer un sommet commun','Dans B, un point intérieur du quadrillage est commun à quatre carrés.'),('Comparer avec le cube','À chaque sommet d’un cube, seules trois faces se rejoignent. Les quatre carrés ne peuvent donc pas se placer comme quatre faces distinctes sans recouvrement.')],r'B n’est pas un patron de cube.'),
Q('Calculer l’aire totale','Additionner les aires des six carrés.', [('Aire d’une face',r'$$2\times2=4\,\mathrm{cm}^2.$$'),('Aire des six faces',r'$$6\times4=24\,\mathrm{cm}^2.$$')],r'$24\,\mathrm{cm}^2$.')],
'L’aire d’une surface s’exprime en cm² ; le volume du cube, qui n’est pas demandé ici, s’exprimerait en cm³.',{1:'patrons_cube',2:'patron_cube_corrige'})

add(277,11,'Du patron à la surface d’un cylindre',r'''Un cylindre fermé a un rayon de $2\,\mathrm{cm}$ et une hauteur de $5\,\mathrm{cm}$. Pour les approximations, utiliser $\pi\approx3{,}14$.

1. Donner les dimensions du rectangle de son patron.
2. Calculer l'aire de ce rectangle.
3. Calculer l'aire des deux disques, puis l'aire totale de la surface du cylindre.
4. Calculer le volume et expliquer la différence d'unité avec la question 3.''',[
Q('Décrire le rectangle','Dérouler la surface latérale.', [('Trouver sa longueur',r'La longueur est le tour d’une base : $2\pi\times2=4\pi\,\mathrm{cm}$.'),('Conserver la hauteur',r'L’autre dimension est la hauteur du cylindre, soit $5\,\mathrm{cm}$.\n\n[IMAGE_1]')],r'Rectangle de $4\pi\,\mathrm{cm}$ sur $5\,\mathrm{cm}$.'),
Q('Calculer la surface latérale','Calculer l’aire du rectangle du patron.', [('Multiplier les dimensions',r'$$\mathcal A_{\text{latérale}}=4\pi\times5=20\pi\,\mathrm{cm}^2.$$')],r'$20\pi\,\mathrm{cm}^2$.'),
Q('Ajouter les deux bases','Additionner les trois pièces du patron.', [('Calculer les disques',r'$$2\times\pi\times2^2=8\pi\,\mathrm{cm}^2.$$'),('Calculer la surface totale',r'$$\begin{aligned}\mathcal A&=20\pi+8\pi=28\pi\,\mathrm{cm}^2,\\\mathcal A&\approx28\times3{,}14=87{,}92\,\mathrm{cm}^2.\end{aligned}$$')],r'$28\pi\,\mathrm{cm}^2$, soit environ $87{,}92\,\mathrm{cm}^2$.'),
Q('Distinguer surface et volume','Multiplier l’aire d’une base par la hauteur.', [('Calculer l’espace intérieur',r'$$V=\pi\times2^2\times5=20\pi\,\mathrm{cm}^3.$$'),('Interpréter les unités','La surface décrit l’enveloppe en unités carrées ; le volume décrit l’espace intérieur en unités cubes.')],r'$20\pi\,\mathrm{cm}^3$.')],
'Le patron aide à calculer une surface : deux disques et un rectangle. Il ne faut pas ajouter des aires pour trouver un volume.',{1:'patron_cylindre_mesure'})

add(277,13,'Dénombrer un empilement de cubes',r'''Des cubes d'arête $2\,\mathrm{cm}$ sont empilés sur six cases. Le tableau donne le nombre de cubes dans chaque pile ; les piles n'ont aucun trou.

| Rangée | Colonne 1 | Colonne 2 | Colonne 3 |
|---|---|---|---|
| Arrière | $1$ | $2$ | $1$ |
| Avant | $3$ | $1$ | $2$ |

1. Combien de cubes contient l'empilement ?
2. Calculer son volume.
3. Dessiner sa vue de face depuis la rangée « Avant » : donner les hauteurs visibles de gauche à droite.
4. On ajoute un cube sur la pile arrière de la colonne 1. Le volume et la vue de face changent-ils ?''',[
Q('Compter les cubes','Additionner les hauteurs des piles.', [('Compter par rangée',r'Arrière : $1+2+1=4$ ; avant : $3+1+2=6$.'),('Assembler',r'$4+6=10$ cubes.')],r'$10$ cubes.'),
Q('Calculer le volume','Multiplier le nombre de cubes par le volume d’un cube.', [('Volume élémentaire',r'$$V_{\text{cube}}=2^3=8\,\mathrm{cm}^3.$$'),('Volume total',r'$$V=10\times8=80\,\mathrm{cm}^3.$$')],r'$80\,\mathrm{cm}^3$.'),
Q('Construire la vue de face','Garder la pile la plus haute de chaque colonne.', [('Comparer avant et arrière',r'Colonne 1 : $3$ cubes ; colonne 2 : $2$ cubes ; colonne 3 : $2$ cubes.'),('Dessiner la silhouette',r'Chaque carré représente une face de cube.\n\n[IMAGE_1]')],r'Hauteurs : $3$, $2$, $2$ cubes, soit $6$, $4$, $4\,\mathrm{cm}$.'),
Q('Interpréter un cube caché','Distinguer volume et silhouette.', [('Mettre à jour le volume',r'On a $11$ cubes, donc $11\times8=88\,\mathrm{cm}^3$.'),('Vérifier la vue','La pile arrière de la colonne 1 passe de 1 à 2 cubes ; elle reste moins haute que les 3 cubes de devant. La silhouette ne change pas.')],r'Le volume devient $88\,\mathrm{cm}^3$ ; la vue de face reste identique.')],
'Une même vue de face peut correspondre à plusieurs empilements : elle ne révèle pas tous les cubes cachés.',{1:'empilement_face'})

add(277,18,'Remplir un aquarium sans déborder',r'''Les dimensions intérieures d'un aquarium sont $60\,\mathrm{cm}$, $40\,\mathrm{cm}$ et $30\,\mathrm{cm}$ de hauteur. Il est rempli aux trois quarts de sa hauteur.

1. Calculer sa capacité totale en litres.
2. Calculer le volume d'eau initial.
3. On ajoute $12\,\mathrm L$. L'aquarium déborde-t-il ?
4. Calculer la hauteur d'eau après cet ajout.''',[
Q('Calculer la capacité','Calculer le volume puis convertir.', [('Volume intérieur',r'$$V=60\times40\times30=72\,000\,\mathrm{cm}^3.$$'),('Passer aux litres',r'$72\,000\,\mathrm{cm}^3=72\,000\,\mathrm{mL}=72\,\mathrm L$.')],r'$72\,\mathrm L$.'),
Q('Calculer le remplissage initial','La base ne change pas : prendre les trois quarts du volume.', [('Prendre la fraction',r'$$72\times\frac34=54\,\mathrm L.$$')],r'$54\,\mathrm L$.'),
Q('Tester le débordement','Comparer le volume final avec la capacité.', [('Ajouter l’eau',r'$54+12=66\,\mathrm L$.'),('Comparer',r'$66\lt72$ : le volume ajouté tient dans le récipient.')],r'Non : il reste $6\,\mathrm L$ de capacité libre.'),
Q('Retrouver la hauteur','Diviser le volume par l’aire de la base.', [('Mettre les unités en accord',r'$66\,\mathrm L=66\,000\,\mathrm{cm}^3$ et $B=60\times40=2\,400\,\mathrm{cm}^2$.'),('Calculer la hauteur',r'$$h=66\,000\div2\,400=27{,}5\,\mathrm{cm}.$$\nCette hauteur est inférieure à $30\,\mathrm{cm}$, ce qui confirme l’absence de débordement.')],r'$27{,}5\,\mathrm{cm}$.')],
'Pour retrouver une hauteur, diviser un volume par une aire de base, avec des unités compatibles.')

add(277,20,'Adapter une boîte à un produit',r'''Une boîte est un prisme droit de longueur $20\,\mathrm{cm}$. Sa base est un triangle rectangle de côtés $5\,\mathrm{cm}$ et $12\,\mathrm{cm}$ perpendiculaires ; le troisième côté mesure $13\,\mathrm{cm}$. On souhaite y loger un produit de volume $750\,\mathrm{mL}$, en raisonnant uniquement sur le volume disponible.

1. Calculer l'aire de la base et la capacité actuelle de la boîte.
2. Cette capacité suffit-elle ? Quelle longueur minimale faut-il conserver pour les mêmes bases ?
3. Pour cette nouvelle longueur, calculer l'aire totale du carton d'une boîte fermée, sans languettes.
4. Expliquer pourquoi le volume seul ne garantit pas qu'un objet rigide entre dans la boîte.''',[
Q('Calculer la capacité actuelle','Calculer l’aire triangulaire puis le volume du prisme.', [('Aire d’une base',r'$$B=\frac{5\times12}{2}=30\,\mathrm{cm}^2.$$'),('Capacité',r'$$V=30\times20=600\,\mathrm{cm}^3=600\,\mathrm{mL}.$$')],r'$B=30\,\mathrm{cm}^2$ ; capacité $600\,\mathrm{mL}$.'),
Q('Adapter la longueur','Conserver les bases et diviser le volume voulu par leur aire.', [('Comparer les capacités',r'$600\lt750$ : la boîte actuelle est trop petite.'),('Calculer la distance entre bases',r'$$L=750\div30=25\,\mathrm{cm}.$$')],r'Non ; il faut une longueur minimale de $25\,\mathrm{cm}$.'),
Q('Calculer le carton','Additionner les deux triangles et les trois rectangles.', [('Aire des bases',r'$2\times30=60\,\mathrm{cm}^2$.'),('Aire latérale et total',r'$$\begin{aligned}\mathcal A_{\text{latérale}}&=(5+12+13)\times25=750\,\mathrm{cm}^2,\\\mathcal A_{\text{totale}}&=750+60=810\,\mathrm{cm}^2.\end{aligned}$$')],r'$810\,\mathrm{cm}^2$ de carton.'),
Q('Interpréter le modèle','Distinguer capacité et forme.', [('Lire la limite du calcul','Deux objets de même volume peuvent avoir des longueurs et des formes très différentes. Un objet très long peut dépasser malgré un volume assez petit.')],r'Il faut aussi contrôler la forme et les dimensions de l’objet.')],
'Les côtés 5 cm, 12 cm et 13 cm sont donnés : aucun théorème de Pythagore n’est nécessaire.')

# ---------- Données, représentations et moyennes ----------
add(278,4,'Lire les emprunts à la bibliothèque',r'''Le diagramme indique le nombre de livres empruntés chaque jour.

[IMAGE_1]

1. Lire le nombre d'emprunts du mercredi et du vendredi.
2. Quel jour compte le plus d'emprunts ? Calculer l'écart avec le jour qui en compte le moins.
3. Calculer le nombre total d'emprunts de la semaine.
4. Calculer la fréquence des emprunts effectués le mercredi.''',[
Q('Lire deux barres','Lire la hauteur à l’aide de l’échelle.', [('Repérer les jours','Les barres Mer et Ven atteignent respectivement 15 et 6 sur l’axe vertical.\n\n[IMAGE_2]')],r'Mercredi : $15$ ; vendredi : $6$.'),
Q('Comparer les extrêmes','Repérer la barre la plus haute et la plus basse.', [('Lire les extrêmes','Mardi compte 18 emprunts ; vendredi en compte 6.'),('Calculer l’écart',r'$18-6=12$ emprunts.')],r'Mardi ; écart de $12$ emprunts.'),
Q('Calculer le total','Additionner tous les effectifs.', [('Additionner les cinq jours',r'$$12+18+15+9+6=60.$$')],r'$60$ emprunts.'),
Q('Calculer une fréquence','Diviser l’effectif du mercredi par le total.', [('Former la fraction',r'$f=\frac{15}{60}$.'),('Simplifier et convertir',r'$$\frac{15}{60}=\frac14=0{,}25=25\,\%.$$')],r'$25\,\%$.')],
'Lire l’échelle avant les hauteurs : une barre indique un effectif, pas automatiquement un pourcentage.',{1:'bibliotheque',2:'bibliotheque_corrige'})

add(278,6,'Deux séries de même moyenne',r'''Deux groupes de quatre élèves ont lu les nombres de livres suivants :

| Groupe | Élève 1 | Élève 2 | Élève 3 | Élève 4 |
|---|---|---|---|---|
| A | $4$ | $4$ | $8$ | $8$ |
| B | $0$ | $6$ | $6$ | $12$ |

1. Calculer le total des livres pour chaque groupe.
2. Calculer chaque moyenne.
3. Dans quel groupe les nombres de livres sont-ils le plus éloignés les uns des autres ? Justifier avec le minimum et le maximum.
4. La moyenne suffit-elle pour décrire les résultats ?''',[
Q('Calculer les totaux','Additionner les quatre valeurs de chaque groupe.', [('Groupe A',r'$4+4+8+8=24$.'),('Groupe B',r'$0+6+6+12=24$.')],r'$24$ livres dans chaque groupe.'),
Q('Calculer les moyennes','Diviser chaque total par son effectif.', [('Vérifier les effectifs','Les deux groupes ont chacun 4 élèves.'),('Diviser',r'$24\div4=6$ pour chacun.')],r'$6$ livres par élève dans chaque groupe.'),
Q('Comparer les répartitions','Examiner les valeurs les plus éloignées.', [('Groupe A',r'Les valeurs vont de 4 à 8, avec un écart $8-4=4$.'),('Groupe B',r'Elles vont de 0 à 12, avec un écart $12-0=12$.')],r'Le groupe B présente des résultats plus dispersés.'),
Q('Interpréter la moyenne','Confronter une même moyenne à deux répartitions.', [('Relier les résultats','La moyenne vaut 6 dans les deux groupes, mais les minima, maxima et répartitions diffèrent.')],r'Non : une même moyenne peut masquer des répartitions différentes.')],
'Une moyenne décrit un partage égal du total ; elle ne restitue pas toutes les observations.')

add(278,11,'Construire un diagramme circulaire',r'''Une enquête auprès de $40$ élèves donne $10$ trajets à pied, $18$ à vélo et $12$ en bus. Chaque élève donne une seule réponse.

1. Vérifier l'effectif total.
2. Calculer la fréquence de chaque catégorie en pourcentage.
3. Calculer les trois angles d'un diagramme circulaire.
4. Construire le diagramme et vérifier la somme des angles.''',[
Q('Vérifier le total','Additionner les effectifs des catégories.', [('Calculer',r'$10+18+12=40$.')],r'Le total est bien $40$ élèves.'),
Q('Calculer les fréquences','Diviser chaque effectif par 40.', [('Former les quotients',r'$$\begin{aligned}f_{\text{pied}}&=\frac{10}{40}=25\,\%,\\f_{\text{vélo}}&=\frac{18}{40}=45\,\%,\\f_{\text{bus}}&=\frac{12}{40}=30\,\%.\end{aligned}$$'),('Vérifier le partage',r'$25+45+30=100\,\%$.')],r'À pied : $25\,\%$ ; vélo : $45\,\%$ ; bus : $30\,\%$.'),
Q('Déterminer les angles','Multiplier chaque fréquence décimale par 360°.', [('Calculer les secteurs',r'$$\begin{aligned}0{,}25\times360&=90^\circ,\\0{,}45\times360&=162^\circ,\\0{,}30\times360&=108^\circ.\end{aligned}$$')],r'$90^\circ$ ; $162^\circ$ ; $108^\circ$.'),
Q('Tracer le diagramme','Reporter successivement les angles au centre.', [('Construire les secteurs','Tracer un cercle et un rayon, puis reporter au rapporteur 90°, 162° et 108°. Ajouter une légende.\n\n[IMAGE_1]'),('Contrôler',r'$90+162+108=360^\circ$ : le disque est entièrement partagé.')],r'Le diagramme comporte les trois secteurs, de somme $360^\circ$.')],
'Dans un diagramme circulaire, les angles sont proportionnels aux effectifs, et non égaux dès qu’il y a trois catégories.',{1:'transports40'})

add(278,13,'Suivre une température',r'''Le graphique relie cinq relevés de température au cours d'une journée.

[IMAGE_1]

1. Lire la température à $10\,\mathrm h$ et à $14\,\mathrm h$.
2. Donner la plus haute température relevée et son heure.
3. Calculer l'augmentation entre $8\,\mathrm h$ et $12\,\mathrm h$, puis la baisse entre $12\,\mathrm h$ et $16\,\mathrm h$.
4. Calculer la moyenne des cinq relevés. Est-ce automatiquement la température moyenne de toute la journée ?''',[
Q('Lire deux points','Repérer l’heure puis lire l’ordonnée.', [('Lire les hauteurs','À 10 h, le point est à 12 °C ; à 14 h, il est à 14 °C.\n\n[IMAGE_2]')],r'$12\,^\circ\mathrm C$ à 10 h et $14\,^\circ\mathrm C$ à 14 h.'),
Q('Repérer le maximum','Chercher le point le plus haut parmi les relevés.', [('Lire le sommet du graphique','Le point de 12 h atteint 16 °C ; les quatre autres relevés sont inférieurs.')],r'$16\,^\circ\mathrm C$ à 12 h.'),
Q('Calculer les évolutions','Soustraire les températures aux bornes.', [('Augmentation',r'$16-8=8\,^\circ\mathrm C$.'),('Baisse',r'$16-10=6\,^\circ\mathrm C$.')],r'Augmentation de $8\,^\circ\mathrm C$, puis baisse de $6\,^\circ\mathrm C$.'),
Q('Interpréter une moyenne de relevés','Moyenner les cinq valeurs connues seulement.', [('Calculer',r'$$\overline T=\frac{8+12+16+14+10}{5}=\frac{60}{5}=12\,^\circ\mathrm C.$$'),('Délimiter la conclusion','Les cinq relevés ne décrivent pas toutes les températures de la journée ; on ignore notamment les températures de nuit.')],r'Moyenne des cinq relevés : $12\,^\circ\mathrm C$ ; pas forcément celle de toute la journée.')],
'Une moyenne doit toujours être associée à la série effectivement étudiée.',{1:'temperatures',2:'temperatures_corrige'})

add(278,18,'Exploiter des données regroupées',r'''Vingt élèves indiquent leur nombre de livres lus pendant un mois.

| Nombre de livres | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|
| Nombre d'élèves | $2$ | $5$ | $8$ | $5$ |

1. Vérifier l'effectif total et calculer le nombre total de livres lus.
2. Calculer la moyenne par élève.
3. Calculer la fréquence des élèves ayant lu au moins deux livres.
4. Un nouvel élève rejoint le groupe ; il a lu six livres. Calculer la nouvelle moyenne.''',[
Q('Retrouver les totaux','Compter les élèves puis leurs livres.', [('Effectif',r'$2+5+8+5=20$ élèves.'),('Somme des valeurs',r'$$0\times2+1\times5+2\times8+3\times5=36\text{ livres}.$$')],r'$20$ élèves ; $36$ livres.'),
Q('Calculer la moyenne','Diviser les livres par les élèves.', [('Choisir le bon dénominateur','Les quatre colonnes ne représentent pas quatre élèves : elles regroupent vingt élèves.'),('Diviser',r'$36\div20=1{,}8$.')],r'$1{,}8$ livre par élève.'),
Q('Compter au moins deux livres','Regrouper les catégories 2 et 3.', [('Compter les élèves concernés',r'$8+5=13$ élèves.'),('Calculer la proportion',r'$$\frac{13}{20}=0{,}65=65\,\%.$$')],r'$65\,\%$.'),
Q('Mettre à jour la moyenne','Modifier à la fois la somme et l’effectif.', [('Nouveaux totaux',r'$36+6=42$ livres et $20+1=21$ élèves.'),('Nouvelle moyenne',r'$42\div21=2$.')],r'$2$ livres par élève.')],
'Dans un tableau regroupé, répéter chaque valeur autant de fois que son effectif : on ne moyenne pas simplement les intitulés des colonnes.')

add(278,20,'Réunir deux classes',r'''Une classe A de $20$ élèves a une moyenne de $12$ sur $20$ à un devoir. Une classe B de $30$ élèves a une moyenne de $14$ sur $20$.

1. Retrouver la somme des notes dans chaque classe.
2. Calculer la moyenne des $50$ élèves réunis.
3. Pourquoi le calcul $(12+14)\div2$ ne convient-il pas ici ?
4. Un élève supplémentaire, noté sur $20$, peut-il porter à lui seul la moyenne des $51$ élèves à $13{,}5$ ?''',[
Q('Retrouver les sommes','Multiplier chaque moyenne par son effectif.', [('Classe A',r'$12\times20=240$ points.'),('Classe B',r'$14\times30=420$ points.')],r'$240$ points et $420$ points.'),
Q('Réunir les données','Additionner les sommes et les effectifs.', [('Former les totaux',r'$240+420=660$ points et $20+30=50$ élèves.'),('Calculer la moyenne commune',r'$660\div50=13{,}2$.')],r'$13{,}2$ sur $20$.'),
Q('Repérer l’erreur','Vérifier le poids de chaque classe.', [('Comparer les effectifs','La classe B compte 30 élèves et la classe A seulement 20. La moyenne 14 intervient donc pour davantage de notes.'),('Comparer les calculs',r'$(12+14)\div2=13$ ne correspondrait à la moyenne commune que si les effectifs des deux classes étaient égaux.')],r'Les effectifs sont différents : les deux moyennes n’ont pas le même poids.'),
Q('Tester l’objectif','Calculer la somme nécessaire puis la note manquante.', [('Somme visée',r'$13{,}5\times51=688{,}5$ points.'),('Note qu’il faudrait ajouter',r'$688{,}5-660=28{,}5$. Cette note dépasse 20 : elle est impossible pour un élève noté sur 20.')],r'Non : il faudrait une note de $28{,}5$ sur $20$.')],
'On peut réunir des moyennes en revenant aux sommes et aux effectifs ; la moyenne des moyennes n’est pas une règle générale.')

# ---------- Hasard : expériences, fréquences et comptage ----------
add(279,4,'Distinguer secteurs et lettres',r'''Une roue comporte quatre secteurs de même angle, marqués A, A, B et B. Chaque secteur a la même chance d'être désigné ; l'aiguille ne s'arrête pas sur une séparation.

[IMAGE_1]

1. Si l'on distingue les quatre secteurs, combien y a-t-il d'issues équiprobables ?
2. Calculer la probabilité d'obtenir la lettre A.
3. Calculer la probabilité d'obtenir la lettre B. Les deux lettres sont-elles équiprobables ?
4. Donner un événement impossible et un événement certain.''',[
Q('Décrire les issues élémentaires','Compter les secteurs individuels.', [('Distinguer les objets','Même si deux secteurs portent la même lettre, ils occupent des positions différentes. Il y a quatre secteurs égaux.')],r'$4$ issues équiprobables.'),
Q('Compter les A','Diviser le nombre de secteurs favorables par quatre.', [('Repérer les secteurs','Deux secteurs portent A.\n\n[IMAGE_2]'),('Former la fraction',r'$P(A)=\frac24=\frac12$.')],r'$P(A)=\frac12$.'),
Q('Comparer les lettres','Compter aussi les secteurs B.', [('Calculer',r'$P(B)=\frac24=\frac12$.'),('Comparer','Les deux lettres ont la même probabilité : elles sont équiprobables ici.')],r'$P(B)=\frac12$ ; oui.'),
Q('Identifier certain et impossible','Comparer avec toutes les lettres présentes.', [('Événement impossible','Obtenir C ne correspond à aucun secteur.'),('Événement certain','Obtenir A ou B rassemble tous les secteurs.')],r'Impossible : C ; certain : A ou B.')],
'L’équiprobabilité des lettres dépend du nombre de secteurs favorables, pas seulement du nombre de lettres différentes.',{1:'roue_aabb',2:'roue_aabb_corrige'})

add(279,6,'Observer vingt lancers de pièce',r'''Une pièce supposée équilibrée a été lancée vingt fois : on a observé $12$ piles et $8$ faces.

1. Calculer la fréquence observée de pile.
2. Donner la probabilité de pile dans le modèle d'une pièce équilibrée.
3. La différence entre les deux nombres prouve-t-elle que la pièce est truquée ?
4. Est-on certain d'obtenir face au lancer suivant ?''',[
Q('Calculer une fréquence','Diviser le nombre de piles par le nombre d’essais.', [('Former le quotient',r'$f=\frac{12}{20}$.'),('Écrire un pourcentage',r'$\frac{12}{20}=0{,}6=60\,\%$.')],r'$60\,\%$.'),
Q('Donner la probabilité théorique','Utiliser l’hypothèse de pièce équilibrée.', [('Compter les deux issues','Pile et face ont la même chance dans ce modèle.'),('Attribuer les probabilités',r'$P(\text{pile})=\frac12=50\,\%$.')],r'$50\,\%$.'),
Q('Interpréter un écart','Distinguer observation et modèle.', [('Comparer',r'$60\,\%$ est différent de $50\,\%$.'),('Éviter une conclusion abusive','Sur une série courte, le hasard peut donner davantage de piles que de faces. Cet écart seul ne prouve pas une tricherie.')],r'Non, cet écart ne suffit pas à prouver que la pièce est truquée.'),
Q('Prévoir le prochain lancer','Le hasard ne doit pas compenser le passé.', [('Revenir au modèle',r'La pièce reste supposée équilibrée : au prochain lancer, pile et face ont chacun une probabilité $\frac12$.')],r'Non : pile reste possible.')],
'Une fréquence décrit une série réalisée ; une probabilité décrit les chances dans le modèle.')

add(279,11,'Comparer une expérience au modèle',r'''Un sac contient deux jetons rouges, un bleu et un vert, tous indiscernables au toucher. Un tirage est suivi d'une remise et d'un mélange. Après $100$ tirages :

| Couleur | Rouge | Bleu | Vert |
|---|---|---|---|
| Tirages observés | $48$ | $32$ | $20$ |

1. Calculer les trois probabilités théoriques.
2. Calculer les trois fréquences observées.
3. Quelle couleur est la plus fréquente ? Est-ce cohérent avec le modèle ?
4. Pourquoi la remise et le mélange sont-ils nécessaires pour répéter la même expérience ?''',[
Q('Décrire le modèle','Compter les jetons équiprobables.', [('Former les probabilités',r'$P(R)=\frac24=\frac12$ ; $P(B)=\frac14$ ; $P(V)=\frac14$.'),('Vérifier leur somme',r'$\frac12+\frac14+\frac14=1$.')],r'Rouge : $\frac12$ ; bleu : $\frac14$ ; vert : $\frac14$.'),
Q('Décrire les résultats','Diviser chaque effectif observé par 100.', [('Calculer',r'$f_R=48\,\%$ ; $f_B=32\,\%$ ; $f_V=20\,\%$.'),('Vérifier le total',r'$48+32+20=100\,\%$.')],r'$48\,\%$, $32\,\%$, $20\,\%$.'),
Q('Comparer sans confondre','Comparer les maxima puis les valeurs.', [('Repérer le maximum','Rouge a le plus grand effectif observé : 48.'),('Relier au modèle',r'Rouge est aussi la couleur de plus grande probabilité ($50\,\%$). Les fréquences ne sont cependant pas exactement les probabilités.')],r'Rouge ; le classement est cohérent avec le modèle.'),
Q('Rétablir les conditions','Retrouver le même contenu à chaque tirage.', [('Remettre le jeton','Sans remise, le nombre et les couleurs des jetons disponibles changeraient.'),('Mélanger','Le mélange évite de garder un jeton repérable à une position privilégiée.')],r'On rétablit le même sac et les mêmes chances de tirage.')],
'Deux couleurs de même probabilité peuvent avoir des fréquences différentes dans une expérience finie.')

add(279,13,'Compter sans compter deux fois',r'''Dix cartes identiques au toucher sont numérotées de $1$ à $10$. On mélange et on tire une carte. L'événement A est « obtenir un multiple de 3 » ; B est « obtenir un nombre inférieur ou égal à 4 ».

1. Lister les issues de A et calculer sa probabilité.
2. Lister les issues de B et calculer sa probabilité.
3. Lister les issues de « A ou B » et calculer sa probabilité.
4. Lister les issues contraires à « A ou B » et calculer leur probabilité.''',[
Q('Étudier A','Lister les multiples de 3 entre 1 et 10.', [('Énumérer','Les issues favorables sont 3, 6 et 9.'),('Calculer',r'$P(A)=\frac3{10}$.')],r'A : $3$, $6$, $9$ ; probabilité $\frac3{10}$.'),
Q('Étudier B','Inclure la valeur 4.', [('Énumérer','Les issues favorables sont 1, 2, 3 et 4.'),('Calculer',r'$P(B)=\frac4{10}$.')],r'B : $1$, $2$, $3$, $4$ ; probabilité $\frac4{10}$.'),
Q('Réunir les issues','Garder chaque numéro une seule fois.', [('Construire la liste','La carte 3 réalise A et B, mais elle reste une seule carte. La liste est 1, 2, 3, 4, 6, 9.'),('Calculer',r'$P(A\text{ ou }B)=\frac6{10}=\frac35$.')],r'$1$, $2$, $3$, $4$, $6$, $9$ ; probabilité $\frac35$.'),
Q('Décrire le contraire','Garder les numéros absents de la liste précédente.', [('Énumérer','Il reste 5, 7, 8 et 10.'),('Calculer et vérifier',r'$\frac4{10}=\frac25$ et $\frac35+\frac25=1$.')],r'$5$, $7$, $8$, $10$ ; probabilité $\frac25$.')],
'Pour « A ou B », une issue qui réalise les deux événements n’est comptée qu’une seule fois.')

add(279,18,'Modifier un jeu de jetons',r'''Un sac contient six jetons rouges, quatre bleus et deux verts, tous équiprobables au tirage. On tire un seul jeton, sans regarder.

1. Calculer la probabilité initiale de rouge.
2. On ajoute trois jetons verts. Calculer la nouvelle probabilité de rouge.
3. Comparer les chances de rouge avant et après l'ajout.
4. À partir du sac modifié, combien de jetons rouges faut-il ajouter pour que rouge retrouve une chance sur deux ? Justifier sans essais au hasard.''',[
Q('Calculer la probabilité initiale','Compter les jetons du sac initial.', [('Total',r'$6+4+2=12$ jetons.'),('Probabilité',r'$P(R)=\frac6{12}=\frac12$.')],r'$\frac12$.'),
Q('Mettre à jour le sac','Modifier le total, sans changer les rouges.', [('Nouveau total',r'$12+3=15$ jetons, toujours 6 rouges.'),('Nouveau quotient',r'$P(R)=\frac6{15}=\frac25=40\,\%$.')],r'$\frac25=40\,\%$.'),
Q('Comparer les chances','Exprimer les probabilités de la même manière.', [('Comparer',r'La chance passe de $50\,\%$ à $40\,\%$ : elle diminue.')],r'Rouge devient moins probable.'),
Q('Rétablir une chance sur deux','Égaliser rouges et non-rouges.', [('Compter les non-rouges',r'Il y a maintenant $4+(2+3)=9$ jetons non rouges.'),('Compléter les rouges',r'Pour une chance sur deux, il faut 9 rouges aussi. On en ajoute $9-6=3$. On vérifie $\frac9{18}=\frac12$.')],r'Ajouter $3$ jetons rouges.')],
'Quand on ajoute des jetons, le numérateur et le dénominateur peuvent tous deux changer. Compter le nouveau sac avant de calculer.')

add(279,20,'Une roue à secteurs inégaux',r'''Une roue a trois secteurs : rouge de $180^\circ$, bleu de $90^\circ$ et vert de $90^\circ$. La probabilité d'un secteur est proportionnelle à son angle. L'aiguille ne s'arrête pas sur une frontière.

[IMAGE_1]

1. Les trois couleurs sont-elles équiprobables ? Calculer leurs probabilités.
2. Calculer la probabilité d'obtenir bleu ou vert.
3. Sur $80$ tours, on observe $44$ rouges. Calculer la fréquence et la comparer à la probabilité de rouge.
4. Représenter une nouvelle roue de même taille dont les trois couleurs seraient équiprobables : quels angles choisir ?''',[
Q('Comparer les secteurs','Diviser chaque angle par 360°.', [('Calculer les rapports',r'$P(R)=\frac{180}{360}=\frac12$ ; $P(B)=\frac{90}{360}=\frac14$ ; $P(V)=\frac14$.'),('Interpréter','Le secteur rouge est deux fois plus grand que chacun des deux autres : les trois couleurs ne sont pas équiprobables.')],r'Non : rouge $\frac12$, bleu $\frac14$, vert $\frac14$.'),
Q('Regrouper deux couleurs','Additionner les angles des secteurs disjoints.', [('Angle favorable',r'$90+90=180^\circ$.'),('Probabilité',r'$P(B\text{ ou }V)=\frac{180}{360}=\frac12$.')],r'$\frac12$.'),
Q('Comparer expérience et modèle','Calculer la fréquence réalisée.', [('Calculer',r'$f_R=\frac{44}{80}=0{,}55=55\,\%$.'),('Comparer',r'La probabilité de rouge est $50\,\%$, alors que sa fréquence observée vaut $55\,\%$. Cet écart reste possible.')],r'$55\,\%$, différent de la probabilité $50\,\%$.'),
Q('Construire une roue équitable','Partager un tour complet en trois angles égaux.', [('Calculer',r'$360\div3=120^\circ$ par couleur.'),('Tracer et contrôler',r'Les trois secteurs de $120^\circ$ forment un tour complet ; chacun a pour probabilité $\frac13$.\n\n[IMAGE_2]')],r'Trois secteurs de $120^\circ$.')],
'Trois couleurs différentes ne signifient pas trois chances égales : examiner la taille des secteurs.',{1:'roue_inegale',2:'roue_egale'})

# ---------- Lire, corriger et concevoir des programmes ----------
add(280,4,'Déboguer des blocs imbriqués',r'''On veut demander un nombre n puis afficher « quatre fois ce nombre, plus trois ». Le programme erroné est :
```console
demander « n ? » et attendre
dire (4 × (réponse + 3))
```

1. Pour l'entrée 2, calculer la sortie attendue et la sortie du programme erroné.
2. Expliquer l'erreur d'imbrication.
3. Écrire la transcription du programme corrigé.
4. Vérifier le programme corrigé pour l'entrée 0.''',[
Q('Comparer deux sorties','Effectuer les deux calculs en respectant les parenthèses.', [('Sortie voulue',r'$4\times2+3=11$.'),('Sortie du programme',r'$4\times(2+3)=4\times5=20$.')],r'Attendue : $11$ ; obtenue : $20$.'),
Q('Localiser l’erreur','Identifier le calcul intérieur.', [('Lire les blocs','Le programme ajoute 3 à la réponse avant de multiplier le tout par 4.'),('Comparer avec l’objectif','L’objectif demande de multiplier d’abord la réponse par 4, puis d’ajouter seulement 3.')],r'L’addition est placée à l’intérieur de la multiplication.'),
Q('Corriger le programme','Placer la multiplication dans le bloc addition.', [('Écrire les blocs dans l’ordre',r'```console\ndemander « n ? » et attendre\ndire ((4 × réponse) + 3)\n```')],r'Afficher $(4\times\text{réponse})+3$.'),
Q('Tester l’entrée zéro','Remplacer réponse par 0.', [('Calculer',r'$4\times0+3=3$.'),('Contrôler le sens','Le terme multiplié disparaît, mais le 3 ajouté reste présent.')],r'Le programme corrigé affiche $3$.')],
'Un test qui donne deux sorties différentes permet de repérer une erreur, mais il faut encore corriger l’organisation des blocs.')

add(280,6,'Compléter un trajet en rectangle',r'''Le lutin part de $A$, orienté vers la droite, stylo baissé.
```console
avancer de 30 pas
tourner à gauche de 90°
avancer de 20 pas
```

1. Tracer le trajet et nommer $B$ puis $C$ les extrémités des deux déplacements.
2. Donner la distance parcourue et la direction finale.
3. Compléter le programme pour fermer le rectangle et revenir en $A$, orienté comme au départ.
4. Calculer la distance totale de ce programme complété.''',[
Q('Représenter les déplacements','Suivre l’ordre des instructions.', [('Premier segment',r'Tracer $[AB]$ de 30 pas vers la droite.'),('Deuxième segment',r'Tourner à gauche puis tracer $[BC]$ de 20 pas vers le haut.\n\n[IMAGE_1]')],r'Un trajet en deux segments perpendiculaires, de $A$ à $C$.'),
Q('Lire l’état final','Distinguer déplacement et rotation.', [('Distance',r'$30+20=50$ pas.'),('Direction','La seule rotation a placé le lutin vers le haut ; avancer ensuite ne change pas cette direction.')],r'$50$ pas ; direction vers le haut.'),
Q('Fermer le rectangle','Ajouter les deux côtés opposés, puis rétablir la direction.', [('Écrire la suite',r'```console\ntourner à gauche de 90°\navancer de 30 pas\ntourner à gauche de 90°\navancer de 20 pas\ntourner à gauche de 90°\n```'),('Vérifier le tracé',r'Les deux nouveaux déplacements reviennent en $A$. La dernière rotation dirige le lutin vers la droite.\n\n[IMAGE_2]')],r'Le rectangle est fermé ; le lutin retrouve sa position et sa direction initiales.'),
Q('Calculer la longueur totale','Additionner les quatre côtés.', [('Calculer',r'$30+20+30+20=100$ pas.')],r'$100$ pas.')],
'Une rotation seule ne trace aucun segment ; la dernière rotation change l’état final sans modifier le rectangle.',{1:'trajet_l',2:'rectangle_30_20'})

add(280,11,'Réparer une boucle trop courte',r'''Le lutin part de $A$, vers la droite, stylo baissé. Il veut tracer un carré de côté 20 pas, mais exécute :
```console
répéter 3 fois :
    avancer de 20 pas
    tourner à gauche de 90°
```

1. Tracer la figure produite par ce programme.
2. Calculer la distance parcourue et donner la direction finale.
3. Corriger un seul nombre pour obtenir le carré.
4. Avec le programme corrigé, donner la distance parcourue, la position et la direction finales.''',[
Q('Suivre les trois répétitions','Tracer un segment par répétition.', [('Lister les directions','Les déplacements vont vers la droite, vers le haut puis vers la gauche.'),('Dessiner',r'Le quatrième côté n’est pas tracé.\n\n[IMAGE_1]')],r'Trois côtés d’un carré, sans fermeture.'),
Q('Décrire l’état après trois tours','Compter les déplacements et les rotations séparément.', [('Distance',r'$3\times20=60$ pas.'),('Direction','Les trois rotations successives donnent haut, gauche, puis bas ; le lutin termine donc orienté vers le bas.')],r'$60$ pas ; direction vers le bas.'),
Q('Corriger le nombre de répétitions','Associer une répétition à chaque côté.', [('Choisir le nombre','Il faut quatre côtés : remplacer 3 par 4 dans le bloc répéter.'),('Vérifier la fermeture',r'Le quatrième déplacement descend de 20 pas jusqu’à $A$.\n\n[IMAGE_2]')],r'Répéter $4$ fois.'),
Q('Contrôler le programme réparé','Compter quatre segments et quatre quarts de tour.', [('Distance',r'$4\times20=80$ pas.'),('État final','Le déplacement ramène en A ; la quatrième rotation ramène la direction vers la droite.')],r'$80$ pas ; en $A$, dirigé vers la droite.')],
'Le contenu d’une boucle est répété entièrement : même la rotation du dernier tour est exécutée.',{1:'carre_incomplet',2:'carre_20'})

add(280,13,'Choisir l’angle pour un triangle',r'''Le lutin part vers la droite, stylo baissé. Pour tracer un triangle équilatéral de côté 40 pas, un élève propose :
```console
répéter 3 fois :
    avancer de 40 pas
    tourner à gauche de 60°
```

1. Quelle confusion l'élève fait-il sur l'angle de rotation ?
2. Calculer l'angle correct du bloc tourner.
3. Écrire le programme corrigé et représenter son tracé.
4. Donner la distance et la rotation totale du programme corrigé.''',[
Q('Identifier la confusion','Distinguer angle intérieur et changement de direction.', [('Lire la mesure 60°','Un triangle équilatéral a des angles intérieurs de 60°.'),('Lire le bloc tourner','Le bloc ne mesure pas l’angle intérieur : il mesure le changement de direction par rapport au déplacement précédent.')],r'L’élève a utilisé l’angle intérieur au lieu de la rotation extérieure.'),
Q('Calculer la rotation','Compléter un angle plat.', [('Utiliser les deux angles',r'$180^\circ-60^\circ=120^\circ$.'),('Vérifier sur un tour',r'$3\times120^\circ=360^\circ$.')],r'Tourner à gauche de $120^\circ$.'),
Q('Tracer le triangle','Répéter trois segments égaux avec la bonne rotation.', [('Corriger les blocs',r'```console\nrépéter 3 fois :\n    avancer de 40 pas\n    tourner à gauche de 120°\n```'),('Lire le résultat',r'Le troisième segment rejoint le départ.\n\n[IMAGE_1]')],r'Un triangle équilatéral de côté 40 pas.'),
Q('Contrôler les totaux','Compter les trois répétitions.', [('Longueur',r'$3\times40=120$ pas.'),('Rotation',r'$3\times120=360^\circ$.')],r'$120$ pas ; $360^\circ$ de rotation au total.')],
'L’angle du bloc tourner est extérieur au polygone ; pour un triangle équilatéral, il vaut 120°, pas 60°.',{1:'triangle_40'})

add(280,18,'Une mauvaise rotation dans le rectangle',r'''Le lutin part de $A$, dirigé vers la droite, stylo baissé. Il exécute :
```console
répéter 2 fois :
    avancer de 50 pas
    tourner à gauche de 90°
    avancer de 20 pas
    tourner à droite de 90°
```

1. Décrire les quatre déplacements et représenter le tracé.
2. Calculer la distance parcourue et décrire la position finale par rapport à $A$.
3. Corriger un seul bloc pour tracer un rectangle.
4. Donner la distance, la position et la direction finales après correction.''',[
Q('Dérouler les deux tours','Après chaque tour, déterminer la nouvelle direction.', [('Premier tour','Le lutin avance de 50 pas à droite puis de 20 pas vers le haut. La rotation à droite le remet vers la droite.'),('Second tour',r'Il recommence les mêmes déplacements : 50 pas à droite puis 20 pas vers le haut.\n\n[IMAGE_1]')],r'Droite 50, haut 20, droite 50, haut 20 : un escalier.'),
Q('Distinguer longueur et position','Additionner les segments puis regrouper leurs directions.', [('Longueur du trajet',r'$50+20+50+20=140$ pas.'),('Position par rapport au départ',r'Le décalage est $50+50=100$ pas vers la droite et $20+20=40$ pas vers le haut.')],r'$140$ pas ; 100 pas à droite et 40 pas au-dessus de $A$.'),
Q('Réparer la rotation','Faire tourner dans le même sens à chaque angle.', [('Modifier un seul bloc','Remplacer la dernière instruction par tourner à gauche de 90°. Le second tour partira alors vers la gauche.'),('Vérifier le rectangle',r'Les déplacements deviennent droite, haut, gauche, bas.\n\n[IMAGE_2]')],r'Remplacer le dernier « droite » par « gauche ».'),
Q('Contrôler le résultat réparé','La longueur des segments ne change pas.', [('Distance',r'$2\times(50+20)=140$ pas.'),('Position et direction','Les déplacements opposés se compensent et les quatre rotations de 90° forment un tour complet.')],r'$140$ pas ; retour en $A$, dirigé vers la droite.')],
'Un programme peut parcourir la bonne distance sans tracer la bonne figure : contrôler aussi les rotations et la fermeture.',{1:'escalier',2:'rectangle_50_20'})

add(280,20,'Programmer un projet de clôture',r'''Un programme demande une longueur $L$ puis une largeur $\ell$, en mètres. Il doit annoncer la longueur de clôture d'un rectangle. Les deux données restent inchangées pendant le calcul. Un élève propose d'afficher $L\times\ell$. On teste avec $L=8$ et $\ell=5$.

1. Expliquer ce que calcule la formule proposée et pourquoi elle ne répond pas au problème.
2. Écrire la formule correcte puis calculer la sortie pour les données du test.
3. Une clôture coûte $3\,\text{€}$ par mètre. Le budget de $90\,\text{€}$ suffit-il ?
4. Un robot trace le rectangle. Écrire une boucle répétée deux fois et préciser son état final s'il part vers la droite.''',[
Q('Identifier la grandeur affichée','Associer la formule à sa signification.', [('Calcul proposé',r'$8\times5=40$ correspond à l’aire du rectangle, en $\mathrm m^2$.'),('Lire l’objectif','La clôture longe les quatre côtés : on cherche une longueur, pas une surface.')],r'La formule calcule l’aire ; elle ne donne pas la longueur de clôture.'),
Q('Corriger la sortie','Additionner deux longueurs et deux largeurs.', [('Former la formule',r'$P=2\times(L+\ell)$.'),('Calculer',r'$$\begin{aligned}P&=2\times(8+5)\\&=2\times13=26\,\mathrm m.\end{aligned}$$')],r'$26\,\mathrm m$.'),
Q('Tester le budget','Multiplier le périmètre par le prix au mètre.', [('Coût',r'$26\times3=78\,\text{€}$.'),('Comparer',r'$78\lt90$ ; il reste $90-78=12\,\text{€}$.')],r'Oui : coût de $78\,\text{€}$, reste $12\,\text{€}$.'),
Q('Écrire une boucle de tracé','Répéter une longueur, une largeur et deux quarts de tour.', [('Écrire les blocs',r'```console\nrépéter 2 fois :\n    avancer de L\n    tourner à gauche de 90°\n    avancer de largeur\n    tourner à gauche de 90°\n```'),('Contrôler la figure et l’état',r'Pour le test, les déplacements valent 8, 5, 8 et 5 mètres. Le robot revient au départ et retrouve la direction vers la droite.\n\n[IMAGE_1]')],r'Deux tours de boucle ; rectangle fermé, position et direction initiales retrouvées.')],
'Tester les unités de la sortie aide à détecter une erreur de formule : des m² ne peuvent pas représenter une longueur de clôture.',{1:'rectangle_8_5'})

def render(num,index,eid,ex):
    level=ex['level'];kind={'easy':'Découverte','medium':'Entraînement','hard':'Problème'}[level]
    titre=f"{kind} - {TITRES[num]} - {ex['titre']}"
    def linebreaks(s):return s.replace(r'\ne','\x00NE').replace(r'\n','\n').replace('\x00NE',r'\ne')
    enonce=linebreaks(ex['enonce'])
    out=f'=== {titre}\nId: {eid}\nDifficulté: {level}\n\nÉnoncé:\n<!-- optitab:1 -->\n{enonce}\n\nÉtapes:\n<!-- optitab:1 -->\n'
    solutions=[]
    for n,(titre,methode,etapes,resultat) in enumerate(ex['questions'],1):
        out+=f'\n## Question {n} : {titre}\n\n::: methode\n{methode}\n:::\n'
        for title,body in etapes:
            body=body.replace(r'25+45+30=100\,\%',r'25\,\%+45\,\%+30\,\%=100\,\%').replace(r'48+32+20=100\,\%',r'48\,\%+32\,\%+20\,\%=100\,\%')
            out+=f'\n::: etape {title}\n{linebreaks(body)}\n:::\n'
        out+=f'\n::: resultat\n{resultat}\n:::\n'
        solutions.append(f'{n}. {resultat}')
    out+='\n::: retenir\n'+ex['retenir']+'\n:::\n\nSolution:\n<!-- optitab:1 -->\n'+'\n'.join(solutions)+'\n'
    return out

TITRES={276:'Parallélogrammes et aires',277:'Solides, disques et volumes',278:'Organiser et interpréter des données',279:'Hasard et probabilités',280:'Penser et programmer par blocs'}

def fraction(n,d):
    f=Fraction(n,d)
    return str(f.numerator) if f.denominator==1 else rf'\frac{{{f.numerator}}}{{{f.denominator}}}'

def trajet_unique(a,c,d):
    n=a+c+d
    return {'titre':f'Trajets : répartition {a}, {c} et {d}','level':'easy','images':{},
      'enonce':f'''Une classe a demandé à chaque élève son mode principal de trajet. On obtient {a} réponses « marche », {c} réponses « vélo » et {d} réponses « bus ». Chaque élève donne une seule réponse.

| Trajet | Marche | Vélo | Bus |
|---|---|---|---|
| Effectif | {a} | {c} | {d} |

1. Calculer l'effectif total.
2. Déterminer le mode le plus fréquent et sa fréquence.
3. Donner la fréquence des élèves venant à pied.
4. Quelle fraction des élèves vient à pied ou à vélo ?
5. Quel angle représente le bus dans un diagramme circulaire ?
6. Une autre classe compte deux fois plus d'élèves et 50 % de réponses « bus ». Combien de ses élèves prennent le bus ? Comparer avec la première classe.''',
      'questions':[
        Q('Calculer le total','Additionner les trois effectifs.',[('Additionner',rf'${a}+{c}+{d}={n}$.')],f'{n} élèves.'),
        Q('Trouver le mode le plus fréquent','Comparer les effectifs puis calculer une fréquence.',[('Comparer',f'Le bus compte {d} élèves, plus que {a} à pied et {c} à vélo.'),('Former le quotient',rf'$f_{{\text{{bus}}}}=\frac{{{d}}}{{{n}}}={fraction(d,n)}=50\,\%$.')],r'Le bus : $50\,\%$.'),
        Q('Calculer la fréquence de marche','Diviser l’effectif de marche par le total.',[('Former la fraction',rf'$f_{{\text{{marche}}}}=\frac{{{a}}}{{{n}}}={fraction(a,n)}$.')],rf'${fraction(a,n)}$.'),
        Q('Regrouper marche et vélo','Additionner les effectifs de catégories disjointes.',[('Regrouper',rf'${a}+{c}={a+c}$ élèves.'),('Diviser',rf'$\frac{{{a+c}}}{{{n}}}={fraction(a+c,n)}$.')],rf'${fraction(a+c,n)}$, soit $50\,\%$.'),
        Q('Passer de la fréquence à l’angle','Multiplier la fréquence par un tour complet.',[('Calculer',r'$\frac12\times360^\circ=180^\circ$.')],r'$180^\circ$.'),
        Q('Comparer les deux classes','Retrouver un effectif à partir du total et de la proportion.',[('Effectif de l’autre classe',rf'$2\times{n}={2*n}$ élèves.'),('Nombre d’élèves en bus',rf'La moitié de ${2*n}$ vaut ${n}$. La première classe en compte seulement ${d}$.')],f'{n} élèves prennent le bus, contre {d} dans la première classe.')],
      'retenir':'Une même fréquence ne donne pas le même nombre de personnes quand les effectifs totaux diffèrent.'}

DICE={3088:('un nombre pair',[2,4,6]),3091:('un nombre impair',[1,3,5]),3095:('un nombre inférieur ou égal à 2',[1,2]),3098:('un multiple de 3',[3,6]),3102:('1 ou 6',[1,6]),3093:('un diviseur de 6',[1,2,3,6]),3100:('un nombre strictement compris entre 2 et 6',[3,4,5])}
def de_unique(eid):
    label,fav=DICE[eid];other=sorted(set(range(1,7))-set(fav));list_f=', '.join(map(str,fav));list_c=', '.join(map(str,other));p=fraction(len(fav),6);pc=fraction(len(other),6)
    return {'titre':'Un dé équilibré : '+label,'level':'easy','images':{},
      'enonce':f'''On lance un dé équilibré à six faces numérotées de 1 à 6. L'événement A est « obtenir {label} ».

1. Lister toutes les issues possibles.
2. Justifier l'équiprobabilité et donner la probabilité d'une face.
3. Lister les issues favorables à A.
4. Calculer la probabilité de A.
5. Décrire l'événement contraire et calculer sa probabilité.
6. Six lancers garantissent-ils que chaque numéro apparaîtra une fois ?''',
      'questions':[
        Q('Lister les issues','Énumérer les numéros des six faces.',[('Énumérer','Les six numéros sont 1, 2, 3, 4, 5 et 6.')],'1, 2, 3, 4, 5 et 6.'),
        Q('Justifier l’équiprobabilité','Utiliser l’hypothèse de dé équilibré.',[('Lire l’hypothèse','Équilibré signifie ici que les six faces ont la même chance.'),('Répartir la probabilité totale',r'Les six probabilités égales ont pour somme 1 : chacune vaut $\frac16$.')],r'Chaque issue a une probabilité de $\frac16$.'),
        Q('Sélectionner les issues favorables','Tester chaque numéro avec la condition de A.',[('Appliquer la condition',f'Parmi les numéros de 1 à 6, ceux qui conviennent sont {list_f}.'),('Compter',f'On compte {len(fav)} issues favorables.')],list_f+'.'),
        Q('Calculer la probabilité','Diviser les cas favorables par les six cas équiprobables.',[('Former et simplifier la fraction',rf'$P(A)=\frac{{{len(fav)}}}6={p}$.')],rf'${p}$.'),
        Q('Étudier l’événement contraire','Garder les numéros qui ne réalisent pas A.',[('Compléter la liste des issues',f'Les numéros restants sont {list_c}.'),('Calculer et vérifier',rf'$P(\text{{contraire de }}A)=\frac{{{len(other)}}}6={pc}$ ; on vérifie ${p}+{pc}=1$.')],f'Obtenir un des numéros {list_c} ; probabilité $'+pc+'$.'),
        Q('Interpréter six lancers','Distinguer une probabilité d’une garantie.',[('Construire un résultat possible','Obtenir six fois le numéro 1 reste possible.'),('Conclure','Les faces peuvent se répéter ; aucune règle n’impose leur apparition une fois chacune.')],'Non. Des répétitions et des absences restent possibles.')],
      'retenir':'L’équiprobabilité décrit les chances à chaque lancer ; elle ne fixe pas la répartition d’une courte série.'}

def write_if_changed(path,content):
    if not path.exists() or path.read_text(encoding='utf8')!=content:path.write_text(content,encoding='utf8')

def main():
    for num in range(276,281):
        p=next(ROOT.glob(f'{num}_*'))
        if not (p/'sauvegardes/revision_2026-10-30').exists():raise RuntimeError('Sauvegarde absente')
        # Toujours partir de la sauvegarde de cette révision : relance sans duplication.
        saved=p/'sauvegardes/revision_2026-10-30'
        text=(saved/'exercices.txt').read_text(encoding='utf8')
        blocks=[b.strip() for b in re.split(r'^===[ \t]*$',text,flags=re.M) if 'Id:' in b]
        corr=json.loads((saved/'figures/correspondance.json').read_text(encoding='utf8'))
        changements=[];output=[]
        doublons=[]
        for index,b in enumerate(blocks):
            eid=re.search(r'^Id: (\d+)',b,re.M).group(1)
            if num==278 and int(eid) in {3069,3076}:
                data=(5,9,14) if eid=='3069' else (9,13,22)
                b=render(num,index,eid,trajet_unique(*data));doublons.append({'id':eid,'correction':'Répartition des trajets distincte ; tableaux, étapes et réponses recalculés.'})
            elif num==279 and int(eid) in DICE:
                b=render(num,index,eid,de_unique(int(eid)));doublons.append({'id':eid,'correction':'Événement distinct : '+DICE[int(eid)][0]})
            elif (num,index) in NEW:
                ex=NEW[num,index];b=render(num,index,eid,ex)
                corr['exercices'].pop(eid,None)
                if ex['images']:
                    corr['exercices'][eid]={str(pos):{'fichier':name+'.png','alt':f"{ex['titre']} : schéma pédagogique de la question ou de sa correction"} for pos,name in ex['images'].items()}
                changements.append({'id':eid,'titre':ex['titre'],'difficulte':ex['level'],'questions':len(ex['questions'])})
            else:
                # Les coefficients plus grands ne créent pas une nouvelle compétence.
                b=re.sub(r'^Difficulté: (?:medium|hard)$','Difficulté: easy',b,flags=re.M)
                first=b.splitlines()[0];family=first.split(' - ')[-1]
                family=re.sub(r'^\d+\.\s*','',family)
                b=b.replace(first,f'=== Découverte - {TITRES[num]} - {index+1}. {family}',1)
                # Titres d'étapes propres à l'opération effectivement réalisée.
                sections=re.split(r'(?=^## Question )',b,flags=re.M)
                for i,section in enumerate(sections):
                    head=section.splitlines()[0].lower() if section else ''
                    names=[('bc et cd','Identifier les côtés opposés'),('ab × ad','Distinguer côté et hauteur'),('ao et oc','Exploiter le milieu commun'),('faces','Dénombrer les éléments du solide'),('trois quarts','Prendre une fraction du volume'),('capacité','Relier volume et capacité'),('cm³','Convertir les unités cubes'),('population','Distinguer population et caractère'),('effectif total','Additionner les effectifs'),('plus fréquent','Repérer le plus grand effectif'),('quelle fraction','Regrouper les catégories disjointes'),('quel angle','Convertir une fréquence en angle'),('autre classe','Relier moyenne, somme et effectif'),('doit-elle','Construire un contre-exemple'),('relation','Relier deux événements contraires'),('impossible','Distinguer certain et impossible'),('après avoir','Rétablir le sac initial'),('toutes les issues','Énumérer les résultats possibles'),('équiprobables','Utiliser l’hypothèse d’équiprobabilité'),('issues favorables','Sélectionner les résultats favorables'),('affirme','Tester une affirmation sur le hasard'),('entrée du programme','Distinguer entrée et sortie'),('calcul est effectué','Remplacer réponse par la donnée'),('prévoir le nombre','Respecter les priorités opératoires'),('saisit 0','Tester la donnée zéro'),('imbrique','Calculer d’abord les parenthèses'),('organisations','Comparer deux sorties pour une même entrée'),('combien de déplacements','Compter les instructions répétées'),('figure obtient','Identifier les côtés et les angles'),('position et','Suivre position et orientation'),('dernière rotation','Distinguer tracé et direction'),('instructions avancer','Compter les instructions de la séquence'),('combien de segments','Multiplier instructions et répétitions'),('longueurs des segments','Dérouler les deux répétitions'),('figure est tracée','Reconnaître le rectangle'),('un seul paramètre','Égaliser les longueurs des côtés'),('périmètre','Additionner les longueurs du contour'),('aire','Calculer la surface demandée'),('volume','Calculer le volume demandé'),('fréquence','Former le rapport effectif sur total'),('moyenne','Diviser la somme par l’effectif'),('diamètre','Doubler le rayon'),('patron','Relier les pièces du patron'),('diagonale','Utiliser les propriétés des diagonales'),('distance','Additionner les déplacements'),('rotation','Compter les changements de direction'),('probabilité','Compter les issues favorables')]
                    names=[('double','Doubler seulement la distance entre bases'),('convertir','Relier volume et capacité'),('combien cette boîte','Identifier les bases du prisme')]+names
                    precise=next((value for key,value in names if key in head),'Identifier les données utiles')
                    section=section.replace('::: etape Calcul détaillé','::: etape '+precise).replace('::: etape Appliquer aux données','::: etape '+precise)
                    sections[i]=section
                b=''.join(sections)
            output.append(b.strip())
        final_text='\n\n===\n\n'.join(output)+'\n\n===\n'
        final_text=final_text.replace('    avancer de largeur','    avancer de ℓ')
        write_if_changed(p/'exercices.txt',final_text)
        write_if_changed(p/'figures/correspondance.json',json.dumps(corr,ensure_ascii=False,indent=2)+'\n')
        write_if_changed(p/'revision_2026-10-30.json',json.dumps({'remplacements':changements,'doublons_corriges':doublons,'ajouts':[],'ids_conserves':True,'reclassement':'Les autres applications paramétriques sont classées Découverte ; les grands nombres ne justifient pas le niveau Problème.'},ensure_ascii=False,indent=2)+'\n')
        (p/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'donnees_espace-revision','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':main()
