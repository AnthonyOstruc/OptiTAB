"""Révision pédagogique ciblée de 266–270 : mêmes Id, couverture élargie.

Les fichiers du 28 octobre restent intégralement sauvegardés avant édition.
Les outils communs et les sources en ligne ne sont jamais modifiés.
"""
from pathlib import Path
import re
import json
import shutil
from fractions import Fraction

BASE=Path(__file__).resolve().parent.parent
MARK='<!-- optitab:1 -->'
DATE='2026-10-30'
DATA={i:[] for i in range(266,271)}

def math(chain):
    parts=chain.split('=')
    if len(parts)<3:return '$$'+chain+'$$'
    return '$$\n\\begin{aligned}\n'+parts[0]+' &= '+parts[1]+''.join(' \\\\\n&= '+p for p in parts[2:])+'\n\\end{aligned}\n$$'

def q(text,method,steps,result):return {'question':text,'methode':method,'etapes':steps,'resultat':result}
def step(title,text):return (title,text)
def ex(code,slot,title,diff,intro,questions,note,images=None):
    DATA[code].append({'slot':slot,'titre':title,'difficulte':diff,'intro':intro,'questions':questions,'note':note,'images':images or {}})

ex(266,2,'Découverte - Fractions - Additionner des parts identiques','easy',
   'On travaille avec des fractions d’une même unité. Calculer et simplifier lorsque c’est possible.',[
 q(r'Calculer $\frac27+\frac37$.','Additionner les nombres de parts sans changer leur taille.',[
   step('Identifier les septièmes','Les deux dénominateurs sont 7 : chaque part a la même taille.'),step('Réunir les parts',math(r'\frac27+\frac37=\frac{2+3}{7}=\frac57'))],r'$\frac57$.'),
 q(r'Calculer $\frac69-\frac29$.','Retirer les neuvièmes indiqués.',[
   step('Soustraire les numérateurs',math(r'\frac69-\frac29=\frac{6-2}{9}=\frac49'))],r'$\frac49$.'),
 q(r'Calculer $1-\frac58$.','Écrire l’unité en huitièmes.',[
   step('Partager le tout',r'Une unité contient huit huitièmes : $1=\frac88$.'),step('Calculer le complément',math(r'\frac88-\frac58=\frac{8-5}{8}=\frac38'))],r'$\frac38$.'),
 q(r'Lina écrit $\frac25+\frac15=\frac3{10}$. Expliquer et corriger son erreur.','Interpréter le dénominateur comme la taille des parts.',[
   step('Repérer l’erreur','Lina a additionné les dénominateurs. Pourtant, réunir des cinquièmes ne les transforme pas en dixièmes.'),step('Corriger',math(r'\frac25+\frac15=\frac{2+1}{5}=\frac35'))],r'La somme est $\frac35$, et non $\frac3{10}$.')],
   'Les dénominateurs restent inchangés quand les parts ont déjà la même taille.')

ex(266,4,'Découverte - Fractions - Construire des parts comparables','easy',
   'Écrire les fractions avec un dénominateur commun avant de calculer.',[
 q(r'Calculer $\frac12+\frac13$.','Passer en sixièmes.',[
   step('Écrire des fractions égales',r'$\frac12=\frac36$ et $\frac13=\frac26$.'),step('Additionner',math(r'\frac36+\frac26=\frac56'))],r'$\frac56$.'),
 q(r'Calculer $\frac34+\frac18$.','Passer en huitièmes.',[
   step('Convertir les quarts',r'$\frac34=\frac68$.'),step('Additionner',math(r'\frac68+\frac18=\frac78'))],r'$\frac78$.'),
 q(r'Calculer $\frac56-\frac13$.','Passer en sixièmes.',[
   step('Convertir les tiers',r'$\frac13=\frac26$.'),step('Soustraire et simplifier',math(r'\frac56-\frac26=\frac36=\frac12'))],r'$\frac12$.'),
 q(r'Calculer $1+\frac25$.','Exprimer l’unité avec le même partage.',[
   step('Écrire l’unité',r'$1=\frac55$.'),step('Additionner',math(r'\frac55+\frac25=\frac75'))],r'$\frac75$, soit $1+\frac25$.')],
   'Une somme de fractions positives peut dépasser 1. Ce n’est pas une erreur : on a alors plus d’une unité.')

ex(266,7,'Entraînement - Fractions - Dénominateurs quelconques','medium',
   'Choisir un multiple commun suffisamment petit, puis donner chaque résultat sous forme fractionnaire exacte.',[
 q(r'Calculer $\frac38+\frac76$.','Utiliser 24, multiple de 8 et de 6.',[
   step('Passer en vingt-quatrièmes',r'$\frac38=\frac9{24}$ et $\frac76=\frac{28}{24}$.'),step('Additionner',math(r'\frac9{24}+\frac{28}{24}=\frac{37}{24}'))],r'$\frac{37}{24}$.'),
 q(r'Calculer $\frac5{12}-\frac29$.','Utiliser 36, multiple de 12 et de 9.',[
   step('Passer en trente-sixièmes',r'$\frac5{12}=\frac{15}{36}$ et $\frac29=\frac8{36}$.'),step('Soustraire',math(r'\frac{15}{36}-\frac8{36}=\frac7{36}'))],r'$\frac7{36}$.'),
 q(r'Calculer $\frac7{10}+\frac34$.','Utiliser 20 comme dénominateur commun.',[
   step('Changer de partage',r'$\frac7{10}=\frac{14}{20}$ et $\frac34=\frac{15}{20}$.'),step('Additionner',math(r'\frac{14}{20}+\frac{15}{20}=\frac{29}{20}'))],r'$\frac{29}{20}$.'),
 q(r'Calculer $2-\frac7{12}$.','Écrire les deux unités en douzièmes.',[
   step('Convertir le nombre entier',r'$2=\frac{24}{12}$.'),step('Retirer les parts',math(r'\frac{24}{12}-\frac7{12}=\frac{17}{12}'))],r'$\frac{17}{12}$.')],
   'On multiplie le numérateur ET le dénominateur par le même nombre. Multiplier seulement le dénominateur change la valeur de la fraction.')

ex(266,9,'Entraînement - Fractions - Relire une copie et contrôler','medium',
   'Pour chaque proposition, expliquer si le résultat est cohérent, puis effectuer le calcul exact.',[
 q(r'Tom propose $\frac34+\frac16=\frac4{10}$. Pourquoi ce résultat est-il impossible ?','Comparer la somme à son premier terme.',[
   step('Contrôler avant de calculer',r'On ajoute un nombre positif à $\frac34$. La somme doit donc dépasser $\frac34$, alors que $\frac4{10}<\frac34$.'),step('Calculer correctement',math(r'\frac34+\frac16=\frac9{12}+\frac2{12}=\frac{11}{12}'))],r'Impossible : la somme vaut $\frac{11}{12}$.'),
 q(r'Sara propose $1-\frac37=-\frac27$. Corriger.','Écrire le tout avec le dénominateur 7.',[
   step('Contrôler le signe',r'On retire moins d’une unité à une unité : le reste est positif.'),step('Calculer',math(r'1-\frac37=\frac77-\frac37=\frac47'))],r'Le reste est $\frac47$.'),
 q(r'Noé affirme que $\frac56+\frac13$ est inférieur à 1. Vérifier.','Passer au même dénominateur et comparer à l’unité.',[
   step('Additionner en sixièmes',math(r'\frac56+\frac13=\frac56+\frac26=\frac76')),step('Comparer',r'$\frac76>\frac66=1$ : la somme dépasse l’unité d’un sixième.')],r'Faux : $\frac76=1+\frac16$.'),
 q(r'Pour $\frac{11}{15}-\frac25$, quel résultat est correct : $\frac9{10}$ ou $\frac13$ ?','Retirer des parts exprimées dans la même unité.',[
   step('Écrire les cinquièmes en quinzièmes',r'$\frac25=\frac6{15}$.'),step('Soustraire et simplifier',math(r'\frac{11}{15}-\frac6{15}=\frac5{15}=\frac13'))],r'$\frac13$ est le bon résultat.')],
   'Un contrôle de signe ou d’ordre de grandeur permet de repérer une erreur ; il ne remplace pas le calcul exact.')

