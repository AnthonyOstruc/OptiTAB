"""Une septième question variée issue des sources originales du même chapitre."""
import hashlib
import json
import re
from config import GRADE
from modele_site import q

def latex_site(s):
    # La macro du livre met seulement la réponse en couleur ; conserver son contenu.
    while r'\res' in s:
        pos=s.index(r'\res');start=pos+4
        if s[start:start+1]=='{':
            depth=1;end=start+1
            while depth:
                depth+=(s[end]=='{')-(s[end]=='}');end+=1
            s=s[:pos]+s[start+1:end-1]+s[end:]
        else:s=s[:pos]+s[start:]
    s=s.replace(r'\begin{questions}','').replace(r'\end{questions}','')
    if r'\item' in s:
        count=0
        def item(_):
            nonlocal count
            count+=1;return f' ({chr(96+count)}) '
        s=re.sub(r'\\item\s*',item,s)
    return re.sub(r'\s+',' ',s).strip()

def append(c,e,i,level,book_figures):
    # Les 15 tâches du CM sont réparties en 5 par difficulté ; les 9 du CE en 3.
    cm=GRADE.startswith('cm');per=5 if cm else 3;item=c.exercices[level*per+i%per]
    text=item['enonce'] if cm else item['consigne'];answer=item['corrige'] if cm else item['reponse']
    method=item['methode'] if cm else c.aide
    figure=item.get('figure')
    key=None
    if figure:
        key=figure if cm else 'livre-'+hashlib.sha256(json.dumps(figure,ensure_ascii=False).encode()).hexdigest()[:16]
        book_figures[key]=figure
    # Certains exercices de lecture utilisent un tableau figurant dans la leçon.
    extra=''
    if cm and not figure and re.search(r'du cours|tableau du|tableau donne',text,re.I):
        raw=' '.join(c.cours)
        tables=re.findall(r'\\begin\{center\}.*?\\end\{center\}',raw,re.S)
        if tables:extra=' '+tables[0]
        else:
            figs=re.findall(r'@FIG:([^@]+)@',raw)
            if figs:key=figs[0];book_figures[key]=key
    texte='Autre situation du chapitre : '+latex_site(text)
    if extra:
        # Convertir le tableau en HTML avec le même moteur que le cours.
        from construire import to_html
        texte+=' '+to_html(extra,[])
    if key:texte+=' [IMAGE_3]'
    control=item['controle'] if cm else item.get('check','')
    # Les contrôles du livre sont exécutés séparément ; aucune source n'est perdue.
    e.questions.append(q(texte,latex_site(method),latex_site(answer)))
    return key,control
