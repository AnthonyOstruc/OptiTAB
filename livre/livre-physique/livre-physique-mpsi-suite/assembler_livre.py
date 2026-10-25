"""Recompose un seul livre LaTeX : liminaires communs, pages et liens continus."""
from pathlib import Path
import re,shutil,json
from construire import page,box,sub,BO,PDFBO

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'livre-physique-mpsi'
OUT=ROOT.parent/'livre-physique-mpsi-integral'

def balanced(s,pos):
    assert s[pos]=='{',(s[pos:pos+80],pos)
    start=pos+1;depth=1;pos+=1
    while depth:
        if s[pos]=='{' and s[pos-1]!='\\':depth+=1
        if s[pos]=='}' and s[pos-1]!='\\':depth-=1
        pos+=1
    return s[start:pos-1],pos

def transform(s,n):
    prefix=f'ch{n:02}-'
    # Les arguments de titres peuvent contenir leurs propres accolades.
    specs={'Page':(3,2),'tocrow':(2,1),'tocresource':(2,1),'fig':(2,0)}
    for cmd,(count,target) in specs.items():
        hits=list(re.finditer(r'\\'+cmd+r'\{',s))
        for m in reversed(hits):
            pos=m.end()-1;args=[]
            for i in range(count):
                while s[pos].isspace():pos+=1
                arg,pos=balanced(s,pos);args.append(arg)
            args[target]=(f'ch{n:02}/' if cmd=='fig' else prefix)+args[target]
            s=s[:m.start()]+'\\'+cmd+''.join('{'+a+'}' for a in args)+s[pos:]
    s=re.sub(r'\\(label|pageref\*?|ref\*?)\{([^{}]+)\}',lambda m:'\\'+m[1]+'{'+prefix+m[2]+'}',s)
    s=re.sub(r'\\hyperref\[([^\]]+)\]',lambda m:r'\hyperref['+prefix+m[1]+']',s)
    return s.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')