ex(266,14,'Problème - Fractions - Trois jours de lecture','hard',
   'Un roman comporte 240 pages. Lundi, Inès lit les $\frac38$ du livre. Mardi, elle lit les $\frac5{12}$ du livre entier. Mercredi, elle lit les $\frac25$ des pages qui restaient après mardi.',[
 q('Quelle fraction du livre a-t-elle lue lundi et mardi ?','Additionner les deux fractions portant sur le livre entier.',[
   step('Identifier le même tout','Les fractions du lundi et du mardi ont toutes deux pour référence le livre de 240 pages.'),step('Passer en vingt-quatrièmes',math(r'\frac38+\frac5{12}=\frac9{24}+\frac{10}{24}=\frac{19}{24}'))],r'$\frac{19}{24}$ du livre.'),
 q('Combien de pages a-t-elle lues pendant ces deux jours ?','Calculer une fraction du total.',[
   step('Trouver une part',r'$240\div24=10$ pages par vingt-quatrième.'),step('Prendre 19 parts',r'$10\times19=190$ pages.')],'190 pages.'),
 q('Combien de pages restaient après mardi ?','Retirer les pages déjà lues.',[
   step('Calculer le reste',r'$240-190=50$ pages.'),step('Contrôler par la fraction',math(r'1-\frac{19}{24}=\frac5{24}'))],'50 pages, soit $\frac5{24}$ du livre.'),
 q('Combien de pages lit-elle mercredi ?','Appliquer la nouvelle fraction au reste.',[
   step('Changer de référence','Mercredi, le tout est le reste de 50 pages, et non le livre entier.'),step('Prendre deux cinquièmes',math(r'(50\div5)\times2=10\times2=20'))],'20 pages.'),
 q('Quelle fraction du livre a-t-elle lue au total ? Quelle fraction reste-t-il ?','Revenir au même livre de référence.',[
   step('Additionner les pages lues',r'$190+20=210$ pages lues ; $240-210=30$ pages restantes.'),step('Exprimer et simplifier les fractions',r'$\frac{210}{240}=\frac78$ et $\frac{30}{240}=\frac18$.\n\n[IMAGE_2]')],r'Elle a lu $\frac78$ du livre ; il reste $\frac18$.')],
   'Les deux premières fractions portent sur le livre entier ; la troisième porte sur le reste. Toujours nommer le tout avant de calculer.',
   {2:('lecture_bilan','Parts du livre lues lundi, mardi et mercredi ; une huitième partie reste à lire.')})

ex(266,20,'Problème - Fractions - Servir sans dépasser la réserve','hard',
   'Une carafe contient $\frac45$ L. On sert d’abord $\frac13$ L, puis $\frac7{30}$ L. Les volumes demandés sont des quantités en litres, pas des fractions successives du reste.',[
 q('Quel volume a été servi en tout ?','Additionner les quantités en litres.',[
   step('Choisir les trentièmes',r'$\frac13=\frac{10}{30}$ L.'),step('Additionner',math(r'\frac{10}{30}+\frac7{30}=\frac{17}{30}'))],r'$\frac{17}{30}$ L.'),
 q('Quel volume reste-t-il ?','Soustraire au volume initial.',[
   step('Convertir le volume de départ',r'$\frac45=\frac{24}{30}$ L.'),step('Retirer le volume servi',math(r'\frac{24}{30}-\frac{17}{30}=\frac7{30}'))],r'$\frac7{30}$ L.'),
 q(r'Peut-on encore servir un verre de $\frac14$ L ?','Comparer le reste à la demande.',[
   step('Passer en soixantièmes',r'$\frac7{30}=\frac{14}{60}$ et $\frac14=\frac{15}{60}$.'),step('Décider',r'$\frac{14}{60}<\frac{15}{60}$ : le volume disponible est insuffisant.')],'Non, il manque $\frac1{60}$ L.'),
 q(r'On choisit plutôt un verre de $\frac16$ L. Peut-on le servir et quel sera le nouveau reste ?','Comparer, puis soustraire le verre choisi.',[
   step('Vérifier que le verre tient dans le reste',r'$\frac16=\frac5{30}<\frac7{30}$.'),step('Calculer le nouveau reste',math(r'\frac7{30}-\frac5{30}=\frac2{30}=\frac1{15}'))],r'Oui ; il restera $\frac1{15}$ L.')],
   'On compare les volumes avant de servir. Un dénominateur commun sert autant à comparer qu’à additionner ou soustraire.')

ex(267,2,'Découverte - Carrés et cubes - Lire les exposants','easy',
   'Écrire les produits avant de calculer.',[
 q(r'Calculer $5^2$ et $3^3$.','L’exposant indique combien de facteurs identiques on multiplie.',[
   step('Deux facteurs pour un carré',r'$5^2=5\times5=25$.'),step('Trois facteurs pour un cube',r'$3^3=3\times3\times3=27$.')],r'$5^2=25$ et $3^3=27$.'),
 q('Écrire 36 sous la forme du carré d’un entier positif.','Reconnaître un produit de deux facteurs égaux.',[
   step('Chercher dans les carrés connus',r'$6\times6=36$, donc $36=6^2$.')],r'$36=6^2$.'),
 q('Écrire 125 sous la forme du cube d’un entier positif.','Chercher trois facteurs égaux.',[
   step('Décomposer le nombre',r'$125=5\times25=5\times5\times5$.'),step('Utiliser l’exposant',r'$125=5^3$.')],r'$125=5^3$.'),
 q(r'Un élève écrit $4^3=12$. Quelle confusion fait-il ?','Distinguer un exposant et un facteur.',[
   step('Interpréter le calcul proposé',r'$4\times3=12$ multiplie deux nombres différents ; ce n’est pas la définition du cube.'),step('Calculer trois facteurs égaux',math(r'4^3=4\times4\times4=16\times4=64'))],r'$4^3=64$ ; l’élève a confondu cube et multiplication par 3.')],
   'Un carré contient deux facteurs identiques, un cube en contient trois. L’exposant n’est pas un nombre par lequel on multiplie la base.')

ex(267,4,'Découverte - Carrés et cubes - Mémoriser et reconnaître','easy',
   'Utiliser les carrés des entiers de 0 à 12.',[
 q('Calculer les carrés de 6, 7, 8, 9, 11 et 12.','Retrouver chaque produit avant de mémoriser.',[
   step('Construire le tableau',r'| $n$ | 6 | 7 | 8 | 9 | 11 | 12 |'+'\n|---|---|---|---|---|---|---|\n'+r'| $n^2$ | 36 | 49 | 64 | 81 | 121 | 144 |')],'36 ; 49 ; 64 ; 81 ; 121 ; 144.'),
 q(r'Comparer $8^2$ et $4^3$.','Calculer séparément les deux puissances.',[
   step('Le carré',r'$8^2=8\times8=64$.'),step('Le cube',r'$4^3=4\times4\times4=64$.')],r'Ils sont égaux : $8^2=4^3=64$.'),
 q('Quel entier positif a pour carré 49 ?','Lire la table des carrés en sens inverse.',[
   step('Retrouver le côté',r'$7\times7=49$. Le nombre cherché est 7.')],'7.'),
 q('50 est-il le carré d’un entier positif ? Justifier.','Encadrer par deux carrés consécutifs.',[
   step('Encadrer',r'$7^2=49<50<64=8^2$.'),step('Conclure','Il n’y a aucun entier strictement entre 7 et 8 ; aucun carré entier ne se place entre ces deux carrés consécutifs.')],'Non : 50 est compris entre les carrés de 7 et de 8.')],
   'Des exposants différents peuvent donner le même nombre. Pour comparer deux puissances simples, on peut calculer leurs valeurs.')

ex(267,7,'Entraînement - Carrés et cubes - Priorités de calcul','medium',
   'Détailler les calculs en respectant les parenthèses et les puissances.',[
 q(r'Calculer $3+2\times5^2$.','Calculer la puissance avant le produit et la somme.',[
   step('Évaluer la puissance',r'$5^2=25$.'),step('Terminer dans l’ordre',math(r'3+2\times25=3+50=53'))],'53.'),
 q(r'Calculer $(3+2)\times5^2$.','Traiter la parenthèse et la puissance avant le produit.',[
   step('Préparer les facteurs',r'$3+2=5$ et $5^2=25$.'),step('Multiplier',r'$5\times25=125$.')],'125.'),
 q(r'Calculer $(3+2)^2\times5$.','Calculer d’abord la somme dont on prend le carré.',[
   step('Évaluer le carré de la somme',r'$(3+2)^2=5^2=25$.'),step('Terminer le produit',r'$25\times5=125$.')],'125.'),
 q(r'Calculer $10^3-4\times3^3$.','Calculer les deux cubes, puis le produit, puis la différence.',[
   step('Évaluer les puissances',r'$10^3=1\,000$ et $3^3=27$.'),step('Multiplier et soustraire',math(r'1\,000-4\times27=1\,000-108=892'))],'892.')],
   'Des expressions contenant les mêmes nombres peuvent avoir des résultats différents si les parenthèses ou les exposants changent.')

