"""Énergie et circuits : situations concrètes et raisonnement qualitatif en 5e."""
from programme_complet import *

C12=Chapitre(12,'D’où vient l’énergie qui fait fonctionner une lampe ?',[
    'Distinguer ressource, réserve, forme d’énergie et convertisseur.',
    'Décrire une chaîne de transferts et de conversions.',
    'Distinguer transfert utile et autres transferts sans faire disparaître l’énergie.'
],[
Lecon('Identifier les sources et les réserves',
    'Un objet qui fonctionne reçoit de l’énergie ou utilise une réserve. Une pile stocke de l’énergie chimique ; des aliments constituent une réserve chimique pour le corps ; de l’eau retenue en hauteur possède une énergie liée à sa position. Soleil, vent, eau en mouvement et combustibles sont des ressources mobilisées dans différents dispositifs. L’électricité est une façon de transférer de l’énergie, pas une ressource primaire extraite telle quelle.',
    ('pc_resources',None),'Quelques ressources utilisées pour l’énergie. La classification concerne leur renouvellement à l’échelle humaine.',
    'Distinguer la ressource et l’appareil : le vent est une ressource ; l’éolienne est un convertisseur. Le mot énergie n’est pas synonyme de courant électrique.',
    'Demander « d’où vient l’énergie ? » puis « quel dispositif la convertit ? ». Nommer chaque élément au lieu de répondre seulement « c’est électrique ».'),
Lecon('Suivre une conversion',
    'Un convertisseur reçoit de l’énergie et la transfère sous d’autres formes ou par d’autres modes de transfert. Une lampe alimentée reçoit de l’énergie par transfert électrique ; elle émet de la lumière et transfère aussi de l’énergie à son environnement sous forme thermique. Un moteur permet notamment de mettre un objet en mouvement. Une chaîne énergétique représente une sélection de ces étapes avec des flèches légendées.',
    ('pc_energy',['Pile','Lampe','Lumière','Transfert\nthermique']),'La pile fournit un transfert électrique à la lampe ; les deux sorties sont des transferts d’énergie vers l’environnement.',
    'Une flèche de chaîne énergétique représente un transfert d’énergie, pas le déplacement d’une substance et pas nécessairement le sens du courant dans un circuit.',
    'Écrire le nom du convertisseur dans la case et la nature du transfert sur les flèches. Vérifier que les sorties ne se limitent pas au seul effet recherché.'),
Lecon('L’énergie ne disparaît pas',
    'Dans un bilan d’énergie, on compte les transferts entrants, les transferts sortants et les variations des réserves. Si un appareil ne stocke pas d’énergie pendant l’intervalle étudié, l’énergie reçue est égale au total de l’énergie transférée. Le joule (J) est l’unité du Système international pour l’énergie. Une énergie dite perdue reste transférée, souvent vers l’environnement sous une forme moins utile pour l’objectif choisi.',
    ('pc_budget',None),'Bilan pédagogique d’un appareil sans variation de réserve : 100 J reçus, 30 J utiles et 70 J par un autre transfert.',
    'Le caractère utile dépend du but : un transfert thermique est recherché pour chauffer, mais peut être secondaire pour éclairer.',
    'Avant d’additionner, vérifier que toutes les valeurs concernent la même durée et la même unité, puis rechercher un éventuel stockage.')
],Activite('Construire une chaîne énergétique',
    'Comparer les fonctions d’une lampe et d’un petit moteur scolaires.',[
    'À partir de documents ou de matériels de classe compatibles, identifier le générateur et le récepteur. Les montages sont validés par le professeur.',
    'Décrire l’effet recherché : lumière ou mouvement. Rechercher aussi les autres transferts, sans toucher une partie qui pourrait être chaude.',
    'Dessiner pour chaque appareil une chaîne comportant la source ou réserve, le convertisseur et les transferts sortants.'
],('pc_energy',['Pile','Moteur','Mouvement','Transfert\nthermique']),
    'Le schéma décrit les transferts d’énergie ; il ne remplace pas un schéma électrique.',[
    'Qu’est-ce qui change entre la chaîne de la lampe et celle du moteur ?',
    'Pourquoi une sortie thermique peut-elle apparaître dans les deux chaînes ?',
    'Quelle réserve diminue lorsque la pile alimente le montage ?'
], 'Le convertisseur et l’effet utile changent : la lampe émet de la lumière, le moteur met un objet en mouvement. Les deux appareils peuvent aussi transférer de l’énergie thermiquement à leur environnement. La réserve d’énergie chimique de la pile diminue. Le schéma doit montrer cette origine et éviter de faire disparaître les transferts secondaires.'),[
    'Une ressource ou une réserve fournit l’énergie utilisée.',
    'Un convertisseur modifie les formes ou les modes de transfert de l’énergie.',
    'Une chaîne énergétique utilise des flèches légendées.',
    'L’énergie s’exprime notamment en joules, symbole J.',
    'Une énergie moins utile pour un objectif n’a pas été détruite.'
], '« La lampe consomme le courant, qui disparaît. » La lampe convertit et transfère de l’énergie ; le courant ne s’épuise pas en traversant le circuit.',[
E(1,'Ressource ou appareil ?',['Classe : vent, éolienne, Soleil, panneau photovoltaïque.'],'Vent et Soleil sont des ressources ; éolienne et panneau photovoltaïque sont des convertisseurs. Une même chaîne doit distinguer ce qui fournit l’énergie et l’objet technique qui l’exploite.'),
E(2,'Une réserve dans la pile',['Sous quelle forme l’énergie est-elle stockée dans une pile ?','Que devient cette réserve pendant l’alimentation d’une lampe ?'],'La pile possède une réserve d’énergie chimique. Cette réserve diminue au cours du fonctionnement ; de l’énergie est transférée au circuit et à l’environnement.'),
E(3,'Nommer une conversion',['Quel effet utile recherche-t-on avec un moteur de jouet ?','Quel effet utile recherche-t-on avec une lampe ?'],'Le moteur sert à produire un mouvement ; la lampe sert à éclairer. Les deux dispositifs peuvent également transférer de l’énergie thermiquement à l’environnement.'),
E(4,'L’unité d’énergie',['Quelle grandeur peut être exprimée en J ?','Que signifie ce symbole ?'],'Le joule, symbole J, est une unité d’énergie. Il ne s’agit pas d’une unité de masse, de durée ou de vitesse.'),
E(5,'Lire une chaîne',['Quel est le convertisseur au centre ?','Nomme les deux sorties représentées.'],'Le convertisseur est la lampe. Les sorties représentent la lumière et un transfert thermique. La pile fournit l’énergie par transfert électrique.',figure=('pc_energy',['Pile','Lampe','Lumière','Transfert\nthermique'])),
E(6,'Compléter un bilan',['Un appareil reçoit 80 J et en transfère 25 J utilement, sans stockage. Quelle autre énergie doit-on comptabiliser ?','Est-elle détruite ?'],'80 - 25 = 55 J sont transférés autrement, par exemple thermiquement selon l’appareil. Cette énergie n’est pas détruite ; elle doit apparaître dans le bilan.',check='80-25==55'),
E(7,'Changer d’objectif',['Un transfert thermique est-il toujours inutile ?','Compare une lampe d’éclairage et un appareil destiné à chauffer.'],'Non. Pour éclairer, le transfert thermique peut être un effet secondaire ; pour chauffer, il peut constituer l’effet recherché. Le mot utile dépend de la fonction choisie.'),
E(8,'Une chaîne solaire',['Un panneau photovoltaïque alimente un moteur. Identifie la ressource, un premier convertisseur et l’effet recherché.'],'Le Soleil fournit le rayonnement reçu ; le panneau photovoltaïque convertit une partie de l’énergie reçue en transfert électrique ; le moteur produit notamment un mouvement. D’autres transferts doivent aussi être pris en compte.'),
E(9,'Un bilan à contrôler',['Le schéma reçoit 100 J et indique 30 J utiles, 70 J autrement. Le total est-il cohérent sans stockage ?','Quelle information faut-il garder identique pour comparer les valeurs ?'],'Oui : 30 + 70 = 100 J. Les valeurs doivent concerner la même durée d’étude et la même unité. Un bilan pris à des durées différentes serait incohérent.',figure=('pc_budget',None),check='30+70==100'),
E(10,'Une réserve qui augmente',['Un dispositif reçoit 50 J, en transfère 35 J à l’extérieur et stocke le reste. Quelle réserve gagne-t-il ?','Pourquoi les seules sorties ne sont-elles pas égales à l’entrée ?'],'La réserve augmente de 50 - 35 = 15 J. L’écart correspond au stockage dans le système ; ce n’est pas une disparition d’énergie.',check='50-35==15'),
E(11,'Des mots précis',['« Le vent fabrique de l’énergie dans l’éolienne. » Reformule sans création d’énergie.'],'Le vent met l’éolienne en mouvement ; son dispositif convertit une partie de l’énergie reçue et la transfère notamment sous forme électrique. L’énergie est transférée et convertie, pas créée à partir de rien.'),
E(12,'Comparer deux appareils',['A reçoit 100 J pour 20 J utiles ; B reçoit 100 J pour 35 J utiles. Lequel fournit davantage d’énergie utile dans ces conditions ?','Calcule les autres transferts si les appareils ne stockent rien.'],'B fournit davantage d’énergie utile. Les autres transferts valent 80 J pour A et 65 J pour B. La comparaison suppose le même objectif et des valeurs mesurées sur des conditions comparables.',check='100-20==80 and 100-35==65'),
E(13,'Une chaîne incomplète',['Une chaîne de moteur ne montre que « pile → mouvement ». Quelles informations manque-t-il ?','Propose une amélioration.'],'Il manque le convertisseur moteur, la nature du transfert entrant et les autres transferts sortants. Ajouter pile → transfert électrique → moteur, puis les sorties mouvement et transfert thermique, et éventuellement son selon le modèle.'),
E(14,'Ne pas additionner des grandeurs différentes',['Un élève additionne 20 J et 5 s pour trouver « 25 d’énergie ». Pourquoi le calcul est-il invalide ?','Quelle règle utiliser ?'],'Il additionne une énergie et une durée, grandeurs différentes. On n’additionne que des grandeurs compatibles exprimées dans la même unité ; l’unité ne se choisit pas après le calcul.'),
E(15,'Un effet secondaire observé',['Un moteur chauffe et fait un peu de bruit. Comment enrichir la chaîne énergétique ?','Pourquoi ne faut-il pas écrire « l’énergie restante est perdue pour toujours » ?'],'Ajouter des transferts thermiques et sonores vers l’environnement. Ils peuvent être moins utiles pour faire tourner le moteur, mais l’énergie existe toujours dans le bilan. Le schéma initial était seulement incomplet.')
],Defi('L’éclairage à améliorer',
    'Deux systèmes reçoivent chacun 200 J pendant la même durée. A transfère 40 J sous forme lumineuse utile ; B en transfère 70 J. Ils ne stockent pas d’énergie pendant l’essai. On recherche le meilleur éclairage pour cette énergie reçue.',
    ('pc_budget',[200,70,130]),['Complète les deux bilans.','Quel système répond mieux au critère annoncé ?','Cite une autre information nécessaire pour choisir un éclairage réel.'],
    'Le critère porte sur l’énergie lumineuse utile pour une même énergie reçue, pas seulement sur le mot « moderne ».',
    'A transfère 160 J autrement et B 130 J. B fournit plus d’énergie lumineuse utile pour 200 J reçus. Un choix réel demande aussi la répartition de la lumière, le confort visuel, la durée de vie, le prix et les conditions d’utilisation. Les données de l’essai ne suffisent pas à classer tous les produits.'))