def make():
    OUT.mkdir(exist_ok=True)
    for d in ('images','figures','chapitres','build'):(OUT/d).mkdir(exist_ok=True)
    for p in (BASE/'images').glob('*.png'):shutil.copy2(p,OUT/'images'/p.name)
    style=(ROOT/'chapitre-06/mpsi-livre.sty').read_text(encoding='utf-8')
    style=style.replace('Chapitre 06',r'Chapitre \currentchapter').replace('Régime sinusoïdal forcé et résonance',r'\currenttitle')
    style=re.sub(r'pdftitle=\{[^}]*\}',r'pdftitle={OptiTAB Physique MPSI - Ondes et signaux - Chapitres 01 a 10}',style)
    style=re.sub(r'pdfsubject=\{[^}]*\}',r'pdfsubject={Cours, exercices, defis, TP, numerique, DM et DS corriges}',style)
    style=style.replace(r'\label{ex-#1}',r'\label{\chapterprefix ex-#1}').replace(r'\label{sol-#1}',r'\label{\chapterprefix sol-#1}')
    style=style.replace(r'\hyperref[ex-#1]',r'\hyperref[\chapterprefix ex-#1]').replace(r'\pageref*{ex-#1}',r'\pageref*{\chapterprefix ex-#1}')
    style=style.replace(r'\vspace{1mm}\refstepcounter{schema}',r'\vspace{.5mm}\refstepcounter{schema}')
    legacy=next(line for line in (BASE/'mpsi-livre.sty').read_text(encoding='utf-8').splitlines() if line.startswith(r'\newcommand{\Page}'))
    style+='\n'+legacy.replace(r'\newcommand{\Page}',r'\newcommand{\PageLegacy}')+'\n'+r'\let\PageModern\Page'+'\n'
    style+='\n'+r'''\newcommand{\currentchapter}{Livre}
\newcommand{\currenttitle}{Ondes et signaux}
\newcommand{\chapterprefix}{}
\renewcommand{\theschema}{\currentchapter.\arabic{schema}}
\renewcommand{\theHschema}{\currentchapter.\arabic{schema}}
\newcommand{\BeginChapter}[2]{\clearpage\renewcommand{\currentchapter}{#1}\renewcommand{\currenttitle}{#2}\renewcommand{\chapterprefix}{ch#1-}\setcounter{schema}{0}\ifnum\numexpr#1\relax=1\let\Page\PageLegacy\else\let\Page\PageModern\fi\pdfbookmark[0]{Chapitre #1 - #2}{chap-book-#1}}
\renewcommand{\planitem}[3]{\par\noindent
\ifnum\numexpr#1\relax<11
\makebox[10mm][l]{\otSemi\fontsize{9}{10}\selectfont\color{otNavy}#1}%
\hyperref[ch#1-chapitre-#1]{{\sffamily\fontsize{9.3}{12.5}\selectfont\color{otInk}#2}}\tocdots{\otSemi\fontsize{9}{10}\selectfont\color{otNavy}\pageref*{ch#1-chapitre-#1}}%
\else
\makebox[10mm][l]{\otSemi\fontsize{9}{10}\selectfont\color{otMuted}#1}%
{\sffamily\fontsize{9.3}{12.5}\selectfont\color{otMuted}#2}\tocdots{\otLight\fontsize{9}{10}\selectfont\color{otMuted}-}%
\fi\par\vspace{.25mm}}
'''
    (OUT/'mpsi-livre.sty').write_text(style,encoding='utf-8')
    plan=(BASE/'plan.tex').read_text(encoding='utf-8').replace('{Ondes stationnaires et corde vibrante}{1.6}','{Ondes stationnaires et corde vibrante — approfondissement}{Approfondissement de 1.6}')
    (OUT/'plan.tex').write_text(plan.replace('\u2014','-'),encoding='utf-8')
    cover=(BASE/'liminaires.tex').read_text(encoding='utf-8').split(r'\input{liminaires-ouverture}')[0]
    cover=cover.replace(r'Formation des images\\et optique géométrique',r'Ondes et signaux\\Cours et entraînement')
    cover=cover.replace('CHAPITRE 01\\quad /\\quad VERSION À VALIDER\\quad /\\quad 25 OCTOBRE 2026','CHAPITRES 01 À 10\\quad /\\quad VOLUME RÉUNI\\quad /\\quad OCTOBRE 2026')
    front=cover
    front+=page('Collection OptiTAB','Physique MPSI','titre-livre',r'''\thispagestyle{mpsiFront}
\vspace{10mm}\begin{center}\includegraphics[width=63mm]{images/logo-couleur.png}\par\vspace{16mm}
{\otSemi\color{otGreenDark}CLASSE PRÉPARATOIRE SCIENTIFIQUE}\par\vspace{6mm}
{\otLight\fontsize{24}{30}\selectfont Ondes et signaux}\par\vspace{8mm}
{\fontsize{16}{23}\selectfont Cours, méthodes et schémas\par Exercices et problèmes corrigés}\par\vspace{12mm}
Chapitres 01 à 10 réunis\par 240 exercices progressifs\par 30 défis avancés\par 10 TP et 10 activités numériques\par 10 DM et 10 DS avec barèmes\par\vspace{12mm}
Collection OptiTAB\par\href{https://www.optitab.net}{optitab.net}\end{center}
\vfill\source{Édition du 25 octobre 2026. Pagination continue ; sommaire et liens communs. Le chapitre 10 est un approfondissement identifié.}
''')
    front+=page('Édition et références','Mentions éditoriales','mentions-livre',rf'''\thispagestyle{{mpsiFront}}
\Sub{{Périmètre du volume}}
Ce PDF rassemble les dix premiers chapitres du projet de manuel de physique MPSI. Les chapitres 1 à 9 développent les rubriques 1.1 à 1.6 « Ondes et signaux » du programme de référence. Le chapitre 10 prolonge la superposition par les ondes stationnaires et la corde vibrante ; il est explicitement identifié comme approfondissement.
\Sub{{Référence réglementaire}}
\href{{{BO}}}{{Arrêté du 5 janvier 2021, NOR ESRS2035779A}}, BO spécial n° 1 du 11 février 2021, annexe 2. \href{{{PDFBO}}}{{Consulter les annexes officielles}}. Le découpage en chapitres et leur ordre sont des choix pédagogiques de la collection. La concordance est précisée à l’ouverture de chaque chapitre.
\Sub{{Énoncés, schémas et données}}
Les exercices, défis et évaluations portant la mention OptiTAB sont des créations pédagogiques. Les schémas sont vectoriels ; les courbes suivent les lois annoncées. Les données fabriquées pour les TP et simulations sont signalées ; elles ne sont pas présentées comme des mesures réalisées.
\Sub{{Supports authentiques}}
Des parcours ciblés renvoient à de vrais TD, DM, DS et sujets de concours. Ils indiquent le diffuseur, la partie travaillée et le lien du document original. Les énoncés et figures extérieurs restent dans leur support d’origine ; les repères de correction du livre sont rédigés indépendamment. Un sujet de concours n’est jamais présenté comme une création OptiTAB.
\Sub{{Suite de la collection}}
Les chapitres 11 à 28 figurent au plan annuel pour situer la progression. Ils ne font pas partie de ce volume ; aucune pagination fictive ne leur est attribuée. Ce livre de physique n’inclut pas un cours annuel de chimie.
\vfill\source{{© OptiTAB, 2026. Conception des contenus et mise en page : collection OptiTAB. Références documentaires consultées le 25 octobre 2026.}}
''')
    front+=page('Pour ouvrir le livre','Avant-propos','avant-livre',r'''\thispagestyle{mpsiFront}
{\fontsize{14}{20}\selectfont\itshape\color{otNavy}Comprendre un phénomène, construire son modèle, puis savoir le mettre à l’épreuve : c’est le fil conducteur de ce livre.\par}
\vspace{4mm}
Le passage du lycée à la MPSI demande de relier une observation, un schéma, une équation et une mesure. Une formule devient utile lorsque l’on sait pourquoi elle s’applique, ce qu’elle prévoit et où elle cesse de convenir. Le cours développe ces liens et donne aux schémas une place dans le raisonnement.
\par\vspace{2mm}
Ce volume commence par la formation des images, poursuit les circuits et les oscillateurs, puis relie réponse fréquentielle, filtrage, propagation et interférences. Les mêmes idées reviennent sous des formes différentes : linéarité, conditions initiales, phase, énergie et confrontation au réel.
\par\vspace{2mm}
Chaque chapitre suit un parcours complet. Un diagnostic réactive les acquis ; le cours explicite les lois ; un TP et une activité numérique entraînent à les tester. Les exercices progressent vers des problèmes plus autonomes. Trois défis, un devoir maison et un devoir surveillé permettent de travailler la rédaction et l’initiative.
\par\vspace{2mm}
Les corrigés servent après une recherche personnelle. Ils expliquent les étapes et les contrôles, mais ne remplacent pas l’effort de reconstruire une solution. Utiliser les indices, noter la première difficulté puis refaire une question quelques jours plus tard donne un meilleur repère que la seule impression d’avoir compris.
\par\vspace{2mm}
Les parcours authentiques complètent cet entraînement par de vrais documents d’enseignement et de concours. Les questions ciblées rendent leur emploi progressif ; les autres parties peuvent demander des connaissances ultérieures. L’original et ses conventions restent toujours la référence de l’énoncé.
\par\vspace{2mm}
La présentation distingue les capacités du programme et les approfondissements. Le chapitre sur les cordes constitue ainsi une ouverture assumée à partir des outils déjà étudiés. Chacun peut ajuster son parcours à celui de sa classe, sans confondre cette ouverture avec une exigence réglementaire supplémentaire.
\vspace{6mm}{\sffamily\small\color{otNavy}Bon travail et bonne progression en physique.}\par
{\sffamily\small\color{otMuted}La collection OptiTAB}
''')
    front+=page('Pour commencer','Utiliser le livre','mode-livre',r'''\thispagestyle{mpsiFront}
\begin{loi}{Un parcours en quatre étapes}
1. Faire le diagnostic et revoir les prérequis.\par
2. Travailler le cours en refaisant les démonstrations et les schémas.\par
3. Chercher les exercices, les défis et les évaluations sans ouvrir immédiatement les solutions.\par
4. Corriger la première erreur, puis refaire une question sans aide.
\end{loi}
\Sub{Trois niveaux de travail}
Les applications installent les conversions, les lois et les limites. Les exercices de méthode demandent de choisir une stratégie et de relier plusieurs représentations. Les approfondissements demandent davantage d’initiative ; leurs résultats particuliers ne sont pas tous des relations à mémoriser.
\Sub{Rédiger en physique}
Annoncer le système, les hypothèses et les orientations. Construire un schéma légendé. Écrire une expression littérale avant les nombres ; vérifier les unités et les limites ; terminer par une interprétation. Un résultat numérique isolé ne dit pas si le modèle a été compris.
\Sub{Lire un corrigé avec profit}
Comparer les démarches avant les valeurs finales. Une différence de convention peut conduire à un signe différent mais cohérent ; une erreur d’unité ou de condition aux limites ne se résout pas en recopiant une formule. Les renvois des corrigés permettent de revenir à l’énoncé.
\Sub{Utiliser les évaluations}
Chaque chapitre contient un DM et un DS de deux heures, avec barème pédagogique sur 20. Le sujet du DS occupe deux pages consécutives. Les points servent à repérer la compétence fragile et à organiser la reprise ; ils ne constituent pas un barème officiel de concours.
\begin{methode}{Navigation commune}
Le sommaire annuel p.\,\pageref{sommaire-livre} ouvre les chapitres disponibles. Les parcours p.\,\pageref{navigation-1} et \pageref{navigation-2} donnent les accès directs au cours, aux exercices, aux devoirs et aux corrections. Les numéros de pages sont continus dans tout le PDF.
\end{methode}
''')
    front+=page('Collection OptiTAB','Sommaire','sommaire-livre',r'''\thispagestyle{mpsiFront}
\begingroup\setlength{\parskip}{0pt}\fontsize{10}{13.5}\selectfont\input{plan}\endgroup
\vspace{2mm}\hrule\vspace{2mm}
\source{Chapitres 01 à 10 inclus et paginés ; 11 à 28 prévus pour la suite. Le chapitre 10 est un approfondissement. Parcours détaillés p.\,\pageref{navigation-1} et \pageref{navigation-2}.}
''')
    manifests={1:dict(titre='Formation des images et optique géométrique')}
    for n in range(2,11):manifests[n]=json.loads((ROOT/f'chapitre-{n:02}/manifest.json').read_text(encoding='utf-8'))
    for group in range(2):
        body=r'\thispagestyle{mpsiFront}'+'\n'
        for n in range(group*5+1,group*5+6):
            pre=f'ch{n:02}-'; course='c-sources' if n==1 else 'cours-1';ds='ds' if n==1 else 'ds1'
            # Le premier chapitre utilise ses intitulés de repères historiques.
            if n==1:ds='ds1'
            body+=sub(f'{n:02} — '+manifests[n]['titre'],r'\begin{tabularx}{\linewidth}{@{}Y r@{}}'+''.join(r'\tocrow{'+a+'}{'+pre+b+'}\n' for a,b in [('Cours et méthodes',course),('Exercices progressifs','td1'),('Devoir maison','dm'),('Devoir surveillé',ds),('Indications et corrigés','indices')])+r'\end{tabularx}')
        front+=page('Accès directs / '+str(group+1),'Parcours des chapitres',f'navigation-{group+1}',body)
    front+=page('Organiser sa progression','Mon tableau de bord','suivi-livre',r'''\thispagestyle{mpsiFront}
Pour chaque chapitre, noter S (réussi seul), A (avec aide) ou R (à reprendre). La date de reprise aide à transformer la correction en apprentissage durable.
\par\vspace{3mm}\begingroup\renewcommand{\arraystretch}{1.8}
\begin{tabularx}{\linewidth}{@{}l Y c c c c@{}}\toprule
Chapitre & Thème & Cours & TD & DS & Reprise\\\midrule
01 & Images & & & & \\
02 & ARQS & & & & \\
03 & Premier ordre & & & & \\
04 & Oscillateur harmonique & & & & \\
05 & Oscillations amorties & & & & \\
06 & Résonance & & & & \\
07 & Filtrage & & & & \\
08 & Propagation & & & & \\
09 & Interférences & & & & \\
10 & Cordes — approfondissement & & & & \\
\bottomrule\end{tabularx}\endgroup
\Sub{Les habitudes à installer}
\checkline{Je dessine avant de calculer.}
\checkline{J’annonce les hypothèses et les unités.}
\checkline{Je vérifie un cas limite et un ordre de grandeur.}
\checkline{Je distingue prévision, simulation et mesure.}
\checkline{Je peux expliquer une erreur puis refaire la question.}
\begin{methode}{Une reprise ciblée}
Choisir une seule difficulté précise : un signe, une condition initiale, une phase, une lecture de graphe. Refaire deux questions qui mobilisent cette difficulté, puis vérifier le progrès dans un problème plus large.
\end{methode}
''')
    front=front.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
    (OUT/'liminaires.tex').write_text(front,encoding='utf-8')
    bodies=[]
    for n in range(1,11):
        src=BASE if n==1 else ROOT/f'chapitre-{n:02}'
        dest=OUT/f'figures/ch{n:02}';dest.mkdir(exist_ok=True)
        for p in (src/'figures').glob('*.tex'):shutil.copy2(p,dest/p.name)
        if n==1:
            lim=(BASE/'liminaires.tex').read_text(encoding='utf-8')
            s=(BASE/'ouverture-chapitre.tex').read_text(encoding='utf-8')+lim.split(r'\input{ouverture-chapitre}',1)[1]
            s+='\n'.join((BASE/f'{name}.tex').read_text(encoding='utf-8') for name in ['cours','exercices','problemes','corriges','sources'])
            s=s[:s.index(r'\Sub{Suite envisagée après validation}')]+sub('Pour poursuivre',r'Le chapitre 2 traite les signaux électriques dans l’ARQS. Les méthodes de schématisation, de contrôle des unités et de confrontation aux mesures restent les mêmes. Les chapitres suivants poursuivent la progression annoncée au sommaire commun.')
        else:
            s=(src/'contenu.tex').read_text(encoding='utf-8')
            s=s[s.index(r'\Page{Chapitre '+f'{n:02}') :]
        s=transform(s,n)
        short={1:'Formation des images',2:'Signaux électriques',3:'Circuits du premier ordre',4:'Oscillateur harmonique',5:'Oscillations amorties',6:'Résonance',7:'Filtrage linéaire',8:'Propagation',9:'Interférences',10:'Ondes stationnaires'}[n]
        s=rf'\BeginChapter{{{n:02}}}{{{short}}}'+'\n'+s
        (OUT/f'chapitres/ch{n:02}.tex').write_text(s,encoding='utf-8')
        bodies.append(r'\input{chapitres/ch'+f'{n:02}'+'}')
    (OUT/'main.tex').write_text('% !TEX program = lualatex\n'+r'\documentclass[11pt,twoside,openany]{book}'+'\n'+r'\usepackage{mpsi-livre}'+'\n'+r'\begin{document}\input{liminaires}'+'\n'+'\n'.join(bodies)+'\n'+r'\end{document}',encoding='utf-8')
    shutil.copy2(BASE/'compiler.py',OUT/'compiler.py')
    (OUT/'manifest.json').write_text(json.dumps(manifests,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Livre unique recomposé : chapitres 01 à 10, liminaires communs.',flush=True)

if __name__=='__main__':make()
