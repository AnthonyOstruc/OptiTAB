"""Matrice de couverture : repères éditoriaux du livre et matrice des attendus officiels.

La matrice officielle reprend, rubrique par rubrique, l’annexe du programme de Seconde générale
et technologique (arrêté du 26-2-2026, BO n° 14 du 2 avril 2026, NOR MENE2602914A, pages 333 à 345).
Chaque attendu est rattaché à des lieux du livre ; chaque lieu est contrôlé dans les sources :
  Cn:motif      cours du chapitre n contenant le motif
  En.i:motif    exercice i du chapitre n (énoncé ou corrigé) contenant le motif
  P:motif       démonstration de référence dont le titre contient le motif
  Dnn           défi d’approfondissement numéro nn
  A:label:motif atelier contenant le motif
  Q:code        question flash rattachée au repère d’automatisme « code »
Les contrôles vérifient la présence ; la pertinence de chaque renvoi a été relue.
"""
from pathlib import Path
import json
from modele import CHAPITRES
import contenu_01_02,contenu_03_04,contenu_05_06,contenu_07_08
import contenu_09_10,contenu_11_12,contenu_13_14,contenu_15_16
from approfondissements import DEFIS
from demonstrations import PREUVES
from ateliers import ATELIERS
from automatismes import SERIES,REPERES_AUTOMATISMES
from liminaires_contenu import EXEMPLES_PAR_REPERE
ROOT=Path(__file__).resolve().parent
PROGRAMME='https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602914A'
BO_PDF='https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2014%20du%202%20avril%202026-515432.pdf'

matrix=[]
for ch in CHAPITRES:
    assert len(ch.cours)==2 and len(ch.exercices)==15 and len(ch.reperes)==4
    for ex in ch.exercices:assert ex.enonce and ex.corrige and ex.methode and ex.controle
    assert [e.difficulte for e in ch.exercices]==[1]*5+[2]*5+[3]*5
    for i,topic in enumerate(ch.reperes):
        exemple=EXEMPLES_PAR_REPERE[ch.numero][i]
        assert 1<=exemple<=len(ch.exercices)
        matrix.append({'contenu':topic,'chapitre':ch.numero,'cours':f'ess-{ch.numero}',
                       'exercices':[f'exo-{ch.numero}-{exemple}'],
                       'titre_exemple':ch.exercices[exemple-1].titre})
    if ch.numero in [8,9,10]:assert all(e.figure for e in ch.exercices)
extensions=[
('Écriture décimale illimitée','D01'),('Périodicité des rationnels','D01'),
('Carré de trois termes','D02'),('Cube de deux termes','D02'),
('Inégalité entre moyennes','D03'),('Barycentres de deux et trois points','D04'),
('Coordonnées du milieu démontrées','Preuve 12'),('Concours des hauteurs','D06'),
('Aire avec deux côtés et un sinus','D07'),('Isobarycentre et médianes','D05'),
('Médiatrices et cercle circonscrit','D08'),('Lieu équidistant d’un point et d’un axe','D09'),
('Régions définies par inégalités','D10'),('Lien carré-racine','D11')]
assert len(matrix)==64 and len(extensions)==14
assert sum(len(p) for t,p in PREUVES)==13

