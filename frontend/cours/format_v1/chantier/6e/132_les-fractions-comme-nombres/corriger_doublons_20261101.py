"""Remplace cinq doublons exacts sans régénérer aucun autre bloc ni figure."""
from pathlib import Path
from fractions import Fraction as F
import json,re,shutil
HERE=Path(__file__).resolve().parent
MARK='<!-- optitab:1 -->'
def q(question,methode,body,reponse,title='Développer le raisonnement'):
    body=re.sub(r'\$\$(.*?)\$\$',lambda m:'\n\n$$'+m[1]+'$$\n\n',body,flags=re.S).strip()
    return dict(question=question,methode=methode,etapes=[(title,body)],reponse=reponse)
def ex(eid,titre,intro,questions,note):
    return dict(id=eid,titre='Entraînement - '+titre,difficulte='medium',introduction=intro,questions=questions,note=note)
REPLACEMENTS={132:[
ex(3279,'Fractions - Comparer des longueurs en huitièmes',r'Un ruban A mesure $\frac58$ m et un ruban B mesure $\frac78$ m. Un troisième ruban C mesure 1 m.',[
 q('Quel ruban est le plus long entre A et B ?', 'Comparer des nombres de parts de même taille.',r'Les deux longueurs sont exprimées en huitièmes de mètre. Sept huitièmes représentent deux parts de plus que cinq huitièmes : $\frac58\lt\frac78$.','B est le plus long.'),
 q('Classer les trois longueurs dans l’ordre croissant.', 'Écrire un mètre en huitièmes.',r'Un mètre entier contient huit huitièmes : $1=\frac88$. On compare donc 5, 7 et 8 parts identiques.',r'$\frac58\lt\frac78\lt1$, soit A, B, C.'),
 q('Quelle longueur manque-t-il au ruban A pour atteindre 1 m ?', 'Compléter cinq huitièmes jusqu’à huit huitièmes.',r'Il manque trois parts de $\frac18$ m. $$\frac58+\frac38=\frac88=1$$',r'$\frac38$ m.')], 'Pour comparer des fractions de même dénominateur, on compare les numérateurs ; l’unité de référence doit rester la même.'),
ex(3286,'Fractions - Retrouver le ruban entier',r'Un morceau de 12 cm représente les $\frac35$ d’un ruban. Le ruban est partagé mentalement en cinq parties de même longueur.',[
 q('Quelle longueur représente un cinquième du ruban ?', 'Partager la longueur connue en trois parts égales.',r'Les 12 cm correspondent à trois cinquièmes, donc à trois parts. $$12\div3=4$$','4 cm.'),
 q('Quelle est la longueur du ruban entier ?', 'Reconstituer les cinq parts de même longueur.',r'Chaque part mesure 4 cm. Le ruban contient cinq parts. $$5\times4=20$$','20 cm.'),
 q('Quelle longueur reste-t-il après avoir retiré le morceau de 12 cm ?', 'Retirer le morceau connu au ruban entier, puis contrôler par les parts.',r'$$20-12=8$$ Il reste deux parts de 4 cm, ce qui confirme $2\times4=8$.','8 cm, soit deux cinquièmes du ruban.')], 'Quand la longueur connue représente trois parts, on la divise d’abord par trois ; on ne la divise pas directement par cinq.'),
ex(3287,'Fractions - Changer de tout de référence',r'Alice mange la moitié d’une petite tarte découpée en 4 parts égales. Bilal mange la moitié d’une grande tarte découpée en 8 parts égales. La grande tarte contient deux fois autant de pâte que la petite.',[
 q('Combien de parts mange chacun ?', 'Prendre la moitié du nombre de parts de chaque tarte.',r'$$4\div2=2\qquad8\div2=4$$ Alice mange deux parts de sa tarte et Bilal quatre parts de la sienne.','Alice : 2 parts ; Bilal : 4 parts.'),
 q('Ont-ils mangé la même fraction de leur propre tarte ?', 'Comparer les fractions de chaque tout.',r'$$\frac24=\frac12\qquad\frac48=\frac12$$ Les deux fractions représentent une moitié de la tarte choisie comme référence.','Oui : chacun a mangé la moitié de sa propre tarte.'),
 q('Ont-ils mangé la même quantité de pâte ? Justifier.', 'Tenir compte de la taille du tout avant de comparer des fractions.',r'La grande tarte représente deux petites tartes. Sa moitié représente donc une petite tarte entière. Alice n’a mangé que la moitié d’une petite tarte. Bilal a mangé deux fois la quantité de pâte mangée par Alice.','Non : Bilal a mangé deux fois autant de pâte.')], 'Des fractions égales de deux touts différents ne donnent pas forcément des quantités égales.'),
ex(3292,'Fractions - Vérifier une graduation décimale',r'Sur une demi-droite graduée, une unité mesure 10 cm. On place A à 13 cm de l’origine et B à 17 cm de l’origine.',[
 q('Quelle longueur représente un dixième d’unité ?', 'Partager la longueur d’une unité en dix parts égales.',r'$$10\div10=1$$ Chaque centimètre représente donc un dixième d’unité.','1 cm.'),
 q('Écrire les abscisses de A et B sous forme fractionnaire puis décimale.', 'Compter les dixièmes depuis l’origine.',r'A est à treize dixièmes de l’origine et B à dix-sept dixièmes. $$\frac{13}{10}=1{,}3\qquad\frac{17}{10}=1{,}7$$',r'A : $\frac{13}{10}=1{,}3$ ; B : $\frac{17}{10}=1{,}7$.'),
 q('Un élève écrit que A est entre 0 et 1 car 13 est un entier. A-t-il raison ?', 'Comparer le numérateur au nombre de dixièmes dans une unité.',r'Une unité correspond à dix dixièmes. Treize dixièmes dépassent donc une unité, mais restent inférieurs à vingt dixièmes. $$1\lt\frac{13}{10}\lt2$$','Non : A est entre 1 et 2.'),
 q('Quelle est la distance de A à B en centimètres, puis en unités ?', 'Distinguer la mesure sur le dessin et l’unité de graduation.',r'$$17-13=4\qquad4\div10=0{,}4$$ Quatre centimètres représentent quatre dixièmes d’unité.','4 cm, soit 0,4 unité.')], 'La longueur choisie pour l’unité relie la règle graduée en centimètres et les abscisses : ici 1 cm représente 0,1 unité.')],
134:[ex(3376,'Proportionnalité - Combien de convives avec un stock ?', 'Une recette pour 6 personnes demande 450 g de farine. Les quantités sont proportionnelles au nombre de personnes. On dispose de 1 000 g de farine.',[
 q('Quelle masse de farine faut-il pour une personne ?', 'Revenir à l’unité en partageant la masse en six parts égales.',r'$$450\div6=75$$ Une part de recette demande 75 g de farine.','75 g.'),
 q('Peut-on servir 12 personnes avec le stock disponible ?', 'Doubler la recette pour six personnes, puis comparer au stock.',r'$$2\times450=900\qquad1\,000-900=100$$ Il faut 900 g, ce qui laisse 100 g.','Oui : il reste 100 g.'),
 q('Combien de personnes peut-on servir au maximum avec 1 000 g ?', 'Tester deux effectifs entiers consécutifs.',r'$$\begin{aligned}13\times75&=975\le1\,000\\14\times75&=1\,050>1\,000\end{aligned}$$ Treize parts sont possibles, mais quatorze demanderaient plus que le stock.','13 personnes au maximum.'),
 q('Après avoir servi le maximum de personnes, combien de farine reste-t-il ? Combien faudrait-il ajouter pour une personne de plus ?', 'Calculer le reste, puis compléter jusqu’à une part supplémentaire.',r'$$\begin{aligned}1\,000-975&=25\\75-25&=50\end{aligned}$$ Les 25 g restants ne suffisent pas à préparer une part de 75 g.','Il reste 25 g ; il faudrait ajouter 50 g.')], 'Un stock peut permettre une quantité non entière de recette ; pour servir des personnes entièrement, on vérifie les deux effectifs entiers qui encadrent la limite.') ]}
