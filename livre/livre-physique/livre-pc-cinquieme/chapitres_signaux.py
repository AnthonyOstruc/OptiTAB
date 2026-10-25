"""Lumière, sons et information : observations et modèles de propagation."""
from programme_complet import *

C17=Chapitre(17,'Que doit-il se passer pour que l’on voie un objet ?',[
    'Distinguer source primaire et objet diffusant.',
    'Expliquer la vision par de la lumière qui entre dans l’œil.',
    'Comparer matériaux transparents, translucides et opaques.'
],[
Lecon('Produire ou diffuser de la lumière',
    'Une source primaire émet de la lumière qu’elle produit : le Soleil et une lampe allumée en sont des exemples. Un objet diffusant renvoie dans plusieurs directions une partie de la lumière reçue. Une feuille éclairée, une planète ou la Lune sont visibles grâce à cette lumière diffusée. Un objet peut donc nous envoyer de la lumière sans être lui-même une source primaire.',
    ('pc_lightchain',None),'Une source éclaire un objet ; une partie de la lumière diffusée par celui-ci peut atteindre l’œil.',
    'Un objet lumineux pour un observateur peut être une source primaire ou un objet diffusant. Préciser l’origine de la lumière évite l’ambiguïté.',
    'Demander si l’objet produit la lumière ou reçoit celle d’une autre source. Ne pas confondre « brillant », « visible » et « source primaire ».'),
Lecon('La lumière doit entrer dans l’œil',
    'Pour voir un objet, de la lumière provenant de cet objet doit entrer dans l’œil. Un objet opaque non lumineux doit donc être éclairé et diffuser vers l’observateur une partie de la lumière reçue. L’œil n’envoie pas un rayon qui va chercher l’objet. Un obstacle opaque peut empêcher la lumière d’atteindre l’œil, même si l’objet reçoit de la lumière ailleurs dans la pièce.',
    ('pc_lightchain',None),'Les flèches montrent un sens de propagation de la lumière, depuis la source jusqu’à l’œil via l’objet.',
    'Être éclairé ne garantit pas d’être visible pour tous les observateurs. Il faut aussi qu’un chemin de lumière relie l’objet à l’œil.',
    'Tracer deux étapes : source → objet, puis objet → œil. Rechercher les obstacles éventuels sur chaque trajet.'),
Lecon('Traverser un matériau',
    'Un matériau transparent laisse passer de la lumière avec une transmission qui permet de voir nettement à travers dans les conditions étudiées. Un matériau translucide transmet mais diffuse la lumière : on ne voit pas nettement à travers. Un matériau opaque ne transmet pas la lumière visible de façon perceptible dans ces conditions ; il peut en absorber et en diffuser une partie. L’épaisseur et l’état du matériau influencent ces observations.',
    ('pc_materials_light',None),'Modèles simplifiés de la transmission de lumière visible à travers trois matériaux.',
    'Opaque ne veut pas dire noir ; une feuille blanche est opaque et diffuse de la lumière. Transparent ne veut pas dire invisible ni sans réflexion.',
    'Comparer les matériaux devant le même objet et la même source adaptée. Ne jamais utiliser le Soleil ou un laser comme source d’observation directe.')
],Activite('Voir à travers, voir l’objet',
    'Distinguer transmission et diffusion avec une lampe adaptée.',[
    'Le professeur fournit une source de faible puissance adaptée, un objet et des écrans transparent, translucide et opaque. Ne pas diriger une source intense vers les yeux.',
    'Observer l’objet à travers chaque écran, avec un éclairage identique. Noter si sa forme est vue nettement, de façon floue ou pas à travers l’écran.',
    'Dessiner le trajet de la lumière pour l’observation de l’objet éclairé, puis préciser quel écran interrompt ou modifie ce trajet.'
],('pc_materials_light',None),'Observer une même scène à travers plusieurs matériaux ; les résultats dépendent aussi de leur épaisseur.',[
    'Quel écran permet une image nette de l’objet ?',
    'Un écran opaque blanc peut-il être lui-même visible ?',
    'Pourquoi la flèche objet → œil est-elle indispensable dans l’explication ?'
], 'Le matériau transparent permet une observation nette dans les conditions prévues. L’écran opaque blanc peut être visible en diffusant la lumière reçue, tout en empêchant de voir l’objet à travers. La flèche objet → œil représente la lumière qui doit entrer dans l’œil ; l’éclairage de l’objet seul ne suffit pas à expliquer la vision.'),[
    'Une source primaire produit la lumière qu’elle émet.',
    'Un objet diffusant renvoie une partie de la lumière qu’il reçoit.',
    'Voir un objet exige que de la lumière provenant de lui entre dans l’œil.',
    'Transparent, translucide et opaque décrivent des comportements de transmission.',
    'Les flèches d’un schéma lumineux suivent le sens de propagation de la lumière.'
], '« L’œil éclaire l’objet pour le voir. » Dans ce modèle, la lumière entre dans l’œil ; elle n’en sort pas pour rechercher l’objet.',[
E(1,'Deux types de sources',['Classe une lampe allumée et la Lune éclairée : source primaire ou objet diffusant.'],'La lampe allumée est une source primaire ; la Lune éclairée diffuse la lumière du Soleil. Elle ne produit pas cette lumière visible.'),
E(2,'Le sens de la lumière',['Pour voir un livre éclairé, la lumière va-t-elle du livre vers l’œil ou de l’œil vers le livre ?','Que reçoit le livre au départ ?'],'La lumière diffusée va du livre vers l’œil. Le livre reçoit auparavant de la lumière d’une source ; l’œil ne l’éclaire pas pour le voir.'),
E(3,'Un écran blanc',['Une feuille blanche qui bloque la vue à travers elle est-elle opaque ?','Peut-elle être visible quand elle est éclairée ?'],'Oui, elle peut être opaque tout en étant visible grâce à la lumière qu’elle diffuse. Opaque et invisible ne sont pas synonymes.'),
E(4,'Nommer un matériau',['Un verre dépoli transmet de la lumière mais ne permet pas une vision nette à travers. Comment le qualifier ?','Comment qualifie-t-on une vitre permettant une vision nette ?'],'Le verre dépoli est translucide dans ces conditions. Une vitre permettant une vision nette est transparente.'),
E(5,'Lire les flèches',['Quel rôle joue l’objet central ?','Quelle flèche correspond à la lumière qui entre dans l’œil ?'],'L’objet central diffuse une partie de la lumière reçue. La flèche allant de l’objet à l’œil représente la lumière reçue par l’observateur.',figure=('pc_lightchain',None)),
E(6,'Dans l’obscurité',['Un objet non lumineux peut-il être vu dans une obscurité totale s’il n’émet aucune lumière ?','Quelle condition manque ?'],'Non dans le modèle étudié : aucune lumière provenant de lui n’entre dans l’œil. Il faut un éclairage et un trajet de lumière vers l’observateur.'),
E(7,'Un objet caché',['Une lampe éclaire un livre, mais un écran opaque masque le livre à l’observateur. Pourquoi peut-il ne pas le voir ?','Quelle étape de la chaîne est interrompue ?'],'L’écran interrompt le trajet de lumière entre le livre et l’œil. Le trajet source-livre peut rester possible ; cela ne suffit pas pour assurer la vision de l’objet.'),
E(8,'Brillant ne veut pas dire primaire',['Une cuillère éclairée brille. Pourquoi cela ne prouve-t-il pas qu’elle produit sa propre lumière ?','Quelle origine de la lumière peut-on proposer ?'],'Elle peut renvoyer la lumière d’une source extérieure. Le fait de paraître brillante ne démontre pas une production de lumière ; il faut rechercher l’origine du rayonnement reçu par l’œil.'),
E(9,'Comparer les trois écrans',['Quel matériau interrompt la transmission représentée ?','Quel matériau disperse les directions transmises ?'],'Le matériau opaque interrompt la transmission visible du schéma. Le translucide transmet dans plusieurs directions, ce qui empêche ici une observation nette à travers.',figure=('pc_materials_light',None)),
E(10,'Éteindre la source',['Une lampe éclaire une balle non lumineuse. On éteint la seule source dans la pièce. Que devient la condition de visibilité ?','Précise l’hypothèse importante.'],'La balle ne reçoit plus l’éclairage nécessaire et ne peut plus diffuser cette lumière vers l’œil. On suppose qu’aucune autre source ni lumière extérieure n’éclaire la scène.'),
E(11,'Une planète visible',['Pourquoi une planète peut-elle être observée alors qu’elle n’est pas une étoile ?','Quel astre fournit principalement la lumière visible diffusée dans le Système solaire ?'],'Elle diffuse une partie de la lumière solaire reçue. Le Soleil est la source primaire principale considérée pour sa visibilité.'),
E(12,'Un schéma à corriger',['Un dessin montre uniquement une flèche œil → objet pour expliquer la vision. Que faut-il modifier ?','Quelle autre information est nécessaire pour un objet diffusant ?'],'Inverser la flèche pour représenter la lumière objet → œil. Ajouter une source qui éclaire l’objet, puis le trajet source → objet. La légende doit préciser qu’on suit la lumière.'),
E(13,'Transparent et réflexion',['Peut-on voir le reflet d’une vitre qui laisse aussi voir à travers ?','Pourquoi cela ne contredit-il pas sa transparence ?'],'Oui. Une vitre peut transmettre une partie de la lumière et en réfléchir une autre. Transparent ne signifie pas que toute la lumière traverse sans autre effet.'),
E(14,'L’épaisseur du matériau',['Une fine couche laisse passer de la lumière ; une grande épaisseur du même matériau en laisse très peu. Quelle précision faut-il ajouter au classement ?','Comment rendre l’essai comparable ?'],'Préciser l’épaisseur et les conditions d’observation. Comparer avec la même source, le même objet, la même géométrie et des épaisseurs annoncées. Le mot matériau seul ne décrit pas toutes les situations.'),
E(15,'Préparer une démonstration',['Conçois une explication avec lampe, objet non lumineux et écran opaque pour montrer les deux conditions de vision.','Quel résultat attendre en masquant chacun des deux trajets ?'],'Éclairer l’objet et observer la lumière diffusée vers l’œil. Masquer source-objet empêche l’éclairage ; masquer objet-œil empêche la lumière diffusée d’atteindre l’observateur. Utiliser une source scolaire adaptée et ne pas diriger une lumière intense vers les yeux.')
],Defi('La boîte à regarder',
    'Une boîte opaque contient une balle non lumineuse. Un trou sert à regarder ; un autre laisse entrer la lumière d’une lampe adaptée. On peut boucher chaque trou séparément. Prépare une explication des observations.',
    ('pc_lightchain',None),['Décris les deux trajets nécessaires pour voir la balle.','Prévois le résultat si le trou d’éclairage est bouché, sans autre source interne.','Explique pourquoi un trou de regard seul ne crée pas de lumière.'],
    'Identifier l’origine de la lumière et sa destination finale dans l’œil.',
    'La lumière doit entrer dans la boîte, atteindre la balle puis être diffusée vers l’œil par le trou de regard. Si l’unique éclairage est bloqué, la balle ne reçoit plus la lumière requise. Un trou de regard ne produit pas de lumière ; il permet seulement un trajet. Une autre lumière parasite doit être exclue pour interpréter le test.'))

