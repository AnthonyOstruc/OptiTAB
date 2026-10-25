"""Constructions corrigées originales, ajoutées à la relecture des consignes."""
from pathlib import Path
import json, math, re
ROOT=Path(__file__).resolve().parent

def plot(xlabel,ylabel,curves,xmin,xmax,ymin,ymax,extra='',legend=''):
    lines=[r'\begin{tikzpicture}',r'\begin{axis}[otMesures,otAxesBout,otLecture,width=113mm,height=47mm,'+
           f'xmin={xmin},xmax={xmax},ymin={ymin},ymax={ymax},'+
           'xlabel={'+xlabel+'},ylabel={'+ylabel+'},scaled ticks=false,xticklabel style={/pgf/number format/fixed,/pgf/number format/precision=3},yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=3},legend style={font=\\small,at={(0.5,1.03)},anchor=south,legend columns=3,draw=none}]']
    for label,style,coords in curves:
        lines.append('\\addplot['+style+'] coordinates {'+' '.join(f'({x:.8g},{y:.8g})' for x,y in coords)+'};')
        if label:lines.append('\\addlegendentry{'+label+'}')
    lines.extend([extra,r'\end{axis}',r'\end{tikzpicture}'])
    return '\n'.join(lines)

def circle(kind):
    # M à droite du centre ; mouvement antihoraire. Échelles de vecteurs distinctes.
    return r'''\begin{tikzpicture}[x=1cm,y=1cm]
\draw[otRule] (0,0) circle (1.15);
\fill[otNavy] (0,0) circle (.04) node[pcLegende,below] {O};
\fill[otNavy] (1.15,0) circle (.05) node[pcLegende,below right] {M};
\draw[pcVitesse] (1.15,0) -- (1.15,1.45) node[pcLegende,above] {$\vec v$, $\vec u_\mathrm t$};
\draw[pcForce] (1.15,0) -- (-.15,0) node[pcLegende,above left] {$\vec a$, $\vec u_\mathrm n$};
\node[pcLegende,align=left,anchor=west] at (2.1,.3) {Vitesse tangente\\Accélération vers le centre};
\end{tikzpicture}'''

def produire():
    figs={};checks=[]
    coords=[(0,1),(1,10.1),(2,35)]
    figs['03-ex07-cor']=plot(r'$V/V_\mathrm E$',r'$\sigma$ (u.a.)',[('', 'otNavy,line width=1pt',coords)],0,2.1,0,39,
          r'\draw[otGreenDark,dashed] (axis cs:1,0)--(axis cs:1,32);\node[pcLegende,anchor=south] at (axis cs:1,33) {équivalence};')
    checks.append(abs((35-10.1)/(10.1-1)-24.9/9.1)<1e-10)
    xs=[-3+i*.05 for i in range(121)]
    figs['09-ex11-cor']=plot(r'$\mathrm{pH}-\mathrm{p}K_\mathrm a$',r'proportion (\%)',[
      ('AH','otNavy,line width=1pt',[(x,100/(1+10**x)) for x in xs]),
      (r'$\mathrm{A^-}$','otGreenDark,line width=1pt',[(x,100/(1+10**(-x))) for x in xs])],-3,3,0,104,
      r'\draw[otMuted,dashed] (axis cs:0,0)--(axis cs:0,100);')
    figs['09-ex12-cor']=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\draw[otMuted,-{Stealth}] (0,0)--(10,0) node[pcLegende,right] {pH};
\draw[otNavy] (4,-.15)--(4,.15);\node[pcLegende,below] at (4,-.2) {$\mathrm pK_a=6{,}1$};
\node[pcLegende,above] at (2,.2) {$\ce{CO2,H2O}$ prédomine};
\node[pcLegende,above] at (7.2,.2) {$\ce{HCO3-}$ prédomine};
\fill[otGreenDark] (7.5,0) circle (.06);\node[pcLegende,below] at (7.5,-.2) {sang : pH 7,4};
\end{tikzpicture}'''
    figs['13-ex04-cor']=circle('manège')
    figs['16-ex12-cor']=circle('hubble')
    figs['13-ex08-cor']=plot('$t$ (s)',r'$v_y$ (m$\cdot$s$^{-1}$)',[('', 'otNavy,line width=1pt',[(0,0),(.25,2.45)])],0,.27,0,2.8)
    figs['13-ex09-cor']=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\fill[otNavy] (0,0) circle (.05) node[pcLegende,below right] {M};
\draw[pcVitesse] (0,0)--(0,1.6) node[pcLegende,right] {$\vec v$};
\draw[otMuted,dashed,-{Stealth}] (0,0)--(-3.2,0) node[pcLegende,below] {$a_\mathrm n=3{,}2$};
\draw[otMuted,dashed,-{Stealth}] (0,0)--(0,1.25) node[pcLegende,left] {$a_\mathrm t=1{,}25$};
\draw[otMuted,dashed] (-3.2,0)--(-3.2,1.25)--(0,1.25);
\draw[pcForce] (0,0)--(-3.2,1.25) node[pcLegende,above left] {$\vec a$};
\draw[otGreenDark] (-.7,0) arc[start angle=180,end angle=158.66,radius=.7];
\node[pcLegende] at (-1.2,.22) {$21^\circ$};
\node[pcLegende,align=left,anchor=west] at (1,.6) {Vers le centre : $\vec u_\mathrm n$\\Vers l'avant : $\vec u_\mathrm t$\\Accélérations en m$\cdot$s$^{-2}$};
\end{tikzpicture}'''
    figs['13-ex11-cor']=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\draw[otRule] (0,0) circle (1.6);