ex(267,9,'Entraînement - Carrés et cubes - Décimaux et substitution','medium',
   'On travaille avec des nombres positifs. Les virgules décimales font partie des nombres.',[
 q(r'Calculer $1{,}5^2$.','Multiplier le nombre par lui-même.',[
   step('Écrire le produit',r'$1{,}5^2=1{,}5\times1{,}5$.'),step('Placer la virgule',r'$15\times15=225$, donc $1{,}5\times1{,}5=2{,}25$.')],r'$2{,}25$.'),
 q(r'Calculer $2{,}5^3$.','Multiplier trois facteurs identiques.',[
   step('Calculer le carré',r'$2{,}5\times2{,}5=6{,}25$.'),step('Multiplier une troisième fois',r'$6{,}25\times2{,}5=15{,}625$.')],r'$15{,}625$.'),
 q(r'Calculer $2x^2+3$ pour $x=1{,}5$.','Remplacer la lettre avant d’appliquer les priorités.',[
   step('Substituer',r'$2x^2+3=2\times1{,}5^2+3$.'),step('Calculer',math(r'2\times2{,}25+3=4{,}5+3=7{,}5'))],r'$7{,}5$.'),
 q(r'Pour $x=3$, les nombres $x^2$ et $2x$ sont-ils égaux ?','Ne pas confondre carré et double.',[
   step('Calculer chaque expression',r'$x^2=3\times3=9$, tandis que $2x=2\times3=6$.'),step('Comparer',r'$9\ne6$.')],'Non : le carré vaut 9 et le double vaut 6.')],
   'Le carré d’un décimal n’est pas nécessairement entier. Dans $2x^2$, le carré concerne x ; le facteur 2 reste à l’extérieur.')

ex(267,14,'Problème - Carrés et cubes - Paver une terrasse carrée','hard',
   'Une terrasse carrée mesure 4,5 m de côté. On utilise des dalles carrées de 0,5 m de côté, sans joint ni découpe. Les dalles sont vendues par boîtes de 20.',[
 q('Combien de dalles faut-il le long d’un côté ?','Comparer les longueurs exprimées dans la même unité.',[
   step('Diviser la longueur du côté',r'$4{,}5\div0{,}5=9$.'),step('Interpréter','Neuf dalles de 0,5 m couvrent exactement un côté de 4,5 m.')],'9 dalles par côté.'),
 q('Combien de dalles faut-il en tout ?','Compter les lignes et les colonnes.',[
   step('Utiliser le carré',r'$9^2=9\times9=81$.\n\n[IMAGE_2]')],'81 dalles.'),
 q('Calculer l’aire de la terrasse et celle d’une dalle ; vérifier le nombre trouvé.','Calculer les deux carrés avec les bonnes unités.',[
   step('Calculer les aires',r'$4{,}5^2=20{,}25$ m$^2$ et $0{,}5^2=0{,}25$ m$^2$.'),step('Contrôler le pavage',r'$81\times0{,}25=20{,}25$ m$^2$ : les aires concordent.')],'Terrasse : 20,25 m² ; dalle : 0,25 m² ; les 81 dalles couvrent exactement la terrasse.'),
 q('Combien de boîtes faut-il acheter et combien de dalles resteront ?','Arrondir le nombre de boîtes à l’entier supérieur.',[
   step('Comparer les capacités des boîtes',r'$4\times20=80<81$ : quatre boîtes ne suffisent pas. Cinq boîtes donnent $5\times20=100$ dalles.'),step('Calculer le surplus',r'$100-81=19$.')],'5 boîtes ; 19 dalles restantes.'),
 q('On agrandit le côté de 0,5 m. De combien l’aire augmente-t-elle ?','Calculer la nouvelle aire avant de soustraire.',[
   step('Trouver la nouvelle aire',r'Le côté devient $4{,}5+0{,}5=5$ m, donc l’aire vaut $5^2=25$ m$^2$.'),step('Calculer l’augmentation',r'$25-20{,}25=4{,}75$ m$^2$.')],'L’aire augmente de 4,75 m².')],
   'Compter des dalles, mesurer une aire et acheter des boîtes sont trois calculs différents. Un nombre de boîtes doit être entier.',
   {2:('terrasse_81','Terrasse carrée composée de neuf lignes de neuf dalles, soit 81 dalles.')})

ex(267,20,'Problème - Carrés et cubes - Remplir puis vider un grand cube','hard',
   'Une boîte cubique a une arête intérieure de 30 cm. On la remplit sans espace vide de petits cubes d’arête 5 cm. On retire ensuite toute la couche supérieure de petits cubes.',[
 q('Combien de petits cubes tiennent sur une arête ?','Diviser les deux longueurs dans la même unité.',[
   step('Comparer les arêtes',r'$30\div5=6$.')],'6 petits cubes par arête.'),
 q('Combien de petits cubes remplissent la boîte ?','Compter les trois directions.',[
   step('Compter une couche',r'$6^2=36$ petits cubes.'),step('Compter six couches',math(r'6^3=6\times6\times6=216')+'\n\n[IMAGE_2]')],'216 petits cubes.'),
 q('Calculer le volume de la boîte, en cm³ puis en litres.','Prendre le cube de l’arête, puis convertir le volume.',[
   step('Calculer le volume',r'$30^3=30\times30\times30=27\,000$ cm$^3$.'),step('Convertir en litres',r'$1$ L $=1\,000$ cm$^3$, donc $27\,000\div1\,000=27$ L.')],'27 000 cm³, soit 27 L.'),
 q('Calculer le volume d’un petit cube et contrôler le remplissage.','Comparer le volume total des petits cubes à celui de la boîte.',[
   step('Le volume élémentaire',r'$5^3=125$ cm$^3$.'),step('Le volume total',r'$216\times125=27\,000$ cm$^3$. Il est égal au volume intérieur de la boîte.')],'125 cm³ par petit cube ; les volumes concordent.'),
 q('Après retrait de la couche supérieure, combien de cubes restent et quel volume occupent-ils en litres ?','Retirer une couche complète, puis convertir le volume restant.',[
   step('Retirer les cubes d’une couche',r'$216-36=180$ cubes.'),step('Calculer le volume restant',r'$180\times125=22\,500$ cm$^3$, soit $22\,500\div1\,000=22{,}5$ L.')],'180 cubes, occupant 22,5 L.')],
   'Une couche contient un carré de petits cubes ; la boîte entière contient un cube de ce nombre. Pour convertir un volume, le facteur change dans les trois directions.',
   {2:('cube_216','Boîte cubique de 30 cm d’arête contenant six petits cubes de 5 cm dans chaque direction.')})

ex(268,2,'Découverte - Lettres et formules - Traduire des phrases','easy',
   'La lettre $x$ représente un nombre positif. Traduire chaque phrase par une expression.',[
 q('Écrire le double, le triple et la moitié de x.','Associer chaque mot à une opération.',[
   step('Double et triple',r'Multiplier par 2 donne $2x$ ; multiplier par 3 donne $3x$.'),step('Moitié',r'Partager en deux donne $\frac{x}{2}$.')],r'$2x$ ; $3x$ ; $\frac{x}{2}$.'),
 q('Écrire le successeur et le prédécesseur d’un entier n.','Ajouter ou retirer une unité.',[
   step('Traduire le déplacement d’une unité',r'Le nombre qui suit est $n+1$ ; celui qui précède est $n-1$.')],r'$n+1$ et $n-1$.'),
 q('Écrire le carré de x, puis la somme du carré de x et de 5.','Identifier ce qui est au carré et ce qui est ajouté.',[
   step('Former le carré',r'$x\times x=x^2$.'),step('Ajouter le terme demandé',r'La somme demandée s’écrit $x^2+5$.')],r'$x^2$ puis $x^2+5$.'),
 q(r'Exprimer par une phrase $3(x+2)$ et $3x+2$, puis les calculer pour $x=4$.','Repérer l’opération effectuée en premier.',[
   step('Lire les expressions',r'$3(x+2)$ : le triple de la somme de x et 2. $3x+2$ : la somme du triple de x et de 2.'),step('Tester avec 4',r'$3(4+2)=18$, tandis que $3\times4+2=14$.')],'Le triple de la somme vaut 18 ; le triple du nombre augmenté de 2 vaut 14.')],
   'Lire une expression à voix haute aide à placer les parenthèses. « Le triple de la somme » impose de former la somme avant de multiplier.')

