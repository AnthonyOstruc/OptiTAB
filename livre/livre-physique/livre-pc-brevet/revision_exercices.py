"""Révision scientifique et iconographique des 288 entraînements du cycle 4."""
import json
from pathlib import Path

HERITAGE=json.loads((Path(__file__).parent/'revision_heritage.json').read_text(encoding='utf8'))
ILLUSTRATIONS=HERITAGE['illustrations']
METHODES=HERITAGE['methodes']

def I(ids,enonce='',corrige='',legende='',solution='',exact=False,exact_correction=False):
    for ident in ids.split():
        assert ident not in ILLUSTRATIONS,ident
        ILLUSTRATIONS[ident]=dict(figure=enonce,figure_correction=corrige,legende_figure=legende,legende_correction=solution,figure_exacte=exact,correction_exacte=exact_correction)

I('1.6',enonce='rev-ex-immersion',corrige='rev-cor-immersion',solution='Le solide déplace 15 mL ; on utilise ce volume avec la seule masse du solide.')
I('1.8',corrige='cor-coque',solution='Une cavité contribue au volume extérieur, mais pas au volume de cuivre.')
I('1.10',enonce='rev-ex-ebullition',corrige='rev-cor-ebullition',legende='Courbe illustrant le palier de trois minutes décrit dans la question.',solution='La température reste constante pendant le changement d’état, à la pression annoncée.')
I('1.11',corrige='rev-cor-separation',solution='Filtration pour retirer le sable ; distillation du filtrat pour recueillir l’eau et laisser le sel non volatil.')
I('1.12',corrige='cor-bulle',solution='Une bulle fait attribuer au solide un volume trop grand et une masse volumique trop petite.')
I('1.13',corrige='rev-cor-intervalle',solution='2,70 appartient à l’intervalle 2,63 à 2,73 g/cm³ ; compatibilité ne signifie pas identification certaine.')
I('1.14',corrige='cor-glaces',solution='Distinguer apport d’eau par les glaciers continentaux et dilatation de l’eau ; la banquise flottait déjà.')
I('D1',corrige='rev-cor-tare',solution='Soustraire la masse du flacon avant de former le quotient masse/volume.')
for ident,key in [('2.3','na'),('2.6','cu'),('2.7','cl'),('2.8','al'),('2.11','mg'),('2.15','isotopes'),('D2','fe3')]:
    I(ident,corrige='rev-cor-atome-'+key,solution='Inventaire des constituants ; représentation symbolique sans échelle de taille ni orbites électroniques.')
