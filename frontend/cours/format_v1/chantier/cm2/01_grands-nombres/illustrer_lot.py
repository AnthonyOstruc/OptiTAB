# -*- coding: utf-8 -*-
"""Figures nouvelles TikZ : numération, bandes et demi-droites."""
from rediger_lot import ROOT,SLUGS,N,F,dec,write,jwrite

def line(count,left,right,point=None,full=False,green=False):
    color='otGreenDark' if green else 'otNavy'
    s=r'\begin{tikzpicture}[x=1cm,y=1cm]'+'\n'
    s+=rf'\draw[{color},line width=.7pt,-{{Stealth[length=2mm]}}] (0,0)--(6.35,0);'+'\n'
    for i in range(count+1):
        x=6*i/count
        s+=rf'\draw[{color},line width=.6pt] ({x:.5f},-.065)--({x:.5f},.065);'+'\n'
    s+=rf'\node[below=5pt,text=otInk] at (0,0) {{$ {left} $}};'+'\n'
    s+=rf'\node[below=5pt,text=otInk] at (6,0) {{$ {right} $}};'+'\n'
    if point is not None:
        x=6*point/count
        s+=rf'\fill[{color}] ({x:.5f},0) circle (1.7pt);'+'\n'
        s+=rf'\node[above=8pt,text={color}] at ({x:.5f},0) {{$A$}};'+'\n'
    return s+r'\end{tikzpicture}'

def bands(rows):
    s=r'\begin{tikzpicture}[x=1cm,y=1cm]'+'\n'
    for j,(a,b,label,color) in enumerate(rows):
        y=-j*1.35
        s+=rf'\fill[{color}!24] (0,{y}) rectangle ({6*a/b},{y+.38});'+'\n'
        s+=rf'\draw[{color},line width=.65pt] (0,{y}) rectangle (6,{y+.38});'+'\n'
        for k in range(1,b):
            x=6*k/b
            s+=rf'\draw[{color},line width=.45pt] ({x},{y})--({x},{y+.38});'+'\n'
        s+=rf'\node[above=6pt,text={color}] at (3,{y+.38}) {{{label}}};'+'\n'
    return s+r'\end{tikzpicture}'

def groups():
    s=r'\begin{tikzpicture}[x=1cm,y=1cm]'+'\n'
    for j in range(4):
        x=j*1.5
        s+=rf'\draw[otNavy,fill=otSky,line width=.65pt] ({x},0) rectangle ({x+1.2},.7);'+'\n'
        s+=rf'\node[text=otInk] at ({x+.6},.35) {{6}};'+'\n'
    s+=r'\node[text=otNavy,above=8pt] at (2.85,.7) {4 groupes de 6 : 24 objets};'+'\n'
    return s+r'\end{tikzpicture}'

def add_ex_image(p,ident,filename,alt):
    text=(p/'exercices.txt').read_text(encoding='utf-8')
    blocks=text.split('\n===\n')
    for i,block in enumerate(blocks):
        if f'Id: nouveau-{ident}\n' in block:
            needle='<!-- optitab:1 -->\n'
            block=block.replace(needle,needle+'[IMAGE_1]\n\n',1)
            blocks[i]=block
    write(p/'exercices.txt','\n===\n'.join(blocks))

def main():
    for idx,slug in enumerate(SLUGS):
        p=ROOT/slug;figs={};mapping={'cours':{'nouveau':{}},'fiches':{'nouvelle':{}},'exercices':{}}
        def cours(pos,name,tikz,alt):
            figs[name]=tikz;mapping['cours']['nouveau'][str(pos)]={'fichier':name+'.png','alt':alt}
        def ex(ident,name,tikz,alt):
            figs[name]=tikz;mapping['exercices'][f'nouveau-{ident}']={'1':{'fichier':name+'.png','alt':alt}}
            add_ex_image(p,ident,name+'.png',alt)
        if idx==0:
            cours(1,'droite_millions',line(5,N(3000000),N(4000000),3),'Droite de trois à quatre millions en cinq intervalles ; A au troisième pas')
            for lev,(start,step) in enumerate([(3000000,200000),(42000000,50000),(208000000,250000)]):
                ex(6+7*lev,'graduation_'+str(lev+1),line(5,N(start),N(start+5*step),3),'Cinq intervalles égaux entre deux bornes entières ; A au troisième pas')
        elif idx==1:
            cours(1,'groupes_de_six',groups(),'Quatre groupes contenant six objets chacun, soit vingt-quatre objets')
        elif idx==2:
            cours(1,'cinq_huitiemes',bands([(5,8,r'Une unité ; $\frac58$ en bleu','otNavy')]),'Une unité partagée en huit parts égales, dont cinq colorées')
            cours(2,'dix_neuf_sixiemes',line(24,'0','4',19),'Demi-droite en sixièmes de zéro à quatre ; A au dix-neuvième pas')
            for lev,(b,start,k) in enumerate([(4,0,7),(6,1,11),(8,2,13)]):
                count=2*b
                ex(5+7*lev,'abscisse_'+str(lev+1),line(count,str(start),str(start+2),k),'Fenêtre de deux unités partagées régulièrement ; point A à lire depuis le début de la fenêtre')
        elif idx==3:
            cours(1,'quarts_huitiemes',bands([(3,4,r'$\frac34$ de la même unité','otNavy'),(6,8,r'$\frac68$ de la même unité','otGreenDark')]),'Deux bandes de même longueur : trois quarts et six huitièmes colorés représentent la même quantité')
        elif idx==4:
            cours(1,'trois_cinquiemes_40',bands([(3,5,r'40 jetons en 5 parts égales','otNavy')]),'Une barre représentant quarante jetons en cinq parts égales, trois parts colorées')
        else:
            cours(1,'graduation_centiemes',line(10,dec(4200),dec(4300),3),'Droite de 4,20 à 4,30 en dix intervalles ; A repère 4,23')
            for lev,(start,step,count) in enumerate([(4200,10,3),(7200,5,7),(12000,1,13)]):
                ex(6+7*lev,'decimal_'+str(lev+1),line(20,dec(start),dec(start+step*20),count),'Vingt intervalles décimaux réguliers entre les bornes indiquées ; point A à repérer')
        write(p/'figures'/'figures.py','# -*- coding: utf-8 -*-\n"""Figures originales CM2, style livre, sans exception de chevauchement."""\nFIGURES = '+repr(figs)+'\n')
        jwrite(p/'figures'/'correspondance.json',mapping)
        print(slug,len(figs),'figures')
if __name__=='__main__':main()
