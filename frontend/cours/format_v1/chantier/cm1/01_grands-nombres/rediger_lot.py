# -*- coding: utf-8 -*-
"""Rédaction originale des cinq chapitres de numération CM1 attribués."""
from pathlib import Path
import json, re, hashlib
ROOT=Path(__file__).resolve().parent.parent
DATA={}; DOCS={}; FIGS={}; MAPS={}
def q(enonce,reponse,raison,methode='Utiliser le sens des nombres et vérifier chaque rang.'):
    return {'q':enonce,'r':reponse,'e':raison,'m':methode}
def ex(titre,contexte,questions,images=None):
    assert len(questions)>=5
    return {'titre':titre,'contexte':contexte,'questions':questions,'images':images or {}}
def init(code):
    d=next(ROOT.glob(f'{code:02}_*'));source=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
    DATA[code]=[];FIGS[code]={};MAPS[code]={'cours':{},'fiches':{},'exercices':{}}
    return source
def add(code,*args,**kw): DATA[code].append(ex(*args,**kw))
def fig(code,name,tikz):FIGS[code][name]=tikz
def image(code,owner,position,name,alt):
    group='exercices' if owner.startswith('nouveau-') else ('cours' if owner=='nouveau' else 'fiches')
    MAPS[code][group].setdefault(owner,{})[str(position)]={'fichier':name+'.png','alt':alt}
def line(start,end,steps,points,labels=None):
    s=[r'\begin{tikzpicture}[x=1cm,y=1cm]',r'\draw[otNavy,line width=.8pt,-{Stealth[length=2mm]}] (0,0)--(6.35,0);']
    for i in range(steps+1):
        x=6*i/steps;s.append(fr'\draw[otNavy,line width=.6pt] ({x:.5f},-.07)--({x:.5f},.07);')
    for i,txt in (labels or {0:start,steps:end}).items():
        s.append(fr'\node[below=6pt,text=otInk] at ({6*i/steps:.5f},0) {{$ {txt} $}};')
    for letter,i,*color in points:
        c=color[0] if color else 'otNavy';x=6*i/steps
        s.extend([fr'\fill[{c}] ({x:.5f},0) circle (1.7pt);',fr'\node[above=8pt,text={c}] at ({x:.5f},0) {{$ {letter} $}};'])
    return '\n'.join(s+[r'\end{tikzpicture}'])
def bands(rows):
    s=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for j,(n,colored,label) in enumerate(rows):
        y=-j*1.55
        for i in range(n):
            fill='otGreen!30' if i<colored else 'white'
            s.append(fr'\fill[{fill}] ({6*i/n:.5f},{y}) rectangle ({6*(i+1)/n:.5f},{y+.62});')
        for i in range(n+1):s.append(fr'\draw[otNavy,line width=.6pt] ({6*i/n:.5f},{y})--({6*i/n:.5f},{y+.62});')
        s.append(fr'\draw[otNavy,line width=.7pt] (0,{y}) rectangle (6,{y+.62});')
        s.append(fr'\node[below=6pt,text=otInk] at (3,{y}) {{{label}}};')
    return '\n'.join(s+[r'\end{tikzpicture}'])
def disk(n,colored):
    s=[r'\begin{tikzpicture}']
    for i in range(n):
        a=90+i*360/n;b=90+(i+1)*360/n
        s.append(fr'\fill[{"otGreen!30" if i<colored else "white"}] (0,0)--({a}:1.25) arc ({a}:{b}:1.25)--cycle;')
        s.append(fr'\draw[otNavy,line width=.6pt] (0,0)--({a}:1.25);')
    return '\n'.join(s+[r'\draw[otNavy,line width=.8pt] (0,0) circle (1.25);',r'\end{tikzpicture}'])
s=init(7)
add(7,'Lire sur la demi-droite','Une unité correspond à quatre petits intervalles.\n\n[IMAGE_1]',[
 q('Quelle fraction de l’unité représente un pas ?',r'$\frac{1}{4}$.','Il faut quatre pas égaux pour aller de zéro à un. Chaque pas représente donc un quart d’unité.'),
 q('Lire la fraction du point A.',r'$\frac{3}{4}$.','A est situé trois pas après zéro. Trois pas d’un quart font trois quarts.'),
 q('Lire la fraction du point B.',r'$\frac{7}{4}$.','B est situé sept pas après zéro. On compte les pas depuis zéro, même lorsque le point dépasse un.'),
 q('Décomposer la fraction de B en un entier et une fraction.',r'$\frac{7}{4}=1+\frac{3}{4}$.','Quatre pas arrivent à un. B est encore trois pas plus loin, donc trois quarts après un.'),
 q('Comparer les fractions de A et B.',r'$\frac{3}{4}<\frac{7}{4}$.','Les pas ont la même taille. B est à droite de A sur la demi-droite et représente un nombre plus grand.')])
fig(7,'quarts',line('0','2',8,[('A',3),('B',7)],{0:'0',4:'1',8:'2'}));image(7,'nouveau-1',1,'quarts','Demi-droite graduée en quarts de zéro à deux, A à trois quarts et B à sept quarts.')
add(7,'Placer des tiers','Une unité correspond à trois intervalles égaux.\n\n[IMAGE_1]',[
 q('Quelle fraction représente un petit intervalle ?',r'$\frac{1}{3}$.','On partage l’intervalle entre zéro et un en trois pas. Chaque pas est un tiers d’unité.'),
 q(r'Placer $C\left(\frac{2}{3}\right)$.','C est au deuxième pas après zéro.','On part de zéro et on avance de deux tiers. C se trouve avant un, qui demande trois pas.'),
 q(r'Placer $D\left(\frac{5}{3}\right)$.','D est au cinquième pas après zéro.','Trois pas font une unité. On avance encore de deux pas pour atteindre cinq tiers.'),
 q('Écrire la position de D avec un entier.',r'$\frac{5}{3}=1+\frac{2}{3}$.','Les cinq tiers se regroupent en trois tiers plus deux tiers. Trois tiers valent exactement un.'),
 q('Quelle distance sépare C et D, en unités ?',r'$\frac{5}{3}-\frac{2}{3}=1$.','Entre le deuxième et le cinquième pas, il y a trois intervalles. Trois tiers font une unité entière.\n\n[IMAGE_2]')])
fig(7,'tiers_vierge',line('0','2',6,[],{0:'0',3:'1',6:'2'}));fig(7,'tiers_corrige',line('0','2',6,[('C',2,'otGreenDark'),('D',5,'otGreenDark')],{0:'0',3:'1',6:'2'}));image(7,'nouveau-2',1,'tiers_vierge','Demi-droite de zéro à deux, chaque unité étant divisée en trois intervalles égaux.');image(7,'nouveau-2',2,'tiers_corrige','Demi-droite en tiers corrigée : C au deuxième pas et D au cinquième pas sont indiqués en vert.')
add(7,'Comparer à l’unité','Une unité entière correspond à autant de parts que le dénominateur.',[
 q(r'Comparer $\frac{5}{6}$ à 1.',r'$\frac{5}{6}<1$.','Il faut six sixièmes pour une unité. Avec cinq sixièmes, il manque une part.'),
 q(r'Comparer $\frac{7}{6}$ à 1.',r'$\frac{7}{6}>1$.','Sept sixièmes sont plus que les six sixièmes nécessaires. La fraction dépasse l’unité.'),
 q(r'Comparer $\frac{6}{6}$ à 1.',r'$\frac{6}{6}=1$.','Le nombre de parts prises est exactement le nombre de parts du partage. L’unité est complète.'),
 q(r'Ranger $\frac{5}{6}$, $\frac{7}{6}$ et $\frac{6}{6}$.',r'$\frac{5}{6}<\frac{6}{6}<\frac{7}{6}$.','Les trois fractions ont le même dénominateur. On range les numérateurs dans l’ordre 5, 6, 7.'),
 q(r'Combien manque-t-il à $\frac{5}{6}$ pour atteindre 1 ?',r'$\frac{1}{6}$.','Une seule part de sixième manque. Ajouter un sixième donne six sixièmes, soit un.')])
add(7,'Même dénominateur','Les parts ont la même taille quand les dénominateurs sont identiques.',[
 q(r'Comparer $\frac{5}{8}$ et $\frac{3}{8}$.',r'$\frac{5}{8}>\frac{3}{8}$.','Cinq parts de même taille couvrent plus que trois. On compare ici les numérateurs.'),
 q(r'Ranger $\frac{4}{5}$, $\frac{1}{5}$ et $\frac{7}{5}$.',r'$\frac{1}{5}<\frac{4}{5}<\frac{7}{5}$.','Le dénominateur commun est 5. L’ordre croissant des numérateurs est 1, 4, 7.'),
 q(r'Comparer $\frac{11}{12}$ et $\frac{7}{12}$.',r'$\frac{11}{12}>\frac{7}{12}$.','Les douzièmes ont la même taille. Onze de ces parts sont plus que sept.'),
 q(r'Quelle fraction est la plus proche de 1 entre $\frac{5}{8}$ et $\frac{7}{8}$ ?',r'$\frac{7}{8}$.','Il manque un huitième à sept huitièmes. Il manque trois huitièmes à cinq huitièmes ; sept huitièmes sont donc plus proches de un.'),
 q(r'Intercaler une fraction entre $\frac{2}{9}$ et $\frac{5}{9}$ sans changer le dénominateur.',r'Par exemple $\frac{2}{9}<\frac{3}{9}<\frac{5}{9}$.','On choisit un numérateur strictement entre 2 et 5. Trois convient ; quatre est une autre réponse possible.')])
add(7,'Une part d’une quantité','Pour trouver une fraction unitaire, partager la quantité en groupes égaux.',[
 q(r'Calculer $\frac{1}{3}$ de 12 billes.',r'$4$ billes.',r'On forme trois groupes égaux : $12\div3=4$. Un groupe correspond au tiers.'),
 q(r'Calculer $\frac{1}{4}$ de 100 mètres.',r'$25$ mètres.',r'On partage la longueur en quatre : $100\div4=25$. Chaque part mesure vingt-cinq mètres.'),
 q(r'Calculer $\frac{1}{2}$ de 18 jetons.',r'$9$ jetons.',r'Deux moitiés égales doivent contenir les dix-huit jetons : $18\div2=9$.'),
 q(r'Calculer $\frac{1}{5}$ de 35 euros.',r'$7$ euros.',r'On cherche une des cinq parts égales : $35\div5=7$.'),
 q(r'Pourquoi le tiers de 12 n’est-il pas $12-3$ ?',r'Le tiers de 12 est $4$, pas $9$.','Prendre le tiers signifie partager en trois groupes égaux. Soustraire trois retire trois objets, ce qui correspond à une autre opération.')])
add(7,'Réunir des parts','Additionner des fractions qui utilisent le même partage.',[
 q(r'Calculer $\frac{3}{8}+\frac{2}{8}$.',r'$\frac{3}{8}+\frac{2}{8}=\frac{5}{8}$.','Trois huitièmes et deux huitièmes font cinq huitièmes. Le nom de la part reste huitième.'),
 q(r'Calculer $\frac{2}{5}+\frac{3}{5}$.',r'$\frac{2}{5}+\frac{3}{5}=1$.','On obtient cinq cinquièmes. Toutes les parts de l’unité sont réunies.'),
 q(r'Calculer $\frac{5}{6}+\frac{4}{6}$.',r'$\frac{5}{6}+\frac{4}{6}=\frac{9}{6}$.','Les neuf parts sont toutes des sixièmes. Le résultat peut dépasser une unité.'),
 q(r'Écrire le résultat précédent avec un entier et une fraction.',r'$\frac{9}{6}=1+\frac{3}{6}$.','Six sixièmes font une unité. Il reste trois sixièmes après ce regroupement.'),
 q(r'Corriger $\frac{3}{8}+\frac{2}{8}=\frac{5}{16}$.',r'Le résultat correct est $\frac{5}{8}$.','On additionne les nombres de parts, pas les partages. Le découpage en huitièmes ne devient pas un découpage en seizièmes.')])
add(7,'Retirer des parts','Retirer seulement des parts de même taille.',[
 q(r'Calculer $\frac{7}{10}-\frac{4}{10}$.',r'$\frac{7}{10}-\frac{4}{10}=\frac{3}{10}$.','En retirant quatre dixièmes de sept dixièmes, il en reste trois. Le dénominateur reste 10.'),
 q(r'Calculer $1-\frac{2}{9}$.',r'$1-\frac{2}{9}=\frac{7}{9}$.','On écrit une unité comme neuf neuvièmes. On retire deux parts à ces neuf parts.'),
 q(r'Calculer $\frac{11}{12}-\frac{5}{12}$.',r'$\frac{11}{12}-\frac{5}{12}=\frac{6}{12}$.','Les fractions parlent toutes les deux de douzièmes. Onze parts moins cinq parts donnent six parts.'),
 q(r'Calculer $2-\frac{3}{4}$.',r'$2-\frac{3}{4}=\frac{5}{4}$.','Deux unités font huit quarts. Après avoir retiré trois quarts, il reste cinq quarts.'),
 q('Le résultat précédent est-il supérieur à un ?',r'Oui : $\frac{5}{4}>1$.','Une unité vaut quatre quarts. Cinq quarts dépassent cette unité d’un quart.')])
add(7,'Compléter jusqu’à un','Compléter chaque égalité pour obtenir le nombre d’unités indiqué à droite.',[
 q(r'Compléter $\frac{5}{9}+\frac{\square}{9}=1$.',r'Le nombre manquant est $4$.',r'Il faut neuf neuvièmes en tout. Le complément du numérateur est $9-5=4$.'),
 q(r'Compléter $\frac{\square}{6}+\frac{1}{6}=1$.',r'Le nombre manquant est $5$.','Six sixièmes font une unité. Il faut donc cinq sixièmes avant d’ajouter le dernier.'),
 q(r'Compléter $\frac{3}{8}+\frac{\square}{8}=1$.',r'Le nombre manquant est $5$.',r'Il manque $8-3=5$ parts de huitième. Le dénominateur ne change pas.'),
 q(r'Compléter $\frac{7}{10}+\frac{\square}{10}=1$.',r'Le nombre manquant est $3$.','Dix dixièmes constituent une unité. Après sept dixièmes, trois dixièmes complètent le tout.'),
 q(r'Compléter $\frac{7}{6}+\frac{\square}{6}=2$.',r'Le nombre manquant est $5$.','Deux unités font douze sixièmes. Il manque cinq sixièmes entre sept et douze sixièmes.')])
add(7,'Des cinquièmes bien placés','La demi-droite est graduée en cinquièmes.\n\n[IMAGE_1]',[
 q('Lire la fraction de E.',r'$\frac{4}{5}$.','E est placé au quatrième pas après zéro. Chaque pas représente un cinquième.'),
 q(r'Placer $F\left(1+\frac{2}{5}\right)$.','F est au deuxième pas après un, soit au septième pas après zéro.','Cinq pas donnent une unité. On ajoute encore les deux pas demandés.'),
 q('Écrire la position de F avec une seule fraction.',r'$1+\frac{2}{5}=\frac{7}{5}$.','Une unité vaut cinq cinquièmes. Avec deux cinquièmes supplémentaires, on obtient sept cinquièmes.'),
 q('Quelle fraction d’unité sépare E et F ?',r'$\frac{7}{5}-\frac{4}{5}=\frac{3}{5}$.','On compte les intervalles entre les quatrième et septième pas. Il y en a trois de même taille.'),
 q('Quel point est le plus proche de un ?',r'E.','E est à un cinquième de un. F est à deux cinquièmes de un ; E est donc le plus proche.\n\n[IMAGE_2]')])
