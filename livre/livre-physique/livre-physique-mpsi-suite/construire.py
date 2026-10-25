"""Fabrication des chapitres 02 à 05, avec la charte validée OptiTAB."""
from pathlib import Path
import shutil, json, re, importlib, subprocess, sys

ROOT=Path(__file__).resolve().parent
PREV=ROOT.parent/'livre-physique-mpsi'
BO='https://www.education.gouv.fr/bo/21/Special1/ESRS2035779A.htm'
PDFBO='https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/8/spe779_annexe_1373648.pdf'

def fig(name,caption):return rf'\fig{{{name}}}{{{caption}}}'
def box(kind,title,body):return '\\begin{'+kind+'}{'+title+'}\n'+body+'\n\\end{'+kind+'}\n'
def qs(*items):return '\\begin{questions}\n'+''.join('\\item '+x+'\n' for x in items)+'\\end{questions}\n'
def sub(title,body):return '\\Sub{'+title+'}\n'+body+'\n'

class Chapter:
    def __init__(self,n,title,section,scope):
        self.n=n;self.title=title;self.section=section;self.scope=scope
        self.course=[];self.ex=[];self.problems=[];self.sources=[];self.checks=[];self.figures={}
    def c(self,title,body):self.course.append((title,body))
    def e(self,title,level,time,body,solution):self.ex.append((title,level,time,body,solution))
    def d(self,title,body,hints,solution):self.problems.append((title,body,hints,solution))
    def f(self,name,body,opts='x=1cm,y=1cm'):
        self.figures[name]='\\begin{tikzpicture}['+opts+']\n'+body+'\n\\end{tikzpicture}\n'
    def check(self,name,actual,expected,tol=1e-7):self.checks.append(dict(nom=name,valeur=float(actual),attendu=float(expected),tolerance=tol))
    def source(self,title,url,target,work,solution):self.sources.append(dict(titre=title,url=url,cible=target,travail=work,corrige=solution))

def page(tag,title,label,body):return '\n\\Page{'+tag+'}{'+title+'}{'+label+'}\n'+body+'\n'

