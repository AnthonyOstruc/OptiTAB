"""Figures originales vectorielles, échelles explicites, variantes de correction."""
from structure import write
import math
F={}
def tik(body,caption='Schéma de principe, sans échelle.'):
    return r'''\begin{tikzpicture}[font=\fontsize{8.5}{10.5}\selectfont,
 line width=.7pt,>=Stealth, every node/.style={align=center},
 fleche/.style={->,line width=1pt,otGreenDark},
 guide/.style={otMuted,dashed,line width=.5pt},
 lab/.style={fill=white,inner sep=1.5pt,text=otInk},
 rayon/.style={thick,postaction={decorate},decoration={markings,
 mark=at position .35 with {\arrow{Stealth}},
 mark=at position .75 with {\arrow{Stealth}}}}]
'''+body+'\n\\end{tikzpicture}\\par\\smallskip\\legende{'+caption+'}\n'
def graph(body,opts='',caption='Données construites pour l’entraînement.'):
    return r'\begin{tikzpicture}\begin{axis}[otMesures,'+opts+']\n'+body+r'\end{axis}\end{tikzpicture}\par\smallskip\legende{'+caption+'}'

F['histogramme']=graph(r'''\addplot[ybar,bar width=6pt,fill=otNavy!65,draw=otNavy] coordinates {(9.8,0)(9.9,2)(10,6)(10.1,2)(10.2,0)};
\addplot[ybar,bar width=6pt,bar shift=7pt,fill=otGreen!55,draw=otGreenDark] coordinates {(9.8,2)(9.9,2)(10,2)(10.1,2)(10.2,2)};
\legend{Série A,Série B}''',r'xlabel={Volume (mL)},ylabel={Effectif},xmin=9.72,xmax=10.28,ymin=0,ymax=7,xtick={9.8,9.9,10,10.1,10.2},ytick={0,2,4,6},legend style={at={(.5,1.03)},anchor=south,legend columns=2,font=\small},height=5cm',
'Classes contiguës de largeur 0,1 mL, repérées par leur centre ; barres décalées pour comparer A et B.')

F['densite']=tik(r'''\draw[otNavy] (0,0)--(0,3.5) (1.2,0)--(1.2,3.5) (0,0)--(1.2,0);
\fill[otNavy!12] (.02,.02) rectangle (1.18,2.5);\draw[otNavy] (0,2.5)--(1.2,2.5);
\foreach \y in {.5,1,1.5,2,2.5,3}{\draw (.9,\y)--(1.2,\y);}
\draw[guide] (1.3,2.5)--(3,2.5);\node[anchor=west] at (3,2.5){Volume prélevé\parbox{1mm}{}};
\node[anchor=west] at (3,1.7){Pesée vide : 42,6 g};\node[anchor=west] at (3,1){Pesée remplie : 58,4 g};
\node at (.6,-.4){20,0 mL};
\solution{\node[text=otGreenDark,anchor=west] at (3,.2){$m=15,8$ g ; $\rho=0,790$ g/mL};}''')

def ccm(synth=False):
    labels=['N','R','S'] if synth else ['R','S','M']
    points=[[(.6,2.6)],[(1.8,1.3)],[(3,2.6),(3,1.3)]] if synth else [[(.6,2.6)],[(1.8,1.3)],[(3,2.6),(3,1.3)]]
    b=r'''\fill[otNavyTint] (-.3,-.3) rectangle (3.9,4.2);
\draw[otNavy] (0,0) rectangle (3.6,3.8);\draw[guide] (0,.5)--(3.6,.5);\draw[otNavy,dashed] (0,3.4)--(3.6,3.4);
\node[anchor=west] at (4,3.4){Front de l’éluant};\node[anchor=west] at (4,.5){Ligne de dépôt};
\draw[->,otMuted] (4.9,1.1)--(4.9,2.7);\node[anchor=west] at (5.1,1.9){Migration};
'''
    for lab,x,ps in zip(labels,[.6,1.8,3],points):
        b+=f'\\node at ({x},-.35){{{lab}}};\\fill[otMuted] ({x},.5) circle (.03);\n'
        for xx,yy in ps:b+=f'\\fill[otNavy!70] ({xx},{yy}) ellipse (.13 and .07);\n'
    b+=r'\solution{\draw[otGreenDark,dashed] (.35,2.6)--(3.3,2.6);\draw[otGreenDark,dashed] (1.55,1.3)--(3.3,1.3);}'
    return tik(b,'CCM après développement ; pistes comparées sur une même plaque, sans échelle.')
F['ccm-identification']=ccm();F['ccm-synthese']=ccm(True)