C13=Chapitre(13,'Pourquoi un seul fil ne suffit-il pas pour allumer une lampe ?',[
    'Identifier générateur, récepteur, fils et interrupteur.',
    'Réaliser et lire un circuit simple avec ses symboles.',
    'Distinguer circuit ouvert, circuit fermé et sens conventionnel du courant.'
],[
Lecon('Des composants et des symboles',
    'Un circuit simple comporte un générateur, des récepteurs et des liaisons conductrices. Une pile peut jouer le rôle de générateur ; une lampe ou un moteur est un récepteur. Un interrupteur permet d’ouvrir ou de fermer un trajet conducteur. Un dipôle possède deux bornes de connexion. Le schéma électrique représente les connexions par des symboles normalisés ; il n’imite pas la forme ou la taille réelle des objets.',
    ('pc_symbols',None),'Exemples de symboles scolaires : pile, lampe, moteur et interrupteur ouvert.',
    'Pour la pile, le trait long représente la borne positive, le trait court la borne négative. Les traits du schéma indiquent les liaisons conductrices.',
    'Faire l’inventaire des composants puis repérer leurs deux bornes. Dessiner les fils à la règle et placer les symboles sans les remplacer par des dessins décoratifs.'),
Lecon('Une boucle conductrice fermée',
    'Une lampe adaptée peut fonctionner lorsque ses deux bornes sont reliées aux deux bornes d’un générateur adapté par une boucle conductrice fermée. Si une liaison est interrompue, le circuit est ouvert et le courant ne circule plus dans cette boucle. La présence de la pile ne suffit pas : il faut un trajet complet. Les composants de classe sont choisis compatibles et le montage est vérifié avant mise en fonctionnement.',
    ('pc_circuit','open'),'L’interrupteur ouvert interrompt la boucle. La lampe est représentée éteinte.',
    'Une lampe éteinte peut avoir plusieurs causes : interrupteur ouvert, mauvais contact, pile inadaptée ou déchargée, lampe défectueuse. Il faut tester méthodiquement.',
    'Suivre le trajet depuis une borne de la pile jusqu’à l’autre. Toute interruption ou mauvais contact empêche le fonctionnement de cette boucle.'),
Lecon('Un sens conventionnel pour le courant',
    'Dans un circuit fermé alimenté par une pile, on représente conventionnellement le courant à l’extérieur du générateur du pôle positif vers le pôle négatif. La lampe ne consomme pas progressivement le courant ; elle reçoit et transfère de l’énergie. Certains récepteurs dépendent du branchement : inverser les bornes d’un petit moteur à courant continu adapté inverse son sens de rotation.',
    ('pc_circuit','direction'),'Les flèches représentent le sens conventionnel à l’extérieur de la pile, dans la boucle fermée.',
    'Le sens de rotation du moteur est distinct du sens conventionnel du courant. Un schéma de circuit et une chaîne énergétique répondent à des questions différentes.',
    'Repérer d’abord + et - sur le générateur. Tracer les flèches seulement sur les fils du circuit extérieur ; ne pas confondre ces flèches avec celles d’une chaîne d’énergie.')
],Activite('Allumer, éteindre et dépanner',
    'Réaliser un circuit à une lampe et expliquer chaque modification.',[
    'Avec le matériel scolaire fourni, préparer un générateur protégé, une lampe adaptée, des fils et un interrupteur. Faire valider le montage hors fonctionnement.',
    'Fermer puis ouvrir l’interrupteur. Noter le fonctionnement de la lampe et représenter les deux situations.',
    'Si la lampe reste éteinte, contrôler une seule cause à la fois avec le professeur : contact, composant ou source.'
],('pc_circuit','closed'),'Un circuit scolaire simple fermé ; la couleur de remplissage aide ici à repérer la lampe en fonctionnement.',[
    'Quel trajet complet permet le fonctionnement ?',
    'Quelle connexion change lorsqu’on ouvre l’interrupteur ?',
    'Pourquoi faut-il éviter de modifier plusieurs éléments à la fois pour dépanner ?'
], 'La boucle relie une borne du générateur à l’autre en traversant la lampe et l’interrupteur fermé. L’ouverture interrompt ce trajet. Modifier une seule cause à la fois permet de relier un changement de fonctionnement à un élément précis ; changer simultanément pile, fils et lampe empêcherait d’identifier la panne.'),[
    'Un générateur fournit l’énergie transférée aux récepteurs.',
    'Une boucle conductrice fermée est nécessaire au fonctionnement du circuit simple.',
    'Un interrupteur ouvre ou ferme une liaison.',
    'Le schéma représente les connexions et les symboles des composants.',
    'Dans le circuit extérieur, le sens conventionnel va du + vers le - de la pile.'
], '« Un seul fil apporte l’électricité à la lampe. » Il faut un trajet de retour vers l’autre borne du générateur pour former une boucle.',[
E(1,'Nommer les composants',['Quel composant peut jouer le rôle de générateur ?','Donne deux exemples de récepteurs.'],'Une pile peut être un générateur. Une lampe et un moteur sont des récepteurs. Leur compatibilité avec le générateur doit être vérifiée.'),
E(2,'Deux bornes',['Que signifie le mot dipôle ?','Combien de bornes comporte le symbole d’une lampe ?'],'Un dipôle possède deux bornes de connexion. Le symbole d’une lampe comporte deux connexions vers les fils du circuit.'),
E(3,'Ouvrir le circuit',['Quel est l’effet d’un interrupteur ouvert dans une boucle unique ?','La présence d’une pile suffit-elle à allumer la lampe ?'],'L’interrupteur ouvert interrompt la boucle ; la lampe ne fonctionne pas dans ce montage. La présence de la pile seule ne suffit pas : la boucle doit être fermée et les composants adaptés.'),
E(4,'Lire les symboles',['Identifie pile, lampe et moteur sur la planche.','Quel trait de la pile représente la borne positive ?'],'La pile est représentée par deux traits parallèles de longueurs différentes ; la lampe par un cercle avec une croix ; le moteur par un cercle avec M. Le trait long est la borne positive.',figure=('pc_symbols',None)),
E(5,'Le sens conventionnel',['Dans le circuit extérieur d’une pile, de quelle borne vers quelle borne représente-t-on le courant ?'],'On le représente du pôle positif vers le pôle négatif dans le circuit extérieur fermé. Il s’agit d’une convention de description.'),
E(6,'Lire une coupure',['Pourquoi la lampe ne fonctionne-t-elle pas sur ce schéma ?','Quelle modification autorisée fermerait la boucle ?'],'L’interrupteur est ouvert et coupe le trajet conducteur. Le fermer permet de compléter la boucle, si les autres connexions et les composants sont corrects.',figure=('pc_circuit','open')),
E(7,'Un dessin ou un schéma ?',['Pourquoi un schéma électrique n’a-t-il pas besoin de respecter la taille réelle des composants ?','Quelle information doit-il préserver absolument ?'],'Le schéma code le circuit par des symboles. Il doit préserver les composants et leurs connexions, pas leurs dimensions ou leurs positions réelles sur la table.'),
E(8,'Une panne à rechercher',['Une lampe reste éteinte dans un circuit apparemment fermé. Propose trois causes possibles.','Pourquoi ne faut-il pas conclure directement que la pile est vide ?'],'Causes possibles : mauvais contact, lampe défectueuse, générateur déchargé ou inadapté. Une observation identique peut avoir plusieurs causes ; il faut les tester successivement selon le protocole de classe.'),
E(9,'Le moteur inversé',['Un moteur à courant continu adapté tourne dans un sens. On inverse les connexions de la pile. Que peut-on observer ?','Faut-il confondre ce sens avec la forme du schéma ?'],'Le moteur peut tourner dans le sens opposé. Le sens de rotation est une propriété du mouvement du moteur ; la forme rectangulaire des fils sur le schéma n’en constitue pas une trajectoire.',figure=('pc_motor',None)),
E(10,'Suivre une boucle',['Décris un trajet complet depuis la borne positive, en passant par les composants du montage simple.','Où faut-il revenir ?'],'On suit un fil, la lampe, l’interrupteur fermé et les autres liaisons jusqu’à la borne négative. L’ordre dépend du schéma, mais le trajet doit relier les deux bornes du générateur par les récepteurs.'),
E(11,'Courant et énergie',['Corrige : « le courant entre dans la lampe et disparaît en lumière ».'],'La lampe reçoit de l’énergie par transfert électrique et en transfère sous forme lumineuse et thermique. Dans une boucle fermée en fonctionnement, on ne décrit pas un courant qui disparaît progressivement dans la lampe.'),
E(12,'Le bon témoin',['Pour tester une lampe, pourquoi faut-il d’abord connaître un montage qui fonctionne ?','Quel composant changer ensuite ?'],'Un montage témoin valide la source et les connexions. Remplacer seulement la lampe connue par celle à tester permet de comparer sans multiplier les causes possibles. Le professeur choisit des composants compatibles.'),
E(13,'Une connexion trompeuse',['Un fil touche l’enveloppe isolante d’une lampe au lieu de sa borne métallique. Pourquoi la boucle peut-elle rester ouverte ?','Quelle information matérielle faut-il vérifier ?'],'Le fil ne touche pas nécessairement une partie conductrice reliée à la borne. Il faut identifier les vraies bornes de connexion et contrôler le contact électrique, pas seulement le contact visuel avec l’objet.'),
E(14,'Deux schémas équivalents',['On déplace une lampe sur le dessin sans changer ses connexions. Le circuit électrique change-t-il forcément ?','Quel contrôle permet de comparer les dessins ?'],'Non. Comparer les connexions entre les bornes des mêmes composants. Des dessins de formes différentes peuvent représenter le même circuit si tous les liens sont conservés.'),
E(15,'Répondre à un cahier des charges',['Propose les composants d’un montage qui allume une lampe et permet de l’éteindre sans retirer de fil.','Explique le rôle de chaque élément.'],'Utiliser un générateur adapté, une lampe, des fils et un interrupteur dans une boucle unique. Le générateur fournit l’énergie ; la lampe éclaire ; les fils réalisent les liaisons ; l’interrupteur ouvre ou ferme la boucle. Le montage est vérifié par le professeur.')
],Defi('Le dossier de dépannage',
    'Une lampe ne s’allume pas. On dispose d’une lampe de référence et de fils connus en bon état, compatibles avec le matériel scolaire utilisé. Construis un arbre de recherche qui évite de changer tout le montage à la fois.',
    ('pc_circuit','closed'),['Indique le premier contrôle visuel hors fonctionnement.','Propose deux substitutions successives.','Explique comment conclure sans aller au-delà de ce que chaque test montre.'],
    'Conserver une source et des composants compatibles ; demander au professeur avant toute modification.',
    'Contrôler les bornes, les contacts et l’interrupteur. Tester ensuite la lampe de référence dans le même circuit ; si elle fonctionne, la lampe initiale est suspecte. Sinon, contrôler les fils un par un puis le générateur avec le professeur. Chaque test compare une seule modification. Une panne peut aussi résulter de plusieurs défauts : ne pas généraliser trop vite.'))