def build(ch):
    assert len(ch.ex)==24 and len(ch.problems)==3 and len(ch.sources)>=2
    for c in ch.checks:assert abs(c['valeur']-c['attendu'])<=c['tolerance'],c
    folder=ROOT/f'chapitre-{ch.n:02}';folder.mkdir(exist_ok=True)
    for d in ['images','figures','build']:(folder/d).mkdir(exist_ok=True)
    for p in (PREV/'images').glob('*.png'):shutil.copy2(p,folder/'images'/p.name)
    style=(PREV/'mpsi-livre.sty').read_text(encoding='utf-8')
    style=style.replace('Chapitre 01',f'Chapitre {ch.n:02}').replace('Chapitre pilote',f'Chapitre {ch.n:02}').replace('Formation des images',ch.title)
    style=style.replace('pdftitle={OptiTAB Physique MPSI Chapitre 1 '+ch.title+'}',f'pdftitle={{OptiTAB Physique MPSI Chapitre {ch.n} {ch.title}}}')
    style=style.replace('\\numexpr#1\\relax=1',f'\\numexpr#1\\relax={ch.n}').replace('chapitre-01',f'chapitre-{ch.n:02}')
    style=style.replace(r'\color{otInk}#2}\par',r'\color{otInk}\raggedright#2\par}')
    style += '\n\\usetikzlibrary{decorations.pathmorphing}\n\\usepgfplotslibrary{groupplots}\n\\RequirePackage[europeanresistors,americaninductors]{circuitikz}\n\\ctikzset{bipoles/length=1cm}\n'
    # Les titres de chapitre longs passent sur deux lignes sans toucher le filet.
    (folder/'mpsi-livre.sty').write_text(style,encoding='utf-8')
    for name,body in ch.figures.items():(folder/'figures'/f'{name}.tex').write_text(body,encoding='utf-8')
    shutil.copy2(PREV/'plan.tex',folder/'plan.tex')
    text=''
    text+=r'''\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
\begin{scope}[shift={(current page.south west)},x=1mm,y=1mm]
\fill[otNavy](0,0)rectangle(210,297);\fill[otNavyDark](0,0)rectangle(210,88);
\draw[white,opacity=.055,step=7mm](0,0)grid(210,297);
\node[anchor=north west,inner sep=0pt]at(23,278){\includegraphics[width=57mm]{images/logo-blanc.png}};
\node[anchor=west,text=otGreen,font=\otSemi\fontsize{12}{15}\selectfont]at(24,235){MPSI\quad /\quad PHYSIQUE};
\node[anchor=west,text=white,font=\sffamily\bfseries\fontsize{52}{56}\selectfont]at(22,211){Physique};
'''
    text+=rf'\node[anchor=north west,text=white,text width=158mm,font=\otLight\fontsize{{31}}{{38}}\selectfont]at(24,191){{{ch.title}}};'+'\n'
    text+=r'''\fill[otGreen](24,149)rectangle(54,150.4);
\node[anchor=north west,text=white,text width=153mm,font=\sffamily\fontsize{11}{16}\selectfont]at(24,139){Cours développé et schémas vectoriels\par 24 exercices et corrigés expliqués\par 3 défis, TP, activité numérique, DM et DS\par Parcours sur des supports authentiques};
\draw[white,opacity=.6,-{Stealth}] (24,46)--(185,46);
\draw[white,opacity=.6,-{Stealth}] (28,17)--(28,81);
'''
    if ch.n in [2,3]:
        text+=r'\draw[otGreen,line width=1.8pt] plot[domain=0:6,samples=100] ({30+24*\x},{48+29*(1-exp(-\x))});'+'\n'
    elif ch.n==4:
        text+=r'\draw[otGreen,line width=1.8pt] plot[domain=0:6,samples=180] ({30+24*\x},{46+27*cos(deg(3*\x))});'+'\n'
    else:
        text+=r'\draw[otGreen,line width=1.8pt] plot[domain=0:6,samples=180] ({30+24*\x},{46+27*cos(deg(3*\x))*exp(-.18*\x)});'+'\n'
    text+=rf'\node[anchor=west,text=white,font=\otSemi\fontsize{{9}}{{12}}\selectfont]at(24,8){{CHAPITRE {ch.n:02}\quad /\quad COLLECTION OPTITAB\quad /\quad OCTOBRE 2026}};'+'\n'+r'\end{scope}\end{tikzpicture}\null'+'\n'
    text+=page('Collection OptiTAB','Physique MPSI','titre',rf'''\thispagestyle{{mpsiFront}}
\vspace{{8mm}}\begin{{center}}\includegraphics[width=63mm]{{images/logo-couleur.png}}\par\vspace{{15mm}}
{{\otSemi\color{{otGreenDark}}CLASSE PRÉPARATOIRE SCIENTIFIQUE}}\par\vspace{{5mm}}
{{\otLight\fontsize{{23}}{{29}}\selectfont Cours et exercices corrigés}}\par\vspace{{12mm}}
{{\fontsize{{18}}{{24}}\selectfont {ch.title}}}\par\vspace{{8mm}}
Chapitre {ch.n:02}\par 24 exercices progressifs ; 3 défis avancés\par TP, numérique, DM et DS avec barèmes\par\vspace{{12mm}}
Collection OptiTAB\par\href{{https://www.optitab.net}}{{optitab.net}}\end{{center}}
\vfill\source{{Édition de travail du 25 octobre 2026. Énoncés OptiTAB originaux, figures vectorielles et corrigés indépendants. Les supports extérieurs sont identifiés à la fin du chapitre.}}
''')
    text+=page('Pour ouvrir le chapitre','Avant-propos et mode d’emploi','avant',rf'''\thispagestyle{{mpsiFront}}
Ce chapitre prolonge le manuel de physique MPSI dans la charte de la collection. Il traite {ch.scope} Le programme de référence est l’\href{{{BO}}}{{arrêté du 5 janvier 2021}}, annexe 2, rubrique {ch.section}.
\Sub{{Comprendre, chercher, vérifier}}
Lire un résultat ne suffit pas à se l’approprier. Redessiner le système, orienter les grandeurs, retrouver les équations puis expliquer leurs limites : ces gestes relient le cours aux problèmes. Une réponse numérique doit comporter une unité, un nombre raisonnable de chiffres et une interprétation.
\begin{{loi}}{{Un parcours en quatre étapes}}
1. Faire le diagnostic p.\,\pageref{{diagnostic}} et reprendre les prérequis fragiles.\par
2. Travailler le cours p.\,\pageref{{cours-1}} et refaire les exemples.\par
3. Chercher les exercices p.\,\pageref{{td1}}, puis les défis et évaluations.\par
4. Corriger, expliquer l’erreur puis refaire une question sans solution.
\end{{loi}}
\Sub{{Utiliser les corrigés}}
Les solutions commencent p.\,\pageref{{corr-diag}}. Avant de les lire, utiliser les indications p.\,\pageref{{indices}}. Le barème du DM et du DS sert à distinguer mise en équation, calcul et interprétation ; ce n’est pas un barème officiel de concours.
\Sub{{Travailler sur de vrais sujets}}
Les pages p.\,\pageref{{sources-1}} et suivantes donnent les liens, les questions ciblées et des repères de correction de supports réellement publiés. Conserver leurs données et figures d’origine. Les énoncés OptiTAB sont des créations pédagogiques, clairement distinguées de ces documents.
\begin{{methode}}{{Une fiche de progrès}}
Après chaque exercice, noter S (réussi seul), A (réussi avec aide) ou R (à reprendre). Choisir une question à refaire deux jours plus tard. Une solution comprise doit pouvoir être reconstruite, pas seulement reconnue.
\end{{methode}}
\source{{© OptiTAB, 2026. Les séries de données créées pour le TP et le numérique sont signalées comme simulations. Les références des auteurs extérieurs restent attachées aux documents d’origine.}}
''')
    text+=page('Collection OptiTAB','Sommaire','sommaire',rf'''\thispagestyle{{mpsiFront}}
\begingroup\setlength{{\parskip}}{{0pt}}\fontsize{{10}}{{13.5}}\selectfont
\source{{MPSI · Physique · Plan de l’ouvrage}}
\input{{plan}}
\endgroup
\vspace{{2mm}}\hrule\vspace{{2mm}}
\tocresource{{Parcours et ressources du chapitre {ch.n:02}}}{{ressources}}
\source{{La pagination concerne ce fascicule. Les autres chapitres sont des volumes séparés ou en préparation ; aucune page fictive n’est attribuée.}}
''')
    nav=[('Diagnostic','diagnostic'),('Cours et méthodes','cours-1'),('Travaux pratiques','tp'),('Activité numérique','numerique'),('24 exercices progressifs','td1'),('Trois défis avancés','defi1'),('Devoir maison','dm'),('Devoir surveillé de 2 heures','ds1'),('Indications progressives','indices'),('Corrigés du diagnostic','corr-diag'),('Corrigés des exercices','corr-td1'),('Corrigés des défis','corr-defi1'),('Corrigé et barème du DM','corr-dm'),('Corrigé et barème du DS','corr-ds1'),('Supports authentiques et références','sources-1')]
    text+=page('Collection OptiTAB','Parcours et ressources','ressources',r'\thispagestyle{mpsiFront}'+'\n'+''.join(r'\tocresource{'+a+'}{'+b+'}\n' for a,b in nav)+r'\begin{docu}{Mon objectif de travail}\checkline{Je refais une démonstration.}\checkline{Je réussis une application sans aide.}\checkline{Je justifie le choix d’un modèle.}\checkline{Je corrige une évaluation et repère la capacité à reprendre.}\end{docu}')
    tag=f'Chapitre {ch.n:02} / '+('Approfondissement' if ch.n==10 else 'Programme officiel')
    text+=page(tag,ch.title,f'chapitre-{ch.n:02}',ch.intro+'\n'+box('loi','Notions et capacités travaillées',ch.mapping)+'\n'+sub('Prérequis',ch.prereq)+'\n'+box('methode','La méthode du chapitre',ch.method)+f'\n\\source{{Concordance : annexe 2 de l’arrêté du 5 janvier 2021, rubrique {ch.section}. {ch.boundary}}}')
    text+=page('Diagnostic / 15 min','Avant d’ouvrir le cours','diagnostic',ch.diagnostic+box('docu','Bilan personnel',r'\checkline{Les conversions et les unités sont maîtrisées.}\checkline{Je peux orienter un schéma et annoncer les hypothèses.}\checkline{Je sais expliquer une condition initiale.}'+r'Corrigé p.\,\pageref{corr-diag}.'))
    for i,(title,body) in enumerate(ch.course,1):text+=page(f'Cours / {i}',title,f'cours-{i}',body)
    text+=page('Pratique / TP',ch.tp_title,'tp',ch.tp)
    text+=page('Pratique / Numérique',ch.num_title,'numerique',ch.num)
    text+=page('Bilan de cours','Les réflexes à conserver','synthese',ch.synthesis)
    for group in range(8):
        body=r'\source{Énoncés OptiTAB originaux. Les durées sont indicatives ; justifier toute réponse.}'+'\n'
        for j in range(group*3,group*3+3):
            title,level,time,pb,sol=ch.ex[j];body+=rf'\ex{{E{j+1:02}}}{{{title}}}{{Niveau {level}}}{{{time}}}'+'\n'+pb+'\n'
        text+=page('Exercices / '+('Applications' if group<3 else 'Méthodes' if group<6 else 'Approfondissement'),ch.td_titles[group],f'td{group+1}',body)
    for j,(title,pb,hints,sol) in enumerate(ch.problems,1):text+=page(f'Défi avancé / D{j}',title,f'defi{j}',rf'\label{{ex-D{j}}}\source{{Problème OptiTAB original. Niveau 3 ; 40 à 60 minutes. Indices p.\,\pageref{{indices}} ; corrigé p.\,\pageref{{corr-defi{j}}}.}}'+'\n'+pb)
    text+=page('Évaluation / DM',ch.dm_title,'dm',r'\source{Devoir maison OptiTAB original ; 1 h 30 à 2 h ; calculatrice autorisée. Barème pédagogique sur 20.}'+'\n'+ch.dm)
    text+=page('Évaluation / DS / 1 sur 2',ch.ds_title,'ds1',r'\source{Devoir surveillé OptiTAB original ; durée 2 h ; calculatrice autorisée ; note sur 20. Les deux pages forment un seul sujet.}'+'\n'+ch.ds[0])
    text+=page('Évaluation / DS / 2 sur 2','Approfondir et conclure','ds2',ch.ds[1]+box('docu','Gestion du temps',r'Lecture : 10 min ; parties A et B : 70 min ; partie C : 30 min ; vérification : 10 min. Une expression littérale, une unité et une interprétation accompagnent les résultats.'))
    text+=page('Aides progressives','Des indices pour repartir','indices',''.join(sub(f'Défi D{j}',h) for j,(_,_,h,_) in enumerate(ch.problems,1))+sub('Exercices',ch.hints)+sub('Évaluations',ch.eval_hints))
    text+=page('Corrigés / Diagnostic','Réactiver les bons réflexes','corr-diag',ch.diag_sol)
    for group in range(8):
        body=''
        for j in range(group*3,group*3+3):
            title,level,time,pb,sol=ch.ex[j];body+=rf'\sol{{E{j+1:02}}}{{{title}}}'+'\n'+sol+'\n'
        text+=page('Corrigés / Exercices',ch.td_titles[group],f'corr-td{group+1}',body)
    for j,(title,pb,hints,sol) in enumerate(ch.problems,1):text+=page(f'Corrigé du défi D{j}',title,f'corr-defi{j}',sol)
    text+=page('Corrigé / DM / Sur 20',ch.dm_title,'corr-dm',ch.dm_sol)
    for j,body in enumerate(ch.ds_sol,1):text+=page(f'Corrigé / DS / {j} sur 2','Calculer et interpréter',f'corr-ds{j}',body)
    for j,s in enumerate(ch.sources,1):
        text+=page('Support authentique / '+str(j),s['titre'],f'sources-{j}',rf'\source{{Source consultée le 25 octobre 2026. {s["cible"]}}}'+'\n'+box('loi','Accéder au document d’origine',rf'\href{{{s["url"]}}}{{Ouvrir le sujet original et conserver ses figures et données.}}')+sub('Parcours de travail',s['travail'])+sub('Repères de correction indépendants',s['corrige'])+r'\source{Ce parcours ne reproduit pas l’épreuve complète. Les questions non ciblées peuvent demander des chapitres ultérieurs. Le temps de travail proposé concerne uniquement cette sélection.}')
    text+=page('Références et suivi','Préparer la suite','references',rf'''\Sub{{Référence réglementaire}}
\href{{{BO}}}{{Bulletin officiel spécial n° 1 du 11 février 2021, arrêté du 5 janvier 2021.}}\par
\href{{{PDFBO}}}{{Annexe officielle regroupée}}, rubrique {ch.section}. {ch.boundary}
\Sub{{Nature des contenus}}
Le cours, les 24 exercices, les trois défis et les évaluations OptiTAB sont rédigés pour cette collection. Les graphiques sont calculés avec les équations annoncées. Les supports authentiques sont identifiés sur les pages précédentes ; leurs énoncés et figures restent dans le document d’origine.
\Sub{{Compétences à confirmer}}
\checkline{{Je peux retrouver l’équation sans mémoriser une suite de signes.}}
\checkline{{Je vérifie les conditions initiales et les limites.}}
\checkline{{Je peux confronter un calcul, un graphe et un bilan énergétique.}}
\checkline{{Je sais corriger mon DS et refaire une question sans aide.}}
\begin{{methode}}{{Prochaine étape}}
{ch.next}
\end{{methode}}
''')
    # Les symboles grecs conservent leur police mathématique dans les unités.
    def units(m):
        parts=re.split(r'(\\(?:mu|Omega))',m.group(1))
        return ''.join(p if p.startswith('\\') else ('\\mathrm{'+p+'}' if p.strip() else p) for p in parts)
    text=re.sub(r'\\mathrm\{([^{}]*(?:\\mu|\\Omega)[^{}]*)\}',units,text)
    blocks=re.split(r'(\\begin\{verbatim\}.*?\\end\{verbatim\})',text,flags=re.S)
    text=''.join(b if i%2 else re.sub(r'(?<!\\)%',r'\\%',b) for i,b in enumerate(blocks))
    # Donner leur propre ligne aux résultats encadrés les plus longs.
    for expression in [r's(t)=s_\infty+(s_0-s_\infty)e^{-t/\tau}',r'x=x_0\cos(\omega_0t)+(v_0/\omega_0)\sin(\omega_0t)']:
        text=text.replace('$\\result{'+expression+'}$','\\[\\result{'+expression+'}\\]')
    text=text.replace('\\].','\\]')
    # Les titres Montserrat ne possèdent pas les glyphes grecs du corps de cours.
    for char,command in {'λ':'lambda','ω':'omega','τ':'tau','φ':'varphi'}.items():
        text=re.sub(char+r'([0-9])',lambda m:'\\ensuremath{\\'+command+'_'+m[1]+'}',text)
    for char,command in {'λ':'lambda','ω':'omega','μ':'mu','τ':'tau','φ':'varphi','π':'pi','δ':'delta','Δ':'Delta','ε':'varepsilon'}.items():
        text=text.replace(char,'\\ensuremath{\\'+command+'}')
    (folder/'contenu.tex').write_text(text,encoding='utf-8')
    main=r'''% !TEX program = lualatex
\documentclass[11pt,twoside,openany]{book}
\usepackage{mpsi-livre}
\begin{document}\input{contenu}\end{document}
'''
    (folder/'main.tex').write_text(main,encoding='utf-8')
    (folder/'manifest.json').write_text(json.dumps(dict(chapitre=ch.n,titre=ch.title,rubrique=ch.section,scope=ch.scope,cours=len(ch.course),exercices=24,defis=3,dm=1,ds=1,sources=ch.sources,controles=ch.checks,figures=list(ch.figures)),ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copy2(PREV/'compiler.py',folder/'compiler.py')
    print(f'Chapitre {ch.n:02} : {len(ch.course)} pages de cours, {len(ch.figures)} figures, {len(ch.checks)} calculs contrôlés.',flush=True)
    return folder

if __name__=='__main__':
    for n in [int(x) for x in sys.argv[1:]] or [2,3,4,5]:
        module=importlib.import_module(f'chapitre{n:02}');build(module.create())
