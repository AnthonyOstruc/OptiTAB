"""Sources éditoriales du manuel ; aucune génération aléatoire des exercices."""
from pathlib import Path
import json, shutil
ROOT = Path(__file__).resolve().parent
CH = []

def E(titre, texte, questions, reponses, fig='', methode='', note=''):
    assert len(questions) == len(reponses) and len(questions) >= 2, titre
    return dict(titre=titre, texte=texte, questions=questions, reponses=reponses,
                fig=fig, methode=methode, note=note)

def C(titre, decor, objectifs, cours, tp, exos, defi, capacites):
    assert len(exos) == 12, (titre, len(exos))
    CH.append(dict(titre=titre,decor=decor,objectifs=objectifs,cours=cours,
                   tp=tp,exos=exos,defi=defi,capacites=capacites))

def Q(items):
    return '\\begin{questions}\n' + '\n'.join('\\item '+v for v in items) + '\n\\end{questions}\n'

def write(name, text):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text+'\n',encoding='utf-8')

def completer_programme():
    if CH[6].get('_enrichi'):return
    CH[6]['_enrichi']=True
    conseils=[
      ('Compter chaque mesure dans une seule classe, puis calculer la moyenne.', 'La moyenne situe la série ; l’histogramme décrit aussi sa dispersion.'),
      ('Séparer le volume de métal du volume extérieur de l’objet.', 'La cavité augmente le volume extérieur sans ajouter une masse de métal correspondante.'),
      ('Revenir à la solution initiale en utilisant le facteur de dilution.', 'La concentration mesurée est celle de la solution effectivement placée dans la gamme.'),
      ('Équilibrer les charges positives et négatives, puis compter les ions.', 'La neutralité porte sur la somme des charges, pas sur une égalité des nombres d’ions.'),
      ('Comparer séparément le nombre de protons et celui des électrons.', 'Deux entités peuvent posséder le même cortège électronique sans être le même élément.'),
      ('Mettre les deux masses dans la même unité avant de diviser.', 'Une erreur entre grammes et kilogrammes produit un facteur mille sur le comptage.'),
      ('Comparer les énergies pour une même masse, puis les températures d’utilisation.', 'Une grande énergie massique ne suffit pas : la température du changement d’état doit aussi convenir.'),
      ('Comparer les quantités de réactif limitant dans des conditions identiques.', 'Une variation de température dépend de l’énergie libérée et des échanges avec l’environnement.'),
      ('Examiner les critères fournis et préciser ceux qui manquent.', 'Un choix de protocole demande plusieurs critères : produits, déchets, énergie et sécurité.'),
      ('Comparer les noyaux avant d’examiner le cortège électronique.', 'Une ionisation ne crée pas un nouvel isotope.'),
      ('Déterminer les composantes du vecteur, puis sa norme par Pythagore.', 'Les composantes d’une vitesse ne s’additionnent pas pour donner sa valeur.'),
      ('Identifier le poids à l’attraction gravitationnelle à la surface de la planète.', 'La masse de l’objet se simplifie dans le calcul de g ; celle de la planète reste présente.'),
      ('Séparer la valeur de la vitesse et son orientation.', 'Une somme des forces non nulle ne signifie pas automatiquement une augmentation de la rapidité.'),
      ('Mesurer une différence de dates, puis utiliser la distance supplémentaire parcourue.', 'Une date d’acquisition dépend de l’origine du temps ; le retard de propagation est une différence.'),
      ('Relier l’exposition au niveau reçu, à la durée et à la distance.', 'La hauteur ou le style d’un son ne donne pas directement son niveau d’intensité sonore.'),
      ('Estimer d’abord la distance par le son, puis le temps de parcours lumineux.', 'Une approximation se justifie par une comparaison d’ordres de grandeur.'),
      ('Comparer plusieurs rapports et les écarts à la précision des mesures.', 'Un modèle expérimental se juge à l’échelle des incertitudes, pas sur l’égalité parfaite de nombres arrondis.'),
      ('Former le quotient distance image sur distance objet et traiter le sens séparément.', 'Un grandissement négatif correspond ici à une image renversée.'),
      ('Lire les unités de la pente puis comparer le décalage aux écarts de mesure.', 'Une faible ordonnée à l’origine n’invalide pas automatiquement le modèle ohmique.'),
      ('Vérifier successivement le capteur, les connexions et l’acquisition.', 'Une valeur instable peut venir de la chaîne de mesure et pas seulement de la grandeur étudiée.')]
    for c,(m,n) in zip(CH,conseils):
        c['exos'][11]['methode']=m;c['exos'][11]['note']=n
    CH[18]['exos'][6]['fig']='parallele'
    CH[18]['defi']['fig']='parallele-defi'
    CH[17]['defi']=E('Agrandir une projection',
        r'Un objet de 2,0 cm est placé à 15 cm d’une lentille de focale 10 cm. On souhaite le projeter sur un écran.',
        [r'Construire l’image et déterminer la position de l’écran.',r'Calculer le grandissement par les tailles puis vérifier par Thalès.',r'Comparer à l’objet placé à 30 cm de la même lentille : quel choix agrandit l’image et quelle place faut-il prévoir derrière la lentille ?'],
        [r'La construction donne une image à 30 cm après la lentille, de taille 4,0 cm et renversée.',r'$\gamma=-4,0/2,0=-2,0$ ; par Thalès, $|\gamma|=30/15=2,0$, cohérent avec le renversement.',r'Lorsque l’objet était placé à 30 cm de la lentille, l’image mesurait 1,0 cm et se formait à 15 cm derrière la lentille. Rapprocher l’objet de F, tout en restant au-delà de F, produit ici une image agrandie mais demande davantage de recul pour l’écran.'],
        'lentille-agrandie',methode=r'Piste 1 : tracer le rayon central et celui qui arrive parallèlement à l’axe. Piste 2 : lire les deux échelles. Piste 3 : comparer au cas du chapitre.',
        note=r'Pour projeter une image agrandie, il faut anticiper à la fois le placement de l’objet et le recul de l’écran.')
    CH[6]['cours'][0]=(CH[6]['cours'][0][0],CH[6]['cours'][0][1]+r'\schema{etats-micro}')
    CH[2]['cours'][2]=(CH[2]['cours'][2][0],CH[2]['cours'][2][1]+r'''\schema{teintes}
    \begin{exemple}[Comparer une teinte]Dans la gamme schématique, X est plus foncée que l'étalon à 4 g/L et plus claire que celui à 6 g/L. On peut proposer $4<c_X<6$ g/L, sans prétendre à une lecture plus précise.\end{exemple}''')

