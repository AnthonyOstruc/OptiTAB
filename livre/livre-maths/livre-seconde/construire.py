"""Assemble le livre sans modifier les livres précédents."""
from pathlib import Path
import json,shutil
from modele import CHAPITRES,FIGURES
import contenu_01_02,contenu_03_04,contenu_05_06,contenu_07_08
import contenu_09_10,contenu_11_12,contenu_13_14,contenu_15_16
from approfondissements import DEFIS
from bilans import BILANS
from demonstrations import PREUVES
from liminaires_contenu import documents,couverture_programme
from generer_figures import write_all

ROOT=Path(__file__).resolve().parent
# Gabarit figé dans ce dossier (copie de la charte du livre de Première utilisée
# pour l'édition du 21 octobre 2026) : la construction ne dépend plus des
# modifications ultérieures de livre-premiere.
TEMPLATE=ROOT/'gabarit'
PAGES=[];INSERTIONS=[]

def write(path,text):
    # Une tabulation dans le TeX produit révèle une commande mangée par un
    # littéral Python non brut (par exemple \toprule devenu « oprule »).
    assert not any(ord(c)<32 and c not in '\n\r' for c in text),str(path)
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-'),encoding='utf-8')

def visual(name,label,page_label,cor=False):
    assert name in FIGURES,name
    INSERTIONS.append({'figure':name,'label':label,'texte':page_label,'corrige':cor})
    return '\\label{'+label+'}\n\\figureGeo'+('[corrige]' if cor else '')+'{'+name+'}\n'

def edition(label,title,subtitle,meta,body,parent=''):
    PAGES.append({'label':label,'titre':title})
    extra='[\\pdfbookmark[0]{'+parent+'}{bm-'+label+'-parent}]' if parent else ''
    return ('\\editionPage'+extra+'{'+label+'}{'+title+'}{'+subtitle+'}{'+meta+'}\n'+
      '\\begin{blocEdition}{'+label+'}\n'+body+'\n\\end{blocEdition}\n')

