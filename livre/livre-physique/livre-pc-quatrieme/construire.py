"""Édition complète de Quatrième, dans la charte de Terminale."""
from pathlib import Path
import json, shutil, re
from donnees import charger, THEMES

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def write(name, text):
    p=HERE/name; p.parent.mkdir(parents=True,exist_ok=True)
    if p.suffix=='.tex' and p.name!='quatrieme-charte.tex':
        text=re.sub(r'(?<!\\)%',r'\\%',text)
        text=text.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
    p.write_text(text,encoding='utf8')

def qs(items):
    return '\\begin{questions}\n'+''.join('\\item '+q+'\n' for q in items)+'\\end{questions}\n'

def box(title,body,kind='definition'):
    return rf'\begin{{pcEncadre}}{{{kind}}}{{{title}}}'+body+'\\end{pcEncadre}\n'

def figure(name,caption=''):
    return rf'\pcFigure{{figures/{name}.pdf}}{{{caption}}}'+'\n' if name else ''

def figure_ex(name,caption='',exact=False):
    command='pcFigureExact' if exact else 'pcFigureEx'
    return rf'\{command}{{figures/{name}.pdf}}{{{caption}}}'+'\n' if name else ''

def solution_ex(ex):
    s=qs(ex.reponses)
    if ex.methode:s+=r'\par\smallskip\noindent\textbf{Pour comprendre.}\enspace '+ex.methode+r'\par'+'\n'
    return s+figure_ex(ex.figure_correction,ex.legende_correction,ex.correction_exacte)

def page(title,subtitle='',label=''):
    return rf'\pcPage{{{title}}}{{{subtitle}}}'+ ('\n'+rf'\phantomsection\label{{{label}}}' if label else '')+'\n'

