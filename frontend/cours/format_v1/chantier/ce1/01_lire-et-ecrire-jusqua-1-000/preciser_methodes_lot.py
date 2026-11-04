"""Retouches ciblées de la clôture : méthodes liées à chaque situation."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent

def changer(code,methods,extras=None):
    d=next(ROOT.glob(f'{code:02}_*'));p=d/'exercices.txt'
    blocks=re.split(r'^===\s*$',p.read_text(encoding='utf-8'),flags=re.M)[1:]
    for i,items in methods.items():
        block=blocks[i-1]
        matches=list(re.finditer(r'::: methode\n(.*?)\n:::',block,re.S))
        assert len(matches)==5
        for j,new in sorted(items.items(),reverse=True):
            m=matches[j-1];block=block[:m.start(1)]+new+block[m.end(1):]
        blocks[i-1]=block
    for i,old,new in extras or []:
        assert old in blocks[i-1],(code,i,old)
        blocks[i-1]=blocks[i-1].replace(old,new)
    p.write_text('===\n'+('\n===\n'.join(b.strip()+'\n' for b in blocks)),encoding='utf-8')

changer(4,{
 5:{1:'Compare les écarts 135 − 125 et 145 − 135, puis ajoute encore dix à chaque rang.',2:'Pars de 125 et ajoute dix trois fois pour écrire quatre nombres.',3:'Ajoute dix à 165, comme entre les nombres précédents.',5:'Compare la réponse du camarade à 165 augmenté de dix.'},
 6:{1:'Vérifie que chaque nombre est le double du précédent ; double encore 16 puis le nombre obtenu.',2:'Pars de 2 et double trois fois pour écrire quatre nombres.',3:'Double 64 pour poursuivre la suite.',5:'Compare la réponse du camarade au double de 64.'},
 7:{1:'Pars du rang 1, qui porte 1, et ajoute deux pour chaque rang suivant jusqu’au rang 12.',2:'Pars de 1 et ajoute deux trois fois pour écrire quatre nombres.',3:'Ajoute deux à 23, comme entre deux nombres impairs voisins.',5:'Compare la réponse du camarade à 23 augmenté de deux.'},
 8:{1:'Calcule les écarts successifs : ils augmentent de un. Après le pas de quatre, utilise cinq puis six.',2:'Pars de 1 et utilise successivement les pas de un, deux et trois.',3:'Le dernier pas était six : ajoute maintenant sept à 22.',5:'Compare la réponse du camarade à 22 augmenté du prochain pas, qui vaut sept.'},
})

calc15={
1:('Lina','Noé','Ajoute d’abord vingt à 125, puis les huit cartes restantes.'),
2:('l’école de 196 élèves','l’école de 238 élèves','Compte de 196 à 200, puis de 200 à 238, et réunis les deux compléments.'),
3:('le bac bleu','le bac rouge','Ajoute quarante à 175, puis les six cubes restants.'),
4:('Zoé','Mila','Retire quatre-vingts à 304 puis rajoute deux, car il fallait retirer seulement 78.'),
5:('la ficelle de 95 cm','la ficelle de 140 cm','Compte de 95 à 100 puis de 100 à 140 ; réunis les deux écarts.'),
6:('Lina','Sami','Retirer 125 de 125 enlève toute la collection : il ne reste aucune différence.'),
7:('le jeu à 38 €','l’autre jeu','Complète 38 jusqu’à quarante, puis ajoute les dix euros restants.'),
8:('Noé','Lina','Retire dix à 63 puis rajoute une bille, car il fallait retirer neuf.'),
9:('B','A','Compte de 185 à 200 puis de 200 à 240 ; réunis les deux écarts.'),
}
methods15={}
for i,(small,big,calculation) in calc15.items():
    methods15[i]={3:calculation}
    if i!=6:
        methods15[i][1]=f'Compare les données de {small} et de {big} pour identifier la quantité la plus grande.'
        methods15[i][5]=f'Ajoute cinq à la quantité de {small}, puis calcule son nouvel écart avec celle de {big}.'
changer(15,methods15)

data16={
1:['Cherche le nombre de livres après l’arrivée des 38 livres, avant les prêts.','Ajoute les 38 livres apportés aux 125 livres présents.','Retire les 47 livres prêtés du nombre obtenu après l’apport.','Retire quarante à 163 puis encore sept ; compte les livres qui restent.','Rajoute les 47 livres prêtés aux livres restants pour retrouver le nombre avant le prêt.'],
2:['Cherche combien de perles sont rouges ou bleues avant de compter les vertes.','Réunis les 86 perles rouges et les 74 perles bleues.','Retire les perles rouges et bleues du total de 245 perles.','Retire cent à 245 puis encore soixante ; les perles restantes sont vertes.','Réunis les perles vertes et les 160 autres perles : tu dois retrouver les 245 perles.'],
3:['Cherche combien de voyageurs restent après la descente, avant la montée.','Retire les 18 voyageurs qui descendent des 43 voyageurs du bus.','Ajoute les 27 voyageurs qui montent aux 25 voyageurs restants.','Ajoute vingt à 25 puis encore sept ; compte les voyageurs présents.','Retire les 27 nouveaux voyageurs du total final pour retrouver les 25 voyageurs déjà présents.'],
4:['Cherche d’abord le prix des six crayons, avant d’ajouter le cahier.','Répète six fois le prix de deux euros pour trouver le prix des crayons.','Ajoute le prix du cahier aux douze euros des crayons.','Ajoute cinq aux douze euros des crayons ; indique le prix total en euros.','Retire le prix du cahier du total payé pour retrouver le prix des six crayons.'],
5:['Cherche d’abord le prix des sept jeux, avant de calculer la monnaie.','Répète sept fois le prix de quatre euros pour trouver le prix des jeux.','Retire le prix des sept jeux des cinquante euros donnés.','Compte de 28 à trente puis de trente à cinquante ; réunis les deux compléments.','Réunis la monnaie rendue et le prix des jeux : tu dois retrouver les cinquante euros donnés.'],
6:['Cherche le prix du cahier et de la pochette pour un seul enfant.','Réunis les trois euros du cahier et les deux euros de la pochette.','Répète huit fois le coût de cinq euros pour un enfant.','Compte huit groupes de cinq euros pour obtenir le coût total.','Compte de cinq en cinq pour vérifier le coût des huit enfants.'],
7:['Cherche combien de balles contiennent les cinq sacs, avant les balles isolées.','Répète cinq fois les six balles contenues dans un sac.','Ajoute les neuf balles isolées aux trente balles dans les sacs.','Ajoute neuf aux trente balles des sacs pour compter toutes les balles.','Retire les neuf balles isolées du total pour retrouver les trente balles des sacs.'],
8:['Cherche le total des places réservées le matin et l’après-midi.','Réunis les 135 réservations du matin et les 78 de l’après-midi.','Retire les 213 places réservées des 260 places disponibles.','Retire deux cents à 260, puis dix et trois ; compte les places libres.','Réunis les places libres et les 213 réservations pour retrouver les 260 places.'],
9:['Cherche le prix des quatre livres : le nombre de livres ne donne pas leur prix.','Répète quatre fois les cinq euros du prix d’un livre.','Retire le prix des quatre livres des trente euros reçus.','Retire vingt aux trente euros reçus ; indique la somme restante en euros.','Réunis l’argent restant et le prix des quatre livres pour retrouver les trente euros reçus.'],
}
changer(16,{i:dict(enumerate(ms,1)) for i,ms in data16.items()},[(7,'Un seul objet ne suffit pas : il faut le prix de tous les objets achetés.','Un seul sac ne suffit pas : il faut compter les balles des cinq sacs.')])

changer(18,{2:{1:'Plie la bande en superposant ses deux extrémités, marque le milieu et colorie une des deux moitiés.'}},[(2,'Le tout contient 2 parts de même taille. Une seule est prise : on écrit 1 au-dessus de la barre et 2 au-dessous.','En superposant les deux extrémités de la bande, on marque un pli au milieu. Les deux morceaux se superposent : ils sont égaux. On colorie un seul morceau sur les deux et on écrit 1 au-dessus de la barre et 2 au-dessous.')])
print('Méthodes précisées : CE1 04, 15, 16 et 18.')