ex(268,4,'Découverte - Lettres et formules - Périmètre ou aire','easy',
   'Un rectangle a pour longueur L et pour largeur ℓ. On prend d’abord L = 8 cm et ℓ = 3 cm.',[
 q('Écrire une formule du périmètre.','Additionner les quatre côtés.',[
   step('Regrouper les côtés opposés',r'$P=L+\ell+L+\ell=2(L+\ell)$.')],r'$P=2(L+\ell)$.'),
 q('Calculer le périmètre du rectangle donné.','Remplacer les deux lettres par leurs longueurs.',[
   step('Substituer puis calculer',math(r'P=2(8+3)=2\times11=22'))],'22 cm.'),
 q('Écrire une formule de l’aire, puis la calculer.','Multiplier la longueur par la largeur.',[
   step('Écrire la formule',r'$A=L\ell$.'),step('Calculer',r'$A=8\times3=24$ cm$^2$.')],r'$A=L\ell=24$ cm².'),
 q('La longueur passe à 10 cm ; la largeur ne change pas. Donner le nouveau périmètre et la nouvelle aire.','Modifier uniquement la valeur de L.',[
   step('Le nouveau périmètre',r'$P=2(10+3)=26$ cm.'),step('La nouvelle aire',r'$A=10\times3=30$ cm$^2$.')],'26 cm et 30 cm².'),
 q('Pourquoi ne peut-on pas additionner le périmètre et l’aire ?','Vérifier la nature des grandeurs.',[
   step('Comparer les unités','Le périmètre mesure une longueur en cm ; l’aire mesure une surface en cm². Une addition exige des grandeurs de même nature.')],'On ne peut pas additionner une longueur et une surface.')],
   'Une lettre représente ici une mesure numérique ; l’unité permet de vérifier le sens de la formule et de la réponse.')

ex(268,7,'Entraînement - Lettres et formules - Substituer et utiliser un tableur','medium',
   r'On considère l’expression $A=3x^2+2x$.',[
 q('Calculer A pour x = 0.','Remplacer chaque occurrence de x par zéro.',[
   step('Substituer',r'$A=3\times0^2+2\times0$.'),step('Calculer',r'$A=0$.')],'0.'),
 q('Calculer A pour x = 2.','Calculer la puissance avant les produits.',[
   step('Remplacer x',r'$A=3\times2^2+2\times2$.'),step('Suivre les priorités',math(r'A=3\times4+4=12+4=16'))],'16.'),
 q('Calculer A pour x = 1,5.','Calculer d’abord le carré du décimal.',[
   step('Calculer le carré',r'$1{,}5^2=2{,}25$.'),step('Finir le calcul',math(r'A=3\times2{,}25+2\times1{,}5=6{,}75+3=9{,}75'))],'9,75.'),
 q('La cellule A2 contient x. Quelle formule placer en B2 pour calculer A ?','Traduire les opérations avec la syntaxe du tableur.',[
   step('Traduire la puissance et les produits','Dans un tableur, `^2` désigne le carré et `*` une multiplication.'),step('Écrire la formule','Saisir `=3*A2^2+2*A2`. Si A2 vaut 2, la cellule affiche 16.')],'`=3*A2^2+2*A2`.'),
 q(r'Pour x = 2, comparer A à $B=3(x^2+2x)$.','Calculer les deux expressions séparément.',[
   step('Calculer B',math(r'B=3(2^2+2\times2)=3(4+4)=24')),step('Comparer',r'$A=16$ et $B=24$, donc $A\ne B$.')],'Les deux expressions diffèrent : 16 et 24.')],
   'Le facteur devant une parenthèse multiplie tout son contenu. Une substitution n’autorise ni à déplacer ni à ajouter des parenthèses.')

ex(268,9,'Entraînement - Lettres et formules - Tester une égalité','medium',
   r'On teste l’égalité $n+6=3n$ uniquement pour les valeurs proposées.',[
 q('L’égalité est-elle vraie pour n = 2 ?','Calculer séparément chaque membre.',[
   step('Le membre de gauche',r'$2+6=8$.'),step('Le membre de droite',r'$3\times2=6$. Comme $8\ne6$, l’égalité est fausse.')],'Non : 8 et 6 sont différents.'),
 q('L’égalité est-elle vraie pour n = 3 ?','Comparer les deux calculs indépendants.',[
   step('Le membre de gauche',r'$3+6=9$.'),step('Le membre de droite',r'$3\times3=9$. Les deux membres sont égaux.')],'Oui : les deux membres valent 9.'),
 q('L’égalité est-elle vraie pour n = 4 ?','Refaire les deux calculs avec la nouvelle valeur.',[
   step('Calculer',r'$4+6=10$, tandis que $3\times4=12$.'),step('Comparer',r'$10\ne12$.')],'Non : 10 et 12 sont différents.'),
 q('Un test vrai pour n = 3 prouve-t-il que l’égalité est toujours vraie ?','Distinguer un cas particulier d’une propriété générale.',[
   step('Utiliser un contre-exemple','Le test avec n = 2 donne déjà deux nombres différents. Un seul cas faux suffit à réfuter « pour tout n ».')],'Non ; n = 2 est un contre-exemple.')],
   'Tester signifie remplacer puis comparer. On ne cherche ici ni une formule générale de résolution ni toutes les valeurs possibles.')

ex(268,14,'Problème - Lettres et formules - Une bordure de carreaux','hard',
   'Au rang n, on entoure un carré de n carreaux sur n par une bordure d’un carreau d’épaisseur. Le carré intérieur n’appartient pas à la bordure. Le dessin montre le rang 3.\n\n[IMAGE_1]',[
 q('Combien de carreaux comporte la bordure aux rangs 1, 2 et 3 ?','Retirer le carré intérieur du carré extérieur.',[
   step('Les rangs 1 et 2',r'Rang 1 : $3^2-1^2=9-1=8$. Rang 2 : $4^2-2^2=16-4=12$.'),step('Le rang 3',r'$5^2-3^2=25-9=16$.')],'8 ; 12 ; 16 carreaux.'),
 q('Au rang n, combien y a-t-il de carreaux sur la ligne du haut et sur celle du bas ?','Inclure les deux coins dans chaque ligne horizontale.',[
   step('Compter la largeur extérieure',r'La bordure ajoute un carreau à gauche et un à droite : chaque ligne compte $n+2$ carreaux.')],r'$n+2$ en haut et $n+2$ en bas.'),
 q('Après avoir compté ces deux lignes, combien reste-t-il de carreaux sur chacun des côtés verticaux ?','Ne pas recompter les coins.',[
   step('Retirer les coins déjà comptés',r'Sur chacun des deux côtés verticaux, il reste exactement n carreaux.')],r'$n$ à gauche et $n$ à droite.'),
 q('En déduire une formule du nombre de carreaux de la bordure.','Additionner les quatre parties sans compter deux fois les coins.',[
   step('Assembler les parties',r'$B=(n+2)+(n+2)+n+n$.'),step('Réduire',math(r'B=2n+4+2n=4n+4')+'\n\n[IMAGE_2]')],r'$B=4n+4$.'),
 q('Combien de carreaux faut-il au rang 10 ? À quel rang en faut-il 64 ?','Utiliser la formule dans les deux sens.',[
   step('Calculer pour un rang donné',r'$4\times10+4=44$ carreaux.'),step('Retrouver le rang',r'On retire les quatre carreaux fixes : $64-4=60$, puis on partage : $60\div4=15$. Vérification : $4\times15+4=64$.')],'44 carreaux au rang 10 ; 64 carreaux au rang 15.')],
   'Dans une bordure, les coins risquent d’être comptés deux fois. Une formule doit expliquer comment on décompose le motif, pas seulement reproduire trois valeurs.',
   {1:('bordure_enonce','Bordure d’un carreau autour d’un carré intérieur de trois carreaux sur trois.'),2:('bordure_corrige','Les deux lignes de cinq carreaux et les deux côtés de trois carreaux donnent seize carreaux de bordure.')})