# --- Matrice des attendus officiels -------------------------------------------------
V,AL,AR,NR,AG,VE,DR,FR,FV,ST,CR,PR='Vocabulaire ensembliste et logique','Algorithmique et programmation','Nombres et calculs · Arithmétique','Nombres et calculs · Nombres réels','Nombres et calculs · Algèbre','Géométrie · Vecteurs','Géométrie · Droites du plan','Fonctions · Représentations','Fonctions · Variations et extrémums','Statistiques · Information chiffrée et statistique descriptive','Statistiques · Croisement de deux variables qualitatives','Probabilités'
OFFICIEL=[
(V,'Notions','Élément, sous-ensemble, ensemble vide, appartenance, inclusion',['C16:sous-ensemble','E16.1:varnothing']),
(V,'Notions','Réunion, intersection, complémentaire (notations barre et E privé de A)',['C16:complémentaire de','E16.1:setminus A']),
(V,'Notions','Ensembles de nombres et intervalles',['C2:mathbb D','E2.3']),
(V,'Notions','Couple et produit cartésien',['C16:produit cartésien','E16.2:couples']),
(V,'Notions','Notation Card(A)',['C16:operatorname{Card}','E16.1:operatorname{Card}','C14:operatorname{Card}']),
(V,'En situation','Proposition mathématique, variables dans une proposition',['C16:Une proposition est']),
(V,'En situation','Connecteurs « et », « ou »',['C16:« Et » exige','E16.3']),
(V,'En situation','Négation de propositions simples',['C16:Nier','E16.3:négation']),
(V,'En situation','Contre-exemple',['E16.6:contre-exemple','E1.10:contre-exemple']),
(V,'En situation','Implication, équivalence logique',['C16:équivalence','E16.4']),
(V,'En situation','Réciproque, contraposée',['C16:contraposée','E16.9:contraposée','E1.13:contraposée']),
(V,'En situation','Quantifications universelle et existentielle en mots (symboles hors programme)',['C16:symboles de quantification','E16.5:il existe']),
(V,'En situation','Raisonnements par disjonction des cas et par l’absurde',['C16:Disjonction','E16.7:disjonction','E16.8:Supposons']),
(AL,'Contenus','Variables de type entier, booléen, flottant, chaîne',['C15:code{bool}','E15.2:booléen']),
(AL,'Contenus','Affectation notée par une flèche en langage naturel',['C15:leftarrow','E15.1:leftarrow']),
(AL,'Contenus','Séquence d’instructions, instruction conditionnelle',['C15:if','E15.4:if x < 0']),
(AL,'Contenus','Boucle bornée (for), boucle non bornée (while)',['C15:while','E15.5:for k','E15.6:while']),
(AL,'Capacités','Écrire une formule combinant des variables',['E15.9:m = (yb - ya)']),
(AL,'Capacités','Lire, comprendre, modifier ou compléter un programme',['E15.13:Corriger','E15.15:dichotomie']),
(AL,'Contenus','Fonctions à un ou plusieurs arguments ; appel',['C15:def','E15.3:f(4)','E15.8:def alignes']),
(AL,'Contenus','Fonction renvoyant un nombre aléatoire ; série obtenue par répétition des appels',['C15:randint','E15.11:def frequence']),
(AL,'Capacités','Lire une fonction renvoyant une moyenne, un écart type, sans listes',['E15.12:def resume']),
(AL,'Capacités','Écrire une fonction renvoyant le résultat d’une expérience aléatoire ou de répétitions indépendantes',['E15.10:def somme2']),
(AL,'Démarche','Passer du langage naturel à Python et inversement',['C15:Du langage naturel à Python','E15.1:langage naturel']),
(AR,'Contenus','Notations N et Z',['C1:mathbb Z','C2:mathbb N']),
(AR,'Contenus','Multiple, diviseur, pair, impair (a = kb)',['C1:il existe un entier $k$']),
(AR,'Capacités','Modéliser et résoudre des problèmes de multiples, diviseurs, parité',['E1.11','E1.12','E1.14']),
(AR,'Capacités','Fractions sous forme irréductible',['C1:irréductible','E1.4']),
(AR,'Démonstration','Somme de deux multiples de a',['P:Somme de deux multiples','E1.6']),
(AR,'Démonstration','Le carré d’un nombre impair est impair',['P:Carré d’un impair','C1:carré d']),
(AR,'Algorithme','Tester si a est multiple de b',['E1.8:def multiple']),
(AR,'Algorithme','Plus grand multiple de a inférieur ou égal à b',['C1:a * (b // a)','E1.9:1000 // 17']),
(NR,'Contenus','Ensemble R, droite numérique',['C2:mathbb R']),
(NR,'Contenus','Intervalles : représentation et notations',['C2:Le programme officiel écrit aussi','E2.4:Représenter']),
(NR,'Contenus','Valeur absolue, distance entre deux réels',['C2:valeur absolue','E2.5:valeur absolue']),
(NR,'Contenus','Inéquation |x − a| ≤ r et intervalle [a − r ; a + r]',['C2:|x-a|\\le r','E2.6']),
(NR,'Contenus','Ensemble D, encadrement décimal à 10^-n',['C2:mathbb D','E2.7','E2.14:amplitude']),
(NR,'Contenus','Ensemble Q, irrationnels (racine de 2, pi)',['C2:irrationnel','E2.1']),
(NR,'Capacités','Lire et placer une abscisse sur une droite graduée',['Q:G1','E2.4:droite']),
(NR,'Capacités','Arrondir avec un nombre de chiffres significatifs adapté',['E2.10:chiffres significatifs']),
(NR,'Démonstration','1/3 n’est pas décimal',['P:tiers n’est pas décimal']),
(NR,'Démonstration','Racine de 2 est irrationnel',['P:Irrationalité de la racine de 2']),
(NR,'Algorithme','Encadrement de racine de 2 par balayage',['E2.15:Balayer','E15.7:def encadrement']),
(NR,'Approfondissements','Développement décimal illimité ; périodicité des rationnels',['D01']),
(AG,'Contenus','Puissances entières relatives, racines carrées, racine de a² = |a|',['C3:sqrt{u^2}=|u|','E3.1','E3.2']),
(AG,'Contenus','Calcul sur des expressions fractionnaires',['C3:fractionnaire','E3.7','E3.8']),
(AG,'Contenus','Somme d’inégalités ; produit par un réel positif ou négatif',['C4:additionner deux inégalités','E4.3:renverse']),
(AG,'Contenus','Comparaison additive (différence) et multiplicative (rapport)',['C4:Comparer deux nombres','E3.10:quotient']),
(AG,'Contenus','Équations ax + b = 0 et inéquations ax + b > 0',['E4.1','E4.3']),
(AG,'Contenus','Équation produit nul',['C4:Un produit est nul','E4.5']),
(AG,'Contenus','Signe de A(x)B(x) et A(x)/B(x)',['C4:Produit ou quotient','E4.8','E4.9']),
(AG,'Contenus','Équation quotient A(x)/B(x) = k et ensemble de définition',['C4:Équation quotient','E4.6']),
(AG,'Capacités','Exprimer une variable en fonction des autres ; relation ax + by = c',['C3:Isoler une variable','E3.9:3x-2y=7']),
(AG,'Capacités','Choisir la forme adaptée d’une expression',['C3:Choisir la forme utile','E3.15']),
(AG,'Capacités','Comparer par différence ou rapport et interpréter en variation additive ou multiplicative',['E3.10:quotient','E11.14:pourcentage']),
(AG,'Capacités','Modéliser un problème par une inéquation',['E4.11','E4.12']),
(AG,'Capacités','Ensembles de solutions : ax = b, a + x = b, ax + b = cx + d, inéquations, x² = a',['C4:x^2=a','E4.2','E4.4']),
(AG,'Démonstration','Racine de ab = racine de a fois racine de b',['P:Racine d’un produit']),
(AG,'Algorithme','Première puissance supérieure ou inférieure à une valeur donnée',['E15.6:def seuilbas','E11.13']),
(AG,'Approfondissements','(a + b + c)², (a + b)³, inégalité des moyennes',['D02','D03']),
(VE,'Contenus','Égalité de deux vecteurs, notation, vecteur nul',['C8:vecteur nul','E8.4']),
(VE,'Contenus','Représentants d’un vecteur',['C8:représentants']),
(VE,'Contenus','Produit par un réel ; colinéarité',['C8:colinéaires','E8.3','E8.7']),
(VE,'Contenus','Combinaison de deux vecteurs non colinéaires',['C8:non colinéaires permettent','E8.13']),
(VE,'Contenus','Base orthonormée, coordonnées, norme ; relation u = x i + y j',['C8:base $(\\vec i,\\vec j)$','C8:a\\vec i+b\\vec j','E8.5']),
(VE,'Contenus','Coordonnées de AB en fonction de A et B',['C8:x_B-x_A','E8.1']),
(VE,'Contenus','Déterminant, critère de colinéarité, alignement, parallélisme',['C8:det(\\vec u,\\vec v)=ad-bc','E8.8','E8.14']),
(VE,'Contenus','Caractérisation vectorielle du milieu',['C8:milieu de $[AB]$','E9.2']),
(VE,'Autres disciplines','Vecteur déplacement, vecteur position',['C8:vecteur position','C8:vecteur déplacement']),
(VE,'Capacités','Représenter une somme à partir de représentants de même origine',['C8:même origine','E8.2']),
(VE,'Capacités','Représenter un vecteur de coordonnées données ; lire des coordonnées',['E8.1','E8.4']),
(VE,'Capacités','Coordonnées d’une somme, d’un produit par un réel',['E8.2','E8.10']),
(VE,'Capacités','Distance entre deux points ; coordonnées du milieu',['C9:AB=\\sqrt','E9.1','E9.2']),
(VE,'Capacités','Problèmes par méthodes vectorielles, repérées ou géométriques',['E9.11','E10.13']),
(VE,'Démonstration','Colinéarité : nullité du déterminant, proportionnalité des coordonnées',['P:Déterminant et colinéarité']),
(VE,'Approfondissements','Barycentres, milieu, hauteurs, aire ab sin C / 2, médianes, médiatrices',['D04','P:Coordonnées du milieu','D06','D07','D05','D08']),
(DR,'Contenus','Vecteur directeur d’une droite',['C10:directeur']),
(DR,'Contenus','Équation cartésienne, équation réduite',['C10:équation cartésienne','C10:y=mx+p']),
(DR,'Contenus','Pente (coefficient directeur)',['C10:pente']),
(DR,'Capacités','Équation à partir de deux points, d’un point et d’un directeur, d’un point et de la pente',['E10.7','E10.6','E10.5']),
(DR,'Capacités','Pente ou directeur à partir d’une équation ou d’un graphique',['E10.2','E10.4']),
(DR,'Capacités','Tracer une droite d’équation donnée',['E10.2:deux points']),
(DR,'Capacités','Trois points alignés ou non',['E10.13']),
(DR,'Capacités','Droites parallèles ou sécantes',['E10.8']),
(DR,'Capacités','Point d’intersection de deux droites sécantes',['E10.9']),
(DR,'Démonstration','Forme générale d’une équation de droite par le déterminant',['P:Forme cartésienne']),
(DR,'Algorithme','Alignement de trois points ; équation d’une droite par deux points',['E15.8:def alignes','E15.9:def droite']),
(DR,'Approfondissements','Points équidistants d’un point et de l’axe des abscisses ; régions définies par des inégalités',['D09','D10']),
(FR,'Contenus','Fonction définie sur un intervalle ou une réunion finie d’intervalles',['C5:D_f','E5.6:cup']),
(FR,'Contenus','Ensemble de définition',['C5:Déterminer le domaine','E5.5']),
(FR,'Contenus','Courbe représentative d’équation y = f(x)',['C5:mathcal C_f','E5.4']),
(FR,'Contenus','Signe d’une fonction affine et des fonctions de référence',['C6:Signe d’une fonction affine','C6:Repère utile','E7.1:tableau de signes']),
(FR,'Contenus','Tableau de signes d’un produit ou d’un quotient',['C4:Produit ou quotient','E4.8','E4.9']),
(FR,'Capacités','Exploiter l’équation d’une courbe : appartenance, coordonnées',['E5.4','Q:F2']),
(FR,'Capacités','Modéliser par des fonctions',['E5.11','E5.14']),
(FR,'Capacités','Fonctions valeur absolue, carré, inverse : définitions et courbes',['C6:x\\mapsto|x|','E6.3','E6.5','E6.7']),
(FR,'Capacités','Résoudre f(x) = k, f(x) < k : méthode graphique, algébrique ou logicielle',['E5.7','E5.10','E6.7']),
(FR,'Capacités','Résoudre f(x) = 0, f(x) > 0 par tableau de signes',['E4.9','E6.10']),
(FR,'Capacités','Résoudre f(x) = g(x), f(x) < g(x) graphiquement ou avec un outil numérique',['C5:f(x)=g(x)','E5.9']),
(FR,'Capacités','Affine, valeur absolue, carré, inverse, racine, cube : f(x) = k, f(x) < k',['E6.4','E6.5','E6.6','E6.7','E6.10']),
(FR,'Objectifs','Fonctions sur N (notation u(n)) ; variable t pour le temps',['C5:u(n)','E5.12','E5.11:C(t)']),
(FV,'Contenus','Croissance, décroissance, monotonie ; tableau de variations',['C7:croissante','E7.6']),
(FV,'Contenus','Maximum, minimum sur un intervalle',['C7:maximum','E7.2']),
(FV,'Contenus','Fonction affine : m taux d’accroissement, p ordonnée à l’origine',['C6:taux d’accroissement','C6:ordonnée à l’origine']),
(FV,'Contenus','Variations d’une fonction affine selon le signe de m',['C7:f(x)=mx+p','E7.1']),
(FV,'Capacités','Relier représentation graphique et tableau de variations',['E7.2','E7.6']),
(FV,'Capacités','Déterminer graphiquement les extrémums',['E7.2']),
(FV,'Capacités','Décrire des variations avec un logiciel, la calculatrice ou Python',['A:atelier-debut:def balayage','E15.15']),
(FV,'Capacités','Fonction affine : relier variations, signe et droite',['C6:La droite est au-dessus','E7.1:tableau de signes']),
(FV,'Capacités','Problèmes d’optimisation',['C7:optimum','E7.11','E7.12']),
(FV,'Capacités','Valeur absolue, carré : signe et variations',['C6:Valeur absolue','E7.3','E6.11']),
(FV,'Capacités','Comparer f(a) et f(b) pour une fonction de référence',['C6:Comparer des images','E6.2','E6.8']),
(FV,'Démonstration','Variations des fonctions affines',['P:Variations d’une fonction affine']),
(FV,'Démonstration','Position relative de y = x et y = x² pour x positif',['P:Position du carré']),
(FV,'Démonstration','Variations des fonctions carré et inverse',['P:La fonction carré','P:La fonction inverse']),
(FV,'Algorithme','Approximation d’un extremum par balayage ou dichotomie',['E7.10','E15.15:def encadremaximum']),
(FV,'Algorithme','Longueur approchée d’une portion de courbe',['E15.14:def longueur']),
(FV,'Approfondissement','Courbes de la racine carrée et du carré sur les positifs',['D11']),
(ST,'Contenus','Pourcentage de pourcentage',['C11:proportion de $A$ dans $E$','E11.6']),
(ST,'Contenus','Variation absolue, coefficient multiplicateur, taux d’évolution',['C11:variation absolue','E11.4']),
(ST,'Contenus','Évolutions successives, évolution réciproque',['C11:réciproque','E11.7','E11.8']),
(ST,'Contenus','Linéarité de la moyenne',['C12:Ajouter $b$','E12.7']),
(ST,'Contenus','Écart type',['C12:écart type','E12.5']),
(ST,'Contenus','Ajout ou suppression d’une valeur : effet sur moyenne et médiane',['E12.11:supprime','E12.13']),
(ST,'Contenus','Histogramme, polygone des fréquences cumulées',['C12:polygone des fréquences cumulées','E12.9','E12.10']),
(ST,'Contenus','Moyenne par classes (moyenne pondérée, centres)',['C12:centres','E12.9','E12.14']),
(ST,'Contenus','Classe médiane, estimation de la médiane',['C12:Médiane groupée','E12.10']),
(ST,'Capacités','Relation entre effectifs, proportions et pourcentages',['E11.1','E11.3']),
(ST,'Capacités','Pourcentages de pourcentages',['E11.6']),
(ST,'Capacités','Valeurs successives et taux ; taux global ; taux réciproque',['E11.5','E11.7','E11.12']),
(ST,'Capacités','Comparer deux séries par moyenne-écart type ou médiane-écart interquartile',['E12.6','E12.12']),
(CR,'Contenus','Tableau croisé d’effectifs',['C13:tableau croisé','E13.1']),
(CR,'Contenus','Fréquence conditionnelle, fréquence marginale',['C13:fréquence marginale','E13.2','E13.6']),
(CR,'Capacités','Compléter un tableau croisé par effectifs ou fréquences conditionnelles',['E13.4','E13.11']),
(CR,'Objectifs','Variables nominales et ordinales ; données réelles',['C13:ordinale','E13.5','E13.10:Insee']),
(CR,'Algorithme','Filtre ET, OU, NON à partir de deux listes',['A:atelier-filtres:groupe  = [','A:atelier-filtres:not reponse[i]']),
(CR,'Algorithme','Tableau croisé à partir du fichier des individus ; fréquences conditionnelles ou marginales',['A:atelier-filtres:def freq_cond','E13.8']),
(PR,'Contenus','Loi des grands nombres, version vulgarisée',['C14:loi des grands nombres','E14.14']),
(PR,'Contenus','Probabilité conditionnelle et notation P_A(B)',['C14:P_A(B)=']),
(PR,'Contenus','Arbres de probabilité',['C14:branches','E14.7','E14.8']),
(PR,'Capacités','Observer la loi des grands nombres par simulation',['E15.11:def frequence']),
(PR,'Capacités','Construire un arbre pondéré ou un tableau ; langue naturelle et registre symbolique',['E14.8','E14.10']),
(PR,'Capacités','Probabilités conditionnelles depuis un tableau croisé ou un arbre',['E14.5','E14.7']),
(PR,'Capacités','Interpréter les pondérations des branches',['C14:somment à 1','E14.8']),
(PR,'Capacités','Lien entre définition et multiplication le long d’un chemin',['C14:P(A\\cap B)=P(A)P_A(B)']),
(PR,'Capacités','Distinguer P_A(B) et P_B(A), faux positifs',['E14.6','E14.11:faux positifs']),
(PR,'Objectifs','Modèle et réalité ; Card(A∩B)/Card(B) ; vocabulaire des tests',['C14:hypothèse du modèle','C14:Card}(A\\cap B)','C14:faux négatifs','E14.11:sensibilité']),
(PR,'Limite','Probabilités totales sur une partition : non attendu, signalé',['C14:n’est pas un attendu']),
]
for code,libelle in REPERES_AUTOMATISMES.items():
    bloc={'C':'Calcul numérique et algébrique','P':'Proportions et pourcentages','E':'Évolutions et variations',
          'F':'Fonctions et représentations','G':'Géométrie','S':'Statistiques','R':'Probabilités'}[code[0]]
    OFFICIEL.append(('Automatismes · '+bloc,'Capacité',libelle,['Q:'+code]))