fig(7,'cinquiemes',line('0','2',10,[('E',4)],{0:'0',5:'1',10:'2'}));fig(7,'cinquiemes_corrige',line('0','2',10,[('E',4),('F',7,'otGreenDark')],{0:'0',5:'1',10:'2'}));image(7,'nouveau-9',1,'cinquiemes','Demi-droite de zéro à deux en cinquièmes, avec E au quatrième pas après zéro.');image(7,'nouveau-9',2,'cinquiemes_corrige','Correction en vert du point F à sept cinquièmes, à droite du point E situé à quatre cinquièmes.')
add(7,'Quelle part est la plus grande ?','Les deux bandes de chaque comparaison ont la même longueur totale.\n\n[IMAGE_1]',[
 q(r'Comparer $\frac{1}{3}$ et $\frac{1}{4}$ avec les bandes.',r'$\frac{1}{3}>\frac{1}{4}$.','En partageant la même longueur en moins de morceaux, chaque morceau est plus grand. Un tiers dépasse donc un quart.'),
 q(r'Comparer $\frac{2}{3}$ et $\frac{2}{4}$.',r'$\frac{2}{3}>\frac{2}{4}$.','Chaque tiers dépasse un quart. En prenant deux de chaque, les deux tiers dépassent aussi les deux quarts.'),
 q(r'Comparer $\frac{1}{2}$ et $\frac{1}{4}$.',r'$\frac{1}{2}>\frac{1}{4}$.','Une moitié recouvre exactement deux quarts de la même unité. Elle est plus grande qu’un seul quart.'),
 q(r'Comparer $\frac{3}{8}$ et $\frac{3}{4}$.',r'$\frac{3}{8}<\frac{3}{4}$.','Un huitième est plus petit qu’un quart. En prenant trois parts de chaque, on conserve cette comparaison.'),
 q('Pourquoi faut-il utiliser des bandes unité de même longueur ?','Pour comparer des fractions du même tout.','Si les bandes entières sont de tailles différentes, la taille des morceaux dépend aussi de cette différence. On ne pourrait plus conclure seulement avec les fractions.')])
fig(7,'tiers_quarts',bands([(3,1,'Un tiers de la bande unité'),(4,1,'Un quart de la même unité')]));image(7,'nouveau-10',1,'tiers_quarts','Deux bandes de longueur identique : un tiers vert au-dessus et un quart vert au-dessous.')
add(7,'Mesurer avec une bande','La bande unité et le segment à mesurer utilisent le même pas : un quart de l’unité.\n\n[IMAGE_1]',[
 q('Combien de petits pas contient une bande unité ?',r'$4$ pas.','Le premier tracé montre une bande unité partagée en quatre intervalles égaux. Un petit pas vaut un quart.'),
 q('Combien de petits pas contient le segment ?',r'$11$ pas.','On compte tous les intervalles entre le début et la fin du segment. Il y en a onze.'),
 q('Écrire la longueur du segment avec une fraction.',r'$\frac{11}{4}$ d’unité.','Onze pas d’un quart donnent onze quarts d’unité. Le dénominateur décrit le pas choisi.'),
 q('Écrire cette longueur avec un entier et une fraction.',r'$\frac{11}{4}=2+\frac{3}{4}$.','Huit quarts font deux unités complètes. Les trois quarts restants complètent la mesure.'),
 q('Combien de quarts manquent pour atteindre trois unités ?',r'$1$ quart.','Trois unités font douze quarts. Le segment en contient onze : un quart supplémentaire suffit.')])
fig(7,'mesure_quarts',r'''\begin{tikzpicture}[x=.55cm,y=1cm]
\draw[otNavy,line width=.8pt] (0,0)--(4,0);
\draw[otNavy,line width=.8pt] (0,-1.3)--(11,-1.3);
\foreach \i in {0,...,4}{\draw[otNavy,line width=.6pt] (\i,-.08)--(\i,.08);}
\foreach \i in {0,...,11}{\draw[otNavy,line width=.6pt] (\i,-1.38)--(\i,-1.22);}
\node[above=8pt,text=otInk] at (2,0) {Bande unité};
\node[below=8pt,text=otInk] at (5.5,-1.3) {Segment à mesurer};
\end{tikzpicture}''');image(7,'nouveau-11',1,'mesure_quarts','Bande unité longue de quatre petits pas et segment à mesurer long de onze pas exactement identiques.')
add(7,'La randonnée','Un sentier mesure vingt kilomètres. Le groupe parcourt le quart du sentier le matin.',[
 q('En combien de groupes égaux partage-t-on la longueur ?',r'$4$ groupes.','Un quart correspond à un groupe parmi quatre de même longueur. Les quatre groupes doivent couvrir les vingt kilomètres.'),
 q('Quelle distance est parcourue le matin ?',r'$5$ km.',r'On calcule un quart de vingt : $20\div4=5$. Le matin correspond à un seul groupe.'),
 q('Quelle distance reste-t-il pour l’après-midi ?',r'$15$ km.',r'On retire la distance du matin à la longueur totale : $20-5=15$.'),
 q('Quelle fraction du sentier reste-t-il à parcourir ?',r'$\frac{3}{4}$.','Sur les quatre quarts du sentier, un a été parcouru. Les trois autres restent pour l’après-midi.'),
 q('Vérifier que les deux distances reconstituent le sentier.',r'$5+15=20$ km.','La somme des distances du matin et de l’après-midi doit retrouver la distance totale. On obtient bien vingt kilomètres.')])
add(7,'Sept parts de deux tartes','Deux tartes identiques sont coupées en sixièmes. Sept parts sont mangées.',[
 q('Écrire la quantité initiale avec le dénominateur 6.',r'$2=\frac{12}{6}$.','Chaque tarte contient six sixièmes. Deux tartes en contiennent douze.'),
 q('Écrire la quantité mangée en fraction de tarte.',r'$\frac{7}{6}$.','L’unité est une tarte. Chaque part représente un sixième de cette unité.'),
 q('Écrire la quantité restante comme une soustraction.',r'$\frac{12}{6}-\frac{7}{6}=\frac{5}{6}$.','On retire les sept parts mangées des douze parts initiales. Les parts gardent toutes la même taille.'),
 q('Reste-t-il plus ou moins d’une tarte ?',r'Moins : $\frac{5}{6}<1$.','Une tarte complète contient six sixièmes. Il ne reste que cinq de ces parts.'),
 q('Si une part supplémentaire est mangée, quelle fraction reste-t-il ?',r'$\frac{5}{6}-\frac{1}{6}=\frac{4}{6}$.','On enlève encore un sixième. Les cinq parts restantes deviennent quatre parts.')])
add(7,'La même longueur ?','Lila prend la moitié d’une bande. Noa prend deux quarts d’une bande unité identique.\n\n[IMAGE_1]',[
 q('Écrire la fraction choisie par Lila.',r'$\frac{1}{2}$.','La bande de Lila est partagée en deux parties égales. Elle prend l’une de ces deux parties.'),
 q('Écrire la fraction choisie par Noa.',r'$\frac{2}{4}$.','Noa utilise un partage en quatre parts égales. Il en prend deux.'),
 q('Ont-ils choisi la même longueur ?',r'Oui : $\frac{1}{2}=\frac{2}{4}$.','Les portions vertes se superposent exactement. Deux quarts forment une moitié de la même bande.'),
 q(r'Compléter $\frac{1}{2}=\frac{\square}{8}$.',r'$\frac{1}{2}=\frac{4}{8}$.','Une unité est composée de huit huitièmes. La moitié de ces huit parts correspond à quatre parts.'),
 q(r'Comparer $\frac{3}{4}$ et $\frac{1}{2}$.',r'$\frac{3}{4}>\frac{1}{2}$.','On remplace la moitié par deux quarts. Trois quarts sont plus que deux quarts.')])
fig(7,'moitie_quarts',bands([(2,1,'Une moitié'),(4,2,'Deux quarts')]));image(7,'nouveau-14',1,'moitie_quarts','Deux bandes unité identiques : une moitié verte et deux quarts verts couvrent exactement la même longueur.')
add(7,'Le ruban partagé','Un ruban de dix-huit mètres est partagé. Ana reçoit la moitié, Bilal le tiers, Chloé le reste.',[
 q('Quelle longueur reçoit Ana ?',r'$9$ m.',r'La moitié s’obtient en partageant en deux : $18\div2=9$.'),
 q('Quelle longueur reçoit Bilal ?',r'$6$ m.',r'Le tiers s’obtient en partageant en trois : $18\div3=6$.'),
 q('Quelle longueur reçoivent Ana et Bilal ensemble ?',r'$15$ m.',r'On additionne les deux longueurs obtenues : $9+6=15$.'),
 q('Quelle longueur reçoit Chloé ?',r'$3$ m.',r'On retire les quinze mètres déjà attribués : $18-15=3$.'),
 q('Vérifier le partage complet.',r'$9+6+3=18$ m.','Les trois morceaux doivent retrouver les dix-huit mètres du ruban de départ. La somme confirme qu’aucune longueur n’est perdue.')])

s=init(8)
add(8,'Des dixièmes à lire','Dix parts égales forment une unité.',[
 q(r'Lire $\frac{7}{10}$ en lettres.','Sept dixièmes.','Le dénominateur 10 donne le nom « dixièmes ». Le numérateur indique sept parts.'),
 q(r'Lire $\frac{23}{10}$ en lettres.','Vingt-trois dixièmes.','On lit d’abord le nombre de parts, vingt-trois. Puis on nomme leur taille : des dixièmes.'),
 q(r'Décomposer $\frac{23}{10}$ en un entier et une fraction.',r'$\frac{23}{10}=2+\frac{3}{10}$.','Vingt dixièmes font deux unités. Il reste trois dixièmes.'),
 q(r'Écrire $\frac{23}{10}$ avec une virgule.',r'$\frac{23}{10}=2{,}3$.','Le nombre contient deux unités et trois dixièmes. Le 3 est le premier chiffre après la virgule.'),
 q('Écrire « trente-six dixièmes » comme un entier et une fraction.',r'$\frac{36}{10}=3+\frac{6}{10}$.','Trente dixièmes forment trois unités. Les six dixièmes restants donnent la partie fractionnaire.')])
add(8,'Sur la demi-droite','L’intervalle entre deux entiers est partagé en dix parties égales.\n\n[IMAGE_1]',[
 q('Quelle fraction représente un petit pas ?',r'$\frac{1}{10}$.','Dix pas égaux permettent d’avancer d’une unité. Chacun vaut donc un dixième.'),
 q('Lire la fraction du point A.',r'$\frac{24}{10}$.','Le point A se trouve quatre pas après deux unités. Deux unités font vingt dixièmes, puis on ajoute quatre dixièmes.'),
 q('Lire la fraction du point B.',r'$\frac{28}{10}$.','Le point B se trouve huit pas après deux unités. Vingt dixièmes plus huit dixièmes donnent vingt-huit dixièmes.'),
 q('Écrire le nombre de A avec une virgule.',r'$\frac{24}{10}=2{,}4$.','Le nombre contient deux unités et quatre dixièmes. Ces chiffres se placent de part et d’autre de la virgule.'),
 q('Quelle fraction d’unité sépare A et B ?',r'$\frac{28}{10}-\frac{24}{10}=\frac{4}{10}$.','On compte quatre petits intervalles entre A et B. Chacun vaut un dixième.')])
fig(8,'dixiemes',line('2','3',10,[('A',4),('B',8)]));image(8,'nouveau-2',1,'dixiemes','Demi-droite de deux à trois divisée en dix intervalles, A au quatrième et B au huitième pas après deux.')
add(8,'Unités, dixièmes, centièmes','Chaque dixième peut être partagé en dix centièmes.',[
 q(r'Compléter $1=\frac{\square}{100}$.',r'$1=\frac{100}{100}$.','Une unité contient cent centièmes. On prend les cent parts pour retrouver l’unité.'),
 q(r'Compléter $\frac{3}{10}=\frac{\square}{100}$.',r'$\frac{3}{10}=\frac{30}{100}$.','Un dixième contient dix centièmes. Trois dixièmes contiennent donc trente centièmes.'),
 q(r'Compléter $\frac{50}{100}=\frac{\square}{10}$.',r'$\frac{50}{100}=\frac{5}{10}$.','On regroupe les cinquante centièmes par paquets de dix. Cinq paquets font cinq dixièmes.'),
 q('Combien de centièmes contiennent deux unités et un dixième ?',r'$210$ centièmes.',r'Deux unités font deux cents centièmes. Un dixième en apporte dix : $200+10=210$.'),
 q(r'Comparer $\frac{6}{10}$ et $\frac{59}{100}$.',r'$\frac{6}{10}>\frac{59}{100}$.','Six dixièmes font soixante centièmes. Soixante centièmes dépassent cinquante-neuf centièmes.')])
add(8,'Vers la virgule','Placer chaque chiffre au bon rang.',[
 q(r'Écrire avec une virgule $35+\frac{7}{10}+\frac{8}{100}$.',r'$35+\frac{7}{10}+\frac{8}{100}=35{,}78$.','Les unités forment 35, le rang des dixièmes reçoit 7 et celui des centièmes reçoit 8.'),
 q(r'Écrire avec une virgule $\frac{4}{10}+\frac{2}{100}$.',r'$\frac{4}{10}+\frac{2}{100}=0{,}42$.','Il n’y a pas d’unité entière. On écrit zéro avant la virgule, puis quatre dixièmes et deux centièmes.'),
 q(r'Écrire avec une virgule $6+\frac{9}{100}$.',r'$6+\frac{9}{100}=6{,}09$.','Le rang des dixièmes est vide. Le zéro garde cette place avant les neuf centièmes.'),
 q(r'Écrire avec une virgule $2+\frac{5}{10}$.',r'$2+\frac{5}{10}=2{,}5$.','Le nombre contient deux unités et cinq dixièmes. On peut aussi écrire 2,50, car le centième est nul.'),
 q(r'Quel chiffre est au rang des centièmes dans $35{,}78$ ?',r'$8$.','Le premier chiffre après la virgule est celui des dixièmes. Le deuxième, 8, est celui des centièmes.')])
add(8,'Depuis la virgule','Écrire des sommes d’unités et de fractions décimales.',[
 q(r'Décomposer $6{,}09$.',r'$6{,}09=6+\frac{9}{100}$.','Six unités sont suivies de zéro dixième et neuf centièmes. Le terme nul des dixièmes peut être omis.'),
 q(r'Décomposer $14{,}3$.',r'$14{,}3=14+\frac{3}{10}$.','La partie entière vaut quatorze. Le chiffre 3 occupe le rang des dixièmes.'),
 q(r'Décomposer $8{,}47$.',r'$8{,}47=8+\frac{4}{10}+\frac{7}{100}$.','On lit successivement huit unités, quatre dixièmes et sept centièmes. Chaque rang donne un terme de la somme.'),
 q(r'Écrire $6{,}09$ avec une seule fraction décimale.',r'$6{,}09=\frac{609}{100}$.','Six unités contiennent six cents centièmes. Avec les neuf centièmes restants, on obtient six cent neuf centièmes.'),
 q(r'Pourquoi $6{,}09$ n’est-il pas égal à $6+\frac{9}{10}$ ?',r'$6{,}09\ne6{,}9$.','Dans 6,09, le 9 représente des centièmes. Le déplacer juste après la virgule le transforme en dixièmes et change sa valeur.')])
add(8,'Fractions en virgule','Les dénominateurs 10 et 100 indiquent le rang de la dernière part.',[
 q(r'Écrire $\frac{45}{10}$ avec une virgule.',r'$\frac{45}{10}=4{,}5$.','Quarante dixièmes font quatre unités. Il reste cinq dixièmes.'),
 q(r'Écrire $\frac{307}{100}$ avec une virgule.',r'$\frac{307}{100}=3{,}07$.','Trois cents centièmes font trois unités. Il reste sept centièmes et aucun dixième supplémentaire.'),
 q(r'Écrire $\frac{8}{100}$ avec une virgule.',r'$\frac{8}{100}=0{,}08$.','Il n’y a ni unité entière ni dixième entier. Deux zéros sont nécessaires pour placer le 8 au rang des centièmes.'),
 q(r'Écrire $\frac{120}{100}$ avec une virgule.',r'$\frac{120}{100}=1{,}2$.','Cent centièmes donnent une unité. Vingt centièmes donnent deux dixièmes, donc 1,20 peut s’écrire 1,2.'),
 q(r'Comparer $\frac{8}{100}$ et $\frac{8}{10}$.',r'$\frac{8}{100}<\frac{8}{10}$.','Huit dixièmes font quatre-vingts centièmes. Huit centièmes sont inférieurs à quatre-vingts centièmes.')])