F['dissolution']=tik(r'''\foreach \x/\t in {0/Peser,3/Dissoudre,6/Transférer,9/Ajuster}{
\node[draw=otRule,rounded corners=2mm,minimum width=2.5cm,minimum height=1cm,fill=otNavyTint] at (\x,1){\t};}
\foreach \x in {1.4,4.4,7.4}{\draw[fleche] (\x,1)--++(.9,0);}
\node[text width=2.5cm] at (0,-.1){Coupelle et balance};\node[text width=2.5cm] at (3,-.1){Un peu d’eau\\puis agitation};
\node[text width=2.5cm] at (6,-.1){Fiole jaugée\\et rinçages};\node[text width=2.5cm] at (9,-.1){Trait de jauge\\puis homogénéiser};
''')
# Fiole et pipette : aucune échelle dimensionnelle de la verrerie.
F['dilution']=tik(r'''\draw[otNavy] (0,0)--(0,2)--(.8,2)--(.8,0)--cycle;
\fill[otNavy!20] (.02,.02) rectangle (.78,1.5);\node[text width=2.6cm] at (.4,-.6){Solution mère\\40,0 g/L};
\draw[otNavy] (3,0)--(3,1) (3.12,0)--(3.12,1);\draw[otNavy] (3.06,1.4) ellipse (.22 and .4);
\draw[otNavy] (3,.2)--(3,1) (3.12,.2)--(3.12,1) (3,1.8)--(3,3) (3.12,1.8)--(3.12,3);
\draw[otGreenDark] (2.8,2.4)--(3.3,2.4);\node at (3.05,3.4){Pipette 10,0 mL};
\path[fill=otNavy!15] (6.4,2.5)--(6.4,1.8)..controls(5.4,1.2)and(5.65,0)..(6.55,0)..controls(7.45,0)and(7.7,1.2)..(6.7,1.8)--(6.7,2.5)--cycle;
\draw[otNavy] (6.4,3)--(6.4,1.8)..controls(5.4,1.2)and(5.65,0)..(6.55,0)..controls(7.45,0)and(7.7,1.2)..(6.7,1.8)--(6.7,3);
\draw[otGreenDark] (6.2,2.5)--(6.9,2.5);
\node[text width=3cm] at (6.55,-.6){Fiole 100,0 mL\\complétée avec de l’eau};
\draw[fleche] (1.2,1.3)--(2.3,1.3);\draw[fleche] (3.6,1.3)--(5.3,1.3);
\solution{\node[text=otGreenDark] at (4.4,4.1){$F=10$ ; $c_f=4,00$ g/L};}''')

F['etalonnage']=graph(r'''\addplot[only marks,otNavy,mark=*] coordinates {(0,1)(20,1.01)(40,1.02)(60,1.03)(80,1.04)(100,1.05)};
\addplot[otNavy,domain=0:100]{1+.0005*x};
\solution{\addplot[otGreenDark,dashed,thick] coordinates {(0,1.03)(60,1.03)(60,1)};\addplot[only marks,otGreenDark] coordinates {(60,1.03)};}''',
r'xlabel={$c_m$ (g/L)},ylabel={$\rho$ (g/mL)},xmin=0,xmax=100,ymin=1,ymax=1.055,xtick={0,20,...,100},ytick={1,1.01,1.02,1.03,1.04,1.05},scaled y ticks=false')

F['atome']=tik(r'''\draw[otNavy,dashed] (0,0) circle (1.4);\fill[otGreen!30] (0,0) circle (.25);\node at (0,0){$+$};
\foreach \a in {30,150,270}{\fill[otNavy] (\a:1.4) circle (.07);}
\draw[guide] (.3,0)--(2.5,0);\node[anchor=west] at (2.5,0){Noyau : protons et neutrons};
\draw[guide] (1.21,.7)--(2.5,1);\node[anchor=west] at (2.5,1){Électrons dans le cortège};
\node[anchor=west] at (2.5,-1){Atome : ordre de $10^{-10}$ m};
\node[anchor=west] at (2.5,-1.6){Noyau : ordre de $10^{-15}$ m};''','Modèle symbolique, sans échelle ; les électrons ne sont pas décrits ici par des orbites.')

cells=[('H',1,1,1),('He',2,8,1),('Li',3,1,2),('Be',4,2,2),('B',5,3,2),('C',6,4,2),('N',7,5,2),('O',8,6,2),('F',9,7,2),('Ne',10,8,2),('Na',11,1,3),('Mg',12,2,3),('Al',13,3,3),('Si',14,4,3),('P',15,5,3),('S',16,6,3),('Cl',17,7,3),('Ar',18,8,3)]
b=''
for sym,z,col,row in cells:
    b+=f'\\node[draw=otRule,fill={"otGreenTint" if col==8 else "otNavyTint"},minimum width=1cm,minimum height=.85cm] at ({col*1.1},{-row}){{\\shortstack{{\\scriptsize {z}\\\\\\large {sym}}}}};\n'
for j,g in enumerate([1,2,13,14,15,16,17,18],1):b+=f'\\node[text=otMuted] at ({j*1.1},0){{{g}}};\n'
F['tableau-periodique']=tik(b,'Trois premières périodes ; colonnes des blocs s et p. La place des groupes 3 à 12 est omise.')

F['lewis']=tik(r'''\node at (0,1.4){Eau};\node at (3.7,1.4){Ammoniac};\node at (8,1.4){Dioxyde de carbone};
\node (O) at (0,0){O};\node (H1) at (-.8,-.5){H};\node (H2) at (.8,-.5){H};
\draw (O)--(H1) (O)--(H2);\draw (-.4,.35)--(-.1,.55) (.1,.55)--(.4,.35);
\node (N) at (3.7,0){N};\foreach \x/\y[count=\k] in {2.8/0,4.6/0,3.7/-.8}{\node(HN\k)at(\x,\y){H};\draw(N)--(HN\k);}
\draw (3.5,.45)--(3.9,.45);
\node(C)at(8,0){C};\node(O1)at(6.9,0){O};\node(O2)at(9.1,0){O};
\draw[double,double distance=2pt] (C)--(O1) (C)--(O2);
\foreach \x in {6.9,9.1}{\draw (\x-.2,.4)--(\x+.2,.4) (\x-.2,-.4)--(\x+.2,-.4);}
\solution{\node[text=otGreenDark] at (0,-1.3){O : 2 liants + 2 non liants};\node[text=otGreenDark] at (5.5,-1.3){N : 3 liants + 1 non liant};}''','Schémas de Lewis fournis ; positions graphiques sans échelle et sans représentation des angles réels.')