C18=Chapitre(18,'Comment prévoir la position et la taille d’une ombre ?',[
    'Utiliser la propagation rectiligne dans un milieu transparent homogène.',
    'Tracer des rayons orientés et reconnaître les limites du modèle.',
    'Distinguer ombre propre, zone d’ombre et ombre portée.'
],[
Lecon('Un modèle de propagation rectiligne',
    'Dans un milieu transparent homogène, la lumière se propage en ligne droite. On représente un trajet par un rayon : un trait rectiligne fléché dans le sens de propagation. Un faisceau est un ensemble de rayons ; le trait du schéma n’est pas un fil matériel. Pour laisser passer la lumière d’une petite source à travers plusieurs trous, les trous doivent être alignés avec la source dans le modèle.',
    ('pc_aligned',False),'Trois trous alignés laissent passer un trajet lumineux direct. Source scolaire adaptée uniquement.',
    'La règle de ligne droite s’applique aux conditions annoncées. La lumière peut changer de direction à une interface ou sur un miroir ; ces situations ne sont pas modélisées ici.',
    'Placer d’abord la source, les ouvertures et l’écran, puis tracer à la règle les trajets possibles avec des flèches.'),
Lecon('Un objet opaque arrête certains trajets',
    'Un objet opaque intercepte une partie de la lumière d’une source. Derrière lui, certains points ne reçoivent pas la lumière directe de cette source : ils appartiennent à une zone d’ombre. Avec une petite source assimilée à un point, on peut tracer deux rayons limites passant au bord de l’objet. Leur prolongement délimite la zone d’ombre et sa rencontre avec un écran.',
    ('pc_shadow',None),'Vue de côté avec une source ponctuelle S et un objet opaque ; les rayons limites sont prolongés jusqu’à l’écran.',
    'Un rayon limite est un outil géométrique. Il ne traverse pas l’objet opaque : il passe au bord et délimite les trajets bloqués.',
    'Relier la source aux deux bords pertinents de l’objet, puis prolonger jusqu’à l’écran. Hachurer ou colorer seulement la zone privée de lumière directe.'),
Lecon('Distinguer les différentes ombres',
    'L’ombre propre est la partie de la surface de l’objet non directement éclairée par la source. La zone d’ombre est la région de l’espace située derrière l’objet qui ne reçoit pas directement cette lumière. L’ombre portée est la tache obtenue lorsque cette zone rencontre un écran. À source et écran fixes, rapprocher l’objet de la source agrandit son ombre portée dans ce modèle de petite source.',
    ('pc_shadows',None),'Une seule petite source est considérée. Les lumières diffusées par la pièce sont négligées dans ce modèle.',
    'Une ombre dépend de la source, de l’objet et de l’écran. Sa taille ne se déduit pas de la seule taille de l’objet.',
    'Pour comparer deux essais, fixer deux positions et ne déplacer que le troisième élément. Préciser ce qui reste fixe avant d’annoncer une règle.')
],Activite('Faire varier une ombre',
    'Tester l’effet de la position d’un objet sur son ombre portée.',[
    'Avec le professeur, utiliser une petite source adaptée, un objet opaque et un écran. Ne pas employer de laser ni regarder une source intense.',
    'Garder source et écran fixes. Placer l’objet à deux positions entre eux, puis comparer la taille de l’ombre portée.',
    'Tracer les deux constructions dans le cahier avec les mêmes échelles et le même objet.'
],('pc_shadow',None),'Le schéma est un modèle de côté ; il ne représente pas la lumière parasite de la pièce.',[
    'Quel élément doit-on déplacer seul pour tester la règle annoncée ?',
    'Quand l’objet se rapproche de la source, comment évolue l’ombre portée ?',
    'Pourquoi faut-il garder la même source et le même écran ?'
], 'On déplace seulement l’objet, entre source et écran fixes. Dans le modèle de petite source, son ombre portée grandit lorsqu’il se rapproche de la source. Garder la source, l’écran, l’objet et les autres conditions identiques permet d’attribuer la variation à la seule position. Une source étendue ou d’autres éclairages peuvent rendre les limites moins nettes.'),[
    'Dans un milieu transparent homogène, les trajets lumineux sont rectilignes.',
    'Un rayon est un trait fléché qui représente un trajet possible.',
    'Un objet opaque intercepte des trajets lumineux.',
    'Ombre propre, zone d’ombre et ombre portée désignent des régions différentes.',
    'La géométrie source-objet-écran détermine l’ombre dans le modèle choisi.'
], '« L’ombre a toujours la taille de l’objet. » Sa taille dépend aussi des distances à la source et à l’écran.',[
E(1,'Une condition de milieu',['Dans quelles conditions du cours représente-t-on la propagation par une droite ?','Quel symbole ajoute-t-on pour donner le sens ?'],'Dans un milieu transparent homogène. Une flèche indique le sens de propagation de la lumière sur le rayon représenté.'),
E(2,'Nommer un rayon',['Un rayon lumineux est-il un fil matériel ?','Quel est son rôle dans un schéma ?'],'Non : c’est une représentation géométrique d’un trajet de lumière. Le trait fléché aide à prévoir les chemins possibles et ne décrit pas un objet matériel tendu dans l’espace.'),
E(3,'Les trous alignés',['Pourquoi l’alignement des trous est-il important ?','Que se passe-t-il si un écran masque le trajet direct ?'],'La propagation rectiligne exige un trajet droit qui passe par les ouvertures. Si un écran opaque masque ce trajet, la lumière directe ne poursuit pas ce chemin.',figure=('pc_aligned',False)),
E(4,'L’ombre sur un mur',['Comment nomme-t-on la tache sombre obtenue sur un écran derrière un objet opaque ?','Comment nomme-t-on la partie non directement éclairée de l’objet ?'],'La tache sur l’écran est l’ombre portée. La partie de la surface de l’objet non directement éclairée est l’ombre propre.'),
E(5,'Un objet opaque',['Un objet transparent donne-t-il nécessairement le même résultat qu’un objet opaque ?','Quelle propriété de l’objet opaque est utilisée dans le modèle ?'],'Non. Le modèle d’ombre utilisé suppose que l’objet intercepte les trajets lumineux. Un matériau transparent transmet une partie de la lumière et demande une analyse différente.'),
E(6,'Une ouverture déplacée',['Le trou de l’écran central est décalé. Pourquoi le trajet représenté s’arrête-t-il ?','Faut-il dessiner un rayon courbé pour qu’il rejoigne le trou ?'],'Il rencontre la partie opaque de l’écran central. On ne courbe pas artificiellement le rayon pour rejoindre l’ouverture : dans le milieu homogène du modèle, le trajet reste rectiligne.',figure=('pc_aligned',True)),
E(7,'Repérer les limites',['Où passent les deux rayons limites ?','À quoi sert leur prolongement ?'],'Ils partent de la source ponctuelle et passent aux bords de l’objet opaque. Leur prolongement délimite la zone d’ombre et la taille de l’ombre portée sur l’écran.',figure=('pc_shadow',None)),
E(8,'Déplacer l’objet',['Source et écran sont fixes. L’objet se rapproche de la petite source. Comment évolue l’ombre portée ?','Quelle condition dois-tu conserver dans la réponse ?'],'Elle grandit dans le modèle étudié. Il faut préciser que source et écran restent fixes et que l’on utilise la même petite source et le même objet entre les deux.'),
E(9,'Un écran derrière l’objet',['Un écran est placé hors de la zone d’ombre. Reçoit-il nécessairement la même tache sombre ?','Pourquoi sa position compte-t-elle ?'],'Non. L’ombre portée correspond à la rencontre de l’écran avec la zone d’ombre. Déplacer l’écran peut modifier la tache ou le placer en dehors de cette région.'),
E(10,'Deux essais comparables',['Un groupe change à la fois la lampe, l’objet et la distance de l’écran. Peut-il attribuer une variation d’ombre à la seule distance ?','Propose un essai mieux contrôlé.'],'Non. Conserver la même source, le même objet, le même écran et ne faire varier qu’une distance définie. Noter toutes les positions pour pouvoir comparer.'),
E(11,'Le sens des flèches',['Pourquoi les flèches partent-elles de S vers l’écran dans la construction ?','Le sens de lecture de la page décide-t-il de leur orientation ?'],'Les flèches suivent la propagation depuis la source. Leur sens n’est pas choisi selon la lecture gauche-droite : si la source est à droite, les flèches peuvent pointer vers la gauche.'),
E(12,'Une ombre moins nette',['L’expérience réelle montre des bords moins nets que le schéma. Donne deux explications compatibles avec les limites annoncées.'],'La source peut être étendue plutôt que ponctuelle, et d’autres lumières peuvent éclairer la zone. L’objet et l’écran peuvent aussi être mal positionnés. Le modèle simplifié ne prétend pas reproduire tous les détails.'),
E(13,'Distinguer trois régions',['Explique la différence entre ombre propre, zone d’ombre et ombre portée sans employer trois fois seulement le mot « sombre ».'],'L’ombre propre appartient à la surface de l’objet ; la zone d’ombre est un volume de l’espace qui ne reçoit pas directement la source ; l’ombre portée est l’intersection de cette zone avec un écran. La localisation distingue les trois notions.'),
E(14,'Une construction impossible',['Un élève trace un rayon qui traverse le centre d’un objet opaque pour rejoindre l’écran. Quelle erreur commet-il ?','Comment construire les limites correctes ?'],'Il fait traverser la lumière à travers l’objet supposé opaque. Les rayons limites passent par les bords de l’objet depuis la source ; on les prolonge jusqu’à l’écran sans les faire traverser le solide.'),
E(15,'Confronter modèle et mesure',['La construction prévoit une ombre plus grande lorsque l’objet approche de la source, mais la mesure paraît inchangée. Que vérifier avant de rejeter la règle ?','Quelle limite de mesure peut intervenir ?'],'Vérifier les positions réellement fixes, la direction du déplacement, la taille de la source et la précision de mesure. Un déplacement trop faible peut produire une variation inférieure à la résolution de la mesure. Refaire une comparaison contrôlée et conserver les résultats observés.')
],Defi('Le théâtre d’ombres',
    'Pour un petit théâtre d’ombres de classe, on souhaite agrandir la silhouette d’un même objet sans changer la source ni déplacer l’écran. La source est petite et les autres éclairages sont limités.',
    ('pc_shadows',None),['Quel déplacement de l’objet proposer ?','Dessine les rayons limites avant et après.','Explique les limites de la prévision pour une lampe très étendue.'],
    'Comparer les angles sous lesquels les bords de l’objet sont vus depuis la petite source.',
    'Rapprocher l’objet de la source en le maintenant entre elle et l’écran. Les rayons limites s’écartent davantage avant d’atteindre l’écran : la silhouette grandit. Une source étendue peut donner des bords moins nets ; il faut alors compléter le modèle ou tester le résultat. Utiliser uniquement la lampe adaptée fournie pour l’activité.'))