add(8,'Le rang de chaque chiffre',r'On étudie $58{,}36$.',[
 q('Donner le chiffre des dixièmes.',r'$3$.','Les dixièmes sont au premier rang à droite de la virgule. On lit donc le chiffre 3.'),
 q('Donner le chiffre des centièmes.',r'$6$.','Les centièmes sont au deuxième rang à droite de la virgule. Ce rang contient 6.'),
 q('Donner la valeur du chiffre 3.',r'$\frac{3}{10}=0{,}3$.','Le chiffre 3 compte des dixièmes et non des unités. Sa contribution est trois dixièmes.'),
 q('Donner la partie entière.',r'$58$.','La partie entière est écrite à gauche de la virgule. Elle compte cinquante-huit unités complètes.'),
 q('Décomposer le nombre en unités, dixièmes et centièmes.',r'$58{,}36=58+\frac{3}{10}+\frac{6}{100}$.','On écrit un terme pour chaque rang. Les dizaines et unités simples peuvent être réunies dans la partie entière 58.')])
add(8,'Deux écritures, un nombre','Traduire sans changer la valeur.',[
 q('Écrire « quatre unités et sept centièmes » avec une virgule.',r'$4{,}07$.','Les sept parts sont des centièmes. Le rang des dixièmes reste zéro.'),
 q('Écrire le même nombre avec une fraction décimale.',r'$4{,}07=\frac{407}{100}$.','Quatre unités font quatre cents centièmes. On ajoute encore sept centièmes.'),
 q('Écrire « douze dixièmes » avec une virgule.',r'$\frac{12}{10}=1{,}2$.','Dix dixièmes forment une unité. Les deux dixièmes supplémentaires donnent la partie décimale.'),
 q('Écrire « deux unités et cinq centièmes » avec une fraction décimale.',r'$2+\frac{5}{100}=\frac{205}{100}$.','Deux unités donnent deux cents centièmes. Les cinq centièmes s’y ajoutent pour en former deux cent cinq.'),
 q('Écrire « trente centièmes » avec le dénominateur 10.',r'$\frac{30}{100}=\frac{3}{10}$.','Dix centièmes forment un dixième. Trente centièmes font trois paquets de dix centièmes.')])
add(8,'Avec la monnaie','Un centime représente un centième d’euro.',[
 q('Écrire trois euros et quarante-cinq centimes en euros.',r'$3{,}45$ euros.','Trois euros forment la partie entière. Quarante-cinq centimes sont quarante-cinq centièmes d’euro.'),
 q('Écrire 275 centimes en euros.',r'$2{,}75$ euros.',r'Deux cents centimes font deux euros. Les soixante-quinze restants donnent $\frac{75}{100}$ d’euro.'),
 q('Écrire huit centimes en euros.',r'$0{,}08$ euro.','Huit centimes ne font pas un dixième d’euro entier. Le 8 se place au deuxième rang après la virgule.'),
 q(r'Combien de centimes représentent $4{,}30$ euros ?',r'$430$ centimes.',r'Quatre euros représentent quatre cents centimes. On ajoute les trente centimes : $400+30=430$.'),
 q('Un prix de 3 euros et 5 centimes s’écrit-il 3,5 euros ?',r'Non : il s’écrit $3{,}05$ euros.','3,5 euros désigne trois euros et cinquante centimes. Le zéro des dixièmes est indispensable pour coder seulement cinq centimes.')])
add(8,'Des zéros qui comptent','Les rangs ne changent pas de place lorsque l’on écrit un nombre.',[
 q('Écrire cinq centièmes avec une virgule.',r'$\frac{5}{100}=0{,}05$.','Le 5 est au rang des centièmes. Le zéro des dixièmes empêche de le confondre avec cinq dixièmes.'),
 q('Écrire cinq dixièmes avec une virgule.',r'$\frac{5}{10}=0{,}5$.','Les dixièmes sont au premier rang après la virgule. On y place directement le chiffre 5.'),
 q('Ces deux nombres sont-ils égaux ?',r'Non : $0{,}05<0{,}5$.','Cinq dixièmes correspondent à cinquante centièmes. Cinq centièmes sont beaucoup plus petits.'),
 q(r'Écrire $0{,}5$ avec le dénominateur 100.',r'$0{,}5=\frac{50}{100}$.','Chaque dixième vaut dix centièmes. Les cinq dixièmes donnent cinquante centièmes.'),
 q(r'Peut-on supprimer le zéro final de $2{,}30$ ?',r'Oui : $2{,}30=2{,}3$.','Le zéro final indique zéro centième supplémentaire. L’enlever laisse les autres chiffres à leur rang et conserve la valeur.')])
add(8,'La grille aux cent cases','La grille unité contient cent cases égales, dont trente-sept sont vertes.\n\n[IMAGE_1]',[
 q('Écrire la fraction colorée.',r'$\frac{37}{100}$.','L’unité contient cent cases de même aire. Trente-sept d’entre elles sont colorées.'),
 q('Écrire ce nombre avec une virgule.',r'$\frac{37}{100}=0{,}37$.','Trente-sept centièmes contiennent trois dixièmes et sept centièmes. Il n’y a pas d’unité entière.'),
 q('Si on colore trois cases de plus, quelle fraction est colorée ?',r'$\frac{40}{100}$.',r'Le nombre de cases colorées devient $37+3=40$. Le total reste cent cases.'),
 q('Écrire cette nouvelle fraction avec une virgule et avec des dixièmes.',r'$\frac{40}{100}=0{,}4=\frac{4}{10}$.','Quarante centièmes se regroupent en quatre paquets de dix centièmes. Chaque paquet vaut un dixième.'),
 q('Après cet ajout, combien de cases restent blanches ?',r'$60$ cases.',r'Quarante cases sur cent sont vertes. Il reste $100-40=60$ cases blanches.')])
grid=[r'\begin{tikzpicture}[x=.55cm,y=.55cm]']
for k in range(37):
    x=k//10;y=9-k%10;grid.append(fr'\fill[otGreen!30] ({x},{y}) rectangle ({x+1},{y+1});')
grid.extend([r'\draw[step=1,otNavy,line width=.45pt] (0,0) grid (10,10);',r'\draw[otNavy,line width=.8pt] (0,0) rectangle (10,10);',r'\end{tikzpicture}'])
fig(8,'grille_37','\n'.join(grid));image(8,'nouveau-11',1,'grille_37','Grille de cent cases égales avec trois colonnes entières vertes et sept cases vertes dans la quatrième colonne.')
add(8,'Le compteur en dixièmes',r'Un compteur affiche $45{,}8$. Il augmente d’un dixième à chaque pas.',[
 q('Quel nombre affiche-t-il après un pas ?',r'$45{,}9$.','Huit dixièmes plus un dixième donnent neuf dixièmes. La partie entière reste 45.'),
 q('Quel nombre affiche-t-il après deux pas ?',r'$46$.','Le dixième suivant complète dix dixièmes. Dix dixièmes s’échangent contre une unité : on passe à 46.'),
 q('Quel nombre affiche-t-il après trois pas ?',r'$46{,}1$.','Après 46, on ajoute encore un dixième. Le rang des dixièmes devient 1.'),
 q('Quel nombre affichait-il un pas avant 45,8 ?',r'$45{,}7$.','On retire un dixième à huit dixièmes. Les unités restent inchangées.'),
 q('Pourquoi 45,10 n’est-il pas l’affichage après 45,9 ?',r'$45{,}10=45{,}1$, alors que le suivant est $46$.','Les chiffres après la virgule occupent des rangs, ils ne forment pas un compteur d’entiers séparé. Le passage de neuf à dix dixièmes crée une unité.')])
add(8,'Les sauts mesurés',r'Trois sauts mesurent $3{,}45$ m, $3{,}5$ m et $3{,}09$ m.',[
 q(r'Décomposer $3{,}45$ avec des fractions décimales.',r'$3{,}45=3+\frac{4}{10}+\frac{5}{100}$.','La partie entière vaut trois mètres. Les deux chiffres suivants valent quatre dixièmes et cinq centièmes de mètre.'),
 q(r'Décomposer $3{,}5$.',r'$3{,}5=3+\frac{5}{10}$.','Il y a trois unités et cinq dixièmes. Aucun centième supplémentaire n’est écrit.'),
 q(r'Décomposer $3{,}09$.',r'$3{,}09=3+\frac{9}{100}$.','Le zéro montre qu’il n’y a pas de dixième supplémentaire. Le 9 est au rang des centièmes.'),
 q('Donner les chiffres des dixièmes dans l’ordre des trois sauts.',r'$4$, $5$ et $0$.','On lit le premier chiffre à droite de la virgule de chaque nombre. Le zéro du troisième nombre compte lui aussi comme un chiffre.'),
 q('Écrire les trois longueurs en centièmes de mètre.',r'$345$, $350$ et $309$ centièmes de mètre.','Trois mètres donnent trois cents centièmes. On ajoute respectivement quarante-cinq, cinquante et neuf centièmes.')])
add(8,'Fractions bien connues','Utiliser le même partage en centièmes pour reconnaître des fractions usuelles.',[
 q(r'Écrire $\frac{1}{2}$ en centièmes.',r'$\frac{1}{2}=\frac{50}{100}$.','La moitié de cent parts représente cinquante parts. Les deux fractions couvrent la même portion de l’unité.'),
 q(r'Écrire $\frac{1}{4}$ en centièmes.',r'$\frac{1}{4}=\frac{25}{100}$.','On partage cent cases en quatre groupes égaux. Un groupe contient vingt-cinq cases.'),
 q(r'Écrire $\frac{3}{4}$ en centièmes.',r'$\frac{3}{4}=\frac{75}{100}$.','Chaque quart représente vingt-cinq centièmes. Trois quarts représentent soixante-quinze centièmes.'),
 q('Écrire ces trois fractions avec une virgule, dans le même ordre.',r'$0{,}5$ ; $0{,}25$ ; $0{,}75$.','Cinquante centièmes s’écrivent 0,50 ou 0,5. Vingt-cinq centièmes et soixante-quinze centièmes s’écrivent sur deux rangs.'),
 q(r'Compléter $\frac{1}{4}+\frac{3}{4}$ et donner une écriture à virgule du résultat.',r'$\frac{1}{4}+\frac{3}{4}=1$.','Les quatre quarts reconstituent une unité. En centièmes, vingt-cinq plus soixante-quinze donnent cent centièmes.')])
add(8,'Vrai ou faux ?',r'Milo dit : « $0{,}7$ représente sept centièmes. » Sara dit : « $2{,}30$ et $2{,}3$ sont égaux. »',[
 q('Milo a-t-il raison ?',r'Non : $0{,}7=\frac{7}{10}$.','Le 7 est au premier rang après la virgule. Il indique des dixièmes et non des centièmes.'),
 q(r'Combien de centièmes représente $0{,}7$ ?',r'$70$ centièmes.','Un dixième contient dix centièmes. Sept dixièmes en contiennent donc soixante-dix.'),
 q('Sara a-t-elle raison ?',r'Oui : $2{,}30=2{,}3$.','Trente centièmes valent trois dixièmes. Les deux nombres ont donc deux unités et trois dixièmes.'),
 q(r'Écrire $2{,}30$ avec le dénominateur 100.',r'$2{,}30=\frac{230}{100}$.','Deux unités valent deux cents centièmes. On y ajoute trente centièmes.'),
 q(r'$2{,}03$ est-il également égal à $2{,}3$ ?',r'Non : $2{,}03<2{,}3$.','Le zéro de 2,03 garde le rang des dixièmes vide. Les trois centièmes sont inférieurs aux trois dixièmes de 2,3.')])

s=init(1)
add(1,'Écrire en chiffres','Construire chaque nombre en gardant la place des rangs vides.',[
 q('Écrire « huit-mille-quarante » en chiffres.',r'$8\,040$.',r'On place 8 dans la classe des mille et 040 dans celle des unités. Le zéro conserve la place des centaines.'),
 q('Écrire « vingt-trois-mille-quatre-cent-cinq » en chiffres.',r'$23\,405$.','La classe des mille est 23. La classe des unités est 405 : le rang des dizaines est vide.'),
 q('Écrire « six-cent-mille-neuf » en chiffres.',r'$600\,009$.','On écrit 600 pour les milliers, puis 009 pour les unités simples. Écrire 6009 ferait perdre deux rangs.'),
 q('Écrire « quatre-vingt-mille-soixante » en chiffres.',r'$80\,060$.','Quatre-vingt mille se code 80 dans la classe des mille. Soixante se code 060 dans la classe suivante.'),
 q('Un élève écrit 804 pour « huit-mille-quarante ». Expliquer et corriger.',r'Il faut écrire $8\,040$.','804 désigne huit centaines et quatre unités. Le nombre demandé contient huit milliers et quatre dizaines, donc deux zéros sont nécessaires.')])
add(1,'Lire en classes','On sépare les classes de trois chiffres avant de lire.',[
 q(r'Écrire $86\,312$ en lettres.','Quatre-vingt-six-mille-trois-cent-douze.','On lit 86 dans la classe des mille, puis 312 dans la classe des unités.'),
 q(r'Écrire $450\,070$ en lettres.','Quatre-cent-cinquante-mille-soixante-dix.','Le groupe 450 se lit avant le mot mille. Le groupe 070 vaut soixante-dix ; les zéros ne se prononcent pas.'),
 q(r'Dans $450\,070$, que représente le groupe 450 ?',r'$450$ milliers.','Le groupe placé à gauche de l’espace appartient à la classe des mille. Il compte les milliers entiers du nombre.'),
 q(r'Dans $86\,312$, quelle est la classe des unités simples ?',r'$312$.','On prend les trois chiffres de droite. Ils représentent trois centaines, une dizaine et deux unités.'),
 q(r'Écrire en chiffres « quatre-cent-cinquante-mille-sept ».',r'$450\,007$.','Le dernier groupe est 007 et non 070. Sept unités ne sont pas sept dizaines.')])
add(1,'La valeur d’un chiffre',r'On étudie le nombre $582\,741$.',[
 q('Donner son chiffre des unités de mille.',r'$2$.','En partant de la droite, on lit unités, dizaines, centaines, puis unités de mille. Le quatrième chiffre est 2.'),
 q('Donner la valeur du chiffre 8.',r'$80\,000$.',r'Le 8 est au rang des dizaines de mille. Sa contribution est $8\times10\,000=80\,000$.'),
 q('Donner son chiffre des centaines.',r'$7$.','Les trois derniers chiffres sont 741. Le 7 compte les centaines de la classe des unités.'),
 q('Quelle valeur prendrait le 8 au rang des centaines ?',r'$800$.',r'Au rang des centaines, chaque unité du chiffre vaut 100. Ainsi $8\times100=800$.'),
 q('Donner le nombre entier de milliers contenus dans ce nombre.',r'$582$ milliers.',r'On regroupe les unités par paquets de mille : $582\,741=582\times1\,000+741$. Il y a 582 paquets complets.')])
add(1,'Chiffre et nombre de dizaines',r'On considère $4\,627$ objets à ranger.',[
 q('Quel est le chiffre des dizaines ?',r'$2$.','Le chiffre des dizaines est le deuxième en partant de la droite. Il indique deux dizaines dans la décomposition par rangs.'),
 q('Combien de paquets complets de dix objets peut-on faire ?',r'$462$ paquets.',r'On prend toutes les dizaines, y compris celles contenues dans les centaines et les milliers : $4\,627=462\times10+7$.'),
 q('Combien d’objets restent hors des paquets ?',r'$7$ objets.',r'Les 462 paquets contiennent $462\times10=4\,620$ objets. Il reste $4\,627-4\,620=7$ objets.'),
 q('Quel est le chiffre des centaines ?',r'$6$.','On repère le troisième chiffre depuis la droite. Ce chiffre seul n’est pas le nombre de centaines.'),
 q('Combien de centaines entières contient le nombre ?',r'$46$ centaines.',r'On peut faire 46 groupes de 100 : $4\,627=46\times100+27$. Les 27 derniers objets ne forment pas une centaine.')])