ex_text={(c.numero,i):e.titre+'\n'+e.enonce+'\n'+e.corrige for c in CHAPITRES for i,e in enumerate(c.exercices,1)}
cours_text={c.numero:'\n'.join(c.cours) for c in CHAPITRES}
preuves=[n for t,p in PREUVES for n,a in p]
ateliers={label:body for label,title,sub,body in ATELIERS}
flash={}
for lettre,titre,questions in SERIES:
    for i,(q,s,k,bloc,reperes) in enumerate(questions,1):
        for r in reperes:flash.setdefault(r,[]).append(f'{lettre}{i}')
def lieu(spec):
    kind,_,rest=spec.partition(':')
    if kind=='Q':
        assert rest in flash,spec
        return 'Questions flash '+', '.join(flash[rest])
    if kind=='P':
        assert any(rest in n for n in preuves),spec
        return 'Démonstration « '+next(n for n in preuves if rest in n)+' »'
    if kind=='A':
        label,_,motif=rest.partition(':')
        assert motif in ateliers[label],spec
        return 'Atelier '+label
    if kind.startswith('D') and kind[1:].isdigit():
        assert 1<=int(kind[1:])<=len(DEFIS),spec
        return 'Défi '+kind
    if kind.startswith('C'):
        n=int(kind[1:]);assert rest in cours_text[n],spec
        return f'Cours du chapitre {n}'
    if kind.startswith('E'):
        n,i=map(int,kind[1:].split('.'))
        assert (n,i) in ex_text and (not rest or rest in ex_text[n,i]),spec
        return f'Exercice {n}.{i}'
    raise ValueError(spec)
