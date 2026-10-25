"""Construit le livre CE2 : PDF vectoriel A4, sommaire et renvois cliquables."""
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
import contenu_nombres,contenu_calcul,contenu_multiplication,contenu_problemes,contenu_fractions,contenu_mesures,contenu_temps,contenu_geometrie
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
        self.c.setTitle('OptiTAB - Mathématiques CE2 - Livre pédagogique')
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
    def begin(self,key,title,eyebrow='MATHÉMATIQUES CE2',subtitle='',adult=False):
        if self.page:self.c.showPage()
        self.page+=1;self.current=key;self.dest[key]=self.page
        self.c.bookmarkPage(key)
        self.pages.append(dict(numero=self.page,cle=key,titre=title,adulte=adult))
        self.c.setFillColor(GREEN);self.c.rect(0,H-5*mm,W,5*mm,stroke=0,fill=1)
        self.c.drawImage(str(ASSETS/'logo-couleur.png'),17*mm,H-23*mm,width=31*mm,height=11*mm,preserveAspectRatio=True,mask='auto')
        self.text('MATHÉMATIQUES  /  CE2',125,15,68,9.2,bold=True,color=NAVY)
        self.line(17,29,193)
        self.text(eyebrow.upper(),17,37,176,10,bold=True,color=GREEN)
        end=self.text(title,17,47,176,23,leading=27,bold=True,color=NAVY)
        if subtitle:self.text(subtitle,17,end+4,176,11.2,color=MUTED)
        self.line(17,283,193)
        self.c.setFont('Text',9);self.c.setFillColor(MUTED)
        self.c.drawString(17*mm,9*mm,'OptiTAB · CE2 · France 2026-2027')
        self.c.drawRightString(193*mm,9*mm,str(self.page))
        if adult:self.c.drawCentredString(105*mm,9*mm,'Pour l’adulte')
    def box(self,label,body,top,h,fill=PALE,size=14):
        self.rect(17,top,176,h,fill)
        self.text(label,23,top+5,164,10.5,bold=True,color=GREEN)
        self.text(body,23,top+13,164,size,maxbottom=top+h-3)
    def link(self,key,x,top,w,h):
        self.c.linkRect('',key,(x*mm,H-(top+h)*mm,(x+w)*mm,H-top*mm),relative=0,thickness=0)
    def outline(self,title,key,level=0):self.c.addOutlineEntry(title,key,level=level,closed=level==0)