I('2.4',corrige='rev-cor-trois-eaux',solution='Le coefficient multiplie la molécule entière : trois molécules contiennent six H et trois O.')
I('2.5',corrige='rev-cor-ions',solution='Perdre un électron donne une charge positive ; en gagner un donne une charge négative. Le noyau reste inchangé.')
I('2.9',corrige='rev-cor-coefficients',solution='Compter chaque type d’atome en multipliant coefficient et indice.')
I('2.10',corrige='rev-cor-oxygene',solution='Atome, molécule et ion sont trois entités différentes ; la charge ne se lit pas comme un nombre d’atomes.')
I('2.13',corrige='rev-cor-echelles-atome',solution='Deux zooms séparés : le diamètre du noyau est environ cent mille fois plus petit que celui de l’atome.')
I('2.14',corrige='rev-cor-neutralite',solution='Additionner les charges de tous les ions ; conserver les signes et les coefficients.')
I('3.4 3.9 6.15',corrige='cor-reaction-eau',solution='Les coefficients rétablissent la conservation des atomes ; les formules des espèces restent inchangées.')
I('3.6',corrige='rev-cor-masse-gaz',solution='Le système pesé est ouvert : la différence correspond au gaz sorti avec les hypothèses données.')
I('3.7',corrige='rev-cor-masse-carbone',solution='Les deux réactifs consommés contribuent à la masse de dioxyde de carbone.')
I('3.8',corrige='rev-cor-ethanol',solution='Inventaire atomique de chaque côté ; l’oxygène de l’éthanol fait aussi partie du bilan.')
I('3.10',corrige='rev-cor-reactif-restant',solution='Ne pas confondre masse des produits formés et masse finale totale avec le réactif restant.')
I('3.11',corrige='rev-cor-temoin',solution='Le changement du témoin empêche d’attribuer avec certitude le résultat au gaz étudié.')
I('3.13',corrige='rev-cor-masse-fer',solution='L’augmentation de masse vient de matière du milieu incorporée dans le produit.')
I('D3',corrige='rev-cor-masse-methane',solution='Bilan complet du modèle : réactifs consommés, produits et dioxygène restant.')
I('4.4',corrige='rev-cor-ions-filtre',solution='Un filtre ordinaire retient les grains, pas les ions dissous de cette solution.')
I('4.5 4.9 4.15',corrige='rev-cor-tests-ions',solution='Prélèvements séparés : chaque réactif sert à une recherche précise ; ne pas cumuler les réactifs dans le même tube.')
I('4.6 5.7',corrige='rev-cor-ph-acide',solution='Le pH augmente de 2 à 4, mais reste inférieur à 7 ; la solution est encore acide.')
I('4.7',corrige='rev-cor-ph-base',solution='Le pH baisse de 12 à 10, mais reste supérieur à 7 ; la solution est encore basique.')
I('4.8',corrige='rev-cor-ph-classement',solution='Classer par comparaison à 7, à température usuelle.')
I('4.14',corrige='rev-cor-ph-ocean',solution='Le pH diminue de 8,2 à 8,0 : acidification, tout en restant dans le domaine basique.')
I('D4',corrige='rev-cor-ph-solutions',solution='A, de pH 3, est acide ; B, de pH 10, est basique. Les tests se font sur des prélèvements séparés.')
I('4.10',corrige='rev-cor-acide-base',solution='Une unité H⁺ réagit avec une unité HO⁻ dans ce modèle ; un éventuel excès reste dans la solution.')
I('4.12',corrige='rev-cor-conduction',solution='Dans la solution, des ions des deux signes se déplacent ; ce ne sont pas des électrons libres qui traversent la solution comme dans le métal.')
I('5.2 5.6',corrige='rev-cor-zinc',solution='Deux H⁺ compensent la charge de Zn²⁺ ; les atomes et la charge totale sont conservés.')
I('5.4 D5',corrige='rev-cor-protection',solution='Une peinture protège en limitant le contact ; une rayure peut laisser agir le milieu sur le métal exposé.')
I('5.9 5.10',corrige='rev-cor-corrosion',solution='Comparer des conditions contrôlées, avec des clous comparables et une même durée ; ne changer qu’un facteur dans la comparaison retenue.')
I('5.11',corrige='rev-cor-masse-corrosion',solution='Une masse de matière issue du milieu s’ajoute au métal pour former les produits.')
I('8.10',corrige='rev-cor-pixels',solution='Convertir le déplacement de l’image en distance réelle avant de diviser par la durée.')
I('8.12',corrige='rev-cor-bus',solution='Pour la vitesse moyenne sur le trajet complet, l’arrêt fait partie de la durée totale.')
I('D8',corrige='rev-cor-trajets',solution='Inclure les trois minutes d’arrêt dans la durée du trajet B ; les deux arrivées sont simultanées dans ce modèle.')
I('9.4',corrige='rev-cor-poids',solution='Le poids est appliqué au centre de gravité dans ce modèle, de direction verticale et de sens vers le bas.')
I('9.8',corrige='rev-cor-poids-lune',solution='La masse reste 60 kg ; les deux poids sont comparés avec la même échelle graphique qualitative.')
I('9.9',corrige='rev-cor-force-echelle',solution='Flèches de 3 cm et 2,5 cm à l’impression à 100 % ; 1 cm représente 4 N.',exact_correction=True)
I('9.10 9.13',corrige='cor-livre-forces',solution='Ne représenter que les forces appliquées au livre ; l’action du livre sur la table concerne un autre système.')
I('9.11',enonce='rev-ex-poids-graphe',corrige='rev-cor-poids-graphe',solution='Les deux mesures sont compatibles avec P = 10 m ; l’origine est une prévision du modèle, pas une mesure ajoutée.')
I('9.14',corrige='cor-manege',solution='La direction de la vitesse change dans le mouvement circulaire uniforme ; cela n’impose pas un changement de sa valeur.')
I('9.15',corrige='rev-cor-forces-5N',solution='Ces deux forces opposées agissent sur le même système ; leurs valeurs sont égales.')
I('D9',corrige='rev-cor-caisse',solution='Deux flèches de 3,92 cm à l’impression à 100 % ; même système et échelle 1 cm pour 10 N.',exact_correction=True)
I('10.2 10.12',corrige='rev-cor-gravitation',solution='Deux flèches opposées, appliquées à deux corps différents ; elles ne se compensent pas sur le seul corps A.')
I('10.4',corrige='rev-cor-centres',solution='La distance d de la loi gravitationnelle est mesurée entre les centres, pas entre les surfaces.')
I('10.6 10.8',corrige='rev-cor-inverse-carre',solution='Le facteur de distance est mis au carré au dénominateur ; à trois fois la distance, la force est divisée par neuf.')
I('10.9',corrige='rev-cor-altitude',solution='Additionner rayon et altitude avant de convertir en mètres ; le point de départ est le centre de la Terre.')
I('10.13',corrige='rev-cor-orbite',solution='Le satellite et son contenu sont en chute commune ; l’impesanteur ne signifie pas absence de gravitation.')
I('D10',corrige='rev-cor-satellite',solution='Distances entre centres et masses en unités SI ; la force diminue lorsque la distance augmente.')
I('11.5 11.6 11.10 11.11 D11',corrige='rev-cor-ec-facteurs',solution='Courbe de rapports à masse constante : le facteur appliqué à la vitesse est mis au carré pour l’énergie cinétique.')
I('11.8',corrige='rev-cor-freinage',solution='L’écart de 2 250 J ne disparaît pas : il est transféré ou converti, notamment par les frottements.')
I('11.9',corrige='rev-cor-chute',solution='Dans le modèle sans frottements, l’énergie mécanique reste 40 J ; les deux formes se redistribuent.')
I('11.14',corrige='rev-cor-chute-reelle',solution='Le bilan mécanique diminue de 15 J ; le bilan total inclut l’énergie transférée au milieu.')
I('11.15',corrige='rev-cor-vehicules',solution='Comparer des résultats dans le même référentiel, après avoir pris le carré des vitesses.')
I('13.1',corrige='rev-cor-mesures',solution='L’ampèremètre est traversé par le courant de la branche ; le voltmètre est relié aux deux bornes du récepteur.')
I('13.3',corrige='rev-cor-serie-018',solution='En régime permanent, la lampe ne consomme pas le courant ; l’intensité est la même avant et après.')
I('13.4',enonce='ex-circuit-parallele',corrige='rev-cor-parallele-12',solution='Deux branches reliées aux mêmes deux nœuds ont la même tension avec la même convention de mesure.')
I('13.5',enonce='rev-ex-noeud-035',corrige='rev-cor-noeud-035',solution='Somme des intensités entrantes égale à la somme des intensités sortantes.')
I('13.6',enonce='rev-ex-noeud-080',corrige='rev-cor-noeud-080',solution='250 mA = 0,250 A ; le courant de la branche inconnue est 0,550 A.')
I('13.7',corrige='rev-cor-serie-9V',solution='Le voltmètre mesure la tension du second récepteur en dérivation ; 3,5 + 5,5 = 9 V.')
I('13.8',corrige='rev-cor-resistances-12',solution='La tension commune ne force pas les intensités à être égales si les résistances diffèrent.')
I('13.9',corrige='cor-voltmetre-inverse',solution='Inverser les bornes de mesure inverse le signe affiché, sans imposer un courant nul dans le récepteur.')
I('13.10',corrige='cor-commandes-independantes',solution='Chaque interrupteur se place en série avec sa lampe dans sa propre branche.')
I('13.12',enonce='rev-ex-noeud-090',corrige='rev-cor-noeud-090',solution='0,90 − 0,20 − 0,35 = 0,35 A ; contrôler la somme des trois sorties.')
I('13.13',corrige='cor-branche-ouverte',solution='L’autre branche conserve un trajet fermé ; une tension exactement inchangée suppose la source idéale du modèle.')
I('13.14',enonce='ex-lampe-court-circuitee',corrige='cor-lampe-court-circuitee',legende='Défaut à analyser sur le schéma, sans le réaliser.',solution='Le fil contourne le récepteur ; couper l’alimentation avant toute modification.')
I('13.15',corrige='rev-cor-eclairage-6V',solution='Les deux lampes reçoivent chacune 6 V et les intensités de branches s’ajoutent au générateur.')
I('D13',enonce='rev-ex-montage-9V',corrige='rev-cor-montage-9V',solution='Une branche contient deux lampes en série ; A se place dans cette branche, V aux bornes de la résistance.')
I('14.8',enonce='rev-ex-ohm-100',corrige='rev-cor-ohm-100',solution='Le quotient U/I vaut 100 ohms pour chacun des trois points ; le modèle est une droite passant par l’origine.')
I('14.12',corrige='rev-cor-lampe-reelle',solution='Exemple de points illustrant les quotients 20 et 35 ohms donnés ; ce ne sont pas de nouvelles mesures de l’énoncé.')
I('14.13',enonce='rev-ex-ohm-inverse',corrige='rev-cor-ohm-inverse',legende='Exemple avec la tension en abscisse et l’intensité en ordonnée.',solution='Dans ces axes, la pente est I/U ; on retrouve R en prenant le quotient inverse U/I.')
I('14.14',corrige='rev-cor-resistances-6',solution='Même tension de 6 V, courants de 60 mA et 30 mA ; la puissance totale vaut 6 × 0,090 = 0,54 W.')
I('D14',corrige='rev-cor-montage-ohm',solution='Mesurer U aux bornes de R et I en série ; le modèle retenu est ici 220 ohms sous 6 V.')