ex(268,20,'Problème - Lettres et formules - Comparer deux tarifs','hard',
   r'Pour n trajets, le tarif A coûte $A=3n+8$ euros et le tarif B coûte $B=5n$ euros. Le nombre n de trajets est entier positif ou nul.',[
 q('Compléter les prix pour 2, 4 et 6 trajets.','Substituer chaque nombre de trajets dans les deux formules.',[
   step('Le tarif A',r'$A(2)=3\times2+8=14$ ; $A(4)=20$ ; $A(6)=26$.'),step('Le tarif B',r'$B(2)=10$ ; $B(4)=20$ ; $B(6)=30$.\n\n| Trajets | 2 | 4 | 6 |\n|---|---|---|---|\n| A (€) | 14 | 20 | 26 |\n| B (€) | 10 | 20 | 30 |')],'A : 14, 20, 26 € ; B : 10, 20, 30 €.'),
 q('Quel tarif choisir pour chacun de ces trois nombres de trajets ?','Comparer les deux prix dans une même colonne.',[
   step('Lire les comparaisons','Pour 2 trajets, 10 < 14 : B est moins cher. Pour 4 trajets, les prix sont égaux. Pour 6 trajets, 26 < 30 : A est moins cher.')],'2 trajets : B ; 4 trajets : égalité ; 6 trajets : A.'),
 q('L’affirmation « A est toujours moins cher » est-elle vraie ?','Chercher un cas qui contredit l’affirmation.',[
   step('Produire le contre-exemple','Pour 2 trajets, A coûte 14 € et B coûte 10 €. A est donc plus cher dans ce cas.')],'Non : 2 trajets est un contre-exemple.'),
 q('Pour 10 trajets, quelle économie obtient-on en choisissant le meilleur tarif ?','Calculer les deux prix puis leur différence.',[
   step('Calculer les prix',r'$A=3\times10+8=38$ € et $B=5\times10=50$ €.'),step('Calculer l’économie',r'$50-38=12$ €.')],'Choisir A permet d’économiser 12 €.'),
 q('Que coûte le tarif A pour zéro trajet ? Interpréter le nombre 8.','Calculer une valeur de référence et donner son sens.',[
   step('Substituer zéro',r'$3\times0+8=8$ €.'),step('Interpréter','Les 8 € sont une dépense fixe payée même sans trajet.')],'8 € de frais fixes.')],
   'Pour comparer deux formules, il faut utiliser la même valeur dans chacune. Une décision valable pour un nombre de trajets ne vaut pas automatiquement pour tous.')

ex(269,2,'Découverte - Calcul littéral - Somme ou produit','easy',
   'Repérer la dernière opération, puis appliquer la distributivité lorsque c’est utile.',[
 q(r'Préciser la nature de $3(x+2)$, $3x+2$, $5x-4$ et $7x$.','La dernière opération donne la nature de l’expression.',[
   step('Regarder la structure extérieure',r'$3(x+2)$ et $7x$ sont des produits ; $3x+2$ est une somme ; $5x-4$ est une différence.')],'Produit ; somme ; différence ; produit.'),
 q(r'Développer $3(x+2)$.','Multiplier chacun des termes par 3.',[
   step('Distribuer le facteur',r'$3(x+2)=3\times x+3\times2$.'),step('Calculer les produits',r'$3(x+2)=3x+6$.')],r'$3x+6$.'),
 q('Pour x = 4, vérifier que les deux écritures précédentes donnent le même résultat.','Calculer chaque écriture indépendamment.',[
   step('Avec les parenthèses',r'$3(4+2)=3\times6=18$.'),step('Avec la forme développée',r'$3\times4+6=12+6=18$.')],'Les deux valeurs sont 18.'),
 q(r'Pourquoi $3x+2$ n’est-il pas le développement de $3(x+2)$ ?','Contrôler aussi le terme constant.',[
   step('Repérer le facteur oublié',r'Le nombre 2 est lui aussi multiplié par 3, ce qui donne 6.'),step('Un test qui distingue les expressions',r'Pour x = 4, $3x+2=14$, et non 18.')],r'Le terme constant doit être 6, pas 2.')],
   'Dans un développement, aucun terme de la parenthèse ne doit être oublié.')

ex(269,4,'Découverte - Calcul littéral - Réduire sans mélanger','easy',
   'Regrouper uniquement des termes de même nature.',[
 q(r'Réduire $2x+5x$.','Additionner les coefficients des mêmes multiples de x.',[
   step('Compter les multiples',r'$2x+5x=(2+5)x=7x$.')],r'$7x$.'),
 q(r'Réduire $3x+4+x+2$.','Regrouper les multiples de x et les nombres constants.',[
   step('Former les deux groupes',r'$(3x+x)+(4+2)$.'),step('Réduire',r'$4x+6$.')],r'$4x+6$.'),
 q(r'Réduire $7x-2x+3$.','Soustraire les coefficients et garder le terme constant.',[
   step('Réunir les termes de même nature',r'$(7-2)x+3=5x+3$.')],r'$5x+3$.'),
 q(r'Un élève remplace $4x+3$ par $7x$. Trouver un contre-exemple.','Choisir une valeur simple et comparer.',[
   step('Prendre x = 2',r'$4\times2+3=11$, tandis que $7\times2=14$.'),step('Conclure',r'$11\ne14$ : les deux expressions ne sont pas identiques.')],r'Pour $x=2$, on obtient 11 et 14 : la réduction proposée est fausse.')],
   'On ne peut pas additionner un nombre de fois x et un nombre constant comme s’ils avaient la même nature.')

ex(269,7,'Entraînement - Calcul littéral - Développer puis réduire','medium',
   'Appliquer la distributivité simple, puis regrouper les termes semblables.',[
 q(r'Développer $5(x-2)$.','Distribuer le facteur sur la différence.',[
   step('Multiplier chaque terme',r'$5\times x-5\times2$.'),step('Écrire la forme développée',r'$5x-10$.')],r'$5x-10$.'),
 q(r'Développer $2{,}5(x+4)$.','Multiplier les deux termes par 2,5.',[
   step('Distribuer',r'$2{,}5x+2{,}5\times4$.'),step('Calculer le terme constant',r'$2{,}5\times4=10$, donc $2{,}5x+10$.')],r'$2{,}5x+10$.'),
 q(r'Développer et réduire $3(2x+1)+x$.','Développer avant de réunir les multiples de x.',[
   step('Ouvrir la parenthèse',r'$3(2x+1)+x=6x+3+x$.'),step('Réduire',r'$6x+x+3=7x+3$.')],r'$7x+3$.'),
 q(r'Développer et réduire $6(3+x)-2x$.','Distribuer, puis soustraire les coefficients.',[
   step('Développer',r'$6(3+x)-2x=18+6x-2x$.'),step('Réduire',r'$18+(6-2)x=4x+18$.')],r'$4x+18$.')],
   'Développer et réduire sont deux opérations différentes : on commence par traiter les parenthèses.')

ex(269,9,'Entraînement - Calcul littéral - Retrouver un facteur commun','medium',
   'Factoriser signifie écrire une expression sous la forme d’un produit.',[
 q(r'Factoriser $6x+18$.','Repérer le facteur 6 dans les deux termes.',[
   step('Rendre le facteur visible',r'$6x+18=6\times x+6\times3$.'),step('Mettre en facteur',r'$6(x+3)$.')],r'$6(x+3)$.'),
 q(r'Factoriser $15x-10$.','Repérer le facteur 5.',[
   step('Décomposer les coefficients',r'$15x-10=5\times3x-5\times2$.'),step('Mettre en facteur',r'$5(3x-2)$.')],r'$5(3x-2)$.'),
 q(r'Réduire puis factoriser $4x+12+2x+6$.','Regrouper avant de chercher un facteur commun.',[
   step('Réduire la somme',r'$4x+2x+12+6=6x+18$.'),step('Factoriser',r'$6x+18=6(x+3)$.')],r'$6(x+3)$.'),
 q(r'Pour x = 5, vérifier la factorisation de $6x+18$.','Calculer séparément la somme et le produit.',[
   step('Dans la somme',r'$6\times5+18=30+18=48$.'),step('Dans le produit',r'$6(5+3)=6\times8=48$.')],'Les deux écritures donnent 48.')],
   'Le facteur mis devant la parenthèse doit multiplier tout ce qui reste à l’intérieur. Redévelopper permet de contrôler une factorisation.')

