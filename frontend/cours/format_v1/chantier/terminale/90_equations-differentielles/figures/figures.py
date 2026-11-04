# -*- coding: utf-8 -*-
"""Figures de la notion « Équations différentielles » (Terminale), style des livres.

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]
"""

FIGURES = {
# ---------------------------------------------------------------- cours
# solutions de y' = 0,5 y : C e^{0,5x} ; celle qui passe par (0 ; 1) en couleur
"cours_ay": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.6cm, xmin=-2.3, xmax=3.4, ymin=-2.7, ymax=3.8,
  xtick={-2,-1,1,2,3}, xticklabels={,,$1$,$2$,$3$}, ytick={-2,-1,1,2,3}, yticklabels={}]
  \addplot[pale, domain=-2.3:1.12] {2*exp(0.5*x)};
  \addplot[pale, domain=-2.3:3.3] {0.5*exp(0.5*x)};
  \addplot[pale, domain=-2.3:3.2] {-0.5*exp(0.5*x)};
  \addplot[pale, domain=-2.3:1.83] {-exp(0.5*x)};
  \addplot[courbe, domain=-2.3:2.5] {exp(0.5*x)};
  \pnt[otGreenDark]{0}{1}
  \node[note,anchor=west] at (axis cs:1.16,3.5) {$C=2$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.55,3.5) {$y=e^{0{,}5x}$};
  \node[note,anchor=west] at (axis cs:3.33,2.72) {$C=0{,}5$};
  \node[note,anchor=west] at (axis cs:3.25,-2.48) {$C=-0{,}5$};
  \node[note,anchor=west] at (axis cs:1.88,-2.5) {$C=-1$};
  \node[anchor=south east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt] at (axis cs:-0.04,1.04) {$1$};
  \node[anchor=south east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt] at (axis cs:-0.04,2.04) {$2$};
  \node[anchor=south east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt] at (axis cs:-0.04,3.04) {$3$};
  \node[anchor=north east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt] at (axis cs:-0.04,-1.04) {$-1$};
  \node[anchor=north east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt] at (axis cs:-0.04,-2.04) {$-2$};
\end{axis}
\end{tikzpicture}""",

# solutions de y' = -0,5 y + 2 : 4 + K e^{-0,5x} ; celle de y(0) = 0 en couleur
"cours_ayb": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=4.4cm, xmin=-0.3, xmax=8.6, ymin=-0.6, ymax=8.8,
  xtick={2,4,6,8}, ytick={2,4,6,8}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,4) -- (axis cs:8,4);
  \addplot[pale, domain=0:8] {4+4*exp(-0.5*x)};
  \addplot[pale, domain=0:8] {4+2*exp(-0.5*x)};
  \addplot[pale, domain=0:8] {4-2*exp(-0.5*x)};
  \addplot[courbe, domain=0:8] {4-4*exp(-0.5*x)};
  \pnt[otGreenDark]{0}{0}
  \node[note,anchor=west,align=left,text=otGreenDark] at (axis cs:8.15,4) {solution\\constante\\$y=4$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.7,2.25) {$y=4-4e^{-0{,}5x}$};
\end{axis}
\end{tikzpicture}""",

# café : T(t) = 20 + 70 e^{-0,1t}, 40 °C atteint en t = 10 ln 3,5
"cours_newton": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.2cm, xmin=-2, xmax=54, ymin=-6, ymax=98,
  xtick={20,30,40,50}, minor xtick={10}, grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=3pt,
  ytick={20,40,60,80}, xlabel={$t$}, ylabel={$T$}]
  \draw[asymptote] (axis cs:0,20) -- (axis cs:52,20);
  \addplot[courbe, domain=0:52] {20+70*exp(-0.1*x)};
  \guides{12.528}{40}
  \pnt{0}{90} \pnt[otGreenDark]{12.528}{40}
  \node[note,anchor=north east] at (axis cs:52,17) {pièce : $20$ °C};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:16,74) {$T(t)=20+70e^{-0{,}1t}$};
  \node[note,anchor=south west] at (axis cs:14,42) {$40$ °C au bout de $10\ln 3{,}5$ min};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1128 (circuit RC)
