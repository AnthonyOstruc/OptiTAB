"""Génère le parcours avancé et les sujets ; conserve les 210 exercices relus."""
from pathlib import Path
import hashlib,json,re
from edition_france_contenu import DEFIS
from edition_france_sujets import SUJETS
from edition_france_figures import FIGURES,ecrire_figures
from edition_france_liminaires import ecrire_liminaires
R=Path(__file__).resolve().parent
ANN=R/'annexes'
placements=[];pages=[]

def page(label,title,subtitle,meta,body,figures=(),corrige=False,parent=None):
    option=rf'[\pdfbookmark[0]{{{parent[0]}}}{{{parent[1]}}}]' if parent else ''
    text=rf'\editionPage{option}{{{label}}}{{{title}}}{{{subtitle}}}{{{meta}}}'+'\n'
    text+=rf'\begin{{blocEdition}}{{{label}}}'+'\n'+body+'\n'
    for i,key in enumerate(figures,1):
        flabel=f'figedition-{label}-{i}'
        text+=rf'\label{{{flabel}}}\figureGeo'+('[corrige]' if corrige else '')+'{'+key+'}\n'
        placements.append(dict(label=flabel,page_label=label,figure=key,corrige=corrige))
    text+=r'\end{blocEdition}'+'\n'
    pages.append(dict(label=label,titre=title,body_sha256=hashlib.sha256(body.encode()).hexdigest()))
    return text

enonces=[r'''\clearpage
\gdef\otChapNum{0}\pagestyle{otFront}
\phantomsection\label{defis-debut}\pdfbookmark[0]{Défis d'approfondissement}{bm-defis}
\otPageTitre{Défis d'approfondissement}{Chercher plus loin avec les outils de Première}
\fontsize{11}{16}\selectfont
Les 210 exercices des chapitres installent les bases et les méthodes. Les
14 défis suivants portent le total à \textbf{224 exercices corrigés}.
Ils prolongent chaque thème par une question qui demande de prendre du recul,
de choisir une représentation ou de relier plusieurs notions.\par\vspace{4mm}
\textbf{Avancé} désigne une modélisation ou une synthèse soutenue.
\textbf{Très exigeant} ajoute une discussion, une preuve ou plusieurs changements de point de vue.
Ces indications sont des repères pédagogiques, pas un classement officiel.\par\vspace{4mm}
Les défis sont facultatifs pour un premier passage. Ils utilisent les notions
de Première ; les étapes qui dépasseraient les outils du cours sont explicitement admises.
Les durées proposées sont indicatives.\par\vspace{5mm}
\editionEtape{Chercher avant de lire la solution}
Faire un dessin ou un tableau, tester un cas simple, puis écrire ce qui manque
pour conclure. En cas de blocage, lire seulement le premier indice, puis reprendre
la recherche. Les indications sont séparées des énoncés et des corrigés.
\begin{center}\renewcommand{\arraystretch}{1.25}
\begin{tabular}{@{}lll@{}}\toprule
Défis & Thèmes & Préparation conseillée\\\midrule
D01 à D02 & Algèbre et suites & Chapitres 1, 2, 12, 13\\
D03 à D06 & Analyse et trigonométrie & Chapitres 1 à 6, 8, 12\\
D07 à D08 & Géométrie & Chapitres 1, 7, 8\\
D09 à D11 & Probabilités et statistiques & Chapitres 1, 9 à 11\\
D12 à D14 & Algorithmes et synthèses & Plusieurs chapitres, selon le défi\\\bottomrule
\end{tabular}\end{center}
\editionRetenir{Une solution incomplète mais justifiée est un progrès.
Après la correction, refaire la question clé sans regarder, puis expliquer pourquoi la méthode fonctionne.}
''']
corrections=[]
for d in DEFIS:
    n=d['numero'];code=f'D{n:02}'
    meta=f"{d['niveau']} · {d['duree']} · Chapitres {d['chapitres']}"
    meta+=rf'\hfill\hyperref[defi-cor-{n}-1]{{Corrigé p.~\pageref*{{defi-cor-{n}-1}}}}'
    enonces.append(page(f'defi-ex-{n}',f'{code} · '+d['titre'],'Recherche et rédaction',meta,d['enonce'],d['figures'].get('enonce',[])))
    for j,body in enumerate(d['corrige'],1):
        title=f'{code} · Corrigé'+(' (suite)' if j>1 else '')
        corrections.append(page(f'defi-cor-{n}-{j}',title,d['titre'],
            rf'\hyperref[defi-ex-{n}]{{Énoncé p.~\pageref*{{defi-ex-{n}}}}} · Démarche et vérifications',
            body,d['figures'].get(f'corrige_{j}',[]),True,
            ('Corrigés des défis','bm-corriges-defis') if n==1 and j==1 else None))