C14=Chapitre(14,'Comment tester un matériau sans prendre de risque ?',[
    'Distinguer conducteur et isolant dans les conditions d’un test.',
    'Construire un test avec des témoins de fonctionnement.',
    'Reconnaître un court-circuit et les règles essentielles de sécurité.'
],[
Lecon('Un matériau dans un circuit de test',
    'Un conducteur permet le passage du courant dans les conditions considérées ; un isolant le limite fortement. Dans un circuit scolaire de test, un échantillon complète une boucle comportant une lampe adaptée. Les métaux usuels conduisent généralement bien ; beaucoup de plastiques secs sont isolants. Le résultat dépend aussi des contacts, de la forme de l’échantillon et de la sensibilité du dispositif.',
    ('pc_test_material',None),'L’échantillon est placé dans la boucle avec un récepteur ; il ne relie pas directement les bornes du générateur.',
    'Une lampe éteinte ne prouve pas à elle seule que l’échantillon est isolant. Il faut vérifier que le montage fonctionne et que les contacts sont corrects.',
    'Valider le montage avec un conducteur connu. Tester ensuite l’échantillon sans changer les autres conditions, puis contrôler les contacts.'),
Lecon('Identifier un court-circuit',
    'Un fil conducteur qui relie directement les bornes d’un dipôle peut le court-circuiter : le courant dispose d’un chemin de très faible résistance qui le contourne. Si les bornes du générateur sont ainsi reliées presque directement, un courant important peut apparaître, avec échauffement et détérioration. Le schéma sert ici à reconnaître une erreur ; le montage dangereux n’est pas à réaliser.',
    ('pc_circuit','short'),'Situation à repérer sur document seulement : le fil contourne l’unique lampe et crée un trajet presque direct entre les bornes de la pile.',
    'Un circuit fermé n’est pas automatiquement correct. Il doit comporter des récepteurs et des liaisons conformes au montage prévu.',
    'Suivre les chemins possibles. Rechercher une liaison qui évite tous les récepteurs et rejoint presque directement les deux bornes du générateur.'),
Lecon('Le corps et l’environnement comptent',
    'Le corps humain peut conduire le courant. L’humidité peut accroître les risques ; l’eau du robinet n’est pas un isolant fiable. On ne teste jamais la conductivité avec son corps ni avec une prise domestique. Les expériences utilisent exclusivement le matériel scolaire de très basse tension et les protections choisies par le professeur. Une pile peut elle-même chauffer en cas de mauvais branchement.',
    ('pc_circuit','open'),'Préparer et modifier un montage hors fonctionnement, puis le faire vérifier avant fermeture.',
    'Le secteur domestique et les batteries puissantes ne sont pas des sources pour les montages du livre. L’isolant d’un appareil abîmé ne se répare pas par un simple essai.',
    'En cas d’anomalie, arrêter l’activité et prévenir le professeur. Ne pas toucher un composant échauffé et ne pas tenter de dépannage sur une installation domestique.')
],Activite('Comparer trois matériaux',
    'Établir un classement argumenté avec un test scolaire et ses limites.',[
    'Le professeur fournit un montage protégé, un témoin conducteur et des échantillons secs identifiés, par exemple métal, plastique et bois sec.',
    'Vérifier le fonctionnement avec le témoin. Remplacer seulement l’échantillon et garder les contacts comparables.',
    'Noter l’observation sans forcer les conclusions. Si la lampe reste éteinte, vérifier à nouveau les contacts puis le témoin.'
],('pc_test_material',None),'Aucun essai sur le corps, le secteur ou un liquide inconnu n’est demandé.',[
    'Pourquoi commence-t-on et termine-t-on par un témoin ?',
    'Comment noter un résultat négatif sans affirmer une propriété absolue ?',
    'Pourquoi le revêtement isolant d’un fil et son cœur métallique ont-ils des rôles différents ?'
], 'Le témoin vérifie que le montage reste fonctionnel avant et après la série. Un résultat négatif s’écrit : « la lampe ne s’allume pas avec cet échantillon dans les conditions du test », puis s’interprète avec les contrôles. Le métal réalise la liaison conductrice ; le revêtement limite les contacts involontaires avec le conducteur.'),[
    'Conductivité et isolation s’évaluent dans des conditions données.',
    'Un test demande un montage validé et des témoins.',
    'Un mauvais contact peut produire un résultat trompeur.',
    'Un court-circuit peut provoquer un échauffement important.',
    'Le corps, le secteur et les sources puissantes sont exclus des essais scolaires du livre.'
], '« La lampe est éteinte, donc l’échantillon est forcément isolant. » Vérifier le montage, les contacts et la sensibilité du test.',[
E(1,'Conducteur ou isolant ?',['Dans les conditions usuelles d’un test scolaire, comment classe-t-on un fil de cuivre et une gaine plastique sèche ?'],'Le cuivre est conducteur et la gaine plastique sèche est isolante dans ces conditions. Le classement décrit leur comportement dans le contexte étudié.'),
E(2,'Le rôle de la gaine',['Pourquoi un fil électrique possède-t-il souvent un cœur métallique entouré de plastique ?'],'Le cœur métallique permet la liaison conductrice. Le plastique limite le contact avec le conducteur et sépare les fils. Une gaine abîmée ne doit pas être ignorée.'),
E(3,'Lire le test',['Où place-t-on l’échantillon dans le circuit ?','Pourquoi conserve-t-on une lampe adaptée dans la boucle ?'],'L’échantillon complète la liaison prévue sur le côté du schéma. La lampe sert de témoin de fonctionnement et de récepteur ; on ne relie pas directement les bornes du générateur avec l’échantillon.',figure=('pc_test_material',None)),
E(4,'Les expériences autorisées',['Peut-on tester un matériau avec les deux contacts d’une prise domestique ?','Quelle source utilise-t-on ici ?'],'Non. On utilise uniquement le matériel scolaire de très basse tension prévu et validé par le professeur. Le secteur ne sert jamais à ces expériences.'),
E(5,'Un chemin dangereux',['Comment nomme-t-on une liaison conductrice presque directe entre les deux bornes d’un générateur ?','Quel risque peut-elle présenter ?'],'C’est un court-circuit du générateur. Il peut entraîner un courant important, un échauffement ou une détérioration ; on ne le réalise pas pour vérifier le risque.'),
E(6,'Un témoin utile',['La lampe ne fonctionne pas avec un échantillon. Elle ne fonctionne pas non plus avec le témoin conducteur. Peut-on classer l’échantillon ?','Quelle étape reprendre ?'],'Non : le montage n’est pas validé. Rechercher la cause de panne ou de mauvais contact avec le professeur, puis refaire le test après avoir retrouvé le fonctionnement du témoin.'),
E(7,'Un métal recouvert',['Une pièce métallique peinte ne ferme pas le circuit lors du test. Pourquoi cela ne prouve-t-il pas que le métal est isolant ?','Que doit-on identifier ?'],'La peinture peut empêcher le contact avec le métal. Il faut identifier la surface réellement touchée par les connexions et contrôler le contact, selon le protocole de classe.'),
E(8,'Repérer le fil ajouté',['Pourquoi le fil supérieur est-il un problème dans ce montage à une seule lampe ?','Faut-il réaliser ce montage ?'],'Le fil contourne l’unique récepteur et laisse un trajet presque direct entre les bornes de la pile. C’est une situation de court-circuit à reconnaître sur document, sans la réaliser.',figure=('pc_circuit','short')),
E(9,'Le corps humain',['Pourquoi ne faut-il pas utiliser ses doigts pour fermer le circuit de test ?','L’absence de sensation serait-elle une preuve de sécurité générale ?'],'Le corps peut conduire le courant et ne constitue pas un échantillon de test. L’absence de sensation dans une situation ne prouve pas la sécurité d’autres tensions, sources ou conditions.'),
E(10,'L’eau et les risques',['Un camarade affirme que toute eau est isolante. Pourquoi cette affirmation est-elle dangereuse ?','Quelle règle appliquer près d’appareils électriques ?'],'Les eaux usuelles contiennent souvent des espèces dissoutes et ne sont pas des isolants fiables. Respecter les consignes d’usage et tenir l’eau à l’écart des montages et appareils non prévus pour cela ; ne pas improviser de test.'),
E(11,'Deux contrôles de contact',['Donne deux raisons possibles d’un mauvais contact avec un échantillon conducteur.','Comment éviter une conclusion trop rapide ?'],'Une surface peinte ou oxydée et une connexion mal placée peuvent empêcher un bon contact. Contrôler les bornes et utiliser un témoin dans les mêmes conditions avant de classer l’échantillon.'),
E(12,'Rédiger un résultat limité',['Le bois sec testé n’allume pas la lampe. Propose une formulation scientifique prudente.','Pourquoi ne faut-il pas étendre le résultat à tout bois humide ?'],'« Avec ce morceau de bois sec, la lampe ne s’allume pas dans les conditions du test validé. » L’humidité et la composition peuvent modifier le comportement ; le résultat ne décrit pas toutes les situations possibles.'),
E(13,'La pile chauffe',['Pendant un montage, une source devient anormalement chaude. Quelle conduite adopter ?','Pourquoi ne faut-il pas poursuivre pour obtenir une mesure ?'],'Arrêter l’activité selon les consignes, ne pas toucher la partie échauffée et prévenir le professeur. Un échauffement peut signaler un mauvais branchement ou un défaut ; poursuivre peut aggraver le risque.'),
E(14,'La variable étudiée',['Un groupe change la pile et l’échantillon entre deux essais. Pourquoi la comparaison est-elle ambiguë ?','Comment améliorer le protocole ?'],'Le fonctionnement peut changer à cause de la source ou du matériau. Conserver le même montage validé et modifier uniquement l’échantillon, avec des contacts comparables et des témoins.'),
E(15,'Concevoir une fiche de test',['Rédige les rubriques nécessaires pour rendre un essai de conductivité compréhensible.','Ajoute une rubrique sur les limites.'],'Indiquer le matériau et son état, le schéma et le matériel, les témoins, les contacts, l’observation et l’interprétation. Ajouter les limites : sensibilité du dispositif, humidité, revêtement et éventuels défauts de contact. Ne pas présenter un résultat unique comme universel.')
],Defi('Le métal déclaré isolant',
    'Deux groupes testent une même tige métallique. L’un allume la lampe et l’autre non. La tige est recouverte d’une peinture isolante sauf sur une petite zone. Prépare une explication et un protocole de vérification encadré.',
    ('pc_test_material',None),['Identifie au moins deux causes possibles de la différence.','Propose une comparaison avec un seul facteur modifié.','Rédige une conclusion qui distingue le matériau et son revêtement.'],
    'Le contact avec l’objet n’est pas forcément un contact électrique avec son cœur métallique.',
    'Les groupes peuvent avoir touché des zones différentes ou utilisé un montage défectueux. Valider d’abord le circuit témoin ; comparer ensuite la zone peinte et la zone métallique accessible sans modifier le reste. La tige peut être conductrice tandis que sa peinture limite le contact. Toute préparation de l’échantillon relève du professeur.'))

