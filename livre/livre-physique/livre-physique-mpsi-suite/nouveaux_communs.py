"""Outils éditoriaux des cinq nouveaux chapitres ; pas de contenu automatique d'exercice."""
from construire import box,qs,sub

def diagnostic(c,items):
    c.diagnostic=qs(*(q for q,a in items))
    c.diag_sol='\n'.join(sub(f'D{i}',a) for i,(q,a) in enumerate(items,1))

def exercices(c,entries):
    assert len(entries)==24
    for i,(title,q,a) in enumerate(entries):
        c.e(title,1 if i<6 else 2 if i<18 else 3,'10 à 15 min' if i<12 else '15 à 25 min',q,a)

def bilan(c,lois,demarches,erreurs):
    c.synthesis=box('loi','Les relations et leurs hypothèses',lois)+sub('Une résolution rédigée',demarches)+box('piege','Erreurs à éviter',erreurs)+box('docu','S’autoévaluer',r'\checkline{Je retrouve les relations à partir du modèle.}\checkline{Je sais interpréter les limites d’une expression.}\checkline{Je peux dessiner et commenter les courbes.}\checkline{Je relie une mesure à la grandeur calculée.}')

TD7='https://mpsi.schleck.ovh/fichiers/td/td7_filtrage_lineaire.pdf'
TD9='https://mpsi.schleck.ovh/fichiers/td/td9_ondes.pdf'
TP12='https://mpsi.schleck.ovh/fichiers/tp/tp12_rlc_rsf.pdf'
DS4='https://mpsi.schleck.ovh/fichiers/devoirs/2025-2026/ds04_enonce.pdf'
DS5='https://mpsi.schleck.ovh/fichiers/devoirs/2025-2026/ds5_molecules_ondes_cinematique.pdf'
DM6='https://mpsi.schleck.ovh/fichiers/devoirs/2025-2026/dm5_ondes_chimie.pdf'