def render(e):
    out=[f"=== {e['titre']}",f"Id: {e['id']}",f"Difficulté: {e['difficulte']}",'','Énoncé:',MARK,e['introduction'],'']
    out += [f"{i}. {x['question']}" for i,x in enumerate(e['questions'],1)]
    out += ['','Étapes:',MARK]
    for i,x in enumerate(e['questions'],1):
        out += [f"## Question {i} : {x['question']}",'','::: methode',x['methode'],':::','']
        for title,body in x['etapes']: out += ['::: etape '+title,body,':::','']
        out += ['::: resultat',x['reponse'],':::','']
    out += ['::: retenir',e['note'],':::','','Solution:',MARK]+[f"{i}. {x['reponse']}" for i,x in enumerate(e['questions'],1)]
    return '\n'.join(out)+'\n\n'
if __name__=='__main__':
    for n,replacements in REPLACEMENTS.items():
        d=next(HERE.parent.glob(str(n)+'_*'))
        backup=d/'sauvegardes/correction_doublons_2026-11-01';backup.mkdir(parents=True,exist_ok=True)
        for name in ('exercices.txt','revision_20261030.json','etat.json'):
            if not (backup/name).exists():shutil.copy2(d/name,backup/name)
        (d/'etat.json').write_text(json.dumps(dict(statut='en_cours',agent='corriger_doublons_calculs',maj='2026-11-01'),indent=2),encoding='utf-8')
        text=(d/'exercices.txt').read_text(encoding='utf-8')
        records=json.loads((d/'revision_20261030.json').read_text(encoding='utf-8'))
        for e in replacements:
            matches=list(re.finditer(r'^=== [^\n]+\nId: '+str(e['id'])+r'\n.*?(?=^===|\Z)',text,re.M|re.S))
            assert len(matches)==1,(n,e['id'],len(matches))
            m=matches[0];text=text[:m.start()]+render(e)+text[m.end():]
            records=[e if x['id']==e['id'] else x for x in records]
        assert len(records)==21
        assert len({x['introduction']+' '.join(q['question'] for q in x['questions']) for x in records})==21
        (d/'exercices.txt').write_text(text,encoding='utf-8')
        (d/'revision_20261030.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
        print(n,'corrigé',','.join(str(e['id']) for e in replacements))