C15=Chapitre(15,'Comment garder une lampe allumée quand une autre s’arrête ?',[
    'Distinguer une association en série et une association en dérivation.',
    'Prévoir les effets d’une ouverture sur les chemins conducteurs.',
    'Placer un interrupteur pour une commande générale ou indépendante.'
],[
Lecon('Une seule boucle : l’association en série',
    'Dans un circuit en série simple, les dipôles sont placés les uns à la suite des autres sur une seule boucle. Si une connexion de cette boucle s’ouvre, le courant ne peut plus circuler et tous les récepteurs de la boucle cessent de fonctionner. Modifier l’ordre des composants sans changer les connexions ne crée pas une nouvelle branche. La forme du dessin peut varier tout en représentant le même circuit.',
    ('pc_circuit','series'),'Deux lampes en série : une seule boucle relie les bornes du générateur.',
    'Compter les lampes ne suffit pas pour identifier le montage. Il faut suivre les chemins et les connexions.',
    'Partir d’une borne du générateur et suivre l’unique trajet. Si l’on traverse successivement les deux lampes sans choix de chemin, elles sont ici en série.'),
Lecon('Plusieurs chemins : la dérivation',
    'Dans une association en dérivation, les récepteurs appartiennent à des branches différentes reliées aux mêmes deux points de connexion. Plusieurs chemins fermés sont possibles avec le générateur. Une branche peut être ouverte tandis qu’une autre reste fermée. Avec une source adaptée et maintenue dans les mêmes conditions, le récepteur de la branche restée fermée peut continuer à fonctionner.',
    ('pc_circuit','parallel'),'L₁ et L₂ se trouvent sur des branches différentes ; les points indiquent des jonctions conductrices.',
    'Une dérivation ne se reconnaît pas simplement à deux traits parallèles sur la feuille. Les bornes des branches doivent être reliées aux mêmes deux points.',
    'Repérer les jonctions puis surligner chaque chemin entre elles. Vérifier que chaque branche de récepteur forme un chemin avec le générateur.'),
Lecon('Commander ensemble ou séparément',
    'Un interrupteur placé dans une portion commune à tous les chemins commande l’ensemble des récepteurs. Un interrupteur placé seulement dans une branche commande cette branche, à condition de ne pas interrompre les autres chemins. On choisit donc l’emplacement selon la fonction demandée. Les comparaisons d’éclat nécessitent des lampes identifiées et un générateur adapté ; on ne généralise pas un résultat à n’importe quels composants.',
    ('pc_circuit','parallel_open'),'L’interrupteur de la branche de L₁ est ouvert ; la branche de L₂ conserve un chemin fermé.',
    'Lampe éteinte ne signifie pas absence de générateur. Il faut chercher quel chemin est ouvert et quels autres restent conducteurs.',
    'Pour prévoir le fonctionnement, ignorer visuellement la branche ouverte puis chercher s’il reste un chemin complet passant par chaque autre récepteur.')
],Activite('Choisir une commande d’éclairage',
    'Comparer la commande de deux lampes dans deux montages scolaires.',[
    'À partir des schémas, proposer un circuit en série et un circuit en dérivation avec deux lampes adaptées. Faire valider les montages avant fonctionnement.',
    'Avec le professeur, ouvrir une liaison prévue dans un chemin de lampe. Noter quelles lampes restent allumées.',
    'Représenter une commande indépendante dans une seule branche et une commande générale sur une portion commune.'
],('pc_circuit','parallel_open'),'Une ouverture localisée dans une branche ne coupe pas automatiquement toutes les autres.',[
    'Quel montage permet à L₂ de fonctionner malgré l’ouverture de la branche de L₁ ?',
    'Où placer une commande qui éteint les deux lampes ?',
    'Pourquoi les deux lampes ne doivent-elles pas être reliées par un fil qui les contourne ?'
], 'Le montage en dérivation permet à L₂ de conserver sa boucle avec le générateur. Une commande générale se place dans une portion commune à tous les trajets, par exemple sur une liaison principale du générateur. Un fil qui contourne les récepteurs peut créer un court-circuit ; il ne constitue pas une commande d’éclairage correcte.'),[
    'En série simple, une seule boucle contient les récepteurs successifs.',
    'Une ouverture dans cette boucle interrompt le fonctionnement de tous ses récepteurs.',
    'En dérivation, plusieurs branches sont reliées aux mêmes deux points.',
    'Une branche ouverte peut laisser fonctionner les autres branches fermées.',
    'La position d’un interrupteur détermine une commande générale ou indépendante.'
], '« Deux lampes dessinées côte à côte sont forcément en dérivation. » Les connexions, pas leur position sur la page, déterminent l’association.',[
E(1,'Une boucle unique',['Dans un circuit simple en série, combien de chemins peut-on suivre dans la boucle ?','Traverse-t-on les deux lampes successivement ?'],'Il existe un seul chemin dans la boucle ; on traverse les deux lampes successivement. Aucune jonction ne permet de choisir une autre branche.'),
E(2,'Nommer l’association',['Identifie l’association représentée.','Quel indice de connexion justifie ta réponse ?'],'Les deux lampes sont en série. Elles appartiennent à une seule boucle et sont traversées successivement en suivant le trajet.',figure=('pc_circuit','series')),
E(3,'Une ouverture en série',['Une des lampes d’un circuit en série devient un circuit ouvert. Que se passe-t-il pour l’autre ?','Pourquoi ?'],'L’autre lampe s’éteint également : la boucle unique est interrompue. Il n’existe pas de chemin alternatif dans ce montage.'),
E(4,'Une dérivation',['Quel montage utilise plusieurs branches entre les mêmes deux points ?','Faut-il que les fils soient dessinés parallèles pour que la propriété existe ?'],'C’est une association en dérivation. La propriété vient des connexions ; les fils peuvent être dessinés autrement tout en conservant les mêmes jonctions.'),
E(5,'Une commande indépendante',['Où placer un interrupteur pour commander seulement une branche de lampe ?'],'Le placer dans cette branche, sans interrompre les portions communes aux autres chemins. Vérifier sur le schéma que les autres récepteurs conservent une boucle fermée avec le générateur.'),
E(6,'Suivre les chemins',['Sur le montage, identifie un chemin passant par L₁ et un autre passant par L₂.','Qu’ont-ils en commun ?'],'Chaque chemin relie les deux bornes du générateur en passant par une branche de lampe. Ils partagent le générateur et certaines liaisons principales ; les lampes occupent des branches différentes.',figure=('pc_circuit','parallel')),
E(7,'La branche ouverte',['Quelle lampe reste sur une boucle fermée ?','Peut-elle fonctionner avec le générateur adapté du modèle ?'],'L₂ reste sur une boucle fermée et peut fonctionner. La branche de L₁ est ouverte par son interrupteur et ne permet pas son fonctionnement.',figure=('pc_circuit','parallel_open')),
E(8,'Commander les deux lampes',['Un interrupteur est placé sur un fil commun entre la pile et toutes les branches. Quelle est sa fonction ?','Que se passe-t-il lorsqu’il est ouvert ?'],'Il réalise une commande générale. Son ouverture interrompt tous les chemins qui ont besoin de cette liaison ; les deux lampes s’éteignent.'),
E(9,'Changer l’ordre',['Dans un circuit en série simple, on échange les positions de deux lampes identiques sans changer les connexions. Crée-t-on une dérivation ?','Que reste-t-il identique ?'],'Non. Le circuit conserve une seule boucle et les deux lampes restent successives. Le nombre de branches et la structure des connexions restent identiques.'),
E(10,'Les conditions d’éclat',['Pourquoi comparer deux lampes inconnues ne suffit-il pas pour établir une règle générale d’éclat en série ?','Quelles informations faut-il contrôler ?'],'L’éclat dépend des caractéristiques des lampes et de la source. Contrôler les modèles de lampes, leur compatibilité, le générateur et ses conditions de fonctionnement. Un exemple ne justifie pas une loi pour tous les composants.'),
E(11,'Reconnaître une jonction',['À quoi servent les points noirs sur les jonctions du schéma ?','Pourquoi un croisement de traits sans convention claire peut-il être ambigu ?'],'Les points indiquent une connexion conductrice. Un croisement sans légende peut laisser hésiter entre fils connectés et fils qui se croisent sans contact ; le schéma doit utiliser une convention explicite.'),
E(12,'Deux lampes pour un couloir',['On veut que chaque lampe puisse rester allumée si la branche de l’autre est ouverte. Quelle association choisir ?','Justifie par les chemins.'],'Choisir la dérivation : chaque lampe possède sa branche, formant un chemin avec le générateur. L’ouverture d’une seule branche n’interrompt pas forcément le chemin de l’autre. Il s’agit d’un modèle scolaire, pas d’une instruction de câblage domestique.'),
E(13,'Une fausse dérivation',['Un dessin possède deux branches, mais un fil relie directement les bornes de la pile. Est-ce un montage correct parce qu’il a plusieurs branches ?','Quel contrôle prime ?'],'Non. Le fil direct peut court-circuiter le générateur. Il faut contrôler tous les chemins, notamment ceux qui évitent les récepteurs. Le nombre de branches ne garantit pas la sécurité.'),
E(14,'Un symptôme, plusieurs causes',['Dans un montage supposé en dérivation, les deux lampes s’éteignent quand on ouvre une seule branche. Cite deux vérifications.'],'Vérifier que le montage réel correspond au schéma et que l’interrupteur n’est pas dans une portion commune. Vérifier aussi le générateur et les connexions. L’observation seule ne permet pas d’identifier sans contrôle la cause exacte.'),
E(15,'Trois fonctions à réaliser',['Propose l’emplacement de trois interrupteurs : un général, un pour L₁ et un pour L₂, dans un montage à deux branches.','Comment vérifier la commande indépendante ?'],'Placer le général dans une portion commune ; placer chacun des deux autres dans sa branche de lampe. Général fermé, ouvrir successivement un interrupteur de branche et vérifier que seule la lampe correspondante s’éteint, dans les conditions du montage validé.')
],Defi('Le tableau de commande',
    'Un modèle de vitrine scolaire comporte deux lampes. On souhaite quatre situations : aucune allumée, seulement L₁, seulement L₂, les deux. Une commande générale doit pouvoir tout arrêter. Le montage reste alimenté uniquement par le matériel scolaire adapté.',
    ('pc_circuit','parallel'),['Choisis l’association et les emplacements des interrupteurs.','Prépare les réglages pour les quatre situations.','Explique le rôle de la commande générale.'],
    'Chaque lampe doit disposer de sa branche ; ajouter ensuite une commande sur un trajet commun.',
    'Choisir deux branches en dérivation, chacune avec son interrupteur, et un interrupteur général sur une liaison commune. Général fermé : ouvrir les deux branches, fermer seulement celle de L₁, seulement celle de L₂, ou les deux. Général ouvert : toutes les lampes s’éteignent quel que soit l’état des commandes de branche.'))