add(1,'Comparer deux nombres','Compléter chaque comparaison et justifier le premier rang qui décide.',[
 q(r'Comparer $45\,806$ et $45\,860$.',r'$45\,806<45\,860$.','Les chiffres sont identiques jusqu’aux centaines. Aux dizaines, 0 est plus petit que 6.'),
 q(r'Comparer $9\,875$ et $12\,034$.',r'$9\,875<12\,034$.','Le premier entier a quatre chiffres et le second cinq. Tout entier à quatre chiffres est inférieur à un entier à cinq chiffres.'),
 q(r'Comparer $304\,065$ et $304\,056$.',r'$304\,065>304\,056$.','Le premier rang différent est celui des dizaines : 6 est plus grand que 5. Les unités ne changent plus la comparaison.'),
 q(r'Comparer $90\,999$ et $100\,000$.',r'$90\,999<100\,000$.','Un nombre de cinq chiffres est inférieur à un nombre de six chiffres. Il ne suffit pas de comparer les premiers chiffres 9 et 1.'),
 q(r'Comparer $52\,700$ et $52\,700$.',r'$52\,700=52\,700$.','Tous les chiffres sont égaux et occupent les mêmes rangs. Les deux écritures désignent le même nombre.')])
add(1,'Décomposer',r'On décompose le nombre $304\,065$.',[
 q('Écrire sa décomposition avec les valeurs des chiffres non nuls.',r'$304\,065=3\times100\,000+4\times1\,000+6\times10+5$.','Chaque chiffre non nul est multiplié par la valeur de son rang. On ne met pas de terme pour les dizaines de mille ni pour les centaines.'),
 q('Quelle contribution apporte le chiffre 3 ?',r'$300\,000$.',r'Le 3 compte les centaines de mille : $3\times100\,000=300\,000$.'),
 q('Quelle contribution apporte le chiffre 4 ?',r'$4\,000$.',r'Le 4 compte les milliers : $4\times1\,000=4\,000$.'),
 q('Écrire ce nombre comme somme de milliers et d’unités simples.',r'$304\,065=304\times1\,000+65$.','La classe des mille vaut 304 milliers. La classe 065 apporte encore 65 unités.'),
 q('Pourquoi ne peut-on pas effacer les deux zéros intérieurs ?',r'$304\,065\ne3\,465$.','Les zéros gardent les rangs sans unités. Les enlever déplace les autres chiffres et change leur valeur.')])
add(1,'Recomposer','Écrire le nombre correspondant à chaque décomposition.',[
 q(r'$7\times10\,000+3\times100+9$.',r'$70\,309$.','On place 7 aux dizaines de mille, 3 aux centaines et 9 aux unités. Les autres rangs reçoivent un zéro.'),
 q(r'$5\times100\,000+2\times10$.',r'$500\,020$.','Le nombre contient cinq centaines de mille et deux dizaines. On remplit les rangs restants avec des zéros.'),
 q(r'$8\times1\,000+4\times10+6$.',r'$8\,046$.','Les huit milliers sont suivis de 046. Le rang des centaines est vide.'),
 q(r'$62\times1\,000+7$.',r'$62\,007$.','Le nombre contient 62 milliers et 7 unités simples. Le dernier groupe s’écrit sur trois chiffres : 007.'),
 q(r'$9\times10\,000+12\times100$.',r'$91\,200$.',r'Douze centaines font $12\times100=1\,200$. On ajoute ensuite $90\,000+1\,200=91\,200$.')])
add(1,'Sur la demi-droite','La droite est graduée régulièrement. Lire les nombres sans se fier à la longueur apparente des étiquettes.\n\n[IMAGE_1]',[
 q('Quelle est la valeur d’un petit intervalle ?',r'$500$.',r'Entre $24\,000$ et $28\,000$, il y a huit intervalles. Comme $8\times500=4\,000$, chaque pas vaut 500.'),
 q('Lire le nombre du point A.',r'$25\,000$.',r'A est à deux pas de $24\,000$ : $24\,000+2\times500=25\,000$.'),
 q('Lire le nombre du point B.',r'$26\,500$.',r'B est à cinq pas de $24\,000$ : $24\,000+5\times500=26\,500$.'),
 q('Lire le nombre du point C.',r'$27\,500$.',r'C est à sept pas de $24\,000$ : $24\,000+7\times500=27\,500$.'),
 q(r'Où placer un point D de nombre $27\,000$ ?',r'À la sixième graduation après $24\,000$, entre B et C.',r'Il faut avancer de $3\,000$ depuis le début. Six pas de 500 donnent $6\times500=3\,000$.')])
fig(1,'graduation',line(r'24\,000',r'28\,000',8,[('A',2),('B',5),('C',7)]));image(1,'nouveau-8',1,'graduation',r'Demi-droite de 24 000 à 28 000 en huit intervalles, A au deuxième, B au cinquième et C au septième pas.')
add(1,'Encadrer','Les deux bornes doivent être des multiples consécutifs du rang demandé.',[
 q(r'Encadrer $45\,670$ entre deux dizaines de mille consécutives.',r'$40\,000<45\,670<50\,000$.','Les deux multiples de 10 000 voisins sont 40 000 et 50 000. Le nombre demandé est strictement entre eux.'),
 q(r'Encadrer $8\,294$ entre deux centaines consécutives.',r'$8\,200<8\,294<8\,300$.','La centaine inférieure est 8 200. La suivante est 8 300, et non 8 400.'),
 q(r'Encadrer $45\,670$ entre deux milliers consécutifs.',r'$45\,000<45\,670<46\,000$.','On conserve les milliers entiers pour la borne inférieure. On ajoute un millier pour la borne supérieure.'),
 q(r'Encadrer $8\,294$ entre deux dizaines consécutives.',r'$8\,290<8\,294<8\,300$.','Les dizaines qui entourent le nombre finissent par zéro. Elles diffèrent exactement de 10.'),
 q(r'Intercaler un entier entre $23\,500$ et $23\,600$.',r'Par exemple $23\,540$ : $23\,500<23\,540<23\,600$.','On choisit un entier strictement plus grand que la borne de gauche et plus petit que celle de droite. Plusieurs réponses sont possibles.')])
add(1,'Ranger des nombres',r'On dispose des nombres $56\,040$, $9\,980$, $56\,400$, $100\,000$ et $55\,999$.',[
 q('Quel est le plus petit ?',r'$9\,980$.','C’est le seul nombre de quatre chiffres. Les autres ont cinq ou six chiffres.'),
 q('Quel est le plus grand ?',r'$100\,000$.','C’est le seul nombre de six chiffres. Il est supérieur aux quatre autres.'),
 q('Ranger les cinq nombres dans l’ordre croissant.',r'$9\,980<55\,999<56\,040<56\,400<100\,000$.','Entre les trois nombres à cinq chiffres, on compare d’abord les milliers puis les centaines. 55 milliers précèdent 56 milliers ; 040 est inférieur à 400.'),
 q('Ranger les trois nombres à cinq chiffres dans l’ordre décroissant.',r'$56\,400>56\,040>55\,999$.','On reprend les trois nombres concernés et on inverse leur ordre croissant. Les signes doivent tous indiquer « supérieur à ».'),
 q(r'Quel nombre de la liste est juste inférieur à $56\,040$ ?',r'$55\,999$.','On regarde le voisin précédent dans la liste rangée. La question porte sur les nombres proposés, pas sur l’entier immédiatement précédent.')])
add(1,'Des parcours à ranger',r'Quatre parcours fictifs mesurent $1\,006$ km, $775$ km, $647$ km et $812$ km. On les nomme respectivement Loire, Seine, Garonne et Rhône.',[
 q('Donner le nom du parcours le plus court.','Garonne, avec $647$ km.','On compare les centaines des longueurs à trois chiffres. 647 est le plus petit des quatre nombres.'),
 q('Donner le nom du parcours le plus long.','Loire, avec $1\,006$ km.','La longueur à quatre chiffres est supérieure aux trois longueurs à trois chiffres.'),
 q('Ranger les quatre parcours du plus court au plus long.','Garonne, Seine, Rhône, Loire.','Les longueurs vérifient $647<775<812<1\,006$. On replace chaque nom devant sa longueur.'),
 q('Quels parcours mesurent moins de 800 km ?','Garonne et Seine.','647 et 775 sont inférieurs à 800. 812 et 1 006 dépassent ce seuil.'),
 q('Quelle longueur sépare les deux parcours les plus courts ?',r'$128$ km.',r'On soustrait les deux longueurs concernées : $775-647=128$. L’unité reste le kilomètre.')])
add(1,'Des carnets de timbres','Chaque carnet contient exactement dix timbres.',[
 q(r'Combien de carnets complets avec $3\,240$ timbres ?',r'$324$ carnets.',r'On forme des paquets de dix : $3\,240=324\times10$. La division tombe juste.'),
 q(r'Combien de carnets complets avec $5\,278$ timbres ?',r'$527$ carnets.',r'On peut utiliser $527\times10=5\,270$ timbres. Un carnet supplémentaire demanderait 5 280 timbres.'),
 q(r'Combien reste-t-il de timbres dans le deuxième cas ?',r'$8$ timbres.',r'On retire les timbres rangés : $5\,278-5\,270=8$.'),
 q('Combien de timbres manque-t-il pour compléter un carnet de plus dans le deuxième cas ?',r'$2$ timbres.',r'Le dernier groupe contient 8 timbres. Il en manque $10-8=2$ pour atteindre dix.'),
 q(r'Quel est le chiffre des dizaines de $5\,278$ et pourquoi n’est-ce pas 527 ?',r'Le chiffre est $7$ ; $527$ est le nombre de dizaines.','Un chiffre est un seul symbole de 0 à 9. Le nombre de dizaines compte tous les paquets, y compris ceux venant des milliers et centaines.')])
add(1,'Un nombre à inventer',r'Chercher des nombres strictement compris entre $45\,300$ et $45\,400$, dont le chiffre des dizaines est 7.',[
 q('Donner un exemple.',r'Par exemple $45\,370$.','Le rang des centaines doit rester 3. On place 7 aux dizaines et on choisit une unité, par exemple zéro.'),
 q('Donner le plus petit nombre possible.',r'$45\,370$.','Les quatre premiers chiffres sont fixés : 4537. La plus petite unité possible est 0.'),
 q('Donner le plus grand nombre possible.',r'$45\,379$.','On conserve les quatre premiers chiffres. La plus grande unité possible est 9.'),
 q('Combien y a-t-il de possibilités ?',r'$10$ possibilités.','Seul le chiffre des unités varie. Il peut prendre chacune des dix valeurs de 0 à 9.'),
 q(r'$45\,407$ convient-il ? Expliquer.','Non.','45 407 dépasse la borne 45 400 et son chiffre des dizaines est 0. Il ne respecte donc aucune de ces deux conditions.')])
add(1,'Avec cinq cartes','Utiliser une fois chacune les cartes 7, 0, 3, 9 et 1.',[
 q('Former le plus grand nombre à cinq chiffres.',r'$97\,310$.','On place les chiffres dans l’ordre décroissant. Les plus grands chiffres prennent ainsi les rangs les plus forts.'),
 q('Former le plus petit nombre à cinq chiffres.',r'$10\,379$.','On commence par le plus petit chiffre non nul, 1. On place ensuite les chiffres restants dans l’ordre croissant, avec 0 en deuxième position.'),
 q('Pourquoi ne peut-on pas commencer par zéro ?','Le nombre n’aurait plus cinq chiffres.','Un zéro initial ne compte pas comme un rang dans l’écriture usuelle d’un entier. 01379 désigne 1 379, qui possède quatre chiffres.'),
 q('Former le plus grand nombre pair possible.',r'$97\,310$.','Un nombre pair finit par 0, 2, 4, 6 ou 8. Seul 0 est disponible ici ; on range ensuite les autres cartes en ordre décroissant.'),
 q('Former le plus petit nombre impair possible.',r'$10\,379$.','Le plus petit nombre formé à la question 2 se termine par 9. Il est déjà impair : aucune modification n’est nécessaire.')])
add(1,'Trois communes',r'Trois communes fictives comptent $45\,806$, $45\,860$ et $9\,980$ habitants.',[
 q('Ranger les populations dans l’ordre décroissant.',r'$45\,860>45\,806>9\,980$.','Les deux nombres de cinq chiffres dépassent celui de quatre chiffres. Entre eux, le rang des dizaines départage 60 et 06 dans les deux derniers chiffres.'),
 q('Encadrer la plus grande entre deux dizaines de mille consécutives.',r'$40\,000<45\,860<50\,000$.','Les dizaines de mille voisines sont 40 000 et 50 000. Le nombre se trouve dans cet intervalle.'),
 q('Donner le chiffre des centaines de la plus grande population.',r'$8$.','Dans les trois derniers chiffres 860, le 8 est au rang des centaines.'),
 q('Combien d’habitants séparent les deux communes les plus peuplées ?',r'$54$ habitants.',r'On calcule la différence : $45\,860-45\,806=54$. Les classes des mille s’annulent.'),
 q(r'Combien manque-t-il à la plus petite commune pour atteindre $10\,000$ habitants ?',r'$20$ habitants.',r'On cherche le complément : $10\,000-9\,980=20$. On vérifie $9\,980+20=10\,000$.')])

s=init(6)
add(6,'Lire une part','Le disque entier est l’unité.\n\n[IMAGE_1]',[
 q('En combien de parts égales le disque est-il partagé ?',r'$8$ parts.','On compte les huit secteurs de même taille. Ils couvrent tout le disque sans se chevaucher.'),
 q('Combien de parts sont colorées ?',r'$3$ parts.','On compte seulement les secteurs verts. Il y en a trois.'),
 q('Écrire la fraction colorée.',r'$\frac{3}{8}$.','Le dénominateur 8 décrit le partage de l’unité. Le numérateur 3 compte les parts colorées.'),
 q('Écrire la fraction non colorée.',r'$\frac{5}{8}$.',r'Il reste $8-3=5$ parts non colorées sur les huit parts égales.'),
 q('La partie colorée est-elle plus petite qu’une moitié ?',r'Oui : $\frac{3}{8}<\frac{4}{8}=\frac{1}{2}$.','La moitié du disque correspond à quatre huitièmes. Trois huitièmes couvrent moins que quatre huitièmes.')])
fig(6,'disque_huitiemes',disk(8,3));image(6,'nouveau-1',1,'disque_huitiemes','Disque partagé en huit secteurs égaux, dont trois secteurs consécutifs sont colorés en vert.')
add(6,'Colorier une fraction','La bande entière est l’unité.\n\n[IMAGE_1]',[
 q(r'Reproduire et colorier $\frac{2}{5}$ de la bande.',r'Colorier $2$ cases sur $5$.','Le dénominateur impose cinq cases égales. Le numérateur indique que deux de ces cases doivent être colorées.'),
 q('Quelle fraction représente une case ?',r'$\frac{1}{5}$.','Chaque case est une des cinq parts égales de l’unité. Elle vaut un cinquième de la bande.'),
 q('Quelle fraction reste blanche après ce coloriage ?',r'$\frac{3}{5}$.',r'Il reste $5-2=3$ cases blanches. Le partage est toujours en cinquièmes.'),
 q('Pour colorier la bande entière, combien de cases faut-il ajouter ?',r'$3$ cases.','On doit remplir les trois cases encore blanches. Changer les positions des cases colorées ne change pas la fraction.'),
 q('Deux élèves colorient deux cases à des places différentes. Leurs fractions sont-elles égales ?',r'Oui : les deux représentent $\frac{2}{5}$.','La fraction dépend du nombre et de la taille des parts. Leur emplacement dans une même bande ne change pas la quantité colorée.')])
fig(6,'bande_vierge',bands([(5,0,'Une unité en cinq parts égales')]));fig(6,'bande_corrigee',bands([(5,2,'Deux cinquièmes de la bande')]));image(6,'nouveau-2',1,'bande_vierge','Bande unité partagée en cinq rectangles égaux non colorés.');image(6,'nouveau-2',2,'bande_corrigee','La même bande unité partagée en cinq cases, avec deux cases colorées en vert.');DATA[6][-1]['questions'][0]['e']+='\n\n[IMAGE_2]'
add(6,'Le bon vocabulaire','Lire le partage avant de compter les parts prises.',[
 q(r'Dans $\frac{7}{10}$, donner le numérateur.',r'$7$.','Le numérateur est le nombre écrit au-dessus du trait. Il compte sept parts prises.'),
 q(r'Dans $\frac{7}{10}$, donner le dénominateur.',r'$10$.','Le dénominateur est écrit sous le trait. Il indique que l’unité est partagée en dix parts égales.'),
 q('Écrire « trois quarts » avec une fraction.',r'$\frac{3}{4}$.','Le mot « quarts » donne le dénominateur 4. Le mot « trois » donne le numérateur 3.'),
 q('Écrire « huit sixièmes » avec une fraction.',r'$\frac{8}{6}$.','L’unité est partagée en six parts égales. On prend huit de ces parts, ce qui dépasse une unité.'),
 q(r'Lire $\frac{11}{12}$ en toutes lettres.','Onze douzièmes.','Le dénominateur 12 donne le nom des parts : douzièmes. Le numérateur indique qu’on en prend onze.')])