F['mole']=tik(r'''\node[draw=otNavy,rounded corners=2mm,minimum width=2.5cm,minimum height=1cm] (m) at (0,0){Masse $m$};
\node[draw=otNavy,rounded corners=2mm,minimum width=2.5cm,minimum height=1cm] (n) at (4.2,0){Nombre $N$};
\node[draw=otGreenDark,rounded corners=2mm,minimum width=2.5cm,minimum height=1cm] (q) at (8.4,0){Quantité $n$};
\draw[fleche] (m)--node[above]{$\div m_{\mathrm{entité}}$}(n);\draw[fleche](n)--node[above]{$\div N_A$}(q);
\node at (0,-.9){Masse en kg};\node at (4.2,-.9){Sans unité};\node at (8.4,-.9){En mol};''','Chaîne de calcul ; les deux masses doivent utiliser la même unité.')

F['etats']=tik(r'''\node[draw=otNavy,fill=otNavyTint,minimum width=2cm,minimum height=1cm] (s) at (0,0){Solide};
\node[draw=otNavy,fill=otNavyTint,minimum width=2cm,minimum height=1cm] (l) at (4,0){Liquide};
\node[draw=otNavy,fill=otNavyTint,minimum width=2cm,minimum height=1cm] (g) at (8,0){Gaz};
\draw[->,otGreenDark] (s.north east) to[bend left=25] node[above]{Fusion}(l.north west);
\draw[->,otNavy] (l.south west) to[bend left=25] node[below]{Solidification}(s.south east);
\draw[->,otGreenDark] (l.north east) to[bend left=25] node[above]{Vaporisation}(g.north west);
\draw[->,otNavy] (g.south west) to[bend left=25] node[below]{Liquéfaction}(l.south east);
\draw[->,otGreenDark] (s.north) to[bend left=40] node[above]{Sublimation}(g.north);
\draw[->,otNavy] (g.south) to[bend left=40] node[below]{Condensation solide}(s.south);''','Les flèches vertes correspondent à des transformations endothermiques.')

F['palier']=graph(r'''\addplot[otNavy,thick] coordinates {(0,-10)(2,0)(6,0)(8,20)};
\node[font=\small,anchor=south] at (axis cs:4,2){Solide + liquide};
\node[font=\small] at (axis cs:1,10){Solide};\node[font=\small] at (axis cs:7,27){Liquide};
\solution{\addplot[otGreenDark,very thick] coordinates {(2,0)(6,0)};}''',r'xlabel={Temps (min)},ylabel={Température (°C)},xmin=0,xmax=8,ymin=-12,ymax=32,xtick={0,2,4,6,8},ytick={-10,0,10,20,30}',
'Chauffage idéalisé de l’eau à pression atmosphérique ; le palier représente la fusion.')

F['reaction']=tik(r'''\node[draw=otRule,rounded corners=2mm,text width=3.4cm,minimum height=1.5cm] at (0,0){État initial\\0,60 mol de $\ce{H2}$\\0,20 mol de $\ce{O2}$};
\draw[fleche] (2,0)--(4,0);\node at (3,.65){$2\ce{H2}+\ce{O2}\to2\ce{H2O}$};
\node[draw=otRule,rounded corners=2mm,text width=3.7cm,minimum height=1.5cm] at (6.1,0){État final\\Transformation totale\\Quantités à déterminer};
\solution{\node[text=otGreenDark] at (6.1,-1.4){0,40 mol d’eau ; 0,20 mol de $\ce{H2}$};}''')

F['reflux']=tik(r'''\draw[otInk!65] (-1.5,-.3)--(-1.5,5.7) (-1.9,-.3)--(.9,-.3);\draw[otInk!65] (-1.5,3.9)--(-.4,3.9);
\draw[otNavy] (-.18,1.75)--(-.18,2.9) (.18,1.75)--(.18,2.9);
\draw[otNavy] (0,1) circle (.8);\fill[otNavy!20] (-.73,.7) rectangle (.73,.95);
\draw[otNavy] (-.35,2.9) rectangle (.35,5.3);\draw[otNavy] (-.13,2.9)--(-.13,5.6) (.13,2.9)--(.13,5.6);
\draw[->,otNavy] (-1.05,3.2)--(-.35,3.2);\node[anchor=east] at (-1.1,3.2){Entrée d’eau};
\draw[->,otNavy] (.35,5)--(1.1,5);\node[anchor=west] at (1.2,5){Sortie d’eau};
\draw[otInk,fill=otRule!30] (-1,.1) rectangle (1,.5);\node[anchor=west] at (2.2,.3){Chauffage};\draw[guide] (1,.3)--(2,.3);
\draw[guide] (.8,1)--(2,1);\node[anchor=west] at (2.2,1){Ballon et mélange};
\draw[guide] (.4,4)--(2,4);\node[anchor=west] at (2.2,4){Réfrigérant vertical};
\node[anchor=west] at (2.2,5.7){Haut ouvert à l’atmosphère};\draw[guide] (.2,5.6)--(2,5.7);
\draw[fleche] (0,4.6)--(0,3.4);\node[anchor=west] at (2.2,2.4){Les condensats retombent};
\draw[guide] (.2,3)--(1.1,2.4)--(2,2.4);''','Montage à reflux de principe, sans échelle ; support et circulation d’eau explicités.')

