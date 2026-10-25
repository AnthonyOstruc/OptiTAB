"""Pages d’accueil, progression annuelle et méthodes illustrées."""
from mise_en_page import *

def liminaires(b):
    b.begin('bienvenue','Mon livre de mathématiques','BIENVENUE EN CE2',subtitle='Je comprends avec des objets, des schémas et des mots.')
    b.box('CE LIVRE APPARTIENT À','Prénom : ........................................................\nClasse : ............................................................',82,40)
    t=136
    for lab,body in [('Je cherche','Je lis la question et je peux garder mes essais.'),('Je représente','Je choisis un dessin, un tableau ou un schéma utile.'),('Je calcule','Je choisis une méthode et je raconte mes étapes.'),('Je vérifie','Je contrôle le résultat et je réponds avec l’unité.')]:
        b.text(lab,22,t,165,16,bold=True,color=GREEN);t=b.text(body,22,t+11,165,14)+10
    b.begin('mode','Comment utiliser ce livre','POUR L’ADULTE',adult=True)
    parts=[
    ('Un chapitre, plusieurs séances','La découverte, la leçon, les méthodes et les neuf exercices se répartissent sur plusieurs séances. Revenir sur une notion à distance. Les bilans peuvent être fractionnés.'),
    ('Rendre le raisonnement visible','Faire reformuler l’objectif, montrer une méthode puis guider un premier essai. Relier le matériel, le schéma et les écritures. Retirer progressivement les aides quand l’enfant peut expliquer sa démarche.'),
    ('Aider sans faire à la place','Lire les énoncés si nécessaire. Demander « Que cherches-tu ? » et « Que représente ce résultat ? ». Accepter une réponse orale avant la trace écrite. Adapter les nombres quand la structure du problème est nouvelle.'),
    ('Observer les progrès','Les corrigés proposent des démarches, des critères et des pistes de reprise. Une erreur aide à identifier ce qui reste à comprendre. Les activités ouvertes peuvent avoir plusieurs réponses valables.'),
    ('Organiser l’année','Consacrer au moins deux tiers du temps aux nombres, au calcul et aux problèmes. Les numéros de chapitres aident à retrouver les notions ; ils ne constituent pas l’ordre de toutes les séances. Suivre les reprises par période.'),
    ('Imprimer et construire','A4 à 100 %, sans ajustement. Vérifier le repère de 5 cm. Photocopier le matériel à découper. Les grandes constructions se font sur une feuille séparée. L’adulte accompagne les premiers gestes au compas et les découpages.')]
    t=81
    for title,body in parts:
        b.text(title,19,t,172,12.5,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.3,leading=15)+8
    b.begin('progression','Une progression sur cinq périodes','POUR L’ADULTE',adult=True)
    periods=[
    ('P1 · Installer le millier et les méthodes','Nombres supérieurs à 1 000 dès le début (1-3), additions et soustractions posées (4-5), calcul mental (6-9). Reprendre les fractions pour établir des égalités (20). Prix à virgule dès P1 (28). Problèmes additifs (15-16), longueurs, masses et figures (24, 26, 32).'),
    ('P2 · Étendre jusqu’à 10 000','Travailler jusqu’à 10 000 au plus tard en P2 (1-3). Décomposer les produits et doubler (10-11). Partages et problèmes mixtes (14, 17). Addition posée des prix au plus tard en P2 (29). Comparer des fractions (21), périmètres, contenances et symétrie (25, 27, 35).'),
    ('P3 · Mesurer avec des fractions','Fractions d’unité de longueur à partir de P3 (22), puis opérations avec des dénominateurs liés (23). Introduire ou poursuivre les multiplications posées (12-13), comparaisons multiplicatives et combinaisons (18-19). Heures, durées, constructions et solides (30-34).'),
    ('P4 · Consolider et transférer','Multiplication posée au plus tard en P4 (12-13) et soustraction posée des prix au plus tard en P4 (29). Reprendre les problèmes en plusieurs étapes, les mesures, les fractions et la symétrie. Lire et construire des graphiques avec une échelle adaptée (36).'),
    ('P5 · Préparer la continuité vers le CM1','Reprises ciblées de tous les domaines, enquêtes et problèmes nouveaux. Renforcer les faits numériques et le choix des procédures. Répartir le bilan final sur plusieurs moments pour déterminer les dernières reprises.')]
    t=81
    for title,body in periods:
        b.text(title,19,t,172,12.5,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.1,leading=14.8)+8
    b.box('LES PROBLÈMES DE LA SEMAINE','36 semaines de 10 histoires sont proposées à l’adulte. Choisir les situations selon les acquis ; elles complètent les problèmes écrits et les activités de la classe.',242,32,size=11.3)
    for part in range(2):
        b.begin(f'sommaire-{part+1}','Sommaire' if not part else 'Sommaire et ressources','PARCOURS DU LIVRE',subtitle='Cliquer sur un titre ou un numéro de page pour le retrouver.')
        if not part:b.outline('Sommaire','sommaire-1')
        t=82
        for ch in CHAPITRES[part*18:(part+1)*18]:
            key=f'ch-{ch.numero}-decouverte';b.text(f'{ch.numero:02}',19,t,12,11.5,bold=True,color=GREEN);b.text(ch.titre,34,t,142,11.3);b.text(str(b.refs.get(key,'…')),179,t,14,11.5,bold=True,color=NAVY);b.link(key,18,t,176,7.8);t+=8
        if part:
            t+=5
            for title,key in [('Les cinq bilans','bilan-1-1'),('Les corrigés expliqués','corriges-intro'),('360 problèmes oraux pour l’adulte','oral-intro'),('Matériel et fiches outils','outils-intro'),('Programme et sources','programme-1')]:
                b.text(title,20,t,155,11.2,bold=True,color=NAVY);b.text(str(b.refs.get(key,'…')),179,t,15,11.2);b.link(key,18,t,176,7.8);t+=8
    b.begin('rituels','Des reprises qui font progresser','POUR L’ADULTE',adult=True)
    t=82
    for title,body in [
    ('Les faits numériques','Reprendre les tables dans les deux sens, les facteurs manquants, les doubles et moitiés utiles. Répartir les rappels dans le temps et mélanger les questions. Les produits qui donnent 60 deviennent des repères.'),
    ('Des procédures expliquées','Ajouter ou retirer près d’une dizaine, multiplier par 10 ou 100, calculer avec des dizaines, décomposer un produit, multiplier par 4 ou par 8. Faire choisir une méthode adaptée ; garder les résultats intermédiaires sur l’ardoise au début.'),
    ('Les repères de fin de CE2','Programme : 15 égalités d’addition en 1 minute ; 12 égalités de multiplication en 1 minute ; 12 faits multiplicatifs usuels en 1 minute ; 15 calculs par procédure en 3 minutes. Les fiches outils permettent des observations après apprentissage.'),
    ('Une observation qui aide','Les temps limités deviennent des routines connues. Valoriser les progrès de l’enfant par rapport à ses propres essais précédents. Maintenir les adaptations habituelles et observer aussi l’explication des méthodes.'),
    ('Les histoires à résoudre','Le programme prévoit au moins dix problèmes par semaine, dont une partie peut être orale. Faire comprendre, représenter, calculer, répondre puis vérifier. Varier les contextes et ne pas annoncer l’opération dans la consigne.')]:
        b.text(title,19,t,172,12.8,bold=True,color=GREEN);t=b.text(body,19,t+9,172,11.6,leading=15.4)+10
    b.begin('suivi','Mes progrès au fil de l’année','À COMPLÉTER AVEC L’ADULTE',subtitle='Je peux réussir avec du matériel, avec un schéma, puis de façon autonome.')
    t=83
    for label in ['Lire et représenter jusqu’à 10 000','Comparer et placer les nombres','Expliquer une addition ou une soustraction','Choisir une procédure de calcul mental','Poser une multiplication à un ou deux chiffres','Comprendre un partage ou un groupement','Comparer et calculer avec des fractions','Mesurer en fractions d’une unité','Planifier les étapes d’un problème','Utiliser les mesures, les prix et les durées','Construire, décrire et reconnaître une symétrie','Organiser et interpréter des données']:
        b.text(label,20,t,138,11.8);b.c.setStrokeColor(RULE)
        for x in [165,176,187]:b.c.rect(x*mm,H-(t+4)*mm,4*mm,4*mm)
        b.line(19,t+10,193);t+=14
    b.text('Trois observations à des dates différentes :\n........................ / ........................ / ........................',20,258,172,10.7,color=MUTED)

