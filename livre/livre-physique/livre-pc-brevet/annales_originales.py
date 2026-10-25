"""Cinq sujets complets du volet PC, originaux, après étude d'annales officielles.

Aucun document ni énoncé de sujet d'examen n'est repris. Les mesures sont des
données pédagogiques construites pour ces problèmes. Trois parties autonomes.
"""
from dataclasses import dataclass

@dataclass
class Question:
    enonce:str
    reponse:str
    methode:str
    points:float
    bareme:str

@dataclass
class Bloc:
    titre:str
    document:str
    figure:str
    questions:list
    figure_correction:str=''

@dataclass
class Sujet:
    n:int
    titre:str
    chapitres:list
    blocs:list

def Q(e,a,m,p,b):return Question(e,a,m,p,b)
def B(t,d,f,qs,fc=''):
    assert sum(q.points for q in qs)==3
    return Bloc(t,d,f,qs,fc)

SUJETS=[
Sujet(11,'Un monte-charge pour les archives',[1,8,9,14,15],[
B('Suivre la cabine',r'Une cabine et son chargement ont une masse totale de 50 kg. La cabine monte verticalement ; son altitude est relevée toutes les secondes. Pendant la portion étudiée, les frottements sont négligés. On modélise la cabine chargée par un point G soumis à son poids et à la force du câble. $g=9{,}8\unite{N/kg}$.','ann11-positions',[
Q('Décrire le mouvement de la cabine dans le référentiel du bâtiment en justifiant les deux mots employés.',
  'Le mouvement est rectiligne, car la trajectoire est verticale et droite, et uniforme : l’altitude augmente de 0,60 m pendant chaque seconde.',
  'Séparer la forme de la trajectoire et l’évolution de la valeur de la vitesse. Les relevés sont faits à durées égales.',.5,'0,25 pour rectiligne justifié ; 0,25 pour uniforme justifié.'),
Q('Calculer la vitesse moyenne entre 0 s et 3 s.',r'$v=d/\Delta t=1{,}80/3{,}0=0{,}60\unite{m/s}$. La distance parcourue est 1,80 m pendant cette montée.',
  'Utiliser la différence entre les altitudes initiale et finale, puis la durée du même intervalle.',1,'0,5 pour quotient et substitution ; 0,5 pour valeur et unité.'),
Q('Calculer le poids de l’ensemble. Pour le mouvement étudié, les forces se compensent. Représenter sans échelle, au point G, les deux forces et indiquer leur valeur.',
  r'$P=mg=50\times9{,}8=490\unite N$. La force du câble vaut aussi 490 N : verticale vers le haut, opposée au poids vertical vers le bas. Elles agissent ici sur le même système.',
  'La compensation impose deux forces de même direction, de même valeur et de sens opposés. Elle est compatible avec une vitesse constante non nulle.',1.5,'0,5 pour le poids ; 0,5 pour directions et sens ; 0,5 pour égalité des valeurs et représentation.')], 'ann11-forces'),
B('Prévoir l’autonomie',r'Le moteur reçoit une tension continue de 24 V et une intensité de 3,0 A, supposées constantes pendant un cycle complet de 6 min. Une batterie fournit 18 Wh utilisables. Aucun autre appareil ne la sollicite dans le modèle. Relations : $P=UI$, $E=P\Delta t$ ; avec W et h, E est en Wh.','',[
Q('Calculer la puissance électrique reçue par le moteur.',r'$P=24\times3{,}0=72\unite W$.','Multiplier tension en volts et intensité en ampères. Le watt mesure une puissance.',1,'0,5 pour relation et substitution ; 0,5 pour résultat avec unité.'),
Q('Calculer l’énergie électrique nécessaire à un cycle en Wh.',r'$6\unite{min}=6/60\unite h=0{,}10\unite h$ ; $E=72\times0{,}10=7{,}2\unite{Wh}$.','Convertir les minutes en heures avant de multiplier une puissance en watts pour obtenir des Wh.',1,'0,5 pour conversion ; 0,5 pour produit et unité.'),
Q('La batterie permet-elle trois cycles complets ? Justifier, puis donner le nombre maximal de cycles dans ce modèle.',r'Trois cycles demandent $3\times7{,}2=21{,}6\unite{Wh}$, au-delà des 18 Wh disponibles. Deux cycles demandent 14,4 Wh : le maximum est donc deux cycles complets.',
  'Comparer des énergies dans la même unité, puis retenir un nombre entier de cycles. Une fraction de cycle ne constitue pas un cycle complet.',1,'0,5 pour comparaison chiffrée ; 0,5 pour deux cycles justifiés.')], 'ann11-autonomie'),
B('Identifier un liquide de maintenance',r'Le laboratoire pèse un récipient vide : 28,5 g. Le même récipient contenant 100,0 mL d’un liquide a une masse de 102,5 g. Références à la même température : A, 0,74 g/mL ; B, 0,90 g/mL ; C, 1,15 g/mL. On donne $\rho=m/V$.','ann11-pesees',[
Q('Déterminer la masse du liquide seul.',r'$m=102{,}5-28{,}5=74{,}0\unite g$.','La masse totale comprend le récipient et son contenu : retrancher la masse du récipient.',.5,'0,25 pour soustraction ; 0,25 pour valeur et unité.'),
Q('Calculer la masse volumique du liquide et indiquer la référence compatible.',r'$\rho=74{,}0/100{,}0=0{,}740\unite{g/mL}$. La valeur est compatible avec A, aux arrondis des références près.',
  'Conserver les unités g et mL pour comparer directement aux références du document.',1,'0,5 pour quotient et unité ; 0,5 pour comparaison à A.'),
Q('En trois à cinq lignes, expliquer pourquoi cette compatibilité ne prouve pas l’identité chimique du liquide. Proposer un contrôle supplémentaire pertinent.',
  'Une même masse volumique peut correspondre à plusieurs substances ou à un mélange. La mesure possède aussi une incertitude. Il faut comparer une autre propriété indépendante, par exemple une température de changement d’état dans un protocole adapté, ou réaliser une analyse chimique appropriée au laboratoire.',
  'Distinguer « compatible avec » et « prouvé ». Le contrôle doit porter sur une propriété différente et rester adapté au produit étudié.',1.5,'0,5 pour possibilité de substances ou mélanges différents ; 0,5 pour limites de mesure ; 0,5 pour contrôle indépendant pertinent.')])]),
Sujet(12,'Comprendre un détecteur optique de fumée',[3,6,16,17],[
B('Un trajet lumineux modifié',r'Dans ce modèle de détecteur, une DEL émet de la lumière dans une petite chambre. Le capteur est placé hors du faisceau direct. Sans fumée, il ne reçoit presque pas de lumière. Des particules de fumée peuvent diffuser une partie de la lumière vers lui. Le dessin représente la présence de fumée.','ann12-optique',[
Q('Identifier la source primaire de lumière et le récepteur.',
  'La DEL est la source primaire : elle produit la lumière émise. Le capteur est le récepteur de lumière.',
  'Attribuer les rôles en suivant la lumière, de sa production jusqu’à sa détection.',.5,'0,25 pour la DEL ; 0,25 pour le capteur.'),
Q('Reproduire le schéma simplifié et ajouter les deux flèches nécessaires pour expliquer l’arrivée de lumière au capteur.',
  'La première flèche va de la DEL aux particules ; la seconde va des particules vers le capteur. Les particules diffusent une partie de la lumière reçue.',
  'Les flèches indiquent le sens de propagation de la lumière. Le capteur n’envoie pas de rayon pour chercher la fumée.',1,'0,5 par trajet fléché correctement orienté.'),
Q('En trois à cinq lignes, expliquer pourquoi le capteur est placé hors du faisceau direct. Pourquoi de la poussière peut-elle aussi perturber ce modèle ?',
  'Hors du faisceau direct, le capteur reçoit peu de lumière en l’absence de particules. Une augmentation de lumière reçue peut donc indiquer une diffusion par des particules. La poussière peut également diffuser de la lumière : cette seule mesure ne donne pas l’identité chimique des particules.',
  'Relier le placement du capteur au signal de référence, puis séparer détection d’une présence et identification de sa nature.',1.5,'0,5 pour faible signal sans particules ; 0,5 pour diffusion ; 0,5 pour limite liée à la poussière.')], 'ann12-optique-cor'),
B('Raisonner sur une combustion',r'Une combustion complète du propane est modélisée par $\ce{C3H8 + 5 O2 -> 3 CO2 + 4 H2O}$. Le document ne modélise pas la formation de fumée ni les produits d’une combustion incomplète.','ann12-molecules',[
Q('Nommer le combustible et le comburant de cette réaction.',
  'Le propane est le combustible ; le dioxygène est le comburant.', 'Repérer la substance qui brûle et le réactif qui permet la combustion.',.5,'0,25 pour chacun des deux noms.'),
Q('Vérifier la conservation des atomes d’oxygène de part et d’autre de l’équation.',
  'À gauche, 5 molécules de dioxygène apportent 10 atomes O. À droite, 3 molécules de dioxyde de carbone apportent 6 atomes O et 4 molécules d’eau en apportent 4 : total 10.',
  'Multiplier le nombre devant la formule par le nombre d’atomes O dans une molécule, puis additionner les produits.',1,'0,5 pour le décompte à gauche ; 0,5 pour celui à droite.'),
Q('Pendant un essai, le réservoir perd 4,4 g de propane. Un élève en déduit que la masse totale des produits formés vaut 4,4 g. Peut-on valider sa conclusion ? Identifier la masse oubliée et écrire le bilan de masse complet, sans calcul numérique.',
  r'Non : la réaction consomme aussi du dioxygène prélevé dans l’air. Sa masse doit être ajoutée à celle du propane consommé. Pour la transformation complète du document : $m_{\rm propane}+m_{\rm dioxygène}=m_{\rm dioxyde\ de\ carbone}+m_{\rm eau}$. La seule perte du réservoir ne donne pas la masse totale des produits.',
  'Définir la frontière du système pesé : le réservoir ne contient pas tout le dioxygène consommé. La conservation porte sur tous les réactifs et tous les produits, pas sur la seule masse de combustible.',1.5,'0,5 pour rejet justifié ; 0,5 pour dioxygène oublié ; 0,5 pour bilan complet.')], 'ann12-bilan'),
B('Recevoir le signal sonore',r'Un essai en plein air utilise un signal bref. Un microphone est situé à 51 m de l’émetteur. On néglige le vent et les réflexions ; la vitesse du son est $340\unite{m/s}$. Deux enregistrements A et B portent sur une même durée de 4 ms.','ann12-son',[
Q('Calculer la durée de propagation directe entre l’émetteur et le microphone.',r'$\Delta t=d/v=51/340=0{,}15\unite s$.','Il s’agit d’un trajet simple : aucune division par deux n’intervient.',1,'0,5 pour quotient ; 0,5 pour durée et unité.'),
Q('Quel enregistrement correspond au son le plus aigu ? Justifier sans confondre fréquence et amplitude.',
  'B correspond au son le plus aigu : il présente quatre oscillations pendant les 4 ms, contre deux pour A. Les amplitudes dessinées sont égales.',
  'Comparer le nombre d’oscillations sur une même durée. Une plus grande amplitude ne signifie pas un son plus aigu.',1,'0,5 pour B ; 0,5 pour comparaison à durée égale.'),
Q('Le son pourrait-il se propager de la même manière dans le vide ? Justifier.',
  'Non. Le son est une perturbation mécanique qui nécessite un milieu matériel pour se propager. Le vide ne fournit pas ce milieu.',
  'Distinguer la propagation du son de celle de la lumière, qui peut se propager dans le vide.',1,'0,5 pour réponse ; 0,5 pour milieu matériel nécessaire.')], 'ann12-son-cor')]),
Sujet(13,'Une station météo sur la côte',[2,6,13,14,18],[
B('Connaître l’air prélevé',r'Un flacon contient 2,0 L d’air sec. Le modèle utilise 78 % de diazote, 21 % de dioxygène et 1 % d’autres gaz en volume. L’azote possède $Z=7$ ; l’isotope étudié possède $A=14$. La formule du diazote est $\ce{N2}$.','ann13-air',[
Q('L’air sec est-il un corps pur ou un mélange ? Justifier.',
  'C’est un mélange : il contient plusieurs espèces chimiques, dont le diazote et le dioxygène.',
  'La transparence et l’aspect uniforme ne prouvent pas qu’un gaz est un corps pur.',.5,'0,25 pour mélange ; 0,25 pour pluralité des espèces.'),
Q('Calculer le volume de dioxygène du prélèvement, en litre puis en millilitres.',r'$V=0{,}21\times2{,}0=0{,}42\unite L=420\unite{mL}$.',
  'Appliquer la proportion au volume total, puis convertir les litres en millilitres.',1,'0,5 pour produit ; 0,5 pour valeurs et conversion.'),
Q('Donner les nombres de protons, de neutrons et d’électrons d’un atome neutre d’azote de cet isotope. Combien d’atomes contient une molécule de diazote ?',
  'L’atome possède 7 protons, 14 − 7 = 7 neutrons et 7 électrons car il est neutre. Une molécule de diazote contient deux atomes d’azote.',
  'Z compte les protons ; A compte protons et neutrons. La neutralité impose autant d’électrons que de protons. L’indice 2 porte sur les atomes de la molécule.',1.5,'0,25 pour chacun des trois inventaires ; 0,25 pour neutralité justifiée ; 0,5 pour deux atomes.')], 'ann13-atome'),
B('Tester un composant résistif',r'Le graphique présente des mesures sur un conducteur ohmique. On utilise $U=RI$ avec U en V, I en A et R en ohms. Le montage de principe du corrigé sera réalisé uniquement avec le matériel scolaire adapté.','ann13-ohm',[
Q('Lire la tension correspondant à une intensité de 30 mA.',r'$U=6{,}0\unite V$ pour $I=30\unite{mA}$.','Partir de 30 mA sur l’axe horizontal, rejoindre la droite puis lire la tension sur l’axe vertical.',.5,'0,5 pour lecture et unité.'),
Q('Calculer la résistance à partir de ce point.',r'$30\unite{mA}=0{,}030\unite A$ ; $R=6{,}0/0{,}030=200\unite\Omega$.',
  'Convertir les milliampères en ampères avant d’appliquer la loi d’Ohm.',1,'0,5 pour conversion et quotient ; 0,5 pour résultat et unité.'),
Q('Schématiser un montage permettant ces mesures avec générateur, résistance, ampèremètre et voltmètre. Préciser leurs branchements.',
  'L’ampèremètre se place en série dans la branche de la résistance ; le voltmètre se branche en dérivation entre les deux bornes de la résistance. Les bornes A et V sont du côté des potentiels les plus élevés, les bornes COM de l’autre côté, pour des lectures positives.',
  'Mesurer I impose de traverser l’ampèremètre. Mesurer U impose de comparer deux points du circuit : le voltmètre relie ces deux points.',1.5,'0,5 pour boucle et résistance ; 0,5 pour ampèremètre en série ; 0,5 pour voltmètre en dérivation.')], 'ann13-mesures'),
B('Transmettre un message',r'La station envoie un signal radio à un relais distant de 120 km. La vitesse retenue est $3{,}0\times10^8\unite{m/s}$. Le message d’étude comporte quatre symboles avec le code A = 10, B = 01, C = 11, D = 00 ; il est composé de huit intervalles de 2 ms. La durée de préparation n’est pas incluse.','ann13-code',[
Q('Décoder les quatre groupes représentés sur le document.', 'Le message est CADB : 11 → C, 10 → A, 00 → D, 01 → B.',
  'Lire chaque groupe depuis le début annoncé ; ne pas décaler le découpage en groupes de deux.',.5,'0,5 pour les quatre symboles dans l’ordre.'),
Q('Calculer la durée totale d’émission du message.',r'$8\times2=16\unite{ms}=0{,}016\unite s$.',
  'Compter les huit intervalles, et non seulement les intervalles codés 1. Le zéro occupe lui aussi du temps.',1,'0,5 pour huit intervalles ; 0,5 pour produit et unité.'),
Q('Calculer la durée de propagation du début du message jusqu’au relais. Expliquer pourquoi elle diffère de la durée d’émission.',
  r'$120\unite{km}=120\,000\unite m$ ; $\Delta t=120\,000/(3{,}0\times10^8)=4{,}0\times10^{-4}\unite s=0{,}40\unite{ms}$. Cette durée est le trajet d’un front du signal, tandis que les 16 ms correspondent à l’émission des huit valeurs successives.',
  'Faire le calcul en mètres et secondes. Un message long peut commencer à arriver avant que son émission soit terminée.',1.5,'0,5 pour conversion ; 0,5 pour quotient, valeur et unité ; 0,5 pour distinction des durées.')], 'ann13-radio')]),
Sujet(14,'Transporter un colis réfrigéré',[1,2,4,8,11],[
B('Étudier une réserve froide',r'Un sachet étanche contient 200 g d’eau pure initialement solide. Sous la pression usuelle, le professeur suit sa température pendant un apport d’énergie. Le sachet reste fermé, sans fuite ; on mesure ici la température de l’eau dans ses différents états.','ann14-fusion',[
Q('Nommer le changement d’état au palier de 0 °C et indiquer les états qui coexistent.',
  'Il s’agit de la fusion. Pendant ce palier, l’eau solide et l’eau liquide coexistent dans le modèle.',
  'Le sens d’évolution compte : la température venait d’une valeur négative pendant un apport d’énergie.',1,'0,5 pour fusion ; 0,5 pour coexistence solide–liquide.'),
Q('Lire la durée du palier et prévoir la masse d’eau après fusion complète.',
  'Le palier dure 6 − 2 = 4 min. La masse d’eau reste 200 g : la même eau est conservée sans fuite.',
  'Une durée est une différence de dates. La conservation de la masse concerne le système fermé, même quand son état change.',1,'0,5 pour durée ; 0,5 pour masse justifiée.'),
Q('Un élève affirme : « La température ne change plus, donc l’eau ne reçoit plus d’énergie. » Discuter cette affirmation.',
  'L’affirmation est fausse dans cette expérience. L’apport d’énergie se poursuit et permet le changement d’état ; pendant la fusion d’un corps pur à pression fixée, la température peut rester constante.',
  'Une température constante ne signifie pas l’absence de transfert d’énergie. Relier l’apport au changement d’état observé.',1,'0,5 pour affirmation rejetée ; 0,5 pour énergie du changement d’état.')], 'ann14-fusion-cor'),
B('Analyser un liquide de conditionnement',r'Un autre prélèvement de liquide présente un pH de 8,0 vers 25 °C. La fiche de test indique : nitrate d’argent + ions chlorure → précipité blanc. Après ajout du réactif à un prélèvement séparé, un précipité blanc apparaît. Pour le chlore, $Z=17$. Les tests sont réalisés au laboratoire sous la conduite du professeur.','ann14-test',[
Q('Classer le liquide selon son pH et justifier.', 'Il est basique : le pH 8,0 est supérieur à 7 vers 25 °C.',
  'Comparer le pH à 7 à la température précisée. Une valeur voisine de 7 n’est pas forcément exactement neutre.',.5,'0,25 pour basique ; 0,25 pour comparaison à 7.'),
Q('Identifier l’ion mis en évidence et donner son nombre d’électrons.',r'Le test met en évidence l’ion chlorure $\ce{Cl-}$. Avec 17 protons et une charge $-1$, il possède 18 électrons.',
  'Un ion négatif possède un excès d’électrons. La charge ne change pas le numéro atomique de l’élément.',1,'0,5 pour identification ; 0,5 pour 18 électrons justifiés.'),
Q('En trois à cinq lignes, expliquer ce que permettent les résultats et ce qu’ils ne prouvent pas sur la composition et l’innocuité du liquide.',
  'Les résultats indiquent un liquide basique dans ces conditions et la présence d’ions chlorure dans la limite du test. Ils ne donnent pas tous les constituants ni leur quantité. Ils ne suffisent pas à garantir l’innocuité : il faut d’autres analyses et les informations adaptées sur le produit et son usage.',
  'Séparer trois conclusions : acidité/basicité, présence d’une espèce et évaluation d’un risque. Un test positif ne démontre pas la pureté ni l’absence d’autres substances.',1.5,'0,5 pour les deux résultats exacts ; 0,5 pour composition non exhaustive ; 0,5 pour innocuité non démontrée.')], 'ann14-ion'),
B('Limiter la vitesse sur un convoyeur',r'Le colis de masse 2,0 kg se déplace en ligne droite sur un convoyeur. Une phase à vitesse constante est comparée à deux réglages : 0,50 m/s et 1,0 m/s. On donne $E_c=\frac12mv^2$, avec les unités SI.','ann14-convoyeur',[
Q('Quelle distance parcourt le colis en 8,0 s à 0,50 m/s constants ?',r'$d=v\Delta t=0{,}50\times8{,}0=4{,}0\unite m$.',
  'Multiplier la vitesse par la durée seulement pour la portion où la vitesse garde la valeur annoncée.',1,'0,5 pour relation et produit ; 0,5 pour distance avec unité.'),
Q('Calculer l’énergie cinétique du colis pour chacun des deux réglages.',r'À 0,50 m/s : $E_c=0{,}5\times2{,}0\times0{,}50^2=0{,}25\unite J$. À 1,0 m/s : $E_c=1{,}0\unite J$.',
  'Mettre toute la valeur de la vitesse au carré. Une masse en kilogrammes et une vitesse en m/s donnent une énergie en joules.',1,'0,5 pour chaque calcul avec unité.'),
Q('Le doublement de vitesse double-t-il l’énergie cinétique ? Justifier, puis expliquer l’intérêt de limiter la vitesse.',
  'Non : à masse constante, doubler la vitesse multiplie l’énergie cinétique par quatre. À vitesse plus faible, il y a moins d’énergie cinétique à transférer lors d’un arrêt ou d’un choc, toutes choses égales par ailleurs.',
  'Comparer les deux énergies calculées et relier le facteur quatre au carré de la vitesse.',1,'0,5 pour facteur quatre ; 0,5 pour intérêt formulé en termes d’énergie.')], 'ann14-energies')]),
Sujet(15,'Une maquette de dirigeable',[2,9,13,14,15],[
B('Décrire le gaz de l’enveloppe',r'La maquette contient de l’hélium modélisé par des atomes neutres séparés. L’isotope représenté possède $Z=2$ et $A=4$. Les points du modèle ne sont pas dessinés à la taille réelle des atomes.','ann15-helium',[
Q('Donner les nombres de protons, de neutrons et d’électrons de cet atome.', 'Il possède 2 protons, 4 − 2 = 2 neutrons et 2 électrons puisqu’il est neutre.',
  'Utiliser Z, puis A − Z, puis la neutralité électrique ; A ne compte pas les électrons.',1,'0,25 pour protons ; 0,25 pour neutrons ; 0,5 pour électrons et neutralité.'),
Q('Le modèle représente-t-il un gaz constitué de molécules de plusieurs atomes ? Justifier.',
  'Non : les entités décrites sont des atomes d’hélium isolés. Il s’agit ici d’un gaz monoatomique.',
  'Une entité n’est pas nécessairement une molécule : tenir compte de la nature du gaz indiquée dans le document.',1,'0,5 pour non ; 0,5 pour atomes isolés.'),
Q('Après compression douce sans fuite, à température redevenue identique, le nombre d’atomes diminue-t-il ? Expliquer la modification du modèle.',
  'Le nombre d’atomes ne diminue pas : aucun gaz n’a quitté le système. On représente les mêmes atomes, de même taille conventionnelle, dans un volume plus petit ; leurs espacements moyens diminuent.',
  'Distinguer la taille des entités, leur nombre et l’espace disponible. Une compression ne détruit pas des atomes.',1,'0,5 pour conservation du nombre ; 0,5 pour réduction des espacements.')], 'ann15-compression'),
B('Équilibrer la maquette',r'La masse totale est de 0,30 kg. Le modèle retient le poids vertical vers le bas et une force de l’air verticale vers le haut de 3,4 N. Le dirigeable peut être retenu par un fil vertical ancré au sol. On donne $g=10\unite{N/kg}$.','ann15-forces-enonce',[
Q('Calculer le poids total de la maquette.',r'$P=mg=0{,}30\times10=3{,}0\unite N$.',
  'La masse est déjà en kilogrammes ; le produit par g donne un poids en newtons.',.5,'0,25 pour produit ; 0,25 pour résultat avec unité.'),
Q('Sans fil, les deux forces indiquées se compensent-elles ? Justifier.',
  'Non : leurs valeurs sont différentes, 3,4 N vers le haut et 3,0 N vers le bas. La résultante du modèle vaut 0,4 N vers le haut.',
  'Deux forces opposées ne se compensent que si leurs valeurs sont égales.',1,'0,5 pour comparaison des valeurs ; 0,5 pour résultante vers le haut.'),
Q('Le fil permet de maintenir le dirigeable immobile. Déterminer la valeur et le sens de sa force sur la maquette, puis représenter les trois forces sans échelle.',
  'Le fil exerce une force de 0,4 N vers le bas. Avec le poids, la somme des forces vers le bas vaut 3,0 + 0,4 = 3,4 N, égale à la force de l’air vers le haut.',
  'Isoler le dirigeable comme système. Le fil ancré au sol tire la maquette vers le bas ; il ne la pousse pas vers le haut.',1.5,'0,5 pour sens ; 0,5 pour 0,4 N justifié ; 0,5 pour schéma complet.')], 'ann15-forces-cor'),
B('Alimenter les accessoires',r'Un générateur adapté fournit une tension constante de 6,0 V à deux branches en dérivation : moteur, 0,20 A ; éclairage, 0,10 A. Les courants restent constants dans le modèle. La batterie fournit 1,8 Wh utilisables. On donne $P=UI$ et $E=P\Delta t$.','ann15-circuit',[
Q('Donner la tension aux bornes de chaque branche et calculer l’intensité fournie par le générateur.',r'Chaque branche reçoit 6,0 V. L’intensité totale est $I=0{,}20+0{,}10=0{,}30\unite A$.',
  'En dérivation, la tension est commune aux branches et le courant principal est la somme des courants de branche.',1,'0,5 pour tension commune ; 0,5 pour intensité totale.'),
Q('Calculer la puissance totale et la durée maximale d’alimentation dans ce modèle.',r'$P=6{,}0\times0{,}30=1{,}8\unite W$ ; $\Delta t=E/P=1{,}8/1{,}8=1{,}0\unite h$.',
  'Une énergie en Wh divisée par une puissance en W donne une durée en heures. La capacité fournie est déjà l’énergie utilisable.',1,'0,5 pour puissance ; 0,5 pour durée avec unité.'),
Q('La branche de l’éclairage devient ouverte. Le moteur est-il nécessairement arrêté ? Expliquer avec le schéma.',
  'Non, dans le modèle à générateur adapté et tension maintenue. La branche du moteur conserve une boucle fermée entre les bornes du générateur. Seule la branche d’éclairage est interrompue.',
  'Suivre un trajet complet incluant le générateur pour chaque branche. Une ouverture dans une branche ne coupe pas automatiquement les autres.',1,'0,5 pour réponse ; 0,5 pour boucle du moteur conservée.')], 'ann15-circuit-cor')]),
]