C16=Chapitre(16,'Comment comparer des choix d’énergie de façon honnête ?',[
    'Distinguer ressource renouvelable, ressource non renouvelable et impact environnemental.',
    'Lire des données d’énergie et distinguer énergie et puissance.',
    'Comparer à service rendu équivalent et proposer des économies argumentées.'
],[
Lecon('Renouvellement et effets sur l’environnement',
    'Une ressource renouvelable est disponible sous forme de flux ou se reconstitue à l’échelle humaine dans les conditions de son exploitation. Soleil, vent et cycle de l’eau en fournissent des exemples. Les stocks de charbon, de pétrole et d’uranium ne se reconstituent pas à cette échelle. Renouvelable ne signifie pas sans impact : fabrication, transport, usage et fin de vie des équipements doivent être considérés.',
    ('pc_resources',None),'La nature renouvelable d’une ressource et les effets de son exploitation sont deux questions liées mais distinctes.',
    'Brûler des combustibles fossiles émet notamment du dioxyde de carbone. L’augmentation des gaz à effet de serre modifie le bilan énergétique du système Terre-atmosphère.',
    'Éviter « toujours propre » ou « sans aucune conséquence ». Préciser le critère comparé : ressource, émissions, matériaux, espace occupé ou service rendu.'),
Lecon('Lire une consommation d’énergie',
    'L’énergie s’exprime en joules et, dans de nombreux documents d’usage, en wattheures (Wh) ou kilowattheures (kWh). Le watt (W) est une unité de puissance : il renseigne sur le rythme du transfert d’énergie. Pour un appareil fonctionnant à puissance constante, 100 W pendant une heure correspondent à 100 Wh ; pendant deux heures, à 200 Wh. On utilise ici cette proportionnalité simple sans confondre W et Wh.',
    ('pc_energy_choice',[120,36]),'Consommations annuelles pédagogiques de deux solutions procurant le même service : 120 kWh et 36 kWh.',
    '1 kWh = 1 000 Wh. Une valeur de puissance seule ne donne pas l’énergie d’un usage : il faut aussi connaître la durée et les conditions de fonctionnement.',
    'Lire l’unité, la période de mesure et le service rendu. Pour comparer des énergies, convertir dans la même unité avant de soustraire.'),
Lecon('Comparer à service équivalent',
    'Un choix d’équipement doit d’abord répondre au même besoin. Comparer deux éclairages demande par exemple un éclairage utile et une durée d’utilisation comparables. Réduire une durée inutile, améliorer l’isolation ou choisir un dispositif moins énergivore peut diminuer l’énergie nécessaire. Il faut néanmoins vérifier le résultat réel et considérer la durée de vie ainsi que les ressources nécessaires à la fabrication.',
    ('pc_energy',['Soleil','Panneau\nphotovoltaïque','Transfert\nélectrique','Autres\ntransferts']),'Une conversion comporte plusieurs transferts ; un dispositif ne convertit pas toute l’énergie reçue en effet utile.',
    'L’effet de serre naturel joue un rôle dans la température terrestre. L’enjeu étudié ici est la modification du bilan par l’augmentation de certains gaz, pas la disparition de tout effet de serre.',
    'Construire un tableau : même service, énergie sur la même durée, durée de vie et limites des données. Formuler une conclusion proportionnée aux informations disponibles.')
],Activite('Comparer deux éclairages fictifs',
    'Calculer une économie et discuter ce que les chiffres permettent de conclure.',[
    'Deux systèmes A et B assurent le même éclairage utile sur une année : A utilise 120 kWh, B 36 kWh. Les données sont fictives et servent à l’exercice.',
    'Comparer les consommations en conservant le même service et la même période. Calculer la différence et la part économisée par rapport à A.',
    'Dresser la liste des autres données utiles pour une décision d’équipement, sans inventer de prix ni de durée de vie.'
],('pc_energy_choice',[120,36]),'Les barres représentent des énergies consommées sur une même année.',[
    'Quelle énergie est économisée avec B sur un an ?',
    'Que représente cette économie sur 120 kWh : plus ou moins de la moitié ?',
    'Pourquoi cette seule comparaison ne suffit-elle pas à un bilan environnemental complet ?'
], 'L’économie vaut 120 - 36 = 84 kWh, soit 70 % de la consommation de référence A ; c’est plus de la moitié. Les seules consommations à l’usage ne décrivent pas fabrication, durée de vie, transport, réparabilité ni fin de vie. La conclusion porte sur l’énergie d’usage pour le service et la période annoncés.'),[
    'Le renouvellement d’une ressource s’évalue à une échelle de temps.',
    'Aucune classification de ressource ne suffit à résumer tous les impacts.',
    'W mesure une puissance ; Wh et kWh mesurent des énergies.',
    '1 kWh = 1 000 Wh ; la durée d’usage compte dans l’énergie consommée.',
    'Une comparaison demande le même service et des conditions explicites.'
], '« L’appareil le moins puissant utilise toujours le moins d’énergie. » La durée et le service rendu doivent aussi être comparés.',[
E(1,'Classer des ressources',['Classe le vent, le pétrole et le Soleil selon leur renouvellement à l’échelle humaine.'],'Vent et Soleil sont des ressources renouvelables à cette échelle ; le pétrole provient d’un stock non renouvelable. Cette classification ne résume pas tous les impacts des équipements.'),
E(2,'Lire les unités',['Associe W, Wh et kWh à puissance ou énergie.'],'W est une unité de puissance. Wh et kWh sont des unités d’énergie. Les symboles ne sont pas interchangeables.'),
E(3,'Une conversion d’énergie',['Convertis 2 kWh en Wh.','Convertis 500 Wh en kWh.'],'2 kWh = 2 000 Wh. 500 Wh = 0,5 kWh. On garde une grandeur énergie pendant la conversion.',check='2*1000==2000 and 500/1000==0.5'),
E(4,'Le bon critère',['Deux appareils n’assurent pas le même éclairage. Peut-on les classer uniquement par leur consommation ?','Quelle condition demander ?'],'On peut comparer leurs nombres, mais pas conclure à une meilleure efficacité pour le même besoin sans service équivalent. Il faut demander un éclairage utile et des conditions d’usage comparables.'),
E(5,'Un renouvelable sans impact ?',['Corrige : « Une éolienne ne nécessite aucune ressource parce que le vent est renouvelable. »'],'Le vent est une ressource renouvelable, mais la fabrication, l’installation, l’entretien et la fin de vie de l’éolienne mobilisent des matériaux et de l’énergie. Renouvelable ne signifie pas sans ressources ni sans impact.'),
E(6,'Lire deux barres',['Calcule l’écart entre A et B.','Quelle période concerne cet écart ?'],'120 - 36 = 84 kWh. L’écart concerne une année selon le document. Il ne faut pas le présenter comme une économie quotidienne.',figure=('pc_energy_choice',[120,36]),check='120-36==84'),
E(7,'La durée de fonctionnement',['Un appareil maintient 50 W pendant 2 h. Avec le repère du cours, quelle énergie utilise-t-il en Wh ?','Que donnerait 1 h ?'],'À puissance constante, 50 W pendant 2 h correspondent à 100 Wh ; pendant 1 h, à 50 Wh. L’énergie est proportionnelle à la durée dans ce cas.',check='50*2==100'),
E(8,'Passer à plusieurs jours',['Un usage consomme 40 Wh par jour. Quelle énergie correspond à 5 jours identiques ?','Exprime-la aussi en kWh.'],'5 × 40 = 200 Wh, soit 0,2 kWh. Le calcul suppose que l’usage quotidien reste identique.',check='40*5==200 and 200/1000==0.2'),
E(9,'Réduire un usage inutile',['Une lampe reçoit de l’énergie pendant qu’une pièce est vide. Quel changement d’usage peut éviter ce transfert inutile ?','Quelle limite faut-il préciser ?'],'Éteindre l’éclairage lorsque le service n’est pas nécessaire peut réduire l’énergie d’usage. La décision doit respecter les besoins de sécurité, de confort et les conditions propres au lieu.'),
E(10,'Un stock non renouvelable',['L’uranium n’émet pas le même bilan direct qu’un combustible fossile lors de l’usage dans une centrale. Est-il pour autant renouvelable ?','Quelles deux questions faut-il distinguer ?'],'Non : le stock d’uranium n’est pas renouvelable à l’échelle humaine. Distinguer renouvellement de la ressource et émissions ou impacts du dispositif. Une seule propriété ne remplace pas un bilan complet.'),
E(11,'Un même service sur deux ans',['A utilise 120 kWh par an et B 36 kWh, avec un usage identique chaque année. Quelle économie de B sur deux ans ?','Quelle hypothèse est nécessaire ?'],'L’économie annuelle est 84 kWh ; sur deux ans, 168 kWh. On suppose le même usage, les mêmes performances et le même service chaque année.',check='(120-36)*2==168'),
E(12,'Moins puissant, mais plus longtemps',['A fonctionne à 20 W pendant 5 h ; B à 40 W pendant 2 h, à puissance constante. Compare les énergies en Wh.','Que montre cet exemple ?'],'A utilise 100 Wh et B 80 Wh. L’appareil moins puissant peut utiliser davantage d’énergie s’il fonctionne plus longtemps. Il faut encore vérifier que le service comparé est pertinent.',check='20*5==100 and 40*2==80'),
E(13,'Une donnée publicitaire',['« 30 % de moins » est annoncé sans référence. Quelles questions poser ?','Pourquoi la durée de mesure compte-t-elle ?'],'Demander 30 % de quelle grandeur, par rapport à quel appareil, pour quel service et quelles conditions. Des périodes ou des durées différentes changent l’énergie ; une comparaison honnête précise sa référence.'),
E(14,'Calculer une part économisée',['On passe de 200 kWh à 150 kWh pour le même service. Quelle économie réalise-t-on ?','Cette économie représente quelle part de 200 kWh ?'],'L’économie est de 50 kWh. 50 sur 200 représente un quart, soit 25 %. Le pourcentage est calculé par rapport à la consommation de départ.',check='200-150==50 and 50/200==0.25'),
E(15,'Un bilan de décision',['Propose trois informations à réunir avant de remplacer un appareil encore fonctionnel par un autre.','Pourquoi la consommation à l’usage ne suffit-elle pas toujours ?'],'Rechercher le service réellement fourni, la consommation selon l’usage, la durée de vie et la réparabilité, ainsi que les impacts de fabrication et de fin de vie. Le remplacement mobilise aussi des ressources ; un choix raisonné considère davantage que le seul chiffre de consommation.')
],Defi('L’affiche d’une classe économe',
    'Une classe veut réduire une consommation d’éclairage de 300 kWh par an. Une meilleure organisation permettrait d’éviter 60 kWh d’usage inutile ; un autre équipement, pour les mêmes heures restantes, permettrait encore 40 kWh d’économie. Les estimations sont fournies pour ce scénario précis.',
    ('pc_energy_choice',[300,200]),['Calcule la consommation finale et l’économie totale.','Exprime l’économie comme une fraction simple de 300 kWh.','Rédige une affiche qui explique les hypothèses et n’annonce pas un impact nul.'],
    'Les deux économies du document concernent des étapes successives déjà définies ; ne pas additionner des pourcentages sans référence.',
    'Consommation finale : 300 - 60 - 40 = 200 kWh ; économie : 100 kWh, soit un tiers de la référence. L’affiche précise le même service, les durées supposées et le caractère estimé des chiffres. Elle distingue économies à l’usage et impacts du matériel. Elle ne prétend pas que l’énergie ou les impacts deviennent nuls.'))

CHAPITRES_ENERGIE=[C12,C13,C14,C15,C16]
