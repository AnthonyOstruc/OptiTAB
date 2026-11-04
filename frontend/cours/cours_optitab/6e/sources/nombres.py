"""Situations de Sixième : numération, calcul exact et fractions."""
from fractions import Fraction as F
from modele_6e import ex,q,n,m


def numeration(i,l):
    if i%2:
        entier=12+3*i+l
        dixieme=2+l
        centieme=3+i%5
        valeur=entier+F(dixieme,10)+F(centieme,100)
        return ex('Lire une mesure décimale',f'Une balance affiche {m(n(valeur))} kg. On veut décrire cette mesure en utilisant les unités, les dixièmes et les centièmes de kilogramme.',[
            q('Quelle est la partie entière de cette mesure ?', 'La partie entière compte les kilogrammes entiers ; elle se lit à gauche de la virgule.', f'{entier} kg.'),
            q('Quel est le chiffre des dixièmes ? Quelle est sa valeur dans la mesure ?', 'Le premier chiffre après la virgule compte des dixièmes ; préciser sa valeur évite de confondre chiffre et quantité.', f'Le chiffre est {dixieme} ; sa valeur est '+m(n(F(dixieme,10)))+' kg.'),
            q('Quel est le chiffre des centièmes ? Quelle est sa valeur ?', 'Le deuxième chiffre après la virgule compte des centièmes ; cent centièmes forment une unité.', f'Le chiffre est {centieme} ; sa valeur est '+m(n(F(centieme,100)))+' kg.'),
            q('Décomposer la mesure en kilogrammes entiers, dixièmes et centièmes.', 'Additionner les contributions de chaque rang sans déplacer la virgule.', m(f'{n(valeur)}={entier}+\\frac{{{dixieme}}}{{10}}+\\frac{{{centieme}}}{{100}}')+' kg.', controle=f'F("{valeur}") == {entier}+F({dixieme},10)+F({centieme},100)'),
            q('Écrire la mesure comme une fraction décimale de dénominateur 100.', 'Chaque kilogramme vaut 100 centièmes et chaque dixième vaut 10 centièmes ; compter tous les centièmes.', m(rf'\frac{{{int(valeur*100)}}}{{100}}')+' kg.'),
            q('Ajouter un zéro à droite du dernier chiffre après la virgule change-t-il la mesure ? Justifier.', 'Un zéro final ajoute un rang qui vaut zéro ; les valeurs des chiffres déjà présents restent les mêmes.', 'Non : '+m(n(valeur))+' et '+m(n(valeur)+'0')+' désignent le même nombre.')],
            'Le chiffre des centièmes et le nombre de centièmes sont différents : le second compte aussi les unités et les dixièmes.',
            dict(type='table',headers=['Unités','Dixièmes','Centièmes'],rows=[[entier,dixieme,centieme]]),True)
    milliards=1+l
    millions=234+11*i
    milliers=15+2*i
    unites=608+i
    valeur=milliards*10**9+millions*10**6+milliers*1000+unites
    return ex('Le compteur de la médiathèque numérique',f'Un compteur affiche {valeur:,} documents consultés, toutes années confondues. Les espaces séparent les classes de trois chiffres.'.replace(',',' '),[
        q('Décomposer le compteur en classes : milliards, millions, milliers et unités.', 'Regrouper les chiffres par trois depuis la droite. Une classe contenant des zéros garde sa place.', f'{milliards} milliard(s), {millions} millions, {milliers} milliers et {unites} unités.'),
        q('Quelle est la valeur de la classe des millions ?', 'La classe des millions doit être multipliée par un million ; son écriture seule ne donne pas sa valeur dans le nombre.', f'{millions*10**6:,} documents.'.replace(',',' ')),
        q('Quel est le chiffre des millions ?', 'Le chiffre des millions est le dernier chiffre de la classe des millions ; il occupe un seul rang.', f'{millions%10}.'),
        q('Quel est le nombre de millions entiers du compteur ?', 'Lire toute la partie située à gauche du rang des millions, ce rang compris. Le milliard compte aussi des millions.', f'{valeur//10**6} millions entiers.', controle=f'{valeur}//1000000 == {valeur//10**6}'),
        q('Écrire une décomposition additive qui permet de retrouver le compteur.', 'Multiplier chaque classe par sa valeur d’unité, puis additionner. Les classes ne doivent ni se chevaucher ni être oubliées.', m(f'{milliards}\\times1\\,000\\,000\\,000')+' + '+m(f'{millions}\\times1\\,000\\,000')+' + '+m(f'{milliers}\\times1\\,000')+' + '+m(str(unites))+'.'),
        q('Le compteur reçoit mille consultations supplémentaires. Quelle classe change ? Donner la nouvelle valeur.', 'Ajouter 1 000 modifie ici la classe des milliers, sans retenue vers les millions. Vérifier la décomposition.', f'{valeur+1000:,} ; la classe des milliers passe de {milliers} à {milliers+1}.'.replace(',',' '))],
        'Un chiffre est un symbole de 0 à 9 ; un nombre peut comporter plusieurs chiffres. Garder les classes de trois pour lire les grands nombres.',
        dict(type='table',headers=['Milliards','Millions','Milliers','Unités'],rows=[[milliards,f'{millions:03d}',f'{milliers:03d}',f'{unites:03d}']]))


