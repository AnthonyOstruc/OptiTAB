"""Schémas vectoriels originaux. Les tracés de lentilles sont calculés."""
from pathlib import Path
import math
R = Path(__file__).resolve().parent / 'figures'
R.mkdir(exist_ok=True)
figs = {}
def add(name, body, opts='x=1cm,y=1cm'):
    figs[name] = '\\begin{tikzpicture}['+opts+']\n'+body+'\n\\end{tikzpicture}\n'

add('spectres',r'''
\draw[axis] (0,0)--(12.2,0);\node[lab,anchor=west]at(12.4,0){$\lambda_0$ (nm)};
\foreach \x/\v in {0/400,4/500,8/600,12/700}{\draw (\x,-.07)--(\x,.07);\node[lab,below]at(\x,-.1){\v};}
\node[lab,anchor=west]at(0,2.9){Spectre continu (source thermique)};
\draw[otOrange,line width=1.3pt] plot[smooth] coordinates{(0,.65)(1,.85)(3,1.3)(6,1.8)(9,2)(12,1.9)};
\node[lab,anchor=west]at(0,5.5){Spectre de raies (source atomique)};
\draw[otMuted] (0,3.5)--(12,3.5);
\foreach \x in {.35,1.35,5.45,10.25}{\draw[otNavy,line width=1.3pt] (\x,3.5)--(\x,4.9);}
\node[lab,anchor=west]at(7.4,4.4){Raies schématiques};
''')
add('modele',r'''
\fill[otNavyTint] (0,0)rectangle(12,2);
\foreach \y in {.4,1,1.6}{\draw[ray] (.5,\y)--(11.5,\y);}
\node[lab]at(6,2.5){Milieu homogène et isotrope : direction constante};
\draw[otInk] (1,-.8)--(1,-2.3) (1,-2.5)--(1,-4);
\draw[ray] (0,-2.4)--(1,-2.4);
\draw[otGreenDark] (1,-2.4)--(4,-1) (1,-2.4)--(4,-3.8);
\node[lab,anchor=west,text width=7cm]at(4.5,-2.4){Une ouverture de taille comparable à $\lambda$ produit une forte diffraction. Le modèle des rayons seuls devient insuffisant.};
''')
add('descartes',r'''
\fill[otNavyTint] (-4.8,-2.9) rectangle (4.8,0);
\draw[otInk] (-4.8,0)--(4.8,0);
\draw[normal] (0,-2.9)--(0,3);
\draw[ray] (-3,2.6)--(0,0);\draw[raytwo] (0,0)--(3,2.6);
\draw[raythree] (0,0)--(1.8,-2.8);
\node[lab]at(-3.4,.4){Milieu 1 : $n_1$};\node[lab]at(-3.4,-.5){Milieu 2 : $n_2>n_1$};
\node[lab]at(-2.7,2.7){Incident};\node[lab]at(2.9,2.8){Réfléchi};
\node[lab]at(2.7,-2.5){Réfracté};\node[lab]at(.9,2.3){Normale};
\draw[otInk] (0,.8) arc(90:139:.8);\node[lab]at(-.45,1.15){$i$};
\draw[otInk] (.52,-.8)arc(-57:-90:.95);\node[lab]at(.35,-1.3){$r$};
\node[lab,below left]at(0,0){$I$};
''')
add('totale',r'''
\foreach \x/\txt in {0/Réfraction,4.3/Incidence limite,8.6/Réflexion totale}{
\begin{scope}[shift={(\x,0)}]\fill[otNavyTint](-1.8,-2)rectangle(1.8,0);\draw[otInk](-1.8,0)--(1.8,0);\draw[normal](0,-2)--(0,1.7);\node[lab]at(0,2.2){\txt};\node[lab]at(-1.1,-1.9){$n_1$};\node[lab]at(-1.1,1.5){$n_2<n_1$};\end{scope}}
\draw[ray](-.8,-1.8)--(0,0);\draw[raytwo](0,0)--(1.4,1.5);
\draw[ray](3.1,-1.5)--(4.3,0);\draw[raytwo](4.3,0)--(6,0);
\draw[ray](7,-1)--(8.6,0);\draw[raytwo](8.6,0)--(10.2,-1);
\node[lab]at(0,-2.5){$i<i_c$};\node[lab]at(4.3,-2.5){$i=i_c$};\node[lab]at(8.6,-2.5){$i>i_c$};
''')
add('miroir',r'''
\fill[pattern=north east lines,pattern color=otRule](0,-2.3)rectangle(.22,2.4);
\draw[otInk,line width=1pt](0,-2.3)--(0,2.4);
\fill[otNavy](-3,0)circle(1.5pt) node[lab,left]{$A$};\fill[otNavy](3,0)circle(1.5pt) node[lab,right]{$A'$};
\draw[ray](-3,0)--(0,1.5);\draw[raytwo](0,1.5)--(-3,3);\draw[virtual](0,1.5)--(3,0);
\draw[ray](-3,0)--(0,-1.5);\draw[raytwo](0,-1.5)--(-3,-3);\draw[virtual](0,-1.5)--(3,0);
\draw[otMuted,<->](-3,-.6)--(0,-.6)node[midway,lab]{$d$};\draw[otMuted,<->](0,-.6)--(3,-.6)node[midway,lab]{$d$};
\node[lab]at(0,3.1){Miroir plan};\node[lab]at(3,1.3){Prolongements};
''')
add('gauss',r'''
\draw[axis](-5,0)--(5.4,0);\draw[lens](0,-1.8)--(0,1.8);
\draw[ray](-4,.45)--(0,.45)--(3,-.225);\draw[raytwo](-4,.45)--(0,0)--(3,-.3375);
\draw[otOrange,dashed](-4,2)--(0,1.6)--(3,-.4);
\node[lab,anchor=west]at(.7,1.7){Rayon trop éloigné de l'axe};
\node[lab,anchor=west]at(-4.5,-1.3){Rayons paraxiaux : proches de l'axe et peu inclinés};
\fill[otNavy](-4,.45)circle(1.5pt)node[lab,above]{$B$};
\node[lab]at(0,-2.2){Lentille};
''')
def lens(name,p,f,h=1,xlo=None,xhi=None):
    q=f*p/(p+f)
    if xlo is None:xlo=min(p,q, -abs(f))*1.18
    if xhi is None:xhi=max(q,abs(f),2)*1.22
    scale=12/(xhi-xlo)
    yi=h*q/p
    end1=h-h*xhi/f
    end2=h*xhi/p
    extent=max(abs(h),abs(yi),abs(end1),abs(end2),1)*1.13
    ys=min(1.15,3.1/extent)
    lines=[f'\\draw[axis]({xlo},0)--({xhi},0);',
      r'\draw[lens](0,-2.5)--(0,2.5);' if f>0 else r'\draw[otInk,line width=1pt](0,-2.5)--(0,2.5);\draw[otInk](-.18,2.5)--(0,2.15)--(.18,2.5);\draw[otInk](-.18,-2.5)--(0,-2.15)--(.18,-2.5);',
      f'\\draw[otInk,-{{Stealth}}]({p},0)--({p},{h});',
      f'\\draw[otGreenDark,-{{Stealth}}]({q},0)--({q},{yi});',
      f'\\draw[ray]({p},{h})--(0,{h})--({xhi},{end1});',
      f'\\draw[raytwo]({p},{h})--(0,0)--({xhi},{end2});']
    if q<0:
      lines += [f'\\draw[virtual](0,{h})--({q},{yi});',f'\\draw[virtual](0,0)--({q},{yi});']
    point_labels=[(p,'A','below'),(p,'B','above left'),(q,"A'",'below'),(q,"B'",'above left' if yi>0 else 'below right'),(-f,'F','below'),(f,"F'",'below')]
    if abs(q+f)<1e-8:
        point_labels=[(x,t,a) for x,t,a in point_labels if t not in ("A'",'F')]+[(q,"A'=F",'below')]
    for x,t,a in point_labels:
      y=h if t=='B' else yi if t=="B'" else 0
      lines.append(f'\\node[lab,{a}]at({x},{y}){{${t}$}};')
    lines += [r'\node[lab,below left]at(0,0){$O$};',r'\node[lab,above]at(0,2.5){$L$};']
    # Lens height is defined in plotting coordinates, remaining inside a fixed drawing box.
    add(name,'\n'.join(lines),f'x={scale:.5f}cm,y={ys:.5f}cm')
