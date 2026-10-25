"""Matrice éditoriale des contenus, capacités et démonstrations du programme 2026."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
(ROOT/'build').mkdir(exist_ok=True)
rows=[]
def add(domain, label, chapter, exercises, proof=None, sujets=()):
    rows.append(dict(domaine=domain,attendu=label,chapitre=chapter,exercices=exercises,preuve=proof,sujets=list(sujets)))

add('Algèbre','Modes de génération, indices et passage entre formule, récurrence, graphique et motifs',2,[1,2,9,10,15])
add('Algèbre','Suites arithmétiques : terme général, variations et sommes de termes consécutifs',2,[3,6,7,12,14],'dem-suites')
add('Algèbre','Suites géométriques : terme général, variations et sommes de termes consécutifs',2,[4,5,6,7,9,11,14],'dem-suites')
add('Algèbre','Modèles discrets à accroissement ou à taux constant ; calcul de seuils',2,[5,11,12,13,14])
add('Algèbre','Comportements à long terme : valeur approchée, croissance sans borne et oscillation',2,[8,9])
add('Algèbre','Sommes des entiers et des puissances successives : justifications',2,[7,12,15],'dem-suites')
add('Algèbre','Formes développée, canonique et factorisée ; somme et produit des racines',1,[2,3,6,9,10],'dem-second-degre')
add('Algèbre',r'Trinômes s’annulant en deux réels donnés ; courbe de $x\mapsto f(x-m)$ par translation',1,[9,15])
add('Algèbre','Discriminant, équations, signe du trinôme et inéquations',1,[4,5,8,11,15],'dem-second-degre')
add('Algèbre','Choix de forme adapté à une comparaison, une aire ou un problème de maximum',1,[6,7,12,13,14])
add('Analyse','Taux de variation, sécantes, nombre dérivé et interprétation en contexte',3,[1,2,6,13,15],'dem-derivation')
add('Analyse','Algorithme : liste des coefficients directeurs des sécantes pour un pas donné',3,[6])
add('Analyse','Équation et construction de tangente ; approximation affine',3,[4,9,10,12,14],'dem-derivation')
add('Analyse','Dérivées de référence, puissances entières et opérations sur les fonctions',3,[3,5,7,8],'dem-derivation')
add('Analyse','Non-dérivabilité de la valeur absolue et de la racine carrée en zéro',3,[11],'dem-derivation')
add('Analyse','Signe de la dérivée, variations, extremums et optimisation',4,[1,2,3,4,5,6,11,12,13,14,15])
add('Analyse','Nombre dérivé nul en un extremum intérieur ; trinôme étudié par sa dérivée',4,[2,5])
add('Analyse','Fonctions paires et impaires ; symétries de leurs courbes',4,[8])
add('Analyse','Comparaison de courbes, tangentes et inégalités par les variations',4,[7,9,10])
add('Analyse','Exponentielle : définition, propriétés algébriques, positivité et croissance',5,[1,2,3,4,5])
add('Analyse','Dérivée exponentielle affine, étude de fonctions et modèles continus',5,[6,7,8,9,10,12,13,14,15])
add('Analyse','Lien avec les suites géométriques ; méthode d’Euler et valeurs approchées de $e$',5,[10,11])
add('Analyse','Cercle trigonométrique, radians, points-images et longueurs d’arcs',6,[1,2,3,5,10,12,13,14,15])
add('Analyse','Sinus, cosinus, valeurs remarquables et symétries des angles',6,[3,4,6,7,8,9,11],'dem-trigonometrie')
add('Analyse',r'Algorithme : approximation de $\pi$ par la méthode d’Archimède',6,[15])
add('Géométrie','Calcul vectoriel dans le plan, coordonnées, normes et bases orthonormées',7,[1,2,4,8,9,10])
add('Géométrie','Produit scalaire par les coordonnées, les normes, un angle ou une projection',7,[2,3,5,6,7,11,12,14])
add('Géométrie','Bilin éarité, symétrie, carrés de normes et calculs sans coordonnées'.replace('Bilin éarité','Bilinéarité'),7,[6,9,10,15])
add('Géométrie','Orthogonalité, longueurs et angles ; formule d’Al-Kashi',7,[4,7,8,11,12],'dem-geometrie')
add('Géométrie','Expression avec un milieu et cercle de diamètre donné',7,[13,15],'dem-geometrie')
add('Géométrie','Vecteurs normaux et équations cartésiennes de droites',8,[1,2,7,10,11,12])
add('Géométrie','Coordonnées d’un projeté orthogonal et configuration repérée',8,[5,6,10,12,13])
add('Géométrie','Équations de cercles : reconnaissance, centre, rayon et utilisation',8,[3,4,8,9,10,12,13,14,15])
add('Probabilités et statistiques','Probabilités conditionnelles, arbres et tableaux ; inversion du conditionnement',9,[1,2,5,6,7,8])
add('Probabilités et statistiques','Partitions, probabilités totales et modèles à plusieurs groupes',9,[5,6,7,8,14,15],'dem-probabilites')
add('Probabilités et statistiques','Indépendance, incompatibilité et évènements contraires',9,[3,4,10,11,14])
add('Probabilités et statistiques','Succession de deux épreuves et répétition de Bernoulli jusqu’à quatre épreuves',9,[9,10,11,12,13])
add('Probabilités et statistiques','Variable aléatoire comme fonction d’un univers fini ; évènements et lois',10,[1,2,3,4,5,10,13,15])
add('Probabilités et statistiques','Espérance, variance, écart type et formule de König-Huygens',10,[2,3,4,6,7,8,11,12,13,14,15],'dem-probabilites')
add('Probabilités et statistiques','Linéarité de l’espérance, transformations et problèmes de jeux équitables',10,[5,7,9,10,11,12,13,14],'dem-probabilites')
add('Probabilités et statistiques','Simulation de lois, échantillons et moyennes observées',11,[4,5,10,12,13])
add('Probabilités et statistiques','Répétition d’échantillons et proportion des écarts à la moyenne sous un seuil donné',11,[10,11,13])
add('Probabilités et statistiques',r'Estimation d’aires et de $\pi$ par Monte-Carlo',11,[8,9])
add('Algorithmique et programmation','Variables, affectations, tests, fonctions et programmation modulaire',12,[1,2,3,6,7,8,9,10,11,12,13,14,15])
add('Algorithmique et programmation','Listes en extension, par ajouts et en compréhension ; modification et parcours',12,[4,5,10,11,12,13])
add('Algorithmique et programmation','Termes, sommes, seuils et factorielle ; Fibonacci et Syracuse',12,[6,7,8,9,12,13])
add('Algorithmique et programmation',r'Méthode de Newton : tangente et approximation de $\sqrt2$',12,[14])
add('Algorithmique et programmation','Moments d’une loi, fréquences de lettres et simulations d’aires',12,[10,11,15])
add('Vocabulaire et logique','Appartenance, inclusion, ensembles de nombres, opérations et intervalles',13,[1,2,4,5,9,13])
add('Vocabulaire et logique','Couples, produit cartésien et cardinal d’un ensemble fini',13,[3])
add('Vocabulaire et logique','Implication, équivalence, réciproque, contraposée et conditions nécessaires ou suffisantes',13,[6,7,12])
add('Vocabulaire et logique','Quantification, négation, contre-exemples et statut des égalités ou des lettres',13,[4,5,8,10,14,15])
add('Vocabulaire et logique','Preuves directes, par cas, par contraposée et par l’absurde',13,[10,11,12,13,15])
add('Automatismes','Valeurs initiales ou finales, taux simples, composés et réciproques',14,[1,2])
add('Automatismes','Calcul littéral, produit nul et signes d’expressions',14,[3,4,9,11])
add('Automatismes','Lectures graphiques, pentes et équations de droites',14,[5,6],sujets=('sujet-A','sujet-B'))
add('Automatismes','Automatismes de Seconde : fractions, puissances, proportions, variable isolée',14,[2,3],sujets=('sujet-B',))
add('Automatismes','Tableaux croisés, probabilités conditionnelles et représentations statistiques',14,[7,10],sujets=('sujet-A','sujet-B'))
add('Automatismes','Histogrammes, diagrammes en barres ou en boîte et indicateurs descriptifs',11,[1,2,3,6,7,14])
add('Compétences transversales','Chercher, modéliser, représenter, raisonner, calculer et communiquer dans des synthèses',14,[12,13,14,15])

chapters={int(p.name[:2]):p for p in (ROOT/'chapitres').glob('*.tex')}
prooftext=(ROOT/'annexes/demonstrations.tex').read_text(encoding='utf-8')
for row in rows:
    text=chapters[row['chapitre']].read_text(encoding='utf-8')
    count=text.count(r'\begin{exercice}')
    assert all(1<=i<=count for i in row['exercices'])
    if row['preuve']:
        assert r'\label{'+row['preuve']+'}' in prooftext
    row['source']=chapters[row['chapitre']].relative_to(ROOT).as_posix()

report={'reference':'BO du 2 avril 2026, NOR MENE2602917A, rentrée 2026-2027',
        'url':'https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A',
        'portee':'Contenus et capacités du programme ; approfondissements facultatifs sélectionnés, sans prétendre les inclure tous.',
        'nature':'Repérage éditorial contrôlé des cours, exercices et preuves ; distinct de la vérification des résultats mathématiques.',
        'nombre_de_groupes':len(rows),'couverture':rows}
(ROOT/'build/couverture-programme.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
out=[r'''\clearpage
\gdef\otChapNum{0}
\pagestyle{otFront}
\phantomsection\label{couverture-programme}
\pdfbookmark[0]{Repères du programme}{bm-couverture-programme}
\otPageTitre{Repères du programme}{Retrouver les contenus, les méthodes et les preuves}
{\fontsize{10}{14}\selectfont
Ce tableau relie les contenus et capacités du programme de Première générale
spécialité aux cours et à des exercices du livre. Il sert à organiser les révisions.
Les approfondissements facultatifs du programme sont sélectionnés ; ils ne
sont pas tous nécessaires à l'apprentissage des attendus. Les références du
texte officiel figurent à la fin du livre.}\par\vspace{3mm}
\begingroup\fontsize{9}{12}\selectfont
\setlength{\tabcolsep}{3pt}
\begin{longtable}{@{}p{101mm}p{58mm}@{}}
\toprule\textbf{Contenu ou capacité travaillée}&\textbf{Où travailler dans le livre}\\\midrule
\endfirsthead
\toprule\textbf{Contenu ou capacité travaillée}&\textbf{Où travailler dans le livre}\\\midrule
\endhead
''']
previous=None
for row in rows:
    if previous!=row['domaine']:
        # Un intitulé de domaine ne reste jamais seul en bas de page.
        out.append('\\multicolumn{2}{@{}l}{\\otSemi\\color{otNavy}'+row['domaine']+'}\\\\*[2mm]\n')
        previous=row['domaine']
    ch=row['chapitre']
    ids=row['exercices']
    links=[r'\hyperref[ess-'+str(ch)+']{Cours p.~\\pageref*{ess-'+str(ch)+'}}']
    # Deux exercices repères, la matrice JSON contient le repérage complet.
    for i in ids[:2]:
        links.append(r'\hyperref[exo-'+f'{ch}-{i}'+']{Ex.~'+f'{ch}.{i}'+'}')
    if row['preuve']:
        links.append(r'\hyperref['+row['preuve']+']{Preuve p.~\\pageref*{'+row['preuve']+'}}')
    for s in row['sujets']:
        links.append(r'\hyperref['+s+']{Sujet '+s[-1]+' p.~\\pageref*{'+s+'}}')
    out.append(row['attendu'].replace('’',"'")+' & '+r'\newline '.join(links)+r'\\[2.3mm]'+'\n')
out.append(r'\bottomrule\end{longtable}\endgroup\clearpage'+'\n')
(ROOT/'annexes/couverture-programme.tex').write_text(''.join(out),encoding='utf-8')
print(f'{len(rows)} groupes de contenus et capacités repérés dans les 14 chapitres.')