indices=[]
for start in range(0,14,5):
    body=[]
    for d in DEFIS[start:start+5]:
        n=d['numero']
        body.append(rf'\editionEtape{{D{n:02} · {d["titre"]}}}')
        for j,hint in enumerate(d['indices'],1):body.append(rf'\textbf{{Indice {j}.}} '+hint+r'\par\smallskip')
    label='indices-defis' if start==0 else f'indices-defis-{start//5+1}'
    indices.append(page(label,'Indications progressives','Lire une aide, puis reprendre la recherche',
        r'Les indices orientent la démarche ; les solutions restent dans la partie Corrigés.','\n'.join(body)))

guide=r'''\clearpage
\gdef\otChapNum{0}\pagestyle{otFront}\phantomsection\label{epreuve-guide}
\pdfbookmark[0]{Préparer l'épreuve anticipée}{bm-epreuve}
\otPageTitre{Préparer l'épreuve}{Première générale · Spécialité mathématiques · 2026-2027}
\fontsize{11}{15}\selectfont
\editionEtape{Le cadre officiel}
La note de service du 11 septembre 2026 définit l'épreuve pour l'année 2026-2027,
au titre du baccalauréat session 2028 ; elle remplace celle du 10 juin 2025.
L'épreuve écrite dure \textbf{2 heures}, a pour coefficient 2 et se passe
\textbf{sans calculatrice}. Le candidat de spécialité compose sur le sujet propre à cet enseignement.
\par\smallskip
{\renewcommand{\arraystretch}{1.12}\begin{tabularx}{\linewidth}{@{}p{43mm}Y@{}}\toprule
Première partie · 6 points & Automatismes : liste de questions à \textbf{réponses courtes}.\\
Deuxième partie · 14 points & Deux ou trois exercices indépendants.\\
Maîtrise de la langue & 2 points sur 20 : orthographe, syntaxe, lexique, organisation du propos.\\
Oral de contrôle & 20 minutes de préparation, 20 minutes d'entretien ; au moins deux exercices
sur des parties différentes du programme, sans calculatrice.\\\bottomrule
\end{tabularx}}\par\vspace{2mm}
\href{https://www.education.gouv.fr/bo/2026/Special4/MENE2622640N}{\textcolor{otNavy}{Définition officielle : note de service du 11 septembre 2026, BO spécial n° 4.}}
\editionEtape{Les automatismes évalués}
Ils relèvent de la rubrique « Automatismes » du programme de Première : évolutions et
variations, calcul numérique et algébrique, fonctions et représentations, statistiques,
probabilités ; s'y ajoutent les automatismes de Seconde. Le chapitre 14 et les sujets A et B
les entraînent. Les sujets zéro publiés en 2025 proposaient un QCM : pour la session 2028,
le candidat écrit lui-même chaque réponse courte.
\editionEtape{Deux entraînements originaux}
Les sujets A et B, créés pour ce livre, ne sont pas des sujets officiels. Chacun comporte
12 automatismes, puis deux exercices indépendants. Leur barème, choix pédagogique du livre, donne 0,5 point
par automatisme et 7 points par exercice, dont 1 point de maîtrise de la langue : orthographe,
phrases construites, vocabulaire précis, étapes enchaînées jusqu'à la conclusion.
\editionEtape{Une gestion du temps à adapter}
Environ 20 minutes pour les automatismes, 40 minutes par exercice et 20 minutes pour relire.
Après la séance, classer chaque erreur (cours, calcul, lecture, rédaction) et refaire plus tard
l'exercice de chapitre correspondant.
\editionRetenir{Une valeur exacte, un signe justifié, un domaine précisé et une phrase
qui répond à la question rendent le raisonnement vérifiable.}
\clearpage
'''
sex=[];scor=[]
for sujet in SUJETS:
    l=sujet['lettre']
    qs='\n'.join(r'\item '+q for q,a in sujet['auto'])
    # Format de la note de service du 11 septembre 2026 : 2 heures, sans calculatrice,
    # automatismes à réponses courtes (6 points), puis deux ou trois exercices (14 points).
    intro=r'''\textbf{Sujet original · Durée : 2 heures · L’usage de la calculatrice n’est pas autorisé.}
\par\smallskip\textbf{Première partie (6 points) : automatismes.} Pour chacune des 12 questions,
reporter son numéro sur la copie et donner une réponse courte, avec les unités utiles ;
aucune justification n’est demandée. Chaque question vaut 0,5 point.
\par\vspace{2mm}'''
    sex.append(page(f'sujet-{l}',f'Sujet {l} · Automatismes','Première partie · 6 points',
        rf'Corrigé p.~\pageref*{{sujet-{l}-cor-auto}}',intro+r'\begin{questions}'+qs+r'\end{questions}',
        sujet.get('figures_auto',[])))
    answers='\n'.join(r'\item '+a for q,a in sujet['auto'])
    scor.append(page(f'sujet-{l}-cor-auto',f'Sujet {l} · Corrigé','Automatismes : réponses et méthode',
        rf'\hyperref[sujet-{l}]{{Énoncé p.~\pageref*{{sujet-{l}}}}}',r'\begin{questions}'+answers+r'\end{questions}',
        sujet.get('figures_auto',[]),True,
        parent=('Corrigés des sujets blancs','bm-corriges-sujets') if l=='A' else None))
    for j,p in enumerate(sujet['problemes'],1):
        meta='7 points, dont 1 point de maîtrise de la langue'
        meta+=rf'\hfill Corrigé p.~\pageref*{{sujet-{l}-cor-{j}}}'
        # Le barème précède la question et reste lisible lorsque le texte occupe deux lignes.
        statement=re.sub(r'(\\item\s*)(.*?)(?:\\hfill\\textit\{([^}]+)\})',
            lambda m:m[1]+r'\mbox{\textit{('+m[3]+r')}}\enspace '+m[2].rstrip(),p['enonce'],flags=re.S)
        if j==1:
            statement=r'''\textbf{Deuxième partie (14 points) : deux exercices indépendants, notés chacun sur 7 points.}
\par\vspace{2mm}'''+statement
        sex.append(page(f'sujet-{l}-ex-{j}',f'Sujet {l} · Exercice {j}','Deuxième partie · '+p['titre'],meta,statement,p.get('figures_ex',[])))
        scor.append(page(f'sujet-{l}-cor-{j}',f'Sujet {l} · Corrigé {j}',p['titre'],
            rf'\hyperref[sujet-{l}-ex-{j}]{{Énoncé p.~\pageref*{{sujet-{l}-ex-{j}}}}} · Raisonnement et rédaction',
            p['corrige'],p.get('figures_cor',[]),True))