"ex_rc": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.9cm, xmin=-0.002, xmax=0.068, ymin=-0.4, ymax=6.2, scaled x ticks=false,
  xtick={0.01,0.02,0.03,0.04,0.05,0.06}, xticklabels={$0{,}01$,$0{,}02$,$0{,}03$,$0{,}04$,$0{,}05$,$0{,}06$},
  ytick={1,2,3,4,5}, xlabel={$t$}, ylabel={$u$}]
  \draw[asymptote] (axis cs:0,5) -- (axis cs:0.066,5);
  \addplot[courbe, domain=0:0.066] {5*(1-exp(-100*x))};
  \guidev{0.02}{4.3233} \guidev{0.05}{4.9663}
  \pnt[otGreenDark]{0.02}{4.3233} \pnt[otGreenDark]{0.05}{4.9663}
  \node[note,anchor=west] at (axis cs:0.0665,5) {$u=E=5$};
  \node[note,anchor=north west] at (axis cs:0.0215,3.8) {$u(0{,}02)\approx4{,}32$};
  \node[note,anchor=north west] at (axis cs:0.0515,4.6) {$u(5\tau)\approx4{,}97$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:0.065,0.35) {$u(t)=5\left(1-e^{-100t}\right)$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1126 (décroissance radioactive)
"ex_radioactif": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.9cm, xmin=-4, xmax=150, ymin=-60, ymax=1120,
  xtick={20,40,60,80,100,120,140}, ytick={100,500,1000}, yticklabels={$100$,$500$,$1\,000$},
  xlabel={$t$}, ylabel={$N$}]
  \addplot[courbe, domain=0:145] {1000*exp(-0.02*x)};
  \guides{34.657}{500} \guides{115.13}{100}
  \pnt[otGreenDark]{34.657}{500} \pnt[otGreenDark]{115.13}{100}
  \node[note,anchor=south west] at (axis cs:37,525) {demi-vie : $T\approx34{,}66$};
  \node[note,anchor=south west] at (axis cs:117,125) {$t\approx115{,}13$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:58,900) {$N(t)=1\,000\,e^{-0{,}02t}$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1124 (mélange)
"ex_melange": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.9cm, xmin=-6, xmax=265, ymin=-3, ymax=58,
  xtick={50,100,150,200,250}, ytick={10,20,30,40,50}, xlabel={$t$}, ylabel={$Q$}]
  \draw[asymptote] (axis cs:0,50) -- (axis cs:255,50);
  \addplot[courbe, domain=0:255] {50*(1-exp(-0.02*x))};
  \guides{30}{22.559}
  \pnt[otGreenDark]{30}{22.559}
  \node[note,anchor=west] at (axis cs:257,50) {$Q=50$};
  \node[note,anchor=north west] at (axis cs:36,20.5) {$Q(30)\approx22{,}56$};
  \node[etiq,text=otNavy,anchor=north east] at (axis cs:252,34) {$Q(t)=50\left(1-e^{-0{,}02t}\right)$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1125 (Newton)
"ex_newton": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.1cm, xmin=-2, xmax=54, ymin=-6, ymax=88,
  xtick={10,20,30,40,50}, ytick={20,40,60,80}, xlabel={$t$}, ylabel={$T$}]
  \draw[asymptote] (axis cs:0,20) -- (axis cs:52,20);
  \draw[seuil] (axis cs:0,25) -- (axis cs:52,25);
  \addplot[courbe, domain=0:52] {20+60*exp(-0.1*x)};
  \guides{10}{42.073} \guidev{24.849}{25}
  \pnt{0}{80} \pnt[otGreenDark]{10}{42.073} \pnt[otGreenDark]{24.849}{25}
  \node[note,anchor=south west] at (axis cs:52.5,25.5) {$T=25$};
  \node[note,anchor=north west] at (axis cs:52.5,19.5) {$T=20$};
  \node[note,anchor=south west] at (axis cs:11.5,44.5) {$T(10)\approx42{,}07$};
  \node[note,anchor=south west] at (axis cs:26,28.5) {$t\approx24{,}85$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:21,72) {$T(t)=20+60e^{-0{,}1t}$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1131 (logistique)
"ex_logistique": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.9cm, xmin=-2, xmax=86, ymin=-50, ymax=1150,
  xtick={20,40,60,80}, ytick={200,400,600,800,1000}, yticklabels={$200$,$400$,$600$,$800$,$1\,000$},
  xlabel={$t$}, ylabel={$P$}]
  \draw[asymptote] (axis cs:0,1000) -- (axis cs:82,1000);
  \addplot[courbe, domain=0:82] {1000/(1+9*exp(-0.1*x))};
  \guides{20}{450.85}
  \pnt{0}{100} \pnt[otGreenDark]{20}{450.85}
  \node[note,anchor=west] at (axis cs:83,1000) {$P=1\,000$};
  \node[note,anchor=north west] at (axis cs:23,415) {$P(20)\approx451$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:44,720) {$P(t)=\dfrac{1\,000}{1+9e^{-0{,}1t}}$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- cours IV : y' = 2y - 4x
# solutions 2x + 1 + C e^{2x} ; solution particulière y_p = 2x + 1 (droite) ; y(0) = 0 en couleur
"cours_ayf": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.8cm, xmin=-2.6, xmax=1.4, ymin=-4.6, ymax=4.6,
  xtick={-2,-1,1}, xticklabels={}, ytick={-4,-2,2,4}, yticklabels={$-4$,$-2$,,$4$}]
  \addplot[pale, domain=-2.5:0.22] {2*x+1+2*exp(2*x)};
  \addplot[pale, domain=-2.5:0.72] {2*x+1+0.5*exp(2*x)};
  \addplot[pale, domain=-2.5:1.2] {2*x+1-0.5*exp(2*x)};
  \addplot[pale, domain=-2.5:0.59] {2*x+1-2*exp(2*x)};
  \addplot[otGreenDark, line width=1.1pt, dash pattern=on 5pt off 2.5pt, domain=-2.5:1.3] {2*x+1};
  \addplot[courbe, domain=-2.5:0.98] {2*x+1-exp(2*x)};
  \pnt[otGreenDark]{0}{0}
  \draw[courbe] (axis cs:-2.45,4.0) -- (axis cs:-2.05,4.0);
  \node[anchor=west,text=otNavy] at (axis cs:-2.0,4.0) {$y=2x+1-e^{2x}$};
  \draw[otGreenDark, line width=1.1pt, dash pattern=on 5pt off 2.5pt] (axis cs:-2.45,3.0) -- (axis cs:-2.05,3.0);
  \node[anchor=west,text=otGreenDark] at (axis cs:-2.0,3.0) {$y_p(x)=2x+1$};
  \draw[pale] (axis cs:-2.45,2.0) -- (axis cs:-2.05,2.0);
  \node[anchor=west,text=otMuted] at (axis cs:-2.0,2.0) {autres solutions};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1132 : solutions de y' = 2y + 4
