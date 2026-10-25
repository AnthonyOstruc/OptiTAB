"""Éditions autonomes des deux options. Ne modifie pas le manuel de spécialité."""
from pathlib import Path
import importlib.util, json, shutil, sys, subprocess, re

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if name=='expertes':
        module.CHAPTERS.extend(load('expertes_matrices').CHAPTERS+load('expertes_graphes').CHAPTERS)
        parts=['Nombres complexes','Arithmétique','Graphes et matrices']
        module.CHAPTERS.sort(key=lambda ch:parts.index(ch['part']))
        end=load('expertes_fin')
        for field in ['PROJECTS','ASSESSMENTS','DOSSIERS','SOLUTIONS_DOSSIERS','CONCORDANCE','COVERAGE','INDEX']:
            setattr(module,field,getattr(end,field))
        assert len(module.CHAPTERS)==12
    return module

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')

def questions(items):
    return '\\begin{questions}\n'+''.join('\\item '+s+'\n' for s in items)+'\\end{questions}\n'

def build(option):
    data=load(option);book=ROOT/('livre-maths-'+option);book.mkdir(exist_ok=True)
    for sub in ['images','chapitres','corriges','build','recherche']:(book/sub).mkdir(exist_ok=True)
    shutil.copy2(ROOT/'livre-terminale/optitab-livre.sty',book/'optitab-livre.sty')
    for img in ['logo-blanc.png','logo-couleur.png']:shutil.copy2(ROOT/'livre-terminale/images'/img,book/'images'/img)
    for src in (ROOT/'tmp/pdfs/recherche-options-terminale').glob('*'):
        if option in src.name or src.stem=='grille-manuels':shutil.copy2(src,book/'recherche'/src.name)
    total=sum(len(c['ex']) for c in data.CHAPTERS)
    style=r'''\renewcommand{\otNiveau}{Terminale · Option}
\renewcommand{\otSousTitre}{Cours et exercices corrigés}
\renewcommand{\otCleardoublepage}{\clearpage}
\usepackage{xurl}
\urlstyle{same}
\linespread{1.04}
\clubpenalty=10000\widowpenalty=10000\displaywidowpenalty=10000
\setlength{\parskip}{1.8mm}
\setlength{\headheight}{16pt}
\renewcommand{\otFootText}[1]{{\otLight\fontsize{6.5}{8}\selectfont\color{otMuted}#1}}
\fancypagestyle{otMain}{\fancyhf{}\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[LE]{\otHeadNum\hspace{0.8em}\otHeadText{\leftmark}}
\fancyhead[RO]{\otHeadText{\rightmark}\hspace{0.8em}\otHeadNum}
\fancyfoot[LE]{\otThumb\otFootNum\hspace{1.2em}\otFootText{OptiTAB · Terminale}}
\fancyfoot[RO]{\otThumb\otFootText{\OptionLivre}\hspace{1.2em}\otFootNum}}
\newcommand{\figurelivre}[2]{\par\addvspace{3mm}\noindent\begin{minipage}{\linewidth}\centering
\includegraphics[width=0.94\linewidth,height=58mm,keepaspectratio]{#1}\par\vspace{1mm}
{\otLight\fontsize{8.5}{11}\selectfont\color{otMuted}\raggedright #2\par}\end{minipage}\par\vspace{2mm}}
\newcommand{\souscours}[1]{\par\addvspace{4mm}\Needspace{5\baselineskip}\noindent
{\otSemi\fontsize{12}{15}\selectfont\color{otNavy}#1}\par\nopagebreak\vspace{1mm}}
\newcommand{\repere}[2]{\par\addvspace{2mm}\noindent\hyperref[#1]{{\otMedium\fontsize{9}{12}\selectfont\color{otGreenDark}#2 · p.~\pageref*{#1}}}\par}
\newcommand{\fiche}[2]{\clearpage\gdef\otHeadTag{}\markboth{#1}{#1}\noindent{\raggedright\hyphenpenalty=10000\otLight\fontsize{24}{29}\selectfont\color{otInk}#1\par}\vspace{2mm}{\otLight\fontsize{10}{13}\selectfont\color{otMuted}#2\par}\vspace{4mm}\noindent{\color{otNavy}\rule{16mm}{1.3pt}}{\color{otRule}\rule[.45pt]{\dimexpr\linewidth-16mm\relax}{.4pt}}\par\vspace{6mm}}
\renewcommand{\exercices}{\par\ifdim\pagetotal<.45\textheight\addvspace{4mm}\else\clearpage\fi}
\patchcmd{\otDansCe}{L'essentiel}{Le cours}{}{}
\patchcmd{\otEntete}{\otBesoinPlace{9\baselineskip}}{\ifotCorriges\otBesoinPlace{5\baselineskip}\else\otBesoinPlace{9\baselineskip}\fi}{}{}
\patchcmd{\otEntete}{\addvspace{6.5mm}}{\addvspace{4.5mm}}{}{}
\patchcmd{\otEntete}{\addvspace{6.5mm}}{\addvspace{4.5mm}}{}{}
\newcommand{\figurepetite}[2]{\par\addvspace{2mm}\noindent\begin{minipage}{\linewidth}\centering\includegraphics[width=.94\linewidth,height=32mm,keepaspectratio]{#1}\par\vspace{1mm}{\otLight\fontsize{8.5}{11}\selectfont\color{otMuted}\raggedright #2\par}\end{minipage}\par\vspace{1mm}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\E}{\mathbb{E}}
\providecommand{\square}{\mdlgwhtsquare}
\renewcommand{\code}[1]{\leavevmode\mbox{\NoAutoSpacing\otMono\fontsize{8.4}{11}\selectfont\color{otNavyDark}\detokenize{#1}}}
\renewcommand{\otQRCours}{\begin{tikzpicture}\node[fill=otNavyTint,rounded corners=2mm,inner sep=4mm,text width=47mm]
{{\otSemi\fontsize{8.5}{11}\selectfont\color{otNavy}Mon carnet de méthodes}\par\vspace{1mm}
{\otLight\fontsize{8}{11}\selectfont Après une erreur, écrire sa cause et refaire une question analogue sans corrigé.}};\end{tikzpicture}}
\renewcommand{\essentiel}{\clearpage\markright{Le cours}\phantomsection\label{ess-\otChapNum}
\otPageTitre{Le cours}{Comprendre · Justifier · Appliquer}\vspace{-4mm}}
\makeatletter
\renewcommand{\corrigesChapitre}[2]{\clearpage\gdef\otChapNum{#1}\gdef\otChapTitle{#2}
\global\otCorrigestrue\gdef\otAccent{otGreenDark}\global\otSoupletrue
\gdef\otHeadTag{\otTwoDigits{\otChapNum}}\markboth{Solutions · #2}{Solutions · #2}
\phantomsection\label{corchap-#1}\pdfbookmark[1]{#1 · #2}{bm-corchap-#1}
\otPageTitre{Solutions · #1}{#2}}
\apptocmd{\corrigesChapitre}{\fontsize{10.5}{13.3}\selectfont\setlength{\parskip}{1mm}\setlist[questions,1]{label=\otLabel{\arabic*.},leftmargin=1.7em,labelsep=.45em,itemsep=.3em,topsep=.2em,partopsep=0pt,parsep=.2em}}{}{}
\makeatother
\lstset{literate={*}{{\char42}}1 {-}{{\char45}}1 {>}{{\char62}}1 {<}{{\char60}}1}
'''
    if option=='expertes':
        style+=r'''\patchcmd{\figurelivre}{height=58mm}{height=50mm}{}{}
\patchcmd{\essSection}{\addvspace{7mm}}{\addvspace{5mm}}{}{}
\patchcmd{\otEntete}{\addvspace{4.5mm}}{\addvspace{3.5mm}}{}{}
\patchcmd{\otEntete}{\addvspace{4.5mm}}{\addvspace{3.5mm}}{}{}
'''
    write(book/'option.sty',style)
    cover=r'''\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
\begin{scope}[shift={(current page.south west)}]
\fill[otNavy] (0,0) rectangle (210mm,297mm);
\shade[bottom color=otNavyDark,top color=otNavy] (0,0) rectangle (210mm,150mm);
\draw[white,opacity=.05,step=8mm] (0,0) grid (210mm,297mm);
\node[anchor=north west,inner sep=0pt] at (22mm,279mm){\includegraphics[width=60mm]{logo-blanc}};
\node[anchor=west,text=otGreen,font=\otSemi\fontsize{11}{14}\selectfont] at (23mm,239mm){\otCaps[18]{Terminale générale · Option}};
\node[anchor=west,text=white,font=\otBold\fontsize{41}{45}\selectfont] at (21mm,216mm){Mathématiques};
\node[anchor=west,text=white,font=\otLight\fontsize{30}{36}\selectfont] at (22mm,196mm){\NomOption};
\fill[otGreen] (24mm,183mm) rectangle (54mm,184.4mm);
\node[anchor=north west,text=white,text width=156mm,font=\otRegular\fontsize{11}{16}\selectfont] at (24mm,170mm)
{Le cours expliqué\enspace·\enspace Des méthodes résolues\\Des exercices progressifs et leurs corrigés};
\node[anchor=north west,text=white,text width=145mm,font=\otRegular\fontsize{10.5}{16}\selectfont] at (24mm,136mm)
{\otCheck\hspace{3mm}\NbChapitres\ chapitres pour apprendre et réviser\\[3mm]
\otCheck\hspace{3mm}\NbExercices\ exercices, du calcul au problème\\[3mm]
\otCheck\hspace{3mm}Schémas et représentations vectorielles\\[3mm]
\otCheck\hspace{3mm}Dossiers de synthèse et ateliers Python};
\draw[otGreen,line width=2pt] (24mm,51mm)--(60mm,51mm);
\node[anchor=west,text=white,font=\otSemi\fontsize{9}{12}\selectfont] at (24mm,41mm){Programme français · Édition 2026-2027};
\node[anchor=west,text=white,opacity=.7,font=\otLight\fontsize{8}{11}\selectfont] at (24mm,31mm){Manuel indépendant fondé sur les textes du Bulletin officiel};
\node[anchor=west,text=white,font=\otMedium\fontsize{10}{12}\selectfont] at (24mm,16mm){optitab.net};
\end{scope}\end{tikzpicture}\null\clearpage
'''
    write(book/'couverture.tex',cover)
    front=r'''\pagestyle{otFront}
\otPageTitre{Apprendre avec OptiTAB}{\OptionLivre · Terminale générale}
Ce manuel accompagne l'enseignement optionnel français de \OptionLivre.
Il associe un cours progressif, des méthodes expliquées, des exercices de trois niveaux et des solutions rédigées.
\begin{savoirfaire}[Un parcours en quatre temps]
\textbf{Comprendre.} Lire le cours et refaire l'exemple résolu, calculs masqués.\par
\textbf{S'entraîner.} Commencer par les exercices accessibles, puis travailler les applications.\par
\textbf{Chercher.} Réserver un vrai temps aux problèmes, aux conjectures et à leur justification.\par
\textbf{Consolider.} Comparer les raisonnements, noter l'erreur puis refaire la question deux jours plus tard.
\end{savoirfaire}
Les points colorés indiquent une difficulté croissante. Les renvois d'un exercice vers sa solution, et de la solution vers l'énoncé, sont cliquables.
Les six compétences se travaillent ensemble : chercher, modéliser, représenter, raisonner, calculer et communiquer.
\souscours{Lire les énoncés avec précision}
Une hypothèse est une information disponible ; une conclusion est ce qu'il faut établir.
Une représentation ou une simulation aide à conjecturer. Une preuve explique pourquoi l'énoncé reste vrai dans tous les cas annoncés.
Chaque problème exige une conclusion dans son contexte et, si nécessaire, une unité, une précision ou une limite du modèle.
\souscours{Données et outils}
Sauf mention contraire, les données des exercices sont fictives et choisies pour l'apprentissage. Les situations médicales, économiques et cryptographiques sont des modèles pédagogiques.
Une valeur exacte précède autant que possible son arrondi. La calculatrice et Python servent à explorer, à calculer et à contrôler ; les arguments mathématiques restent explicités.
\vfill
{\small OptiTAB · Édition numérique, octobre 2026. Textes, exercices et figures de cette édition : création éditoriale OptiTAB. Les programmes officiels restent la propriété de leurs auteurs institutionnels. Ce manuel indépendant n'est pas une publication du ministère et ne revendique aucune homologation.}
\clearpage
\otPageTitre{Sommaire}{Un itinéraire complet, des outils aux synthèses}
'''
    for i,c in enumerate(data.CHAPTERS,1):
        front+=rf'\noindent\makebox[9mm][l]{{\otSemi\color{{otNavy}}{i:02}}}\hyperref[chap-{i}]{{{c["title"]}\otPoints\pageref*{{chap-{i}}}}}\par\vspace{{2.6mm}}'+'\n'
    front+=r'''\vspace{4mm}\repere{dossiers}{Dossiers et évaluations de synthèse}
\repere{corriges-debut}{Corrigés détaillés}
\repere{concordance}{Concordance avec le programme et sources}
\repere{index-methodes}{Index des méthodes et formules}
\clearpage
\otPageTitre{Faire le point}{Diagnostic de départ · À reprendre après quelques semaines}
'''+data.DIAGNOSTIC+r'''
\clearpage\otPageTitre{Mon parcours}{Cocher après une réussite autonome, puis après révision}
\begin{tabularx}{\linewidth}{@{}p{8mm}Yccc@{}}\toprule
& Chapitre & Cours & Exercices & Révision\\\midrule
'''
    for i,c in enumerate(data.CHAPTERS,1):front+=rf'{i} & {c["title"]} & $\square$ & $\square$ & $\square$ \\[2mm]'+'\n'
    front+=r'\bottomrule\end{tabularx}\par\vspace{5mm}Une case indique une réussite sans aide. Si un exercice résiste, revenir au cours et au premier exemple avant de reprendre le problème.\clearpage\pagestyle{otMain}'
    write(book/'liminaires.tex',front)
    plan=''
    for i,c in enumerate(data.CHAPTERS,1):
        body=rf'\begin{{ouverture}}[{c.get("deco","courbe")}]{{{i}}}{{{c["title"]}}}{{{c["part"]}}}{{{c["tags"]}}}'+'\n'
        body+=''.join('\\objectif{'+x+'}\n' for x in c['goals'])
        body+='\\prerequis{'+c['pre']+'}\n\\end{ouverture}\n\\essentiel\n'+c['course']
        body+='\n\\exercices\n'
        for j,ex in enumerate(c['ex'],1):
            if j in (1,5,9):
                if j>1:body+='\\clearpage\n'
                body+='\\markright{'+{1:'Prendre confiance',5:'Appliquer et relier',9:'Chercher et argumenter'}[j]+'}\n'
                body+='\\begingroup\\renewcommand{\\otBesoinPlace}[1]{}\\begin{minipage}{\\linewidth}\n'
                body+='\\rubrique{'+{1:'Prendre confiance',5:'Appliquer et relier',9:'Chercher et argumenter'}[j]+'}\n'
            body+=rf'\begin{{exercice}}[{ex["level"]}]{{{ex["title"]}}}'+'\n'+ex.get('intro','')+'\n'+questions(ex['q'])+'\\end{exercice}\n'
            if j in (4,8,12):body+='\\end{minipage}\\endgroup\n'
        write(book/'chapitres'/f'{i:02}.tex',body)
        corr=rf'\corrigesChapitre{{{i}}}{{{c["title"]}}}'+'\n'
        for j,ex in enumerate(c['ex'],1):
            if option=='expertes' and i==10 and j==11:
                corr+='\\par\\begingroup\\renewcommand{\\otBesoinPlace}[1]{}\\noindent\\begin{minipage}{\\linewidth}\n'
            corr+=rf'\begin{{corrige}}{{{j}}}{{{ex["title"]}}}'+'\n'+questions(ex['a'])+'\\end{corrige}\n'
            if option=='expertes' and i==10 and j==12:corr+='\\end{minipage}\\endgroup\n'
        write(book/'corriges'/f'{i:02}.tex',corr)
        plan+=rf'\otPlanChap{{{i}}}{{{c["title"]}}}{{}}'+'\n'
    write(book/'plan.tex',plan)
    write(book/'dossiers.tex',data.DOSSIERS)
    write(book/'corriges-dossiers.tex',data.SOLUTIONS_DOSSIERS)
    write(book/'concordance.tex',data.CONCORDANCE)
    write(book/'index.tex',data.INDEX)
    main=r'\documentclass[11pt,twoside,openany]{book}'+'\n\\usepackage{optitab-livre}\n\\usepackage{option}\n'
    for key,val in [('OptionLivre','Mathématiques '+data.NOM),('NomOption',data.NOM),('NbChapitres',str(len(data.CHAPTERS))),('NbExercices',str(total))]:main+=rf'\newcommand{{\{key}}}{{{val}}}'+'\n'
    main+=r'\hypersetup{pdftitle={OptiTAB - Mathématiques '+data.NOM+r' - Terminale - Manuel complet},pdfauthor={OptiTAB},pdfsubject={France - Enseignement optionnel - Édition 2026-2027},pdfkeywords={cours, exercices progressifs, corrigés, programme français}}'+'\n'
    main+=r'\begin{document}\pagenumbering{alph}\input{couverture}\pagenumbering{arabic}\input{liminaires}'+'\n'
    main+=''.join(rf'\input{{chapitres/{i:02}}}'+'\n' for i in range(1,len(data.CHAPTERS)+1))
    main+='\\input{dossiers}\n\\clearpage\\phantomsection\\label{corriges-debut}\\pdfbookmark[0]{Corrigés}{solutions}\n'
    main+=''.join(rf'\input{{corriges/{i:02}}}'+'\n' for i in range(1,len(data.CHAPTERS)+1))
    main+='\\input{corriges-dossiers}\n\\input{concordance}\n\\input{index}\n\\end{document}\n'
    write(book/'main.tex',main)
    write(book/'README.md',f'# Mathématiques {data.NOM} · Terminale\n\nSources éditoriales : `../livres-options-terminale/{option}.py`.\n\nGénérer les sources : `python ../livres-options-terminale/construire.py {option}`.\nCompiler : `lualatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex` (plusieurs passes jusqu’à stabilisation).\n\nProgramme : BO spécial n° 8 du 25 juillet 2019. Édition 2026-2027. Textes officiels archivés dans recherche. Contenu original ; ne pas confondre avec un document ministériel.\n')
    write(book/'inventaire.json',json.dumps({'option':data.NOM,'chapitres':len(data.CHAPTERS),'exercices':total,'questions':sum(len(e['q']) for c in data.CHAPTERS for e in c['ex']),'chapters':[{'numero':i,'titre':c['title'],'exercices':len(c['ex'])} for i,c in enumerate(data.CHAPTERS,1)]},ensure_ascii=False,indent=2))
    print(book)

if __name__=='__main__':build(sys.argv[1])