F['nucleaire']=tik(r'''\node[draw=otNavy,rounded corners=2mm,minimum height=1cm] at (0,0){$\ce{^{2}_{1}H}$};
\node at (1,0){+};\node[draw=otNavy,rounded corners=2mm,minimum height=1cm] at (2,0){$\ce{^{3}_{1}H}$};
\draw[fleche] (3,0)--(4.4,0);
\node[draw=otGreenDark,rounded corners=2mm,minimum height=1cm] at (5.6,0){$\ce{^{4}_{2}He}$};\node at (6.7,0){+};
\node[draw=otNavy,rounded corners=2mm,minimum height=1cm] at (7.8,0){$\ce{^{1}_{0}n}$};
\node at (3.8,1){Fusion nucléaire};
\solution{\node[text=otGreenDark] at (3.8,-1){$A: 2+3=4+1$\qquad $Z:1+1=2+0$};}''')

F['chronophoto']=tik(r'''\draw[->,otMuted] (-.3,0)--(10.3,0) node[right]{$x$ (m)};
\foreach \x/\lab/\val in {0/0/0,.6/1/{0,20},2.4/2/{0,80},5.4/3/{1,80},9.6/4/{3,20}}{
\fill[otNavy] (\x,0) circle (.06);\node[above] at (\x,.1){$M_{\lab}$};\node[below] at(\x,-.08){$\val$};}
\node at (5,1.2){Entre deux images : $\Delta t=0,20$ s};
\solution{\draw[fleche] (.6,0)--(2.1,0);\node[text=otGreenDark] at(1.35,-.9){$\vect v_1$ : 3,0 m/s};
\draw[fleche] (5.4,0)--(8.9,0);\node[text=otGreenDark] at (7.2,-.9){$\vect v_3$ : 7,0 m/s};}''',
'Positions : 3 cm sur le dessin pour 1 m ; vecteurs du corrigé : 1 cm pour 2 m/s. Deux échelles distinctes.')

F['mouvement-circulaire']=tik(r'''\draw[otNavy] (0,0) circle (1.5);\fill[otMuted](0,0)circle(.03);\node[below]at(0,0){O};
\foreach \a/\lab in {0/1,90/2,180/3,270/4}{\fill[otNavy](\a:1.5)circle(.05);\node at(\a:1.9){$M_{\lab}$};}
\solution{\draw[fleche](1.5,0)--(1.5,1);\draw[fleche](0,1.5)--(-1,1.5);\draw[fleche](-1.5,0)--(-1.5,-1);\draw[fleche](0,-1.5)--(1,-1.5);}
\node[text width=4cm] at (5,0){Sens du mouvement :\\inverse des aiguilles\\d’une montre};''')

F['bilan-forces']=tik(r'''\fill[otRule!40] (-2,-.2) rectangle (2,0);\draw[otInk](-2,0)--(2,0);
\draw[fill=otNavyTint,otNavy] (-.8,0) rectangle (.8,.7);\fill[otInk](0,.35)circle(.04);
\node[anchor=west] at (3,.7){Système : le livre};\node[anchor=west] at (3,.1){Acteurs : Terre et table};
\solution{\draw[fleche](0,.35)--(0,1.7) node[above]{$\vect F_{\mathrm{table}\to\mathrm{livre}}$};\draw[->,otNavy,thick](0,.35)--(0,-1) node[below]{$\vect P$};}''')
F['inertie']=F['bilan-forces']
F['reciprocite']=tik(r'''\node[draw=otNavy,circle,minimum size=1cm] (a) at (0,0){A};\node[draw=otNavy,circle,minimum size=1cm](b)at(6,0){B};
\draw[otMuted,dashed] (a)--(b);\draw[fleche](0,0)--(2,0)node[above,pos=.7]{$\vect F_{B\to A}$};
\draw[->,otNavy,thick](6,0)--(4,0)node[above,pos=.7]{$\vect F_{A\to B}$};
\node at (3,-1){Même valeur, sens opposés, deux systèmes différents};''','Exemple d’interaction attractive, sans échelle.')
F['suspension']=tik(r'''\draw[otInk](-1,3)--(1,3);\draw[otInk](0,3)--(0,.4);\draw[fill=otNavyTint,otNavy](0,0)circle(.4);
\node[anchor=west]at(2,1.5){$m=0,200$ kg ; $g=10,0$ N/kg};
\solution{\draw[fleche](0,0)--(0,2)node[right]{$\vect T$};\draw[->,otNavy,thick](0,0)--(0,-2)node[right]{$\vect P$};}''',
'Forces du corrigé : 1 cm pour 1 N ; géométrie du montage sans échelle.')
F['chute']=tik(r'''\foreach \x/\t in {0/Montée,4/Sommet,8/Descente}{\node at(\x,2.1){\t};\draw[otNavy,fill=otNavyTint](\x,0)circle(.18);}
\solution{\foreach \x in {0,4,8}{\draw[->,otNavy,thick](\x,0)--(\x,-1.3)node[below]{$\vect P$};}
\draw[fleche](0,0)--(0,1.4)node[right]{$\vect v$};\node[text=otGreenDark]at(4,1){$\vect v=\vect 0$};\draw[fleche](8.35,0)--(8.35,-1.5)node[right]{$\vect v$};}''',
'Trois phases d’un même lancer vertical ; forces et vitesses ne partagent pas une échelle commune.')

