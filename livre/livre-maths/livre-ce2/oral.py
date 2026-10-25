from mise_en_page import *

def grands_nombres(s):
    return re.sub(r'\b\d{4,}\b',lambda m:f'{int(m.group()):,}'.replace(',',' '),str(s))

def oraux(b):
    b.begin('oral-intro','360 problèmes à raconter','BANQUE ORALE POUR L’ADULTE',adult=True);b.outline('Banque de problèmes oraux','oral-intro')
    b.box('36 SEMAINES · 10 HISTOIRES PAR SEMAINE','Lire sans révéler la réponse ni l’opération. Faire représenter et expliquer. Les réponses de ces pages sont réservées à l’adulte.',83,40,size=13.4)
    t=137
    for title,body in [
    ('Choisir selon les apprentissages','Les semaines sont des propositions. Les situations ne suivent pas obligatoirement l’ordre des chapitres. Garder une structure déjà enseignée ou la préparer avec de petits nombres.'),
    ('Faire varier les structures','Chaque semaine propose des problèmes additifs, une comparaison, deux étapes, un produit, un partage ou groupement, une situation de prix, une mesure, une comparaison multiplicative et des choix organisés.'),
    ('Adapter le champ numérique','Les nombres supérieurs à 1 000 sont présents dès le début ; le champ additif va jusqu’à 10 000 à partir de la semaine 8. Les produits à deux chiffres se proposent après leur apprentissage. Les histoires à trois étapes restent sous 100.'),
    ('Compléter cette banque','Les fractions, les constructions, les enquêtes et les tâches de mesure figurent dans les chapitres. Ajouter des situations vécues en classe et laisser l’enfant inventer ses propres problèmes.')]:
        b.text(title,20,t,170,12.5,bold=True,color=GREEN);t=b.text(body,20,t+8,170,11.5,leading=15.3)+10
    for week in problemes_oraux():
        n=week['numero'];b.begin(f'oral-{n}',f'Semaine {n:02} · Dix petites histoires','PROBLÈMES ORAUX',subtitle=f'Champ additif jusqu’à {week["plafond"]:,} · Lire à l’enfant.'.replace(',',' '),adult=True);t=81
        for i,p in enumerate(week['problemes'],1):
            b.text(str(i),18,t,9,10.7,bold=True,color=GREEN);end=b.text(grands_nombres(p['enonce']),29,t,162,10.5,leading=13.3)
            end=b.text(grands_nombres('Réponse : '+str(p['reponse'])+' · '+p['calcul']),29,end+1.2,162,9.1,leading=11.4,color=MUTED)
            b.line(29,end+2,191);t=end+5.1
