"""Bilans transversaux, méthodes et lexique avec renvois aux chapitres."""
from maquette import *
from programme_complet import E,TITRES
import construire as pilote

BILANS=[
('A','Matière et Système solaire',[
E(1,'Les passages de l’eau',['Nomme le passage solide → liquide et le passage gaz → liquide.','Dans un sachet fermé sans fuite, la masse de la glace est 40 g. Quelle masse d’eau obtient-on après fusion ?'],
    'Les passages sont la fusion et la liquéfaction. On obtient 40 g d’eau après fusion, si l’on considère la même eau sans perte. Le changement d’état conserve la masse dans le système fermé.',figure=('pc_changes',None)),
E(2,'Le contenu d’un flacon',['Un flacon contient eau, sel entièrement dissous et sable visible. Est-il globalement homogène ou hétérogène à l’œil nu ?','Décris deux étapes pour récupérer sable puis sel.'],
    'Le mélange est hétérogène car le sable est visible comme phase distincte. Filtrer pour retenir le sable ; évaporer l’eau du filtrat pour récupérer le sel non volatil. Le filtrat contient encore le sel dissous.'),
E(3,'Deux volumes à lire',['Une éprouvette passe de 26 mL à 40 mL après immersion complète d’un solide. Calcule son volume.','Donne deux conditions nécessaires pour que la mesure corresponde au volume du solide.'],
    'Le solide occupe 40 - 26 = 14 mL, soit 14 cm³. Il doit être complètement immergé, non absorbant, insoluble et sans réaction avec l’eau ; éviter les bulles et tout débordement.',check='40-26==14'),
E(4,'Une conclusion de chimie',['Un gaz trouble l’eau de chaux initialement limpide dans le test fourni. Quelle espèce est présente ?','Pourquoi cela ne prouve-t-il pas que le gaz est pur ?'],
    'Le test indique la présence de dioxyde de carbone dans les conditions fournies. D’autres gaz peuvent être présents dans l’échantillon ; une présence ne démontre pas une pureté.'),
E(5,'Une place dans l’espace',['Classe Soleil, Terre et Lune par catégorie d’astre.','À l’échelle 1 cm pour 50 millions de km, place la Terre dont la distance moyenne au Soleil vaut environ 150 millions de km.'],
    'Soleil : étoile ; Terre : planète ; Lune : satellite naturel de la Terre. La Terre se place à 150 ÷ 50 = 3 cm du Soleil. Les diamètres ne sont pas automatiquement à la même échelle.',check='150/50==3')]),
('B','Mouvement et interactions',[
E(1,'Décrire avec un repère',['Un passager reste assis dans un train. Décris sa situation par rapport au siège puis au quai lorsque le train avance.','Pourquoi les deux descriptions ne se contredisent-elles pas ?'],
    'Il est au repos par rapport au siège et en mouvement par rapport au quai. Les descriptions portent sur des repères différents ; le mouvement doit toujours être associé à un repère.'),
E(2,'Lire des positions',['Les positions sont prises à durées égales. Quelle ligne correspond à une valeur de vitesse constante ?','Quelle ligne montre une augmentation de cette valeur, et sur quel indice t’appuies-tu ?'],
    'A présente des espacements constants. B montre des espacements croissants : davantage de distance est parcourue pendant chaque intervalle de même durée.',figure=('pc_chrono',None)),
E(3,'Un déplacement chiffré',['Un mobile parcourt 90 m en 30 s. Calcule sa vitesse moyenne.','Exprime cette vitesse en km/h.'],
    '90 ÷ 30 = 3 m/s. 3 × 3,6 = 10,8 km/h. Le calcul utilise la distance réellement parcourue et la durée du même trajet.',check='90/30==3 and 3*3.6==10.8'),
E(4,'Un aller avec une pause',['Une sortie fait 2 km en 30 min, pause comprise. Calcule sa vitesse moyenne en km/h.','La moyenne permet-elle d’affirmer une vitesse constante pendant la sortie ?'],
    '30 min = 0,5 h ; 2 ÷ 0,5 = 4 km/h. La moyenne ne prouve pas une vitesse constante ; une pause est même annoncée.',check='2/0.5==4'),
E(5,'Un livre au repos',['Cite deux objets qui interagissent avec un livre posé sur une table, en négligeant l’air.','Classe les interactions en contact ou à distance.'],
    'La table interagit par contact et la Terre à distance. Le repos du livre ne signifie pas absence d’interactions.')]),
('C','Énergie et circuits',[
E(1,'Une chaîne à compléter',['Une pile alimente une lampe. Nomme la réserve initiale et l’effet lumineux recherché.','Indique un autre transfert à ajouter au bilan.'],
    'La pile possède une réserve d’énergie chimique ; la lampe reçoit un transfert électrique et émet de la lumière. Un transfert thermique vers l’environnement doit aussi être considéré.'),
E(2,'Une branche ouverte',['Quelle lampe conserve un chemin fermé avec le générateur ?','Où placer une commande qui coupe les deux lampes ?'],
    'L₂ conserve une boucle fermée ; L₁ est dans la branche ouverte. Une commande générale se place dans une portion commune à tous les chemins, par exemple sur une liaison principale du générateur.',figure=('pc_circuit','parallel_open')),
E(3,'Un test à interpréter',['Un métal peint n’allume pas la lampe d’un circuit de test. Donne une cause possible autre que « le métal est isolant ».','Cite un contrôle indispensable.'],
    'La peinture peut empêcher le contact électrique ; un mauvais contact ou un défaut du montage est aussi possible. Vérifier avec un conducteur témoin dans un montage validé.'),
E(4,'Un bilan de 120 J',['Un appareil sans stockage reçoit 120 J et transfère 45 J utilement. Quelle autre énergie faut-il compter ?','Cette énergie a-t-elle disparu ?'],
    '120 - 45 = 75 J sont transférés autrement. L’énergie n’a pas disparu ; elle peut notamment être transférée thermiquement à l’environnement selon l’appareil.',check='120-45==75'),
E(5,'Une économie documentée',['Deux solutions comparables utilisent 180 kWh et 120 kWh sur une année. Calcule l’économie.','Pourquoi cette comparaison ne constitue-t-elle pas tout le bilan environnemental ?'],
    'L’économie est 60 kWh sur l’année. Il reste à considérer fabrication, durée de vie, transport, réparation et fin de vie, ainsi que la validité du service comparé.',check='180-120==60')]),
('D','Lumière, sons et information',[
E(1,'Expliquer la vision',['Nomme les deux étapes nécessaires pour voir un objet non lumineux éclairé.','Quel sens doit avoir la flèche qui rejoint l’œil ?'],
    'La source éclaire l’objet ; l’objet diffuse une partie de la lumière vers l’œil. La dernière flèche va de l’objet vers l’œil, car la lumière doit y entrer.',figure=('pc_lightchain',None)),
E(2,'Une ombre à prévoir',['Dans quel type de milieu utilise-t-on une propagation rectiligne ?','À source et écran fixes, comment varie l’ombre portée si l’objet se rapproche de la petite source ?'],
    'On utilise le modèle dans un milieu transparent homogène. L’ombre portée grandit dans cette géométrie à petite source, avec le même objet entre source et écran.'),
E(3,'La distance d’un écho',['Un écho revient après 0,5 s. Avec 340 m/s, calcule la distance totale parcourue.','Déduis la distance à l’obstacle dans le modèle aller-retour direct.'],
    'Le trajet total vaut 340 × 0,5 = 170 m. L’obstacle se situe à 85 m, car le son a effectué l’aller et le retour.',check='340*0.5/2==85'),
E(4,'Un code partagé',['Avec A = 10, B = 01, C = 11 et D = 00, décode 11 | 10 | 01.','Chaque valeur dure 1 s. Quelle durée occupent les six valeurs ?'],
    'Le message est CAB. Six valeurs de 1 s durent 6 s, hors préparation. Le code et le repérage des intervalles doivent être partagés.'),
E(5,'Écouter en préservant son audition',['Pourquoi un son apprécié peut-il présenter un risque ?','Cite deux façons de réduire l’exposition.'],
    'Le risque dépend notamment du niveau et de la durée, pas seulement du plaisir d’écoute. Réduire le niveau, limiter la durée, s’éloigner des sources fortes et utiliser les protections adaptées sont des moyens de prévention.')])]

