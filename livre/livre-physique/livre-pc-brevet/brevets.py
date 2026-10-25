"""Dix volets PC originaux, 30 minutes, 9 points scientifiques + 1 point de langue."""
from dataclasses import dataclass
from donnees import E
@dataclass
class Partie:
    titre:str
    exercice:object
    points:list
@dataclass
class Sujet:
    numero:int
    titre:str
    chapitres:list
    parties:list
def P(titre,document,figure,questions,reponses,points,calculs=None):
    e=E(titre,questions,reponses,document,figure,calculs)
    assert len(e.questions)==len(points)
    return Partie(titre,e,points)
def S(n,titre,chapitres,a,b):
    assert sum(a.points)==4 and sum(b.points)==5
    return Sujet(n,titre,chapitres,[a,b])
SUJETS=[
S(1,'Se déplacer en limitant les rejets',[3,6,8,11,12],
P('Un vélo en mouvement',r'Un ensemble vélo-cycliste de masse $80\unite{kg}$ parcourt une portion rectiligne de 200 m en 40 s. Le graphique fournit les positions relevées. On donne $E_c=\tfrac12 mv^2$, avec les unités SI. Les valeurs sont des données d’étude.','bb01-velo',
r'Décrire le mouvement sur cette portion dans le référentiel de la route.@@Calculer la vitesse moyenne en m/s.@@Calculer l’énergie cinétique correspondant à cette vitesse et prévoir sa valeur si la vitesse double.',
r'Rectiligne uniforme : la position croît linéairement avec le temps. \textbf{Barème :} 0,5 point pour rectiligne ; 0,5 pour uniforme et sa lecture graphique.@@$v=d/\Delta t=200/40=5\unite{m/s}$. \textbf{Barème :} 0,5 pour relation et substitution ; 0,5 pour valeur et unité.@@$E_c=0{,}5\times80\times5^2=1\,000\unite J$. Si v double à masse fixée, $E_c$ est multipliée par quatre : $4\,000\unite J$. \textbf{Barème :} 1 point pour le premier calcul ; 1 pour facteur et seconde valeur.',[1,1,2],[('200/40',5),('.5*80*5**2',1000),('.5*80*10**2',4000)]),
P('Deux solutions énergétiques',r'Pour une comparaison fictive sur le même trajet : solution A, 20 kWh d’électricité avec une émission de cycle de vie fournie de 50 g de CO2 par kWh ; solution B, combustion émettant 4 000 g de CO2. La réaction modèle du combustible est $\ce{CH4 + 2 O2 -> CO2 + 2 H2O}$. Le tableau ne décrit que l’indicateur CO2 fourni, pas tous les impacts.','',
r'Nommer le comburant de la réaction fournie.@@Compter les atomes d’oxygène de chaque côté de l’équation.@@Calculer la masse de CO2 associée à A en kg.@@En quatre à six lignes, comparer A et B sur l’indicateur donné et préciser une limite environnementale de la conclusion.',
r'Le dioxygène, $\ce{O2}$. \textbf{Barème :} 1 point pour le nom.@@Quatre O de chaque côté : quatre à gauche dans $2\,\ce{O2}$ ; deux dans CO2 et deux dans $2\,\ce{H2O}$ à droite. \textbf{Barème :} 0,5 point par côté.@@$20\times50=1\,000\unite g=1{,}0\unite{kg}$. \textbf{Barème :} 0,5 pour produit ; 0,5 pour conversion et unité.@@A est associée à 1,0 kg de CO2 contre 4,0 kg pour B. Dans les conditions et le périmètre des données, A émet quatre fois moins de CO2. Le résultat ne mesure pas tous les impacts, par exemple matériaux, autres polluants ou biodiversité. \textbf{Barème scientifique :} 1 point pour comparaison chiffrée ; 1 pour périmètre et limite pertinente. La langue est appréciée séparément sur l’ensemble du sujet.',[1,1,1,2],[('20*50/1000',1)])),
S(2,'Contrôler une eau au laboratoire',[1,2,4],
P('Masse volumique et mélange',r'Un récipient vide a une masse de 32,0 g. Avec 50,0 mL d’un liquide, sa masse est 82,0 g. Le liquide est transparent et contient des ions dissous. À température de l’étude, la masse volumique de l’eau pure est voisine de 1,00 g/mL.','b01-rho',
r'Calculer la masse de liquide.@@Déterminer sa masse volumique en g/mL.@@Peut-on affirmer que ce liquide est de l’eau pure et potable ? Donner deux arguments distincts.',
r'$m=82{,}0-32{,}0=50{,}0\unite g$. \textbf{Barème :} 0,5 pour soustraction ; 0,5 pour résultat et unité.@@$\rho=m/V=50{,}0/50{,}0=1{,}00\unite{g/mL}$. \textbf{Barème :} 0,5 pour quotient ; 0,5 pour valeur et unité.@@Non. Les ions dissous montrent qu’il ne s’agit pas d’un corps pur constitué uniquement d’eau ; une masse volumique voisine de l’eau ne prouve pas la pureté. La potabilité demande des critères chimiques et microbiologiques supplémentaires. \textbf{Barème :} 1 point pour pureté argumentée ; 1 pour potabilité distincte.',[1,1,2],[('82-32',50),('50/50',1)]),
P('Les résultats d’analyse',r'Le pH vaut 6. Une banque de tests indique : nitrate d’argent + ions chlorure → précipité blanc ; soude + ions cuivre(II) → précipité bleu. Sur deux prélèvements, on obtient un précipité blanc au premier test et aucun bleu au second. Pour Cl, Z = 17.','',
r'Classer le liquide selon son pH.@@Quel ion est mis en évidence par le précipité blanc ?@@Combien d’électrons possède cet ion monoatomique ?@@En quatre à six lignes, proposer les précautions nécessaires pour comparer les tests et préciser la portée du résultat négatif au cuivre.',
r'Acide, car pH 6 est inférieur à 7 vers 25 °C. \textbf{Barème :} 0,5 pour classement ; 0,5 pour critère.@@L’ion chlorure $\ce{Cl-}$. \textbf{Barème :} 1 point pour nom ou formule non ambiguë.@@18 électrons : Z = 17 protons et un électron de plus pour la charge −1. \textbf{Barème :} 0,5 pour 18 ; 0,5 pour justification.@@Utiliser des prélèvements séparés, des réactifs adaptés et des témoins. Respecter les protections et éviter de contaminer les flacons. Le test cuivre négatif indique l’absence de précipité détectable dans les conditions ; une quantité inférieure à la sensibilité du test reste possible. \textbf{Barème scientifique :} 1 point pour protocole et témoin ; 1 pour limite du négatif.',[1,1,1,2],[('17+1',18)])),
S(3,'Éclairer un refuge',[12,13,14,15],
P('Le circuit d’éclairage',r'Une source continue idéale de 12 V alimente deux lampes en dérivation. La première est traversée par 0,30 A, la seconde par 0,20 A. Chaque lampe possède son interrupteur en série dans sa branche.','bb03-refuge',
r'Donner la tension aux bornes de chaque lampe.@@Calculer l’intensité fournie par la source.@@Décrire où brancher un voltmètre pour la première lampe et un ampèremètre pour la seconde.',
r'12 V pour chaque lampe, car elles sont reliées aux mêmes deux nœuds. \textbf{Barème :} 0,5 pour valeurs ; 0,5 pour loi.@@$I_G=0{,}30+0{,}20=0{,}50\unite A$. \textbf{Barème :} 0,5 pour loi ; 0,5 pour calcul.@@Voltmètre en dérivation aux bornes de la première ; ampèremètre en série dans la seconde branche, après coupure avant modification. \textbf{Barème :} 1 point par branchement correct.',[1,1,2],[('.3+.2',.5)]),
P('Une réserve limitée',r'La puissance totale des lampes est constante et vaut 6,0 W. La batterie peut fournir au plus 36 Wh d’énergie utilisable. On néglige les autres consommations. On donne $E=P\Delta t$ et $1\unite{Wh}=3\,600\unite J$.','',
r'Calculer l’énergie utilisée par les deux lampes en 4 h.@@Convertir cette énergie en joules.@@Déterminer la durée maximale théorique à 6,0 W.@@En quatre à six lignes, expliquer pourquoi une durée réelle peut être plus courte et proposer une économie d’énergie justifiée.',
r'$E=6\times4=24\unite{Wh}$. \textbf{Barème :} 0,5 pour relation ; 0,5 pour valeur et unité.@@$24\times3\,600=86\,400\unite J$. \textbf{Barème :} 0,5 pour conversion ; 0,5 pour résultat.@@$\Delta t=36/6=6\unite h$. \textbf{Barème :} 0,5 pour division ; 0,5 pour durée et hypothèse.@@La durée théorique suppose la réserve intégralement utilisable et les seules lampes comme récepteurs. Pertes et autres appareils peuvent réduire l’autonomie. Éteindre une lampe inutile diminue la puissance totale, donc l’énergie reçue pour une même durée. \textbf{Barème scientifique :} 1 point pour une limite liée au modèle ; 1 pour action reliée à E = PΔt.',[1,1,1,2],[('6*4',24),('24*3600',86400),('36/6',6)])),
S(4,'Préparer une mission lunaire',[9,10,16],
P('Peser un équipement',r'Un équipement de masse 12 kg est transporté de la Terre à la Lune. On donne $g_T=10\unite{N/kg}$, $g_L=1{,}6\unite{N/kg}$ et $P=mg$. L’équipement est posé immobile sur un sol horizontal.','b09-poids',
r'Donner sa masse sur la Lune.@@Calculer son poids sur la Lune.@@Décrire les deux forces du modèle d’équilibre sur le sol lunaire, avec leur direction, sens et valeur.',
r'12 kg : le transport ne change pas la masse dans ce contexte. \textbf{Barème :} 1 point pour valeur et distinction.@@$P_L=12\times1{,}6=19{,}2\unite N$. \textbf{Barème :} 0,5 pour relation ; 0,5 pour calcul.@@Poids vertical local vers le centre lunaire et action du sol en sens opposé, de valeurs 19,2 N dans le modèle à deux forces. \textbf{Barème :} 1 point pour poids décrit ; 1 pour support et compensation.',[1,1,2],[('12*1.6',19.2)]),
P('Communiquer avec la Terre',r'La distance Terre-Lune est prise égale à $3{,}84\times10^8\unite m$. Un signal radio voyage à $3{,}00\times10^8\unite{m/s}$ dans le vide. On néglige tous les retards électroniques. La relation de gravitation fournie est $F=Gm_A m_B/d^2$.','bb04-radio',
r'Le signal radio est-il sonore ou électromagnétique ?@@Calculer la durée d’un trajet simple.@@Calculer la durée minimale d’un aller-retour.@@En quatre à six lignes, expliquer pourquoi une station en orbite reste soumise à la gravitation et prévoir l’effet d’une distance centrale doublée sur F, à masses fixées.',
r'Électromagnétique ; il peut se propager dans le vide. \textbf{Barème :} 1 point pour nature.@@$\Delta t=d/c=1{,}28\unite s$. \textbf{Barème :} 0,5 pour relation ; 0,5 pour résultat.@@$2\times1{,}28=2{,}56\unite s$. \textbf{Barème :} 0,5 pour aller-retour ; 0,5 pour durée.@@En orbite, la station et ses occupants restent attirés par l’astre et sont en chute commune. L’impesanteur ne signifie donc pas une force gravitationnelle nulle. Avec les mêmes masses et une distance centrale doublée, le dénominateur est multiplié par quatre ; F est divisée par quatre. \textbf{Barème scientifique :} 1 point pour explication orbitale ; 1 pour facteur justifié.',[1,1,1,2],[('3.84e8/3e8',1.28),('2*1.28',2.56)])),
S(5,'Entretenir une structure métallique',[2,3,4,5],
P('Comparer des protections',r'Quatre clous identiques sont suivis pendant sept jours. A : air sec, pas de rouille ; B : eau au contact de l’air, rouille ; C : eau salée au contact de l’air, rouille ; D : eau désaérée maintenue sans dioxygène, pas de rouille. Les autres paramètres sont comparables.','b05-corrosion',
r'La corrosion est-elle une transformation physique ou chimique ?@@Quel facteur est testé en comparant B et D ?@@Ces seuls résultats permettent-ils d’affirmer que le sel double la vitesse de corrosion ? Justifier et proposer une mesure supplémentaire.',
r'Chimique : des espèces de la rouille se forment. \textbf{Barème :} 0,5 pour nature ; 0,5 pour formation d’espèces.@@Le rôle du dioxygène disponible, l’eau étant présente dans les deux cas. \textbf{Barème :} 1 point pour facteur.@@Non : « rouille » est qualitatif et ne mesure pas une vitesse. Comparer une quantité de métal corrodé sur des durées identiques, avec répétitions, permettrait d’estimer un effet du sel. \textbf{Barème :} 1 point pour limite ; 1 pour mesure quantitative et conditions.',[1,1,2]),
P('Le fer dans une solution acide',r'La réaction fournie est $\ce{Fe + 2 H+ -> Fe^{2+} + H2}$. Le fer a Z = 26. Après réaction, un test encadré identifie le gaz ; un précipité vert avec la soude identifie Fe2+. Le pH passe de 2 à 4.','',
r'Nommer le gaz produit.@@Déterminer le nombre d’électrons dans Fe2+.@@Le liquide final est-il neutre ? Justifier.@@En quatre à six lignes, relier les observations à la réaction fournie, puis distinguer cette réaction de la corrosion habituelle du fer dans l’air humide.',
r'Dihydrogène, H2. \textbf{Barème :} 1 point.@@$26-2=24$ électrons. \textbf{Barème :} 0,5 pour valeur ; 0,5 pour perte de deux électrons.@@Non : pH 4 est encore acide vers 25 °C. \textbf{Barème :} 0,5 pour réponse ; 0,5 pour critère.@@Le gaz H2 et les ions Fe2+ sont les produits de l’équation. La consommation d’ions H+ est cohérente avec une hausse du pH. La corrosion habituelle dans l’air humide met notamment en jeu eau et dioxygène et forme d’autres composés ; l’équation acide-fer ne la décrit pas à elle seule. \textbf{Barème scientifique :} 1 point pour lien observations-modèle ; 1 pour distinction de situations.',[1,1,1,2],[('26-2',24)])),
S(6,'Mesurer sous l’eau et préserver l’audition',[14,15,17,18],
P('Le sonar d’un bateau',r'Un sonar émet un signal ultrasonore de fréquence 40 kHz. Dans l’eau étudiée, sa vitesse est 1 500 m/s. L’écho provenant du fond revient après 0,080 s. Le fond est supposé horizontal et le trajet vertical.','bb06-sonar',
r'Convertir la fréquence en Hz et la comparer à la limite audible usuelle de 20 000 Hz.@@Quelle distance totale le signal a-t-il parcourue ?@@Calculer la profondeur et justifier le facteur 2.',
r'$40\unite{kHz}=40\,000\unite{Hz}$, au-dessus de la limite usuelle : ultrason. \textbf{Barème :} 0,5 pour conversion ; 0,5 pour comparaison.@@$d_{total}=1\,500\times0{,}080=120\unite m$. \textbf{Barème :} 0,5 pour relation ; 0,5 pour calcul.@@Le signal parcourt l’aller et le retour, donc la profondeur vaut $120/2=60\unite m$. \textbf{Barème :} 1 point pour trajet double ; 1 pour profondeur et unité.',[1,1,2],[('40*1000',40000),('1500*.08',120),('1500*.08/2',60)]),
P('Alimenter et interpréter',r'L’appareil fonctionne en courant continu sous 12 V avec une intensité moyenne supposée constante de 0,50 A. Il est utilisé 20 min. On donne $P=UI$, $E=P\Delta t$. Un son peut être intense même si sa fréquence est élevée ou faible.','',
r'Calculer la puissance reçue.@@Convertir 20 min en secondes.@@Calculer l’énergie reçue en J.@@En quatre à six lignes, expliquer pourquoi la fréquence seule ne mesure pas le risque auditif et citer deux mesures de prévention adaptées à une écoute sonore.',
r'$P=12\times0{,}50=6{,}0\unite W$. \textbf{Barème :} 0,5 pour relation ; 0,5 pour calcul.@@$20\times60=1\,200\unite s$. \textbf{Barème :} 1 point pour conversion.@@$E=6\times1\,200=7\,200\unite J$. \textbf{Barème :} 0,5 pour relation ; 0,5 pour résultat.@@La fréquence caractérise surtout la hauteur et ne donne pas le niveau sonore ni la durée d’exposition. Le risque dépend notamment de ces deux facteurs. Réduire le niveau, s’éloigner de la source et faire des pauses sont des mesures adaptées ; une protection appropriée peut être nécessaire. \textbf{Barème scientifique :} 1 point pour distinction fréquence/niveau/durée ; 0,5 par mesure cohérente, jusqu’à 1 point.',[1,1,1,2],[('12*.5',6),('20*60',1200),('6*1200',7200)])),
S(7,'Recycler et identifier des matériaux',[1,2,3,12],
P('Un morceau de métal',r'Un bloc compact de masse 54,0 g déplace 20,0 mL d’eau quand il est complètement immergé sans bulle. Références à température donnée : aluminium 2,70 ; fer 7,8 ; cuivre 8,9 g/cm³. Un noyau d’aluminium décrit ici contient 13 protons et 14 neutrons.','bb07-metaux',
r'Calculer la masse volumique du bloc.@@Quelle référence est la plus compatible avec le résultat ?@@Donner Z, A et le nombre d’électrons de l’atome neutre décrit.',
r'$\rho=54{,}0/20{,}0=2{,}70\unite{g/cm^3}$. \textbf{Barème :} 0,5 pour quotient ; 0,5 pour unité et valeur.@@L’aluminium ; cette seule propriété ne prouve pas la pureté. \textbf{Barème :} 1 point pour identification compatible.@@$Z=13$, $A=27$ et 13 électrons. \textbf{Barème :} 0,5 pour Z ; 0,5 pour A ; 1 pour nombre d’électrons et neutralité.',[1,1,2],[('54/20',2.7),('13+14',27)]),
P('Refondre ou transformer',r'Un atelier pédagogique étudie un modèle de recyclage. Pour un lot, il reçoit 5,0 MJ d’énergie et en transfère 3,5 MJ utilement à la matière. Le reste est transféré vers l’environnement. La fusion est supposée ne former aucune nouvelle espèce. Les données sont fictives.','',
r'La fusion décrite est-elle une transformation physique ou chimique ?@@Calculer l’énergie transférée vers l’environnement.@@Une masse de 54,0 g fond sans perte ni réaction : quelle masse liquide obtient-on ?@@En quatre à six lignes, expliquer pourquoi « l’énergie perdue » n’est pas détruite et proposer une limite au slogan « recycler ne coûte aucune ressource ».',
r'Physique : changement d’état sans nouvelle espèce. \textbf{Barème :} 0,5 pour nature ; 0,5 pour justification.@@$5{,}0-3{,}5=1{,}5\unite{MJ}$. \textbf{Barème :} 0,5 pour bilan ; 0,5 pour résultat.@@54,0 g, par conservation de la masse dans les conditions données. \textbf{Barème :} 1 point.@@L’énergie transférée vers l’environnement existe encore, notamment sous forme thermique, mais n’est plus utile au procédé. Le recyclage demande aussi énergie, collecte et tri. Il peut réduire certains prélèvements sans supprimer tous les besoins ni toutes les pertes de matière. \textbf{Barème scientifique :} 1 point pour conservation avec périmètre ; 1 pour besoin de ressources expliqué.',[1,1,1,2],[('5-3.5',1.5)])),
S(8,'Produire et économiser l’électricité',[12,13,14,15],
P('Une journée de production',r'Le graphique donne la puissance électrique d’un panneau sur une journée modèle. On l’approxime à 0 W avant 10 h, 200 W de 10 h à 14 h, puis 0 W après 14 h. L’énergie est stockée avec un dispositif dont les pertes sont négligées pour ce premier calcul.','bb08-solaire',
r'Identifier la conversion principale du panneau.@@Lire la durée de production dans le modèle.@@Calculer l’énergie fournie en Wh puis en kWh.',
r'Transfert reçu par rayonnement lumineux, conversion en énergie électrique, avec d’autres sorties notamment thermiques dans la réalité. \textbf{Barème :} 1 point pour entrée et sortie principales.@@4 h. \textbf{Barème :} 1 point pour lecture de 10 h à 14 h.@@$E=200\times4=800\unite{Wh}=0{,}800\unite{kWh}$. \textbf{Barème :} 1 point pour calcul Wh ; 1 pour conversion kWh.',[1,1,2],[('200*4',800),('800/1000',.8)]),
P('Réduire une consommation',r'Ancienne lampe : 40 W ; nouvelle lampe : 8 W pour le même service d’éclairage étudié. Utilisation : 5 h par jour pendant 100 jours. Prix fictif : 0,25 € par kWh. On donne $E=P\Delta t$.','',
r'Calculer la différence de puissance.@@Calculer l’énergie économisée en kWh sur les 100 jours.@@Calculer l’économie monétaire associée.@@En quatre à six lignes, expliquer pourquoi une ressource renouvelable n’assure pas une production constante et proposer un autre critère pour comparer les deux lampes.',
r'$40-8=32\unite W$. \textbf{Barème :} 1 point.@@$E=0{,}032\times5\times100=16\unite{kWh}$. \textbf{Barème :} 0,5 pour unités et durée ; 0,5 pour résultat.@@$16\times0{,}25=4{,}00$ €. \textbf{Barème :} 0,5 pour produit ; 0,5 pour coût.@@La ressource solaire se renouvelle, mais la puissance dépend de l’éclairement, de la météo et de l’heure. Un stockage ou une autre production peut être nécessaire pour certains usages. Durée de vie, qualité de l’éclairage ou impacts de fabrication sont d’autres critères pertinents. \textbf{Barème scientifique :} 1 point pour variabilité expliquée ; 1 pour autre critère cohérent.',[1,1,1,2],[('40-8',32),('.032*5*100',16),('16*.25',4)])),
S(9,'Observer un système planétaire',[7,10,16],
P('Une lumière ancienne',r'Une étoile est située à 4 années-lumière. On fournit $1\unite{al}=9{,}46\times10^{12}\unite{km}$ et $c=3{,}00\times10^5\unite{km/s}$. Dans un schéma, une planète reçoit la lumière de l’étoile et en diffuse une partie vers un observateur.','bb09-etoile',
r'L’année-lumière est-elle une durée ou une distance ?@@Convertir 4 al en km.@@Distinguer étoile et planète comme sources lumineuses et préciser l’ancienneté approximative de la lumière observée de l’étoile.',
r'Une distance. \textbf{Barème :} 1 point.@@$4\times9{,}46\times10^{12}=3{,}784\times10^{13}\unite{km}$. \textbf{Barème :} 0,5 pour produit ; 0,5 pour résultat et unité.@@L’étoile est une source primaire ; la planète est un objet diffusant dans le modèle. La lumière de l’étoile reçue a été émise environ quatre ans auparavant. \textbf{Barème :} 1 point pour distinction ; 1 pour délai.',[1,1,2],[('4*9.46e12',3.784e13)]),
P('Attraction entre deux corps',r'Deux corps sont modélisés par $m_A=1{,}0\times10^{20}\unite{kg}$, $m_B=2{,}0\times10^{10}\unite{kg}$ et $d=1{,}0\times10^6\unite m$. On donne $F=Gm_A m_B/d^2$, avec $G=6{,}67\times10^{-11}$ en SI.','b10-forces',
r'La force gravitationnelle est-elle attractive ou répulsive ?@@Calculer sa valeur.@@Que devient cette valeur si la distance triple à masses inchangées ?@@En quatre à six lignes, expliquer pourquoi les deux corps subissent des forces de même valeur sans que ces forces se compensent sur un seul corps, puis citer une limite du dessin.',
r'Attractive. \textbf{Barème :} 1 point.@@$F=1{,}334\times10^8\unite N$, soit environ $1{,}3\times10^8\unite N$. \textbf{Barème :} 0,5 pour substitution avec d² ; 0,5 pour calcul et unité.@@F est divisée par neuf, soit environ $1{,}48\times10^7\unite N$. \textbf{Barème :} 0,5 pour facteur ; 0,5 pour valeur.@@Les deux forces appartiennent à la même interaction mais s’exercent sur des corps différents. Elles ne sont donc pas deux forces opposées appliquées au même système. Le dessin n’est pas à l’échelle et le modèle assimile les corps à des masses ponctuelles ou sphériques. \textbf{Barème scientifique :} 1 point pour systèmes distincts ; 1 pour limite annoncée.',[1,1,1,2],[('6.67e-11*1e20*2e10/(1e6)**2',1.334e8),('1.334e8/9',14822222.222222222)])),
S(10,'Mener une enquête scientifique',[3,4,8,14,18],
P('Lire une caractéristique',r'Le graphique U(I) provient d’une résistance scolaire. Un point correspond à I = 0,020 A et U = 4,0 V. On fournit $U=RI$ et $P=UI$ en courant continu. La puissance maximale admissible est de 0,25 W.','bb10-ohm',
r'Quel aspect du graphe est compatible avec un conducteur ohmique ?@@Calculer la résistance avec le point fourni.@@Calculer la puissance au point donné et comparer à la limite.',
r'Une droite passant par l’origine, à la dispersion des mesures près. \textbf{Barème :} 0,5 pour droite ; 0,5 pour origine.@@$R=4{,}0/0{,}020=200\unite\Omega$. \textbf{Barème :} 0,5 pour quotient ; 0,5 pour résultat.@@$P=4{,}0\times0{,}020=0{,}080\unite W$, inférieure à 0,25 W. \textbf{Barème :} 1 point pour calcul ; 1 pour comparaison justifiée.',[1,1,2],[('4/.02',200),('4*.02',.08)]),
P('Distinguer les observations',r'Un professeur présente deux transformations : A, eau liquide qui bout ; B, carbonate réagissant avec un acide et dégageant un gaz. Le gaz B trouble l’eau de chaux. Dans les deux cas, des bulles apparaissent. Une pesée de B en système ouvert passe de 120,0 g à 118,9 g sans projection ni autre échange.','',
r'Nommer le changement d’état dans A.@@Identifier le gaz mis en évidence dans B.@@Calculer la masse de gaz qui a quitté B avec les hypothèses données.@@En quatre à six lignes, expliquer pourquoi des bulles ne prouvent pas seules une réaction et proposer un contrôle permettant de renforcer l’interprétation de B.',
r'Vaporisation, ici ébullition. \textbf{Barème :} 1 point.@@Dioxyde de carbone. \textbf{Barème :} 1 point.@@$120{,}0-118{,}9=1{,}1\unite g$. \textbf{Barème :} 0,5 pour bilan ; 0,5 pour masse et unité.@@Les bulles peuvent provenir d’un changement d’état, d’un dégazage ou d’une réaction. Dans B, le test identifie CO2 ; il faut aussi comparer les espèces initiales et finales. Un témoin sans mise en contact des réactifs et un contrôle de l’eau de chaux renforcent l’attribution. \textbf{Barème scientifique :} 1 point pour mécanismes distincts ; 1 pour contrôle pertinent.',[1,1,1,2],[('120-118.9',1.1)])),
]