for name,content in [('defis-enonces','\n'.join(enonces)),('defis-corriges','\n'.join(corrections)),
    ('indices-defis','\n'.join(indices)),('preparation-epreuve',guide),('sujets-enonces','\n'.join(sex)),('sujets-corriges','\n'.join(scor))]:
    (ANN/(name+'.tex')).write_text(content+'\n',encoding='utf-8')
ecrire_figures()
ecrire_liminaires(R)
manifest=dict(version='France 2026-2027',base_exercices=210,defis=14,exercices_total=224,
    sujets_blancs=2,automatismes_sujets=24,problemes_sujets=4,
    defis_detail=[{k:v for k,v in d.items() if k not in ('enonce','corrige')} for d in DEFIS],
    pages=pages,figures=placements,fichiers_figures=list(FIGURES),
    sources_officielles=[
        dict(titre='Programme de Première spécialité',url='https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A',application='rentrée 2026-2027'),
        dict(titre='Bulletin officiel n° 14 du 2 avril 2026 (PDF)',url='https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2014%20du%202%20avril%202026-515432.pdf',application='programme et automatismes de Première et de Seconde'),
        dict(titre="Définition de l'épreuve anticipée",url='https://www.education.gouv.fr/bo/2026/Special4/MENE2622640N',application='année scolaire 2026-2027, baccalauréat session 2028'),
        dict(titre='Bulletin officiel spécial n° 4 du 17 septembre 2026 (PDF)',url='https://www.education.gouv.fr/sites/default/files/document/20260917boenjsspe4pdf-520753.pdf',application="note de service de l'épreuve et annexe des attendus rédactionnels"),
        dict(titre='Ressources Éduscol',url='https://eduscol.education.gouv.fr/5688/epreuve-anticipee-de-mathematiques-aux-baccalaureats-general-et-technologique')],
    consultation='2026-10-23')
(R/'edition-france-manifeste.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ('exercices_total','defis','sujets_blancs')}))