def produire():
    import contenu_matiere, contenu_mouvement, contenu_signaux
    from evaluations import DS
    assert len(CH)==20 and len(DS)==6
    completer_programme()
    source = ROOT.parent/'livre-pc-premiere'
    for name in ('optitab-livre.sty','pc-livre.sty','compiler.py'):
        s=(source/name).read_text(encoding='utf-8')
        if name=='optitab-livre.sty':
            for a,b in [('Première · Spécialité','Seconde générale et technologique'),
                        ('{21}','{20}'),('{315}','{240}'),('{336}','{260}'),
                        ('Spécialité physique-chimie · Première','Physique-chimie · Seconde'),
                        ('de deux heures','de 90 minutes'),('Deux heures','90 minutes'),
                        ("deux heures d'affilée","90 minutes d'affilée"),
                        ('\\textbf{2 heures}','\\textbf{90 minutes}')]:s=s.replace(a,b)
            # Six chiffres sur une ligne de couverture trop longue : niveau court, voie ailleurs.
            s=s.replace('\\newcommand{\\otNiveau}{Seconde générale et technologique}',
                        '\\newcommand{\\otNiveau}{Seconde · Voie générale et technologique}')
        if name=='compiler.py':
            s=s.replace("'.png','.dat'","'.png','.dat','.pdf'")
        write(name,s)
    for name in ('couverture/premiere.tex','couverture/quatrieme.tex','liminaires/titre.tex'):
        s=(source/name).read_text(encoding='utf-8').replace('Première','Seconde').replace('première','seconde')
        s=s.replace('de spécialité physique-chimie','de physique-chimie')
        s=s.replace('Exercices inspirés des devoirs surveillés','Six évaluations avec barèmes détaillés')
        s=s.replace("Les exercices s'inspirent des devoirs surveillés et des contrôles de seconde ;",
                    'Les situations sont originales et adaptées au programme français ;')
        s=s.replace("L'équipe pédagogique OptiTAB","Collection OptiTAB")
        s=s.replace('Des bases accessibles aux défis très exigeants','Des bases accessibles aux problèmes d’approfondissement')
        # Ne promet pas des ressources web particulières dont l'existence n'a pas été contrôlée.
        s=s.replace('Prolonge ton travail en ligne', 'Retrouve la collection OptiTAB')
        s=s.replace('Cours, fiches de synthèse et exercices\n       sur', 'Le site de la collection :')
        write(name,s)
    plan=[];chapfiles=[];corfiles=[];defis=[];indices=[];defcors=[]
    parties={1:('1','Mesurer et raisonner'),2:('2','Constitution et transformations de la matière'),
             11:('3','Mouvement et interactions'),14:('4','Ondes et signaux')}
    for i,c in enumerate(CH,1):
        if i in parties:
            n,t=parties[i];plan.append(f'\\otPlanPartie{{{n}}}{{{t}}}')
        plan.append(f'\\otPlanChap{{{i}}}{{{c["titre"]}}}{{12}}')
        part='Outils de la démarche scientifique' if i==1 else ('Constitution et transformations' if i<11 else ('Mouvement et interactions' if i<14 else 'Ondes et signaux'))
        s=f'\\begin{{ouverture}}[{c["decor"]}]{{{i}}}{{{c["titre"]}}}{{{part}}}{{Observer · Modéliser · Expérimenter · Expliquer}}\n'
        s+='\n'.join('\\objectif{'+v+'}' for v in c['objectifs'])
        s+='\n\\prerequis{Proportionnalité, conversions et lecture de graphiques.}\n\\end{ouverture}\n\\essentiel\n'
        for k,(titre,texte) in enumerate(c['cours'],1):
            texte=texte.replace(r'\schema{',r'\schema[corrige]{')
            s+=f'\\essSection{{{k}}}{{{titre}}}\n{texte}\n'
        s+='\\essSection{'+str(len(c['cours'])+1)+'}{Expérimenter et modéliser}\n'+c['tp']+'\n'
        # Les conseils de rédaction figurent dans les méthodes communes et les
        # corrigés ciblés ; éviter un encadré identique à la fin de chaque cours.
        s+='\\exercices\n'
        cor=f'\\clearpage\\corrigesChapitre{{{i}}}{{{c["titre"]}}}\n\\corrigesSouples\n'
        for j,e in enumerate(c['exos'],1):
            # Coupures éditoriales : ne pas laisser le dernier exercice seul
            # sur une page après une série comportant de grandes figures.
            if (i,j) in {(8,9),(11,9)}:s+='\\clearpage\n'
            if (i,j) in {(2,10),(3,9),(12,9),(15,9)}:cor+='\\clearpage\n'
            if j in (1,5,9):s+='\\rubrique{'+{1:'Prendre confiance',5:'S’entraîner',9:'Raisonner et approfondir'}[j]+'}\n'
            s+=f'\\begin{{blocLivre}}{{ex-{i}-{j}}}\\begin{{exercice}}[{(j-1)//4+1}]{{{e["titre"]}}}\n'+e['texte']+'\n'
            if e['fig']:s+='\\schema{'+e['fig']+'}\n'
            s+=Q(e['questions'])+'\\end{exercice}\\end{blocLivre}\n'
            cor+=f'\\begin{{blocLivre}}{{cor-{i}-{j}}}\\begin{{corrige}}{{{j}}}{{{e["titre"]}}}\n'
            if e['methode']:cor+='\\demarche{'+e['methode']+'}\n'
            if e['fig']:cor+='\\schema[corrige]{'+e['fig']+'}\n'
            cor+=Q(e['reponses'])
            if e['note']:cor+='\\retiens{'+e['note']+'}\n'
            cor+='\\end{corrige}\\end{blocLivre}\n'
        slug=f'{i:02d}';write(f'chapitres/{slug}.tex',s);write(f'corriges/{slug}.tex',cor)
        chapfiles.append(f'\\input{{chapitres/{slug}}}');corfiles.append(f'\\input{{corriges/{slug}}}')
        d=c['defi']
        defis.append(f'\\editionPage{{defi-ex-{i}}}{{Défi D{i:02d} · {d["titre"]}}}{{Chapitre {i} · Approfondissement}}{{Chercher, organiser, justifier · 25 à 40 minutes}}\n\\label{{defi-ex-{i}-1}}\n'+d['texte']+'\n'+('\\schema{'+d['fig']+'}\n' if d['fig'] else '')+Q(d['questions'])+f'\\smallskip\\otRenvoi{{Indications}}{{indice-{i}}}\\hfill\\otRenvoi{{Corrigé}}{{defi-cor-{i}-1}}\n')
        indices.append('\\par\\addvspace{3mm}\\noindent\\begin{minipage}{\\linewidth}\n'+f'{{\\otSemi\\color{{otNavy}}Défi D{i:02d}}}\\phantomsection\\label{{indice-{i}}}\\par\\vspace{{1mm}}\n'+d['methode']+'\n\\end{minipage}\\par\n')
        defcors.append(f'\\editionPage{{defi-cor-{i}-1}}{{Solution du défi D{i:02d}}}{{{d["titre"]}}}{{Une démarche possible ; d’autres rédactions sont recevables.}}\n'+('\\schema[corrige]{'+d['fig']+'}\n' if d['fig'] else '')+Q(d['reponses'])+'\\editionRetenir{'+d['note']+'}\n')
    write('plan.tex','\n'.join(plan))
    defis[0]=defis[0].replace('\\label{defi-ex-1-1}', '\\label{defi-ex-1-1}\\label{defis-debut}')
    write('annexes/defis-enonces.tex','\n'.join(defis))
    write('annexes/indices-defis.tex','\\editionPage{indices-defis}{Indications progressives}{Défis D01 à D10}{Lire une piste, puis reprendre sa recherche.}\\fontsize{10}{13}\\selectfont\n'+'\n'.join(indices[:10])+'\n\\editionPage{indices-suite}{Indications progressives}{Défis D11 à D20}{Lire une piste, puis reprendre sa recherche.}\\fontsize{10}{13}\\selectfont\n'+'\n'.join(indices[10:]))
    write('annexes/defis-corriges.tex','\n'.join(defcors))
    for i,d in enumerate(DS,1):
        assert sum(d['points'])==20
        ss=f'\\devoirDS{{{i}}}{{{d["portee"]}}}{{'+','.join(f'{e["titre"]}/{p}' for e,p in zip(d['exos'],d['points']))+'}\n'
        cc=f'\\clearpage\\corrigeDevoir{{{i}}}\n'
        for j,(e,p,marks) in enumerate(zip(d['exos'],d['points'],d['bareme']),1):
            assert len(marks)==len(e['questions']) and sum(marks)==p
            ss+=f'\\begin{{blocLivre}}{{ds-{i}-{j}}}\\begin{{exoBac}}{{{p}}}{{{e["titre"]}}}\n'+e['texte']+'\n'
            cc+=f'\\begin{{blocLivre}}{{dscor-{i}-{j}}}\\begin{{corrigeBac}}{{{p}}}{{{e["titre"]}}}\n\\demarche{{'+e['methode']+'}\n'
            if e['fig']:
                ss+='\\schema{'+e['fig']+'}\n';cc+='\\schema[corrige]{'+e['fig']+'}\n'
            ss+=Q(e['questions'])+'\\end{exoBac}\\end{blocLivre}\n'
            cc+=Q([a+'\\pts{'+str(m).replace('.',',')+' pt}' for a,m in zip(e['reponses'],marks)])+'\\end{corrigeBac}\\end{blocLivre}\n'
        write(f'devoirs/ds-{i:02d}.tex',ss);write(f'devoirs/corrige-{i:02d}.tex',cc)
    from liminaires import produire_liminaires
    produire_liminaires(CH)
    main=r'''\documentclass[11pt,twoside,openany]{book}
\usepackage{optitab-livre}
\usepackage{pc-livre}
\usetikzlibrary{fit,patterns,decorations.pathmorphing,decorations.markings}
\pgfplotsset{otMesures/.style={axis lines=left,width=12cm,height=5.8cm,
 ticklabel style={font=\scriptsize},label style={font=\small},
 grid=major,grid style={otRule,line width=.3pt},clip=true,
 /pgf/number format/use comma,/pgf/number format/1000 sep={\,}}}
\input{adaptations}
\hypersetup{pdftitle={Physique-chimie - Seconde générale et technologique},pdfauthor={OptiTAB},
 pdfsubject={Manuel complet : cours illustrés, 240 exercices, 20 défis et 6 évaluations corrigées}}
\begin{document}
\pagenumbering{alph}\input{couverture/premiere}
\thispagestyle{empty}\null\clearpage
\pagenumbering{arabic}
\input{liminaires/titre}\input{liminaires/copyright}
\input{liminaires/mode-emploi}\input{liminaires/sommaire}\input{liminaires/parcours}
'''
    main+='\\pagestyle{otMain}\n'+'\n'.join(chapfiles)+'\n\\input{annexes/defis-enonces}\n\\input{annexes/indices-defis}\n\\partieDevoirs\n\\input{annexes/methodes-devoir}\n'
    main+='\n'.join(f'\\input{{devoirs/ds-{i:02d}}}' for i in range(1,7))+'\n\\partieCorriges\n'
    main+='\n'.join(corfiles)+'\n\\input{annexes/defis-corriges}\n\\corrigesDevoirsDebut\n'
    main+='\n'.join(f'\\input{{devoirs/corrige-{i:02d}}}' for i in range(1,7))+'\n\\input{annexes/donnees-programme}\n\\input{liminaires/references}\n\\input{couverture/quatrieme}\n\\end{document}'
    write('main.tex',main)
    write('inventaire.json',json.dumps([dict(numero=i,titre=c['titre'],exercices=len(c['exos']),questions=sum(len(e['questions']) for e in c['exos']),capacites=c['capacites']) for i,c in enumerate(CH,1)],ensure_ascii=False,indent=2))
    print('20 chapitres, 240 exercices, 20 défis, 6 évaluations : sources produites.')

if __name__=='__main__':
    # Même module pour les importations des sources éditoriales.
    import sys
    sys.modules['structure']=sys.modules[__name__]
    produire()