"ex_verif": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6cm, height=4.6cm, xmin=-3.2, xmax=1.75, ymin=-4.6, ymax=4.6,
  xtick={-3,-2,-1,1}, ytick={-4,-2,2,4}]
  \draw[seuil] (axis cs:-3.2,-2) -- (axis cs:1.05,-2);
  \addplot[pale, domain=-3.2:0.94] {exp(2*x)-2};
  \addplot[pale, domain=-3.2:0.47] {-exp(2*x)-2};
  \addplot[pale, domain=-3.2:-0.5] {-3*exp(2*x)-2};
  \addplot[courbe, domain=-3.2:0.39] {3*exp(2*x)-2};
  \pnt[otGreenDark]{0}{1}
  \node[note,anchor=west,text=otOrange!80!black] at (axis cs:1.08,-2) {$y=-2$};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:-0.3,2.6) {$y=3e^{2x}-2$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1123 : P(t) = 5 000 e^{0,03t}
"ex_population": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.2cm, xmin=-1.5, xmax=42, ymin=-600, ymax=17500, scaled y ticks=false,
  xtick={10,20,30,40}, ytick={5000,10000,15000}, yticklabels={$5\,000$,$10\,000$,$15\,000$},
  xlabel={$t$}, ylabel={$P$}]
  \addplot[courbe, domain=0:40] {5000*exp(0.03*x)};
  \guides{10}{6749.3} \guides{23.105}{10000}
  \pnt{0}{5000} \pnt[otGreenDark]{10}{6749.3} \pnt[otGreenDark]{23.105}{10000}
  \node[note,anchor=north west] at (axis cs:11,6300) {$P(10)\approx6\,749$};
  \node[note,anchor=north west] at (axis cs:24.2,9500) {$t\approx23{,}1$ ans};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:27,14200) {$P(t)=5\,000\,e^{0{,}03t}$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1127 : P(t) = 3 500 e^{0,02t} - 2 500
"ex_immigration": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.2cm, xmin=-1.2, xmax=32, ymin=-120, ymax=3100, scaled y ticks=false,
  xtick={5,10,15,20,25,30}, ytick={1000,2000,3000}, yticklabels={$1\,000$,$2\,000$,$3\,000$},
  xlabel={$t$}, ylabel={$P$}]
  \addplot[courbe, domain=0:30] {3500*exp(0.02*x)-2500};
  \guides{5}{1368.1} \guides{12.566}{2000}
  \pnt{0}{1000} \pnt[otGreenDark]{5}{1368.1} \pnt[otGreenDark]{12.566}{2000}
  \node[note,anchor=north west] at (axis cs:5.6,1290) {$P(5)\approx1\,368$};
  \node[note,anchor=north west] at (axis cs:13.3,1930) {$t\approx12{,}57$ ans};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.5,2950) {$P(t)=3\,500\,e^{0{,}02t}-2\,500$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1129 : proportion restante e^{-λt}, t en milliards d'années
"ex_uranium": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4cm, xmin=-0.4, xmax=10.8, ymin=-6, ymax=112,
  xtick={1,2,4,6,8,10}, ytick={25,50,75,100}, yticklabels={$25\,\%$,$50\,\%$,$75\,\%$,$100\,\%$},
  xlabel={$t$}, ylabel={$\frac{N}{N_0}$}]
  \addplot[courbe, domain=0:10.3] {100*exp(-0.154644*x)};
  \guides{1}{85.67} \guides{4.4823}{50}
  \pnt{0}{100} \pnt[otGreenDark]{1}{85.67} \pnt[otGreenDark]{4.4823}{50}
  \node[note,anchor=south west] at (axis cs:1.3,87) {$85{,}7\,\%$ au bout de $1$ milliard d’années};
  \node[note,anchor=south west] at (axis cs:4.75,51) {demi-vie $\approx4{,}48$ milliards d’années};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1130 : T(t) = 25 + 75 e^{-0,02t}