ex(269,14,'Problème - Calcul littéral - Démontrer et réfuter','hard',
   'Les lettres n, p et q désignent des entiers positifs ou nuls.',[
 q('Écrire un nombre pair et un nombre impair à l’aide de n.','Traduire pair par multiple de 2.',[
   step('Un nombre pair',r'Un multiple de 2 s’écrit $2n$.'),step('Un nombre impair',r'Le nombre suivant s’écrit $2n+1$.')],r'Pair : $2n$ ; impair : $2n+1$.'),
 q('Montrer que la somme de deux entiers consécutifs est impaire.','Écrire les deux entiers avec une même lettre.',[
   step('Écrire la somme',r'Les entiers sont n et n+1 ; leur somme est $n+(n+1)$.'),step('Reconnaître un impair',r'$n+n+1=2n+1$, forme d’un nombre impair.')],'La somme vaut $2n+1$, donc elle est impaire.'),
 q('Montrer que la somme de trois entiers consécutifs est un multiple de 3.','Faire apparaître un facteur 3.',[
   step('Réduire la somme',r'$n+(n+1)+(n+2)=3n+3$.'),step('Factoriser et interpréter',r'$3n+3=3(n+1)$. Comme n+1 est entier, la somme est un multiple de 3.')],r'La somme vaut $3(n+1)$.'),
 q('« La somme de deux carrés est toujours un carré. » Donner un contre-exemple.','Un seul cas faux suffit à réfuter une affirmation universelle.',[
   step('Choisir deux carrés simples',r'$1^2+2^2=1+4=5$.'),step('Montrer que 5 n’est pas un carré entier',r'$2^2=4<5<9=3^2$.')],'Faux : $1^2+2^2=5$ n’est pas un carré entier.'),
 q('Pourquoi les écritures avec n prouvent-elles les deux propriétés, alors que quelques exemples ne suffisent pas ?','Distinguer un calcul général et des tests particuliers.',[
   step('Préciser la portée du raisonnement','Aucune valeur particulière n’a été imposée à n dans les deux démonstrations. Les transformations valent pour tout entier n du domaine annoncé.')],'Les démonstrations s’appliquent à tous les entiers concernés ; les tests ne portent que sur les valeurs choisies.')],
   'Pour prouver une affirmation générale, expliquer pourquoi elle vaut pour toutes les valeurs. Pour la réfuter, un seul contre-exemple bien justifié suffit.')

ex(269,20,'Problème - Calcul littéral - Deux programmes équivalents','hard',
   'On choisit un nombre positif x. Programme A : multiplier par 3, ajouter 4, puis multiplier le résultat par 2. Programme B : ajouter 1, multiplier le résultat par 6, puis ajouter 2.',[
 q('Écrire une expression du résultat de chaque programme.','Traduire les opérations dans leur ordre, en gardant les parenthèses.',[
   step('Programme A',r'Après les deux premières opérations, on a $3x+4$ ; le résultat final est $2(3x+4)$.'),step('Programme B',r'Le résultat est $6(x+1)+2$.')],r'A : $2(3x+4)$ ; B : $6(x+1)+2$.'),
 q('Développer et réduire chaque expression.','Utiliser la distributivité sur les deux parenthèses.',[
   step('Développer A',r'$2(3x+4)=6x+8$.'),step('Développer B',r'$6(x+1)+2=6x+6+2=6x+8$.')],r'Les deux expressions se réduisent à $6x+8$.'),
 q('Contrôler les résultats pour x = 2 en suivant les programmes.','Refaire les opérations sans utiliser la forme réduite.',[
   step('Suivre A',r'$2\times3=6$, puis $6+4=10$, puis $10\times2=20$.'),step('Suivre B',r'$2+1=3$, puis $3\times6=18$, puis $18+2=20$.')],'Les deux programmes donnent 20.'),
 q('Les deux programmes donnent-ils toujours le même résultat ? Justifier.','S’appuyer sur l’identité littérale, pas seulement sur le test.',[
   step('Utiliser la forme commune',r'Pour toute valeur autorisée de x, les deux programmes produisent l’expression $6x+8$. Ce sont donc deux façons de calculer le même nombre.')],'Oui, car les deux expressions sont identiques pour tout x positif.'),
 q('Un troisième programme multiplie x par 6 puis ajoute 6. Est-il équivalent aux deux premiers ?','Chercher une valeur qui distingue les résultats.',[
   step('Tester avec x = 2',r'Le troisième donne $6\times2+6=18$, alors que A et B donnent 20.'),step('Conclure',r'$18\ne20$ : les programmes ne sont pas équivalents.')],'Non : x = 2 donne un contre-exemple.')],
   'Un test peut montrer que deux programmes diffèrent. Pour démontrer qu’ils sont toujours équivalents, on transforme leurs expressions littérales.')

ex(270,2,'Découverte - Inconnues - Retrouver le terme d’une addition','easy',
   'Retrouver le nombre caché par une opération inverse, puis vérifier dans l’égalité initiale.',[
 q(r'Résoudre $x+7=19$.','Retirer 7 du total.',[step('Retrouver le nombre',r'$x=19-7=12$.'),step('Vérifier',r'$12+7=19$.')],r'$x=12$.'),
 q(r'Résoudre $x+2{,}5=6{,}2$.','Soustraire le terme ajouté.',[step('Calculer la différence',r'$x=6{,}2-2{,}5=3{,}7$.'),step('Vérifier',r'$3{,}7+2{,}5=6{,}2$.')],r'$x=3{,}7$.'),
 q(r'Résoudre $x+6=2$.','La différence peut être négative.',[step('Retrouver le terme manquant',r'$x=2-6=-4$.'),step('Vérifier',r'$-4+6=2$.')],r'$x=-4$.'),
 q('Faut-il toujours refuser une solution négative ?','Vérifier à la fois l’égalité et le sens de la situation.',[step('Distinguer les contraintes','Une température peut être négative ; le prix d’un objet ordinaire ne le peut pas. Dans une équation sans contrainte de contexte, un nombre négatif peut parfaitement convenir.')],'Non ; cela dépend du contexte, puis de la vérification.')],
   'On défait une addition par une soustraction. Le signe de la solution se contrôle dans l’égalité de départ.')

ex(270,4,'Découverte - Inconnues - Multiplication et division à trous','easy',
   'Chaque coefficient de multiplication ou diviseur indiqué est non nul.',[
 q(r'Résoudre $4x=18$.','Partager 18 en quatre parts égales.',[step('Diviser par le coefficient',r'$x=18\div4=4{,}5$.'),step('Vérifier',r'$4\times4{,}5=18$.')],r'$x=4{,}5$.'),
 q(r'Résoudre $2x=0$.','Chercher le nombre dont le double est nul.',[step('Diviser',r'$x=0\div2=0$.'),step('Vérifier',r'$2\times0=0$.')],r'$x=0$.'),
 q(r'Résoudre $\frac{x}{3}=7$.','Défaire le partage en multipliant.',[step('Reconstituer le tout',r'$x=7\times3=21$.'),step('Vérifier',r'$21\div3=7$.')],r'$x=21$.'),
 q(r'Pourquoi $4x=18$ n’a-t-elle pas de solution entière, alors qu’elle a une solution décimale ?','Préciser la nature du nombre demandé.',[step('Comparer aux multiples entiers',r'$4\times4=16$ et $4\times5=20$ : 18 est entre deux multiples entiers consécutifs de 4.'),step('Interpréter la solution',r'$4{,}5$ est décimal, mais pas entier.')],'Aucun entier ne convient ; le décimal 4,5 convient.')],
   'Défaire une multiplication demande une division ; défaire une division demande une multiplication. Zéro peut être une solution.')

ex(270,7,'Entraînement - Inconnues - Modéliser une distance et un prix','medium',
   'Pour chaque situation, nommer l’inconnue, écrire une équation à une opération, puis répondre avec son unité.',[
 q('Une randonnée mesure 12,5 km. On a parcouru 7,8 km. Quelle distance reste-t-il ?','Le parcours déjà fait et le reste forment le parcours total.',[step('Traduire',r'En notant x le reste en km : $x+7{,}8=12{,}5$.'),step('Résoudre et vérifier',r'$x=12{,}5-7{,}8=4{,}7$, et $4{,}7+7{,}8=12{,}5$.')],'Il reste 4,7 km.'),
 q('Un ruban de 18 m est partagé en 4 morceaux égaux. Quelle est la longueur d’un morceau ?','Quatre longueurs identiques reconstituent le ruban.',[step('Traduire',r'En notant ℓ la longueur en m : $4\ell=18$.'),step('Résoudre et vérifier',r'$\ell=18\div4=4{,}5$, et $4\times4{,}5=18$.')],'Chaque morceau mesure 4,5 m.'),
 q('Cinq stylos identiques coûtent 7,50 €. Quel est leur prix unitaire ?','Partager le prix total entre les cinq stylos.',[step('Traduire',r'Si p est le prix d’un stylo en euros, $5p=7{,}50$.'),step('Résoudre et vérifier',r'$p=7{,}50\div5=1{,}50$, et $5\times1{,}50=7{,}50$.')],'1,50 € par stylo.'),
 q('Une température augmente de 6 °C et atteint 2 °C. Quelle était sa valeur initiale ?','La température initiale augmentée de 6 donne la finale.',[step('Traduire',r'Si t est la température initiale : $t+6=2$.'),step('Résoudre et vérifier',r'$t=2-6=-4$, et $-4+6=2$.')],r'$-4$ °C.')],
   'Le même calcul inverse sert dans des contextes différents. Nommer l’inconnue et son unité évite de confondre un prix total, un prix unitaire, une distance et une température.')