def build():
    chs=charger()
    for d in ['figures','images','chapitres','corriges','build','annexes']:(HERE/d).mkdir(exist_ok=True)
    shutil.copy2(ROOT/'livre-pc-terminale/optitab-livre.sty',HERE/'optitab-livre.sty')
    for n in ['logo-blanc.png','logo-couleur.png']:shutil.copy2(ROOT.parent/'livre-maths/livre-terminale/images'/n,HERE/'images'/n)
    charte=(ROOT/'livre-pc-cinquieme/cinquieme-charte.tex').read_text(encoding='utf8')
    charte=charte.replace('Cinquième','Quatrième').replace('L’essentiel','Le cours')
    # Aucun redimensionnement de page de texte : seules les figures sont ajustées.
    charte=charte.replace(r'\adjincludegraphics[max width=\linewidth]',r'\adjincludegraphics[max width=\linewidth,max height=57mm]')
    charte+=r'''
\renewcommand{\otTitreLivre}{Physique-chimie}
\renewcommand{\otSousTitre}{Cours et exercices corrigés}
\clubpenalty=10000\widowpenalty=10000\displaywidowpenalty=10000
\renewcommand{\pcPage}[2]{\clearpage\markright{#1}\otPageTitre{#1}{#2}\vspace{-4mm}}
\renewcommand{\otFootText}[1]{{\otLight\fontsize{6.5}{8}\selectfont\color{otMuted}#1}}
\fancypagestyle{otMain}{\fancyhf{}\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[LE]{\otHeadNum\hspace{.8em}\otHeadText{\leftmark}}
\fancyhead[RO]{\otHeadText{\rightmark}\hspace{.8em}\otHeadNum}
\fancyfoot[LE]{\otThumb\otFootNum\hspace{1.2em}\otFootText{OptiTAB · Quatrième}}
\fancyfoot[RO]{\otThumb\otFootText{Physique-chimie · Cours et exercices corrigés}\hspace{1.2em}\otFootNum}}
\patchcmd{\otEntete}{\addvspace{6.5mm}}{\addvspace{4mm}}{}{}
\patchcmd{\otEntete}{\addvspace{6.5mm}}{\addvspace{4mm}}{}{}
\patchcmd{\otEntete}{\otBesoinPlace{9\baselineskip}}{\otBesoinPlace{5\baselineskip}}{}{}
\newcommand{\unite}[1]{\ensuremath{\,\symup{#1}}}
\setlength{\emergencystretch}{2em}
\Urlmuskip=0mu plus 1mu\relax
\newcommand{\pcAnnexe}[2]{\clearpage\gdef\otChapNum{0}\gdef\otHeadTag{}\markboth{#1}{#1}\pcPage{#1}{#2}}
\newcommand{\pcDefiTitre}[2]{\otEntete{otNavy}{D#1}{#2}{3}{\otRenvoi{Corrigé}{cor-defi-#1}}}
\newcommand{\pcSolutionDefi}[2]{\otEntete{otGreen}{D#1}{#2}{0}{\otRenvoi{Énoncé}{defi-ex-#1}}}
\newcommand{\pcGrille}{\par\vspace{4mm}\begin{tikzpicture}\draw[step=5mm,otRule!70,line width=.3pt] (.2pt,0) grid (\dimexpr\linewidth-.2pt\relax,60mm);\end{tikzpicture}}
\newcommand{\pcGrilleCourte}{\par\vspace{4mm}\begin{tikzpicture}\draw[step=5mm,otRule!70,line width=.3pt] (.2pt,0) grid (\dimexpr\linewidth-.2pt\relax,30mm);\end{tikzpicture}}
\newcommand{\pcRepere}[2]{\par\noindent\hyperref[#1]{{\otMedium\fontsize{9}{12}\selectfont\color{otGreenDark}#2 · p.~\pageref*{#1}}}\par\vspace{2mm}}
\newcommand{\pcMot}[1]{{\otSemi\color{otNavy}#1}}
\newcommand{\pcCase}{\tikz[baseline=-.5mm]\draw[otMuted,line width=.4pt] (0,0) rectangle (2mm,2mm);}
\newcommand{\pcFigureEx}[2]{\par\vspace{1.5mm}\noindent\begin{minipage}{\linewidth}\centering\adjincludegraphics[max width=\linewidth,max height=46mm]{#1}\par\ifstrempty{#2}{}{\vspace{1mm}{\otLight\fontsize{8.7}{11.5}\selectfont\color{otMuted}\raggedright #2\par}}\end{minipage}\par\vspace{1.5mm}}
\newcommand{\pcFigureExact}[2]{\par\vspace{1.5mm}\noindent\begin{minipage}{\linewidth}\centering\includegraphics{#1}\par\ifstrempty{#2}{}{\vspace{1mm}{\otLight\fontsize{8.7}{11.5}\selectfont\color{otMuted}\raggedright #2\par}}\end{minipage}\par\vspace{1.5mm}}
\renewcommand{\corrigesChapitre}[2]{\clearpage\gdef\otChapNum{#1}\gdef\otChapTitle{#2}\gdef\otHeadTag{\otTwoDigits{#1}}
\global\otCorrigestrue\global\otSoupletrue\gdef\otAccent{otGreenDark}\markboth{Solutions · #2}{Solutions · #2}
\phantomsection\label{corchap-#1}\pdfbookmark[1]{#1 · #2}{bm-corchap-#1}\otPageTitre{Corrigés · #1}{#2}
\fontsize{11}{14}\selectfont\setlength{\parskip}{1mm}\setlist[questions,1]{label=\otLabel{\arabic*.},leftmargin=1.7em,labelsep=.45em,itemsep=.25em,topsep=.2em,parsep=.1em}}
\sisetup{locale=FR,per-mode=symbol}
'''
    write('quatrieme-charte.tex',charte)
    from liminaires import COUVERTURE, debut
    from annexes import documents
    write('couverture.tex',COUVERTURE)
    write('liminaires.tex',debut(chs))
    for c in chs:
        n=c.numero
        text=rf'\begin{{ouverture}}[college{c.theme}]{{{n}}}{{{c.titre}}}{{Partie {c.theme} · {THEMES[c.theme-1][2]}}}{{{c.question}}}'+'\n'
        text+=''.join(r'\objectif{'+x+'}\n' for x in c.objectifs)
        text+=''.join(r'\prerequis{'+x+'}\n' for x in c.prerequis)
        text+='\\end{ouverture}\n'+page('Le cours',c.titre,f'ess-{n}')
        for j,(title,body,fig,caption) in enumerate(c.lecons,1):
            if j==3:text+='\\clearpage\n'
            text+=rf'\essSection{{{j}}}{{{title}}}'+'\n'+body+'\\par\n'+figure(fig,caption)
        text+=box('Un exemple expliqué',c.exemple,'method')
        text+=page('Expérimenter et retenir',c.titre,f'activite-{n}')
        text+=box('Investigation en classe',c.activite,'method')
        text+=r'\pcSousTitre{Ce que je dois savoir expliquer}'+qs(c.bilan)
        text+=box('Une erreur à éviter',c.erreur,'attention')
        text+=r'\pcRepere{cor-activite-'+str(n)+r'}{Pistes pour l’investigation}\pcGrille'
        text+='\n'
        for j,ex in enumerate(c.exercices,1):
            if j in [1,6,11]:
                level=(j-1)//5+1;rub=['Je démarre','Je m’entraîne','Je raisonne'][level-1]
                text+='\\clearpage\\markright{'+rub+'}\n\\rubrique{'+rub+'}\n'
            text+='\\par\\noindent\\begin{minipage}{\\linewidth}\n'
            text+=rf'\begin{{exercice}}[{(j-1)//5+1}]{{{ex.titre}}}'+'\n'
            if ex.document:text+=box('Document',ex.document)
            text+=figure_ex(ex.figure,ex.legende_figure,ex.figure_exacte)+qs(ex.questions)+'\\end{exercice}\n\\end{minipage}\n'
        text+=page('Défi du chapitre',c.titre,f'defi-ex-{n}')
        text+=rf'\pcDefiTitre{{{n}}}{{{c.defi.titre}}}'+'\n'
        if c.defi.document:text+=box('Situation',c.defi.document)
        text+=figure_ex(c.defi.figure,c.defi.legende_figure,c.defi.figure_exacte)+qs(c.defi.questions)+r'\pcGrille'+'\n'
        write(f'chapitres/{n:02}.tex',text)
        corr=rf'\corrigesChapitre{{{n}}}{{{c.titre}}}'+'\n'
        for j,ex in enumerate(c.exercices,1):
            corr+='\\par\\noindent\\begin{minipage}{\\linewidth}\n'
            corr+=rf'\begin{{corrige}}{{{j}}}{{{ex.titre}}}'+'\n'+solution_ex(ex)+'\\end{corrige}\n\\end{minipage}\n'
        corr+='\\par\\noindent\\begin{minipage}{\\linewidth}\n'+rf'\phantomsection\label{{cor-defi-{n}}}\pcSolutionDefi{{{n}}}{{{c.defi.titre}}}'+solution_ex(c.defi)+'\\end{minipage}\n'
        corr+='\\par\\noindent\\begin{minipage}{\\linewidth}\n'+rf'\phantomsection\label{{cor-activite-{n}}}\pcSousTitre{{Pistes pour l’investigation}}'+'\n'+ACTIVITES[n]+'\\par\\end{minipage}\n'
        write(f'corriges/{n:02}.tex',corr)
    write('plan.tex',''.join(rf'\otPlanChap{{{c.numero}}}{{{c.titre}}}{{}}'+'\n' for c in chs))
    write('annexes.tex',documents(chs))
    main=r'''\documentclass[11pt,twoside,openany]{book}
\usepackage{optitab-livre}
\usepackage[version=4]{mhchem}
\usepackage{siunitx}
\usepackage{adjustbox}
\input{quatrieme-charte}
\hypersetup{pdftitle={OptiTAB - Physique-chimie - Quatrième - Manuel complet},pdfauthor={OptiTAB},pdfsubject={France - Cycle 4 - Édition 2026-2027},pdfkeywords={cours, schémas, exercices, corrigés, programme français}}
\begin{document}\pagenumbering{alph}\input{couverture}\pagenumbering{arabic}\input{liminaires}\clearpage\pagestyle{otMain}
'''
    main+=''.join(rf'\input{{chapitres/{c.numero:02}}}'+'\n' for c in chs)
    main+=r'\pcAnnexe{Corrigés détaillés}{Comprendre les démarches et refaire sans aide}\phantomsection\label{corriges-debut}\pdfbookmark[0]{Corrigés détaillés}{solutions}'+'\n'
    main+=box('Utiliser les corrigés','Cherche avant de lire. Compare le raisonnement et les unités, puis referme le livre et recommence. Les conclusions expérimentales restent limitées aux conditions du protocole.','method')
    main+=r'''\pcSousTitre{Retrouver les quatre thèmes}
\pcRepere{corchap-1}{Matière : mesures, modèles et transformations}
\pcRepere{corchap-9}{Mouvements : vitesses, interactions et poids}
\pcRepere{corchap-12}{Énergie : bilans et lois de l’électricité}
\pcRepere{corchap-18}{Signaux : lumière, son et information}
\pcSousTitre{Faire de l’erreur un outil}
\begin{questions}
\item Repérer la première étape différente de ta démarche : lecture, modèle, conversion ou calcul.
\item Expliquer l’erreur en une phrase et conserver une correction lisible dans le cahier.
\item Refaire sans aide une question analogue, puis revenir au problème initial après quelques jours.
\end{questions}
\begin{pcEncadre}{definition}{Une réponse complète}
La bonne valeur ne suffit pas : une relation justifiée, des unités cohérentes et une conclusion dans le contexte montrent ce que tu as compris. Une réponse expérimentale peut être nuancée si les mesures ne permettent pas de trancher.
\end{pcEncadre}
'''
    main+=''.join(rf'\input{{corriges/{c.numero:02}}}'+'\n' for c in chs)
    main+='\\input{annexes}\n\\end{document}\n'
    write('main.tex',main)
    print('Sources du manuel generees : 20 chapitres, 300 exercices et 20 defis.')

from corrections_activites import ACTIVITES
if __name__=='__main__':build()