C19=Chapitre(19,'Pourquoi entend-on un objet qui vibre ?',[
    'Relier l’émission d’un son à une vibration.',
    'Identifier le milieu de propagation et utiliser une vitesse fournie.',
    'Distinguer hauteur d’un son, niveau sonore et conditions d’écoute.'
],[
Lecon('Une vibration à l’origine du son',
    'Une source sonore met en vibration un milieu matériel : corde, membrane, règle ou colonne d’air, par exemple. La perturbation se transmet de proche en proche dans le milieu et peut atteindre un récepteur comme l’oreille ou un microphone. L’air ne se déplace pas tout entier depuis la source jusqu’à l’oreille avec le son ; il transmet une perturbation. Une vibration peut rester peu visible tout en étant audible.',
    ('pc_vibration',None),'Une règle vibre et met l’air en vibration ; la flèche indique la propagation, pas le transport de toute la matière.',
    'L’émetteur vibre, le milieu transmet et le récepteur reçoit. Ces trois rôles doivent être distingués dans l’explication.',
    'Identifier ce qui vibre à la source et le milieu situé entre source et récepteur. Ne pas répondre seulement « le son va dans l’air ».'),
Lecon('Un milieu et une durée de propagation',
    'Le son se propage dans les gaz, les liquides et les solides, avec une vitesse qui dépend du milieu et de ses conditions. Il ne se propage pas dans le vide. Dans l’air proche de la température ambiante, on utilise ici la valeur arrondie de 340 m/s. Le son met donc un temps mesurable à parcourir une distance. Un écho correspond à un trajet aller puis retour après réflexion.',
    ('pc_vacuum_sound',None),'Une sonnerie reste en fonctionnement sous une cloche ; raréfier l’air atténue la transmission par l’air. D’autres chemins par les supports peuvent subsister.',
    'Pour un écho, la distance parcourue par le son est deux fois la distance de l’obstacle dans le modèle d’aller-retour direct.',
    'Utiliser distance = vitesse × durée avec la valeur fournie. Dessiner le trajet avant de diviser par deux pour une distance à un obstacle.'),
Lecon('Aigu, grave, fort : des propriétés différentes',
    'La hauteur distingue un son aigu d’un son grave : une vibration plus rapide correspond à une fréquence plus élevée, exprimée en hertz (Hz). Le niveau sonore, exprimé en décibels (dB), renseigne sur une autre propriété liée à la force du son reçu. On peut donc avoir un son grave fort ou aigu faible. Les risques auditifs dépendent notamment du niveau et de la durée d’exposition, pas seulement du caractère agréable du son.',
    ('pc_soundtrace',None),'Traces schématiques à mêmes échelles de temps et d’amplitude : B présente plus d’oscillations que A ; C a une amplitude plus grande que A.',
    'Réduire le niveau d’écoute, limiter la durée et s’éloigner des sources fortes protège l’audition. Une exposition gênante doit être interrompue ; ne pas attendre une douleur pour réduire le son.',
    'Comparer d’abord le nombre d’oscillations sur une même durée, puis l’amplitude sur une même échelle. Ne pas additionner les décibels comme des longueurs.')
],Activite('Observer et enregistrer une vibration',
    'Mettre en relation une source vibrante et un signal enregistré à niveau modéré.',[
    'Avec le professeur, faire vibrer doucement une règle maintenue sur une table ou utiliser une source scolaire adaptée. Garder les oreilles à distance raisonnable.',
    'Observer le mouvement et, si le matériel le permet, enregistrer un signal avec un microphone. Conserver les réglages pour comparer deux essais.',
    'Sans enregistrement, exploiter les trois traces schématiques proposées et leurs échelles identiques.'
],('pc_soundtrace',None),'A et C ont le même nombre d’oscillations ; B en présente davantage sur la même durée.',[
    'Quelle trace correspond à une vibration plus rapide que A ?',
    'Quelle trace garde le même rythme mais une plus grande amplitude ?',
    'Pourquoi modifier le volume n’est-il pas la même chose que modifier la hauteur ?'
], 'B présente davantage d’oscillations que A pendant la même durée : sa fréquence est plus élevée. C conserve le rythme de A mais avec une amplitude plus grande dans ce modèle. Hauteur et niveau sonore ne sont donc pas la même propriété. La comparaison suppose les mêmes échelles et les mêmes réglages d’acquisition ; l’activité ne demande pas de produire des sons forts.'),[
    'Un son provient d’une source qui vibre.',
    'Sa propagation exige un milieu matériel ; elle n’a pas lieu dans le vide.',
    'Dans l’air ambiant, on utilise souvent environ 340 m/s.',
    'Fréquence et hauteur diffèrent du niveau sonore.',
    'Le niveau, la durée et la distance à la source comptent pour l’exposition sonore.'
], '« Un son aigu est forcément plus fort. » La hauteur et le niveau sonore sont deux propriétés différentes.',[
E(1,'À la source',['Quel mouvement d’une membrane de haut-parleur est à l’origine du son ?','Comment nomme-t-on un dispositif qui reçoit ce son pour l’enregistrer ?'],'La membrane vibre. Un microphone peut recevoir le signal sonore et permettre son enregistrement. L’émetteur et le récepteur ont des rôles distincts.'),
E(2,'Le milieu nécessaire',['Le son peut-il se propager dans le vide ?','Donne deux types de milieux matériels où il peut se propager.'],'Le son ne se propage pas dans le vide. Il peut se propager dans un gaz comme l’air, dans un liquide ou dans un solide, avec des vitesses différentes.'),
E(3,'Une vitesse avec son unité',['Quelle valeur arrondie utilise le cours pour le son dans l’air ambiant ?','Quelle unité accompagne 340 ?'],'On utilise environ 340 m/s. La vitesse est exprimée en mètres par seconde ; 340 seul ne constitue pas un résultat complet.'),
E(4,'Deux propriétés',['Un son est grave et fort. Ces deux mots décrivent-ils la même propriété ?','Quelle propriété est associée à la fréquence ?'],'Non. Grave décrit la hauteur ; fort décrit le niveau reçu. La fréquence est liée à la hauteur : une fréquence plus élevée correspond à un son plus aigu.'),
E(5,'Une protection raisonnée',['Cite deux moyens de réduire l’exposition à un son trop fort.','Faut-il attendre d’avoir mal pour agir ?'],'Réduire le niveau, limiter la durée et s’éloigner de la source sont des moyens de réduire l’exposition. Il ne faut pas attendre la douleur pour diminuer un son gênant ou trop fort.'),
E(6,'Distance parcourue en une seconde',['Avec 340 m/s, quelle distance le son parcourt-il en 1 s dans le modèle ?','Et en 2 s ?'],'Il parcourt environ 340 m en 1 s et 680 m en 2 s, si les conditions de propagation restent celles du modèle.',check='340*2==680'),
E(7,'Un trajet direct',['Deux points sont séparés de 170 m. Calcule la durée de propagation directe avec 340 m/s.','L’unité du résultat est-elle le mètre ?'],'170 ÷ 340 = 0,5 s. Le résultat est une durée en secondes, pas une distance en mètres.',check='170/340==0.5'),
E(8,'Comparer des traces',['Quelle trace a une fréquence plus élevée que A ?','Entre A et C, qu’est-ce qui change dans le modèle ?'],'B présente plus d’oscillations dans la même durée : sa fréquence est plus élevée. Entre A et C, l’amplitude change tandis que le rythme des oscillations reste identique.',figure=('pc_soundtrace',None)),
E(9,'La cloche et le vide',['Pourquoi le son transmis par l’air s’atténue-t-il lorsqu’on raréfie fortement l’air ?','Pourquoi faut-il mentionner les supports du montage ?'],'Le milieu gazeux qui transmet la perturbation est fortement raréfié. Les supports solides peuvent encore transmettre des vibrations ; l’expérience réelle ne se réduit pas à un trajet uniquement dans l’air.',figure=('pc_vacuum_sound',None)),
E(10,'Un écho simple',['Un écho revient 1 s après un son bref. Quelle distance totale le son a-t-il parcourue ?','À quelle distance se situe l’obstacle dans le modèle aller-retour ?'],'Distance totale : 340 × 1 = 340 m. L’obstacle est à 340 ÷ 2 = 170 m, car le son parcourt l’aller et le retour.',figure=('pc_echo',None),check='340/2==170'),
E(11,'La matière ne voyage pas tout entière',['Pourquoi la flèche de propagation n’indique-t-elle pas que l’air de la source arrive entièrement dans l’oreille ?','Qu’est-ce qui se transmet ?'],'Une perturbation vibratoire se transmet de proche en proche dans le milieu. Cela ne signifie pas que toute la masse d’air parcourt le trajet depuis la source jusqu’au récepteur.'),
E(12,'Un délai de 3 secondes',['Un signal lumineux et un son sont émis simultanément à distance. Le son arrive environ 3 s plus tard ; on néglige ici le temps de la lumière. Estime la distance.','Quelle approximation utilises-tu ?'],'La distance est environ 340 × 3 = 1 020 m. On utilise une propagation directe dans l’air avec 340 m/s et on néglige le temps de propagation de la lumière sur cette distance.',check='340*3==1020'),
E(13,'Un écho plus rapide',['Le retour d’un écho prend 0,4 s. Calcule la distance de l’obstacle.','Quelle erreur donnerait une distance deux fois trop grande ?'],'Distance parcourue : 340 × 0,4 = 136 m. Distance à l’obstacle : 68 m. Oublier de diviser le trajet aller-retour par deux donnerait 136 m.',check='340*0.4/2==68'),
E(14,'Comparer des enregistrements',['Deux traces ont le même nombre apparent d’oscillations, mais l’une représente 1 s et l’autre 2 s. Peut-on conclure à la même hauteur ?','Quel contrôle manque ?'],'Non. Le nombre d’oscillations doit être comparé sur une même durée ; à nombre égal sur deux fois plus de temps, le rythme est plus faible. Il faut vérifier les échelles temporelles avant la comparaison.'),
E(15,'Une idée à discuter',['« Ma musique préférée ne peut pas abîmer l’audition. » Explique pourquoi cette affirmation est fausse.','Quelles données comptent davantage que le goût musical ?'],'Le caractère agréable ne supprime pas le risque lié à une exposition trop intense ou trop longue. Le niveau reçu, la durée, la distance et les protections comptent. Une gêne ou des signes inhabituels doivent conduire à arrêter l’exposition et à en parler à un adulte.')
],Defi('Le mur repéré par un écho',
    'Un document d’acquisition donne un écho 0,6 s après l’émission d’un son bref. Le trajet est direct jusqu’à un mur puis revient au récepteur situé près de la source. On utilise 340 m/s et on néglige les autres réflexions.',
    ('pc_echo',None),['Dessine l’aller et le retour.','Calcule la distance parcourue par le son puis la distance au mur.','Explique pourquoi une mesure réelle peut différer légèrement du modèle.'],
    'La durée fournie concerne le trajet complet, pas seulement l’aller.',
    'Le son parcourt environ 340 × 0,6 = 204 m au total ; le mur est à environ 102 m. Les deux trajets doivent être comptés. La température, la précision de mesure, l’emplacement du récepteur et d’autres réflexions peuvent produire des écarts. Le résultat est une estimation dans les conditions du document.'))