F['propagation-son']=tik(r'''\node[draw=otNavy,rounded corners=2mm,text width=2.4cm,minimum height=1cm](s)at(0,0){Objet vibrant};
\node[draw=otNavy,rounded corners=2mm,text width=3cm,minimum height=1cm](m)at(4.5,0){Milieu matériel};
\node[draw=otNavy,rounded corners=2mm,text width=2.5cm,minimum height=1cm](r)at(9,0){Récepteur};
\draw[fleche](s)--(m);\draw[fleche](m)--(r);\node at(4.5,-1){Propagation de proche en proche ; pas de transport global d’air};''')
F['retard-son']=tik(r'''\draw[->,otMuted] (0,0)--(9,0);\node[draw=otNavy,fill=otNavyTint]at(0,0){Source};
\foreach \x/\l in {3/1,7/2}{\draw[otNavy,fill=white](\x,-.2)rectangle(\x+.3,.2);\node[above]at(\x,.3){Microphone \l};}
\draw[<->,otGreenDark](3,-.8)--node[below]{1,02 m}(7,-.8);
\node[anchor=west]at(.5,1.2){Signal reçu au second microphone 3,00 ms plus tard};
\solution{\node[text=otGreenDark]at(4.5,-1.7){$v=1,02/0,00300=340$ m/s};}''')
F['echo']=tik(r'''\node[draw=otNavy,fill=otNavyTint,text width=2cm]at(0,0){Émetteur\\récepteur};\draw[otInk,line width=3pt](8,-1)--(8,1.4);\node[above]at(8,1.5){Obstacle};
\draw[fleche](1.2,.4)--(7.8,.4);\draw[->,otNavy,thick](7.8,-.4)--(1.2,-.4);\node at(4.5,1.1){Aller};\node at(4.5,-1){Retour};
\draw[<->,otMuted](0,-1.8)--node[below]{$d$}(8,-1.8);''','Trajet total du signal : 2d ; schéma sans échelle.')
F['signal-periodique']=graph(r'''\addplot[otNavy,thick,domain=0:8,samples=160]{sin(180*x)};
\solution{\draw[<->,otGreenDark,thick](axis cs:.5,1.3)--node[above,font=\small]{$T=2,0$ ms}(axis cs:2.5,1.3);}''',
r'xlabel={Temps (ms)},ylabel={Signal (unité arbitraire)},xmin=0,xmax=8,ymin=-1.3,ymax=1.8,xtick={0,1,...,8},ytick={-1,0,1}')
F['timbres']=graph(r'''\addplot[otNavy,thick,domain=0:6,samples=180]{sin(180*x)};
\addplot[otGreenDark,thick,dashed,domain=0:6,samples=180]{sin(180*x)+.28*sin(540*x)};\legend{A,B}''',
r'xlabel={Temps (ms)},ylabel={Signal (unité arbitraire)},xmin=0,xmax=6,ymin=-1.5,ymax=1.5,xtick={0,1,...,6},legend style={font=\small,at={(1,1)},anchor=north east}')

# Bande spectrale construite avec 80 rectangles vectoriels, sans image bitmap.
colors=['violet','blue','cyan','green','yellow','orange','red']
b=r'\node[anchor=east]at(-.4,1.3){Continu};\node[anchor=east]at(-.4,0){Raies};'
stops=[(111,28,176),(34,73,210),(40,187,234),(49,184,74),(247,220,62),(245,147,55),(222,60,64)]
for j in range(140):
    u=j*6/139;k=min(int(u),5);f=u-k
    rgb=[round(stops[k][c]*(1-f)+stops[k+1][c]*f) for c in range(3)]
    b+=f'\\definecolor{{otSpec{j}}}{{RGB}}{{{rgb[0]},{rgb[1]},{rgb[2]}}}\\fill[otSpec{j}]({j*.06:.3f},1)rectangle({(j+1)*.06:.3f},1.6);\n'
b+=r'\fill[black!85](0,-.3)rectangle(8.4,.3);'
for xx,col in [(.85,'blue'),(2.04,'green'),(4.25,'yellow'),(6.4,'red')]:b+=f'\\draw[{col},line width=2pt]({xx},-.28)--({xx},.28);'
b+=r'\draw[->,otMuted](0,-.9)--(8.7,-.9)node[right]{$\lambda$};\node[below]at(0,-.9){400 nm};\node[below]at(8.4,-.9){800 nm};'
F['spectres']=tik(b,'Spectres schématiques ; les positions des raies ne sont pas des références d’identification.')

