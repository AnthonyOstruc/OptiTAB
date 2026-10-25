"""Construit uniquement le nouveau volume, à partir des données originales."""
from pathlib import Path
import json,importlib
from modele import CHAPITRES,FIGURES
ROOT=Path(__file__).resolve().parent
TEMPLATE=ROOT/'_modele_collection'
for path in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(path.stem)
from approfondissements import DEFIS
from bilans import BILANS
from ressources import PREUVES,OUTILS
from liminaires_contenu import documents,couverture_programme,SOURCES
from generer_figures import write_all
PAGES=[];INSERTIONS=[]
EDITION='Édition 2028-2029 · Nouveau programme · Brevet 2029'

def write(path,text):
    assert not any(ord(c)<32 and c not in '\n\r\t' for c in text),path
    if Path(path).parts[0] in ('chapitres','corriges','annexes'):
        # Un % non échappé ouvrirait un commentaire LaTeX et tronquerait le texte.
        import re
        assert not re.search(r'(?<!\\)%',text),(path,'signe % non échappé')
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-'),encoding='utf8')
def nettoyer():
    """Les fichiers des dossiers générés sont tous reconstruits : on retire les anciens."""
    for dossier in ['chapitres','corriges','figures']:
        for p in (ROOT/dossier).glob('*.tex'):p.unlink()
def visual(nom,label,parent,cor=False):
    assert nom in FIGURES,nom
    INSERTIONS.append(dict(figure=nom,label=label,texte=parent,corrige=cor))
    return '\\label{'+label+'}\\figureGeo'+('[corrige]' if cor else '')+'{'+nom+'}\n'
def edition(label,title,sub,meta,body,parent=''):
    PAGES.append(dict(label=label,titre=title))
    extra='[\\pdfbookmark[0]{'+parent+'}{bm-'+label+'-parent}]' if parent else ''
    return '\\editionPage'+extra+'{'+label+'}{'+title+'}{'+sub+'}{'+meta+'}\n\\begin{blocEdition}{'+label+'}\n'+body+'\n\\end{blocEdition}\n'