def build():
    write_all(ROOT)
    assert len(CHAPITRES)==16 and len(DEFIS)==16 and len(BILANS)==2
    style=(TEMPLATE/'optitab-livre.sty').read_text(encoding='utf-8')
    write(Path('optitab-livre.sty'),style.replace('Première · Spécialité','Seconde · Générale et technologique'))
    for fname in ['figures-geometrie.sty','relecture-livre.sty','edition-france.sty']:
        shutil.copy2(TEMPLATE/fname,ROOT/fname)
    oldmain=(TEMPLATE/'main.tex').read_text(encoding='utf-8')
    decors=oldmain[oldmain.index(r'\newcommand{\otDecoseconddegre}'):oldmain.index(r'\newcommand{\otBrouillon}')]
    main=r'''% !TEX program = lualatex
\documentclass[11pt,twoside,openany]{book}
\usepackage{optitab-livre}
\usepackage{figures-geometrie}
\usepackage{relecture-livre}
\usepackage{edition-france}
\usepackage{longtable}
\newcommand{\ligneSommaire}[2]{\par\vspace{3.5mm}\hyperref[#2]{#1}\hfill{\small p.\,\pageref*{#2}}\par}
\newcommand{\otDecoalgorithmique}{\otDecoboucles}
\newcommand{\otDecostatistique}{\otDecograndsnombres}
\newcommand{\otDecoprobabilites}{\otDecoconditionnelles}
\hypersetup{pdftitle={Mathématiques - Seconde générale et technologique - Livre complet},
pdfsubject={France 2026-2027 : cours, 256 exercices corrigés, questions flash, approfondissements et deux bilans},pdfauthor={OptiTAB}}
'''+decors+r'''
\begin{document}
\pagenumbering{alph}
\input{couverture/premiere}
\pagenumbering{arabic}
\input{liminaires/titre}
\input{liminaires/copyright}
\input{liminaires/avant-propos}
\input{liminaires/mode-emploi}
\input{liminaires/parcours}
\input{liminaires/sommaire}
\input{liminaires/tableau-de-bord}
\pagestyle{otMain}
'''
    plan='';currentpart=None
    for c in CHAPITRES:
        if c.partie!=currentpart:
            num,title=c.partie.split(' · ',1)
            plan+='\\otPlanPartie{'+num+'}{'+title+'}\n';currentpart=c.partie
        plan+='\\otPlanChap{'+str(c.numero)+'}{'+c.titre+'}{15}\n'
        fname=f'{c.numero:02d}-{c.slug}'
        main+='\\input{chapitres/'+fname+'}\n'
        text='\\begin{ouverture}['+c.deco+']{'+str(c.numero)+'}{'+c.titre+'}{Partie '+c.partie+'}\n{'+c.sous_titre+'}\n'
        text+='\n'.join('\\objectif{'+s+'}' for s in c.objectifs)+'\n'
        text+='\n'.join('\\prerequis{'+s+'}' for s in c.prerequis)+'\n\\end{ouverture}\n'
        text+='\\pagestyle{otMain}\\essentiel\\fontsize{11}{15}\\selectfont\n'
        text+='\n\\clearpage\n'.join(c.cours)
        for i,e in enumerate(c.exercices,1):
            if i in [1,6,11]:text+='\n\\clearpage\\rubrique{'+{1:'Découverte',6:'Entraînement',11:'Problèmes'}[i]+'}\n'
            ident=f'{c.numero}-{i}'
            text+='\\begin{blocLivre}{ex-'+ident+'}\n\\begin{exercice}['+str(e.difficulte)+']{'+e.titre+'}\n'+e.enonce+'\n'
            if e.figure:text+=visual(e.figure,'fig-ex-'+ident,'exo-'+ident)
            text+='\\end{exercice}\n\\end{blocLivre}\n'
        write(Path('chapitres')/(fname+'.tex'),text+'\n\\clearpage\n')
        corr='\\clearpage\\pagestyle{otMain}\\fontsize{11}{15}\\selectfont\n\\corrigesChapitre{'+str(c.numero)+'}{'+c.titre+'}\n'
        for i,e in enumerate(c.exercices,1):
            ident=f'{c.numero}-{i}'
            corr+='\\begin{blocLivre}{cor-'+ident+'}\n\\begin{corrige}{'+str(i)+'}{'+e.titre+'}\n\\demarche{'+e.methode.replace('%',r'\%')+'}\n'+e.corrige+'\n'
            if e.figure:corr+=visual(e.figure,'fig-cor-'+ident,'cor-'+ident,True)
            corr+='\\end{corrige}\n\\end{blocLivre}\n'
        write(Path('corriges')/(fname+'.tex'),corr)
    write(Path('plan.tex'),plan)
    cover=(TEMPLATE/'couverture/premiere.tex').read_text(encoding='utf-8').replace('14 défis','16 défis').replace('224','256').replace('Deux sujets blancs originaux','Deux bilans de fin d’année')
    write(Path('couverture/premiere.tex'),cover)
    back=(TEMPLATE/'couverture/quatrieme.tex').read_text(encoding='utf-8')
    begin=back.index('       Ce livre rassemble');end=back.index(r'\par}\vspace{9mm}',begin)
    back=back[:begin]+'''       Ce livre réunit les cours et 256 exercices corrigés de Seconde générale et technologique :
       240 exercices progressifs dans 16 chapitres et 16 défis facultatifs. Les corrigés
       expliquent les méthodes et les vérifications. Figures, arbres, démonstrations et
       deux bilans permettent de travailler toute l’année en autonomie.'''+back[end:]
    write(Path('couverture/quatrieme.tex'),back.replace('Réussir sa Première','Réussir sa Seconde').replace('14 chapitres','16 chapitres'))
    title=(TEMPLATE/'liminaires/titre.tex').read_text(encoding='utf-8').replace('224 exercices progressifs et deux sujets blancs corrigés','256 exercices progressifs et deux bilans corrigés')
    write(Path('liminaires/titre.tex'),title)
    mode=(TEMPLATE/'liminaires/mode-emploi.tex').read_text(encoding='utf-8')
    mode=mode.replace("dans l'esprit de l'épreuve anticipée de mathématiques",'pour relier les notions de Seconde et prendre des initiatives')
    mode=mode.replace('Choisir la bonne forme','Somme de multiples')
    mode=mode.replace(r'On considère la fonction $f$ définie sur $\R$ par $f(x)=x^{2}-6x+5$.',r'Les entiers $a$ et $b$ sont multiples de 9. Étudier $a+b$.')
    write(Path('liminaires/mode-emploi.tex'),mode)
    shutil.copy2(TEMPLATE/'liminaires/tableau-de-bord.tex',ROOT/'liminaires/tableau-de-bord.tex')
    for name,content in documents().items():write(Path('liminaires')/(name+'.tex'),content)
    text=r'''\clearpage\gdef\otChapNum{0}\pagestyle{otFront}\phantomsection\label{defis-debut}\pdfbookmark[0]{Défis d’approfondissement}{bm-defis}
\otPageTitre{Défis d’approfondissement}{Un parcours facultatif pour aller plus loin}
Les 16 défis demandent davantage d’initiative que les exercices de chapitre. Ils restent fondés sur des outils accessibles à partir de la Seconde ; les prolongements sont définis dans l’énoncé. Les pistes d’approfondissement du programme sont toutes repérées dans la matrice finale.\par\medskip
Chercher d’abord sans aide. Les indications sont séparées des énoncés ; ouvrir la première, puis la seconde seulement si nécessaire. Prévoir de 30 à 90 minutes selon le défi, éventuellement en plusieurs séances.\par\medskip
\begin{savoirfaire}[Conserver une trace de recherche]Dessiner, tester un cas, écrire une conjecture, puis revenir aux hypothèses. Dans le corrigé, repérer l’idée qui débloque le problème et la formulation de la conclusion.\end{savoirfaire}
\begin{tabularx}{\linewidth}{@{}lY@{}}\toprule
D01 à D03 & Nombres, identités et inégalités.\\[2mm]
D04 à D11 & Barycentres, concours de droites, aires et lieux.\\[2mm]
D12 à D13 & Paramètres et dispersion.\\[2mm]
D14 à D16 & Tableaux, contrôles et dénombrement.\\\bottomrule
\end{tabularx}
'''
    for i,d in enumerate(DEFIS,1):
        label=f'defi-ex-{i}';body=d.enonce
        if d.figure:body+=visual(d.figure,f'fig-defi-ex-{i}',label)
        text+=edition(label,f'D{i:02d} · {d.titre}','Recherche et rédaction',d.prerequis+r' · \hyperref[defi-cor-'+str(i)+r'-1]{Corrigé p.\,\pageref*{defi-cor-'+str(i)+'-1}}',body)
    write(Path('annexes/defis-enonces.tex'),text)
    text=''
    for start in range(0,16,4):
        body=''
        for i,d in list(enumerate(DEFIS,1))[start:start+4]:
            body+='\\editionEtape{D'+f'{i:02d}'+' · '+d.titre+'}\n'
            body+='\\textbf{Indice 1.} '+d.indices[0]+'\\par\\smallskip\n\\textbf{Indice 2.} '+d.indices[1]+'\\par\n'
        if start==0:text+=r'\clearpage\phantomsection\label{indices-debut}\pdfbookmark[0]{Indications des défis}{bm-indices}'+'\n'
        text+=edition('indices-'+str(start//4+1),'Indications progressives','Une aide, puis une nouvelle recherche','Ne consulter que l’aide nécessaire.',body)
    write(Path('annexes/indices-defis.tex'),text)
    corr=''
    for i,d in enumerate(DEFIS,1):
        for j,body in enumerate(d.solutions,1):
            label=f'defi-cor-{i}-{j}'
            if d.figure and j==len(d.solutions):body+=visual(d.figure,f'fig-defi-cor-{i}',label,True)
            corr+=edition(label,f'D{i:02d} · Corrigé'+(' (suite)' if j>1 else ''),d.titre,r'\hyperref[defi-ex-'+str(i)+r']{Énoncé p.\,\pageref*{defi-ex-'+str(i)+r'}} · Démarche et contrôles',body,'Corrigés des défis' if i==j==1 else '')
    write(Path('annexes/defis-corriges.tex'),corr)
    text=r'''\editionPage[\pdfbookmark[0]{Deux bilans de fin d’année}{bm-bilans}]{bilans-guide}{Travailler les bilans}{Seconde · Synthèse des apprentissages}{Deux entraînements originaux, sans valeur d’épreuve officielle.}
\begin{blocEdition}{bilans-guide}
\editionEtape{Organisation proposée}
Chaque bilan dure environ 2 heures. Les dix automatismes se traitent sans calculatrice en 15 à 20 minutes. Pour les problèmes, la calculatrice est autorisée si le professeur ne donne pas d’autre consigne. Les questions demandant une forme exacte restent à traiter exactement.
\editionEtape{Barème d’entraînement}
Les automatismes valent 5 points, à raison de 0,5 point chacun. Les trois problèmes valent 5 points chacun. Total : 20 points ; le barème détaillé est un choix de ce livre. Une démarche correcte peut être valorisée même si un calcul intermédiaire échoue.
\editionEtape{Avant et après la séance}
Prévoir une feuille de brouillon et une copie pour la rédaction. Donner les hypothèses, les étapes et les unités. Après correction, classer les difficultés : notion, méthode, calcul ou rédaction. Refaire une question de chaque difficulté repérée.
\editionRetenir{Un bilan sert à identifier le prochain travail utile. Reprendre ensuite les exercices ciblés.}
\end{blocEdition}
'''
    PAGES.append({'label':'bilans-guide','titre':'Travailler les bilans'})
    cor=''
    for b in BILANS:
        auto='\\begin{questions}\n'+'\n'.join('\\item '+q for q,s,k in b.automatismes)+'\n\\end{questions}'
        text+=edition(f'bilan-{b.lettre}-auto',f'Bilan {b.lettre} · Automatismes',b.titre,'5 points · Sans calculatrice · 0,5 point par réponse',auto)
        autosol='\\begin{questions}\n'+'\n'.join('\\item '+s for q,s,k in b.automatismes)+'\n\\end{questions}'
        cor+=edition(f'bilan-{b.lettre}-cor-auto',f'Bilan {b.lettre} · Corrigé','Automatismes expliqués',r'\hyperref[bilan-'+b.lettre+r'-auto]{Énoncé p.\,\pageref*{bilan-'+b.lettre+'-auto}}',autosol,'Corrigés des bilans' if b.lettre=='A' else '')
        for i,p in enumerate(b.problemes,1):
            label=f'bilan-{b.lettre}-ex-{i}';body=p.enonce
            if p.figure:body+=visual(p.figure,f'fig-{label}',label)
            text+=edition(label,f'Bilan {b.lettre} · Problème {i}',p.titre,'5 points · Démarche et rédaction attendues',body)
            labelcor=f'bilan-{b.lettre}-cor-{i}';body=p.corrige
            if p.figure:body+=visual(p.figure,f'fig-{labelcor}',labelcor,True)
            cor+=edition(labelcor,f'Bilan {b.lettre} · Corrigé {i}',p.titre,r'\hyperref['+label+r']{Énoncé p.\,\pageref*{'+label+'}}',body)
    write(Path('annexes/bilans-enonces.tex'),text)
    write(Path('annexes/bilans-corriges.tex'),cor)
    proof='';count=0
    for i,(title,proofs) in enumerate(PREUVES,1):
        body=''
        for name,argument in proofs:
            count+=1;body+='\\begin{demonstration}['+str(count)+'. '+name+']\n'+argument+'\n\\end{demonstration}\n'
        if i==1:proof+=r'\clearpage\phantomsection\label{preuves-debut}\pdfbookmark[0]{Démonstrations de référence}{bm-preuves}'+'\n'
        proof+=edition('preuves-'+str(i),'Démonstrations',title,'Lire les hypothèses, les transformations et la conclusion.',body)
    write(Path('annexes/demonstrations.tex'),proof)
    write(Path('annexes/couverture-programme.tex'),couverture_programme())
    from automatismes import SERIES,FIGURES_SERIES
    def series_bloc(series,corrige):
        body=''
        for lettre,titre,questions in series:
            body+='\\editionEtape{Série '+lettre+' · '+titre+'}\n'
            figure=FIGURES_SERIES[lettre]+'\n' if not corrige and lettre in FIGURES_SERIES else ''
            items=[('\\otEtiq{otMuted}{'+bloc+'}\\enspace '+s if corrige else q) for q,s,k,bloc,reperes in questions]
            # Chaque question reste d’un seul tenant : pas de coupure entre deux colonnes.
            body+='\\begin{deuxcolonnes}'+figure+'\\begin{questions}\n'+'\n'.join('\\item \\begin{minipage}[t]{\\linewidth}\\raggedright\\leavevmode '+it+'\\end{minipage}' for it in items)+'\n\\end{questions}\\end{deuxcolonnes}\n'
        return body
    intro=(r'''Ces questions flash entretiennent les automatismes de la partie transversale du programme : calcul, proportions, évolutions, fonctions, géométrie, statistiques et probabilités. Une série se traite sans calculatrice, à l’oral ou à l’écrit, en 5 à 10 minutes ; la reprendre plusieurs fois dans l’année, en commençant dès les premiers chapitres. Les corrigés indiquent le bloc du programme de chaque question.'''+'\n')
    pages_auto=[(SERIES[:2],'Séries A et B · Nombres, calculs et proportions'),(SERIES[2:],'Séries C et D · Géométrie, fonctions, données et hasard')]
    text='';cor=''
    for j,(groupe,sous_titre) in enumerate(pages_auto,1):
        text+=edition(f'automatismes-{j}','Automatismes · Questions flash',sous_titre,
          r'Sans calculatrice · \hyperref[automatismes-cor-'+str(j)+r']{Corrigé p.\,\pageref*{automatismes-cor-'+str(j)+'}}',
          (intro if j==1 else '')+series_bloc(groupe,False),'Automatismes : questions flash' if j==1 else '')
        cor+=edition(f'automatismes-cor-{j}','Automatismes · Corrigés',sous_titre,
          r'\hyperref[automatismes-'+str(j)+r']{Énoncés p.\,\pageref*{automatismes-'+str(j)+'}} · Réponses et justifications courtes',
          series_bloc(groupe,True),'Corrigés des automatismes' if j==1 else '')
    write(Path('annexes/automatismes-enonces.tex'),text)
    write(Path('annexes/automatismes-corriges.tex'),cor)
    main+=r'''\input{annexes/automatismes-enonces}
\input{annexes/defis-enonces}
\input{annexes/indices-defis}
\input{annexes/bilans-enonces}
\input{annexes/demonstrations}
\partieCorriges
'''
    for c in CHAPITRES:main+='\\input{corriges/'+f'{c.numero:02d}-{c.slug}'+'}\n'
    main+=r'''\input{annexes/automatismes-corriges}
\input{annexes/defis-corriges}
\input{annexes/bilans-corriges}
\input{annexes/ateliers}
\input{annexes/couverture-programme}
\input{liminaires/references}
\input{couverture/quatrieme}
\end{document}
'''
    from ateliers import ATELIERS,FIGURES_ATELIERS
    workshop=''
    for label,title,sub,body in ATELIERS:
        if label in FIGURES_ATELIERS:
            assert body.count('@@FIGURE@@')==1,label
            body=body.replace('@@FIGURE@@',visual(FIGURES_ATELIERS[label],'fig-'+label,label))
        workshop+=edition(label,title,sub,'Une ressource à reprendre au fil de l’année.',body)
    write(Path('annexes/ateliers.tex'),workshop)
    write(Path('main.tex'),main)
    manifest={'niveau':'Seconde générale et technologique','programme':'https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602914A',
      'date':'2026-10-23','audit_programme':'2026-10-23','questions_flash':sum(len(s[2]) for s in SERIES),
      'chapitres':16,'exercices_chapitres':240,'defis':16,'exercices_total':256,'bilans':2,
      'automatismes_bilans':20,'problemes_bilans':6,'demonstrations':count,'visuels_uniques':len(FIGURES),'insertions_visuelles':len(INSERTIONS),
      'pages_annexes':PAGES,'figures':INSERTIONS,
      'exercices':[{'chapitre':c.numero,'numero':i,'titre':e.titre,'difficulte':e.difficulte,'figure':e.figure,'methode':e.methode,'controle':e.controle} for c in CHAPITRES for i,e in enumerate(c.exercices,1)]}
    write(Path('manifeste-seconde.json'),json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in manifest.items() if k not in ['exercices','figures','pages_annexes']},ensure_ascii=True,indent=2))

if __name__=='__main__':build()