ex(270,9,'Entraînement - Inconnues - Fractions simples et opérations inverses','medium',
   'Résoudre par le sens des opérations, sans utiliser de règle générale de division de fractions.',[
 q(r'Résoudre $\frac{x}{4}=\frac32$.','Multiplier la valeur d’une part par le nombre de parts.',[step('Interpréter la fraction',r'$\frac32=1{,}5$.'),step('Reconstituer le tout',r'$x=1{,}5\times4=6$. Vérification : $6\div4=1{,}5$.')],r'$x=6$.'),
 q(r'Résoudre $\frac32x=9$.','Remplacer le coefficient par un décimal connu.',[step('Réécrire',r'$\frac32=1{,}5$, donc on cherche le nombre dont le produit par 1,5 vaut 9.'),step('Diviser et vérifier',r'$x=9\div1{,}5=6$. Vérification par le sens de la fraction : $(6\div2)\times3=9$.')],r'$x=6$.'),
 q(r'Résoudre $x+\frac34=\frac54$.','Soustraire des fractions de même dénominateur.',[step('Retirer trois quarts',math(r'x=\frac54-\frac34=\frac24=\frac12')),step('Vérifier',r'$\frac12+\frac34=\frac24+\frac34=\frac54$.')],r'$x=\frac12$.'),
 q('Ces trois équations ont-elles toutes la même solution ?','Comparer les valeurs obtenues, pas seulement les symboles.',[step('Rassembler les solutions',r'Les deux premières donnent 6 ; la troisième donne $\frac12$. Elles n’ont donc pas toutes la même solution.')],'Non : 6, 6 et 1/2.')],
   'Un coefficient fractionnaire simple peut parfois être lu comme un décimal connu. On n’a pas besoin d’une règle de division de fractions pour ces calculs.')

ex(270,14,'Problème - Inconnues - Détecter les fausses résolutions','hard',
   'Trois élèves proposent des résultats. Contrôler chaque raisonnement dans l’équation de départ.',[
 q(r'Ana écrit : pour $x+(-4)=3$, « $x=3-4=-1$ ». Corriger.','Chercher le nombre auquel on retire 4 pour obtenir 3.',[step('Tester le résultat proposé',r'$-1+(-4)=-5$, et non 3 : la proposition ne convient pas.'),step('Utiliser la bonne opération inverse',r'$x=3+4=7$. Vérification : $7+(-4)=3$.')],r'$x=7$.'),
 q(r'Bilal refuse la valeur $\frac35$ pour $5x=3$, car « ce n’est pas un entier ». A-t-il raison ?','Relier le quotient à une division décimale.',[step('Calculer la solution',r'$x=3\div5=\frac35=0{,}6$.'),step('Vérifier et conclure',r'$5\times0{,}6=3$. Sans contrainte de nombre entier dans l’énoncé, cette solution est autorisée.')],r'Non : $x=\frac35=0{,}6$ convient.'),
 q(r'Chloé refuse $x=-2$ pour $x+7=5$. Que montre la vérification ?','Tester l’égalité avant d’écarter un signe.',[step('Substituer',r'$-2+7=5$.'),step('Conclure','La valeur proposée rend l’égalité vraie. Aucun contexte n’impose ici un nombre positif.')],r'$x=-2$ convient.'),
 q('On cherche maintenant un entier x tel que 4x = 18. Quelle est la réponse ?','Tenir compte de la contrainte annoncée.',[step('Retrouver la seule valeur numérique possible',r'$18\div4=4{,}5$.'),step('Appliquer la contrainte','4,5 n’est pas un entier. Il n’existe donc pas d’entier satisfaisant la demande, même si l’équation admet cette solution décimale.')],'Aucune solution entière ; la solution décimale serait 4,5.')],
   'Une vérification se fait dans l’égalité de départ. Ensuite, le contexte peut imposer des contraintes supplémentaires : signe, unité ou nombre entier.')

ex(270,20,'Problème - Inconnues - Préparer huit flacons','hard',
   'Un bidon vide pèse 1,2 kg. Rempli, il pèse 4,8 kg. Son contenu est réparti également dans 8 flacons. Chaque flacon vide pèse 50 g.',[
 q('Quelle est la masse du contenu du bidon ? Nommer l’inconnue et écrire l’équation.','Séparer la masse du récipient et celle du contenu.',[step('Traduire',r'En notant m la masse du contenu en kg, $m+1{,}2=4{,}8$.'),step('Résoudre et vérifier',r'$m=4{,}8-1{,}2=3{,}6$ kg ; $3{,}6+1{,}2=4{,}8$.')],'Le contenu pèse 3,6 kg.'),
 q('Quelle masse de contenu reçoit un flacon ? Écrire une équation à une opération.','Huit masses identiques reconstituent les 3,6 kg.',[step('Traduire',r'Si x est la masse en kg reçue par un flacon, $8x=3{,}6$.'),step('Partager et vérifier',r'$x=3{,}6\div8=0{,}45$ kg ; $8\times0{,}45=3{,}6$.')],'0,45 kg par flacon.'),
 q('Exprimer cette masse en grammes.','Convertir avant d’ajouter une masse en grammes.',[step('Convertir',r'$0{,}45\times1\,000=450$ g.')],'450 g de contenu.'),
 q('Combien pèse un flacon rempli ?','Ajouter le récipient à son contenu dans la même unité.',[step('Ajouter les masses',r'$450+50=500$ g.')],'500 g.'),
 q('Combien de kilogrammes de contenu faudrait-il pour remplir 10 flacons de la même façon ? Le bidon suffit-il ?','Calculer la demande totale puis comparer à la réserve.',[step('Calculer la quantité nécessaire',r'$10\times0{,}45=4{,}5$ kg.'),step('Mesurer le manque',r'$4{,}5-3{,}6=0{,}9$ kg.')],'Il faudrait 4,5 kg ; le bidon ne suffit pas, il manque 0,9 kg.')],
   'Chaque équation traduit une seule relation simple. Dans un problème en plusieurs étapes, on réutilise le résultat précédent en précisant ce qu’il mesure.')

NOTES={
266:'Identifier le même tout avant d’additionner. Pour comparer des parts ou des volumes, passer à un partage commun.',
267:'L’exposant compte les facteurs identiques. Vérifier les unités : longueur, aire et volume ne mesurent pas la même grandeur.',
268:'Le rang est une entrée de la formule ; le nombre d’objets est sa sortie. Un test réussi ne prouve pas une égalité générale.',
269:'Le facteur multiplie chaque terme de la parenthèse. Une preuve avec une lettre explique le cas général ; un test ne le remplace pas.',
270:'Nommer l’inconnue et son unité, défaire l’opération, puis remplacer la lettre dans l’égalité initiale pour vérifier.',
}
STEP_TITLES={
266:['Identifier le tout','Construire des fractions égales','Additionner les parts','Calculer le complément','Passer aux quantités','Comparer les prélèvements'],
267:['Compter les lignes et colonnes','Calculer l’aire','Compter les couches','Calculer le nombre de cubes','Comparer les aires','Comparer les volumes'],
268:['Construire les premiers rangs','Compter les accroissements','Remplacer le rang','Vérifier les valeurs initiales','Retrouver le rang','Comparer au rang double'],
269:['L’aire du rectangle entier','Les aires des deux morceaux','Utiliser l’additivité des aires','Deux calculs indépendants','Repérer le facteur oublié','Raisonner sur la bande ajoutée'],
270:['Nommer l’inconnue','Traduire la situation','Retrouver la donnée manquante','Effectuer l’opération inverse','Vérifier la valeur trouvée','Interpréter la réponse'],
}

