"""Révision locale des notions attribuées 266–270, sans accès à la base.

Les fichiers de source et les identités d'exercices sont conservés.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import re

BASE = Path(__file__).resolve().parent.parent

def frac(a, b=1):
    f = F(a, b)
    return str(f.numerator) if f.denominator == 1 else rf"\frac{{{f.numerator}}}{{{f.denominator}}}"

def box(kind, title, content):
    return f"::: {kind}{(' ' + title) if title else ''}\n{content}\n:::\n"

def calc(*lines):
    if len(lines) == 1:
        return '$$' + lines[0] + '$$'
    return '$$\n\\begin{aligned}\n' + ' \\\\\n'.join(lines) + '\n\\end{aligned}\n$$'

def question(number, text, method, work, result):
    return f"## Question {number} : {text}\n\n" + box('methode', '', method) + '\n' + box('etape', 'Raisonnement et calcul', work) + '\n' + box('resultat', '', result)

def figure_rectangle(k, b):
    return rf"""\begin{{tikzpicture}}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {{$x$ cm}};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {{{b} cm}};
\node[anchor=east] at (-.2,.85) {{{k} cm}};
\node[anchor=north,text=otMuted] at (2.3,-.25) {{Schéma non à l'échelle}};
\end{{tikzpicture}}"""

def figure_cube(n):
    size=2.2
    step=size/n
    lines=[r'\begin{tikzpicture}',r'\fill[otNavy!8] (0,0) rectangle (2.2,2.2);']
    for j in range(n+1):
        x=j*step
        lines += [rf'\draw[otNavy!55,line width=.4pt] ({x:.5f},0)--({x:.5f},2.2);',rf'\draw[otNavy!55,line width=.4pt] (0,{x:.5f})--(2.2,{x:.5f});']
    lines += [rf'\node[anchor=south] at (1.1,2.45) {{{n} carreaux de côté}};',r'\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);',r'\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);',r'\draw[geoTrait] (5.6,2.2)--(6.35,2.95);',r'\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);',r'\draw[geoAide] (4.15,.75)--(4.15,2.95);',rf'\node[anchor=north] at (4.5,-.2) {{{n} cubes par arête}};',r'\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};',r'\end{tikzpicture}']
    return '\n'.join(lines)

def figure_facture(n,b,total):
    w=5.2/n
    s=[r'\begin{tikzpicture}']
    for i in range(n):
        x=i*w
        s += [rf'\draw[geoTrait,fill=otNavy!8] ({x:.4f},0) rectangle ({x+w:.4f},.8);',rf'\node[text=otNavy] at ({x+w/2:.4f},.4) {{$x$}};']
    s += [rf'\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);',rf'\node[text=otGreenDark] at (5.75,.4) {{{b}\,\euro}};',rf'\node[anchor=south] at (3.15,1.1) {{Total : {total}\,\euro}};',r'\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};',r'\end{tikzpicture}']
    return '\n'.join(s).replace(r'\euro',r'\text{€}')

COURSES = {
266: r'''::: objectifs
Additionner et soustraire des fractions, calculer une part d'une quantité et distinguer une fraction du total d'une fraction du reste.
:::

## I. Additionner des parts de même taille

::: propriete Même dénominateur
Pour $b>0$, on conserve la taille des parts :
$$\frac{a}{b}+\frac{c}{b}=\frac{a+c}{b}$$
$$\frac{a}{b}-\frac{c}{b}=\frac{a-c}{b}$$
:::

::: methode Dénominateurs différents
1. Choisir un multiple commun des dénominateurs.
2. Multiplier le numérateur et le dénominateur de chaque fraction par le même nombre non nul.
3. Additionner ou soustraire les numérateurs, puis simplifier si possible.
:::

::: exemple Une somme supérieure à un
$$
\begin{aligned}
\frac34+\frac56 &= \frac9{12}+\frac{10}{12} \\
&= \frac{19}{12} \\
&=1+\frac7{12}
\end{aligned}
$$
Une fraction peut être supérieure à l'unité.
:::

[IMAGE_1]

::: attention
On n'additionne jamais les dénominateurs : $\frac12+\frac13=\frac56$, et non $\frac25$.
:::

## II. Calculer une part et un reste

::: methode Fraction d'une quantité
Prendre $\frac ab$ d'une quantité revient à la partager en $b$ parts égales, puis à prendre $a$ parts. Les $\frac35$ de 40 valent $(40\div5)\times3=24$.
:::

::: exemple Deux fractions du même total
On parcourt $\frac25$ d'un trajet le matin et $\frac13$ du trajet entier l'après-midi.
$$
\begin{aligned}
\text{Part parcourue} &= \frac6{15}+\frac5{15}=\frac{11}{15} \\
\text{Part restante} &= 1-\frac{11}{15}=\frac4{15}
\end{aligned}
$$
:::

::: exemple Une fraction du reste
Sur 60 livres, on range d'abord le tiers : $60\div3=20$ livres. Il reste $60-20=40$ livres. Le quart du reste vaut $40\div4=10$ livres. On a donc rangé $20+10=30$ livres, soit la moitié du total.
:::

::: retenir
Avant d'additionner des fractions, identifier le tout auquel chacune se rapporte. Une fraction du reste doit être appliquée au reste déjà calculé. Contrôler que la quantité utilisée et la quantité restante redonnent le total.
:::
''',
267: r'''::: objectifs
Comprendre les écritures au carré et au cube, mémoriser les carrés de 0 à 12 et calculer des aires, des volumes et des expressions avec des puissances.
:::

## I. Deux ou trois facteurs identiques

::: definition Carré et cube
Pour un nombre positif ou nul $a$ :
$$a^2=a\times a$$
$$a^3=a\times a\times a$$
L'exposant indique le nombre de facteurs identiques. $4^3=64$, et non $4\times3$.
:::

| $a$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $a^2$ | 0 | 1 | 4 | 9 | 16 | 25 | 36 |

| $a$ | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|
| $a^2$ | 49 | 64 | 81 | 100 | 121 | 144 |

::: exemple
$2^3=8$, $3^3=27$, $5^3=125$ et $10^3=1\,000$. Reconnaître $25=5^2$ aide à retrouver un côté de carré.
:::

## II. Respecter les priorités

::: methode
Calculer les parenthèses, puis les puissances, puis les multiplications et divisions, puis les additions et soustractions.
:::

::: exemple
$$
\begin{aligned}
3+2\times5^2 &= 3+2\times25 \\
&=3+50 \\
&=53
\end{aligned}
$$
En revanche, $(3+2)^2=5^2=25$.
:::

::: exemple Remplacer une lettre
Pour $x=4$, $2x^2+3=2\times4^2+3=2\times16+3=35$.
:::

## III. Relier les puissances aux grandeurs

::: propriete
Un carré de côté $c$ a pour aire $c^2$. Un cube d'arête $c$ a pour volume $c^3$. Avec un côté en cm, l'aire est en cm$^2$ et le volume en cm$^3$.
:::

[IMAGE_1]

::: exemple Changer d'unité
$1$ dm$=10$ cm, donc $1$ dm$^3=10\times10\times10=1\,000$ cm$^3$.
:::

::: attention
$(2+3)^2=25$, tandis que $2^2+3^2=13$ : on ne distribue pas un carré sur une somme.
:::

::: retenir
Doubler un côté multiplie l'aire par $2\times2=4$. Doubler une arête multiplie le volume par $2\times2\times2=8$.
:::
''',
268: r'''::: objectifs
Passer d'une situation à une formule, remplacer une lettre par un nombre, décrire un motif et tester une égalité.
:::

## I. Écrire une formule

::: definition La lettre représente un nombre
Une lettre peut représenter un nombre qui varie. Le double de $x$ s'écrit $2x$, son successeur $x+1$ et son carré $x^2$.
$2x$ signifie $2\times x$ ; $x^2$ signifie $x\times x$.
:::

::: exemple Périmètre et aire
Pour un rectangle de longueur $L$ et de largeur $\ell$ :
$$P=2(L+\ell)\qquad A=L\ell$$
Avec $L=7$ cm et $\ell=3$ cm, $P=2\times(7+3)=20$ cm et $A=7\times3=21$ cm$^2$.
:::

::: methode Décrire un motif évolutif
1. Compter au premier rang.
2. Trouver ce qui est ajouté à chaque nouveau rang.
3. Pour le rang $n$, ajouter $n-1$ fois cet accroissement au nombre de départ.
:::

[IMAGE_1]

::: exemple Carrés accolés
Le premier carré utilise 4 allumettes. Chaque carré supplémentaire partage un côté avec le précédent et ajoute 3 allumettes.
$$4+3(n-1)=3n+1$$
Au rang 5, on utilise $3\times5+1=16$ allumettes.
:::

## II. Substituer une valeur et tester une égalité

::: methode
Remplacer chaque occurrence de la lettre par la même valeur, rétablir les multiplications et respecter les priorités.
:::

::: exemple
Pour $x=2$ :
$$
\begin{aligned}
3x^2+2x &= 3\times2^2+2\times2 \\
&=12+4 \\
&=16
\end{aligned}
$$
:::

::: definition Tester une égalité
Calculer séparément ses deux membres. Pour $x=4$, $2x+1=9$ est vraie car $2\times4+1=9$. Pour $x=3$, elle est fausse car $7\ne9$.
:::

::: attention
Quelques tests réussis ne prouvent pas une propriété générale. Un seul contre-exemple suffit à montrer qu'une affirmation universelle est fausse. On additionne seulement des grandeurs de même nature.
:::

::: methode Explorer avec un tableur
Si A2 contient une valeur de $n$, `=3*A2+1` calcule $3n+1$. Recopier vers le bas permet de tester plusieurs rangs et de formuler une conjecture.
:::

::: retenir
Une formule décrit tous les rangs autorisés. Distinguer le rang d'un motif et le nombre d'objets qu'il contient.
:::
''',
269: r'''::: objectifs
Reconnaître une somme et un produit, développer ou factoriser une expression simple, réduire et démontrer avec des lettres.
:::

## I. Développer et factoriser

::: definition Reconnaître la structure
La dernière opération donne la nature de l'expression : $3x+2$ est une somme ; $3(x+2)$ est un produit.
:::

::: propriete Distributivité
$$k(a+b)=ka+kb$$
$$k(a-b)=ka-kb$$
Développer transforme un produit en somme ou différence. Factoriser effectue la transformation inverse grâce à un facteur commun.
:::

[IMAGE_1]

::: exemple Lire les aires
Le rectangle a une hauteur de 4 cm et une largeur de $(x+3)$ cm, avec $x>0$. Son aire vaut $4(x+3)$ cm$^2$. Les deux morceaux ont pour aires $4x$ et $12$ cm$^2$ :
$$4(x+3)=4x+12$$
:::

::: methode Factoriser
Dans $6x+18$, repérer $6x=6\times x$ et $18=6\times3$, puis écrire $6x+18=6(x+3)$.
:::

::: attention
$3(x+5)=3x+15$. Le facteur 3 multiplie chacun des deux termes.
:::

## II. Réduire une expression

::: propriete Regrouper les termes de même nature
$3x+5x=8x$, $x+x=2x$ et $1x=x$. On ne peut pas réduire $3x+5$ à $8x$.
:::

::: exemple
$$
\begin{aligned}
2{,}5x+4+x+1 &= (2{,}5+1)x+(4+1) \\
&=3{,}5x+5
\end{aligned}
$$
:::

## III. Démontrer ou réfuter

::: demonstration Somme de deux nombres pairs
Deux nombres pairs s'écrivent $2p$ et $2q$, avec $p$ et $q$ entiers. Leur somme est $2p+2q=2(p+q)$. Comme $p+q$ est entier, cette somme est paire.
:::

::: definition Contre-exemple
Pour réfuter « $x+3=3x$ pour tout $x$ », prendre $x=1$ : $4\ne3$. Ce seul cas suffit.
:::

::: retenir
Tester aide à conjecturer ; une démonstration explique pourquoi une propriété vaut pour toutes les valeurs considérées.
:::
''',
270: r'''::: objectifs
Nommer une inconnue, résoudre une opération à trou par une opération inverse et vérifier une réponse dans la situation de départ.
:::

## I. Retrouver un nombre inconnu

::: definition Équation et solution
Une inconnue est un nombre à déterminer. Une équation est une égalité où intervient une inconnue. Une solution est une valeur qui rend cette égalité vraie.
:::

::: methode Une addition à trou
Pour résoudre $x+7=19$, chercher le nombre auquel on ajoute 7 pour obtenir 19 :
$$x=19-7=12$$
Vérification : $12+7=19$.
:::

::: methode Une multiplication à trou
Avec $a\ne0$, l'équation $ax=c$ donne $x=c\div a$.
Pour $5x=18$ :
$$x=18\div5=\frac{18}{5}=3{,}6$$
Vérification : $5\times3{,}6=18$.
:::

::: exemple Une division à trou
Pour $\frac{x}{3}=1$, multiplier 1 par 3 : $x=3$. Pour $2x=0$ et $\frac{x}{2}=0$, la solution est $x=0$.
:::

::: attention
$5x$ signifie $5\times x$. Une solution peut être nulle ou négative si le contexte l'autorise : $x+6=2$ donne $x=2-6=-4$.
:::

## II. Résoudre un problème

::: methode
1. Nommer l'inconnue et son unité.
2. Écrire la relation connue.
3. Retrouver le nombre par les opérations inverses.
4. Vérifier dans la situation initiale et répondre avec une phrase.
:::

::: exemple Des carnets identiques
Trois carnets coûtent 10,50 €. Si $x$ est le prix d'un carnet en euros, $3x=10{,}50$. Donc $x=10{,}50\div3=3{,}50$. Un carnet coûte 3,50 €.
:::

[IMAGE_1]

::: exemple Remonter deux opérations par le raisonnement
Deux pochettes identiques et un emballage de 2 € coûtent 10 €. Retirer d'abord l'emballage : $10-2=8$ €. Partager ensuite le prix des pochettes : $8\div2=4$ € par pochette. Vérifier : $2\times4+2=10$ €.
:::

::: remarque Pour aller plus loin
Une facture de ce type peut se traduire par $2x+2=10$. En 5e, on la traite ici par raisonnement arithmétique. Les techniques générales de résolution des équations $ax+b=c$ sont étudiées en 4e.
:::

::: retenir
L'opération inverse retrouve une valeur ; la substitution permet de la contrôler. Une réponse doit respecter les unités et les contraintes du problème.
:::
'''}

SHEETS = {
266:r'''::: objectifs
Calculer avec des fractions en identifiant toujours le même tout.
:::

## I. Sommes et différences
::: formule
$$\frac ab+\frac cb=\frac{a+c}{b}$$
$$\frac ab-\frac cb=\frac{a-c}{b}\quad(b>0)$$
:::
::: methode
Dénominateurs différents : choisir un multiple commun, écrire des fractions égales, calculer les numérateurs et simplifier.
$$\frac34-\frac16=\frac9{12}-\frac2{12}=\frac7{12}$$
:::
## II. Parts et restes
- Les $\frac35$ de 40 : $(40\div5)\times3=24$.
- Part restante : $1-$ part utilisée.
- Fraction du reste : calculer le reste avant d'appliquer la nouvelle fraction.
::: attention
Ne pas additionner les dénominateurs. Ne pas confondre « du total » et « du reste ». Quantité utilisée + quantité restante = quantité initiale.
:::
''',
267:r'''::: objectifs
Reconnaître un carré, un cube et leurs unités.
:::
## I. Formules
::: formule
$$a^2=a\times a\qquad a^3=a\times a\times a$$
:::
Carrés de 0 à 12 : **0 ; 1 ; 4 ; 9 ; 16 ; 25 ; 36 ; 49 ; 64 ; 81 ; 100 ; 121 ; 144**.
## II. Calculs et grandeurs
- Priorités : parenthèses, puissances, produits/quotients, sommes/différences.
- Aire d'un carré de côté $c$ cm : $c^2$ cm$^2$.
- Volume d'un cube d'arête $c$ cm : $c^3$ cm$^3$.
- $1$ dm$^3=1\,000$ cm$^3$.
::: retenir
Côté doublé : aire multipliée par 4 ; arête doublée : volume multiplié par 8.
:::
::: attention
$4^3=64$, et non 12. $(2+3)^2=25$, tandis que $2^2+3^2=13$.
:::
''',
268:r'''::: objectifs
Écrire une formule, calculer sa valeur et contrôler une égalité.
:::
## I. Traduire
| Expression | Écriture |
|---|---|
| Double de $x$ | $2x$ |
| Successeur de $x$ | $x+1$ |
| Carré de $x$ | $x^2$ |
| Rectangle de côtés $L$ et $\ell$ | $P=2(L+\ell)$ ; $A=L\ell$ |
## II. Réflexes
::: methode
Substitution : remplacer chaque lettre par sa valeur, rétablir les multiplications et suivre les priorités.
Pour $x=2$, $3x^2+2x=3\times4+4=16$.
:::
Pour un motif : **départ + accroissement $\times(n-1)$**. Carrés accolés : $4+3(n-1)=3n+1$ allumettes.
::: attention
Tester une égalité : calculer ses deux membres séparément. Des tests réussis ne constituent pas une preuve pour toutes les valeurs.
:::
''',
269:r'''::: objectifs
Utiliser la distributivité, réduire et justifier une propriété.
:::
## I. Transformer
::: formule
$$k(a+b)=ka+kb$$
$$k(a-b)=ka-kb$$
:::
- Développer : $4(x+3)=4x+12$.
- Factoriser : $6x+18=6(x+3)$.
- Réduire : $3x+5x+2+4=8x+6$.
## II. Justifier
Une preuve utilise une propriété pour toutes les valeurs. Exemple : $2p+2q=2(p+q)$ est pair pour des entiers $p,q$.
Un **contre-exemple** suffit à réfuter une affirmation générale.
::: attention
Multiplier chaque terme : $3(x+5)=3x+15$. Ne pas réduire $3x+5$ à $8x$. Plusieurs tests vrais ne remplacent pas une preuve.
:::
''',
270:r'''::: objectifs
Retrouver une inconnue puis vérifier la réponse.
:::
## I. Opérations inverses
| Équation | Calcul | Vérification |
|---|---|---|
| $x+7=19$ | $x=19-7=12$ | $12+7=19$ |
| $5x=18$ | $x=18\div5=3{,}6$ | $5\times3{,}6=18$ |
| $\frac{x}{3}=1$ | $x=1\times3=3$ | $3\div3=1$ |
## II. Méthode
1. Nommer l'inconnue avec son unité.
2. Traduire la relation connue.
3. Utiliser l'opération inverse.
4. Remplacer l'inconnue dans la relation initiale et conclure.
::: attention
$5x$ est un produit. Zéro peut être une solution : $2x=0$ donne $x=0$. Une solution négative est possible si le contexte l'autorise.
:::
'''}

def main():
    for code in range(266,271):
        d=next(BASE.glob(str(code)+'_*'))
        (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'coordination','maj':'2026-10-28'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
        figures={}
        corr={'cours':{},'fiches':{},'exercices':{}}
        def image(kind,oid,pos,name,alt,tikz):
            figures[name]=tikz
            corr[kind].setdefault(str(oid),{})[str(pos)]={'fichier':name+'.png','alt':alt}
        course=next(d.glob('cours_*.txt')); sheet=next(d.glob('fiche_*.txt'))
        cid=meta['cours'][0]['id']; sid=meta['fiches'][0]['id']
        course.write_text(course.read_text(encoding='utf-8').splitlines()[0]+'\n\n<!-- optitab:1 -->\n'+COURSES[code],encoding='utf-8')
        sheet.write_text(sheet.read_text(encoding='utf-8').splitlines()[0]+'\n\n<!-- optitab:1 -->\n'+SHEETS[code],encoding='utf-8')
        if code==266:
            tikz=r'''\begin{tikzpicture}
\fill[otNavy!22] (0,0) rectangle (3,.7);
\fill[otGreen!25] (0,-1.5) rectangle (3.33333,-.8);
\draw[geoTrait] (0,0) rectangle (4,.7);
\draw[geoTrait] (0,-1.5) rectangle (4,-.8);
\foreach \x in {1,2,3} {\draw[otNavy!55] (\x,0)--(\x,.7);}
\foreach \x in {.66667,1.33333,2,2.66667,3.33333} {\draw[otNavy!55] (\x,-1.5)--(\x,-.8);}
\node[anchor=west] at (4.25,.35) {$\frac34$};
\node[anchor=west] at (4.25,-1.15) {$\frac56$};
\node[anchor=south,text=otMuted] at (2,1) {Même unité, partages différents};
\end{tikzpicture}'''
        elif code==267: tikz=figure_cube(3)
        elif code==268:
            tikz=r'''\begin{tikzpicture}
\foreach \x in {0,1,2} {\draw[geoTrait] (\x,0) rectangle +(1,1);}
\node[anchor=south] at (1.5,1.25) {3 carrés accolés};
\node[anchor=north,text=otGreenDark] at (1.5,-.25) {$4+3+3=10$ allumettes};
\end{tikzpicture}'''
        elif code==269: tikz=figure_rectangle(4,3)
        else: tikz=figure_facture(2,2,10)
        image('cours',cid,1,'cours_modele',f"Illustration du cours : {meta['titre']}",tikz)
        old=(d/'exercices.txt').read_text(encoding='utf-8')
        blocks=[b.strip() for b in re.split(r'^===[ \t]*$',old,flags=re.M) if b.strip()]
        new=[]
        for b in blocks:
            eid=int(re.search(r'^Id:\s*(\d+)',b,re.M)[1])
            header,body=b.split('Énoncé:',1)
            statement=body.split('Étapes:')[0].strip()
            statement=re.sub(r'\[IMAGE_\d+\]\s*','',statement)
            qs=re.findall(r'^\d+\. (.+)$',statement,re.M)
            assert len(qs)==6,(eid,len(qs))
            steps=[]; answers=[]
            def q(i,method,work,result):
                steps.append(question(i,qs[i-1],method,work,result)); answers.append(result)
            if code==266:
                m=re.search(r'contient (\d+) L.*?\\frac\{(\d+)\}\{(\d+)\}.*?\\frac\{(\d+)\}\{(\d+)\}',statement,re.S)
                if m:
                    total,a,den,c,den2=map(int,m.groups()); assert den==2*den2
                    used=F(a,den)+F(c,den2); rest=1-used
                    morning=total*F(a,den); afternoon=total*F(c,den2)
                    q(1,'Identifier le tout auquel chaque fraction se rapporte.','Les deux prélèvements sont exprimés comme des parts du volume initial. Aucun remplissage ne change cette référence.','Les deux fractions portent sur le même réservoir initial : on peut les additionner.')
                    q(2,'Obtenir le même dénominateur sans changer la valeur de la fraction.',calc(rf'\frac{{{c}}}{{{den2}}}=\frac{{{c}\times2}}{{{den2}\times2}}=\frac{{{2*c}}}{{{den}}}'),rf'$\frac{{{c}}}{{{den2}}}=\frac{{{2*c}}}{{{den}}}$.')
                    q(3,'Additionner les numérateurs, puis simplifier.',calc(rf'\frac{{{a}}}{{{den}}}+\frac{{{2*c}}}{{{den}}}=\frac{{{a+2*c}}}{{{den}}}='+frac(used)),rf'La fraction utilisée est ${frac(used)}$.')
                    q(4,'Écrire le tout avec le même dénominateur.',calc(rf'1-\frac{{{a+2*c}}}{{{den}}}=\frac{{{den}}}{{{den}}}-\frac{{{a+2*c}}}{{{den}}}='+frac(rest)),rf'Il reste ${frac(rest)}$ du volume initial.')
                    q(5,'Appliquer chaque fraction au volume initial.',calc(rf'V_{{\text{{utilisé}}}}&={total}\times {frac(used)}={frac(total*used)}',rf'V_{{\text{{restant}}}}&={total}-{frac(total*used)}={frac(total*rest)}'),f'{int(total*used)} L utilisés ; {int(total*rest)} L restants.')
                    compare='plus' if afternoon>morning else 'moins' if afternoon<morning else 'autant'
                    q(6,'Calculer séparément chaque prélèvement et comparer.',calc(rf'V_{{\text{{matin}}}}&=({total}\div {den})\times {a}={frac(morning)}',rf'V_{{\text{{après-midi}}}}&=({total}\div {den2})\times {c}={frac(afternoon)}'),f'On utilise {compare} d’eau l’après-midi ; l’écart vaut {abs(int(afternoon-morning))} L.')
                else:
                    total,den=map(int,re.search(r'possède (\d+) livres.*?sur (\d+)',statement,re.S).groups())
                    morning=F(total,den); remaining=total-morning; afternoon=remaining/4; done=morning+afternoon; left=total-done
                    statement=statement.replace('1/d et 1/4',rf'$\frac1{{{den}}}$ et $\frac14$')
                    qs[5]=qs[5].replace('1/d et 1/4',rf'$\frac1{{{den}}}$ et $\frac14$')
                    for i,method,expr,res in [(1,'Partager le total selon la fraction du matin.',rf'{total}\div {den}={frac(morning)}',morning),(2,'Retirer les livres déjà rangés.',rf'{total}-{frac(morning)}={frac(remaining)}',remaining),(3,'Appliquer le quart au reste, et non au total.',rf'{frac(remaining)}\div4={frac(afternoon)}',afternoon),(4,'Additionner les deux quantités rangées.',rf'{frac(morning)}+{frac(afternoon)}={frac(done)}',done),(5,'Retirer du total les livres rangés dans la journée.',rf'{total}-{frac(done)}={frac(left)}',left)]:
                        q(i,method,calc(expr),f'{int(res)} livres.')
                    q(6,'Identifier les deux références avant toute addition.',f'Le matin, le tout est constitué des {total} livres. L’après-midi, le quart porte sur les {int(remaining)} livres restants.',f'On ne peut pas additionner directement ces fractions : le quart porte sur {int(remaining)} livres, pas sur {total}.')
            elif code==267:
                n=int(re.search(r'carrée de (\d+)',statement)[1])
                q(1,'Compter les lignes et les colonnes.',f'Il y a {n} lignes de {n} carreaux chacune.',rf'Le nombre de carreaux s’écrit ${n}\times{n}={n}^2$.')
                q(2,'Multiplier le nombre de carreaux par l’aire d’un carreau.',calc(rf'A={n}^2\times1={n*n}'),f'L’aire de la mosaïque est {n*n} cm².')
                q(3,'Compter les cubes le long d’une arête verticale.',f'Chaque couche a une épaisseur d’un petit cube ; la hauteur mesure {n} petits cubes.',f'Le grand cube comporte {n} couches.')
                q(4,'Multiplier le nombre de cubes par couche par le nombre de couches.',calc(rf'N={n}\times{n}\times{n}={n}^3={n**3}'),f'Le cube contient {n**3} petits cubes.')
                q(5,'Le nombre de lignes et le nombre de colonnes doublent.',calc(rf'A_{{\text{{nouvelle}}}}&=({2*n})^2={4*n*n}',rf'\frac{{A_{{\text{{nouvelle}}}}}}{{A_{{\text{{initiale}}}}}}&=\frac{{{4*n*n}}}{{{n*n}}}=4'),f'L’aire est multipliée par 4 ; elle vaut {4*n*n} cm².')
                q(6,'Les trois dimensions du cube doublent.',calc(rf'V_{{\text{{nouveau}}}}&=({2*n})^3={8*n**3}',rf'\frac{{V_{{\text{{nouveau}}}}}}{{V_{{\text{{initial}}}}}}&=\frac{{{8*n**3}}}{{{n**3}}}=8'),f'Le volume est multiplié par 8 ; il vaut {8*n**3} cm³.')
                statement=statement.replace('\n\n1.','\n\n[IMAGE_1]\n\n1.',1)
                image('exercices',eid,1,f'carre_cube_{n}',f'Mosaïque de {n} carreaux de côté et cube de {n} petits cubes par arête.',figure_cube(n))
            elif code==268:
                start,inc=map(int,re.search(r'utilise (\d+) allumettes.*?ajoute (\d+) allumettes',statement,re.S).groups())
                rank=int(re.search(r'rang (\d+)',qs[2])[1])
                target=int(re.search(r'(\d+) allumettes',qs[4])[1]); c=start-inc; found=(target-c)//inc
                q(1,'Ajouter le même nombre d’allumettes à chaque nouveau rang.',calc(rf'N_2&={start}+{inc}={start+inc}',rf'N_3&={start+inc}+{inc}={start+2*inc}'),f'Rang 2 : {start+inc} allumettes ; rang 3 : {start+2*inc} allumettes.')
                q(2,'Compter les accroissements après le premier rang.',f'Entre le rang 1 et le rang $n$, il y a $n-1$ accroissements de {inc} allumettes.\n'+calc(rf'N={start}+{inc}(n-1)={inc}n+{c}'),rf'Le nombre d’allumettes au rang $n$ vaut ${inc}n+{c}$.')
                value=inc*rank+c
                q(3,'Remplacer la lettre par le rang demandé.',calc(rf'N={inc}\times{rank}+{c}={value}'),f'Au rang {rank}, il y a {value} allumettes.')
                q(4,'Tester la formule séparément sur chacun des premiers rangs.',calc(rf'N_1&={inc}\times1+{c}={start}',rf'N_2&={inc}\times2+{c}={start+inc}',rf'N_3&={inc}\times3+{c}={start+2*inc}'),'Oui : les trois valeurs retrouvées coïncident avec les premiers rangs. Ces tests seuls ne constituent pas une preuve générale.')
                q(5,'Retirer le terme fixe puis partager en accroissements égaux.',calc(rf'n=({target}-{c})\div{inc}={found}')+'\nVérification : '+rf'${inc}\times{found}+{c}={target}$.',f'On obtient {target} allumettes au rang {found}.')
                q(6,'Comparer le nombre au rang double avec le double du nombre initial.',calc(rf'N_{{{2*rank}}}&={inc}\times{2*rank}+{c}={2*inc*rank+c}',rf'2N_{{{rank}}}&=2\times{value}={2*value}'),f'Non : au rang {2*rank}, il y a {2*inc*rank+c} allumettes, alors que le double de {value} vaut {2*value}.')
            elif code==269:
                k,add=map(int,re.search(r'hauteur de (\d+) cm.*?x \+ (\d+) cm',statement,re.S).groups())
                val=int(re.search(r'x = (\d+)',qs[3])[1]); area=k*(val+add)
                statement=statement.replace(f'largeur de x + {add} cm',rf'largeur de $(x+{add})$ cm').replace('x positif','$x$ strictement positif').replace('largeurs x cm', 'largeurs $x$ cm').replace(f'x = {val} cm',rf'$x={val}$').replace('valeur de x','valeur de $x$')
                qs=re.findall(r'^\d+\. (.+)$',statement,re.M)
                q(1,'Multiplier toute la largeur par la hauteur.',rf'La largeur vaut $(x+{add})$ cm et la hauteur {k} cm.',rf'L’aire vaut ${k}(x+{add})$ cm².')
                q(2,'Utiliser la hauteur commune et la largeur de chaque morceau.',calc(rf'A_1&={k}\times x={k}x',rf'A_2&={k}\times{add}={k*add}'),rf'Les deux aires sont ${k}x$ cm² et ${k*add}$ cm².')
                q(3,'Additionner les aires des deux morceaux.','Les rectangles recouvrent exactement la figure, sans chevauchement.\n'+calc(rf'{k}(x+{add})={k}x+{k*add}'),rf'La forme développée de l’aire est ${k}x+{k*add}$ cm².')
                q(4,'Calculer séparément les deux expressions pour la même valeur.',calc(rf'{k}({val}+{add})&={k}\times{val+add}={area}',rf'{k}\times{val}+{k*add}&={k*val}+{k*add}={area}'),f'Les deux expressions donnent {area} cm².')
                q(5,'Contrôler que le facteur multiplie chaque terme.',rf'Le morceau fixe a une largeur de {add} cm et une hauteur de {k} cm. Son aire est ${k}\times{add}={k*add}$ cm².',rf'Le terme constant est ${k*add}$, car ${add}$ doit aussi être multiplié par ${k}$.')
                q(6,'Raisonner sur la bande ajoutée pour toute valeur de la lettre.',rf'Lorsque $x$ augmente de 1, on ajoute une bande de largeur 1 cm et de hauteur {k} cm. Son aire vaut ${k}\times1={k}$ cm².',f'L’aire augmente de {k} cm², quelle que soit la valeur initiale de $x$.')
                statement=statement.replace('\n\n1.','\n\n[IMAGE_1]\n\n1.',1)
                image('exercices',eid,1,f'rectangle_{k}_{add}',f'Rectangle de hauteur {k} cm partagé en largeurs x cm et {add} cm.',figure_rectangle(k,add))
            else:
                m=re.search(r'achète (\d+) pochettes.*?emballage à (\d+) €.*?total(e)? est de (\d+) €',statement,re.S)
                if m:
                    n,fee,_,total=m.groups(); n,fee,total=map(int,(n,fee,total)); subtotal=total-fee; price=F(subtotal,n); delta=F(6,n)
                    q(1,'Nommer précisément ce que l’on cherche.','Toutes les pochettes sont identiques ; leur prix unitaire est donc le même.','L’inconnue $x$ est le prix d’une pochette, en euros.')
                    q(2,'Additionner le prix des pochettes et celui de l’emballage.',rf'Les {n} pochettes coûtent ${n}x$ euros. L’emballage ajoute {fee} euros.',rf'La facture se traduit par ${n}x+{fee}={total}$.')
                    q(3,'Retirer de la facture la dépense qui ne concerne pas les pochettes.',calc(rf'{total}-{fee}={subtotal}'),f'Les seules pochettes coûtent {subtotal} €.')
                    q(4,'Partager le prix des pochettes en parts égales.',calc(rf'x={subtotal}\div{n}={frac(price)}'),rf'Une pochette coûte ${frac(price)}$ €.')
                    q(5,'Reconstituer la facture avec le prix trouvé.',calc(rf'{n}\times{frac(price)}+{fee}={subtotal}+{fee}={total}'),'On retrouve le total initial : la réponse est vérifiée.')
                    q(6,'Répartir les 6 € supplémentaires sur le même nombre de pochettes.',calc(rf'\text{{Hausse par pochette}}&=6\div{n}={frac(delta)}',rf'\text{{Nouveau prix}}&={frac(price)}+{frac(delta)}={frac(price+delta)}'),rf'Le prix augmente de ${frac(delta)}$ € par pochette ; le nouveau prix est ${frac(price+delta)}$ €.')
                    statement=statement.replace('\n\n1.','\n\n[IMAGE_1]\n\n1.',1)
                    statement=statement.replace('4. Résoudre l’équation et donner le prix d’une pochette.','4. Retrouver le prix d’une pochette par les opérations inverses.')
                    steps[3]=steps[3].replace('Résoudre l’équation et donner le prix d’une pochette.','Retrouver le prix d’une pochette par les opérations inverses.')
                    statement=statement.replace('\n\n[IMAGE_1]', '\n\n'+box('remarque','Pour aller plus loin','La facture comporte deux opérations. On la résout ici par un raisonnement arithmétique. La résolution algébrique générale des équations $ax+b=c$ relève de la 4e.')+'\n[IMAGE_1]')
                    image('exercices',eid,1,f'facture_{n}_{fee}_{total}',f'Facture de {n} pochettes de prix inconnu et emballage de {fee} euros, total de {total} euros.',figure_facture(n,fee,total))
                else:
                    den,out=map(int,re.search(r'partage en (\d+) parts égales et affiche (\d+)',statement).groups()); value=den*out
                    q(1,'Traduire le partage par une division.',f'Le nombre choisi est partagé en {den} parts égales ; chaque part vaut {out}.',rf'L’équation est $\frac{{x}}{{{den}}}={out}$.')
                    q(2,'Utiliser l’opération inverse de la division.',f'Pour retrouver le nombre avant le partage, multiplier la valeur d’une part par le nombre de parts.',f'Il faut multiplier {out} par {den}.')
                    q(3,'Effectuer la multiplication inverse.',calc(rf'x={out}\times{den}={value}'),rf'La solution est $x={value}$.')
                    q(4,'Remettre la valeur trouvée dans le programme.',calc(rf'{value}\div{den}={out}'),'On retrouve bien le résultat affiché.')
                    q(5,'Chercher le nombre dont le produit par un nombre non nul est zéro.',calc(rf'{den}\times0=0'),r'La solution est $x=0$.')
                    q(6,'Distinguer l’équation et les contraintes de la situation.',f'Le deuxième programme accepte zéro et donne bien zéro. Une équation d’addition peut aussi avoir une solution négative : $x+6=2$ donne $x=-4$.','Non. Zéro ou un nombre négatif peut convenir si le contexte l’autorise.')
            header=re.sub(r'^Image:.*\n','',header,flags=re.M)
            # Les images sont entièrement pilotées par correspondance.json.
            result='\n'.join(f'{i}. {a}' for i,a in enumerate(answers,1))
            nb=header.rstrip()+'\n\nÉnoncé:\n'+statement+'\n\nÉtapes:\n<!-- optitab:1 -->\n'+'\n'.join(steps)+'\nSolution:\n<!-- optitab:1 -->\n'+result+'\n'
            new.append(nb)
        (d/'exercices.txt').write_text('\n===\n\n'.join(new),encoding='utf-8')
        fd=d/'figures'; fd.mkdir(exist_ok=True)
        (fd/'figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ originales, palette et polices communes du chantier."""\nFIGURES = {\n'+''.join(f'{name!r}: r"""{tikz}""",\n' for name,tikz in figures.items())+'}\n',encoding='utf-8')
        (fd/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(code,len(new),'exercices',len(figures),'figures')

if __name__=='__main__':
    main()
