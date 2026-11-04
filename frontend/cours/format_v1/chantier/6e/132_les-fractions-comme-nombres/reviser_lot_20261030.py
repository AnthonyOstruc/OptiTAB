"""Révision pédagogique sixième : sauvegarde préalable, génération UTF-8, identifiants conservés."""
from pathlib import Path
from fractions import Fraction as F
import json, re, shutil

BASE=Path(__file__).resolve().parent.parent
IDS=(132,134,135,136,137,284,285)
DIRS={n:next(BASE.glob(str(n)+'_*')) for n in IDS}
MARK='<!-- optitab:1 -->'
RECORDS={n:[] for n in IDS}
CHECKS=[]

def dec(x):
    x=F(x)
    s=format(float(x),'.8f').rstrip('0').rstrip('.')
    return s.replace('.', '{,}')
def frac(a,b=1):
    x=F(a,b)
    return str(x.numerator) if x.denominator==1 else rf'\frac{{{x.numerator}}}{{{x.denominator}}}'
def M(s):
    if s.count('=')>=2 and not any(t in s for t in (r'\begin',r'\quad',r'\qquad','<','>',r'\ne',r'\le',r'\ge')):
        left,*right=s.split('=')
        s=r'\begin{aligned}'+left+'&='+r'\\&='.join(right)+r'\end{aligned}'
    return '$$'+s+'$$'
def chain(*s): return M(r'\begin{aligned}'+r'\\'.join(s)+r'\end{aligned}')
def Q(q,m,steps,a): return dict(question=q,methode=m,etapes=steps,reponse=a)
def C(a,b):
    CHECKS.append((str(a),str(b)))
    assert F(a)==F(b),(a,b)
def add(n,eid,title,diff,intro,qs,note):
    RECORDS[n].append(dict(id=eid,titre=title,difficulte=diff,introduction=intro,questions=qs,note=note))

for n,d in DIRS.items():
    backup=d/'sauvegardes'/'revision_2026-10-30'
    backup.mkdir(parents=True,exist_ok=True)
    for p in d.glob('*.txt'):
        if not (backup/p.name).exists(): shutil.copy2(p,backup/p.name)
    if (d/'figures').exists() and not (backup/'figures').exists(): shutil.copytree(d/'figures',backup/'figures')
    (d/'etat.json').write_text(json.dumps(dict(statut='en_cours',agent='calculs',maj='2026-10-30'),ensure_ascii=False,indent=2),encoding='utf-8')