def bilans(b):
    b.c.addOutlineEntry('Bilans des quatre thèmes','bilan-A',0,False)
    for letter,title,items in BILANS:
        part=1;b.begin(f'bilan-{letter}',f'Bilan {letter} · {title}','ÉVALUATION · 5 MISSIONS · 20 POINTS',subtitle='Travaille dans ton cahier. Chaque mission vaut 4 points : 2 points par question.');t=82
        for e in items:
            h=pilote.ex_height(b,e)
            if t+h>274:
                part+=1;b.begin(f'bilan-{letter}-{part}',f'Bilan {letter} · suite','ÉVALUATION · POURSUIVRE ET VÉRIFIER');t=82
            key=f'mission-{letter}-{e.n}';b.dest[key]=b.page;b.c.bookmarkPage(key)
            b.rect(22,t,19,8,fill=NAVY);b.p(f'{letter}.{e.n}',24,t+1.3,15,10.5,font='Bold',color=white);b.link(f'cor-bilan-{letter}',22,t,19,8)
            t=b.p(e.titre,45,t,142,13.4,font='Bold')+5
            if e.figure:t=b.fig(e.figure,t,65)+4
            for i,q in enumerate(e.questions):
                b.p(chr(97+i)+'.',23,t,6,11.8,font='Bold',color=GREEN);t=b.p(q,31,t,157,11.8)+3
            b.line(22,t+2,188);t+=9
        if t<233:b.box('RELIRE AVANT DE CORRIGER','Ai-je précisé les conditions, les unités, le sens des flèches et les étapes du raisonnement ? Une valeur juste sans explication ne répond pas toujours à toute la question.',246,30,size=11.2,fill=MINT,accent=GREEN)