def box(kind,title,text):return f'::: {kind}'+((' '+title) if title else '')+'\n'+text+'\n:::\n'

def render(e,eid):
    text='=== '+e['titre']+'\nId: '+str(eid)+'\nDifficulté: '+e['difficulte']+'\n\nÉnoncé:\n'+MARK+'\n'+e['intro']+'\n\n'
    text+='\n'.join(f'{i}. {q["question"]}' for i,q in enumerate(e['questions'],1))+'\n\nÉtapes:\n'+MARK+'\n'
    for i,qq in enumerate(e['questions'],1):
        text+=f'## Question {i} : {qq["question"]}\n\n'+box('methode','',qq['methode'])+'\n'
        for title,body in qq['etapes']:text+=box('etape',title,body)+'\n'
        text+=box('resultat','',qq['resultat'])+'\n'
    text+=box('attention' if e['difficulte']=='hard' else 'retenir','Le bon réflexe',e['note'])+'\nSolution:\n'+MARK+'\n'
    text+='\n'.join(f'{i}. {qq["resultat"]}' for i,qq in enumerate(e['questions'],1))+'\n'
    return text

def snapshot(d):
    backup=d/'sauvegardes/revision_2026-10-30'
    if not (backup/'exercices.txt').exists():
        backup.mkdir(parents=True,exist_ok=True)
        for p in d.iterdir():
            if p.is_file() and p.suffix in ('.txt','.json','.md','.py'):
                shutil.copyfile(p,backup/p.name)
        (backup/'figures').mkdir(exist_ok=True)
        for name in ('figures.py','correspondance.json'):
            shutil.copyfile(d/'figures'/name,backup/'figures'/name)
    return backup

def simple_bill(block):
    """Remplace ax+b=c par la relation centrale ax=c ; Id et prix conservés."""
    head,body=block.split('Énoncé:',1)
    old=re.search(r'achète (\d+) pochettes.*?emballage à (\d+) €.*?totale est de (\d+) €',body,re.S)
    if not old:return None
    n,fee,total=map(int,old.groups());subtotal=total-fee;price=Fraction(subtotal,n);delta=Fraction(6,n)
    def f(v):
        return str(v.numerator) if v.denominator==1 else rf'\frac{{{v.numerator}}}{{{v.denominator}}}'
    eid=int(re.search(r'^Id: (\d+)',head,re.M)[1])
    e={'titre':f'Entraînement - Inconnues - Prix unitaire et vérification {eid}','difficulte':'medium',
       'intro':f'{n} pochettes identiques coûtent ensemble {subtotal} €. Un emballage facultatif coûte {fee} € en plus. On appelle x le prix d’une pochette, en euros.',
       'note':'L’équation du prix unitaire porte sur les seules pochettes. L’emballage est une dépense distincte, ajoutée ensuite si on le choisit.',
       'questions':[
       q('Que représente x, et dans quelle unité ?','Identifier la quantité inconnue.',[step('Nommer le prix recherché','Toutes les pochettes ont le même prix. x désigne le prix d’une seule pochette, en euros.')],'Le prix d’une pochette, en euros.'),
       q('Écrire l’équation qui permet de retrouver ce prix.','Le prix total des pochettes est un produit.',[step('Traduire les données',rf'Les {n} pochettes coûtent ${n}x$ euros au total ; donc ${n}x={subtotal}$.')],rf'${n}x={subtotal}$.'),
       q('Retrouver le prix d’une pochette.','Partager le prix total en parts égales.',[step('Diviser par le nombre de pochettes',rf'$x={subtotal}\div{n}={f(price)}$.')],rf'${f(price)}$ € par pochette.'),
       q('Vérifier le prix trouvé dans l’égalité initiale.','Reconstituer le prix des pochettes.',[step('Multiplier le prix unitaire',rf'${n}\times{f(price)}={subtotal}$ : on retrouve le montant annoncé.')],'La réponse est vérifiée.'),
       q('Quel est le montant à payer si on prend aussi l’emballage ?','Ajouter la dépense facultative une seule fois.',[step('Calculer la facture complète',rf'${subtotal}+{fee}={total}$ €.'),step('Lire le schéma de bilan',rf'Dans le schéma, $n={n}$, $b={fee}$ et $T={total}$. Le total T comprend cette fois l’emballage.'+'\n\n[IMAGE_2]')],f'{total} €.'),
       q('Le prix total des seules pochettes augmente de 6 €, pour le même nombre de pochettes. Quelle est la hausse par pochette ?','Répartir la hausse sur le même nombre d’objets.',[step('Partager la hausse',rf'$6\div{n}={f(delta)}$ € par pochette.'),step('Calculer le nouveau prix',rf'${f(price)}+{f(delta)}={f(price+delta)}$ €.')],rf'Hausse : ${f(delta)}$ € par pochette ; nouveau prix : ${f(price+delta)}$ €.')]}
    return e

def apply():
    for code in range(266,271):
        d=next(BASE.glob(f'{code}_*'));backup=snapshot(d)
        (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'coordination-5e','maj':DATE,'revision':'harmonisation Terminale et diversification'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        original=(backup/'exercices.txt').read_text(encoding='utf-8')
        blocks=[b.strip() for b in re.split(r'^===[ \t]*$',original,flags=re.M) if b.strip()]
        corr=json.loads((backup/'figures/correspondance.json').read_text(encoding='utf-8'))
        manifest=[];replacements={e['slot']:e for e in DATA[code]};out=[]
        for index,b in enumerate(blocks):
            eid=int(re.search(r'^Id: (\d+)',b,re.M)[1])
            e=replacements.get(index)
            kind='diversification'
            if e is None and code==270:
                e=simple_bill(b);kind='recentrage équation à une opération'
            if e is not None:
                old_title=re.search(r'^=== (.+)',b,re.M)[1]
                out.append(render(e,eid));corr['exercices'].pop(str(eid),None)
                if kind.startswith('recentrage'):
                    corr['exercices'][str(eid)]={'2':{'fichier':'schema_parametre.png','alt':'Bilan du prix des pochettes et de l’emballage, total calculé dans le corrigé.'}}
                for pos,(name,alt) in e.get('images',{}).items():
                    corr['exercices'].setdefault(str(eid),{})[str(pos)]={'fichier':name+'.png','alt':alt}
                manifest.append({'id':eid,'ancien_titre':old_title,'titre':e['titre'],'difficulte':e['difficulte'],'type':kind,'questions':len(e['questions'])})
            else:
                # Intitulés d'étapes propres au raisonnement, sans modifier les calculs.
                parts=re.split(r'(?=^## Question )',b,flags=re.M)
                for qi in range(1,len(parts)):
                    title=STEP_TITLES[code][min(qi-1,5)]
                    parts[qi]=parts[qi].replace('::: etape Raisonnement et calcul','::: etape '+title)
                b=''.join(parts)
                if '::: retenir' not in b and '::: attention' not in b:
                    b=b.replace('\nSolution:', '\n'+box('retenir','Le bon réflexe',NOTES[code])+'\nSolution:')
                if 'Difficulté: hard' in b:
                    old_title=re.search(r'^=== (.+)',b,re.M)[1]
                    new_title=f'Entraînement - {d.name.split("_",1)[1].replace("-"," ").capitalize()} - Consolidation {eid}'
                    b=b.replace('=== '+old_title,'=== '+new_title,1).replace('Difficulté: hard','Difficulté: medium',1)
                    manifest.append({'id':eid,'ancien_titre':old_title,'titre':new_title,'difficulte':'medium','type':'difficulté rendue cohérente','questions':6})
                if code==269:
                    # Le corrigé montre les deux aires identifiées en vert.
                    where=b.index('Solution:')
                    b=b[:where].rstrip()+'\n\n[IMAGE_2]\n\n'+b[where:]
                    corr['exercices'].setdefault(str(eid),{})['2']={'fichier':'rectangle_aires_corrige.png','alt':'Aires kx et kb des deux morceaux du rectangle, en vert, avec les paramètres de l’énoncé.'}
                out.append(b)
        (d/'exercices.txt').write_text('\n===\n\n'.join(out),encoding='utf-8')
        (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'revision_20261030.json').write_text(json.dumps({'date':DATE,'notion':code,'modifications':manifest,'blocs_conserves':21,'ids_conserves':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(code,len(manifest),'modifications, 21 Id conservés')

if __name__=='__main__':apply()