"ex_temperature": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.2cm, xmin=-5, xmax=196, ymin=-6, ymax=112,
  xtick={60,120,180}, minor xtick={30,90,150}, grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=3pt,
  ytick={25,50,75,100}, xlabel={$t$}, ylabel={$T$}]
  \draw[asymptote] (axis cs:0,25) -- (axis cs:188,25);
  \draw[seuil] (axis cs:0,30) -- (axis cs:188,30);
  \addplot[courbe, domain=0:188] {25+75*exp(-0.02*x)};
  \guides{60}{47.59} \guidev{135.4}{30}
  \pnt{0}{100} \pnt[otGreenDark]{60}{47.59} \pnt[otGreenDark]{135.4}{30}
  \node[note,anchor=south west] at (axis cs:63,50) {$T(60)\approx47{,}59$};
  \node[note,anchor=west] at (axis cs:137,9) {$t\approx135{,}4$};
  \node[note,anchor=west] at (axis cs:189,32) {$T=30$};
  \node[note,anchor=west] at (axis cs:189,22) {$T=25$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:70,86) {$T(t)=25+75e^{-0{,}02t}$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- nouveau-1 : y' = -0,5y + 1
"en1_famille": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-0.5, xmax=7.6, ymin=-4.2, ymax=6.8,
  xtick={1,2,3,4,5,6,7}, ytick={-4,-2,2,4,6}]
  \addplot[pale, domain=0:7.3] {2+4*exp(-0.5*x)};
  \addplot[pale, domain=0:7.3] {2+2*exp(-0.5*x)};
  \addplot[pale, domain=0:7.3] {2-2*exp(-0.5*x)};
  \addplot[pale, domain=0:7.3] {2-4*exp(-0.5*x)};
  \pnt{0}{4} \pnt{2}{0}
  \node[anchor=south west,text=otNavy] at (axis cs:0.12,4.1) {$A$};
  \node[anchor=north west,text=otNavy] at (axis cs:2.2,-0.2) {$B$};
