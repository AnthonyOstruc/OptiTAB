"""Construit le livre CP : PDF vectoriel A4, sommaire et renvois cliquables."""
from pathlib import Path
import json,html,shutil,hashlib,re
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import modele
import contenu_nombres,contenu_calcul,contenu_mesures_geometrie
from modele import CHAPITRES,SOURCES
from ressources import BILANS,COUVERTURE,problemes_oraux
from dessins import diagram

ROOT=Path(__file__).resolve().parent;BUILD=ROOT/'build';BUILD.mkdir(exist_ok=True)
ASSETS=ROOT/'images';ASSETS.mkdir(exist_ok=True)
for f in ['logo-couleur.png','logo-blanc.png']:
    if not (ASSETS/f).exists():shutil.copy2(ROOT.parent/'livre-cm1/images'/f,ASSETS/f)
for name,file in [('Text','arial.ttf'),('Bold','arialbd.ttf'),('Italic','ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Text',normal='Text',bold='Bold',italic='Italic',boldItalic='Bold')
W,H=210*mm,297*mm
NAVY=HexColor('#1B3C8E');INK=HexColor('#1C2130');GREEN=HexColor('#3B8544')
MUTED=HexColor('#59657A');RULE=HexColor('#D5DAE3');PALE=HexColor('#F0F4FB');MINT=HexColor('#EFF6EF');CREAM=HexColor('#FCF4E6')

class Livre:
    def __init__(self,path,refs=None):
        self.c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
        self.c.setTitle('OptiTAB - Mathématiques CP - Livre pédagogique')
        self.c.setAuthor('Collection OptiTAB');self.c.setSubject('Cours, schémas, exercices et corrigés - France 2026-2027')
        self.page=0;self.pages=[];self.dest={};self.refs=refs or {};self.current=None;self.textblocks=[];self.figureblocks=[];self.figures=0
    def text(self,s,x,top,w,size=14,leading=None,bold=False,color=INK,maxbottom=279):
        if not s:return top
        s=html.escape(str(s)).replace('\n','<br/>')
        s=re.sub(r' ([?!:;])',lambda m:'\u00a0'+m.group(1),s)
        s=re.sub(r'(\d) (cm|m|€)(?=\W|$)',lambda m:m.group(1)+'\u00a0'+m.group(2),s)
        st=ParagraphStyle('p',fontName='Bold' if bold else 'Text',fontSize=size,leading=leading or size*1.34,textColor=color,spaceAfter=0)
        p=Paragraph(s,st);pw,ph=p.wrap(w*mm,1000)
        bottom=top+ph/mm
        if bottom>maxbottom+.1:raise ValueError(f'Page {self.page} {self.current}: texte hors zone {bottom:.1f} : {s[:80]}')
        p.drawOn(self.c,x*mm,H-top*mm-ph)
        self.textblocks.append(dict(page=self.page,x=x,top=top,w=w,h=ph/mm,texte=html.unescape(s)))
        return bottom
    def rect(self,x,top,w,h,fill=PALE,stroke=None,r=3):
        self.c.setFillColor(fill);self.c.setStrokeColor(stroke or fill)
        self.c.roundRect(x*mm,H-(top+h)*mm,w*mm,h*mm,r*mm,stroke=bool(stroke),fill=1)
    def line(self,x1,top,x2,color=RULE,width=.65):
        self.c.setStrokeColor(color);self.c.setLineWidth(width);self.c.line(x1*mm,H-top*mm,x2*mm,H-top*mm)
    def fig(self,spec,top,h=40,x=23,w=164):
        if not spec:return
        if top+h>279:raise ValueError(f'Figure hors zone page {self.page}, {self.current}: {top+h:.1f} mm')
        diagram(self.c,spec,x*mm,H-(top+h)*mm,w*mm,h*mm);self.figures+=1
        self.figureblocks.append(dict(page=self.page,cle=self.current,figure=spec,x=x,top=top,w=w,h=h))
    def lines(self,top,h=20,x=27,w=156):
        for yy in range(0,int(h),8):self.line(x,top+yy,x+w)
    def begin(self,key,title,eyebrow='MATHÉMATIQUES CP',subtitle='',adult=False):
        if self.page:self.c.showPage()
        self.page+=1;self.current=key;self.dest[key]=self.page
        self.c.bookmarkPage(key)
        self.pages.append(dict(numero=self.page,cle=key,titre=title,adulte=adult))
        self.c.setFillColor(GREEN);self.c.rect(0,H-5*mm,W,5*mm,stroke=0,fill=1)
        self.c.drawImage(str(ASSETS/'logo-couleur.png'),17*mm,H-23*mm,width=31*mm,height=11*mm,preserveAspectRatio=True,mask='auto')
        self.text('MATHÉMATIQUES  /  CP',125,15,68,9.2,bold=True,color=NAVY)
        self.line(17,29,193)
        self.text(eyebrow.upper(),17,37,176,10,bold=True,color=GREEN)
        end=self.text(title,17,47,176,23,leading=27,bold=True,color=NAVY)
        if subtitle:self.text(subtitle,17,end+4,176,11.2,color=MUTED)
        self.line(17,283,193)
        self.c.setFont('Text',9);self.c.setFillColor(MUTED)
        self.c.drawString(17*mm,9*mm,'OptiTAB · CP · France 2026-2027')
        self.c.drawRightString(193*mm,9*mm,str(self.page))
        if adult:self.c.drawCentredString(105*mm,9*mm,'Pour l’adulte')
    def box(self,label,body,top,h,fill=PALE,size=14):
        self.rect(17,top,176,h,fill)
        self.text(label,23,top+5,164,10.5,bold=True,color=GREEN)
        self.text(body,23,top+13,164,size,maxbottom=top+h-3)
    def link(self,key,x,top,w,h):
        self.c.linkRect('',key,(x*mm,H-(top+h)*mm,(x+w)*mm,H-top*mm),relative=0,thickness=0)
    def outline(self,title,key,level=0):self.c.addOutlineEntry(title,key,level=level,closed=level==0)

def couverture(b):
    c=b.c;b.page=1;b.current='couverture';b.dest['couverture']=1;b.pages.append(dict(numero=1,cle='couverture',titre='Couverture',adulte=False))
    c.bookmarkPage('couverture');c.setFillColor(NAVY);c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(HexColor('#122A66'));p=c.beginPath();p.moveTo(0,0);p.lineTo(W,0);p.lineTo(W,140*mm);p.curveTo(125*mm,100*mm,75*mm,150*mm,0,105*mm);p.close();c.drawPath(p,stroke=0,fill=1)
    c.drawImage(str(ASSETS/'logo-blanc.png'),20*mm,H-35*mm,width=48*mm,height=18*mm,preserveAspectRatio=True,mask='auto')
    b.text('LE LIVRE POUR APPRENDRE ET COMPRENDRE',20,49,172,10.3,bold=True,color=white)
    b.text('Mathématiques',20,68,174,35,leading=40,bold=True,color=white)
    b.text('CP',18,91,170,91,leading=99,bold=True,color=white)
    b.text('Je manipule. Je dessine.\nJe calcule. J’explique.',21,137,164,20,leading=27,color=white)
    b.rect(20,174,170,23,fill=HexColor('#244A9F'))
    b.text('30 chapitres illustrés · 270 exercices\n5 bilans · 360 problèmes oraux · Corrigés',26,180,159,13.4,leading=19,color=white)
    # Une collection visuelle lisible, sans décor parasite sur les pages de travail.
    c.saveState();c.setFillColor(white)
    for i in range(10):
        x=27+(i%5)*16;y=220+(i//5)*16
        c.setStrokeColor(HexColor('#9EB4DC'));c.roundRect(x*mm,H-(y+14)*mm,14*mm,14*mm,2*mm,stroke=1,fill=0)
        if i<8:c.setFillColor(HexColor('#8BC58B'));c.circle((x+7)*mm,H-(y+7)*mm,3.4*mm,stroke=0,fill=1)
    c.restoreState();b.text('8 = 5 + 3',124,231,60,21,bold=True,color=white)
    b.text('COLLECTION OPTITAB',20,267,120,10,bold=True,color=white)
    b.text('France · Édition 2026-2027',20,273,170,11,color=white)
    b.outline('Bienvenue dans le livre de CP','couverture')

def liminaires(b):
    b.begin('bienvenue','Mon livre de mathématiques','BIENVENUE',subtitle='Un parcours pour chercher, comprendre et progresser.')
    b.box('CE LIVRE APPARTIENT À','Prénom : ........................................................\nClasse : ............................................................',82,40)
    b.text('Tu peux prendre le temps de chercher.',20,133,170,20,bold=True,color=NAVY)
    t=155
    for lab,body in [('Je manipule','J’utilise des jetons, des cubes, une règle ou une horloge.'),('Je dessine','Je fais un schéma pour voir ce qui se passe.'),('Je raconte','J’explique avec mes mots ce que je comprends.'),('Je vérifie','Je contrôle ma réponse et j’essaie encore si besoin.')]:
        b.text(lab,22,t,165,15,bold=True,color=GREEN);t=b.text(body,22,t+9,165,14)+9
    b.begin('mode','Comment utiliser ce livre','POUR L’ADULTE',adult=True)
    sections=[('Une lecture accompagnée','Lire les consignes à voix haute aussi longtemps que nécessaire. La lecture autonome ne doit pas empêcher l’enfant de montrer ce qu’il comprend en mathématiques. Accepter une réponse orale, un geste ou une manipulation avant l’écriture.'),('Un chapitre, plusieurs séances','Découverte : manipuler et parler. Leçon : reprendre le schéma et l’exemple. Entraînement : choisir quelques exercices, puis y revenir. Les trois pages d’exercices ne constituent pas une séance unique.'),('Observer pour mieux aider','Demander « Comment as-tu fait ? ». Si une réponse est fausse, reprendre un cas plus simple avec des objets. Faire ensuite essayer une nouvelle situation proche. Le corrigé donne une démarche possible, pas une seule façon autorisée.'),('Une année, des reprises','Alterner nombres, problèmes, mesures et géométrie. Reprendre les faits numériques tous les jours. Consacrer au moins deux tiers du temps aux nombres, au calcul et aux problèmes. Le rangement du livre par chapitre ne constitue pas un emploi du temps.'),('Le support','A4, impression en taille réelle à 100 %. Le repère de longueur en annexe permet de vérifier l’échelle. Les pages de matériel sont à photocopier. Les couleurs aident au repérage ; les quantités restent lisibles en noir et blanc.')]
    t=80
    for lab,body in sections:
        b.text(lab,19,t,172,13,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.7,leading=16)+9
    b.begin('progression','Une progression sur cinq périodes','POUR L’ADULTE',adult=True)
    periods=[('P1 · Installer le nombre','Ch. 1 à 8. Dénombrer, ajouter, enlever, construire la dizaine et les nombres jusqu’à 20. Rangs et motifs. En parallèle : formes et règle (25), positions (28), comparaison de masses par manipulation (23).'),('P2 · Étendre jusqu’à 59','Ch. 9 à 12, avec les calculs dans le champ connu. Lire, écrire, comparer ; doubles et moitiés. Débuter la monnaie (21) et la mesure de longueurs (22). Réinvestir les petites histoires parties-tout (17).'),('P3 · Étendre jusqu’à 100','Ch. 13 à 19 : nombres, calculs et problèmes ; échanges de dizaines. Reprendre 11 et 12 jusqu’à 100. Heures entières (24), solides (27), longueurs et masses. Les chapitres 17 à 19 se construisent progressivement.'),('P4 · Relier les connaissances','Ch. 20 : problèmes en deux étapes avec des nombres jusqu’à 30. Ch. 30 : addition posée après les procédures mentales. Constructions (26), enquêtes (29) et déplacements (28). Reprendre les autres domaines.'),('P5 · Consolider et transférer','Reprises ciblées dans tous les chapitres, jeux, nouvelles enquêtes et situations concrètes. Achever l’addition posée si elle n’a pas été introduite en P4. Bilan final en plusieurs moments ; retour sur les difficultés repérées.')]
    t=81
    for lab,body in periods:
        b.text(lab,19,t,172,13,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.6,leading=15.3)+9
    b.box('RITUEL DE PROBLÈMES','La banque contient 36 semaines de 10 problèmes à lire à voix haute. Adapter le champ numérique aux acquis ; répartir les problèmes sur la semaine et faire expliquer les démarches.',238,35,size=11.5)
    # Sommaire : deux pages, 15 chapitres par page.
    for part in range(2):
        b.begin(f'sommaire-{part+1}','Sommaire' if part==0 else 'Sommaire et ressources','PARCOURS DU LIVRE',subtitle='Les titres et numéros de page sont cliquables.')
        if part==0:b.outline('Sommaire','sommaire-1')
        t=83
        for c in CHAPITRES[part*15:(part+1)*15]:
            key=f'ch-{c.numero}-decouverte';num=b.refs.get(key,'…')
            b.text(f'{c.numero:02d}',19,t,12,12,bold=True,color=GREEN)
            b.text(c.titre,34,t,142,12.2);b.text(str(num),179,t,14,12,bold=True,color=NAVY)
            b.link(key,18,t,176,9);t+=9.5
        if part==1:
            t+=6
            for title,key in [('Les cinq bilans','bilan-1-1'),('Les corrigés expliqués','corriges-intro'),('360 problèmes oraux pour l’adulte','oral-intro'),('Matériel et fiches outils','outils-intro'),('Programme et sources officielles','couverture-programme-1')]:
                b.text(title,20,t,155,11.5,bold=True,color=NAVY);b.text(str(b.refs.get(key,'…')),179,t,15,11.5);b.link(key,18,t,176,8);t+=8
    b.begin('rituel','Un petit rituel pour apprendre','POUR L’ADULTE',adult=True)
    t=82
    for lab,body in [('1. Montrer et dire','Présenter un petit nombre, une décomposition ou une situation. Demander à l’enfant de décrire ce qu’il voit et ce qu’il cherche.'),('2. Enseigner une méthode','Modéliser la démarche à voix haute, avec des objets si nécessaire. Faire essayer immédiatement une situation proche et expliciter le lien entre objets, dessin et calcul.'),('3. S’entraîner brièvement','Choisir quelques questions variées et proposer des reprises espacées. La vitesse vient après la compréhension et la mémorisation.'),('4. Mesurer ses progrès','En fin de CP, le programme donne des repères de fluence : 8 faits d’addition en 1 minute, 8 doubles ou moitiés usuels en 1 minute ; 9 calculs par procédure en 3 minutes. Utiliser les fiches outils seulement après l’apprentissage.'),('5. Réinvestir','Lire les problèmes oraux sans indiquer l’opération. Autoriser le matériel, demander une réponse avec l’unité et faire vérifier sa cohérence. Varier les quantités et les contextes.')]:
        b.text(lab,19,t,172,13,bold=True,color=GREEN);t=b.text(body,19,t+9,172,12,leading=16)+10
    b.begin('suivi','Mes progrès','À COMPLÉTER AVEC L’ADULTE',subtitle='Je peux réussir avec du matériel, avec un schéma, puis sans aide.')
    t=82
    for label in ['Compter et représenter une quantité','Lire et écrire les nombres','Comparer et placer les nombres','Expliquer une addition ou une soustraction','Calculer avec une méthode','Résoudre une petite histoire','Mesurer et utiliser la monnaie','Lire une heure entière','Reconnaître et construire des formes','Suivre un déplacement','Faire une enquête et un graphique']:
        b.text(label,20,t,138,12.6);b.c.setStrokeColor(RULE)
        for x in [165,176,187]:b.c.rect(x*mm,H-(t+4)*mm,4*mm,4*mm)
        b.line(19,t+10,193);t+=15
    b.text('Les trois cases permettent de noter une réussite à trois dates différentes.\nDates : ........................ / ........................ / ........................',20,257,172,10.7,color=MUTED)

def chapitre(b,c):
    n=c.numero;key=f'ch-{n}-decouverte'
    b.begin(key,c.titre,f'CHAPITRE {n:02d} · {c.domaine}',subtitle='Je découvre avec des objets.')
    b.outline(f'{n:02d}. {c.titre}',key)
    b.box('MON OBJECTIF',c.objectif,83,29)
    b.text('Je prépare',20,121,169,12,bold=True,color=GREEN)
    b.text(c.materiel,20,130,169,13)
    b.box('JE MANIPULE ET JE RACONTE',c.manipulation,151,49,fill=MINT,size=14)
    b.fig(c.figure,207,48)
    b.text('Observe le schéma. Montre ce que tu reconnais et explique-le.',22,263,166,12.4,color=MUTED)
    b.begin(f'ch-{n}-lecon',c.titre,f'CHAPITRE {n:02d} · JE RETIENS',subtitle='Je comprends, puis j’essaie avec l’adulte.')
    t=83
    for i,rule in enumerate(c.lecon,1):
        b.rect(17,t,176,29,fill=PALE if i%2 else MINT)
        b.text(str(i),22,t+6,10,16,bold=True,color=GREEN)
        b.text(rule,35,t+5,151,14,maxbottom=t+27);t+=33
    b.box('UN EXEMPLE EXPLIQUÉ',c.exemple,185,39,fill=CREAM,size=13.3)
    b.box('À TOI, AVEC L’ADULTE',c.guide,231,39,fill=MINT,size=14)
    b.text('Je dis ce que j’ai fait et je vérifie ma réponse.',22,274,165,10.5,color=MUTED)
    if n==11:
        b.begin('ch-11-moitie','Chercher une moitié','CHAPITRE 11 · MÉTHODE À REPRENDRE EN P3',subtitle='Je décompose pour utiliser les moitiés que je connais.')
        b.box('DEUX PARTS ÉGALES','Je partage chaque morceau en deux, puis je réunis une moitié de chaque morceau.',83,31,size=13.7)
        b.box('EXEMPLE 1 · LA MOITIÉ DE 46','46 = 40 + 6.\nLa moitié de 40 est 20. La moitié de 6 est 3.\n20 + 3 = 23. La moitié de 46 est 23.',122,51,fill=MINT,size=14)
        b.box('EXEMPLE 2 · LA MOITIÉ DE 38','38 = 20 + 18.\nLa moitié de 20 est 10. La moitié de 18 est 9.\n10 + 9 = 19. La moitié de 38 est 19.',181,51,fill=CREAM,size=14)
        b.box('À FAIRE ENSEMBLE','Cherche la moitié de 54, puis la moitié de 72.\nDécompose en nombres faciles à partager.',240,36,size=13.5)
    for j in range(3):
        b.begin(f'ch-{n}-ex-{j+1}',c.titre,f'CHAPITRE {n:02d} · '+['JE COMMENCE','JE M’ENTRAÎNE','JE CHERCHE'][j],subtitle='Date : ..................................   Prénom : ..................................')
        if n==29 and j==0:
            exercices_page(b,c.exercices[:2],chapter=n)
            b.begin('ch-29-graphique','Le graphique de mon enquête','CHAPITRE 29 · JE CONSTRUIS',subtitle='Je reprends les résultats de mon tableau.')
            b.rect(17,83,9,9,fill=NAVY,r=2);b.text('3',19,84.2,6,12,bold=True,color=white);b.link('cor-29',17,83,9,9)
            b.text(c.exercices[2].consigne,30,83,160,14.1,leading=18.6)
            b.fig(c.exercices[2].figure,109,140,x=28,w=160)
            b.text('Une case coloriée représente le vote d’une personne.',24,257,164,13.2,bold=True,color=GREEN)
            continue
        exercices_page(b,c.exercices[j*3:(j+1)*3],start_number=j*3+1,chapter=n)

def exercices_page(b,items,start_number=1,chapter=None):
    t=83
    for j,e in enumerate(items):
        num=start_number+j
        b.rect(17,t,9,9,fill=NAVY,r=2);b.text(str(num),19,t+1.2,6,12,bold=True,color=white)
        end=b.text(e.consigne,30,t,160,14.1,leading=18.6,maxbottom=t+28)
        if e.figure:
            # 38 mm pour les figures ; les réponses sont portées sur le dessin ou sous le schéma.
            height=39 if e.figure[0] not in ['columnblank'] else 40
            b.fig(e.figure,end+2,height,x=28,w=160)
            bottom=end+height+4
            if bottom<t+61:b.lines(bottom+1,h=max(0,t+61-bottom-1),x=31,w=157)
        else:b.lines(end+12,h=max(8,t+58-end-12),x=31,w=157)
        if chapter:
            key=f'cor-{chapter}'
            b.link(key,17,t,9,9)
        if j<2:b.line(17,t+65,193)
        t+=67

def bilans(b):
    for i,(title,after,items) in enumerate(BILANS,1):
        for j in range(2):
            key=f'bilan-{i}-{j+1}';b.begin(key,title,f'BILAN {i} · '+('PREMIÈRE PARTIE' if j==0 else 'DEUXIÈME PARTIE'),subtitle='À proposer en plusieurs moments, sans aide au départ.')
            if j==0:b.outline(title,key)
            exercices_page(b,items[j*3:(j+1)*3],start_number=j*3+1)

def corriges(b):
    b.begin('corriges-intro','Comprendre les réponses','CORRIGÉS ET ACCOMPAGNEMENT',adult=True)
    b.outline('Corrigés expliqués','corriges-intro')
    b.box('POUR UTILISER LES CORRIGÉS','Laisser l’enfant chercher avant de lire une réponse. Lui demander d’expliquer une autre démarche possible. Refaire ensuite une situation avec d’autres nombres ou d’autres objets.',83,49,size=13.5)
    b.text('Quand la réponse est un tracé',20,144,172,15,bold=True,color=GREEN)
    b.text('Comparer les positions des sommets, les longueurs, les alignements ou le nombre d’objets. Un dessin différent peut être correct s’il respecte toutes les contraintes. Pour les activités libres et les enquêtes, les critères de validation remplacent une réponse unique.',20,156,172,13)
    b.text('Quand la réponse est un calcul',20,197,172,15,bold=True,color=GREEN)
    b.text('Faire retrouver le sens de l’opération. Utiliser une collection ou un schéma, puis vérifier par une autre action : réunir après un retrait, recomposer un partage ou comparer avec une estimation.',20,209,172,13)
    b.box('RETOUR AUX EXERCICES','Les numéros de chapitre sont cliquables. Dans les pages d’exercices, cliquer sur un numéro ouvre la page du corrigé correspondant.',246,29,size=11.8)
    for c in CHAPITRES:
        b.begin(f'cor-{c.numero}',c.titre,f'CORRIGÉ DU CHAPITRE {c.numero:02d}',adult=True)
        b.outline(f'Corrigé {c.numero:02d}',f'cor-{c.numero}',1)
        b.link(f'ch-{c.numero}-ex-1',17,37,176,10)
        t=81
        b.text('Avec l’adulte',19,t,172,10.7,bold=True,color=GREEN)
        guide=c.guide_reponse
        if c.numero==11:guide+=' Méthode P3 : 54 = 40 + 14, sa moitié est 20 + 7 = 27 ; 72 = 60 + 12, sa moitié est 30 + 6 = 36.'
        t=b.text(guide,19,t+7,172,11.3,leading=14.5)+7
        for i,e in enumerate(c.exercices,1):
            b.text(f'{i}.',19,t,10,11.6,bold=True,color=NAVY)
            end=b.text(e.reponse,30,t,161,11.5,leading=14.7,maxbottom=246)
            dest='ch-29-graphique' if c.numero==29 and i==3 else f'ch-{c.numero}-ex-{(i-1)//3+1}'
            b.link(dest,18,t,10,max(6,end-t));t=end+4
        b.box('POINT DE VIGILANCE',c.vigilance,213,33,fill=CREAM,size=10.7)
        b.box('SI L’ENFANT HÉSITE',c.aide,249,26,fill=MINT,size=10.8)
    for i,(title,after,items) in enumerate(BILANS,1):
        b.begin(f'cor-bilan-{i}',title,f'CORRIGÉ DU BILAN {i}',adult=True)
        t=83
        for j,e in enumerate(items,1):
            b.text(str(j)+'.',19,t,10,12,bold=True,color=NAVY);t=b.text(e.reponse,30,t,160,12,leading=16)+11
        b.box('INTERPRÉTER LES RÉPONSES','Repérer la notion à reprendre, puis revenir au chapitre correspondant. Une erreur isolée ne suffit pas à décrire les acquis. Proposer une situation proche un autre jour.',237,37,size=11.7)

def oraux(b):
    b.begin('oral-intro','360 problèmes à raconter','BANQUE ORALE POUR L’ADULTE',adult=True)
    b.outline('Banque de 360 problèmes oraux','oral-intro')
    b.box('36 SEMAINES · 10 PROBLÈMES PAR SEMAINE','Lire chaque histoire sans annoncer l’opération. L’enfant peut utiliser des objets, dessiner, calculer puis répondre oralement ou sur son ardoise. Les réponses sont réservées à l’adulte.',83,49,size=13.5)
    t=145
    for title,body in [('Semaines 1 à 7','Petites quantités, ajouts, retraits, parties cachées et recherche du départ. Plafonds progressifs : 5, 8, 10 puis 20.'),('Semaines 8 à 14','Même travail dans le champ jusqu’à 59. Diminuer les quantités si la structure du problème est nouvelle.'),('Semaines 15 à 21','Extension à 100 pour les histoires additives en une étape. Groupes égaux jusqu’à 30 dès la semaine 15 ; partages dès la semaine 18 et paquets dès la semaine 20.'),('Semaines 22 à 36','Reprises variées, avec un problème en deux étapes par semaine dans le champ jusqu’à 30. Faire inventer d’autres histoires au fil de la semaine.')]:
        b.text(title,20,t,170,12.3,bold=True,color=GREEN);t=b.text(body,20,t+8,170,11.7,leading=15.4)+8
    for week in problemes_oraux():
        n=week['numero'];b.begin(f'oral-{n}',f'Semaine {n:02d} · Dix petites histoires','PROBLÈMES ORAUX',subtitle=f'Champ additif jusqu’à {week["plafond"]} · Lire les énoncés à l’enfant.',adult=True)
        t=81
        for i,p in enumerate(week['problemes'],1):
            b.text(str(i),18,t,9,10.8,bold=True,color=GREEN)
            end=b.text(p['enonce'],29,t,162,11.1,leading=14.2)
            end=b.text('Réponse : '+str(p['reponse'])+' · '+p['calcul'],29,end+1.2,162,9.7,leading=12.4,color=MUTED)
            b.line(29,end+2,191);t=end+5.8

def outils(b):
    b.begin('outils-intro','Matériel et fiches outils','À PHOTOCOPIER ET À MANIPULER',subtitle='Garder le livre entier ; utiliser des copies des pages suivantes.')
    b.outline('Matériel et fiches outils','outils-intro')
    b.text('Pour les manipulations',20,85,170,18,bold=True,color=GREEN)
    b.text('Des jetons, des cubes, des bandes, des pièces de jeu et une horloge aident à comprendre. On peut aussi utiliser des objets de la classe.',20,100,170,14)
    b.text('Pour découper',20,141,170,18,bold=True,color=GREEN)
    b.text('Un adulte prépare le matériel et accompagne l’utilisation des ciseaux. Les pièces et billets ci-après sont des dessins de jeu.',20,156,170,14)
    b.text('Pour les mesures',20,196,170,18,bold=True,color=GREEN)
    b.text('Imprimer à 100 %, sans « ajuster à la page ». Vérifier cette longueur avec une vraie règle : elle doit mesurer 5 cm.',20,211,170,14)
    b.line(32,254,82,color=NAVY,width=2)
    for x in [32,82]:b.c.setStrokeColor(NAVY);b.c.line(x*mm,H-250*mm,x*mm,H-258*mm)
    b.text('5 cm',48,261,35,12,bold=True)
    b.begin('outil-dizaines','Des dizaines et des unités','MATÉRIEL À DÉCOUPER')
    b.text('Une barre contient dix petits carrés. Un petit carré représente une unité.',20,82,171,14)
    for row in range(2):
        for col in range(5):
            xx=24+col*34;top=110+row*66
            for k in range(10):b.rect(xx,top+k*5,5,5,fill=MINT,stroke=GREEN,r=0)
    for j in range(20):b.rect(24+(j%10)*16,244+(j//10)*12,5,5,fill=PALE,stroke=NAVY,r=0)
    b.begin('outil-boites','Des boîtes de dix','MATÉRIEL À PHOTOCOPIER')
    b.text('Pose des jetons dans les cases. Remplis d’abord une ligne de cinq.',20,82,172,14)
    for top in [112,167,222]:b.fig(('tenframe',0),top,40)
    b.begin('outil-bande','Les nombres jusqu’à 100','OUTIL POUR COMPTER ET SE REPÉRER')
    b.text('Lis chaque ligne de gauche à droite. Ajoute 10 pour descendre d’une ligne.',20,82,172,13.5)
    cw=16;rh=13;x=25;top=111
    for row in range(10):
        for col in range(10):
            n=row*10+col+1;b.rect(x+col*cw,top+row*rh,cw,rh,fill=MINT if col==9 else white,stroke=RULE,r=0)
            b.text(str(n),x+col*cw+2.5,top+row*rh+3.5,cw-3,12,bold=col==9)
    b.text('Et avant 1, il y a 0.',25,251,162,13,bold=True,color=GREEN)
    b.begin('outil-argent','La monnaie du petit magasin','MONNAIE DE JEU À DÉCOUPER')
    b.text('Pièces : 1 € et 2 €. Billets : 5 €, 10 €, 20 € et 50 €.',20,82,172,13.5)
    for top in [111,159,207]:b.fig(('money',[1,1,2,2,5,10]),top,35)
    b.fig(('money',[20,20,50]),249,25)
    b.begin('outil-horloges','Des horloges à compléter','MATÉRIEL À PHOTOCOPIER')
    b.text('Dessine une petite aiguille et une grande aiguille pour montrer une heure entière.',20,82,172,14)
    for top in [109,166,223]:b.fig(('blankclocks',2),top,45)
    b.begin('outil-formes','Des formes à assembler','MATÉRIEL À DÉCOUPER')
    b.text('Découpe sur les contours. Avec l’adulte, cherche des assemblages qui forment une nouvelle figure.',20,82,172,14)
    for top in [114,171,228]:b.fig(('shapes','cutout'),top,40)
    b.begin('outil-faces','Six faces pour faire un cube','MATÉRIEL À DÉCOUPER AVEC L’ADULTE')
    b.text('Découpe ces six carrés identiques. Assemble les faces avec du ruban adhésif ou de la pâte adhésive en observant un cube réel.',20,82,172,14)
    for i in range(6):
        xx=40+(i%2)*78;top=116+(i//2)*53;b.rect(xx,top,40,40,fill=white,stroke=NAVY,r=0)
    b.text('Chaque face est un carré de 4 cm de côté à l’impression à 100 %.',20,269,172,11.4,color=MUTED)
    b.begin('outil-grille','Un quadrillage pour chercher','OUTIL À PHOTOCOPIER')
    b.text('Trace, reproduis ou complète une figure. Un carreau mesure 1 cm à l’impression à 100 %.',20,82,172,14)
    for i in range(17):
        b.c.setStrokeColor(RULE);b.c.setLineWidth(.4);b.c.line((25+i*10)*mm,H-112*mm,(25+i*10)*mm,H-272*mm)
    for j in range(17):b.line(25,112+j*10,185,width=.4)
    b.begin('outil-mots','Les mots des nombres','OUTIL POUR ÉCRIRE JUSQU’À 50')
    words=['zéro','un','deux','trois','quatre','cinq','six','sept','huit','neuf','dix','onze','douze','treize','quatorze','quinze','seize','dix-sept','dix-huit','dix-neuf']
    for i,s in enumerate(words):
        col=i//10;row=i%10;b.text(f'{i}   {s}',22+col*86,83+row*10,81,13.2)
    b.box('LES FAMILLES', '20 : vingt · 30 : trente · 40 : quarante · 50 : cinquante\n21 : vingt-et-un · 32 : trente-deux · 48 : quarante-huit',193,38,size=12.5)
    b.box('POUR L’ADULTE','Les mots composant les nombres sont reliés par des traits d’union dans ce livre. Faire écrire les nombres jusqu’à 50 en reliant le nom à la quantité.',239,33,size=11.3)
    b.begin('outil-calculs','Mes faits numériques','À APPRENDRE ET À RETROUVER',subtitle='Cherche d’abord avec des objets, puis essaie de te souvenir.')
    b.text('Les couples pour faire 10',20,82,172,17,bold=True,color=GREEN)
    for i in range(6):b.text(f'{i} + {10-i} = 10',27,99+i*9,155,15)
    b.text('Les doubles de 1 à 10',20,160,172,17,bold=True,color=GREEN)
    for i in range(1,11):
        col=(i-1)//5;row=(i-1)%5;b.text(f'{i} + {i} = {2*i}',27+col*85,177+row*10,78,15)
    b.box('RETROUVER UNE MOITIÉ','Si 7 + 7 = 14, la moitié de 14 est 7.\nDoubles : 20 → 40 ; 30 → 60 ; 40 → 80 ; 50 → 100.',238,36,size=13)
    b.begin('outil-tables','Les additions de 0 à 10','OUTIL POUR APPRENDRE',subtitle='Choisis une ligne ou une colonne. Cache une case et retrouve son résultat.')
    step=14;left=21;top=87
    for r in range(12):
        for col in range(12):
            label='+' if r==0 and col==0 else str(col-1) if r==0 else str(r-1) if col==0 else str(r+col-2)
            b.rect(left+col*step,top+r*step,step,step,fill=MINT if r==0 or col==0 else white,stroke=RULE,r=0)
            b.text(label,left+col*step+3,top+r*step+4,step-4,12.2,bold=r==0 or col==0)
    b.text('Le résultat de 4 + 6 se trouve à la ligne 4 et dans la colonne 6.',21,263,170,11.6,color=MUTED)
    b.begin('outil-fluence','Observer les progrès en calcul','FICHE POUR L’ADULTE',adult=True)
    b.text('À proposer après l’apprentissage. Comparer les progrès de l’enfant au fil du temps. Ne pas mélanger les trois types de tâche dans un même chronométrage.',20,82,172,12)
    groups=[('A · 8 faits d’addition · 1 minute',['3 + 4','6 + 2','9 + 1','5 + 5','7 + 3','4 + 4','8 + 2','6 + 7'],'7 ; 8 ; 10 ; 10 ; 10 ; 8 ; 10 ; 13.'),('B · 8 doubles et moitiés usuels · 1 minute',['double de 6','moitié de 18','double de 20','moitié de 60','double de 9','moitié de 100','double de 40','moitié de 16'],'12 ; 9 ; 40 ; 30 ; 18 ; 50 ; 80 ; 8.'),('C · 9 calculs par procédure · 3 minutes',['29 + 1','48 - 2','34 + 20','76 - 30','47 + 6','35 + 9','24 + 38','moitié de 48','60 - 7'],'30 ; 46 ; 54 ; 46 ; 53 ; 44 ; 62 ; 24 ; 53.')]
    t=111
    for title,qs,answers in groups:
        b.text(title,20,t,172,12.3,bold=True,color=GREEN);t+=10
        for i,q in enumerate(qs):
            x=23+(i%3)*56;y=t+(i//3)*10;b.text(q+' = …',x,y,54,11.7)
        t+=34;b.text('Réponses : '+answers,23,t,168,9.7,color=MUTED);t+=13

def fin(b):
    for part in range(2):
        b.begin(f'couverture-programme-{part+1}','Repères du programme','CORRESPONDANCES POUR L’ADULTE',subtitle='Les activités constituent une proposition éditoriale pour le CP.',adult=True)
        if part==0:b.outline('Programme et références','couverture-programme-1')
        t=82
        for title,chs in COUVERTURE[part*11:(part+1)*11]:
            b.text(title,19,t,172,11.6,bold=True,color=NAVY);t=b.text('Chapitres '+chs,19,t+8,172,11,color=MUTED)+4
        if part==1:
            b.text('Périmètre : calculs jusqu’à 100 ; problèmes en deux étapes, groupes et partages jusqu’à 30 ; euros entiers ; heures entières. Pas de calculatrice dans le parcours courant.',20,260,172,10.6,color=MUTED)
    b.begin('guide-aide','Aider sans faire à la place','NOTES PÉDAGOGIQUES',adult=True)
    t=82
    notes=[('L’enfant recompte sans arrêt','Proposer des collections structurées : cinq et encore, puis dix et encore. Faire expliquer ce qu’il reconnaît avant de recompter.'),('Il inverse les chiffres','Faire fabriquer les deux nombres : 24 et 42. Faire dire « deux dizaines, quatre unités » puis « quatre dizaines, deux unités ». Relier chaque chiffre à ce qu’il représente.'),('Il choisit une opération à partir d’un mot','Rejouer l’histoire avec des jetons. Demander ce qui est connu et ce qui est cherché. Une histoire où l’on donne peut demander de retrouver le départ.'),('Il réussit avec des objets mais pas avec un dessin','Dessiner pendant la manipulation, puis montrer les correspondances. Cacher progressivement le matériel sans imposer sa disparition avant la compréhension.'),('Il échoue sur une tâche longue','Réduire le nombre de questions, lire à voix haute et laisser répondre oralement. Reprendre le même objectif dans une situation courte.'),('Il a déjà compris','Demander une explication, une vérification ou une autre représentation. Faire inventer un problème avec une réponse connue plutôt qu’agrandir systématiquement les nombres.')]
    for title,body in notes:
        b.text(title,19,t,172,12.4,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.6,leading=15.3)+8
    for part in range(2):
        b.begin(f'sources-{part+1}','Sources et statut des activités','RÉFÉRENCES CONSULTÉES LE 23 OCTOBRE 2026',adult=True)
        t=82
        for idx,(title,description,url) in enumerate(SOURCES[part*4:(part+1)*4],start=part*4+1):
            b.text(f'{idx}. {title}',19,t,172,12.3,bold=True,color=NAVY)
            b.c.linkURL(url,(19*mm,H-(t+9)*mm,191*mm,H-t*mm),relative=0,thickness=0)
            t=b.text(description,19,t+10,172,11.4,leading=15)+3
            short=url.replace('https://','');t=b.text(short,19,t,172,9.1,leading=12,color=MUTED)+12
        if part==1:
            b.box('DES EXERCICES ORIGINAUX','Les leçons, exercices, bilans, problèmes oraux et schémas de ce livre sont des créations pour la collection OptiTAB. Ils s’appuient sur les domaines du programme et les familles de tâches consultées ; ils ne sont pas des sujets officiels.',204,39,size=11.5)
            b.text('Publication indépendante, sans validation ni label du ministère. Les ressources officielles sont accessibles par les titres cliquables. Les supports de début CP 2026 et les ressources de point d’étape disponibles en 2026 ont été consultés ; aucun support de janvier 2027 n’est présenté comme déjà disponible.',20,252,172,10.2,leading=13.2)
    b.begin('bravo','Ce que je sais faire maintenant','MON PARCOURS DE CP',subtitle='À raconter avec des objets, des dessins et des mots.')
    b.box('JE CHOISIS UNE RÉUSSITE','Je montre un exercice que je sais refaire.\nJe dis ce que j’ai compris et comment je vérifie.',83,40,fill=MINT)
    b.text('Mon dessin ou mon schéma',22,136,165,16,bold=True,color=GREEN)
    b.rect(20,151,170,69,fill=white,stroke=RULE)
    b.text('Ce que je veux encore apprendre à mieux faire :',22,235,165,13.4)
    b.lines(252,22,x=22,w=166)

def construire(path,refs=None):
    b=Livre(path,refs);couverture(b);liminaires(b)
    for c in CHAPITRES:chapitre(b,c)
    bilans(b);corriges(b);oraux(b);outils(b);fin(b)
    b.c.save();return b

if __name__=='__main__':
    assert len(CHAPITRES)==30
    first=construire(BUILD/'mise-en-page.pdf')
    final=construire(BUILD/'optitab-cp-complet.pdf',first.dest)
    assert first.dest==final.dest,'Pagination instable'
    meta=dict(pages=final.page,chapitres=len(CHAPITRES),exercices=270,bilans=5,questions_bilans=30,problemes_oraux=360,insertions_figures=final.figures,destinations=final.dest,plan=final.pages)
    (BUILD/'manifeste.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-texte.json').write_text(json.dumps(final.textblocks,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-figures.json').write_text(json.dumps(final.figureblocks,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in meta.items() if k not in ['destinations','plan']},ensure_ascii=False))