add(6,'Des parts vraiment égales ?','Le rectangle est découpé en trois morceaux : un grand morceau vert et deux petits morceaux blancs égaux.\n\n[IMAGE_1]',[
 q('Les trois morceaux ont-ils la même aire ?','Non.','Le morceau vert couvre la moitié du rectangle. Chaque morceau blanc ne couvre qu’un quart.'),
 q(r'Peut-on affirmer que le vert représente $\frac{1}{3}$ du rectangle ?','Non.','Compter un morceau sur trois ne suffit pas. Pour écrire un tiers, il faudrait trois parts de même aire.'),
 q('Quelle fraction du rectangle est réellement verte ?',r'$\frac{1}{2}$.','La séparation du milieu coupe le rectangle en deux surfaces égales. Toute la surface de gauche est verte.'),
 q('Quelle fraction représente chacun des petits morceaux blancs ?',r'$\frac{1}{4}$.','La moitié droite est partagée en deux morceaux égaux. Chaque petit morceau est donc la moitié d’une moitié, un quart.'),
 q('Comment obtenir quatre parts égales sans changer le contour ?','Couper le grand morceau vert en deux moitiés égales.','Les deux nouvelles parts vertes auront la même aire que les deux parts blanches. Le rectangle contiendra alors quatre quarts.')])
fig(6,'parts_inegales',r'''\begin{tikzpicture}
\fill[otGreen!30] (0,0) rectangle (3,1.5);
\draw[otNavy,line width=.8pt] (0,0) rectangle (6,1.5);
\draw[otNavy,line width=.7pt] (3,0)--(3,1.5);
\draw[otNavy,line width=.7pt] (3,.75)--(6,.75);
\end{tikzpicture}''');image(6,'nouveau-4',1,'parts_inegales','Rectangle partagé en une moitié verte et deux quarts blancs ; les trois morceaux n’ont pas la même aire.')
add(6,'Au-delà de l’unité','Chaque bande est une unité de même taille, partagée en quatre parts égales.\n\n[IMAGE_1]',[
 q('Combien de quarts sont colorés en tout ?',r'$5$ quarts.','La première bande contient quatre cases vertes. La deuxième en contient une ; on en compte cinq en tout.'),
 q('Écrire la fraction représentée.',r'$\frac{5}{4}$.','Chaque part est un quart de bande. Cinq parts donnent cinq quarts, même si elles occupent deux bandes.'),
 q('Combien d’unités entières sont complètement colorées ?',r'$1$ unité.','La première bande est entièrement verte. La deuxième n’est pas entièrement remplie.'),
 q('Écrire la fraction comme un entier et une fraction inférieure à un.',r'$\frac{5}{4}=1+\frac{1}{4}$.','Quatre quarts forment une unité. Après cette unité, il reste un quart.'),
 q('Encadrer cette fraction par deux entiers consécutifs.',r'$1<\frac{5}{4}<2$.','Cinq quarts dépassent les quatre quarts d’une unité. Ils sont inférieurs aux huit quarts de deux unités.')])
fig(6,'cinq_quarts',bands([(4,4,'Première bande unité'),(4,1,'Deuxième bande unité')]));image(6,'nouveau-5',1,'cinq_quarts','Deux bandes unité identiques en quarts : quatre quarts verts sur la première et un quart vert sur la seconde.')
add(6,'Entier caché','Regrouper les parts pour former des unités entières.',[
 q(r'Décomposer $\frac{7}{4}$ en un entier et une fraction inférieure à un.',r'$\frac{7}{4}=1+\frac{3}{4}$.','On regroupe quatre quarts pour faire une unité. Trois quarts restent après ce regroupement.'),
 q(r'Que vaut $\frac{9}{3}$ ?',r'$\frac{9}{3}=3$.','Chaque unité contient trois tiers. Neuf tiers forment trois paquets complets de trois.'),
 q(r'Décomposer $\frac{14}{5}$.',r'$\frac{14}{5}=2+\frac{4}{5}$.',r'Dix cinquièmes donnent deux unités. On compte encore $14-10=4$ cinquièmes.'),
 q(r'Décomposer $\frac{17}{6}$.',r'$\frac{17}{6}=2+\frac{5}{6}$.','Deux unités font douze sixièmes. Les cinq sixièmes restants sont inférieurs à une unité.'),
 q(r'Un élève écrit $\frac{7}{4}=1+\frac{3}{7}$. Corriger son erreur.',r'$\frac{7}{4}=1+\frac{3}{4}$.','Le partage reste en quarts après avoir retiré une unité. Le dénominateur ne devient pas 7.')])
add(6,'Recomposer','Transformer les unités complètes dans le partage demandé.',[
 q(r'Écrire $2+\frac{3}{5}$ avec une seule fraction.',r'$2+\frac{3}{5}=\frac{13}{5}$.',r'Deux unités font $\frac{10}{5}$. On ajoute trois cinquièmes pour obtenir treize cinquièmes.'),
 q(r'Écrire $1+\frac{2}{3}$ avec une seule fraction.',r'$1+\frac{2}{3}=\frac{5}{3}$.','Une unité représente trois tiers. Trois tiers plus deux tiers font cinq tiers.'),
 q(r'Écrire $3+\frac{1}{4}$ avec une seule fraction.',r'$3+\frac{1}{4}=\frac{13}{4}$.','Trois unités contiennent douze quarts. Avec le quart restant, on obtient treize quarts.'),
 q(r'Écrire $2+\frac{5}{6}$ avec une seule fraction.',r'$2+\frac{5}{6}=\frac{17}{6}$.','Deux unités font douze sixièmes. Douze sixièmes et cinq sixièmes donnent dix-sept sixièmes.'),
 q(r'Écrire $4$ en tiers.',r'$4=\frac{12}{3}$.',r'Chaque unité contient trois tiers. Quatre unités contiennent $4\times3=12$ tiers.')])
add(6,'Encadrer une fraction','Chercher les paquets complets de parts, puis l’unité suivante.',[
 q(r'Encadrer $\frac{11}{4}$ entre deux entiers consécutifs.',r'$2<\frac{11}{4}<3$.','Deux unités font huit quarts et trois unités douze quarts. Onze est entre huit et douze.'),
 q(r'Encadrer $\frac{17}{5}$ entre deux entiers consécutifs.',r'$3<\frac{17}{5}<4$.','Trois unités font quinze cinquièmes et quatre unités vingt cinquièmes. Dix-sept cinquièmes sont entre les deux.'),
 q(r'Encadrer $\frac{8}{3}$.',r'$2<\frac{8}{3}<3$.','Six tiers font deux unités. Neuf tiers font trois unités, et huit tiers n’atteignent pas cette borne.'),
 q(r'Encadrer $\frac{9}{10}$.',r'$0<\frac{9}{10}<1$.','Neuf dixièmes sont positifs. Il manque un dixième pour former une unité entière.'),
 q(r'Pourquoi $2<\frac{11}{4}<4$ n’est-il pas l’encadrement demandé ?','Les entiers $2$ et $4$ ne sont pas consécutifs.','Cette comparaison est vraie, mais elle laisse de côté la borne plus proche 3. Deux entiers consécutifs se suivent sans entier entre eux.')])
add(6,'Sept galettes pour quatre','Quatre enfants se partagent équitablement sept galettes identiques.',[
 q('Après avoir donné une galette entière à chacun, combien de galettes restent ?',r'$3$ galettes.',r'On utilise quatre galettes pour les quatre enfants. Il en reste $7-4=3$.'),
 q('En partageant chacune des galettes restantes en quatre, combien de quarts obtient-on ?',r'$12$ quarts.',r'Chaque galette donne quatre quarts. Trois galettes donnent $3\times4=12$ quarts.'),
 q('Combien de quarts supplémentaires reçoit chaque enfant ?',r'$3$ quarts.',r'On partage les douze quarts entre quatre enfants : $12\div4=3$. Chacun reçoit la même quantité.'),
 q('Écrire la part de chaque enfant de deux façons.',r'$\frac{7}{4}=1+\frac{3}{4}$ de galette.','La galette entière de départ vaut quatre quarts. Avec les trois quarts supplémentaires, chaque enfant reçoit sept quarts.'),
 q('Combien de quarts ont été distribués en tout ?',r'$28$ quarts.',r'Chaque enfant reçoit sept quarts, donc $4\times7=28$. C’est aussi $7\times4=28$ quarts dans sept galettes.')])
add(6,'Égales à un entier','Une unité contient autant de parts que le dénominateur l’indique.',[
 q(r'Compléter $\frac{\square}{6}=1$.',r'$\frac{6}{6}=1$.','Il faut six sixièmes pour reconstituer une unité. Le numérateur doit donc être 6.'),
 q(r'Compléter $\frac{12}{\square}=1$.',r'$\frac{12}{12}=1$.','Pour obtenir une unité, le nombre de parts prises doit égaler le nombre de parts du partage. Le dénominateur est 12.'),
 q('Combien de quarts font deux unités ?',r'$8$ quarts, soit $\frac{8}{4}=2$.',r'Une unité contient quatre quarts. Deux unités en contiennent $2\times4=8$.'),
 q('Combien de cinquièmes font trois unités ?',r'$15$ cinquièmes.',r'Chaque unité contient cinq cinquièmes. On calcule $3\times5=15$.'),
 q(r'Que vaut $\frac{20}{5}$ ?',r'$\frac{20}{5}=4$.','On regroupe vingt cinquièmes par paquets de cinq. Quatre paquets complets donnent quatre unités.')])
add(6,'Le gâteau de la fête','Un gâteau est découpé en douze parts égales. Cinq parts sont mangées le midi et quatre le soir.',[
 q('Quelle fraction est mangée le midi ?',r'$\frac{5}{12}$.','L’unité est le gâteau entier, partagé en douze. On compte les cinq parts prises le midi.'),
 q('Quelle fraction est mangée le soir ?',r'$\frac{4}{12}$.','Le gâteau n’est pas redécoupé. Les quatre parts du soir sont encore des douzièmes du gâteau initial.'),
 q('Quelle fraction a été mangée au total ?',r'$\frac{5}{12}+\frac{4}{12}=\frac{9}{12}$.',r'Les parts sont de même taille. On additionne leurs nombres : $5+4=9$.'),
 q('Quelle fraction reste-t-il ?',r'$\frac{3}{12}$.',r'Le gâteau contient douze parts. Il reste $12-9=3$ douzièmes.'),
 q('Combien de parts faudrait-il ajouter au reste pour obtenir une moitié de gâteau ?',r'$3$ parts.',r'Une moitié de gâteau contient six douzièmes. Avec trois parts restantes, il en manque $6-3=3$.')])
add(6,'La frise de la classe','Une frise contient vingt carreaux identiques. Les élèves peignent en bleu un quart de la frise.',[
 q('Combien de groupes égaux faut-il former pour repérer un quart ?',r'$4$ groupes.','Le dénominateur 4 impose quatre groupes de même taille. On partage tous les vingt carreaux entre ces groupes.'),
 q('Combien de carreaux contient un quart de la frise ?',r'$5$ carreaux.',r'On partage les vingt carreaux par quatre : $20\div4=5$.'),
 q('Combien de carreaux restent à peindre ?',r'$15$ carreaux.',r'Cinq carreaux sont peints. Il en reste $20-5=15$.'),
 q('Écrire la fraction qui reste avec le dénominateur 20.',r'$\frac{15}{20}$.','Chaque carreau vaut un vingtième de frise. Les quinze carreaux restants font quinze vingtièmes.'),
 q('Écrire cette même fraction avec le dénominateur 4.',r'$\frac{15}{20}=\frac{3}{4}$.','Sur les quatre groupes égaux, un seul est peint. Les trois autres groupes restent blancs : ce sont trois quarts.')])
add(6,'Des tartes en sixièmes','Deux tartes identiques sont coupées en six parts égales chacune. Sept parts sont mangées.',[
 q('Quelle fraction de tarte a été mangée ?',r'$\frac{7}{6}$.','L’unité choisie est une tarte, et non l’ensemble des deux. Chaque part représente un sixième de tarte.'),
 q('Cette fraction est-elle supérieure ou inférieure à une unité ?',r'$\frac{7}{6}>1$.','Une tarte entière contient six parts. Sept parts dépassent cette quantité d’un sixième.'),
 q('Décomposer la fraction mangée en un entier et une fraction.',r'$\frac{7}{6}=1+\frac{1}{6}$.','On regroupe six parts pour faire une tarte entière. Une part reste après cette tarte.'),
 q('Combien de parts y avait-il au départ ?',r'$12$ parts.',r'Deux tartes de six parts contiennent $2\times6=12$ parts au total.'),
 q('Quelle fraction de tarte reste-t-il ?',r'$\frac{5}{6}$.',r'Il reste $12-7=5$ parts. Chaque part est toujours un sixième d’une tarte.')])
add(6,'Dépasser un sans calculer','Pour comparer à une unité, comparer le nombre de parts au nombre nécessaire pour la former.',[
 q(r'Comparer $\frac{9}{8}$ à 1.',r'$\frac{9}{8}>1$.','Neuf parts sont prises alors que huit huitièmes suffisent pour une unité. La fraction dépasse un.'),
 q(r'Comparer $\frac{5}{6}$ à 1.',r'$\frac{5}{6}<1$.','Il manque un sixième pour reconstituer une unité. Le numérateur est inférieur au dénominateur.'),
 q(r'Comparer $\frac{12}{12}$ à 1.',r'$\frac{12}{12}=1$.','On prend exactement toutes les douze parts de l’unité. Aucun morceau ne manque et rien ne dépasse.'),
 q(r'Comparer $\frac{20}{19}$ à 1.',r'$\frac{20}{19}>1$.','Une unité contient dix-neuf dix-neuvièmes. Avec vingt de ces parts, on dépasse une unité.'),
 q('Inventer une fraction supérieure à un avec le dénominateur 7.',r'Par exemple $\frac{8}{7}>1$.','Il faut un numérateur supérieur à 7. Huit convient, mais neuf ou dix conviendraient aussi.')])
add(6,'La moitié de qui ?','Hugo affirme : « Une demi-pizza est toujours plus grande qu’un quart de pizza. » Léna répond : « Il faut connaître les pizzas entières ! »',[
 q('Sur une même pizza, comparer une moitié et un quart.',r'$\frac{1}{2}>\frac{1}{4}$.','La moitié contient deux quarts de la même pizza. Elle est donc plus grande qu’un seul quart.'),
 q('Hugo a-t-il raison si les pizzas ont des tailles différentes ?','Non, pas toujours.','Une fraction se rapporte à une unité précise. La moitié d’une petite pizza peut être plus petite qu’un quart d’une très grande pizza.'),
 q('Une petite pizza a la même aire que deux parts carrées identiques. Combien de ces parts vaut sa moitié ?',r'$1$ part carrée.','On partage les deux parts en deux groupes égaux. Chaque groupe contient une part.'),
 q('Une grande pizza a la même aire que douze de ces parts carrées. Combien de parts vaut son quart ?',r'$3$ parts carrées.',r'On partage douze en quatre : $12\div4=3$. Le quart de la grande pizza vaut trois parts.'),
 q('Dans cet exemple, quelle portion est la plus grande ?','Le quart de la grande pizza.','Il vaut trois parts carrées, contre une seule pour la moitié de la petite. Pour comparer les portions, on utilise ici la même unité d’aire.')])