\end{axis}
\end{tikzpicture}""",

"en1_famille_corr": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-0.5, xmax=7.6, ymin=-4.2, ymax=6.8,
  xtick={1,2,3,4,5,6,7}, ytick={-4,-2,2,4,6}]
  \addplot[pale, domain=0:7.3] {2+4*exp(-0.5*x)};
  \addplot[pale, domain=0:7.3] {2-2*exp(-0.5*x)};
  \addplot[pale, domain=0:7.3] {2-4*exp(-0.5*x)};
  \addplot[otGreenDark, line width=1pt, dash pattern=on 5pt off 2.5pt, domain=0:7.3] {2};
  \addplot[otGreenDark, line width=1.35pt, domain=0:7.3] {2+2*exp(-0.5*x)};
  \addplot[otGreenDark, line width=1.35pt, domain=0:7.3] {2-2*exp(1-0.5*x)};
  \pnt{0}{4} \pnt{2}{0}
  \node[anchor=south west,text=otNavy] at (axis cs:0.12,4.1) {$A$};
  \node[anchor=north west,text=otNavy] at (axis cs:2.2,-0.2) {$B$};
  \node[text=otGreenDark] at (axis cs:1.0,3.78) {$f$};
  \node[anchor=north west,text=otGreenDark] at (axis cs:0.75,-1.9) {$g$};
  \node[anchor=west,text=otGreenDark] at (axis cs:7.4,2) {$y=2$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- nouveau-2 : f(x) = (2x + 1)e^{-x}
"en2_etude": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4cm, xmin=-0.4, xmax=7.4, ymin=-0.25, ymax=1.62,
  xtick={1,2,3,4,5,6,7}, ytick={0.5,1,1.2131}, yticklabels={$0{,}5$,$1$,}]
  \addplot[courbe, domain=0:7] {(2*x+1)*exp(-x)};
  \guides{0.5}{1.2131}
  \pnt{0}{1} \pnt[otGreenDark]{0.5}{1.2131}
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:0.62,1.22) {$f\left(\frac{1}{2}\right)=\frac{2}{\sqrt{e}}\approx1{,}21$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.6,0.5) {$f(x)=(2x+1)e^{-x}$};
\end{axis}
\end{tikzpicture}""",
}

XLAB = {
    "cours_ayf": [(-2, "c", "-2"), (-1, "h", "-1"), (1, "h", "1")],
    "cours_newton": [(12.528, "c", r"12{,}5")],
}