def corrections_bilans(b):
    b.c.addOutlineEntry('Corrigés des bilans','cor-bilan-A',0,False)
    for letter,title,items in BILANS:
        b.begin(f'cor-bilan-{letter}',f'Bilan {letter} · éléments de correction','COMPRENDRE ET ÉVALUER');t=82
        b.p('Barème indicatif : 2 points pour chaque réponse correcte et justifiée. Pour un calcul, valoriser la méthode et l’unité ; pour une explication, les idées exactes et reliées.',22,t,166,11.5);t+=27
        for e in items:
            b.p(f'{letter}.{e.n}',22,t,18,11.5,font='Bold',color=NAVY);b.link(f'mission-{letter}-{e.n}',22,t,18,9)
            t=b.p(e.reponse,44,t,144,11.4)+7
        if t<237:b.box('UTILISER LE RÉSULTAT','Repère la connaissance ou la méthode à reprendre. Reviens au chapitre concerné, puis refais une mission sans regarder la solution avant de comparer.',247,29,size=11.2,fill=MINT,accent=GREEN)

LEXIQUE=[
('Action mécanique','Action pouvant déformer un objet ou modifier son mouvement.',11),
('Air','Mélange de gaz ; dans l’air sec, environ 78 % de diazote et 21 % de dioxygène en volume.',4),
('Boucle','Chemin fermé passant par le générateur et des récepteurs dans un circuit.',13),
('Changement d’état','Transformation physique qui conserve la nature de la substance et modifie son état.',3),
('Circuit ouvert','Circuit dont un trajet est interrompu ; une boucle ouverte ne permet pas le courant.',13),
('Code','Règles partagées qui associent des signaux ou des suites de valeurs à une information.',20),
('Conducteur','Matériau permettant le passage du courant dans les conditions considérées.',14),
('Conservation','Maintien d’une grandeur totale dans les conditions et le système précisés.',3),
('Convertisseur','Dispositif qui reçoit de l’énergie et la transfère sous d’autres formes ou modes.',12),
('Corps pur','Échantillon constitué d’une seule espèce chimique dans le modèle étudié.',4),
('Sens conventionnel du courant','Sens de description du courant dans le circuit extérieur : du + vers le - de la pile.',13),
('Court-circuit','Liaison de très faible résistance qui contourne un dipôle ; celle du générateur présente un risque.',14),
('Décantation','Séparation de phases d’un mélange hétérogène après repos.',6),
('Dérivation','Association avec des branches reliées aux mêmes deux points de connexion.',15),
('Diffusion lumineuse','Renvoi d’une partie de la lumière reçue dans plusieurs directions.',17),
('Dipôle','Composant électrique possédant deux bornes de connexion.',13),
('Dissolution','Dispersion d’un soluté dans un solvant donnant une solution, sans être une fusion.',5),
('Distillation','Séparation avec vaporisation puis liquéfaction d’un constituant recueilli comme distillat.',6),
('Durée','Temps écoulé entre deux dates ; elle peut s’exprimer en secondes.',10),
('Écho','Signal sonore reçu après réflexion ; sa durée peut inclure un aller-retour.',19),
('Émetteur','Objet ou dispositif qui produit le signal transmis.',20),
('Énergie','Grandeur transférée et convertie dans les systèmes ; son unité SI est le joule.',12),
('Espèce chimique','Catégorie de constituants identiques du point de vue chimique.',4),
('Étoile','Astre qui produit la lumière qu’il émet, comme le Soleil.',8),
('Évaporation','Vaporisation à la surface d’un liquide, possible sans ébullition.',3),
('Filtrat','Liquide qui traverse le filtre pendant une filtration.',6),
('Filtration','Séparation par une barrière poreuse retenant certaines particules.',6),
('Fréquence','Nombre de vibrations par seconde pour une vibration périodique ; unité : hertz.',19),
('Fusion','Passage de l’état solide à l’état liquide.',3),
('Générateur','Dipôle qui permet de fournir de l’énergie au circuit, par exemple une pile.',13),
('Homogène','Se dit d’un mélange présentant une seule phase visible à l’échelle considérée.',4),
('Hétérogène','Se dit d’un mélange dont on distingue plusieurs phases ou constituants.',4),
('Hypothèse','Proposition d’explication ou de réponse à mettre à l’épreuve.',1),
('Information','Sens attribué à un signal selon un code et un contexte.',20),
('Interaction','Action mutuelle entre deux objets, de contact ou à distance.',11),
('Isolant','Matériau limitant fortement le passage du courant dans les conditions considérées.',14),
('Liquéfaction','Passage de l’état gazeux à l’état liquide.',3),
('Masse','Grandeur mesurée avec une balance ; unité SI : kilogramme.',2),
('Mélange','Échantillon contenant plusieurs espèces chimiques.',4),
('Ménisque','Courbure de la surface d’un liquide près des parois ; pour l’eau usuelle, lire le bas.',2),
('Miscibilité','Aptitude de deux liquides à former une phase homogène dans les conditions étudiées.',5),
('Modèle','Représentation simplifiée choisie pour expliquer ou prévoir certains phénomènes.',1),
('Vitesse moyenne','Distance totale parcourue divisée par la durée correspondante.',10),
('Niveau sonore','Grandeur liée au son reçu, exprimée en décibels ; différente de la hauteur.',19),
('Ombre portée','Tache obtenue sur un écran à l’intersection avec une zone d’ombre.',18),
('Ombre propre','Partie de la surface d’un objet non directement éclairée par la source considérée.',18),
('Opaque','Se dit d’un matériau qui ne transmet pas perceptiblement la lumière visible dans les conditions étudiées.',17),
('Palier','Portion de courbe pendant laquelle la grandeur reste presque constante.',3),
('Planète','Astre en révolution autour d’une étoile ; il diffuse la lumière reçue.',8),
('Produit','Espèce formée au cours d’une transformation chimique.',7),
('Propagation','Transmission d’une perturbation ou d’un signal depuis une source.',19),
('Puissance','Rythme du transfert d’énergie ; unité SI : watt.',16),
('Rayon lumineux','Trait rectiligne fléché représentant un trajet de lumière dans le modèle.',18),
('Réactif','Espèce consommée au cours d’une transformation chimique.',7),
('Récepteur','Dispositif qui reçoit un signal ; en électricité, dipôle qui reçoit l’énergie transférée.',13),
('Renouvelable','Se dit d’une ressource disponible sous forme de flux ou renouvelée à l’échelle humaine.',16),
('Repère','Référence choisie pour décrire des positions et un mouvement.',9),
('Résidu','Matière retenue sur un filtre ou restant après une opération de séparation.',6),
('Révolution','Mouvement orbital d’un astre autour d’un autre.',8),
('Rotation','Mouvement d’un objet sur lui-même autour d’un axe.',8),
('Satellite naturel','Astre en révolution autour d’une planète ; la Lune est celui de la Terre.',8),
('Saturation','État d’une solution qui ne dissout plus de soluté supplémentaire dans les conditions données.',5),
('Série','Association de dipôles successifs dans une même branche.',15),
('Signal','Variation physique émise, transmise et reçue ; à distinguer de son interprétation.',20),
('Solidification','Passage de l’état liquide à l’état solide.',3),
('Solubilité','Limite de quantité dissoute pour un soluté, un solvant et des conditions précisés.',5),
('Soluté','Substance dissoute dans un solvant.',5),
('Solution','Mélange homogène contenant un solvant et un ou plusieurs solutés.',5),
('Solvant','Liquide dans lequel le soluté se dissout dans les situations du livre.',5),
('Source primaire','Objet qui produit la lumière qu’il émet.',17),
('Système','Objet ou ensemble choisi comme sujet d’étude, avec des limites précisées.',11),
('Tare','Remise à zéro d’une balance avec le récipient afin de mesurer la masse ajoutée.',2),
('Température','Grandeur mesurée avec un thermomètre ; elle est ici exprimée en degré Celsius.',3),
('Trajectoire','Ensemble des positions successives d’un point dans le repère choisi.',9),
('Transformation chimique','Transformation qui consomme des espèces et en forme de nouvelles.',7),
('Translucide','Se dit d’un matériau transmettant de la lumière sans permettre une vision nette à travers.',17),
('Transparent','Se dit d’un matériau permettant une vision nette à travers dans les conditions étudiées.',17),
('Unité','Référence utilisée pour exprimer la mesure d’une grandeur.',2),
('Vaporisation','Passage de l’état liquide à l’état gazeux, par évaporation ou ébullition.',3),
('Volume','Grandeur qui mesure l’espace occupé ; unité SI : mètre cube.',2)
]