def build():
    assert len(CHAPITRES)==18 and len(DEFIS)==18 and len(BILANS)==2
    nettoyer()
    write_all(ROOT)
    style=(TEMPLATE/'optitab-livre.sty').read_text(encoding='utf8')
    style=style.replace('Première · Spécialité','Troisième · Brevet 2029')
    style=style.replace('Le cours complet','La collection OptiTAB').replace('Fiches, cours et exercices en ligne sur','Retrouver OptiTAB sur')
    write(Path('optitab-livre.sty'),style)
    old=(TEMPLATE/'main.tex').read_text(encoding='utf8')
    decors=old[old.index(r'\newcommand{\otDecoseconddegre}'):old.index(r'\newcommand{\otBrouillon}')]
    main=r'''% !TEX program = lualatex
\documentclass[11pt,twoside,openany]{book}
\usepackage{optitab-livre}
\usepackage{figures-geometrie}
\usepackage{relecture-livre}
\usepackage{edition-france}
\newcommand{\ligneSommaire}[2]{\par\vspace{3.5mm}\hyperref[#2]{#1}\hfill{\small p.\,\pageref*{#2}}\par}
\newcommand{\otDecoalgorithmique}{\otDecoboucles}
\newcommand{\otDecoprobabilites}{\otDecoconditionnelles}
\newcommand{\otDecogeometrie}{\otDecoGrille
\draw[white,opacity=.25,line width=1pt](113mm,24mm)--(194mm,24mm)--(194mm,100mm)--cycle;
\draw[white,opacity=.25,line width=.8pt](186mm,24mm)--(186mm,32mm)--(194mm,32mm);}
\hypersetup{pdftitle={Mathématiques - Troisième - Nouveau programme - Brevet 2029 - Livre complet},
pdfsubject={France, édition 2028-2029, programme 2026 : 18 chapitres, 288 exercices corrigés, deux brevets blancs},pdfauthor={OptiTAB}}
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
\input{liminaires/nouveautes}
\input{liminaires/sommaire}
\input{liminaires/tableau-de-bord}
\pagestyle{otMain}
'''
    plan='';part=None
    for c in CHAPITRES:
        if c.partie!=part:
            n,t=c.partie.split(' · ',1);plan+='\\otPlanPartie{'+n+'}{'+t+'}\n';part=c.partie
        plan+='\\otPlanChap{'+str(c.numero)+'}{'+c.titre+'}{15}\n'
        fname=f'{c.numero:02}-{c.slug}'
        main+='\\input{chapitres/'+fname+'}\n'
        text='\\begin{ouverture}['+c.deco+']{'+str(c.numero)+'}{'+c.titre+'}{Partie '+c.partie+'}\n{'+c.sous_titre+'}\n'
        text+='\n'.join('\\objectif{'+t+'}' for t in c.objectifs)+'\n'
        text+='\n'.join('\\prerequis{'+t+'}' for t in c.prerequis)+'\n\\end{ouverture}\n'
        text+='\\pagestyle{otMain}\\essentiel\\fontsize{11}{15}\\selectfont\n'+'\n\\clearpage\n'.join(c.cours)
        cor='\\clearpage\\pagestyle{otMain}\\fontsize{11}{15}\\selectfont\\corrigesChapitre{'+str(c.numero)+'}{'+c.titre+'}\n'
        for i,e in enumerate(c.exercices,1):
            if i in [1,6,11]:text+='\n\\clearpage\\rubrique{'+{1:'Découverte',6:'Entraînement',11:'Problèmes'}[i]+'}\n'
            ident=f'{c.numero}-{i}'
            text+='\\begin{blocLivre}{ex-'+ident+'}\\begin{exercice}['+str(e.difficulte)+']{'+e.titre+'}\n'+e.enonce+'\n'
            if e.figure:text+=visual(e.figure,'fig-ex-'+ident,'exo-'+ident)
            text+='\\end{exercice}\\end{blocLivre}\n'
            cor+='\\begin{blocLivre}{cor-'+ident+'}\\begin{corrige}{'+str(i)+'}{'+e.titre+'}\\demarche{'+e.methode.replace('%',r'\%')+'}\n'+e.corrige+'\n'
            if e.figure:cor+=visual(e.figure,'fig-cor-'+ident,'cor-'+ident,True)
            cor+='\\end{corrige}\\end{blocLivre}\n'
        write(Path('chapitres')/(fname+'.tex'),text+'\n\\clearpage\n')
        write(Path('corriges')/(fname+'.tex'),cor)
    write(Path('plan.tex'),plan)
    cover=(TEMPLATE/'couverture/premiere.tex').read_text(encoding='utf8').replace('224','288').replace('14 défis','18 défis').replace('Deux sujets blancs originaux','Deux brevets blancs originaux')
    ancien=r'{Année complète\enspace·\enspace Exercices progressifs\enspace·\enspace Corrigés détaillés\enspace·\enspace Méthodes}'
    assert ancien in cover
    cover=cover.replace(ancien,r'{Édition 2028-2029\enspace·\enspace Nouveau programme\enspace·\enspace Brevet 2029}')
    cover=cover.replace(r'{\otMedium\fontsize{7}{9}\selectfont Année complète}',r'{\otMedium\fontsize{7}{9}\selectfont Programme 2026}')
    # Géométrie de couverture : parallélogramme et relation de Chasles.
    start=cover.index('  % Repère,');end=cover.index('  % Logo',start)
    cover=cover[:start]+r'''  % Parallélogramme et somme de deux vecteurs (relation de Chasles)
\draw[white,opacity=.22,line width=.6pt](98mm,32mm)--(160mm,32mm)--(194mm,88mm)--(132mm,88mm)--cycle;
\draw[white,opacity=.85,line width=1.6pt,-{Stealth[length=4.2mm,width=3.2mm]}](98mm,32mm)--(158.5mm,32mm);
\draw[white,opacity=.85,line width=1.6pt,-{Stealth[length=4.2mm,width=3.2mm]}](160mm,32mm)--(193.2mm,86.7mm);
\draw[otGreen,line width=3pt,-{Stealth[length=6mm,width=4.6mm]}](98mm,32mm)--(192.4mm,87.1mm);
\fill[white](98mm,32mm)circle(1.8mm);\fill[otGreen](98mm,32mm)circle(.9mm);
'''+cover[end:]
    write(Path('couverture/premiere.tex'),cover)
    back=(TEMPLATE/'couverture/quatrieme.tex').read_text(encoding='utf8')
    start=back.index('       Ce livre rassemble');end=back.index(r'\par}\vspace{9mm}',start)
    back=back[:start]+'''       Cette édition suit le nouveau programme de mathématiques du cycle 4,
       applicable en Troisième à la rentrée 2028. Elle réunit les cours et
       288 exercices corrigés : 270 exercices progressifs dans 18 chapitres
       et 18 défis facultatifs. Vecteurs, quartiles, identités remarquables,
       inéquations, sphère et sections sont traités en détail. Deux brevets
       blancs originaux préparent la session 2029.'''+back[end:]
    back=back.replace('Réussir sa Première','Réussir sa Troisième').replace('14 chapitres','18 chapitres').replace('Des tableaux de variations et des courbes soignés','Des figures, tableaux et scripts par blocs soignés')
    back=back.replace('ANNÉE COMPLÈTE\\\\18 chapitres\\\\Édition 2026','NOUVEAU PROGRAMME\\\\18 chapitres\\\\Édition 2028-2029')
    assert 'Édition 2028-2029' in back
    back=back.replace('Prolonge ton travail en ligne','Collection OptiTAB').replace('Cours, fiches de synthèse et exercices\n       sur \\textbf{\\otSite}. Scanne le code pour y accéder.','Du collège au lycée : une même présentation pour\\par apprendre, chercher et progresser.')
    write(Path('couverture/quatrieme.tex'),back)
    title=(TEMPLATE/'liminaires/titre.tex').read_text(encoding='utf8').replace('224 exercices progressifs et deux sujets blancs corrigés','288 exercices progressifs et deux brevets blancs corrigés').replace("L'équipe pédagogique OptiTAB",'Collection OptiTAB')
    ancre=r'''  \node[anchor=base,inner sep=0pt,text=otInk,
    font=\otMedium\fontsize{10}{12}\selectfont] at (105mm,42mm)'''
    assert ancre in title
    title=title.replace(ancre,r'''  \node[anchor=base,inner sep=0pt,text=otGreenDark,
    font=\otSemi\fontsize{10.5}{13}\selectfont] at (105mm,112mm)
    {Édition 2028-2029\enspace·\enspace Nouveau programme\enspace·\enspace Brevet 2029};
'''+ancre)
    write(Path('liminaires/titre.tex'),title)
    write(Path('liminaires/tableau-de-bord.tex'),(TEMPLATE/'liminaires/tableau-de-bord.tex').read_text(encoding='utf8'))
    for nom,body in documents().items():write(Path('liminaires')/(nom+'.tex'),body)
    text=edition('defis-debut','Dix-huit défis','Un défi par chapitre · Parcours facultatif','Chercher avant de consulter les deux indications.',r'''Ces problèmes demandent davantage d’initiative. Ils utilisent les outils du livre ; les prolongements sont définis dans l’énoncé. Aucun défi n’ajoute une exigence officielle au brevet.\par\bigskip
\begin{savoirfaire}[Une recherche qui avance]Faire un schéma, tester un petit cas, comparer deux méthodes, conserver les essais et préciser ce qui reste à prouver. Ouvrir la première indication seulement après une recherche réelle ; revenir au problème avant de lire la seconde.\end{savoirfaire}
\begin{savoirfaire}[Après la solution]Identifier l’idée décisive et la refaire sur une feuille vierge. Expliquer pourquoi elle fonctionne compte autant que retrouver le résultat.\end{savoirfaire}''','Défis d’approfondissement')
    cor='';ind=''
    for i,d in enumerate(DEFIS,1):
        body=d.enonce
        if d.figure:body+=visual(d.figure,f'fig-defi-{i}',f'defi-ex-{i}')
        text+=edition(f'defi-ex-{i}',f'D{i:02} · Défi',d.titre,'Approfondissement · 30 à 60 minutes indicatives',body)
        body=d.corrige
        if d.figure:body+=visual(d.figure,f'fig-defi-cor-{i}',f'defi-cor-{i}',True)
        cor+=edition(f'defi-cor-{i}',f'D{i:02} · Corrigé',d.titre,r'\hyperref[defi-ex-'+str(i)+r']{Énoncé p.\,\pageref*{defi-ex-'+str(i)+'}}',body,'Corrigés des défis' if i==1 else '')
    for start in range(0,18,3):
        body=''
        for i,d in enumerate(DEFIS[start:start+3],start+1):
            body+=r'\editionEtape{D'+f'{i:02} · '+d.titre+r'}\textbf{Indice 1.} '+d.indices[0]+r'\par\medskip\textbf{Indice 2.} '+d.indices[1]+r'\par'+'\n'
        label='indices-debut' if start==0 else f'indices-{start+1}'
        ind+=edition(label,'Indications progressives',f'Défis {start+1} à {start+3}','Ne lire que l’aide nécessaire.',body,'Indications des défis' if start==0 else '')
    write(Path('annexes/defis-enonces.tex'),text);write(Path('annexes/defis-corriges.tex'),cor);write(Path('annexes/indices-defis.tex'),ind)
    text=edition('bilans-guide','Deux brevets blancs','Session 2029 · Sujets originaux','Durée totale : 2 heures · Note sur 20 · Coefficient 2',r'''
Définition retenue : note de service du 11 septembre 2026 (BO spécial n° 4 du
17 septembre 2026), en vigueur à compter de la session 2027. Au 23 octobre 2026,
aucun texte propre à la session 2029 n’était publié ; vérifier avant l’examen
qu’aucune modification n’est intervenue.
\editionEtape{Partie 1 : 20 minutes, sans calculatrice}
Automatismes et applications directes : 6 points. Questions à réponses courtes,
portant sur les automatismes du cycle 4 ou l’application directe d’une propriété,
d’une formule ou d’un théorème. Ici, douze questions à 0,5 point. La première
copie est relevée au bout de 20 minutes.
\editionEtape{Partie 2 : 1 h 40, calculatrice autorisée}
Raisonnement et résolution de problèmes : 14 points. Exercices indépendants,
sans QCM ; toutes les réponses sont justifiées, sauf indication contraire. La
maîtrise de la langue est évaluée sur 2 points. Utiliser une seconde copie ;
le passage de la première à la seconde partie se fait sans pause.
\editionEtape{Le barème de ce livre}
Chaque problème vaut 3,5 points : trois questions à 1 point et 0,5 point pour
la maîtrise de la langue et la clarté de la rédaction. Les 2 points de maîtrise
de la langue sont ainsi inclus dans les 14 points. Ce partage est un choix
d’entraînement ; il ne préjuge pas des barèmes des sujets officiels.
\editionEtape{Après la séance}
Comparer les démarches, classer les erreurs par notion et refaire les questions
utiles sans correction. Les essais et démarches engagés, même non aboutis, sont
valorisés : un résultat numérique faux n’efface pas une démarche correcte.
''','Deux brevets blancs')
    cor=''
    for b in BILANS:
        auto=r'\begin{questions}'+'\n'+'\n'.join(r'\item '+q for q,s,k in b.automatismes)+r'\end{questions}'
        text+=edition(f'bilan-{b.lettre}-auto',f'Brevet blanc {b.lettre}',b.titre,'Partie 1 · 20 min · Sans calculatrice · 6 points',auto)
        autosol=r'\begin{questions}'+'\n'+'\n'.join(r'\item '+s for q,s,k in b.automatismes)+r'\end{questions}'
        cor+=edition(f'bilan-{b.lettre}-cor-auto',f'Brevet {b.lettre} · Corrigé','Automatismes expliqués',r'\hyperref[bilan-'+b.lettre+r'-auto]{Énoncé p.\,\pageref*{bilan-'+b.lettre+'-auto}}',autosol,'Corrigés des brevets blancs' if b.lettre=='A' else '')
        for i,p in enumerate(b.problemes,1):
            lab=f'bilan-{b.lettre}-ex-{i}';body=p.enonce
            if p.figure:body+=visual(p.figure,'fig-'+lab,lab)
            text+=edition(lab,f'Brevet {b.lettre} · Problème {i}',p.titre,'Partie 2 · 1 h 40 pour les quatre problèmes · 3,5 points',body)
            labcor=f'bilan-{b.lettre}-cor-{i}';body=p.corrige
            if p.figure:body+=visual(p.figure,'fig-'+labcor,labcor,True)
            cor+=edition(labcor,f'Brevet {b.lettre} · Corrigé {i}',p.titre,r'\hyperref['+lab+r']{Énoncé p.\,\pageref*{'+lab+'}}',body)
    write(Path('annexes/bilans-enonces.tex'),text);write(Path('annexes/bilans-corriges.tex'),cor)
    proof=''
    for i,(t,b) in enumerate(PREUVES,1):proof+=edition('preuves-debut' if i==1 else f'preuves-{i}','Comprendre les preuves',t,'Les arguments ci-dessous éclairent des propriétés utilisées dans le livre.',b,'Démonstrations' if i==1 else '')
    write(Path('annexes/demonstrations.tex'),proof)
    outils=''
    for i,(t,b) in enumerate(OUTILS,1):outils+=edition('outils-debut' if i==1 else f'outils-{i}','Fiche outil',t,'À consulter au fil des chapitres.',b,'Fiches outils' if i==1 else '')
    write(Path('annexes/outils.tex'),outils)
    write(Path('annexes/couverture-programme.tex'),couverture_programme())
    main+=r'''\input{annexes/defis-enonces}
\input{annexes/indices-defis}
\input{annexes/bilans-enonces}
\input{annexes/demonstrations}
\partieCorriges
'''
    for c in CHAPITRES:main+='\\input{corriges/'+f'{c.numero:02}-{c.slug}'+'}\n'
    main+=r'''\input{annexes/defis-corriges}
\input{annexes/bilans-corriges}
\input{annexes/outils}
\input{annexes/couverture-programme}
\input{liminaires/references}
\input{couverture/quatrieme}
\end{document}
'''
    write(Path('main.tex'),main)
    manifest=dict(niveau='Troisième - DNB série générale',edition='2028-2029',programme='Arrêté du 18-2-2026, BO n° 10 du 5-3-2026 (cycle 4, application en 3e à la rentrée 2028)',session=2029,
      definition_epreuve='Note de service du 11-9-2026, NOR MENE2623228N, BO spécial n° 4 du 17-9-2026, en vigueur à compter de la session 2027 ; aucun texte propre à la session 2029 au 23-10-2026',
      date='2026-10-23',chapitres=18,exercices_chapitres=270,defis=18,exercices_total=288,brevets_blancs=2,automatismes=24,problemes_brevets=8,visuels_uniques=len(FIGURES),insertions_visuelles=len(INSERTIONS),figures=INSERTIONS,pages_annexes=PAGES,sources=SOURCES,exercices=[dict(chapitre=c.numero,numero=i,titre=e.titre,difficulte=e.difficulte,figure=e.figure) for c in CHAPITRES for i,e in enumerate(c.exercices,1)])
    write(Path('manifeste-troisieme-2028.json'),json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in manifest.items() if k not in ['figures','pages_annexes','sources','exercices']},ensure_ascii=True,indent=2))
if __name__=='__main__':build()