F['refraction']=tik(r'''\fill[otNavyTint](-3,-2)rectangle(3,0);\draw[otNavy](-3,0)--(3,0);\draw[guide](0,-2)--(0,2.5);
\draw[->,otNavy,thick](-1.5,2.598)--(0,0);\node[anchor=east]at(-1.4,2.4){Incident};
\draw[otMuted](0,.9)arc(90:120:.9);\node at(-.3,1.25){$i$};\node[anchor=west]at(1.5,1.5){Air $n_1=1,00$};
\node[anchor=west]at(1.5,-1.6){Verre $n_2=1,50$};\node[above right]at(0,0){I};\node at(0,2.9){Normale};
\enonce{\draw[otMuted,dotted](0,0)--(.707,-2);\node at(.6,-.7){$r$};}
\solution{\draw[fleche](0,0)--(.707,-2);\draw[otGreenDark](0,-.9)arc(270:289.47:.9);\node[text=otGreenDark]at(.8,-.7){$r=19,5^\circ$};}''',
'Trajet dans le plan d’incidence ; dessin des rayons pour i = 30°, indices fournis. Le rayon réfléchi est traité séparément.')
F['reflexion']=tik(r'''\draw[otInk,line width=1pt](-3,0)--(3,0);\draw[guide](0,0)--(0,2.7);\draw[->,otNavy,thick](-1.93,2.30)--(0,0);
\node at(-.45,1.15){$i=40^\circ$};\node at(0,3){Normale};
\solution{\draw[fleche](0,0)--(1.93,2.30);\node[text=otGreenDark]at(1,1.1){$i'=40^\circ$};}''','Rayons réfléchis dans le plan d’incidence ; angles mesurés à la normale.')
F['snell-graphe']=graph(r'''\addplot[only marks,otNavy]coordinates{(.1,.15)(.2,.30)(.3,.45)(.4,.60)(.5,.75)};
\addplot[otNavy,domain=0:.55]{1.5*x};
\solution{\addplot[otGreenDark,dashed,thick]coordinates{(0,.6)(.4,.6)(.4,0)};}''',r'xlabel={$\sin r$},ylabel={$\sin i$},xmin=0,xmax=.6,ymin=0,ymax=.9,xtick={0,.1,...,.6},ytick={0,.15,...,.9}')
b=r'''\fill[otNavy!10](0,0)--(1.6,3)--(3.2,0)--cycle;\draw[otNavy](0,0)--(1.6,3)--(3.2,0)--cycle;
\draw[->,otInk,thick](-2,1.3)--(.693333,1.3);\node at(-1,1.8){Lumière blanche};'''
normal=math.atan(1.6/3)
prism_data=[]
for couleur,n,texte,delta in [('otRed',1.50,'Rouge',.12),('violet',1.53,'Violet',-.12)]:
    alpha=-normal+math.asin(math.sin(normal)/n)
    pente=math.tan(alpha);entree=1.3*1.6/3
    xx=(3.2-(1.6/3)*1.3+(1.6/3)*pente*entree)/(1+(1.6/3)*pente)
    yy=1.3+pente*(xx-entree)
    sortie=normal-math.asin(n*math.sin(normal-alpha))
    yfin=yy+math.tan(sortie)*(5.3-xx)
    prism_data.append((n,entree,xx,yy,alpha,sortie))
    b+=f'\\draw[{couleur},rayon]({entree:.6f},1.3)--({xx:.6f},{yy:.6f})--(5.3,{yfin:.6f});\\node[anchor=west,text={couleur}]at(5.4,{yfin+delta:.6f}){{{texte}}};'
F['prisme']=tik(b,'Dispersion par un prisme : déviation calculée aux deux interfaces. Deux radiations seulement sont dessinées ; schéma sans échelle.')

def lentille(p=20,foyer=False):
    # Échelle : 0,2 cm de dessin pour 1 cm réel ; y : 1 cm de dessin pour 1 cm réel.
    pp=10*p/(p-10);xx=-p*.2;xi=pp*.2;yi=-2*pp/p
    b=f'\\draw[->,otMuted](-6.6,0)--({max(5,xi+.8)},0)node[right]{{Axe}};'+r'''\draw[<->,otNavy,thick](0,-2.8)--(0,2.8);
\foreach \x/\l in {-2/F,2/{F'}}{\draw[otInk](\x,-.08)--(\x,.08);\node[below]at(\x,-.1){$\l$};}
\node[below left]at(0,-.1){O};'''
    if foyer:
        b+=r"\foreach \y in {1,2}{\draw[->,otNavy](-5,\y)--(0,\y);\draw[fleche](0,\y)--(2,0)--(3,-\y/2);}\draw[<->,otMuted](0,-1.4)--node[below]{$f'=10$ cm}(2,-1.4);"
    else:
        b+=f'\\draw[->,otInk,thick]({xx},0)--({xx},2)node[above]{{B}};\\node[below]at({xx},0){{A}};\n'
        b+=r'\enonce{\node[text=otMuted]at(-.5,3.2){Construire l’image réelle};}'
        b+=f'\\solution{{\\draw[otGreenDark,rayon]({xx},2)--(0,2)--({xi},{yi});\\draw[otNavy,rayon]({xx},2)--({xi},{yi});\\draw[->,otGreenDark,thick]({xi},0)--({xi},{yi})node[below]{{$B^{{\\prime}}$}};\\node[above]at({xi},0){{$A^{{\\prime}}$}};}}'
    return tik(b,'Échelle horizontale : 1 cm de dessin pour 5 cm réels ; verticale : 1 cm pour 1 cm réel. Les rayons se construisent sur ces deux échelles.')