from revision_brevets import enrichir, CORRIGES, METHODES
enrichir(SUJETS)

def documents():
    from construire import page,box,figure_ex,qs
    s=r'\global\otCorrigesfalse\global\otSouplefalse\gdef\otAccent{otNavy}\pcAnnexe{Dix brevets blancs}{Volets physique-chimie · Série générale · Préparation 2027}\phantomsection\label{brevets}\pdfbookmark[0]{Dix brevets blancs}{bm-brevets}'+'\n'
    s+=box('Un entraînement au volet de physique-chimie','Chaque sujet est prévu pour 30 minutes et noté sur 10 : 9 points scientifiques et 1 point pour la langue. L’épreuve officielle de sciences dure une heure et comporte deux disciplines retenues parmi trois. Les sujets de ce livre préparent uniquement le volet physique-chimie. Ce sont des créations OptiTAB, sans statut de sujet officiel.','method')
    s+=r'''\pcSousTitre{Conditions de travail}
Prévoir une copie, un brouillon et une calculatrice de collège pour ces entraînements. À l’examen, suivre les consignes du sujet reçu. Chercher sans le cours ; réserver trois minutes à la relecture. Les démarches pertinentes, même incomplètes, peuvent rapporter les points de méthode explicités dans les corrigés.
\pcSousTitre{Le point de langue}
Les quatre dimensions sont appréciées sur la copie entière : orthographe, construction des phrases, vocabulaire scientifique et organisation de la réflexion. Pour l’autoévaluation proposée ici, chacune vaut au plus 0,25 point. Le barème scientifique est séparé. Il ne s’agit pas d’une grille ministérielle imposant cette subdivision.
\pcSousTitre{Parcours conseillé}
Sujets 1 à 3 : commencer après les chapitres correspondants. Sujets 4 à 7 : croiser les thèmes. Sujets 8 à 10 : composer en temps limité sans aide. Tous les documents et nombres d’étude sont originaux ou explicitement annoncés comme références du cours.
'''
    for x in SUJETS:s+=rf'\pcRepere{{bb-{x.numero}}}{{Sujet {x.numero:02} · {x.titre}}}'+'\n'
    for x in SUJETS:
        qnum=0
        for k,part in enumerate(x.parties,1):
            s+=page(f'Brevet blanc {x.numero:02}',x.titre,f'bb-{x.numero}' if k==1 else '')
            if k==1:s+=rf'\pdfbookmark[1]{{{x.numero:02} · {x.titre}}}{{bm-bb-{x.numero}}}'+'\n'
            s+=rf'\noindent\textbf{{Volet PC · 30 min · /10}}\hfill Partie {k}/2 · {sum(part.points)} points scientifiques'+'\n'
            s+=r'\par\vspace{2mm}Les essais et démarches sont pris en compte. Répondre sur une copie séparée.\par'+'\n'
            s+=box(part.titre,part.exercice.document)+figure_ex(part.exercice.figure,part.exercice.legende_figure)
            for q,pt in zip(part.exercice.questions,part.points):
                qnum+=1
                s+=rf'\par\addvspace{{3mm}}\noindent\textbf{{Question {qnum} · {pt} point'+('s' if pt>1 else '')+r'}\quad '+q+r'\par'+'\n'
            s+=r'\vfill'+rf'\pcRepere{{cor-bb-{x.numero}}}{{Corrigé, barème et remédiation}}'+'\n'
            if k==2:s+=r'{\small 1 point de langue sur l’ensemble de la copie : voir la grille d’autoévaluation.}'+'\n'
    s+=r'\global\otCorrigestrue\global\otSoupletrue\gdef\otAccent{otGreenDark}\pcAnnexe{Corrigés des brevets blancs}{Des points de méthode, des réponses et des critères de réussite}\phantomsection\label{cor-brevets}\pdfbookmark[0]{Corrigés des brevets blancs}{bm-cor-brevets}'+'\n'
    s+=box('Se corriger sans masquer ses erreurs','Attribuer les points à partir des critères. Conserver une démarche pertinente même si une erreur de calcul se propage ; éviter de retirer deux fois les mêmes points pour une même erreur. La proposition de correction décrit une répartition pédagogique, pas un barème d’examen.','method')
    s+=r'''\pcSousTitre{Attribuer le point de langue}
Pour chacune des quatre dimensions, attribuer 0 si la compréhension est très gênée ou le critère absent, 0,125 si la maîtrise reste fragile et 0,25 si elle est satisfaisante. Une copie courte correcte n’a pas à devenir artificiellement longue. Prendre en compte les réponses de toute la copie, particulièrement la dernière question rédigée.
\pcSousTitre{Reprendre après le bilan}
Choisir une erreur de connaissance, de modèle ou de conversion. Relire la partie de cours indiquée, refaire un exercice puis reprendre la question du sujet blanc quelques jours plus tard. Une note totale renseigne moins bien qu’une liste précise des points à retravailler.
'''
    for x in SUJETS:
        qnum=0
        for k,part in enumerate(x.parties,1):
            s+=page(f'Corrigé du sujet {x.numero:02}',part.titre,f'cor-bb-{x.numero}' if k==1 else '')
            s+=rf'\pcRepere{{bb-{x.numero}}}{{Revenir à l’énoncé}}'+'\n'
            for a,pt in zip(part.exercice.reponses,part.points):
                qnum+=1
                s+=r'\par\noindent\begin{minipage}{\linewidth}\pcSousTitre{'+f'Question {qnum} · {pt} point'+('s' if pt>1 else '')+'}\n'+a+r'\par'+'\n'
                s+=r'\smallskip\noindent\textbf{Démarche.}\enspace '+METHODES[x.numero,qnum]+r'\par'+'\n'
                if qnum in CORRIGES.get(x.numero,{}):s+=figure_ex(*CORRIGES[x.numero][qnum])
                s+=r'\end{minipage}\par'+'\n'
            if k==1:
                s+=r'\par\noindent\begin{minipage}{\linewidth}'+'\n'
                s+=box('Ma grille de bilan après les sept questions',r'Partie 1 : /4 ; partie 2 : /5 ; langue : /1. Total : /10. Après la correction du sujet entier, noter une réussite et une priorité de travail.','method')
                refs=[rf'\hyperref[chap-{n}]{{chapitre {n} (p.~\pageref*{{chap-{n}}})}}' for n in x.chapitres]
                s+=r'{\small\textbf{Pour reprendre le cours : }'+r' ; '.join(refs)+r'.\par}\end{minipage}\par'+'\n'
    return s