CALCULS=[
 ('1.8/3',.6),('50*9.8',490),('24*3',72),('72*6/60',7.2),('3*7.2',21.6),('2*7.2',14.4),('102.5-28.5',74),('74/100',.74),
 ('51/340',.15),('0.21*2',.42),('6/.03',200),('8*2',16),('120000/3e8',.0004),
 ('6-2',4),('.5*8',4),('.5*2*.5**2',.25),('.5*2*1**2',1),('.3*10',3),('3.4-3',.4),('.2+.1',.3),('6*.3',1.8),('1.8/1.8',1),
]

def figures_utilisees():return {f for s in SUJETS for b in s.blocs for f in [b.figure,b.figure_correction] if f}

def documents():
    from construire import page,box,figure_ex
    s=r'\global\otCorrigesfalse\global\otSouplefalse\gdef\otAccent{otNavy}\pcAnnexe{Cinq sujets format annales}{Physique-chimie · 30 minutes · Sujets originaux 11 à 15}\phantomsection\label{annales-originales}\pdfbookmark[0]{Cinq sujets au format des annales}{bm-annales-originales}'+'\n'
    s+=box('Des sujets complets pour composer','Chaque sujet contient trois parties indépendantes, neuf questions et tous les documents nécessaires. Durée conseillée : 30 minutes. Le total est de 9 points scientifiques, complétés par 1 point de langue selon la grille du livre. Les contextes, les mesures, les questions et les figures ont été créés pour ces entraînements. Ce ne sont pas des annales officielles reproduites.','method')
    s+=r'''\pcSousTitre{Un parcours en trois temps}
Prévoir environ 8 minutes par partie, puis 6 minutes pour lire et relire l’ensemble. Une réponse justifiée compte davantage qu’une valeur isolée. Les relations utiles et les hypothèses du modèle figurent dans les documents. Les schémas sans échelle ne doivent pas être mesurés à la règle.
\pcSousTitre{Après la composition}
Pour chaque question, le corrigé distingue la réponse, la démarche et les critères du barème. Garder les étapes justes même si une erreur de calcul se propage. Les points d’une même erreur ne sont pas retirés deux fois. Le point de langue porte sur l’ensemble des réponses, sans imposer un texte inutilement long.
'''
    for x in SUJETS:s+=rf'\pcRepere{{ann-{x.n}}}{{Sujet {x.n} · {x.titre}}}'+'\n'
    for x in SUJETS:
        for k,b in enumerate(x.blocs,1):
            s+=page(f'Sujet {x.n} · Énoncé',x.titre,f'ann-{x.n}' if k==1 else '')
            if k==1:s+=rf'\pdfbookmark[1]{{{x.n} · {x.titre}}}{{bm-ann-{x.n}}}'+'\n'
            s+=rf'\textbf{{PC · 30 min · /10}}\hfill Partie {k}/3 · 3 points scientifiques'+'\n'
            s+=box('Document · '+b.titre,b.document)
            if b.figure:s+=figure_ex(b.figure,'Document original · données pédagogiques. Schéma sans échelle, sauf axes gradués.')
            for j,q in enumerate(b.questions,1):
                n=(k-1)*3+j;pt=str(q.points).replace('.',',')
                s+=r'\par\addvspace{3mm}\noindent\begin{minipage}{\linewidth}\textbf{'+f'Question {n} · {pt} point'+('s' if q.points>1 else '')+r'}\quad '+q.enonce+r'\par\end{minipage}\par'+'\n'
            s+=r'\vfill'+rf'\pcRepere{{cor-ann-{x.n}}}{{Corrigé expliqué, barème et bilan}}'+'\n'
    s+=r'\global\otCorrigestrue\global\otSoupletrue\gdef\otAccent{otGreenDark}\pcAnnexe{Corrigés des sujets 11 à 15}{Comprendre le modèle, les calculs et les critères de réussite}\phantomsection\label{cor-annales-originales}\pdfbookmark[0]{Corrigés des sujets 11 à 15}{bm-cor-annales-originales}'+'\n'
    s+=box('Une grille pour progresser','Chaque sujet : partie 1 /3, partie 2 /3, partie 3 /3 et langue /1, soit /10. Relire d’abord la démarche avant d’attribuer les points. Repérer une erreur de modèle, une erreur de lecture et une erreur d’unité si elles existent, puis choisir un exercice du cours pour reprendre la difficulté.','method')
    for x in SUJETS:
        for k,b in enumerate(x.blocs,1):
            s+=page(f'Corrigé du sujet {x.n}',b.titre,f'cor-ann-{x.n}' if k==1 else '')
            s+=rf'\pcRepere{{ann-{x.n}}}{{Revenir à l’énoncé}}'+'\n'
            for j,q in enumerate(b.questions,1):
                n=(k-1)*3+j
                s+=r'\par\noindent\begin{minipage}{\linewidth}\pcSousTitre{'+f'Question {n}'+r'}'+q.reponse+r'\par\smallskip\textbf{Démarche.}\enspace '+q.methode+r'\par\smallskip{\small\textbf{Barème.}\enspace '+q.bareme+r'\par}\end{minipage}\par'+'\n'
            if b.figure_correction:s+=figure_ex(b.figure_correction,'Modèle de correction · les légendes précisent les directions, les connexions ou les résultats.')
            if k==3:
                refs=' ; '.join(rf'\hyperref[chap-{n}]{{chapitre {n} (p.~\pageref*{{chap-{n}}})}}' for n in x.chapitres)
                s+=r'\par\noindent\begin{minipage}{\linewidth}{\small\textbf{Bilan :} /3 + /3 + /3 + /1 = /10.\par\textbf{Pour reprendre :} '+refs+r'.\par}\end{minipage}\par'+'\n'
    s+=page('Sources des sujets 11 à 15','Des attendus étudiés, des documents et des problèmes nouveaux','sources-annales')
    s+=box('Ce qui a été étudié','Les annales officielles servent à analyser la place des documents, les changements d’unité, le raisonnement progressif, les constructions et les réponses argumentées. Le volet PC du sujet 2025 consulté est noté sur 25, celui de 2026 sur 10. Pour ces entraînements 2027, les critères scientifiques et le point de langue suivent le cadre actuel et restent séparés.','method')
    s+=r'''\pcSousTitre{Sources primaires consultées le 24 octobre 2026}
\begin{questions}
\item Ministère de l’Éducation nationale, DNB 2025, sciences, série générale, sujet 25GENSCAN1 : analyse de la progression des questions, des documents et de la tâche de synthèse.
\item Ministère de l’Éducation nationale, DNB 2026, sciences, série générale, sujet 26GENSCAN1 : analyse de l’usage de mesures et de documents indépendants.
\item Éduscol, sujet de référence de physique-chimie pour le DNB 2027 : analyse des attendus de rédaction et des critères de réponse.
\item Bulletin officiel, note du 11 septembre 2026, NOR MENE2623228N, partie I.4 : durée et modalités de sciences applicables à compter de la session 2027.
\end{questions}
\pcSousTitre{Consulter les documents officiels}
{\small\url{https://eduscol.education.gouv.fr/5607/les-epreuves-du-dnb}\par
\url{https://www.education.gouv.fr/bo/2026/Hebdo4/MENE2623228N}\par
\url{https://www.education.gouv.fr/brevet-bac-et-cap-les-sujets-des-examens-2026-504911}\par}
\pcSousTitre{Des choix éditoriaux explicites}
Le monte-charge, le détecteur optique, la station météo, le colis réfrigéré et le dirigeable constituent cinq dossiers originaux. Les séries numériques et les schémas ont été construits pour ces exercices. Aucun sujet n’annonce les thèmes qui seront retenus à l’examen. La concordance générale du programme figure dans les annexes du manuel.
'''
    return s