F['lentille-foyers']=lentille(foyer=True);F['lentille-2f']=lentille(20);F['lentille-3f']=lentille(30)
F['lentille-agrandie']=lentille(15)
F['oeil']=tik(r'''\draw[otNavy] (0,0) ellipse (2 and 1.3);\draw[otNavy,thick](-1.5,-.85)--(-1.5,-.7) (-1.5,.7)--(-1.5,.85);
\draw[<->,otGreenDark,thick](-1.1,-.9)--(-1.1,.9);\draw[otRed,thick](1.7,-.8)--(1.7,.8);
\draw[->,otMuted](-3.5,.6)--(-1.1,.6)--(1.7,0);\draw[otMuted](-3.5,-.3)--(-1.1,-.3)--(1.7,0);
\node[anchor=east]at(-2.2,1.7){Diaphragme : pupille};\draw[guide](-1.5,.7)--(-2.2,1.4);
\node[anchor=west]at(2.7,1.5){Lentille : système optique};\draw[guide](-1.1,.9)--(-.5,1.5)--(2.4,1.5);
\node[anchor=west]at(2.7,-.8){Écran : rétine};\draw[guide](1.7,-.5)--(2.5,-.8);''','Œil réduit : un point lointain sur l’axe donne une image sur l’écran rétinien ; schéma de principe sans échelle anatomique.')

# Symboles électriques rectangulaires selon la convention usuelle française.
F['mesures-circuit']=tik(r'''\draw[otInk] (0,0)--(0,2)--(2,2);\draw[otInk](2.6,2)--(4,2)--(4,0)--(0,0);
\draw[otNavy,fill=white](2.3,2)circle(.3);\node at(2.3,2){\enonce{1}\solution{A}};
\draw[fill=white,otNavy](1.6,-.22)rectangle(2.9,.22);\node[below]at(2.25,-.25){R};
\draw[otInk](1.2,0)--(1.2,-1.3)--(1.95,-1.3) (2.55,-1.3)--(3.3,-1.3)--(3.3,0);
\draw[otNavy,fill=white](2.25,-1.3)circle(.3);\node at(2.25,-1.3){\enonce{2}\solution{V}};
\draw[otNavy,fill=white](0,1)circle(.35);\node at(0,1){G};\node[above left]at(0,1.4){$+$};
\solution{\node[anchor=west]at(5,1.5){A en série};\node[anchor=west]at(5,.6){V en dérivation sur R};}
\enonce{\node[anchor=west,text width=3.7cm]at(5,1){Identifier les appareils 1 et 2.};}
\draw[fleche](.6,2)--(1.3,2)node[above]{$I$};''')
F['noeud']=tik(r'''\fill[otInk](0,0)circle(.07);\draw[->,otNavy](-3,0)--(0,0);\draw[->,otNavy](0,0)--(2,1.2);\draw[->,otNavy](0,0)--(2,-1.2);
\node[above]at(-1.8,0){$I=0,30$ A};\node[above]at(1.6,1.3){$I_1=0,12$ A};\node[below]at(1.6,-1.3){$I_2$};\node[anchor=west]at(4,0){$I=I_1+I_2$};
\solution{\node[text=otGreenDark,anchor=west]at(4,-.8){$I_2=0,18$ A};}''')
F['ohm']=graph(r'''\addplot[only marks,otNavy]coordinates{(0,0)(10,2)(20,4)(30,6)(40,8)};\addplot[otNavy,domain=0:40]{.2*x};
\solution{\addplot[otGreenDark,dashed,thick]coordinates{(0,4)(20,4)(20,0)};}''',r'xlabel={$I$ (mA)},ylabel={$U$ (V)},xmin=0,xmax=40,ymin=0,ymax=8.5,xtick={0,10,20,30,40},ytick={0,2,4,6,8}')
F['serie']=tik(r'''\draw[otInk](0,0)--(0,3)--(6,3)--(6,0)--(0,0);\draw[fill=white,otNavy](0,1.5)circle(.35);\node at(0,1.5){G};\node[left]at(-.4,2){9,0 V};
\foreach \x/\l/\r in {2/1/100,4.5/2/200}{\draw[fill=white,otNavy](\x-.5,2.8)rectangle(\x+.5,3.2);\node[above]at(\x,3.3){$R_\l=\r\,\Omega$};}
\draw[fleche](.6,3)--(1.1,3)node[above]{$I$};\node[above left]at(0,1.9){$+$};
\solution{\node[text=otGreenDark]at(3,1.2){$I=30$ mA ; $U_1=3,0$ V ; $U_2=6,0$ V};}''')
F['capteur-courbe']=graph(r'''\addplot[only marks,otNavy]coordinates{(0,20)(10,16)(20,12)(30,8)(40,4)};\addplot[otNavy,domain=0:40]{20-.4*x};
\solution{\addplot[otGreenDark,dashed,thick]coordinates{(0,10)(25,10)(25,0)};}''',r'xlabel={Température (°C)},ylabel={$R$ (k$\Omega$)},xmin=0,xmax=40,ymin=0,ymax=22,xtick={0,10,20,30,40},ytick={0,4,8,12,16,20}',
r'Modèle local construit : $R=20,0-0,400\theta$, uniquement de 0 à 40 °C.')
F['pont-capteur']=tik(r'''\draw[otInk](0,0)--(0,4)--(4,4)--(4,0)--(0,0);\draw[fill=white,otNavy](0,2)circle(.4);\node at(0,2){G};\node[left]at(-.5,2.6){$U_0$};\node[above left]at(0,2.5){$+$};
\draw[fill=white,otNavy](3.75,2.7)rectangle(4.25,3.5);\node[anchor=west]at(4.5,3.1){$R_0$};
\draw[otGreenDark,fill=otGreenTint](3.75,.6)rectangle(4.25,1.4);\node[anchor=east]at(3.5,1){Capteur $R_c$};
\fill[otInk](4,2)circle(.05);\draw[->,otNavy](4,2)--(7,2);\node[anchor=west]at(7.1,2){Entrée de mesure};
\draw[->,otGreenDark,thick](6,.1)--(6,1.9);\node[right]at(6,1){$U$};\draw[guide](4,0)--(6.3,0);\node[below]at(4,0){Référence 0 V};
\draw[fleche](1,4)--(2,4)node[above]{$I$};''',r'Pont résistif ; entrée d’acquisition de très grande résistance. Tension $U$ : point milieu par rapport à la référence $0\,\mathrm{V}$.')