# Conserver les données des familles utiles, mais développer réellement chaque raisonnement.
for n,d in DIRS.items():
    if n==136: continue
    old=(d/'sauvegardes'/'revision_2026-10-30'/'exercices.txt').read_text(encoding='utf-8')
    blocks=[b for b in re.split(r'^===[ \t]*$',old,flags=re.M) if re.search(r'^Id:',b,re.M)]
    for i,b in enumerate(blocks):
        eid=int(re.search(r'^Id: (\d+)',b,re.M)[1]); level=i//7
        intro=b.split('Énoncé:\n',1)[1].split('\nÉtapes:',1)[0].replace(MARK,'')
        intro=re.sub(r'\[IMAGE_\d+\]','',intro).strip().split('\n\n1.',1)[0].strip()
        title=b.strip().splitlines()[0].replace('=== ','')
        title=re.sub(r' - \d+\.',f' - {i+1}.',title,count=1)
        diff='easy' if i<7 else 'medium'
        if diff=='medium': title=title.replace('Problème -','Entraînement -',1)
        qs=[]
        if n==132:
            a,z=map(int,re.search(r'(\d+) tartes.*?entre (\d+) personnes',intro).groups())
            cmp='moins d’une tarte' if a<z else 'exactement une tarte' if a==z else 'plus d’une tarte'
            C(F(a,z)*z,a);C(F(2*a,2*z),F(a,z))
            qs=[
                Q('Quelle division décrit la part d’une personne ?','Diviser la quantité totale par le nombre de parts égales.', [('Identifier le total et le nombre de parts',f'Il y a {a} tartes à distribuer en {z} parts identiques : on cherche la quantité reçue dans une seule part.')],rf'${a}\div{z}$.'),
                Q('Exprimer cette part comme une fraction de tarte.','Écrire le quotient exact sous forme fractionnaire.', [('Passer de la division au nombre',M(rf'{a}\div{z}=\frac{{{a}}}{{{z}}}'))],rf'$\frac{{{a}}}{{{z}}}$ de tarte.'),
                Q(f'Chaque tarte est coupée en {z} morceaux égaux. Combien obtient-on de morceaux en tout ?','Compter le même nombre de morceaux pour chaque tarte.', [('Déterminer la taille d’un morceau',rf'Un morceau mesure $\frac{{1}}{{{z}}}$ de tarte.'),('Compter tous les morceaux',M(rf'{a}\times{z}={a*z}'))],f'{a*z} morceaux.'),
                Q('Combien de ces morceaux reçoit chaque personne ?','Répartir les morceaux sans modifier leur taille.', [('Partager les morceaux',M(rf'{a*z}\div{z}={a}')),('Reconstituer la part',rf'{a} morceaux de $\frac{{1}}{{{z}}}$ de tarte représentent $\frac{{{a}}}{{{z}}}$ de tarte.')],f'{a} morceaux.'),
                Q('Comparer la part d’une personne à une tarte entière.','Comparer le nombre de morceaux reçus au nombre nécessaire pour une unité.', [('Compter les morceaux d’une unité',f'Une tarte entière contient {z} de ces morceaux ; une personne en reçoit {a}.')],f'Chaque personne reçoit {cmp}.'),
                Q('Si on double les tartes et les personnes, la part change-t-elle ?','Comparer les quotients des deux partages.', [('Doubler les deux quantités',f'On partage alors {2*a} tartes entre {2*z} personnes.'),('Réduire la nouvelle fraction',M(rf'\frac{{{2*a}}}{{{2*z}}}=\frac{{{a}\times2}}{{{z}\times2}}=\frac{{{a}}}{{{z}}}'))],'Non : chaque personne reçoit la même quantité.')]
            note='Le dénominateur précise la taille des morceaux ; le numérateur indique combien on en prend. Des parts égales sont indispensables.'
        elif n==137:
            dims=re.search(r'(\d+) dm.*?(\d+) dm',intro)
            if not dims: raise ValueError(intro)
            a,z=map(int,dims.groups()); area=a*z
            for x,y in [(F(area,100),F(a,10)*F(z,10)),(area*100,a*10*z*10),(2*area,2*a*z)]: C(x,y)
            qs=[
                Q('Combien de carreaux de 1 dm de côté tient-on dans une ligne ?','Comparer la longueur de la ligne au côté du carreau.', [('Compter les unités le long du bord',M(rf'{a}\div1={a}'))],f'{a} carreaux.'),
                Q('Combien de lignes et combien de carreaux au total ?','Multiplier le nombre de carreaux par ligne par le nombre de lignes.', [('Compter les lignes',f'La largeur est {z} dm : il y a {z} lignes de carreaux.'),('Compter la surface pavée',M(rf'{a}\times{z}={area}'))],f'{z} lignes et {area} carreaux.'),
                Q('Quelle est l’aire en décimètres carrés ?','Un carreau de 1 dm de côté représente une unité d’aire.', [('Associer un carreau à son aire',rf'$1\ \mathrm{{dm}}\times1\ \mathrm{{dm}}=1\ \mathrm{{dm}}^2$ ; les {area} carreaux couvrent la surface sans chevauchement.')],rf'${area}\ \mathrm{{dm}}^2$.'),
                Q('Convertir cette aire en centimètres carrés.','Un carré de 1 dm de côté contient 100 carrés de 1 cm de côté.', [('Justifier le facteur 100',M(r'1\ \mathrm{dm}^2=10\times10\ \mathrm{cm}^2=100\ \mathrm{cm}^2')),('Convertir l’aire',M(rf'{area}\times100={area*100}'))],rf'${area*100}\ \mathrm{{cm}}^2$.'),
                Q('Convertir cette aire en mètres carrés.','Il faut 100 décimètres carrés pour un mètre carré.', [('Passer à une unité plus grande',M(rf'{area}\div100={dec(F(area,100))}'))],rf'${dec(F(area,100))}\ \mathrm{{m}}^2$.'),
                Q('On double seulement la longueur. L’aire double-t-elle ? Le périmètre aussi ?','Comparer séparément la surface couverte et la longueur du contour.', [('Calculer la nouvelle aire',M(rf'{2*a}\times{z}={2*area}')),('Comparer les contours',chain(rf'P_1&=2\times({a}+{z})={2*(a+z)}',rf'P_2&=2\times({2*a}+{z})={2*(2*a+z)}'))],rf'L’aire double : ${2*area}\ \mathrm{{dm}}^2$. Le périmètre passe de {2*(a+z)} à {2*(2*a+z)} dm : il ne double pas.')]
            note='L’aire mesure une surface et s’exprime en unités carrées ; le périmètre mesure le contour et s’exprime en unités de longueur.'
        elif n==284:
            a,z=map(int,re.search(r'\\frac\{(\d+)\}\{(\d+)\}',intro).groups())
            v=int(re.search(r'(\d+) L',intro)[1]); used=F(a+2,z); left=1-used
            C(v*used+v*left,v);C(F(1,z//2),F(2,z))
            qs=[
                Q('Les deux fractions ont-elles la même référence ?','Identifier le tout utilisé avant de comparer ou d’additionner.', [('Lire les deux indications',f'Les deux prélèvements sont exprimés par rapport aux {v} L de départ, et non au contenu restant après le matin.')],'Oui : la quantité initiale du réservoir.'),
                Q('Écrire la fraction de l’après-midi avec le même dénominateur que celle du matin.','Multiplier numérateur et dénominateur par le même entier.', [('Transformer sans changer la valeur',M(rf'\frac{{1}}{{{z//2}}}=\frac{{1\times2}}{{{z//2}\times2}}=\frac{{2}}{{{z}}}'))],rf'$\frac{{2}}{{{z}}}$.'),
                Q('Quelle fraction de la quantité initiale a été utilisée en tout ?','Additionner des fractions exprimées avec la même unité fractionnaire.', [('Additionner les numérateurs',M(rf'\frac{{{a}}}{{{z}}}+\frac{{2}}{{{z}}}=\frac{{{a+2}}}{{{z}}}'))],rf'${frac(used)}$ de la quantité initiale.'),
                Q('Quelle fraction de la quantité initiale reste-t-il ?','Écrire le tout avec le même dénominateur avant de soustraire.', [('Retirer la fraction utilisée',M(rf'1-\frac{{{a+2}}}{{{z}}}=\frac{{{z}}}{{{z}}}-\frac{{{a+2}}}{{{z}}}=\frac{{{z-a-2}}}{{{z}}}'))],rf'${frac(left)}$ de la quantité initiale.'),
                Q('Calculer les volumes utilisés et restants en litres.','Appliquer chaque fraction à la quantité initiale.', [('Trouver le volume d’une part',M(rf'{v}\div{z}={dec(F(v,z))}')),('Compter les parts',chain(rf'V_{{\mathrm{{utilisé}}}}&={dec(F(v,z))}\times{a+2}={dec(v*used)}',rf'V_{{\mathrm{{restant}}}}&={v}-{dec(v*used)}={dec(v*left)}'))],rf'${dec(v*used)}$ L utilisés et ${dec(v*left)}$ L restants.'),
                Q('À quel moment prélève-t-on le plus ? Quel est l’écart en litres ?','Comparer des fractions de la même quantité avec le même dénominateur.', [('Comparer les nombres de parts',f'Le matin utilise {a} parts ; l’après-midi en utilise 2.'),('Calculer l’écart',M(rf'{abs(a-2)}\times{dec(F(v,z))}={dec(v*F(abs(a-2),z))}'))],('Même volume aux deux moments.' if a==2 else ('Le matin' if a>2 else 'L’après-midi')+rf' prélève ${dec(v*F(abs(a-2),z))}$ L de plus.'))]
            note='Additionner les numérateurs n’est possible qu’après avoir obtenu le même dénominateur. Le dénominateur commun reste inchangé.'
        elif n==285:
            v=int(re.search(r'(\d+) (?:personnes|élèves)',intro)[1]); p=int(re.search(r'(\d+)\s*%',intro)[1]); part=F(v*p,100)
            C(part+(v-part),v);C(2*part,F(2*v*p,100))
            qs=[
                Q('Que représente ici 100 % ?','Chercher l’effectif total auquel le pourcentage se rapporte.', [('Identifier la population de référence',f'L’enquête porte sur {v} personnes ; elles constituent le groupe entier.')],f'Les {v} personnes interrogées.'),
                Q('Écrire le pourcentage sous forme de fraction sur 100.','Traduire le mot pour cent.', [('Remplacer le symbole par une fraction',M(rf'{p}\,\%=\frac{{{p}}}{{100}}'))],rf'$\frac{{{p}}}{{100}}$.'),
                Q('Donner l’écriture décimale correspondante.','Diviser le nombre de pour cent par 100.', [('Passer de centièmes à l’écriture décimale',M(rf'{p}\div100={dec(F(p,100))}'))],rf'${dec(F(p,100))}$.'),
                Q('Combien de personnes ont donné cette réponse ?','Multiplier l’effectif total par la proportion.', [('Appliquer la proportion au groupe',M(rf'{v}\times\frac{{{p}}}{{100}}={dec(part)}'))],rf'${dec(part)}$ personnes.'),
                Q('Quel pourcentage et combien de personnes n’ont pas donné cette réponse ?','Retirer la partie étudiée au groupe entier.', [('Calculer le pourcentage complémentaire',M(rf'100-{p}={100-p}')),('Calculer l’effectif complémentaire',M(rf'{v}-{dec(part)}={dec(v-part)}'))],rf'${100-p}\,\%$, soit ${dec(v-part)}$ personnes.'),
                Q('On double l’effectif total avec le même pourcentage. Combien donnent alors cette réponse ?','Garder la même proportion mais changer le tout de référence.', [('Doubler l’effectif',M(rf'2\times{v}={2*v}')),('Appliquer le pourcentage',M(rf'{2*v}\times\frac{{{p}}}{{100}}={dec(2*part)}'))],rf'${dec(2*part)}$ personnes.')]
            note='Un pourcentage ne donne pas un effectif à lui seul : il faut toujours connaître le tout de référence.'
        elif n==135:
            circle=re.search(r'rayon de (\d+)\s*m',intro)
            if circle:
                r=int(circle[1]);di=2*r;per=F(314,100)*di
                C(per,di*F(314,100));C(100*per,di*314)
                qs=[
                    Q('Décrire un rayon du cercle.','Relier le centre à un point du cercle.', [('Distinguer rayon et diamètre',f'Un rayon ne traverse que la moitié du disque : sa longueur est {r} m.')],f'Un segment reliant le centre à un point du cercle, de longueur {r} m.'),
                    Q('Calculer le diamètre.','Un diamètre contient deux rayons.', [('Additionner les deux rayons',M(rf'2\times{r}={di}'))],f'{di} m.'),
                    Q('Écrire le périmètre exact avec le nombre π.','Multiplier le diamètre par π.', [('Choisir la formule du contour',M(rf'P=\pi\times{di}={di}\pi'))],rf'${di}\pi$ m.'),
                    Q('Avec π approché par 3,14, estimer ce périmètre.','Remplacer π dans le produit ; conserver le signe approché.', [('Calculer avec la valeur approchée',M(rf'P\approx{di}\times3{{,}}14={dec(per)}'))],rf'Environ ${dec(per)}$ m.'),
                    Q('Exprimer cette approximation en centimètres.','Un mètre contient 100 centimètres.', [('Convertir la longueur approchée',M(rf'{dec(per)}\times100={dec(100*per)}'))],rf'Environ ${dec(100*per)}$ cm.'),
                    Q('Si le diamètre double, que devient le périmètre ?','Dans le produit π fois diamètre, seul le diamètre est doublé.', [('Calculer le nouveau contour',M(rf'\pi\times{2*di}=2\times({di}\pi)')),('Estimer',M(rf'2\times{dec(per)}={dec(2*per)}'))],rf'Il double : ${2*di}\pi$ m, soit environ ${dec(2*per)}$ m.')]
                note='Le nombre π reste dans la valeur exacte. Remplacer π par 3,14 donne une approximation, jamais une égalité exacte avec le périmètre.'
            else:
                a,z=map(int,re.search(r'(\d+) m de long.*?(\d+) m de large',intro).groups());p=2*(a+z);wire=p-1;roll=(wire+4)//5
                C(roll*5-wire,5*roll-(p-1))
                qs=[
                    Q('Exprimer les deux dimensions en centimètres.','Multiplier chaque longueur en mètres par 100.', [('Convertir séparément',chain(rf'{a}\times100&={100*a}',rf'{z}\times100&={100*z}'))],f'{100*a} cm et {100*z} cm.'),
                    Q('Quelle grandeur faut-il calculer pour entourer le potager ?','Distinguer le bord et la surface intérieure.', [('Repérer le trajet du grillage','Le grillage suit le contour du potager, sans recouvrir l’intérieur.')],'Le périmètre.'),
                    Q('Calculer le périmètre.','Additionner les quatre côtés du rectangle.', [('Regrouper les côtés égaux',M(rf'P=2\times({a}+{z})=2\times{a+z}={p}'))],f'{p} m.'),
                    Q('Quelle longueur de grillage faut-il avec l’ouverture de 1 m ?','Retirer du contour la partie qui reste libre.', [('Soustraire l’ouverture',M(rf'{p}-1={wire}'))],f'{wire} m.'),
                    Q('Le grillage est vendu en rouleaux de 5 m. Combien de rouleaux entiers acheter ?','Chercher le premier multiple de 5 qui couvre toute la longueur.', [('Encadrer la longueur nécessaire',M(rf'{5*(roll-1)}<{wire}\le{5*roll}')),('Choisir le nombre entier suffisant',f'{roll-1} rouleaux ne suffisent pas ; {roll} rouleaux fournissent {5*roll} m.')],f'{roll} rouleaux.'),
                    Q('Quelle longueur de grillage restera inutilisée ?','Soustraire la longueur posée à la longueur achetée.', [('Calculer le reste',M(rf'{5*roll}-{wire}={5*roll-wire}'))],f'{5*roll-wire} m.')]
                note='Un achat par rouleaux impose un nombre entier : on arrondit par excès pour avoir assez de matériau.'
        elif n==134:
            recipe=re.search(r'(\d+) personnes.*?(\d+) g',intro)
            scale=re.search(r'1\s*[/:]\s*(\d+)',intro)
            if recipe:
                a,z=map(int,recipe.groups());unit=F(z,a);people=int(400//unit)
                C(unit*a,z);C(unit*6,F(6*z,a));C(400-people*unit,F(400)-people*unit)
                qs=[
                    Q('Quelle masse de farine correspond à une personne ?','Revenir à l’unité en partageant la masse de la recette.', [('Partager en parts égales',M(rf'{z}\div{a}={dec(unit)}'))],rf'${dec(unit)}$ g par personne.'),
                    Q('Quelle masse faut-il pour six personnes ?','Multiplier la masse par personne par le nouvel effectif.', [('Calculer six parts',M(rf'{dec(unit)}\times6={dec(6*unit)}'))],rf'${dec(6*unit)}$ g.'),
                    Q('Quelle masse de farine par personne faut-il garder pour cette recette ?','Repérer ce qui reste constant quand on change les quantités.', [('Contrôler la recette initiale',M(rf'{a}\times{dec(unit)}={z}'))],rf'${dec(unit)}$ g par personne.'),
                    Q('Avec 400 g, combien de personnes au maximum peut-on servir entièrement ?','Comparer deux effectifs entiers consécutifs.', [('Tester l’effectif possible et le suivant',chain(rf'{people}\times{dec(unit)}&={dec(people*unit)}\le400',rf'{people+1}\times{dec(unit)}&={dec((people+1)*unit)}>400'))],f'{people} personnes au maximum.'),
                    Q('Si l’on double le nombre de personnes, quelle masse faut-il ?','Doubler une grandeur impose de doubler l’autre dans cette recette.', [('Doubler les deux quantités',chain(rf'2\times{a}&={2*a}',rf'2\times{z}&={2*z}'))],f'{2*z} g pour {2*a} personnes.'),
                    Q(rf'Une autre recette utilise 100 g fixes, puis ${dec(unit)}$ g par personne. Est-elle proportionnelle au nombre de personnes ?','Tester le doublement en tenant compte de la quantité fixe.', [('Calculer pour une puis deux personnes',chain(rf'100+{dec(unit)}&={dec(100+unit)}',rf'100+2\times{dec(unit)}&={dec(100+2*unit)}')),('Comparer au double',rf'Le double de ${dec(100+unit)}$ est ${dec(200+2*unit)}$, différent de ${dec(100+2*unit)}$.')],'Non : la masse fixe de 100 g empêche le doublement.')]
                note='Revenir à une personne est une méthode de proportionnalité. Quand on sert des personnes entières, une division non entière exige une décision adaptée au contexte.'
            elif scale:
                e=int(scale[1]); a=int(re.search(r'(\d+) cm.*?(?:long|longueur)',intro)[1]) if re.search(r'(\d+) cm.*?(?:long|longueur)',intro) else int(re.findall(r'(\d+) cm',intro)[0]);z=2
                C(F(e*a,100),F(e,100)*a)
                qs=[
                    Q('Quelle longueur réelle représente 1 cm sur ce plan ?','Lire l’échelle avec la même unité des deux côtés.', [('Interpréter le rapport',f'1 cm sur le plan représente {e} cm dans la réalité.'),('Convertir en mètres',M(rf'{e}\div100={dec(F(e,100))}'))],rf'{e} cm, soit ${dec(F(e,100))}$ m.'),
                    Q(f'Quelle longueur réelle représente {a} cm sur le plan, en centimètres ?','Multiplier la longueur du plan par le nombre de centimètres réels correspondant à 1 cm.', [('Changer d’échelle',M(rf'{a}\times{e}={a*e}'))],f'{a*e} cm.'),
                    Q('Exprimer cette longueur réelle en mètres.','Convertir les centimètres réels obtenus.', [('Diviser par 100',M(rf'{a*e}\div100={dec(F(a*e,100))}'))],rf'${dec(F(a*e,100))}$ m.'),
                    Q('Quelle longueur réelle représente une largeur de 2 cm sur le plan ?','Appliquer le même agrandissement à toutes les longueurs.', [('Calculer puis convertir',chain(rf'2\times{e}&={2*e}\ \mathrm{{cm}}',rf'{2*e}\div100&={dec(F(2*e,100))}\ \mathrm{{m}}'))],rf'${dec(F(2*e,100))}$ m.'),
                    Q('Un segment représente 5 m dans la réalité. Quelle est sa longueur exacte sur le plan en centimètres ?','Revenir à une seule longueur de plan après avoir unifié les unités.', [('Convertir la longueur réelle',r'$5\ \mathrm{m}=500\ \mathrm{cm}$.'),('Diviser par la longueur réelle d’un centimètre du plan',M(rf'500\div{e}={frac(500,e)}'))],rf'${frac(500,e)}$ cm.'),
                    Q('On photocopie le plan en doublant toutes ses longueurs. Que représente désormais 1 cm de copie ?','Une même distance réelle occupe maintenant deux fois plus de place.', [('Suivre une longueur témoin',f'Les {e} cm réels occupent maintenant 2 cm de copie.'),('Revenir à un centimètre de copie',M(rf'{e}\div2={e//2}'))],f'{e//2} cm réels : nouvelle échelle 1/{e//2}.')]
                note='L’échelle compare des longueurs exprimées dans la même unité. Avant tout calcul, distinguer longueur sur le plan et longueur réelle.'
            else:
                nums=re.findall(r'(\d+)',intro);price=int(nums[0]);p=int(nums[1]);discount=F(price*p,100)
                C(price-discount,price*(1-F(p,100)))
                qs=[
                    Q('Quelle somme représente 100 % du prix ?','Identifier le prix avant la remise.', [('Fixer le tout de référence',f'Le prix initial est {price} € ; la remise est une partie de ce prix.')],f'{price} €.'),
                    Q('Écrire le pourcentage de remise sous forme de fraction.','Lire pour cent comme sur cent.', [('Traduire le symbole',M(rf'{p}\,\%=\frac{{{p}}}{{100}}'))],rf'$\frac{{{p}}}{{100}}$.'),
                    Q('Calculer le montant de la remise.','Appliquer la fraction au prix initial.', [('Calculer la partie retirée',M(rf'{price}\times\frac{{{p}}}{{100}}={dec(discount)}'))],rf'${dec(discount)}$ €.'),
                    Q('Calculer le prix après remise.','Retirer le montant économisé une seule fois.', [('Soustraire la remise',M(rf'{price}-{dec(discount)}={dec(price-discount)}'))],rf'${dec(price-discount)}$ €.'),
                    Q('Quel pourcentage du prix reste-t-il à payer ?','Compléter le pourcentage de remise jusqu’à 100.', [('Calculer le complément',M(rf'100-{p}={100-p}'))],f'{100-p} %.'),
                    Q('Le prix remisé est-il proportionnel au prix initial si le taux de remise reste identique ?','La même fraction du prix est conservée pour tous les achats.', [('Identifier la part conservée',rf'Pour chaque prix, on paie $\frac{{{100-p}}}{{100}}$ de ce prix. Doubler le prix initial double donc le prix payé.')],'Oui, si le même pourcentage s’applique à chaque prix.')]
                note='Le pourcentage de remise s’applique au prix initial ; le montant retiré en euros n’est pas le nombre de pour cent.'
        add(n,eid,title,diff,intro,qs,note)

def render(ex):
    out=[f"=== {ex['titre']}",f"Id: {ex['id']}",f"Difficulté: {ex['difficulte']}",'','Énoncé:',MARK,ex['introduction'],'']
    out += [f"{i}. {q['question']}" for i,q in enumerate(ex['questions'],1)]
    out += ['','Étapes:',MARK]
    for i,q in enumerate(ex['questions'],1):
        out += [f"## Question {i} : {q['question']}",'','::: methode',q['methode'],':::','']
        for title,body in q['etapes']: out += [f'::: etape {title}',body,':::','']
        out += ['::: resultat',q['reponse'],':::','']
    out += ['::: retenir',ex['note'],':::','','Solution:',MARK]+[f"{i}. {q['reponse']}" for i,q in enumerate(ex['questions'],1)]
    return '\n'.join(out)+'\n\n===\n'

if __name__=='__main__':
    # Données diversifiées et cours ajoutés par les modules voisins, sans reconversion.
    import runpy
    ctx=globals()
    for module in ('exercices_diversifies_20261030.py','documents_20261030.py'):
        runpy.run_path(str(Path(__file__).parent/module),init_globals=ctx)
    for n,d in DIRS.items():
        (d/'exercices.txt').write_text('\n'.join(render(ex) for ex in RECORDS[n]),encoding='utf-8')
        (d/'revision_20261030.json').write_text(json.dumps(RECORDS[n],ensure_ascii=False,indent=2),encoding='utf-8')
    (Path(__file__).parent/'calculs_exacts_20261030.json').write_text(json.dumps(CHECKS,indent=2),encoding='utf-8')
    print('Révision produite :', {n:len(x) for n,x in RECORDS.items()},len(CHECKS),'contrôles exacts préparatoires.')