def methodes(b,ch):
    n=ch.numero
    if n in [12,13]:
        two=n==13;b.begin(f'ch-{n}-methode','Le sens des lignes du calcul',f'CHAPITRE {n:02} · MÉTHODE PAS À PAS')
        if two:
            b.box('JE SÉPARE LES UNITÉS ET LES DIZAINES','16 = 6 + 10. Je cherche 234 fois 6, puis 234 fois 10.',83,30,size=14)
            b.fig(('multwo',[234,16]),119,99)
            b.box('JE RÉUNIS LES DEUX PRODUITS','1 404 correspond à × 6.\n2 340 correspond à × 10, avec zéro unité.\n1 404 + 2 340 = 3 744.',226,47,fill=MINT,size=13.5)
        else:
            b.box('JE GARDE LA VALEUR DES RANGS','6 × 3 = 18 unités : j’écris 8 unités et j’échange 10 unités contre 1 dizaine. Cette dizaine rejoint le calcul des dizaines.',83,40,size=13.6)
            b.fig(('mulone',[246,3]),135,76)
            b.box('JE VÉRIFIE EN DÉCOMPOSANT','200 × 3 = 600 ; 40 × 3 = 120 ; 6 × 3 = 18.\n600 + 120 + 18 = 738.',226,43,fill=MINT,size=13.5)
    elif n==19:
        b.begin('ch-19-arbre','Suivre chaque choix dans un arbre','CHAPITRE 19 · MÉTHODE')
        b.text('Deux entrées, trois plats et deux desserts : chaque chemin complet donne un menu. Suis les branches pour retrouver les douze menus.',20,82,172,13.4)
        b.fig(('choicetree',None),113,119,x=20,w=173)
        b.box('JE VÉRIFIE','Pour chaque entrée, il y a 3 × 2 = 6 menus. Avec deux entrées : 2 × 6 = 12 menus.',241,32,fill=MINT,size=13)
    elif n==22:
        b.begin('ch-22-regle','La même unité, plusieurs partages','CHAPITRE 22 · MÉTHODE')
        b.box('L’UNITÉ RESTE LA MÊME','Les règles en quarts et en dixièmes utilisent toutes les deux l’unité u de 4 cm. Le zéro est le départ de la mesure.',83,38,size=13.5)
        b.fig(('unitlength',[4,1,2]),130,46)
        b.fig(('unitlength',[10,1,5]),187,46)
        b.text('Les deux segments ont la même longueur :\n1 u + 1/2 u = 1 u + 5/10 u.',23,249,164,14,bold=True,color=GREEN)
    elif n==29:
        b.begin('ch-29-aligner','Aligner les euros et les centimes','CHAPITRE 29 · MÉTHODE')
        b.box('J’ADDITIONNE','7,85 € + 0,68 €. Les euros sont sous les euros, les dizaines de centimes sous les dizaines de centimes.',83,38,size=13.5)
        b.fig(('eurocolumn',['7,85','0,68','+']),127,43)
        b.box('JE SOUSTRAIS PAR ÉCHANGES','10,00 € - 3,65 €. Je peux vérifier en centimes : 1 000 - 365 = 635, soit 6,35 €.',181,38,fill=MINT,size=13.5)
        b.fig(('eurocolumn',['10,00','3,65','-']),227,43)
    elif n==35:
        b.begin('ch-35-plier','Du pliage au quadrillage','CHAPITRE 35 · MÉTHODE')
        b.box('JE CONTRÔLE LES DISTANCES','La ligne pointillée est l’axe. Chaque sommet à gauche est associé à un sommet à droite, sur la même ligne et à la même distance de l’axe.',83,40,size=13.5)
        b.fig(('symmetrymethod',None),138,87)
        b.box('JE VÉRIFIE PAR SUPERPOSITION','Photocopie, plie sur l’axe ou utilise du papier calque. Les deux moitiés doivent se superposer exactement.',241,32,fill=MINT,size=13)