s=init(9)
add(9,'Le piège classique',r'Comparer $3{,}5$ et $3{,}45$ en tenant compte de la valeur des rangs.',[
 q(r'Écrire $3{,}5$ avec deux chiffres après la virgule.',r'$3{,}5=3{,}50$.','Le zéro ajouté au rang des centièmes ne change aucune valeur. Cinq dixièmes valent cinquante centièmes.'),
 q('Donner le nombre de centièmes après les trois unités dans chaque nombre.',r'$50$ centièmes et $45$ centièmes.','On compare les parts restantes après la même partie entière. Elles doivent être exprimées dans la même unité.'),
 q('Donner la bonne comparaison.',r'$3{,}5>3{,}45$.','Les parties entières sont identiques. Cinquante centièmes dépassent quarante-cinq centièmes.'),
 q('Quel est le premier rang qui permet de décider ?','Le rang des dixièmes.','3,5 contient cinq dixièmes et 3,45 seulement quatre dixièmes. Les centièmes ne renversent pas cette comparaison.'),
 q('Quelle est la différence entre les deux nombres ?',r'$3{,}50-3{,}45=0{,}05$.','On retire quarante-cinq centièmes de cinquante centièmes. Les trois unités de chaque nombre s’annulent.')])
add(9,'Compléter par un symbole','Comparer d’abord les parties entières, puis les rangs après la virgule.',[
 q(r'Comparer $6{,}08$ et $6{,}8$.',r'$6{,}08<6{,}8$.','Les parties entières sont égales. Au rang des dixièmes, zéro est plus petit que huit.'),
 q(r'Comparer $12{,}34$ et $9{,}99$.',r'$12{,}34>9{,}99$.','La partie entière douze dépasse neuf. Il n’est pas nécessaire de comparer les chiffres décimaux.'),
 q(r'Comparer $4{,}07$ et $4{,}7$.',r'$4{,}07<4{,}7$.','Les sept centièmes du premier nombre sont plus petits que les sept dixièmes du second. Les parties entières sont identiques.'),
 q(r'Comparer $8{,}20$ et $8{,}2$.',r'$8{,}20=8{,}2$.','Vingt centièmes représentent exactement deux dixièmes. Le zéro final ne change pas le nombre.'),
 q(r'Comparer $10$ et $9{,}99$.',r'$10>9{,}99$.','Dix unités dépassent neuf unités et une partie d’unité. Le nombre 9,99 reste strictement inférieur à dix.')])
add(9,'Ranger cinq nombres',r'On dispose de $7{,}3$ ; $7{,}09$ ; $7{,}31$ ; $7{,}1$ ; $6{,}99$.',[
 q('Quel est le plus petit nombre ?',r'$6{,}99$.','Il a une partie entière égale à six. Tous les autres ont une partie entière égale à sept.'),
 q('Quel est le plus grand nombre ?',r'$7{,}31$.','Parmi les nombres de partie entière sept, les trois dixièmes sont les plus grands. Avec un centième supplémentaire, 7,31 dépasse 7,30.'),
 q('Ranger les cinq nombres dans l’ordre croissant.',r'$6{,}99<7{,}09<7{,}1<7{,}3<7{,}31$.','On peut compléter les nombres avec des zéros : 7,10 et 7,30. Puis on compare les rangs de gauche à droite.'),
 q(r'Quel nombre de la liste est juste avant $7{,}3$ dans ce rangement ?',r'$7{,}1$.','Dans la liste ordonnée, 7,1 est le voisin situé à gauche de 7,3. La question porte sur les nombres proposés.'),
 q('Ranger les trois plus grands dans l’ordre décroissant.',r'$7{,}31>7{,}3>7{,}1$.','On sélectionne les trois derniers du rangement croissant. On les écrit ensuite du plus grand au plus petit.')])
add(9,'Encadrer par des entiers','Chercher les unités complètes, puis l’entier suivant.',[
 q(r'Encadrer $4{,}62$ entre deux entiers consécutifs.',r'$4<4{,}62<5$.','La partie entière est quatre. Le nombre dépasse quatre mais n’atteint pas cinq.'),
 q(r'Encadrer $0{,}85$ entre deux entiers consécutifs.',r'$0<0{,}85<1$.','Le nombre ne contient aucune unité complète. Sa partie décimale positive le place entre zéro et un.'),
 q(r'Encadrer $17{,}04$.',r'$17<17{,}04<18$.','Dix-sept unités sont complètes. Les quatre centièmes supplémentaires ne forment pas une unité de plus.'),
 q(r'Encadrer $9{,}99$.',r'$9<9{,}99<10$.','Le nombre est très proche de dix, mais il lui manque encore un centième. Sa borne supérieure est dix.'),
 q(r'Pourquoi $4<4{,}62<6$ ne répond-il pas à la demande ?',r'Les bornes $4$ et $6$ ne sont pas consécutives.','Cet encadrement est vrai, mais un entier, cinq, se trouve entre les deux bornes. Il faut resserrer la borne supérieure à cinq.')])
add(9,'Partie entière','La partie entière compte les unités complètes.',[
 q(r'Donner la partie entière de $17{,}83$.',r'$17$.','On lit les chiffres situés à gauche de la virgule. Les quatre-vingt-trois centièmes ne forment pas une unité complète.'),
 q(r'Donner la partie entière de $9{,}04$.',r'$9$.','Le nombre contient neuf unités et quatre centièmes. Sa partie entière est donc neuf.'),
 q(r'Donner la partie entière de $0{,}76$.',r'$0$.','Le nombre est inférieur à un. Il ne contient aucune unité complète.'),
 q(r'Donner la partie entière de $12{,}99$.',r'$12$.','La partie entière reste douze même si le nombre est proche de treize. Elle n’est pas un arrondi.'),
 q(r'La partie entière de $7{,}83$ est-elle son arrondi à l’entier ?',r'Non : partie entière $7$, arrondi $8$.','La partie entière compte les unités complètes. L’arrondi choisit l’entier le plus proche, ici huit.')])
add(9,'Lire entre les graduations','La demi-droite est graduée en dixièmes.\n\n[IMAGE_1]',[
 q('Lire le nombre du point A.',r'$5{,}3$.','A se trouve trois petits pas après cinq. Chaque pas vaut un dixième.'),
 q('Lire le nombre du point B.',r'$5{,}8$.','B est au huitième pas après cinq. Il représente cinq unités et huit dixièmes.'),
 q(r'Où placer $C(5{,}45)$ ?',r'Au milieu entre $5{,}4$ et $5{,}5$.','Cinq centièmes sont la moitié d’un dixième. Le nombre 5,45 se situe donc à mi-chemin entre ces deux graduations.'),
 q('Ranger les nombres de A, B et C dans l’ordre croissant.',r'$5{,}3<5{,}45<5{,}8$.','Sur la demi-droite, A est à gauche de C et C à gauche de B. Cet ordre correspond à l’ordre des nombres.'),
 q('Quel point est le plus proche de six ?',r'B.','B est situé à deux dixièmes de six. A et C sont plus à gauche et donc plus éloignés de six.\n\n[IMAGE_2]')])
fig(9,'droite_decimale',line('5','6',10,[('A',3),('B',8)]));fig(9,'droite_corrigee',line('5','6',10,[('A',3),('C',4.5,'otGreenDark'),('B',8)]));image(9,'nouveau-6',1,'droite_decimale','Demi-droite de cinq à six graduée en dixièmes, A à 5,3 et B à 5,8.');image(9,'nouveau-6',2,'droite_corrigee','Correction : C en vert est placé au milieu de l’intervalle de 5,4 à 5,5, entre A et B.')
add(9,'Intercaler au centième','Dans tout cet exercice, utiliser au plus deux chiffres après la virgule.',[
 q(r'Donner un nombre strictement entre $2{,}4$ et $2{,}5$.',r'Par exemple $2{,}4<2{,}45<2{,}5$.','On écrit les bornes en centièmes : 2,40 et 2,50. 2,45 se situe entre les deux.'),
 q('Donner un autre nombre dans le même intervalle.',r'Par exemple $2{,}4<2{,}41<2{,}5$.','Le premier centième après 2,40 est 2,41. Il reste inférieur à 2,50.'),
 q(r'Donner un nombre strictement entre $8{,}3$ et $8{,}4$.',r'Par exemple $8{,}3<8{,}35<8{,}4$.','On choisit trente-cinq centièmes entre trente et quarante centièmes. La partie entière reste huit.'),
 q(r'Peut-on intercaler un nombre avec au plus deux chiffres après la virgule entre $8{,}31$ et $8{,}32$ ?',r'Non, avec cette précision.','31 et 32 sont des nombres consécutifs de centièmes. Aucun nombre de centièmes entier n’est strictement entre eux.'),
 q(r'Combien de nombres au centième sont strictement entre $2{,}40$ et $2{,}50$ ?',r'$9$ nombres.','On peut choisir 2,41, 2,42, et ainsi de suite jusqu’à 2,49. Les bornes sont exclues et les neuf centièmes intermédiaires conviennent.')])
add(9,'Arrondir à l’entier','Choisir l’entier le plus proche. À égale distance, prendre l’entier supérieur.',[
 q(r'Arrondir $7{,}3$ à l’entier.',r'$7$.','7,3 est à trois dixièmes de sept et à sept dixièmes de huit. Sept est donc le plus proche.'),
 q(r'Arrondir $7{,}83$ à l’entier.',r'$8$.','7,83 est à dix-sept centièmes de huit et à quatre-vingt-trois centièmes de sept. On retient huit.'),
 q(r'Arrondir $12{,}5$ à l’entier.',r'$13$.','12,5 est exactement au milieu entre douze et treize. La convention choisit l’entier supérieur, treize.'),
 q(r'Arrondir $4{,}49$ à l’entier.',r'$4$.','4,49 est inférieur au milieu 4,5. Il est plus proche de quatre que de cinq.'),
 q(r'Arrondir $0{,}76$ à l’entier.',r'$1$.','Le milieu entre zéro et un est 0,5. 0,76 se situe du côté de un.')])
add(9,'Compter de dixième en dixième',r'On part de $3{,}7$ et on ajoute $0{,}1$ à chaque pas.',[
 q('Quel nombre vient après un pas ?',r'$3{,}8$.','Sept dixièmes plus un dixième font huit dixièmes. La partie entière reste trois.'),
 q('Quel nombre vient après deux pas ?',r'$3{,}9$.','On a ajouté deux dixièmes aux sept dixièmes de départ. Cela donne neuf dixièmes.'),
 q('Quel nombre vient après trois pas ?',r'$4$.','Le troisième dixième complète dix dixièmes. On les échange contre une unité entière.'),
 q('Quel nombre vient après quatre pas ?',r'$4{,}1$.','Après quatre unités, le pas suivant ajoute un dixième. Le nombre dépasse donc quatre.'),
 q('Écrire toute la suite, du départ jusqu’au premier nombre supérieur à quatre.',r'$3{,}7$ ; $3{,}8$ ; $3{,}9$ ; $4$ ; $4{,}1$.','On conserve toujours le même pas d’un dixième. Le franchissement de l’unité fait passer 3,9 à 4, pas à 3,10.')])
add(9,'Le même nombre ?','Un zéro n’a pas le même effet selon sa position.',[
 q(r'$5{,}60$ et $5{,}6$ sont-ils égaux ?',r'Oui : $5{,}60=5{,}6$.','Soixante centièmes correspondent à six dixièmes. Le zéro final peut être omis.'),
 q(r'$5{,}06$ et $5{,}6$ sont-ils égaux ?',r'Non : $5{,}06<5{,}6$.','Six centièmes sont inférieurs à six dixièmes. Le zéro après la virgule garde un rang vide indispensable.'),
 q(r'$07{,}2$ et $7{,}2$ sont-ils égaux ?',r'Oui : $07{,}2=7{,}2$.','Le zéro placé à gauche de l’écriture ne compte aucune dizaine supplémentaire. Il ne change pas la valeur.'),
 q(r'$3{,}00$ et $3$ sont-ils égaux ?',r'Oui : $3{,}00=3$.','Il y a trois unités, zéro dixième et zéro centième. Les rangs décimaux n’ajoutent rien.'),
 q(r'Peut-on effacer le zéro de $8{,}04$ pour écrire $8{,}4$ ?',r'Non : $8{,}04\ne8{,}4$.','Le zéro intérieur garantit que le 4 compte des centièmes. Le retirer transforme les centièmes en dixièmes.')])
add(9,'Le podium du saut',r'Lina saute $3{,}45$ m, Maya $3{,}5$ m et Inès $3{,}09$ m.',[
 q('Qui réalise le saut le plus long ?','Maya.','3,5 s’écrit 3,50. Cinquante centièmes dépassent quarante-cinq centièmes et neuf centièmes.'),
 q('Qui réalise le saut le plus court ?','Inès.','Les trois sauts ont trois mètres entiers. Neuf centièmes sont la plus petite partie restante.'),
 q('Donner le classement du meilleur au moins bon saut.','Maya, Lina, Inès.','Les longueurs vérifient $3{,}5>3{,}45>3{,}09$. Le meilleur saut est celui de longueur maximale.'),
 q('Donner l’écart entre les sauts de Maya et de Lina.',r'$0{,}05$ m.',r'On utilise des centièmes : $3{,}50-3{,}45=0{,}05$. Cela correspond à cinq centièmes de mètre.'),
 q('Arrondir chacun des trois sauts au mètre entier le plus proche.','Lina : $3$ m ; Maya : $4$ m ; Inès : $3$ m.','3,45 et 3,09 sont en dessous du milieu 3,5. Le saut 3,5 est exactement au milieu et s’arrondit à l’entier supérieur.')])
add(9,'La toise de la classe',r'Quatre tailles sont $1{,}38$ m, $1{,}4$ m, $1{,}29$ m et $1{,}33$ m.',[
 q('Donner la plus petite taille.',r'$1{,}29$ m.','Les parties entières sont identiques. Deux dixièmes sont inférieurs à trois dixièmes et à quatre dixièmes.'),
 q('Donner la plus grande taille.',r'$1{,}4$ m.','On peut écrire 1,40. Quarante centièmes dépassent les autres parties décimales proposées.'),
 q('Ranger les tailles dans l’ordre croissant.',r'$1{,}29<1{,}33<1{,}38<1{,}4$.','Après avoir comparé les dixièmes, on départage 1,33 et 1,38 grâce aux centièmes : trois puis huit.'),
 q('Quelle taille est juste au-dessus de 1,33 m dans cette liste ?',r'$1{,}38$ m.','Le rangement croissant donne les voisins successifs. Le nombre immédiatement à droite de 1,33 dans la liste est 1,38.'),
 q('Quelle différence sépare la plus grande et la plus petite taille ?',r'$0{,}11$ m.',r'On aligne les rangs : $1{,}40-1{,}29=0{,}11$. Il y a onze centièmes de mètre d’écart.')])
add(9,'Des intermédiaires bien choisis','Rester dans les nombres qui ont au plus deux chiffres après la virgule.',[
 q(r'Donner deux nombres différents strictement entre $6{,}2$ et $6{,}3$.',r'Par exemple $6{,}24$ et $6{,}27$.','Les bornes s’écrivent 6,20 et 6,30. Les parties décimales 24 et 27 centièmes sont entre vingt et trente centièmes.'),
 q('Vérifier leur ordre avec les deux bornes.',r'$6{,}2<6{,}24<6{,}27<6{,}3$.','Les parties entières sont toutes égales à six. On compare donc les nombres de centièmes 20, 24, 27 et 30.'),
 q('Quel est le plus petit nombre au centième strictement supérieur à 6,2 ?',r'$6{,}21$.','6,2 est égal à 6,20. Ajouter un centième donne le premier nombre au centième qui le dépasse.'),
 q('Quel est le plus grand nombre au centième strictement inférieur à 6,3 ?',r'$6{,}29$.','6,3 est égal à 6,30. Retirer un centième donne le plus grand nombre au centième situé en dessous.'),
 q(r'Y a-t-il un nombre au centième strictement entre $6{,}24$ et $6{,}25$ ?',r'Non, avec au plus deux chiffres après la virgule.','Vingt-quatre et vingt-cinq sont deux nombres consécutifs de centièmes. Une précision plus fine dépasserait le cadre de cet exercice de CM1.')])
add(9,'L’étiquette effacée',r'Un paquet coûte $4{,}05$ euros et un autre $4{,}5$ euros. Tom pense que le premier est plus cher.',[
 q('Écrire les deux prix en centimes.',r'$405$ centimes et $450$ centimes.','Quatre euros valent quatre cents centimes. On ajoute respectivement cinq centimes et cinquante centimes.'),
 q('Comparer les deux prix.',r'$4{,}05<4{,}5$.','Les deux prix ont quatre euros. Cinq centimes sont inférieurs à cinquante centimes.'),
 q('Expliquer l’erreur de Tom.','Il compare les chiffres sans tenir compte de leurs rangs.','Le 5 de 4,05 vaut cinq centièmes d’euro. Celui de 4,5 vaut cinq dixièmes, soit cinquante centièmes.'),
 q('Combien économise-t-on en choisissant le moins cher ?',r'$0{,}45$ euro.',r'La différence vaut $4{,}50-4{,}05=0{,}45$. Cela représente quarante-cinq centimes.'),
 q('Un troisième paquet coûte 4,15 euros. Où se place-t-il entre les deux autres ?',r'$4{,}05<4{,}15<4{,}5$.','Quinze centimes dépassent cinq centimes mais restent inférieurs à cinquante centimes. La partie entière est la même.')])