\draw[otMuted,-{Stealth}] (-1.9,0)--(2,0) node[pcLegende,right] {$x$};
\draw[otMuted,-{Stealth}] (0,-1.8)--(0,1.9) node[pcLegende,above] {$y$};
\fill[otNavy] (0,0) circle (.04) node[pcLegende,below left] {O};
\fill[otNavy] (1.1314,1.1314) circle (.05) node[pcLegende,above right] {$M(1{,}41;1{,}41)$ m};
\draw[otMuted,dashed] (1.1314,0)--(1.1314,1.1314)--(0,1.1314);
\draw[pcForce] (1.1314,1.1314)--(.4,.4) node[pcLegende,left] {$\vec a$};
\node[pcLegende,align=left,anchor=west] at (2.6,-.65) {$t=0{,}50$ s ; angle $45^\circ$\\$a\simeq4{,}93$ m$\cdot$s$^{-2}$\\Vecteur dirigé vers O};
\end{tikzpicture}'''
    figs['14-ex03-cor']=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\fill[otNavyTint] (-.45,-.25) rectangle (.45,.25);
\draw[otRule] (-2,-.3)--(3,-.3);
\fill[otNavy] (0,0) circle (.04) node[pcLegende,below right] {G};
\draw[pcForce] (0,0)--(0,1.2) node[pcLegende,above] {$\vec N$};
\draw[pcForce] (0,0)--(0,-1.2) node[pcLegende,below] {$\vec P$};
\draw[pcForce] (0,0)--(-1.5,0) node[pcLegende,above] {$\vec f$};
\draw[pcVitesse] (1.1,.65)--(2.8,.65) node[pcLegende,above] {$\vec v$};
\node[pcLegende,align=left,anchor=west] at (3.4,.2) {Forces représentées sans échelle\\$N=P$ ; frottement vers l'arrière};
\end{tikzpicture}'''
    x=[0,.120,.240,.360,.480,.600,.720];z=[1,1.152,1.289,1.409,1.514,1.604,1.677]
    ec=[];ep=[];em=[]
    for i in range(1,6):
        vx=(x[i+1]-x[i-1])/.08;vz=(z[i+1]-z[i-1])/.08
        c=.5*.058*(vx*vx+vz*vz);p=.058*9.81*z[i];t=.04*i
        ec.append((t,c));ep.append((t,p));em.append((t,c+p))
    checks.append(max(y for _,y in em)-min(y for _,y in em)<.015)
    figs['15-ex09-cor']=plot('$t$ (s)','énergie (J)',[('$E_c$','otNavy,mark=*',ec),('$E_{pp}$','otGreenDark,mark=square*',ep),('$E_m$','otOrange,mark=triangle*',em)],.02,.22,0,1.5)
    planets=[(.387,.241),(.723,.615),(1,1),(1.524,1.881),(5.203,11.86),(9.537,29.45)]
    figs['16-ex07-cor']=plot('$a^3$ (ua$^3$)','$T^2$ (an$^2$)',[('', 'otNavy,only marks,mark=*',[(a**3,t*t) for a,t in planets]),('', 'otGreenDark,dashed',[(0,0),(900,900)])],0,930,0,930)
    figs['18-ex08-cor']=plot('$1/V$ (mL$^{-1}$)','$p$ (hPa)',[('', 'otNavy,only marks,mark=*',[(1/v,p) for v,p in zip([60,50,40,30,20],[1013,1218,1521,2024,3035])]),('', 'otGreenDark,dashed',[(0,0),(.052,60800*.052)])],0,.054,0,3400)
    figs['18-ex09-cor']=plot(r'$\theta$ ($^\circ$C)','$p$ (hPa)',[('', 'otNavy,only marks,mark=*',list(zip([10,30,50,70,90],[881,944,1005,1068,1130]))),('', 'otGreenDark,dashed',[(-273.05,0),(100,1161.125)])],-290,110,0,1250,
      r'\node[pcLegende,anchor=west] at (axis cs:-255,120) {extrapolation du modèle};')
    ts=[10*k for k in range(361)]
    figs['20-ex08-cor']=plot('$t$ (min)',r'$T$ ($^\circ$C)',[('Euler','otNavy,line width=1pt',[(t/60,20+60*(1-10/1500)**(t/10)) for t in ts]),('exact','otGreenDark,dashed',[(t/60,20+60*math.exp(-t/1500)) for t in ts])],0,60,18,84)
    figs['22-ex02-cor']=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\draw[otNavy,line width=2pt] (0,-1.3)--(0,-.12) (0,.12)--(0,1.3);