officiel=[];manquants=[]
for p,r,a,specs in OFFICIEL:
    lieux=[]
    for s in specs:
        try:lieux.append(lieu(s))
        except (AssertionError,KeyError,ValueError):manquants.append(s)
    officiel.append({'partie':p,'rubrique':r,'attendu':a,'lieux':lieux,'statut':'présent' if len(lieux)==len(specs) else 'à reprendre'})
assert not manquants,manquants
parties=sorted({o['partie'] for o in officiel})

text='\n'.join(p.read_text(encoding='utf-8') for folder in ['chapitres','corriges','annexes'] for p in (ROOT/folder).glob('*.tex'))
for forbidden in [r'\forall',r'\exists',r'\frac{d',r'\ln',r'\binom',r'\lfloor',r'\lceil','\t']:
    assert forbidden not in text,forbidden
report={'programme':PROGRAMME,'bo_pdf':BO_PDF,
 'texte_officiel':'Arrêté du 26-2-2026, JO du 27-3-2026, BO n° 14 du 2 avril 2026, NOR MENE2602914A ; annexe pages 333 à 345 du BO',
 'application':'2026-2027','date_recherche':'2026-10-21','date_audit':'2026-10-23','groupes_editoriaux':matrix,
 'approfondissements_programme':[{'piste':a,'repere':b} for a,b in extensions],
 'preuves_programme':11,'demonstrations_livre':13,'chapitres':16,
 'matrice_officielle':officiel,'attendus_officiels':len(officiel),'attendus_presents':sum(o['statut']=='présent' for o in officiel),
 'precision':'Matrice issue de la lecture intégrale de l’annexe officielle de 13 pages, reprise attendu par attendu lors de l’audit du 23 octobre 2026. Chaque renvoi est contrôlé dans les sources ; les renvois de pages sont contrôlés sur le PDF compilé. Les approfondissements sont facultatifs ; leur présence ne les transforme pas en attendus obligatoires.'}
(ROOT/'build/couverture-programme.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'chapitres':16,'groupes_editoriaux':64,'pistes_facultatives':14,'preuves_programme':11,
                  'attendus_officiels':len(officiel),'attendus_presents':report['attendus_presents'],'parties':len(parties)},indent=2))