add(9,'L’erreur de rangement',r'Aya écrit : « $12{,}34$ est plus grand que $12{,}5$, car 34 est plus grand que 5. »',[
 q('Expliquer l’erreur d’Aya.','Elle compare 34 centièmes à 5 dixièmes comme s’ils étaient de même taille.','Les deux écritures n’ont pas le même nombre de chiffres après la virgule. Il faut comparer rang par rang ou tout écrire en centièmes.'),
 q('Donner la comparaison correcte.',r'$12{,}34<12{,}5$.','On écrit 12,5 sous la forme 12,50. Trente-quatre centièmes sont inférieurs à cinquante centièmes.'),
 q('Arrondir 12,34 à l’entier.',r'$12$.','12,34 est inférieur au milieu 12,5. L’entier douze est plus proche que treize.'),
 q('Arrondir 12,5 à l’entier.',r'$13$.','Le nombre est exactement au milieu entre douze et treize. La convention d’arrondi choisit l’entier supérieur.'),
 q('Les deux nombres ont-ils la même partie entière ?',r'Oui : $12$.','La partie entière compte les unités complètes. Les deux nombres contiennent douze unités, même si leurs arrondis sont différents.')])

# Un travail sur des dénominateurs multiples complète les exercices du livre.
DATA[7][5]['questions'][4]=q(r'Calculer $\frac{1}{2}+\frac{1}{4}$ en utilisant des quarts.',r'$\frac{1}{2}+\frac{1}{4}=\frac{3}{4}$.','Une moitié vaut deux quarts. On réunit donc deux quarts et un quart : cela donne trois quarts.','Exprimer les deux fractions dans le même partage avant de réunir les parts.')
DATA[7][6]['questions'][4]=q(r'Calculer $\frac{1}{2}-\frac{1}{4}$ en utilisant des quarts.',r'$\frac{1}{2}-\frac{1}{4}=\frac{1}{4}$.','On écrit la moitié comme deux quarts. En retirant un quart de ces deux quarts, il reste un quart.','Changer la moitié en deux quarts avant de retirer une part.')

DOCS[1]=(r'''Titre: Les nombres entiers jusqu’à 999 999

<!-- optitab:1 -->
::: objectifs
Lire et écrire les nombres jusqu’à six chiffres, comprendre la valeur des rangs, distinguer chiffre et nombre de dizaines, comparer, ranger, encadrer et lire une demi-droite graduée.
:::

## I. Lire les classes et les rangs

::: definition Classes de trois chiffres
On groupe les chiffres par trois en partant de la droite. La classe des unités simples contient les unités, les dizaines et les centaines. La classe des mille contient les unités de mille, les dizaines de mille et les centaines de mille.
:::

| Classe | Groupe dans $304\,065$ |
|---|---|
| Mille | $304$ |
| Unités simples | $065$ |

On lit : « trois-cent-quatre-mille-soixante-cinq ». Le dernier groupe 065 représente soixante-cinq unités. Les zéros ne se prononcent pas, mais ils gardent les rangs vides.

::: propriete Échanger entre les rangs
Dix unités d’un rang font une unité du rang suivant : dix unités font une dizaine, dix dizaines une centaine, dix centaines un millier. La valeur d’un chiffre dépend donc de sa place.
:::

::: exemple Décomposer sans perdre les zéros
$$
304\,065=3\times100\,000+4\times1\,000+6\times10+5
$$
Le 3 vaut trois cent mille, le 4 quatre mille et le 6 soixante. Les dizaines de mille et les centaines sont absentes : on garde des zéros dans l’écriture du nombre.
:::

## II. Chiffre ou nombre de dizaines ?

::: methode Compter tous les paquets
Dans $4\,627$, le **chiffre** des dizaines est 2 : c’est un seul symbole. Le **nombre de dizaines** est 462 : on compte toutes les dizaines complètes, même celles contenues dans les centaines et les milliers.
$$
4\,627=462\times10+7
$$
On peut donc remplir 462 carnets de dix objets, et il reste sept objets.
:::

::: attention Ne pas confondre
Un chiffre est compris entre 0 et 9. Le nombre de dizaines, de centaines ou de milliers peut avoir plusieurs chiffres. Dans $4\,627$, le chiffre des centaines est 6, mais le nombre de centaines est 46.
:::

## III. Comparer, ranger et encadrer

::: methode Comparer de gauche à droite
Un entier avec moins de chiffres est plus petit. Si les nombres ont autant de chiffres, comparer le premier rang différent en partant de la gauche.
$$
9\,875<12\,034
$$
$$
45\,806<45\,860
$$
Dans la deuxième comparaison, les dizaines décident : zéro dizaine est inférieur à six dizaines.
:::

Ranger dans l’ordre **croissant**, c’est aller du plus petit au plus grand. Dans l’ordre **décroissant**, on va du plus grand au plus petit.

::: exemple Encadrer et intercaler
Entre deux milliers consécutifs : $45\,000<45\,670<46\,000$.

Entre deux dizaines de mille consécutives : $40\,000<45\,670<50\,000$.

Intercaler un entier, c’est en choisir un strictement entre les bornes : $23\,500<23\,540<23\,600$.
:::

## IV. Lire une demi-droite graduée

[IMAGE_1]

::: methode Commencer par le pas
Entre $24\,000$ et $28\,000$, on compte huit intervalles, et non neuf. Le pas vaut 500, car $8\times500=4\,000$. A est deux pas après le début : $24\,000+2\times500=25\,000$. On compte toujours les intervalles entre les traits.
:::

::: retenir
Lire les classes, repérer le rang de chaque chiffre, puis vérifier les zéros. Pour comparer, partir de la gauche. Pour une graduation, trouver le pas avant de lire le point.
:::
''',r'''Titre: Synthèse : les nombres entiers jusqu’à 999 999

<!-- optitab:1 -->
::: objectifs
Retenir les réflexes de numération et de comparaison.
:::

## I. Classes et valeurs

Les chiffres sont groupés par trois : classe des mille, puis classe des unités simples. Dans $304\,065$, les groupes sont $304$ et $065$.

::: formule
$304\,065=300\,000+4\,000+60+5$.
:::

Chaque rang vaut dix fois le rang situé à sa droite. Les zéros gardent la place des rangs vides.

## II. Chiffre et nombre

Dans $4\,627$, le chiffre des dizaines est **2**, mais il y a **462 dizaines** complètes : $4\,627=462\times10+7$.

## III. Les méthodes

1. Comparer les nombres de chiffres, puis les rangs de gauche à droite.
2. Ranger du plus petit au plus grand pour l’ordre croissant.
3. Encadrer avec deux multiples consécutifs du rang demandé.
4. Sur une demi-droite, compter les **intervalles** pour trouver le pas.

::: attention
Ne pas enlever un zéro intérieur. Ne pas confondre un chiffre avec un nombre de paquets. Deux bornes consécutives n’ont aucun autre multiple du rang demandé entre elles.
:::
''')
image(1,'nouveau',1,'graduation',MAPS[1]['exercices']['nouveau-8']['1']['alt'])

DOCS[6]=(r'''Titre: Découvrir les fractions

<!-- optitab:1 -->
::: objectifs
Lire et représenter une fraction, reconnaître des parts égales, dépasser l’unité, passer d’une fraction à un entier et une fraction, et encadrer entre deux entiers consécutifs.
:::

## I. Une unité, des parts égales

::: definition Le sens d’une fraction
On choisit d’abord une **unité** : une bande entière, un disque entier ou une longueur. Si on partage cette unité en huit parts égales, chaque part vaut un huitième. Trois de ces parts forment $\frac{3}{8}$ de l’unité.

Le **dénominateur**, en bas, donne le nombre de parts égales du partage. Le **numérateur**, en haut, compte les parts prises.
:::

[IMAGE_1]

::: exemple Lire la fraction
Le disque possède huit secteurs égaux, dont trois verts. La partie verte représente $\frac{3}{8}$ et la partie blanche $\frac{5}{8}$. Ensemble, les huit huitièmes forment une unité : $\frac{8}{8}=1$.
:::

::: attention Compter ne suffit pas
Un morceau sur trois n’est pas forcément un tiers. Il faut que les trois morceaux aient la même taille. Des morceaux peuvent avoir des formes différentes tout en ayant la même aire, mais l’égalité des aires doit être vérifiée.
:::

## II. Dépasser une unité

::: propriete Une fraction est aussi un nombre
On peut prendre plus de parts que celles d’une seule unité. Les unités utilisées doivent être identiques. Cinq quarts, c’est une unité entière et encore un quart.
$$
\frac{5}{4}=1+\frac{1}{4}
$$
:::

[IMAGE_2]

Pour comparer une fraction à 1, comparer son numérateur à son dénominateur. S’il est plus petit, il manque des parts. S’il est égal, l’unité est complète. S’il est plus grand, on dépasse une unité.

## III. Regrouper et décomposer

::: methode Faire des paquets complets
Pour décomposer $\frac{13}{5}$, on cherche combien de paquets de cinq cinquièmes sont complets. Dix cinquièmes font deux unités, puis il reste trois cinquièmes.
$$
\frac{13}{5}=2+\frac{3}{5}
$$
Inversement, deux unités font dix cinquièmes. En ajoutant trois cinquièmes, on retrouve treize cinquièmes.
:::

::: exemple Un entier caché
Neuf tiers forment trois paquets de trois tiers : $\frac{9}{3}=3$. Une fraction peut donc être égale à un entier.
:::

## IV. Encadrer et partager

::: methode Encadrer entre deux entiers consécutifs
Onze quarts se placent entre huit quarts et douze quarts. Or huit quarts font deux unités et douze quarts en font trois.
$$
2<\frac{11}{4}<3
$$
Les bornes 2 et 3 se suivent : elles sont consécutives.
:::

::: exemple Sept galettes pour quatre enfants
On donne d’abord une galette à chacun : quatre galettes sont utilisées. Les trois restantes sont coupées en quarts, ce qui donne douze quarts. Chaque enfant reçoit encore trois quarts. Sa part totale est $\frac{7}{4}=1+\frac{3}{4}$ de galette.
:::

::: retenir
Toujours préciser l’unité et vérifier l’égalité des parts. Le partage reste le même lorsqu’on regroupe les parts : le dénominateur ne change pas. Des fractions différentes peuvent désigner une unité entière ou plusieurs unités.
:::
''',r'''Titre: Synthèse : découvrir les fractions

<!-- optitab:1 -->
::: objectifs
Comprendre le partage et les fractions qui dépassent un.
:::

## I. Lire une fraction

Dans $\frac{3}{8}$, **8** est le dénominateur : huit parts égales dans l’unité. **3** est le numérateur : trois parts prises.

::: attention
Choisir l’unité. Vérifier que les parts sont égales. Une moitié d’une petite unité ne se compare pas directement à un quart d’une autre unité plus grande.
:::

## II. Comparer à un

- Numérateur plus petit : fraction inférieure à un.
- Numérateur égal : fraction égale à un.
- Numérateur plus grand : fraction supérieure à un.

## III. Décomposer et recomposer

::: formule
$\frac{13}{5}=2+\frac{3}{5}$ et $\frac{9}{3}=3$.
:::

Regrouper les parts qui font des unités complètes. Pour recomposer, transformer d’abord les unités dans le partage demandé.

## IV. Encadrer

Pour onze quarts, huit quarts font 2 et douze quarts font 3 : $2<\frac{11}{4}<3$.

::: retenir
Le dénominateur nomme les parts ; il ne change pas quand on les compte ou les regroupe.
:::
''')
image(6,'nouveau',1,'disque_huitiemes',MAPS[6]['exercices']['nouveau-1']['1']['alt']);image(6,'nouveau',2,'cinq_quarts',MAPS[6]['exercices']['nouveau-5']['1']['alt'])

DOCS[7]=(r'''Titre: Utiliser les fractions

<!-- optitab:1 -->
::: objectifs
Lire et placer des fractions sur une demi-droite, comparer des parts, additionner et soustraire dans un même partage, reconnaître des écritures égales et calculer une fraction unitaire d’une quantité.
:::

## I. Des nombres sur une demi-droite

::: definition L’unité de graduation
Sur une demi-droite, la distance de 0 à 1 représente une unité. Si on la partage en quatre intervalles égaux, chaque pas vaut $\frac{1}{4}$. Pour placer une fraction en quarts, on compte les pas depuis zéro.
:::

[IMAGE_1]

::: exemple Continuer après un
A est à trois pas de zéro : sa position est $\frac{3}{4}$. B est à sept pas : sa position est $\frac{7}{4}=1+\frac{3}{4}$. On continue à compter après le point de nombre 1, sans changer la taille du pas.
:::

## II. Comparer des fractions

::: methode Même dénominateur
Quand les parts ont la même taille, on compare leur nombre. Cinq huitièmes sont plus grands que trois huitièmes : $\frac{5}{8}>\frac{3}{8}$. Sur la demi-droite, le plus grand nombre est le plus à droite.
:::

::: propriete Une seule part, des partages différents
Pour une même unité, partager en moins de parts donne des parts plus grandes. Ainsi $\frac{1}{3}>\frac{1}{4}$. Cette règle ne permet pas de comparer n’importe quelles fractions : elle concerne ici une seule part de chaque partage.
:::

::: exemple Changer de partage sans changer de longueur
Une moitié couvre exactement deux quarts : $\frac{1}{2}=\frac{2}{4}$. Pour comparer $\frac{3}{4}$ à une moitié, comparer trois quarts à deux quarts : $\frac{3}{4}>\frac{1}{2}$.
:::

[IMAGE_2]

## III. Réunir ou retirer des parts

::: methode Conserver la taille des parts
Si les dénominateurs sont les mêmes, additionner ou soustraire les numérateurs. Garder le dénominateur : les parts ne sont pas redécoupées.
$$
\frac{3}{8}+\frac{2}{8}=\frac{5}{8}
$$
$$
\frac{7}{10}-\frac{4}{10}=\frac{3}{10}
$$
:::

::: exemple Quand un partage est un multiple de l’autre
Une moitié vaut deux quarts. Avant d’ajouter un quart, on exprime donc toutes les parts en quarts.
$$
\frac{1}{2}+\frac{1}{4}=\frac{2}{4}+\frac{1}{4}=\frac{3}{4}
$$
Pour retirer un quart à une moitié : $\frac{1}{2}-\frac{1}{4}=\frac{1}{4}$.
:::

::: attention
On n’additionne pas les dénominateurs. Trois huitièmes et deux huitièmes font cinq huitièmes, et non cinq seizièmes. Avant de calculer, les parts doivent être de même taille.
:::

## IV. Une part d’une quantité

::: methode Calculer une fraction unitaire
Prendre le tiers de douze billes, c’est partager les douze billes en trois groupes égaux et en garder un. On calcule $12\div3=4$ : un tiers de douze billes vaut quatre billes.

Prendre le quart de cent mètres donne $100\div4=25$ mètres. Le dénominateur indique le nombre de groupes égaux.
:::

::: retenir
Identifier l’unité, puis le partage. Comparer ou calculer avec des parts de même taille. Pour une fraction unitaire d’une quantité, partager cette quantité par le dénominateur.
:::
''',r'''Titre: Synthèse : utiliser les fractions

<!-- optitab:1 -->
::: objectifs
Placer, comparer et calculer avec des parts égales.
:::

## I. Placer et comparer

Un pas vaut un quart si quatre intervalles relient 0 à 1. Compter depuis zéro : sept pas donnent $\frac{7}{4}=1+\frac{3}{4}$.

Même dénominateur : comparer les numérateurs. Pour une même unité, un tiers est plus grand qu’un quart.

## II. Réunir, retirer, changer de partage

::: formule
$\frac{3}{8}+\frac{2}{8}=\frac{5}{8}$ ; $\frac{7}{10}-\frac{4}{10}=\frac{3}{10}$.
:::

Une moitié vaut deux quarts : $\frac{1}{2}=\frac{2}{4}$. Donc $\frac{1}{2}+\frac{1}{4}=\frac{3}{4}$.

::: attention
Conserver le dénominateur quand les parts ont la même taille. Ne pas additionner ou soustraire les dénominateurs.
:::

## III. Une fraction unitaire d’une quantité

Partager en groupes égaux, puis prendre un groupe. Le tiers de douze vaut quatre, car $12\div3=4$. Le quart de cent vaut vingt-cinq, car $100\div4=25$.

::: retenir
Sur une demi-droite, le plus grand nombre se trouve le plus à droite. Pour toute représentation, garder la même unité.
:::
''')
image(7,'nouveau',1,'quarts',MAPS[7]['exercices']['nouveau-1']['1']['alt']);image(7,'nouveau',2,'moitie_quarts',MAPS[7]['exercices']['nouveau-14']['1']['alt'])