lens('lentille-reelle',-4,1.5,xlo=-4.7,xhi=3.15)
lens('lentille-virtuelle',-1,2,xlo=-3,xhi=2.6)
lens('lentille-divergente',-4,-2,xlo=-4.8,xhi=3)
lens('ex-lentille',-3,2,xlo=-3.8,xhi=6.8)
lens('corr-loupe',-.6,1,h=.45,xlo=-1.8,xhi=1.35)
add('ex-lame',r'''
\fill[otNavyTint](0,-1.4)rectangle(2,1.9);\draw[otInk](0,-1.4)--(0,1.9) (2,-1.4)--(2,1.9);
\draw[ray](-1,1.8)--(0,.8)--(2,-.269045)--(3,-1.269045);
\node[lab]at(1,1.6){Verre};\node[lab]at(-1.2,-.6){Air};\node[lab]at(3.1,.9){Air};
\node[lab,above right]at(0,.8){$I$};\node[lab,above right]at(2,-.269045){$J$};
\draw[otMuted,<->](0,-1.8)--(2,-1.8)node[midway,lab]{$e$};
''','x=1cm,y=1cm')
add('corr-lame',r'''
\fill[otNavyTint](0,-1.4)rectangle(2,1.9);\draw[otInk](0,-1.4)--(0,1.9) (2,-1.4)--(2,1.9);
\draw[ray](-1,1.8)--(0,.8)--(2,-.269045)--(3,-1.269045);
\draw[normal](-1.3,.8)--(1.1,.8) (.8,-.269045)--(3.5,-.269045);
\draw[otMuted,dashed](0,.8)--(2.9,-2.1);
\draw[otOrange,<->](2,-.269045)--(1.5345225,-.7345225);
\node[lab]at(2.25,-.8){$s$};\node[lab]at(1,1.6){Verre};
\node[lab,above right]at(0,.8){$I$};\node[lab,above right]at(2,-.269045){$J$};
\node[lab]at(-1.2,-.6){Air};\node[lab]at(3.1,.9){Air};
''','x=1cm,y=1cm')
add('ex-construction',r'''
\draw[axis](-5.5,0)--(4.5,0);\draw[lens](0,-.9)--(0,1.2);
\draw[otInk,-{Stealth}](-4.5,0)--(-4.5,.8);
\foreach \x/\t in {-4.5/A,-1.5/F,0/O,1.5/F'}{\node[lab,below]at(\x,0){$\t$};}
\node[lab,above]at(-4.5,.8){$B$};\node[lab,above]at(0,1.2){$L$};
''')
add('ex-profondeur',r'''
\draw[axis](-3.5,0)--(8.5,0);\draw[lens](0,-1)--(0,1);
\draw[otInk,line width=1pt](6,-1)--(6,1);
\fill[otNavy](-3,0)circle(1.5pt)node[lab,above]{$A$};
\node[lab,above]at(0,1){Ouverture $a$};\node[lab,above]at(6,1){Capteur};
\draw[otMuted,<->](0,-1.4)--(6,-1.4)node[midway,lab]{$q_0$};
''')
add('ex-association',r'''
\draw[axis](-3.5,0)--(4,0);\draw[lens](0,-1.1)--(0,1.1);
\draw[otInk,line width=1pt](2,-1.1)--(2,1.1);\draw[otInk](1.85,1.1)--(2,.85)--(2.15,1.1) (1.85,-1.1)--(2,-.85)--(2.15,-1.1);
\draw[otInk,-{Stealth}](-3,0)--(-3,.7);\node[lab,above]at(-3,.7){$B$};
\foreach \x/\t in {-3/A,-1/F_1,0/O_1,1/F'_1=F'_2,2/O_2,3/F_2}{\node[lab,below]at(\x,0){$\t$};}
\node[lab,above]at(0,1.1){$L_1$};\node[lab,above]at(2,1.1){$L_2$};
''','x=1.4cm,y=1cm')
add('foyers',r'''
\draw[axis](-5,0)--(5.5,0);\draw[lens](0,-2)--(0,2);
\foreach \h in {.2,.7,1.2}{\draw[ray](-4,\h+.8)--(0,\h)--(3,-.6);}
\draw[normal](3,-1.5)--(3,1.8);\node[lab,below]at(3,0){$F'$};\node[lab,right]at(3,-.6){$B'_{\infty}$};
\node[lab,below left]at(0,0){$O$};\node[lab]at(-3,2.2){Faisceau parallèle incliné};
\node[lab]at(3,2.2){Plan focal image};
''')
add('distances',r'''
\draw[axis](-5,0)--(5.5,0);\draw[lens](0,-.7)--(0,.7);
\foreach \x/\t in {-4/A,-1.5/F,0/O,1.5/F',2.4/A'}{\fill[otInk](\x,0)circle(1.2pt);\node[lab,below]at(\x,0){$\t$};}
\draw[otNavy,->](0,1.4)--(-4,1.4)node[midway,lab]{$\overline{OA}<0$};
\draw[otGreenDark,->](0,2.2)--(2.4,2.2)node[midway,lab]{$\overline{OA'}>0$};
\draw[otOrange,->](-1.5,-1.2)--(-4,-1.2)node[midway,lab]{$\overline{FA}$};
\draw[otOrange,->](1.5,-1.2)--(2.4,-1.2)node[midway,lab]{$\overline{F'A'}$};
''')
add('bessel',r'''
\draw[axis](0,0)--(12.3,0);\draw[otInk,->](.5,0)--(.5,1.1)node[lab,above]{Objet};
\draw[otInk,line width=1pt](11.5,-1.4)--(11.5,1.4)node[lab,above]{Écran};
\draw[lens](3,-1.3)--(3,1.3);\draw[lens](9,-1.3)--(9,1.3);
\node[lab,below]at(3,-1.35){$x_1$};\node[lab,below]at(9,-1.35){$x_2$};
\draw[otNavy,<->](.5,-2.4)--(11.5,-2.4)node[midway,lab]{$D$};
\draw[otGreenDark,<->](3,2.1)--(9,2.1)node[midway,lab]{$d$};
\node[lab]at(6,3){Deux positions de netteté pour $D>4f'$};
''')
add('oeil',r'''
\draw[axis](-3,0)--(7,0);\draw[lens](0,-1.5)--(0,1.5);
\draw[otInk,line width=1.2pt](4,-1.7)--(4,1.7);\node[lab,above]at(4,1.7){Rétine fixe};
\draw[ray](-2.5,1)--(0,1)--(4,0);\draw[raytwo](-2.5,-1)--(0,-1)--(4,0);
\node[lab,above]at(0,1.8){Lentille de vergence variable};
\draw[otMuted,<->](0,-2.3)--(4,-2.3)node[midway,lab]{$\ell\simeq17$ mm};
\node[lab,anchor=west]at(4.5,-.9){Image réelle};
''')
add('photo',r'''
\draw[axis](-4,0)--(5.7,0);\draw[lens](0,-1.6)--(0,1.6);
\draw[otInk,line width=1.1pt](4,-1.9)--(4,1.9);\node[lab,above]at(4,1.9){Capteur mobile};
\draw[otInk,line width=2pt](-.35,-2)--(-.35,-.8) (-.35,.8)--(-.35,2);
\draw[ray](-3,.6)--(0,.6)--(4,-.8);\draw[raytwo](-3,.6)--(0,0)--(4,-.8);
\draw[otGreenDark,->](4,0)--(4,-.8);\node[lab,left]at(-3,.6){$B$};\node[lab,right]at(4,-.8){$B'$};
\node[lab]at(-2,-1.7){Diaphragme};\node[lab]at(1.4,2.35){Objectif};
''')
add('profondeur',r'''
\draw[axis](-1,0)--(12.5,0);\draw[lens](0,-2)--(0,2);
\draw[otInk,line width=1pt](7,-2.2)--(7,2.2);\node[lab,above]at(7,2.2){Capteur fixé à $q_0$};
\draw[ray](0,1.8)--(10,0);\draw[ray](0,-1.8)--(10,0);\draw[raytwo](0,1.8)--(5,0)--(9,-1.44);\draw[raytwo](0,-1.8)--(5,0)--(9,1.44);
\fill[otNavy](10,0)circle(1.5pt);\fill[otGreenDark](5,0)circle(1.5pt);
\node[lab,below]at(5,-.1){$q<q_0$};\node[lab,below]at(10,-.1){$q>q_0$};
\draw[otNavy,<->](7.35,-.54)--(7.35,.54);\node[lab,anchor=west]at(8,.8){Tache de flou};
\node[lab,left]at(0,1.8){$a/2$};\node[lab,left]at(0,-1.8){$-a/2$};
''')
add('fibre',r'''
\fill[otNavyTint](0,-1)rectangle(11,1);\fill[otGreenTint](0,1)rectangle(11,1.7);\fill[otGreenTint](0,-1.7)rectangle(11,-1);
\draw[otInk](0,-1.7)--(0,1.7) (0,1)--(11,1) (0,-1)--(11,-1);
\draw[normal](-2,0)--(11.5,0);\draw[ray](-2,-1)--(0,0)--(2.5,1)--(7.5,-1)--(11,.4);
\draw[normal](2.5,-.5)--(2.5,2.3);
\node[lab]at(7,1.35){Gaine $n_2$};\node[lab]at(5,.55){Cœur $n_1>n_2$};\node[lab]at(-1,1.2){$n_0$};
\node[lab]at(.9,.16){$\theta$};\draw[otInk](2.5,.4)arc(-90:-158:.6);\node[lab]at(2.15,.4){$i$};\node[lab]at(-1,-.18){$\alpha$};
''')
add('dispersion',r'''
\fill[otNavyTint](0,-.8)rectangle(12,.8);\draw[otInk](0,.8)--(12,.8) (0,-.8)--(12,-.8);
\draw[ray](0,0)--(12,0);\draw[raytwo](0,0)--(2,.8)--(6,-.8)--(10,.8)--(12,0);
\node[lab]at(6,1.6){Trajet oblique : longueur $L/\cos\theta$};
\node[lab]at(6,-1.6){Trajet axial : longueur $L$};
\draw[otMuted,<->](0,-2.3)--(12,-2.3)node[midway,lab]{$L$};
''')
add('banc',r'''
\draw[otInk,line width=1pt](0,0)--(12.3,0);
\foreach \x in {0,.5,...,12}{\draw[otMuted](\x,0)--(\x,-.12);}
\draw[otInk,->](.8,0)--(.8,1.2);\draw[lens](4,-.4)--(4,1.8);\draw[otInk,line width=1pt](10.7,-.2)--(10.7,2);
\node[lab,above]at(.8,1.3){Objet};\node[lab,above]at(4,1.8){Lentille};\node[lab,above]at(10.7,2){Écran};
\draw[otNavy,<->](.8,-.8)--(4,-.8)node[midway,lab]{$p=x_L-x_A$};
\draw[otGreenDark,<->](4,-1.5)--(10.7,-1.5)node[midway,lab]{$q=x_E-x_L$};
''')
add('microscope',r'''
\draw[axis](-3,0)--(10,0);\draw[lens](0,-1.8)--(0,1.8);\draw[lens](7,-1.8)--(7,1.8);
\draw[otInk,->](-2.5,0)--(-2.5,.4);\draw[otGreenDark,->](4.5,0)--(4.5,-.72);
\draw[ray](-2.5,.4)--(0,.4)--(4.5,-.72)--(7,-1.3422)--(9.5,-.6222);
\draw[raytwo](-2.5,.4)--(0,0)--(4.5,-.72)--(7,-1.12)--(9.5,-.4);
\foreach \x/\t in {-2.5/A,-1.8/F_1,0/O_1,1.8/F'_1,4.5/F_2,7/O_2,9.5/F'_2}{\node[lab,below]at(\x,.05){$\t$};}
\node[lab,above]at(-2.5,.4){$B$};\node[lab,below]at(4.5,-.8){$B_1$};
\node[lab,above]at(0,1.8){Objectif};\node[lab,above]at(7,1.8){Oculaire};
\draw[otMuted,<->](1.8,2.6)--(4.5,2.6)node[midway,lab]{$\Delta$};
''')
# A geometrically consistent microscope drawing: f1=1.8, p=-3, q=4.5.
figs['microscope']=figs['microscope'].replace('(-2.5,','(-3,').replace(r'\node[lab,above]at(-2.5',r'\node[lab,above]at(-3').replace('{-2.5/A','{-3/A')
# Set object height 0.48 so that the intermediate height is -0.72.
figs['microscope']=figs['microscope'].replace(',.4)',',.48)').replace('(0,.4)','(0,.48)').replace('(7,-1.3422)','(7,-1.386667)').replace('(9.5,-.6222)','(9.5,-.666667)')
add('capteur-pluie',r'''
\fill[otNavyTint](0,0)rectangle(12,1.8);\draw[otInk](0,0)--(12,0) (0,1.8)--(12,1.8);
\draw[normal](4,-.3)--(4,3.8);\draw[ray](1.85484,0)--(4,1.8)--(6.14516,0);\draw[raytwo](4,1.8)--(7.088,3.6);
\node[lab]at(9,.9){Verre};\node[lab]at(9,2.6){Air ou eau};\node[lab]at(1.85484,-.6){Émetteur};\node[lab]at(6.14516,-.6){Détecteur};
\node[lab]at(2.4,2.7){Rayon transmis si le seuil le permet};
''')
add('dioptre-apparent',r'''
\fill[otNavyTint](-4,-3)rectangle(4,0);\draw[otInk](-4,0)--(4,0);
\fill[otNavy](0,-2.4)circle(1.5pt)node[lab,below]{$A$};\fill[otGreenDark](0,-1.6)circle(1.5pt)node[lab,left]{$A'$};
\draw[ray](0,-2.4)--(1.2,0)--(2.4,1.6);\draw[raytwo](0,-2.4)--(-1.2,0)--(-2.4,1.6);
\draw[virtual](1.2,0)--(0,-1.6);\draw[virtual](-1.2,0)--(0,-1.6);
\draw[normal](0,-3)--(0,2);\node[lab]at(-3,-.5){Eau};\node[lab]at(-3,.5){Air};
''')
for name,tex in figs.items():
    (R/(name+'.tex')).write_text(tex,encoding='utf-8')
print(f'{len(figs)} figures vectorielles produites.')