C20=Chapitre(20,'Comment un signal devient-il une information ?',[
    'Identifier émetteur, signal, milieu et récepteur.',
    'Utiliser un code simple pour transmettre un message.',
    'Distinguer signal et information, et exploiter un délai de transmission.'
],[
Lecon('De l’émetteur au récepteur',
    'Un signal est une variation physique que l’on peut émettre, transmettre et recevoir. Il peut être lumineux ou sonore dans les exemples du livre. L’émetteur le produit ; un milieu ou un trajet permet sa propagation ; un récepteur le détecte. L’information est le sens que l’on attribue à ce signal à l’aide de règles et d’un contexte. Le même signal peut porter des informations différentes selon le code partagé.',
    ('pc_signal',None),'Un signal physique et le message interprété ne sont pas la même chose.',
    'Un voyant rouge ne signifie pas à lui seul la même chose sur tous les appareils. Il faut connaître sa fonction ou sa légende.',
    'Présenter la chaîne : émetteur → nature du signal et trajet → récepteur → information interprétée. Vérifier que les participants partagent le même code.'),
Lecon('Coder avec deux états',
    'On peut coder un message avec deux états distinguables : lampe allumée ou éteinte, notés 1 et 0. Il faut aussi convenir des durées, du début et de la fin du message et de la façon de regrouper les valeurs. Avec des groupes de deux valeurs, les combinaisons 00, 01, 10 et 11 permettent de coder quatre symboles. Un état physique n’acquiert son sens qu’avec le code annoncé.',
    ('pc_code',None),'Huit intervalles identiques portent huit valeurs. Le découpage en groupes doit être convenu avant la transmission.',
    'Un zéro peut porter de l’information : il ne signifie pas nécessairement une absence de message. Un signal trop faible ou masqué peut entraîner une erreur de lecture.',
    'Écrire le tableau du code, repérer les intervalles, puis regrouper les valeurs sans en sauter. Relire le résultat avec le récepteur.'),
Lecon('Mesurer et transmettre prend du temps',
    'Un capteur transforme une grandeur mesurée en un signal exploitable. Par exemple, une température peut donner un signal électrique ensuite utilisé pour un affichage. Une variation continue et une suite de valeurs codées ne se décrivent pas de la même manière. La propagation prend aussi un temps : la lumière voyage dans le vide à environ 300 000 km/s, bien plus vite que le son dans l’air, sans être instantanée.',
    ('pc_sensor',None),'Le capteur relie une grandeur physique à un signal ; l’affichage utilise une conversion et un code.',
    'Une valeur affichée dépend du capteur, de son réglage et de sa précision. La lecture d’un écran ne dispense pas de vérifier l’unité ni les conditions de mesure.',
    'Pour un délai de propagation, utiliser la distance et la vitesse dans des unités compatibles. Préciser si la durée concerne un aller simple ou un aller-retour.')
],Activite('Transmettre quatre symboles',
    'Mettre à l’épreuve un code lumineux simple à faible intensité.',[
    'Convenir du code A = 10, B = 01, C = 11, D = 00 ; choisir des intervalles de 1 s et une longueur de message connue. Utiliser une lampe adaptée, sans viser les yeux.',
    'Préparer le message ACDA en groupes de deux valeurs, puis transmettre avec un repère de départ partagé.',
    'Faire noter les huit valeurs par le récepteur avant de traduire. Comparer les erreurs possibles si le début ou les intervalles sont mal repérés.'
],('pc_code',[1,0,1,1,0,0,1,0]),'Code de l’activité : 10 | 11 | 00 | 10. Chaque valeur occupe ici un intervalle de 1 s.',[
    'Quel message le récepteur doit-il retrouver ?',
    'Quelle durée faut-il pour les huit intervalles, hors préparation ?',
    'Pourquoi le début, la durée des intervalles et le tableau de code sont-ils indispensables ?'
], 'Le message est ACDA. Les huit intervalles de 1 s durent 8 s. Sans synchronisation de départ ou sans durée commune, le récepteur peut décaler le regroupement. Sans le tableau partagé, les mêmes valeurs ne donnent pas nécessairement le même message. La longueur connue aide aussi à distinguer les zéros de fin et une transmission terminée.'),[
    'Un signal physique est produit, transmis et reçu.',
    'L’information dépend d’un code et d’un contexte partagés.',
    'Un codage à deux états nécessite un repérage des durées et des groupes.',
    'Un capteur associe une grandeur mesurée à un signal exploitable.',
    'La propagation lumineuse ou sonore a une vitesse finie et un délai.'
], '« Une lampe éteinte ne transmet rien. » Dans un code convenu, un intervalle éteint peut représenter la valeur 0 et porter de l’information.',[
E(1,'Nommer les rôles',['Une lampe clignote et un capteur la détecte. Qui est l’émetteur et qui est le récepteur ?','Quelle est la nature du signal ?'],'La lampe est l’émetteur et le capteur le récepteur. Le signal est lumineux. L’information dépend du code attribué au clignotement.'),
E(2,'Signal ou information ?',['Pour une sonnette, distingue la variation physique entendue et le sens habituel donné au son.'],'Le signal est sonore. L’information habituelle est qu’une personne appelle à la porte, selon le contexte. Le son et son interprétation sont deux éléments distincts.'),
E(3,'Deux valeurs possibles',['Quels états d’une lampe peuvent coder 1 et 0 ?','L’état 0 peut-il faire partie d’un message ?'],'On peut convenir que 1 signifie allumée et 0 éteinte pendant un intervalle. L’état 0 fait partie du message si le code et les durées sont partagés.'),
E(4,'Quatre combinaisons',['Liste tous les groupes différents de deux valeurs 0 ou 1.','Combien de symboles peuvent-ils représenter avec un code sans ambiguïté ?'],'00, 01, 10 et 11 : quatre groupes différents. On peut leur attribuer quatre symboles distincts, à condition de connaître le découpage en groupes.'),
E(5,'Lire les valeurs',['Écris la suite des huit valeurs.','Combien de groupes de deux contient-elle ?'],'La suite est 10110010. Elle contient quatre groupes de deux : 10 | 11 | 00 | 10. La lecture respecte les intervalles et leur ordre.',figure=('pc_code',None)),
E(6,'Décoder un message',['Avec A = 10, B = 01, C = 11, D = 00, décode 10 | 01 | 11.','Pourquoi les séparations sont-elles utiles ?'],'Le message est ABC. Les séparations indiquent les groupes à traduire et évitent un décalage de lecture.'),
E(7,'Coder un autre message',['Avec le même code, écris DAB en groupes.','Combien d’intervalles sont nécessaires ?'],'DAB donne 00 | 10 | 01, soit six intervalles. La longueur du message doit être connue ou sa fin signalée par une règle convenue.'),
E(8,'Calculer la durée',['Huit valeurs occupent chacune 0,5 s. Quelle durée totale faut-il, hors préparation ?','Quelle donnée modifierait ce résultat ?'],'8 × 0,5 = 4 s. Une durée différente d’intervalle ou l’ajout de pauses de séparation modifierait la durée totale.',check='8*0.5==4'),
E(9,'Un capteur de température',['Quelle grandeur est mesurée par le capteur ?','Pourquoi faut-il vérifier l’unité sur l’affichage ?'],'Il mesure une température. Une valeur affichée sans unité ne permet pas de savoir précisément ce qui est annoncé ; l’unité et les conditions de mesure restent nécessaires.',figure=('pc_sensor',None)),
E(10,'Un délai lumineux fourni',['La lumière parcourt 600 000 km dans le vide. Avec 300 000 km/s, quelle durée de propagation obtient-on ?','La propagation est-elle instantanée ?'],'600 000 ÷ 300 000 = 2 s environ. La durée est courte mais non nulle : la propagation n’est pas instantanée.',check='600000/300000==2'),
E(11,'Un code non partagé',['Deux groupes donnent des lettres différentes à 10. Pourquoi peuvent-ils lire des messages différents à partir du même signal ?','Que faut-il convenir avant ?'],'L’interprétation dépend du tableau de code. Les groupes doivent partager les mêmes associations, le découpage et les durées avant la transmission pour retrouver la même information.'),
E(12,'La lumière du Soleil',['On utilise 150 millions de km et 300 000 km/s. Calcule la durée approximative du trajet Soleil-Terre.','Exprime-la en minutes et secondes.'],'150 000 000 ÷ 300 000 = 500 s, soit 8 min 20 s. Ce calcul emploie une distance moyenne et une vitesse arrondie ; le résultat est un ordre de grandeur.',check='150000000/300000==500 and 8*60+20==500'),
E(13,'Un décalage de début',['Pourquoi commencer à lire une valeur trop tard peut-il changer tout un message codé par groupes de deux ?','Propose une règle de départ.'],'Le regroupement peut être décalé et attribuer de mauvais couples aux symboles. Convenir d’un signal de départ distinct ou d’un compte à rebours et d’une longueur de message connue permet de synchroniser la lecture.'),
E(14,'Un signal masqué',['Une lumière ambiante empêche de distinguer lampe allumée et éteinte. Le tableau de code suffit-il à corriger le problème ?','Quel aspect de la chaîne faut-il améliorer ?'],'Non. Il faut d’abord que les deux états physiques soient détectables. Améliorer le contraste et les conditions de réception avec le matériel adapté, sans augmenter dangereusement l’intensité vers les yeux.'),
E(15,'Deux sens pour le même voyant',['Un voyant rouge signifie « enregistrement » sur un appareil et « défaut » sur un autre. Est-ce une contradiction physique ?','Quelle distinction explique la situation ?'],'Non. Le signal physique peut être semblable tandis que l’information change avec le code et le contexte de l’appareil. Lire la légende ou la notice permet d’interpréter le voyant correctement.')
],Defi('Un message que l’on peut vérifier',
    'Tu dois transmettre le mot BACA avec le code A = 10, B = 01, C = 11, D = 00. Chaque valeur dure 0,5 s. La longueur est connue du récepteur. Prévois ensuite une méthode simple pour vérifier qu’il a reçu le bon message.',
    ('pc_signal',['Lampe','Signal codé','Observateur']),['Écris les huit valeurs dans l’ordre.','Calcule la durée de transmission, hors préparation et vérification.','Propose une règle de confirmation et explique sa limite.'],
    'Une répétition ou un retour du message peut révéler une erreur, sans garantir à lui seul l’absence de toute erreur.',
    'BACA donne 01 | 10 | 11 | 10, soit 01101110. Huit valeurs de 0,5 s durent 4 s. Le récepteur peut relire ou retransmettre sa suite au premier groupe pour comparaison. Cette confirmation aide à repérer des erreurs, mais une même erreur répétée reste possible ; le code, la synchronisation et les conditions de réception doivent rester contrôlés.'))

CHAPITRES_SIGNAUX=[C17,C18,C19,C20]
