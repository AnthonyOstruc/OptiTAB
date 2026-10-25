"""Recompose le manuel de 5e avec la charte LuaLaTeX du livre de Terminale.

Les données pédagogiques restent les sources validées du manuel complet.
Les pages des deux premiers chapitres sont capturées sémantiquement : aucune
page n'est insérée comme une image. Les schémas sont exportés en PDF vectoriel.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib, html, json, re, shutil, subprocess, unicodedata
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import maquette
from schemas import draw
import construire as ancien
import construire_complet as complet
from contenu import CH1, CH2, PLAN, SOURCES
from programme_complet import TITRES, THEMES, SOURCES_COMPLEMENTAIRES
from annexes_completes import BILANS, LEXIQUE, annexes

ROOT=Path(__file__).resolve().parent
REF=ROOT.parent/'livre-pc-terminale'
OUT=ROOT/'template-terminale'
FIG=OUT/'figures'
BUILD=OUT/'build'
for p in (OUT,FIG,BUILD,OUT/'images'):p.mkdir(parents=True,exist_ok=True)
CHS={ch.n:ch for ch in complet.CHAPITRES}
EXOS={1:CH1,2:CH2,**{n:ch.exercices for n,ch in CHS.items()}}
from revision_exercices import enrichir,DEFIS_CORRIGES,BILANS_CORRIGES
enrichir(EXOS)
BREAKS=set(json.loads((ROOT/'equilibrage-template.json').read_text(encoding='utf8')))

def tex(s):
    """Texte UTF-8, balisage pédagogique simple et symboles scientifiques."""
    s=html.unescape(str(s)).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
    parts=re.split(r'(<\/?(?:b|i|sup|sub)>|<br\s*/?>)',s)
    tags={'<b>':r'\textbf{','</b>':'}','<i>':r'\emph{','</i>':'}',
          '<sup>':r'\textsuperscript{','</sup>':'}','<sub>':r'\textsubscript{','</sub>':'}'}
    chars={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$',
           '#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}',
           '^':r'\textasciicircum{}','→':r'\(\rightarrow\)','←':r'\(\leftarrow\)',
           '↔':r'\(\leftrightarrow\)','≈':r'\(\approx\)','×':r'\(\times\)',
           '÷':r'\(\div\)','≤':r'\(\leq\)','≥':r'\(\geq\)','θ':r'\(\theta\)',
           '²':r'\textsuperscript{2}','³':r'\textsuperscript{3}',
           '₂':r'\textsubscript{2}','₃':r'\textsubscript{3}','₄':r'\textsubscript{4}'}
    out=[]
    for p in parts:
        if p in tags:out.append(tags[p])
        elif re.fullmatch(r'<br\s*/?>',p):out.append(r'\par ')
        else:out.append(''.join(chars.get(c,c) if c!='\n' else r'\par ' for c in p))
    return ''.join(out)

def para(s):return tex(s)+r'\par'+ '\n'
def box(label,body,kind='definition'):
    # La charte de Terminale porte les mêmes libellés, couleurs et filets.
    return rf'\begin{{pcEncadre}}{{{kind}}}{{{tex(label)}}}'+ '\n'+para(body)+r'\end{pcEncadre}'+'\n'
def questions(items):
    return '\\begin{questions}\n'+''.join('\\item '+tex(q)+'\n' for q in items)+'\\end{questions}\n'

figures={}; insertions=[]
def figure(spec,height=70,width=164,caption=''):
    # Réduction proportionnelle uniquement : aucune déformation des schémas.
    # Les dessins historiques adaptent leur tracé à la hauteur d'origine.
    height=float(height);width=float(width)
    key=json.dumps([spec,height,width],ensure_ascii=False,sort_keys=True)
    name=hashlib.sha256(key.encode()).hexdigest()[:16]
    if key not in figures:
        path=FIG/(name+'.pdf')
        if spec[0]=='revision':
            shutil.copy2(FIG/('revision-'+spec[1]+'.pdf'),path)
        else:
            c=canvas.Canvas(str(path),pagesize=(width*mm,height*mm),pageCompression=1)
            c.setTitle('OptiTAB - '+spec[0]);c.setAuthor('OptiTAB')
            draw(c,spec,0,0,width*mm,height*mm);c.save()
        figures[key]=dict(file=name+'.pdf',schema=spec,width=width,height=height)
    insertions.append(name)
    # Taille naturelle, avec une largeur maximale égale au bloc courant.
    return (rf'\pcFigure{{figures/{name}.pdf}}{{{tex(caption)}}}'+'\n')

class Capture:
    def __init__(self):
        self.pages=[];self.blocks=[];self.page=0;self.dest={};self.refs={}
        self.c=SimpleNamespace(bookmarkPage=lambda *a,**k:None,addOutlineEntry=lambda *a,**k:None)
    def begin(self,key,title,eyebrow='',**kw):
        self.page+=1;self.key=key
        self.blocks=[];self.pages.append(dict(key=key,title=title,eyebrow=eyebrow,meta=kw,blocks=self.blocks))
    def p(self,s,*args,**kw):
        if kw.get('measure'):return max(5,len(str(s))/65*4.5)
        if len(args)>3:kw['size']=args[3]
        self.blocks.append(('p',str(s),kw));return (args[1] if len(args)>1 else 0)+8
    def box(self,label,body,*args,**kw):self.blocks.append(('box',label,body,kw));return 0
    def fig(self,spec,top,h,**kw):self.blocks.append(('fig',spec,h,kw));return top+h
    def bullets(self,items,*args,**kw):self.blocks.append(('bullets',items,kw));return 0
    def table(self,rows,top,widths,**kw):self.blocks.append(('table',rows,widths,kw));return 0
    def section(self,n,title,*args,**kw):self.blocks.append(('section',n,title));return 0
    def rect(self,*args,**kw):pass
    def line(self,*args,**kw):pass
    def link(self,*args,**kw):pass
    def url(self,*args,**kw):pass

def table(rows,widths):
    total=sum(widths);n=len(widths)
    cols=''.join(r'>{\raggedright\arraybackslash}p{'+f'{(164-4.0*n)*w/total:.2f}'+r'mm}' for w in widths)
    result='\\begin{center}\n{\\renewcommand{\\arraystretch}{1.35}\\fontsize{11}{14}\\selectfont\n'
    result+='\\setlength{\\tabcolsep}{2mm}\\begin{tabular}{@{}'+cols+'@{}}\\toprule\n'
    for i,row in enumerate(rows):
        result+=' & '.join((r'\otTete{'+tex(s)+'}' if i==0 else tex(s)) for s in row)+r'\\'+ '\n'
        if i==0:result+=r'\midrule'+'\n'
    return result+r'\bottomrule\end{tabular}}\end{center}'+'\n'

def captured(page,skip_titles=False):
    out=[]
    for b in page['blocks']:
        kind=b[0]
        if kind=='p':
            s,kw=b[1:]
            if not s:continue
            if kw.get('font')=='Bold' and kw.get('size',12)>=14:
                out.append(r'\pcSousTitre{'+tex(s)+'}\n')
            else:out.append(para(s))
        elif kind=='box':
            label,body,kw=b[1:];accent=kw.get('accent')
            style='method' if accent==maquette.GREEN else 'attention' if accent==maquette.ORANGE else 'definition'
            out.append(box(label,body,style))
        elif kind=='fig':
            spec,h,kw=b[1:];out.append(figure(spec,h,kw.get('w',166),kw.get('caption','')))
        elif kind=='bullets':out.append(questions(b[1]))
        elif kind=='table':out.append(table(b[1],b[2]))
        elif kind=='section':out.append(r'\essSection{'+tex(b[1])+'}{'+tex(b[2])+'}\n')
    return ''.join(out).replace('}\\n','}\n')

def pcpage(title,subtitle='',label='',bookmark=False):
    s='\\pcPage{'+tex(title)+'}{'+tex(subtitle)+'}\n'
    if label:s+='\\phantomsection\\label{'+label+'}\n'
    if bookmark:s+='\\pdfbookmark[0]{'+tex(title)+'}{bm-'+label+'}\n'
    return s

def write_sources():
    from figures_revision import produire
    produire()
    for name in ('optitab-livre.sty','pc-livre.sty'):shutil.copy2(REF/name,OUT/name)
    for name in ('logo-blanc.png','logo-couleur.png'):shutil.copy2(ROOT/'images'/name,OUT/'images'/name)
    shutil.copy2(ROOT/'cinquieme-charte.tex',OUT/'cinquieme-charte.tex')
    # Ajustements de format uniquement, isolés du livre de Terminale.
    sty=(OUT/'optitab-livre.sty').read_text(encoding='utf8')
    sty=sty.replace(r'\fontsize{112}{112}',r'\fontsize{90}{90}').replace('at (21mm,46mm)','at (21mm,53mm)')
    sty=sty.replace(r'\noindent{\otLight\fontsize{30}{34}\selectfont\color{otInk}#1}\par',
                    r'\noindent{\otLight\fontsize{30}{34}\selectfont\color{otInk}\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000 #1\par}')
    start=sty.index('      \\node[anchor=base west,inner sep=0pt,text=white] at (24mm,27mm)')
    end=sty.index('    \\end{scope}',start)
    sty=sty[:start]+r'''      \node[anchor=south west,inner sep=0pt,text=white,text width=166mm,
        font=\otSemi\fontsize{25}{29}\selectfont,align=left] at (24mm,22mm)
        {\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000 #3\par};
      \node[anchor=south west,inner sep=0pt,text=white,opacity=0.82,text width=166mm,
        font=\otLight\fontsize{9.5}{12}\selectfont,align=left] at (24mm,7mm) {#5};
''' +sty[end:]
    sty=sty.replace(r'at (17mm,7.5mm) {#2};',r'at (17mm,7.5mm) {\parbox{112mm}{\raggedright #2}};')
    (OUT/'optitab-livre.sty').write_text(sty,encoding='utf8')
    cover=(REF/'couverture/premiere.tex').read_text(encoding='utf8')
    cover=cover.replace('Schémas de montages et de molécules','Schémas clairs et activités guidées')
    cover=cover.replace('Sujets type bac et préparation à l\'ECE','Quatre bilans pour faire le point')
    cover=cover.replace('exercices}}','exercices et}}').replace('corrigés}}','défis corrigés}}')
    # Une courbe simple de distance remplace le titrage de Terminale.
    a=cover.index('  % Repère et courbe');z=cover.index('  % Logo',a)
    cover=cover[:a]+r'''  % Trajectoire lumineuse et mesures de distance : décor de collège.
  \draw[white,opacity=0.2,line width=0.6pt] (105mm,18mm) -- (105mm,90mm) -- (210mm,90mm);
  \foreach \x in {117,137,157,177,197}{
    \draw[white,opacity=0.14] (\x mm,18mm) -- (\x mm,90mm);}
  \draw[otGreen,line width=2.2pt,line cap=round] (105mm,20mm) -- (205mm,83mm);
  \foreach \x/\y in {105/20,125/32.6,145/45.2,165/57.8,185/70.4,205/83}{
    \fill[white] (\x mm,\y mm) circle (1.5mm);}
''' +cover[z:]
    (OUT/'couverture.tex').write_text(cover,encoding='utf8')
    plan=[];number=1
    for i,(_,theme,chapters) in enumerate(PLAN,1):
        plan.append(r'\otPlanPartie{'+str(i)+'}{'+tex(theme)+'}\n')
        for title,_ in chapters:
            plan.append(r'\otPlanChap{'+str(number)+'}{'+tex(title)+'}{15}\n');number+=1
    (OUT/'plan.tex').write_text(''.join(plan),encoding='utf8')

    body=[r'''% Généré depuis les contenus pédagogiques du manuel complet.
\documentclass[12pt,twoside,openany]{book}
\usepackage{optitab-livre}
\usepackage{pc-livre}
\usepackage{adjustbox}
\input{cinquieme-charte}
\hypersetup{pdftitle={Physique-Chimie - Cinquième - Manuel complet},
 pdfsubject={Cours illustrés, activités, exercices progressifs et corrigés - Cycle 4 - 2026-2027},pdfauthor={OptiTAB}}
\begin{document}
\pagenumbering{alph}
\input{couverture}
\pagenumbering{arabic}
\pagestyle{otFront}
''']
    # Sommaire, dimensionné pour vingt chapitres et quatre thèmes.
    body.append(pcpage('Sommaire','Cinquième · Physique-chimie · Programme français de cycle 4','sommaire',True))
    body.append(r'\begingroup\setlength{\parskip}{0pt}'+'\n')
    number=1
    for i,(_,theme,chs) in enumerate(PLAN,1):
        body.append(r'\pcSomPartie{'+str(i)+'}{'+tex(theme)+'}\n')
        for title,_ in chs:
            body.append(r'\pcSomLigne{'+f'{number:02}'+'}{'+tex(title)+'}{chap-'+str(number)+'}\n');number+=1
    body.append(r'\vspace{3mm}\pcSomLigne{B}{Bilans des quatre thèmes}{bilans-debut}'+'\n')
    body.append(r'\pcSomLigne{C}{Corrigés détaillés}{corriges-debut}'+'\n')
    body.append(r'\pcSomLigne{i}{Méthodes, unités, lexique et références}{annexes-debut}'+'\n')
    body.append(r'\endgroup'+'\n')
    body.append(pcpage('Mode d’emploi','Une démarche pour comprendre, puis s’entraîner','mode',True))
    for lab,txt in [('1 · Observer','Décrire les faits, préciser les conditions et poser une question.'),
                    ('2 · Chercher','Formuler une hypothèse et proposer un test qui pourrait la mettre à l’épreuve.'),
                    ('3 · Mesurer','Choisir l’instrument, noter les résultats avec leurs unités et contrôler le protocole.'),
                    ('4 · Expliquer','Relier les observations aux connaissances et rédiger une conclusion argumentée.')]:
        body.append(box(lab,txt,'method' if lab[0] in '24' else 'definition'))
    body.append(r'\pcSousTitre{Trois niveaux pour progresser}'+'\n')
    for lev,title,txt in [(1,'Je démarre','Reconnaître, nommer et appliquer.'),(2,'Je m’entraîne','Lire un schéma, mesurer, calculer et expliquer.'),(3,'Je raisonne','Croiser des données, critiquer une méthode et argumenter.')]:
        body.append(r'\noindent\otDots{'+str(lev)+r'}\quad\textbf{'+tex(title)+r'}\enspace '+tex(txt)+r'\par\vspace{2mm}'+'\n')
    body.append(pcpage('Parcours et ressources','Retrouver une méthode et comprendre ses erreurs','ressources',True))
    for title,target in [('Travailler en sécurité','securite'),('Corrigés des exercices','corriges-debut'),('Bilans des quatre thèmes','bilans-debut'),('Mesurer et contrôler','methode-mesure'),('Construire et lire un graphique','methode-graphique'),('Calculer avec les unités','methode-calcul'),('Grandeurs et conversions','unites'),('Lexique scientifique','lexique'),('Programme et progression','programme'),('Références','references')]:
        body.append(r'\otLigneRessource{'+target+'}{'+tex(title)+'}\n')
    body.append(box('Une méthode qui fonctionne','Cherche d’abord seul, écris tes essais et explique ta réponse. Utilise le corrigé pour comprendre l’erreur, puis refais la question sans regarder la solution.','method'))
    body.append(box('Le cadre du manuel','Programme français du cycle 4 : BO du 30 juillet 2020, référence confirmée pour 2026-2027. La progression de 5e est un choix pédagogique. Manuel OptiTAB indépendant, sans validation institutionnelle revendiquée.'))
    cap=Capture();complet.front(cap)
    sec=next(p for p in cap.pages if p['key']=='securite')
    body.append(pcpage(sec['title'],'Démarche expérimentale','securite',True)+captured(sec))

    # Premiers chapitres : capture sémantique sans coordonnées de l'ancienne maquette.
    legacy={}
    for n,fn in ((1,ancien.cours1),(2,ancien.cours2)):
        c=Capture();fn(c);legacy[n]=c.pages
    defi_legacy={};cor_legacy={}
    for n in (1,2):
        c=Capture();ancien.defis(c,n);defi_legacy[n]=c.pages[0]
        c=Capture();ancien.corriges(c,n,EXOS[n]);cor_legacy[n]=next(p for p in c.pages if p['key']==f'cor-defi-{n}')
    for n in range(1,21):
        body.append(r'\clearpage\pagestyle{otMain}'+'\n')
        if n<3:
            blocks=legacy[n][0]['blocks'];question=blocks[0][1]
            objectifs=next(b[1] for b in blocks if b[0]=='bullets')
        else:question=CHS[n].question;objectifs=CHS[n].objectifs
        part=1 if n<=8 else 2 if n<=11 else 3 if n<=16 else 4
        body.append(r'\begin{ouverture}[college'+str(part)+']{'+str(n)+'}{'+tex(TITRES[n])+'}{Partie '+str(part)+' · '+tex(THEMES[n])+'}{'+tex(question)+'}\n')
        for o in objectifs:body.append(r'\objectif{'+tex(o)+'}\n')
        body.append(r'\end{ouverture}'+'\n')
        if n<3:
            for k,p in enumerate(legacy[n][1:]):
                body.append(pcpage('L’essentiel' if k==0 else p['title'],TITRES[n],p['key']))
                if k==0:body.append(r'\phantomsection\label{ess-'+str(n)+'}\n')
                body.append(r'\begin{pcFiche}{'+p['key']+'}\n'+captured(p)+r'\end{pcFiche}'+'\n')
        else:
            ch=CHS[n]
            for k,le in enumerate(ch.lecons,1):
                body.append(pcpage('L’essentiel',f'Chapitre {n:02} · {TITRES[n]}',f'ch-{n}-cours-{k}'))
                if k==1:body.append(r'\phantomsection\label{ess-'+str(n)+'}\n')
                content=r'\essSection{'+str(k)+'}{'+tex(le.titre)+'}\n'+para(le.texte)
                content+=figure(le.schema,70,166,le.legende)
                content+=box('À retenir',le.retenir)+box('Une méthode concrète',le.methode,'method')
                body.append(r'\begin{pcFiche}{'+f'cours-{n}-{k}'+'}\n'+content+r'\end{pcFiche}'+'\n')
            ac=ch.activite
            body.append(pcpage('Activité expérimentale',ac.titre,f'ch-{n}-activite'))
            content=box('Mission',ac.mission,'method')+questions(ac.etapes)+figure(ac.schema,65,166,ac.legende)+questions(ac.questions)
            body.append(r'\begin{pcFiche}{activite-'+str(n)+'}\n'+content+r'\end{pcFiche}'+'\n')
            body.append(pcpage('L’essentiel à retenir',f'Chapitre {n:02} · Synthèse et autoévaluation',f'ch-{n}-bilan'))
            content=''.join(box('Repère '+str(k),s,'definition' if k%2 else 'method') for k,s in enumerate(ch.bilan,1))
            content+=box('Une erreur à éviter',ch.erreur,'attention')
            body.append(r'\begin{pcFiche}{synthese-'+str(n)+'}\n'+content+r'\end{pcFiche}'+'\n')
        # Trois rubriques aux niveaux identiques à la maquette validée.
        for level,title,items in [(1,'Je démarre',EXOS[n][:5]),(2,'Je m’entraîne',EXOS[n][5:11]),(3,'Je raisonne',EXOS[n][11:])]:
            if level==1:body.append('\\clearpage\\markright{Exercices}\n')
            for index,e in enumerate(items):
                if f'exo-{n}-{e.n}' in BREAKS:body.append('\\clearpage\n')
                body.append(r'\begin{blocLivre}{exo-'+f'{n}-{e.n}'+'}\n')
                # La rubrique reste avec son premier exercice. Les niveaux se
                # suivent, comme dans le modèle de Terminale, si la place suffit.
                if index==0:body.append(r'\rubrique{'+tex(title)+'}\n')
                body.append(r'\begin{exercice}['+str(level)+']{'+tex(e.titre)+'}\n')
                if e.document:body.append(r'\begin{donnees}'+para(e.document)+r'\end{donnees}'+'\n')
                if e.figure:body.append(figure(e.figure,e.hauteur or 65,166,e.caption))
                body.append(questions(e.questions)+r'\end{exercice}\end{blocLivre}'+'\n')
        if n<3:
            p=defi_legacy[n]
            body.append(pcpage('Défi · Prendre une initiative',p['title'],f'defi-ex-{n}'))
            body.append(r'\begin{pcFiche}{defi-'+str(n)+'}\n'+captured(p)+r'\end{pcFiche}'+'\n')
        else:
            d=CHS[n].defi
            body.append(pcpage('Défi · Prendre une initiative',d.titre,f'defi-ex-{n}'))
            content=para(d.situation)+figure(d.schema,70)+questions(d.questions)+box('Indice progressif',d.aide,'method')
            body.append(r'\begin{pcFiche}{defi-'+str(n)+'}\n'+content+r'\end{pcFiche}'+'\n')

    body.append(r'\clearpage\gdef\otChapNum{0}\pagestyle{otFront}'+'\n')
    body.append(pcpage('Bilans des quatre thèmes','Mobiliser ses connaissances dans des situations variées','bilans-debut',True))
    body.append(para('Ces quatre bilans proposent cinq missions chacun. Pour chaque mission, réponds aux deux questions et justifie ta réponse. Un barème indicatif est proposé dans les corrigés.'))
    for letter,title,_ in BILANS:body.append(r'\otLigneRessource{bilan-'+letter+'}{'+tex('Bilan '+letter+' · '+title)+'}\n')
    body.append(box('Relire avant de corriger','Ai-je précisé les conditions, les unités, le sens des flèches et les étapes du raisonnement ? Une valeur juste sans explication ne répond pas toujours à toute la question.','method'))
    for letter,title,items in BILANS:
        body.append(pcpage('Bilan '+letter,title,'bilan-'+letter))
        body.append(r'\begin{pcFiche}{bilan-'+letter+'}\n')
        for e in items:
            body.append(r'\begin{blocLivre}{mission-'+letter+'-'+str(e.n)+'}\n')
            body.append(r'\pcMission{'+letter+'}{'+str(e.n)+'}{'+tex(e.titre)+'}\n')
            if e.document:body.append(box('Document',e.document))
            # Le schéma des changements d’état donnerait la réponse à A.1.
            # Il accompagne sa correction ; les autres documents utiles restent ici.
            if e.figure and (letter,e.n)!=('A',1):body.append(figure(e.figure,60))
            body.append(questions(e.questions)+r'\end{blocLivre}'+'\n')
        body.append(r'\end{pcFiche}'+'\n')

    body.append(r'\partieCorriges'+'\n')
    annex=Capture();annexes(annex)
    a12=next(p for p in annex.pages if p['key']=='solutions-1')
    for n in range(1,21):
        body.append('\\clearpage\\corrigesChapitre{'+str(n)+'}{'+tex(TITRES[n])+'}\n')
        for e in EXOS[n]:
            if f'cor-{n}-{e.n}' in BREAKS:body.append('\\clearpage\n')
            body.append(r'\begin{blocLivre}{cor-'+f'{n}-{e.n}'+'}\n')
            body.append(r'\begin{corrige}{'+str(e.n)+'}{'+tex(e.titre)+'}\n'+para(e.reponse))
            if e.methode:body.append(box('Pour comprendre',e.methode,'method'))
            if e.figure_correction:body.append(figure(e.figure_correction,65,166,'Modèle de correction · les proportions sont indicatives sauf mention contraire.'))
            body.append(r'\end{corrige}\end{blocLivre}'+'\n')
        body.append(pcpage('Activité et défi',f'Chapitre {n:02} · Éléments de réponse',f'solutions-{n}'))
        body.append(r'\begin{pcFiche}{solutions-'+str(n)+'}\n')
        if n<3:
            b=a12['blocks'][n-1]
            body.append(box(b[1],b[2],'method'))
            body.append(r'\pcRetour{ch-'+str(n)+'-activite}{Revenir à l’activité}'+'\n')
            body.append(r'\phantomsection\label{defi-cor-'+str(n)+'}\n')
            body.append(r'\pcSousTitre{'+tex(cor_legacy[n]['title'])+'}\n')
            body.append(captured(cor_legacy[n]))
        else:
            ch=CHS[n]
            body.append(box(ch.activite.titre,ch.activite.correction,'method'))
            body.append(r'\pcRetour{ch-'+str(n)+'-activite}{Revenir à l’activité}'+'\n')
            body.append(r'\phantomsection\label{defi-cor-'+str(n)+'}\n')
            body.append(box(ch.defi.titre,ch.defi.correction))
            if n in DEFIS_CORRIGES:body.append(figure(DEFIS_CORRIGES[n],65,166,'Construction ou modèle de correction.'))
        body.append(r'\pcRetour{defi-ex-'+str(n)+'}{Revenir au défi}'+'\n')
        body.append(r'\end{pcFiche}'+'\n')
    body.append(r'\clearpage\gdef\otChapNum{0}\pagestyle{otFront}'+'\n')
    for letter,title,items in BILANS:
        body.append(pcpage('Corrigé du bilan '+letter,title,'cor-bilan-'+letter))
        body.append(para('Barème indicatif : 2 points pour chaque réponse correcte et justifiée. Pour un calcul, valoriser la méthode et l’unité ; pour une explication, les idées exactes et reliées.'))
        for e in items:
            body.append(r'\begin{blocLivre}{cor-mission-'+letter+'-'+str(e.n)+'}\n')
            body.append(r'\pcSolutionMission{'+letter+'}{'+str(e.n)+'}{'+tex(e.titre)+'}\n'+para(e.reponse)+r'\end{blocLivre}'+'\n')
            # Le dessin et la réponse restent dans un seul bloc insécable.
            if (letter,e.n) in BILANS_CORRIGES:
                body[-1]=body[-1].replace(r'\end{blocLivre}',figure(BILANS_CORRIGES[letter,e.n],65,166,'Modèle de correction.')+r'\end{blocLivre}')
            if e is items[-1]:
                body[-1]=body[-1].replace(r'\end{blocLivre}',box('Utiliser le résultat','Repère la connaissance ou la méthode à reprendre. Reviens au chapitre concerné, puis refais une mission sans regarder la solution avant de comparer.','method')+r'\end{blocLivre}')
    body.append(r'\clearpage\gdef\otChapNum{0}\gdef\otAccent{otNavy}\pagestyle{otFront}\phantomsection\label{annexes-debut}'+'\n')
    for p in annex.pages:
        if p['key']=='solutions-1' or p['key'].startswith('lexique-'):continue
        body.append(pcpage('Grandeurs et unités' if p['key']=='unites' else p['title'],p['eyebrow'],p['key'],p['key'] in ['methode-mesure','unites','competences']))
        body.append(r'\begin{pcFiche}{annexe-'+p['key']+'}\n'+captured(p)+r'\end{pcFiche}'+'\n')
    body.append(pcpage('Lexique scientifique','80 mots pour comprendre et expliquer','lexique',True))
    entries=sorted(LEXIQUE,key=lambda q:unicodedata.normalize('NFKD',q[0]).encode('ascii','ignore').decode().lower())
    for term,definition,n in entries:
        body.append(r'\begin{pcLexique}{'+tex(term)+'}{'+str(n)+'}\n'+para(definition)+r'\end{pcLexique}'+'\n')
    body.append(pcpage('Programme et progression','Les choix du manuel','programme',True))
    body.append(para('Le programme national définit les attendus sur les trois années du cycle 4. Ce manuel propose une progression complète pour la 5e, construite à partir des repères de début de cycle. L’équipe pédagogique peut organiser les apprentissages autrement.'))
    body.append(table([['Thème du programme','Chapitres'],['Organisation et transformations de la matière','1 à 8'],['Mouvement et interactions','9 à 11'],['Énergie, transferts et conversions','12 à 16'],['Signaux pour observer et communiquer','17 à 20']],[130,36]))
    body.append(box('Une progression sur trois années','Les modèles atomiques détaillés, les équations de réaction, la grandeur quotient masse volumique, la modélisation formelle des forces et les lois électriques sont approfondis aux niveaux suivants. Ici, les circuits, les interactions et les transferts d’énergie sont étudiés surtout par observations et raisonnements simples.','method'))
    body.append(para('Le titre « manuel complet » désigne cette progression de 5e ; il ne prétend pas traiter à lui seul tous les attendus de fin de 3e.'))
    body.append(pcpage('Références','Sources consultées le 23 octobre 2026','references',True))
    for i,(title,desc,url) in enumerate(SOURCES+SOURCES_COMPLEMENTAIRES,1):
        body.append(r'\begin{blocLivre}{source-'+str(i)+'}\n')
        body.append(r'\pcSousTitre{'+str(i)+'. '+tex(title)+'}\n'+para(desc))
        body.append(r'{\otLight\fontsize{9}{12}\selectfont\color{otMuted}\url{'+url+r'}}\par\end{blocLivre}'+'\n')
    body.append(box('Créations originales','Textes, exercices, corrigés et schémas sont des créations pour cet ouvrage. Les documents officiels servent de références de programme et de démarche. Les séries annoncées comme pédagogiques sont des exemples à exploiter, pas des mesures effectuées par l’élève.'))
    body.append(r'\end{document}'+'\n')
    source=''.join(body).replace('}\\n','}\n').replace('\\par\\n','\\par\n')
    (OUT/'main.tex').write_text(source,encoding='utf8')
    manifest=dict(chapitres=20,exercices=sum(map(len,EXOS.values())),defis=20,bilans=4,missions=20,lexique=len(LEXIQUE),figures=list(figures.values()),insertions=len(insertions),style_reference=str(REF/'optitab-livre.sty'))
    (BUILD/'contenu.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in manifest.items() if k!='figures'},ensure_ascii=False),flush=True)

def compile_book():
    def aux_hash():
        p=BUILD/'main.aux'
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    for index in range(1,6):
        before=aux_hash();print(f'LuaLaTeX : passe {index}',flush=True)
        run=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-aux-directory=build','main.tex'],cwd=OUT,capture_output=True)
        output=(run.stdout+run.stderr).decode('utf8',errors='replace')
        (BUILD/f'compilation-{index}.txt').write_text(output,encoding='utf8')
        log=(BUILD/'main.log').read_text(encoding='utf8',errors='replace')
        if 'Output written on main.pdf' not in log or 'Fatal error' in log:
            raise RuntimeError(output[-4500:])
        if not any(t in log for t in ('Label(s) may have changed','undefined references')) and before==aux_hash():break
    else:raise RuntimeError('Renvois non stabilisés après cinq passes.')
    problems=[line for line in log.splitlines() if any(t in line for t in ('Overfull','Missing character','multiply defined','PCFICHE-TROP'))]
    (BUILD/'alertes-typographiques.json').write_text(json.dumps(problems,ensure_ascii=False,indent=2),encoding='utf8')
    print(re.search(r'Output written on main.pdf[^\n]*',log).group(0),flush=True)
    print(f'Alertes typographiques : {len(problems)}',flush=True)
    if problems:print('\n'.join(problems[:30]),flush=True)

if __name__=='__main__':
    write_sources();compile_book()