F['etats-micro']=tik(r'''\foreach \x/\t in {0/Solide,4/Liquide,8/Gaz}{\draw[otRule,fill=otNavyTint](\x,0)rectangle(\x+3,2.3);\node at(\x+1.5,2.7){\t};}
\foreach \x in {.8,1.5,2.2}{\foreach \y in {.5,1.1,1.7}{\fill[otNavy](\x,\y)circle(.09);}}
\foreach \x/\y in {4.5/.4,5.2/.5,5.9/.35,6.6/.5,4.8/1,5.6/1.1,6.3/1,5.1/1.6,6.1/1.65}{\fill[otNavy](\x,\y)circle(.09);}
\foreach \x/\y in {8.3/.3,9.4/.4,10.6/.3,8.5/1.1,9.5/1.15,10.7/1.1,8.3/2,9.4/2,10.5/2}{\fill[otNavy](\x,\y)circle(.09);}
''','Modèle microscopique d’une même espèce : entités identiques et en même nombre ; distances et tailles sans échelle.')
F['teintes']=tik(r'''\foreach \x/\c/\a in {0/0/0,1.5/2/15,3/4/30,4.5/6/45,6/8/60}{
\fill[otNavy!\a] (\x,0)rectangle(\x+.7,1.7);\draw[otNavy](\x,2.2)--(\x,0)--(\x+.7,0)--(\x+.7,2.2);\node at(\x+.35,-.5){\c\ g/L};}
\fill[otNavy!38](8,0)rectangle(8.7,1.7);\draw[otNavy](8,2.2)--(8,0)--(8.7,0)--(8.7,2.2);\node at(8.35,-.5){X};
\node at(3.3,2.8){Même soluté, même épaisseur de solution observée};
\solution{\node[text=otGreenDark]at(4.5,-1.3){$4<c_X<6$ g/L dans cette comparaison visuelle};}''','Échelle de teintes schématique : comparaison qualitative, sans mesure colorimétrique précise.')
def parallele(r1,r2):
    b=r'''\draw[otInk](0,0)--(0,3)--(6,3)--(6,0)--(0,0);\draw[otInk](3,0)--(3,3);
\draw[otNavy,fill=white](0,1.5)circle(.35);\node at(0,1.5){G};\node[left]at(-.4,2){6,0 V};\node[above left]at(0,1.9){$+$};
\draw[fill=white,otNavy](2.75,1)rectangle(3.25,2);\draw[fill=white,otNavy](5.75,1)rectangle(6.25,2);
\draw[fleche](3,2.8)--(3,2.2)node[right]{$I_1$};\draw[fleche](6,2.8)--(6,2.2)node[right]{$I_2$};\draw[fleche](.7,3)--(1.5,3)node[above]{$I$};'''
    b+=f'\\node[anchor=east]at(2.5,1.5){{$R_1={r1}\\,\\Omega$}};\\node[anchor=west]at(6.6,1.5){{$R_2={r2}\\,\\Omega$}};'
    b+=f'\\solution{{\\node[text=otGreenDark]at(3,-.8){{$I_1={6000/r1:g}$ mA ; $I_2={6000/r2:g}$ mA}};}}'
    return tik(b,'Deux résistances entre les mêmes nœuds : même tension de 6,0 V ; circuit sans échelle.')
F['parallele']=parallele(100,200);F['parallele-defi']=parallele(200,300)

def produire_figures():
    for name,s in F.items():
        for fill in ('white','otNavyTint'):
            s=s.replace('[fill='+fill+',otNavy]','[otNavy,fill='+fill+']')
        write('figures/'+name+'.tex',s)
    print(len(F),'sources de figures vectorielles écrites.')
if __name__=='__main__':produire_figures()