def annexes(b):
    b.begin('solutions-1','Activités des chapitres 1 et 2','ÉLÉMENTS DE RÉPONSE',outline=True)
    b.box('CHAPITRE 1 · LE VERRE PROTÈGE-T-IL LE PAPIER ?',
        'Le papier peut rester sec lorsque le gobelet est descendu verticalement : l’air piégé empêche l’eau d’occuper tout l’intérieur. Si le gobelet est assez incliné, des bulles s’échappent et l’eau entre davantage. Ces observations mettent en évidence une matière invisible qui occupe un volume. Un protocole valide doit distinguer les observations de l’explication.',82,57,size=11.8)
    b.box('CHAPITRE 2 · PRÉPARER 50 mL D’EAU',
        'Une masse voisine de 50 g est attendue pour 50 mL d’eau à température ambiante. Les valeurs réelles dépendent de la précision, du ménisque, de la tare et des pertes au transfert. Une table de résultats doit contenir les mesures obtenues, pas des valeurs inventées pour correspondre à la prévision. Comparer les essais et expliquer les écarts avec le protocole.',154,57,size=11.8,fill=MINT,accent=GREEN)
    b.p('Les réponses aux activités ouvertes peuvent varier. Elles doivent rester compatibles avec les faits observés et annoncer les limites du modèle ou de la mesure.',23,243,164,11.7,color=MUTED)
    b.begin('methode-mesure','Mesurer et contrôler un résultat','FICHE MÉTHODE 1',outline=True)
    b.box('1 · CHOISIR','Identifier la grandeur, l’instrument, sa capacité et sa graduation. Une balance mesure une masse ; une éprouvette, un volume ; un thermomètre, une température.',82,33,size=11.8)
    b.box('2 · RELEVER','Effectuer la tare si nécessaire, placer l’œil correctement, attendre la stabilisation et noter toutes les unités. Garder les résultats réellement mesurés.',124,33,size=11.8,fill=MINT,accent=GREEN)
    b.box('3 · COMPARER','Répéter la mesure dans des conditions comparables. Deux valeurs proches peuvent différer à cause de la précision des instruments ou du protocole.',166,33,size=11.8)
    b.box('4 · CONCLURE','Écrire une phrase adaptée à la précision disponible. Ne pas donner une longue suite de décimales qui ne correspond pas à la mesure. Un calcul ne rend pas une graduation plus fine.',208,38,size=11.8,fill=MINT,accent=GREEN)
    b.p('Exemple : si le pas de lecture est 2 mL, un résultat calculé comme 24,000 000 mL ne décrit pas une lecture aussi précise.',23,260,164,11.3,color=MUTED)
    b.begin('methode-graphique','Construire et lire un graphique','FICHE MÉTHODE 2')
    b.bullets(['Identifier la grandeur placée sur chaque axe et son unité.','Choisir des graduations régulières et des échelles lisibles.','Placer les points à partir du tableau ; ne pas inverser les coordonnées.','Décrire la tendance avant de proposer une interprétation.'],82,size=11.8,gap=4)
    b.fig(('pc_speed',None),143,73,caption='Exemple : 0, 3, 6, 9 et 12 m aux dates 0, 1, 2, 3 et 4 s.')
    b.box('UNE LECTURE ARGUMENTÉE','À 2 s, la distance lue est 6 m. La droite passe par l’origine et indique ici une distance proportionnelle à la durée. Le modèle correspond à 3 m parcourus par seconde.',238,37,size=11.7,fill=MINT,accent=GREEN)
    b.begin('methode-calcul','Calculer sans perdre les unités','FICHE MÉTHODE 3')
    b.box('UN EXEMPLE COMPLET','''Question : vitesse moyenne pour 240 m en 2 min.
Données : distance 240 m ; durée 2 min = 120 s.
Méthode : vitesse moyenne = distance ÷ durée.
Calcul : 240 ÷ 120 = 2.
Conclusion : la vitesse moyenne est de 2 m/s.''',82,70,size=12)
    b.bullets(['Choisir les unités avant le calcul.','Garder une durée et une distance qui concernent le même trajet.','Contrôler l’ordre de grandeur et l’unité du résultat.','Pour un trajet par étapes : additionner les distances et les durées avant de calculer la moyenne.'],169,size=11.8,gap=4)
    b.box('UN CONTRÔLE RAPIDE','À 2 m/s pendant 120 s, on retrouve 240 m. Ce retour aux données aide à repérer une inversion de quotient ou une erreur de conversion.',245,30,size=11.5,fill=MINT,accent=GREEN)
    b.begin('unites','Grandeurs, unités et instruments','AIDE-MÉMOIRE',outline=True)
    b.table([
        ['Grandeur','Unité utilisée','Instrument ou document'],
        ['Masse','kg, g','Balance'],['Volume','m³, L, mL','Éprouvette, dimensions'],
        ['Température','°C','Thermomètre'],['Durée','s, min, h','Chronomètre, horloge'],
        ['Distance','m, km','Règle, mètre, carte'],['Vitesse moyenne','m/s, km/h','Distance et durée'],
        ['Énergie','J, Wh, kWh','Bilan ou mesure d’énergie'],['Puissance','W','Document ou mesure adaptée'],
        ['Fréquence','Hz','Acquisition ou document'],['Niveau sonore','dB','Sonomètre ou document']
    ],82,[45,45,76],rowheight=14,size=11.3)
    b.box('NE PAS CONFONDRE','Masse et volume ; durée et date ; vitesse et distance ; énergie et puissance ; fréquence et niveau sonore. Une unité permet souvent de retrouver la grandeur avant tout calcul.',247,30,size=11.5,fill=MINT,accent=GREEN)
    b.begin('conversions','Les équivalences à retrouver','AIDE-MÉMOIRE')
    b.table([['Masses','Volumes','Durées'],['1 kg = 1 000 g','1 L = 1 000 mL','1 h = 60 min'],['1 g = 1 000 mg','1 L = 100 cL','1 min = 60 s'],['0,5 kg = 500 g','1 L = 10 dL','1 h = 3 600 s'],['250 g = 0,25 kg','1 L = 1 dm³','0,5 h = 30 min'],['','1 mL = 1 cm³','1 min 30 s = 90 s']],83,[55,56,55],rowheight=15,size=11.2)
    b.box('VITESSES','1 m/s = 3,6 km/h. Pour convertir de m/s en km/h, multiplier par 3,6 ; pour le trajet inverse, diviser par 3,6.',188,31,size=11.8)
    b.box('ÉNERGIES','1 kWh = 1 000 Wh. Le symbole kWh désigne une énergie ; kW désigne une puissance. Le repère 1 mL d’eau ≈ 1 g à température ambiante n’est pas une conversion universelle entre volume et masse.',230,45,size=11.7,fill=MINT,accent=GREEN)
    # Le tri utilise une clé sans accents pour conserver un ordre alphabétique lisible.
    import unicodedata
    entries=sorted(LEXIQUE,key=lambda q:unicodedata.normalize('NFKD',q[0]).encode('ascii','ignore').decode().lower())
    chunks=[];chunk=[];used=0
    for entry in entries:
        h=12+b.p(entry[1],w=164,size=10.9,measure=True)
        if chunk and used+h>192:chunks.append(chunk);chunk=[];used=0
        chunk.append(entry);used+=h
    if chunk:chunks.append(chunk)
    for part,chunk in enumerate(chunks,1):
        b.begin(f'lexique-{part}','Lexique scientifique',f'COMPRENDRE LES MOTS · {part}/{len(chunks)}',subtitle='Le numéro de chapitre est cliquable et renvoie au cours.',outline=part==1);t=82
        for term,definition,n in chunk:
            b.p(term,22,t,145,11.8,font='Bold',color=NAVY);b.p(f'Ch. {n}',171,t,17,10.4,font='Bold',color=GREEN);b.link(f'ch-{n}-ouverture',170,t,18,8)
            t=b.p(definition,23,t+6,164,10.9)+6
    b.begin('competences','Faire le point sur tes acquis','BILAN PERSONNEL')
    b.p('Reprends les exercices et les bilans après correction. Pour chaque compétence, retrouve un exemple que tu sais expliquer sans regarder la solution.',22,82,166,12)
    t=112
    for title,body in [('DÉCRIRE','Nommer les objets, les substances, les états, les composants et les conditions.'),('EXPÉRIMENTER','Proposer une hypothèse, choisir les témoins et ne changer qu’un facteur à la fois.'),('MESURER','Choisir un instrument, lire ses graduations et exprimer une valeur avec son unité.'),('MODÉLISER','Utiliser des particules, un circuit, une chaîne ou des rayons avec une légende et des limites.'),('ARGUMENTER','Relier une observation à une connaissance, faire un calcul cohérent et nuancer la conclusion.')]:
        b.box(title,body,t,27,size=11.5,fill=PALE if int((t-112)/32)%2==0 else MINT);t+=32
