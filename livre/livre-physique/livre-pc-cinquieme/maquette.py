"""Maquette éditoriale A4 OptiTAB. Coordonnées en mm depuis le haut."""
from pathlib import Path
import html,json,re
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parent;BUILD=ROOT/'build';BUILD.mkdir(exist_ok=True)
W,H=210*mm,297*mm
NAVY=HexColor('#1B3C8E');DARK=HexColor('#122A66');GREEN=HexColor('#3B8544')
INK=HexColor('#1C293B');MUTED=HexColor('#596A7C');RULE=HexColor('#D3DCE5')
PALE=HexColor('#F0F4FA');MINT=HexColor('#EFF6F1');CREAM=HexColor('#FCF5E9')
CYAN=HexColor('#D8EEF4');TEAL=HexColor('#217D95');ORANGE=HexColor('#BD721F')
for name,file in [('Body','calibri.ttf'),('Bold','calibrib.ttf'),('Italic','calibrii.ttf'),('Title','segoeuil.ttf'),('Head','segoeuib.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')

class Livre:
    def __init__(self,path,refs=None,complet=False):
        self.complet=complet
        self.c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
        self.c.setTitle('OptiTAB - Physique-chimie 5e - Sommaire et chapitres 1 et 2')
        self.c.setAuthor('OptiTAB');self.c.setSubject('Maquette de validation - Programme français de cycle 4 - 2026-2027')
        if complet:
            self.c.setTitle('OptiTAB - Physique-chimie 5e - Manuel complet')
            self.c.setSubject('Cours, activités, exercices et corrigés - Programme français de cycle 4 - 2026-2027')
        self.page=0;self.key='';self.chapter=0;self.ch_title='';self.refs=refs or {};self.dest={};self.pages=[];self.blocks=[];self.figures=[];self.exercises=[]
    def p(self,s,x=22,top=75,w=166,size=12,leading=None,font='Body',color=INK,maxbottom=276,markup=False,measure=False):
        if not s:return top
        text=str(s) if markup else html.escape(str(s))
        text=text.replace('\n','<br/>')
        text=re.sub(r' ([?!:;])',lambda m:'\u00a0'+m.group(1),text)
        text=re.sub(r'(\d) (kg|g|mg|mL|cL|L|cm³|dm³|m³|°C)(?=\W|$)',lambda m:m.group(1)+'\u00a0'+m.group(2),text)
        st=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.30,textColor=color)
        para=Paragraph(text,st);_,ph=para.wrap(w*mm,2000)
        if measure:return ph/mm
        bottom=top+ph/mm
        if bottom>maxbottom+.05:raise ValueError(f'Page {self.page} {self.key}: {bottom:.1f} mm : {s[:80]}')
        para.drawOn(self.c,x*mm,H-top*mm-ph)
        self.blocks.append(dict(page=self.page,key=self.key,x=x,top=top,w=w,h=ph/mm,text=html.unescape(text)))
        return bottom
    def rect(self,x,top,w,h,fill=PALE,stroke=None,r=2):
        self.c.setFillColor(fill);self.c.setStrokeColor(stroke or fill);self.c.setLineWidth(.55)
        self.c.roundRect(x*mm,H-(top+h)*mm,w*mm,h*mm,r*mm,stroke=bool(stroke),fill=1)
    def line(self,x,top,x2,color=RULE,width=.6):
        self.c.setStrokeColor(color);self.c.setLineWidth(width);self.c.line(x*mm,H-top*mm,x2*mm,H-top*mm)
    def begin(self,key,title,eyebrow='',chapter=0,chapter_title='',subtitle='',outline=False):
        if self.page:self.c.showPage()
        self.page+=1;self.key=key;self.dest[key]=self.page
        self.chapter=chapter;self.ch_title=chapter_title
        self.pages.append(dict(page=self.page,key=key,title=title,chapter=chapter))
        self.c.bookmarkPage(key)
        self.c.drawImage(str(ROOT/'images/logo-couleur.png'),20*mm,H-21*mm,width=28*mm,height=10*mm,preserveAspectRatio=True,mask='auto')
        self.p('PHYSIQUE-CHIMIE  /  5e',121,15,67,9.2,font='Bold',color=NAVY)
        self.line(20,28,190)
        if chapter:
            self.rect(0,37,9,11,fill=NAVY,r=0);self.p(f'{chapter:02}',1.2,39.6,7,8.4,font='Bold',color=white)
        self.p(eyebrow.upper(),22,37,166,9.4,font='Bold',color=GREEN)
        end=self.p(title,21,45,168,25,leading=29,font='Title',color=NAVY,maxbottom=73)
        if subtitle:self.p(subtitle,22,end+4,166,10.8,color=MUTED,maxbottom=77)
        self.line(20,283,190)
        self.p(str(self.page),20,286,12,9,font='Bold',color=NAVY,maxbottom=294)
        self.p('OPTITAB · CINQUIÈME · '+(f'CHAPITRE {chapter:02}' if chapter else ('PHYSIQUE-CHIMIE' if self.complet else 'MAQUETTE DE VALIDATION')),36,286,145,8.2,color=MUTED,maxbottom=294)
        if outline:self.c.addOutlineEntry(title,key,level=0,closed=False)
    def section(self,n,title,top=78):
        self.p(str(n),22,top,8,13,font='Bold',color=NAVY)
        end=self.p(title,32,top,156,14,font='Bold');self.line(22,end+3,188);return end+8
    def box(self,label,body,top,h,x=22,w=166,fill=PALE,size=11.8,accent=NAVY):
        self.rect(x,top,w,h,fill=fill,r=1.8)
        self.c.setFillColor(accent);self.c.rect(x*mm,H-(top+h)*mm,1.0*mm,h*mm,stroke=0,fill=1)
        self.p(label.upper(),x+4,top+3.5,w-8,9.3,font='Bold',color=accent,maxbottom=top+h-2)
        return self.p(body,x+4,top+10.5,w-8,size,maxbottom=top+h-3,markup=True)
    def fig(self,spec,top,h,x=22,w=166,caption=None):
        from schemas import draw
        if top+h>277:raise ValueError(f'Figure hors zone : {self.key}')
        draw(self.c,spec,x*mm,H-(top+h)*mm,w*mm,h*mm)
        self.figures.append(dict(page=self.page,key=self.key,spec=spec,x=x,top=top,w=w,h=h))
        if caption:return self.p(caption,x,top+h+2,w,9.5,color=MUTED)
        return top+h
    def bullets(self,items,top,x=23,w=164,size=11.8,gap=3):
        for s in items:
            self.c.setFillColor(GREEN);self.c.circle(x*mm,H-(top+2.4)*mm,.7*mm,stroke=0,fill=1)
            top=self.p(s,x+4,top,w-4,size,markup=True)+gap
        return top
    def table(self,rows,top,widths,x=22,rowheight=12,size=11.2,header=True):
        for r,row in enumerate(rows):
            xx=x
            for j,(s,ww) in enumerate(zip(row,widths)):
                self.rect(xx,top,ww,rowheight,fill=PALE if r==0 and header else white,stroke=RULE,r=0)
                self.p(s,xx+2.3,top+2.4,ww-4.6,size,font='Bold' if r==0 and header else 'Body',color=NAVY if r==0 and header else INK,maxbottom=top+rowheight-1,markup=True);xx+=ww
            top+=rowheight
        return top
    def link(self,key,x,top,w,h):
        self.c.linkRect('',key,(x*mm,H-(top+h)*mm,(x+w)*mm,H-top*mm),relative=0,thickness=0)
    def url(self,url,x,top,w,h):
        self.c.linkURL(url,(x*mm,H-(top+h)*mm,(x+w)*mm,H-top*mm),relative=0,thickness=0)
    def answerlines(self,top,rows=3,x=27,w=156):
        for i in range(rows):self.line(x,top+i*7,x+w)
    def save(self):self.c.save()