DOCS[8]=(r'''Titre: Fractions décimales et écriture à virgule

<!-- optitab:1 -->
::: objectifs
Comprendre les dixièmes et les centièmes, passer des fractions décimales à la virgule, décomposer un nombre et reconnaître le rôle des zéros.
:::

## I. Des parts de dix et de cent

::: definition Les fractions décimales étudiées en CM1
Une fraction décimale représente un partage de l’unité en dix, en cent, puis dans d’autres partages par dix. En CM1, on utilise les dixièmes et les centièmes, avec les dénominateurs 10 et 100.

Une unité contient dix dixièmes ou cent centièmes. Un dixième contient dix centièmes.
:::

$$
1=\frac{10}{10}=\frac{100}{100}
$$
$$
\frac{3}{10}=\frac{30}{100}
$$

## II. Le code de la virgule

::: definition La place des chiffres
À gauche de la virgule se trouvent les unités complètes. Le premier chiffre à droite compte les dixièmes et le deuxième compte les centièmes.
:::

| Position dans $35{,}78$ | Écriture | Valeur |
|---|---|---|
| Partie entière | $35$ | $35$ unités |
| Dixièmes | $7$ | $\frac{7}{10}$ |
| Centièmes | $8$ | $\frac{8}{100}$ |

::: exemple Décomposer
$$
35{,}78=35+\frac{7}{10}+\frac{8}{100}
$$
Le nombre se lit « trente-cinq unités et soixante-dix-huit centièmes ». La virgule sert à coder les rangs : elle ne sépare pas deux entiers indépendants.
:::

## III. Passer d’une écriture à l’autre

::: methode Fraction vers virgule
Pour $\frac{307}{100}$, trois cents centièmes donnent trois unités. Il reste sept centièmes et aucun dixième entier : $\frac{307}{100}=3{,}07$.

Pour $\frac{45}{10}$, quarante dixièmes donnent quatre unités et il reste cinq dixièmes : $\frac{45}{10}=4{,}5$.
:::

::: methode Virgule vers fraction
Dans $6{,}09$, six unités font six cents centièmes. Ajouter neuf centièmes donne $6{,}09=\frac{609}{100}$. On peut aussi décomposer : $6{,}09=6+\frac{9}{100}$.
:::

[IMAGE_1]

Sur la grille, chaque petite case vaut un centième de l’unité. Trente-sept cases vertes représentent $\frac{37}{100}=0{,}37$. Trois colonnes complètes font trois dixièmes, et sept cases ajoutent sept centièmes.

## IV. Les zéros et le passage d’une unité

::: propriete Un zéro final peut être omis
Trente centièmes valent trois dixièmes : $2{,}30=2{,}3$. Le zéro final n’ajoute aucune part. En revanche, $2{,}03\ne2{,}3$ : le zéro intérieur garde le rang des dixièmes vide.
:::

::: exemple Compter en dixièmes
Après $45{,}8$ vient $45{,}9$, puis $46$. Dix dixièmes s’échangent contre une unité. L’écriture $45{,}10$ représente $45{,}1$ et ne peut pas être le nombre suivant $45{,}9$.
:::

::: retenir
Dix centièmes font un dixième ; dix dixièmes font une unité. Lire le rang avant de lire le chiffre. En CM1, les nombres étudiés ont au plus deux chiffres après la virgule.
:::
''',r'''Titre: Synthèse : fractions décimales et virgule

<!-- optitab:1 -->
::: objectifs
Passer des parts décimales à leur écriture à virgule.
:::

## I. Les échanges

::: formule
$1=\frac{10}{10}=\frac{100}{100}$ et $\frac{1}{10}=\frac{10}{100}$.
:::

À droite de la virgule : d’abord les dixièmes, puis les centièmes.

## II. Décomposer et recomposer

$35{,}78=35+\frac{7}{10}+\frac{8}{100}$.

$\frac{307}{100}=3{,}07$ : trois unités et sept centièmes.

$6{,}09=\frac{609}{100}$ : six unités font six cents centièmes, puis on ajoute neuf centièmes.

## III. Les zéros

::: attention
Un zéro final peut être omis : $2{,}30=2{,}3$. Un zéro intérieur garde un rang vide : $2{,}03\ne2{,}3$.
:::

## IV. Franchir une unité

En ajoutant un dixième : $45{,}8$, puis $45{,}9$, puis $46$. Dix dixièmes font une nouvelle unité.

::: retenir
Un centime est un centième d’euro. Huit centimes s’écrivent $0{,}08$ euro ; huit dixièmes d’euro s’écrivent $0{,}8$ euro.
:::
''')
image(8,'nouveau',1,'grille_37',MAPS[8]['exercices']['nouveau-11']['1']['alt'])

DOCS[9]=(r'''Titre: Comparer, encadrer et arrondir les décimaux

<!-- optitab:1 -->
::: objectifs
Comparer des nombres décimaux jusqu’aux centièmes, ranger et intercaler des nombres, lire une graduation, distinguer partie entière et arrondi à l’entier.
:::

## I. Comparer des rangs de même valeur

::: methode Partir de la gauche
Comparer d’abord les parties entières. Si elles sont égales, comparer les dixièmes, puis les centièmes. Le premier rang différent décide.
$$
12{,}34>9{,}99
$$
La partie entière suffit ici : douze dépasse neuf.
:::

::: exemple Le piège des longueurs d’écriture
Pour comparer $3{,}5$ et $3{,}45$, écrire $3{,}5=3{,}50$. Cinquante centièmes dépassent quarante-cinq centièmes, donc $3{,}5>3{,}45$. On peut aussi comparer les dixièmes : cinq dixièmes dépassent quatre dixièmes.
:::

::: attention
Le nombre qui possède le plus de chiffres après la virgule n’est pas forcément le plus grand. On ne compare pas 45 et 5 comme des entiers : ce sont quarante-cinq centièmes et cinq dixièmes.
:::

## II. Ranger et lire une graduation

Ranger dans l’ordre croissant, c’est aller du plus petit au plus grand. Sur une demi-droite, cela revient à lire de gauche à droite.

[IMAGE_1]

::: methode Lire le pas avant le point
Entre 5 et 6, dix intervalles égaux donnent un pas d’un dixième. A est à trois pas après 5 : son nombre est $5{,}3$. B est à huit pas : son nombre est $5{,}8$. Le nombre $5{,}45$ se placerait au milieu entre $5{,}4$ et $5{,}5$.
:::

## III. Partie entière, encadrement, intercalation

::: definition Partie entière
Pour un nombre positif, la partie entière compte les unités complètes. Dans $7{,}83$, elle est 7. Les quatre-vingt-trois centièmes ne constituent pas une unité entière supplémentaire.
:::

::: exemple Encadrer et intercaler
Entre deux entiers consécutifs : $7<7{,}83<8$.

On peut intercaler un nombre au centième entre deux dixièmes : $2{,}4<2{,}45<2{,}5$.
:::

::: attention La précision de l’écriture
Entre $8{,}31$ et $8{,}32$, on ne peut pas intercaler un nombre avec **au plus deux chiffres** après la virgule : ce sont deux centièmes consécutifs. Cela ne dit pas que l’intervalle est vide si l’on autorise des écritures plus précises, étudiées plus tard.
:::

## IV. Arrondir à l’entier

::: definition L’entier le plus proche
L’arrondi à l’entier est l’entier le plus proche du nombre. Au milieu exact entre deux entiers, on choisit l’entier supérieur.
:::

::: methode Utiliser le milieu
Le milieu entre 7 et 8 est $7{,}5$. Ainsi, $7{,}3$ s’arrondit à 7 ; $7{,}83$ s’arrondit à 8. Au milieu exact, $12{,}5$ s’arrondit à 13.
:::

::: retenir
La partie entière et l’arrondi sont deux idées différentes : dans $7{,}83$, la partie entière est 7, mais l’arrondi est 8. Comparer les rangs, utiliser les zéros finaux si nécessaire, puis vérifier les bornes.
:::
''',r'''Titre: Synthèse : comparer et arrondir les décimaux

<!-- optitab:1 -->
::: objectifs
Comparer au bon rang et choisir l’entier le plus proche.
:::

## I. Comparer et ranger

1. Comparer les parties entières.
2. Si elles sont égales, comparer les dixièmes, puis les centièmes.
3. Ajouter un zéro final si cela aide : $3{,}5=3{,}50>3{,}45$.

::: attention
Ne pas comparer seulement le nombre de chiffres après la virgule. Les zéros intérieurs sont indispensables : $6{,}08<6{,}8$.
:::

## II. Encadrer et intercaler

La partie entière de $7{,}83$ est 7 : $7<7{,}83<8$.

On peut écrire $2{,}4<2{,}45<2{,}5$. Entre deux centièmes consécutifs, aucune écriture à deux chiffres décimaux ne convient.

## III. Arrondir à l’entier

Repérer le milieu entre les deux entiers voisins. Avant le milieu, prendre l’entier inférieur ; après, l’entier supérieur. Au milieu exact, prendre l’entier supérieur.

::: exemple
$7{,}3$ s’arrondit à 7 ; $7{,}83$ à 8 ; $12{,}5$ à 13.
:::

::: retenir
La partie entière compte les unités complètes. L’arrondi choisit l’entier le plus proche.
:::
''')
image(9,'nouveau',1,'droite_decimale',MAPS[9]['exercices']['nouveau-6']['1']['alt'])

def method(qt,code):
    if qt['m']!='Utiliser le sens des nombres et vérifier chaque rang.':return qt['m']
    text=qt['q'].lower()
    if 'arrond' in text:return 'Repérer les deux entiers voisins et leur milieu, puis choisir le plus proche.'
    if 'partie entière' in text:return 'Compter les unités complètes sans confondre partie entière et arrondi.'
    if 'comparer' in text or 'comparaison' in text:return 'Comparer les valeurs de même rang ou les parts de même taille.'
    if 'ranger' in text or 'classement' in text:return 'Comparer les nombres, puis les écrire dans le sens demandé.'
    if 'encadr' in text:return 'Chercher les deux bornes voisines du rang ou de l’unité demandé.'
    if 'placer' in text or 'point' in text or 'pas' in text:return 'Identifier la valeur d’un intervalle, puis compter les pas depuis un repère connu.'
    if 'fraction' in text and code in (6,7):return 'Identifier l’unité, la taille des parts et le nombre de parts concernées.'
    if 'chiffre' in text or 'rang' in text:return 'Associer chaque chiffre à la valeur du rang qu’il occupe.'
    if 'décompos' in text or 'recompos' in text:return 'Regrouper les unités complètes et conserver la valeur des parts restantes.'
    if code==1:return 'Organiser les unités par rangs ou par paquets, puis vérifier les données de la question.'
    if code in (6,7):return 'Garder la même unité et suivre le nombre de parts égales.'
    return 'Relier unités, dixièmes et centièmes pour conserver la même valeur.'

def write_all():
 for code,items in DATA.items():
    d=next(ROOT.glob(f'{code:02}_*'));source=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
    assert len(items)==len(source['exercices'])==15
    chunks=[];manifest=[]
    for i,e in enumerate(items,1):
        typ='Découverte' if i<=5 else ('Entraînement' if i<=10 else 'Problème')
        diff='easy' if i<=5 else ('medium' if i<=10 else 'hard')
        enonce=e['contexte']+'\n\n'+'\n'.join(f'{j}. '+qt['q'] for j,qt in enumerate(e['questions'],1))
        stages=[]
        for j,qt in enumerate(e['questions'],1):
            stages.append(f"## Question {j} : {qt['q']}\n\n::: methode\n{method(qt,code)}\n:::\n\n::: etape Comprendre et raisonner\n{qt['e']}\n:::\n\n::: resultat\n{qt['r']}\n:::")
        solution='\n'.join(f'{j}. '+qt['r'] for j,qt in enumerate(e['questions'],1))
        chunks.append(f"=== {typ} - {e['titre']}\nId: nouveau-{i}\nDifficulté: {diff}\n\nÉnoncé:\n<!-- optitab:1 -->\n{enonce}\n\nÉtapes:\n<!-- optitab:1 -->\n"+'\n\n'.join(stages)+f'\n\nSolution:\n<!-- optitab:1 -->\n{solution}\n')
        manifest.append({'id':f'nouveau-{i}','source':source['exercices'][i-1]['titre'],'titre':e['titre'],'questions':e['questions']})
    texts={'cours_nouveau.txt':DOCS[code][0],'fiche_nouvelle.txt':DOCS[code][1],'exercices.txt':'\n===\n'.join(chunks)}
    for name,body in texts.items():(d/name).write_text(body.strip()+'\n',encoding='utf-8')
    (d/'verification_questions.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'figures').mkdir(exist_ok=True)
    (d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures originales CM1, style livre, sans exception de chevauchement."""\nFIGURES = '+repr(FIGS[code])+'\n',encoding='utf-8')
    (d/'figures/correspondance.json').write_text(json.dumps(MAPS[code],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'empreintes_finales.json').write_text(json.dumps({name:hashlib.sha256((d/name).read_bytes()).hexdigest() for name in texts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    coverage='\n'.join(f'| {i} | {src["titre"]} | nouveau-{i} : {items[i-1]["titre"]}, cinq questions et cinq raisonnements |' for i,src in enumerate(source['exercices'],1))
    (d/'COUVERTURE.md').write_text('# Couverture du chapitre CM1\n\nLes quinze activités du livre sont conservées dans leur ordre pédagogique et enrichies à cinq questions chacune. Les identifiants sont nouveaux : aucun historique CM1 ne préexistait.\n\n| Source | Activité du livre | Livraison |\n|---|---|---|\n'+coverage+'\n\nProgramme : [BO cycle 3](https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf), sections CM1. Entiers à six chiffres, fractions jusqu’au dénominateur 20 et fractions décimales 10/100, nombres à deux chiffres décimaux au maximum.\n'+('Les sources 7 et 13 demandaient une précision supérieure aux centièmes : remplacement par un travail explicite sur les possibilités d’intercalation au centième. Aucun millième n’est enseigné.\n' if code==9 else ''),encoding='utf-8')
    (d/'RAPPORT.md').write_text('# Rapport CM1\n\nÉtat : textes et figures sources rédigés ; compilation, vérification mathématique et relecture graphique à terminer.\n\n15 exercices enrichis, 75 questions. Chaque question possède méthode, raisonnement, résultat et solution courte. Cours et synthèse au format pilote, explications adaptées au CM1. Les sources locales restent intactes.\n\n'+f'{len(FIGS[code])} schémas TikZ originaux prévus ; correspondance explicite et textes alternatifs précis. Aucun schéma ancien conservé et aucune tolérance de chevauchement.\n\n'+('Corrections : titre borné à 999 999 ; les longueurs géographiques non vérifiées sont des parcours fictifs.\n' if code==1 else 'Corrections : unités de référence explicites et parts égales ; dénominateurs dans la borne CM1.\n')+('Les demandes de millièmes et de densité générale du chapitre source sont remplacées par des intercalations limitées au centième. Arrondi à l’entier uniquement.\n' if code==9 else ''),encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'cm1_nombres','maj':'2026-11-01'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(code,len(items),'exercices',sum(len(e['questions']) for e in items),'questions',len(FIGS[code]),'figures')
if __name__=='__main__':write_all()