\draw[otNavy,line width=1.2pt] (6,-1.4)--(6,1.4);
\draw[otMuted,dashed] (-1,0)--(6.3,0);
\draw[otNavy,line width=.8pt,-{Stealth}] (0,0)--(6,.9);\draw[otNavy,line width=.8pt,-{Stealth}] (0,0)--(6,-.9);
\draw[otGreenDark] (1,0) arc[start angle=0,end angle=8.53,radius=1];
\node[pcLegende] at (1.5,.28) {$\theta$};
\draw[otMuted,{Stealth}-{Stealth}] (6.4,-.9)--(6.4,.9) node[midway,right,pcLegende] {$L$};
\draw[otMuted,{Stealth}-{Stealth}] (0,-1.7)--(6,-1.7) node[midway,below,pcLegende] {$D$};
\node[pcLegende,above] at (0,1.4) {fente};\node[pcLegende,above] at (6,1.4) {écran};
\end{tikzpicture}'''
    ts=[k/200 for k in range(201)]
    figs['22-ex08-cor']=plot('$t$ (s)','signal (u.a.)',[
      ('$s_1$','otNavy,line width=.8pt',[(t,math.sin(2*math.pi*t)) for t in ts]),
      ('$s_2$','otMuted,dashed',[(t,math.cos(2*math.pi*t)) for t in ts]),
      ('somme','otGreenDark,line width=1.1pt',[(t,math.sin(2*math.pi*t)+math.cos(2*math.pi*t)) for t in ts])],0,1,-1.6,1.6)
    figs['26-ex06-cor']=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\draw[otNavy] (0,.15)--(0,1.2)--(4,1.2)--(4,.35) (4,-.35)--(4,-1.2)--(0,-1.2)--(0,-.15);
\draw[otNavy,line width=1pt] (-.4,.15)--(.4,.15) (-.4,-.15)--(.4,-.15);
\draw[otNavy,fill=white] (3.8,-.35) rectangle (4.2,.35);
\node[pcLegende,left] at (-.5,0) {$C$};\node[pcLegende,right] at (4.3,0) {$R$};
\node[pcLegende,left] at (0,.5) {$+$};\node[pcLegende,left] at (0,-.5) {$-$};
\draw[pcVitesse] (1,1.2)--(2.5,1.2) node[midway,above,pcLegende] {$i$};
\draw[pcForce] (-1,-.8)--(-1,.8) node[midway,left,pcLegende] {$u_C$};
\draw[pcForce] (5,-.8)--(5,.8) node[midway,right,pcLegende] {$u_R$};
\node[pcLegende,align=left,anchor=west] at (6,.1) {Décharge : $i>0$\\$u_R=u_C$\\$i=-C\,\mathrm du_C/\mathrm dt$};
\end{tikzpicture}'''
    ts=[k*.02 for k in range(231)]
    figs['26-ex08-cor']=plot('$t$ (s)','$u_C$ (V)',[('Euler','otNavy,line width=1pt',[(t,5*(1-(1-.001)**(t/.001))) for t in ts]),('exact','otGreenDark,dashed',[(t,5*(1-math.exp(-t))) for t in ts])],0,4.7,0,5.3)
    assert all(checks)
    for name,content in figs.items():
        (ROOT/'figures'/('rev-'+name+'.tex')).write_text('% Illustration originale OptiTAB, révision 24/10/2026\n'+content+'\n',encoding='utf-8')
    (ROOT/'build/revision-figures.json').write_text(json.dumps({'figures':list(figs),'calculs':len(checks)},ensure_ascii=False,indent=2),encoding='utf-8')
    print(len(figs),'figures de correction produites')

if __name__=='__main__':produire()