def reperage(i,l):
    bas=3+i
    unites=100*bas
    cents=24+17*l+3*i
    if cents%10==0:cents+=1
    valeur=F(unites+cents,100)
    voisin=valeur+F(1+l,100)
    arrondi_entier=bas+(cents>=50)
    arrondi_dixieme=F((int(valeur*100)+5)//10,10)
    return ex('Comparer les temps de deux coureurs',f'Ana termine une course en {m(n(valeur))} s et Bilal en {m(n(voisin))} s. Les chronométrages sont donnés au centième. Le plus petit temps correspond au coureur le plus rapide.',[
        q('Qui a réalisé le meilleur temps ? Justifier.', 'Les parties entières sont identiques ; comparer ensuite les dixièmes et les centièmes de gauche à droite.', 'Ana, car '+m(n(valeur)+'<'+n(voisin))+'.'),
        q('Encadrer le temps d’Ana entre deux entiers consécutifs.', 'La partie entière donne l’entier juste avant le nombre ; ajouter 1 pour l’entier suivant.', m(f'{bas}<{n(valeur)}<{bas+1}')+'.'),
        q('Encadrer ce temps entre deux dixièmes consécutifs.', 'Conserver jusqu’au rang des dixièmes pour la borne inférieure puis ajouter un dixième pour la borne supérieure.', m(f'{n(F(int(valeur*10),10))}<{n(valeur)}<{n(F(int(valeur*10)+1,10))}')+'.'),
        q('Donner l’arrondi du temps d’Ana à l’unité.', 'Comparer la partie décimale à 0,5. L’arrondi est l’entier le plus proche ; à égalité, choisir le supérieur.', f'{arrondi_entier} s.', controle=f'abs(F("{valeur}")-{arrondi_entier}) <= F(1,2)'),
        q('Donner l’arrondi du temps d’Ana au dixième.', 'Observer le chiffre des centièmes : de 0 à 4, garder le dixième ; de 5 à 9, passer au dixième supérieur.', m(n(arrondi_dixieme))+' s.', controle=f'abs(F("{valeur}")-F("{arrondi_dixieme}")) <= F(1,20)'),
        q('Pourquoi faut-il garder les temps initiaux pour départager les coureurs ?', 'Un arrondi remplace plusieurs nombres voisins par la même valeur ; il peut masquer l’écart entre deux performances.', f'Les temps exacts diffèrent de {l+1} centième(s), même si un affichage arrondi les rend parfois identiques.')],
        'Comparer des décimaux en complétant si besoin avec des zéros. Un arrondi est une valeur approchée, pas une égalité exacte.',
        dict(type='decimal_line',value=float(valeur),other=float(voisin),lower=bas),True)


def calcul_decimal(i,l):
    from scenarios_communs import operations
    if i%2==0:return operations(i,l)
    masse=F(12+i,10)
    prix=F(25+5*l,10)
    fruit=masse*prix
    pain=F(12+l,10)
    total=fruit+2*pain
    billet=10+l*5
    return ex('Vérifier le ticket du marché',f'On achète {m(n(masse))} kg de pommes à {m(n(prix))} € le kilogramme et deux pains à {m(n(pain))} € chacun. On paie avec {billet} €.',[
        q('Quelle opération donne le prix des pommes ?', 'Le prix au kilogramme indique le coût d’un kilogramme ; multiplier par le nombre de kilogrammes achetés.', m(n(masse))+r' × '+m(n(prix))+'.'),
        q('Estimer le prix des pommes avant de poser le calcul.', 'Remplacer les nombres par des nombres proches faciles à multiplier ; l’estimation servira à contrôler la place de la virgule.', f'Un peu moins de 2 kg à environ {round(float(prix))} € le kg : quelques euros, pas quelques dizaines d’euros.'),
        q('Calculer le prix exact des pommes.', 'Multiplier les décimaux ou travailler avec leurs fractions décimales ; conserver la valeur exacte du produit.', m(n(fruit))+' €.', m(n(masse)+r'\times'+n(prix)+'='+n(fruit)), f'F("{masse}")*F("{prix}") == F("{fruit}")'),
        q('Calculer le prix des deux pains.', 'Deux objets au même prix coûtent deux fois le prix d’un objet.', m(n(2*pain))+' €.'),
        q('Calculer le total à payer.', 'Additionner les deux dépenses exprimées en euros. En calcul posé, aligner les unités et les virgules.', m(n(total))+' €.', m(n(fruit)+'+'+n(2*pain)+'='+n(total))),
        q('Quelle monnaie doit-on rendre ? Vérifier en revenant au billet.', 'Soustraire le total payé du billet. Ajouter ensuite achats et monnaie pour retrouver la somme remise.', m(n(billet-total))+' €.', m(n(total)+'+'+n(billet-total)+f'={billet}'), f'F("{total}")+F("{billet-total}") == {billet}')],
        'L’ordre de grandeur aide à placer la virgule. Garder les unités et contrôler une soustraction par une addition.',
        dict(type='table',headers=['Produit','Quantité','Prix unitaire'],rows=[['Pommes',str(float(masse))+' kg',str(float(prix))+' €/kg'],['Pain',2,str(float(pain))+' €']]),True)


def division(i,l):
    from scenarios_communs import divisibilite
    if i%2==0:return divisibilite(i,l)
    personnes=3+l
    part=F(25+5*i+2*l,10)
    total=personnes*part
    return ex('Partager une dépense équitablement',f'{personnes} amis se partagent également une dépense de {m(n(total))} €. Chacun doit payer la même somme, au centime près.',[
        q('Quelle division permet de calculer la part de chacun ?', 'La somme totale est partagée en autant de parts qu’il y a de personnes ; le diviseur est un entier non nul.', m(n(total)+f'\\div{personnes}')+'.'),
        q('Estimer la valeur d’une part.', 'Chercher un multiple proche du nombre de personnes pour prévoir la taille de la réponse.', f'Chaque part est comprise entre {int(part)} € et {int(part)+1} €.'),
        q('Calculer le montant exact d’une part.', 'Effectuer la division décimale par l’entier. On peut aussi convertir le total en centimes puis partager.', m(n(part))+' €.', controle=f'F("{total}")/{personnes} == F("{part}")'),
        q('Vérifier la division par une multiplication.', 'Le montant d’une part multiplié par le nombre de personnes doit redonner le total à partager.', m(n(part)+f'\\times{personnes}='+n(total))+' €.'),
        q('Un ami règle deux parts. Combien paie-t-il et combien reste-t-il à payer ?', 'Deux parts valent deux fois la part unitaire ; enlever ce paiement du total pour calculer le reste.', m(n(2*part))+' € payés ; '+m(n(total-2*part))+' € restants.'),
        q('Si une personne supplémentaire participe au partage initial, la part peut-elle augmenter ?', 'Le total reste fixe et se répartit entre davantage de personnes : chaque part devient plus petite, sans refaire nécessairement toute la division.', 'Non, la part diminue ; on partage le même total entre plus de personnes.')],
        'Le quotient décimal donne la valeur d’une part. Le contrôle inverse est dividende = diviseur × quotient.',
        dict(type='flow',labels=[str(float(total))+' €',f'{personnes} parts égales','Montant d’une part ?']),True)


def fraction_quotient(i,l):
    personnes=3+l+i%3
    tartes=2+i%4
    quotient=F(tartes,personnes)
    return ex('Partager des tartes sans en perdre',f'On partage équitablement {tartes} tartes identiques entre {personnes} personnes. Chaque tarte peut être découpée en autant de parts que nécessaire.',[
        q('Quelle division décrit la part d’une personne ?', 'Partager plusieurs unités entre plusieurs personnes demande de diviser le nombre d’unités par le nombre de personnes.', m(f'{tartes}\\div {personnes}')+'.'),
        q('Exprimer cette part comme une fraction de tarte.', 'La fraction est aussi un quotient : le numérateur est le nombre de tartes et le dénominateur le nombre de personnes.', m(rf'\frac{{{tartes}}}{{{personnes}}}')+' de tarte.'),
        q('Si chaque tarte est coupée en autant de morceaux que de personnes, combien de morceaux obtient-on ?', 'Chaque tarte produit le même nombre de morceaux ; multiplier par le nombre de tartes.', f'{tartes*personnes} morceaux de taille 1/{personnes} de tarte.'),
        q('Combien de ces morceaux reçoit chaque personne ?', 'Chaque personne prend un morceau de chaque tarte ; le nombre total de morceaux se partage équitablement.', f'{tartes} morceaux, soit '+m(n(quotient))+' de tarte.', controle=f'F({tartes}*{personnes},{personnes}) == {tartes}'),
        q('Une personne reçoit-elle moins d’une tarte, exactement une tarte ou plus d’une tarte ?', 'Comparer le nombre de tartes au nombre de personnes, donc le numérateur au dénominateur.', 'Moins d’une tarte.' if tartes<personnes else 'Exactement une tarte.' if tartes==personnes else 'Plus d’une tarte.'),
        q('Si on double à la fois le nombre de tartes et le nombre de personnes, la part change-t-elle ?', 'Multiplier les deux termes d’une fraction par le même entier non nul conserve la fraction.', 'Non : '+m(rf'\frac{{{2*tartes}}}{{{2*personnes}}}=\frac{{{tartes}}}{{{personnes}}}')+'.', controle=f'F({2*tartes},{2*personnes}) == F({tartes},{personnes})')],
        'Une fraction représente un nombre et peut être supérieure à 1. Le quotient est défini même si son écriture décimale n’est pas finie.',
        dict(type='fraction_units',denominator=personnes,numerator=tartes),True)


def calcul_fractions(i,l):
    from scenarios_communs import additions_fractions
    return additions_fractions(i,l)


BUILDERS={'numeration':numeration,'reperage':reperage,'calcul-decimal':calcul_decimal,
    'division':division,'fraction-quotient':fraction_quotient,'calcul-fractions':calcul_fractions}