METHODES.update({
'1.6':r'$V=43-28=15\unite{mL}=15\unite{cm^3}$. On calcule ensuite $\rho=40{,}5/15=2{,}70\unite{g/cm^3}$. Utiliser 43 mL compterait aussi l’eau initiale.',
'1.8':r'Partir de $m=\rho V$ et isoler $V=m/\rho=178/8{,}9=20\unite{cm^3}$. Le volume extérieur d’un objet creux ne se substitue pas au volume du matériau.',
'1.12':r'Avec le volume apparent, $54/25=2{,}16\unite{g/cm^3}$. Avec le volume réel de 20 cm³, on aurait $54/20=2{,}70\unite{g/cm^3}$. Une mesure biaisée peut donc changer l’identification proposée.',
'D1':r'La masse du liquide vaut $109-45=64\unite g$. Avec 80 mL, $\rho=64/80=0{,}80\unite{g/mL}$. La proximité avec 0,79 g/mL rend l’éthanol compatible ; d’autres liquides ou mélanges peuvent avoir une valeur proche.',
'2.3':r'Le numéro atomique compte les protons : $Z=11$. Le nombre de nucléons est $A=11+12=23$. Un atome neutre possède autant d’électrons que de protons.',
'2.6':r'Le noyau de cuivre conserve ses 29 protons. La charge $2+$ signifie deux électrons de moins que l’atome neutre : $29-2=27$. Ne pas retrancher des protons.',
'2.8':r'$N=A-Z=27-13=14$ neutrons. L’atome neutre possède 13 électrons ; l’ion $\ce{Al^3+}$ en a $13-3=10$.',
'2.11':r'La charge en unités élémentaires vaut $12-10=+2$ ; avec $Z=12$, il s’agit de $\ce{Mg^2+}$. Le signe vient du déficit d’électrons.',
'2.13':r'$10^{-10}/10^{-15}=10^5$. Si l’atome mesure 10 m dans une maquette, le noyau mesurerait $10/10^5=10^{-4}\unite m=0{,}1\unite{mm}$.',
'2.14':r'Chaque ion chlorure porte la charge $-1$. Deux ions calcium portent ensemble $2\times(+2)=+4$ : il faut donc quatre ions chlorure pour obtenir $+4-4=0$.',
'D2':r'$Z=26$, $A=26+30=56$. La charge vaut $26-23=+3$, donc $\ce{Fe^3+}$ ; les neutrons ne contribuent pas à cette charge.',
'3.8':r'À gauche : C = 2, H = 6 et O = $1+3\times2=7$. À droite : C = $2\times1=2$, H = $3\times2=6$ et O = $2\times2+3=7$. Les nombres d’atomes sont égaux pour chaque élément.',
'3.10':r'La masse initiale totale vaut $10+25=35\unite g$. S’il reste 5 g de réactif, les produits formés représentent $35-5=30\unite g$ ; la masse finale totale reste 35 g.',
'D3':r'La masse initiale est $8+40=48\unite g$. La masse finale est $22+18+8=48\unite g$. Les 8 g de dioxygène restant doivent figurer dans le bilan ; ils ne font pas partie des produits formés.',
'4.15':r'Prélever deux portions de solution dans deux tubes propres. Ajouter quelques gouttes de nitrate d’argent au premier pour rechercher les chlorures ; utiliser la soude dans l’autre pour rechercher notamment les ions cuivre(II). Comparer avec un témoin adapté et conclure dans les limites du test.',
'5.10':r'Choisir deux clous comparables, même volume d’eau, même accès à l’air, même température et même durée. Ne faire varier que la salinité. Comparer ensuite le même indicateur de corrosion ; une expérience isolée ne quantifie pas toutes les situations réelles.',
'8.10':r'La calibration donne $1/200=0{,}005\unite m$ par pixel. Donc $d=80\times0{,}005=0{,}40\unite m$, puis $v=0{,}40/0{,}20=2{,}0\unite{m/s}$.',
'8.11':r'Additionner d’abord les distances et les durées : $d=120\unite{km}$, $\Delta t=3\unite h$, donc $v_{\rm moy}=40\unite{km/h}$. La moyenne arithmétique des deux vitesses ne convient pas lorsque les durées diffèrent.',
'8.12':r'Le trajet complet dure $20+10=30\unite{min}=0{,}50\unite h$. La distance reste 12 km : $v_{\rm moy}=12/0{,}50=24\unite{km/h}$.',
'9.6':r'Convertir d’abord : $150\unite g=0{,}150\unite{kg}$. Ensuite $P=mg=0{,}150\times9{,}8=1{,}47\unite N$, soit environ 1,5 N.',
'9.8':r'$P_{\rm Terre}=60\times10=600\unite N$ et $P_{\rm Lune}=60\times1{,}6=96\unite N$. Le poids est multiplié par $1{,}6/10=0{,}16$ ; la masse ne change pas.',
'9.9':r'Une longueur se calcule en divisant la force par le nombre de newtons représentés par un centimètre : $12/4=3\unite{cm}$. Inversement, $2{,}5\times4=10\unite N$.',
'D9':r'$P=4\times9{,}8=39{,}2\unite N$. À l’équilibre dans le modèle à deux forces, la force du fil a aussi cette valeur. Chaque flèche mesure $39{,}2/10=3{,}92\unite{cm}$. Les deux flèches s’appliquent à la caisse.',
'10.9':r'$d=R+h=6\,400+400=6\,800\unite{km}=6{,}8\times10^6\unite m$. Employer seulement l’altitude ferait partir la mesure de la surface et non du centre.',
'10.11':r'Le facteur de masse est 2, celui du carré de la distance est $2^2=4$ ; le facteur total est donc $2/4=0{,}5$. Traiter séparément les modifications avant de les combiner.',
'D10':r'$F=6{,}67\times10^{-11}\times(6{,}0\times10^{24})\times500/(7{,}0\times10^6)^2\approx4{,}1\times10^3\unite N$. Doubler la distance divise par quatre : environ $1{,}0\times10^3\unite N$.',
'11.7':r'$54\unite{km/h}=54/3{,}6=15\unite{m/s}$. Alors $E_c=\frac12\times1\,000\times15^2=112\,500\unite J=112{,}5\unite{kJ}$. Mettre 54 au carré sans conversion donnerait une valeur fausse.',
'11.8':r'$E_{c,i}=\frac12\times60\times10^2=3\,000\unite J$, puis $E_{c,f}=\frac12\times60\times5^2=750\unite J$. L’écart est $3\,000-750=2\,250\unite J$.',
'11.11':r'Une hausse de 20 % donne le facteur de vitesse $1+20/100=1{,}2$. Le facteur d’énergie est $1{,}2^2=1{,}44$ : la hausse d’énergie vaut donc $(1{,}44-1)\times100=44\,\%$.',
'11.15':r'A : $\frac12\times800\times20^2=160\,000\unite J$. B : $\frac12\times1\,600\times10^2=80\,000\unite J$. Le rapport A/B vaut 2 : la masse seule ne suffit pas à comparer.',
'D11':r'Conserver les valeurs non arrondies de $50/3{,}6$ et $100/3{,}6$ jusqu’au calcul final. Le rapport des vitesses est exactement 2, donc celui des énergies exactement 4 dans le modèle, même si les résultats affichés sont arrondis.',
'13.6':r'La loi des nœuds donne $I_G=I_1+I_2$. Avec $I_1=0{,}250\unite A$, $I_2=0{,}80-0{,}250=0{,}550\unite A=550\unite{mA}$.',
'13.7':r'Les tensions des récepteurs en série s’ajoutent : $U_2=U_G-U_1=9-3{,}5=5{,}5\unite V$. Le voltmètre se connecte aux deux bornes de ce second récepteur.',
'D13':r'Contrôler séparément chaque branche : $4+5=9\unite V$ pour les lampes et 9 V pour la résistance. Convertir les courants avant la somme : $0{,}150+0{,}060=0{,}210\unite A$.',
'14.8':r'Former $1/0{,}01$, $2/0{,}02$ et $3/0{,}03$ : on obtient chaque fois 100 ohms. Le contrôle graphique porte aussi sur l’origine ; trois quotients cohérents ne valident pas des conditions jamais testées.',
'14.9':r'$I=U/R=10/100=0{,}10\unite A$, puis $P=UI=1{,}0\unite W$. Comparer dans la même unité : $1{,}0/0{,}25=4$, donc la limite est dépassée.',
'14.13':r'La pente se forme comme ordonnée/abscisse. Si I est vertical et U horizontal, elle vaut I/U en A/V. La résistance reste U/I en V/A, c’est-à-dire en ohms.',
'14.14':r'$I_1=6/100=0{,}060\unite A$, $I_2=6/200=0{,}030\unite A$. Le générateur fournit $I_G=0{,}090\unite A$, donc $P_G=UI_G=0{,}54\unite W$.',
'D14':r'Pour chaque résistance, appliquer $I=U/R$ puis $P=UI$. Sous 6 V : $P_{100}=0{,}36\unite W>0{,}25\unite W$ ; $P_{220}\approx0{,}164\unite W<0{,}25\unite W$. Le contrôle de puissance précède la réalisation.',
'15.7':r'Choisir la paire d’unités avant le produit : $30\unite{min}=0{,}5\unite h$ donne $60\times0{,}5=30\unite{Wh}$. En secondes, $30\unite{min}=1\,800\unite s$ donne $60\times1\,800=108\,000\unite J$. Les deux écritures sont cohérentes car 1 Wh = 3 600 J.',
'D15':r'La durée d’usage vaut $4\times20=80\unite h$. Additionner les dix lampes : $P_A=120\unite W$, $P_B=80\unite W$. L’écart de 40 W sur 80 h donne $3\,200\unite{Wh}=3{,}2\unite{kWh}$ ; multiplier ensuite par le prix d’un kWh.',
})

def enrichir(chs):
    for c in chs:
        for j,ex in enumerate(c.exercices+[c.defi],1):
            ident=f'{c.numero}.{j}' if j<=15 else f'D{c.numero}'
            for key,val in ILLUSTRATIONS.get(ident,{}).items():setattr(ex,key,val)
            ex.methode=METHODES.get(ident,'')
            if ident=='2.14':ex.reponses[1]=r'Quatre ions chlorure : $2\times2-4=0$.'
            if ident=='D9':ex.questions[1]=r'Tracer les forces qui s’appliquent à la caisse, à l’échelle 1 cm pour 10 N.'
