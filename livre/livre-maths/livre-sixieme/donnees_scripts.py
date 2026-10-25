"""Programmes de calcul et déplacements de Sixième, avec répétitions et tests d'exécution."""
from fractions import Fraction
# Instructions : entrée, calcul, sortie, avancer, tourner d'un quart de tour, répéter.
SCRIPTS={
'cours-blocs':[('input',),('calc','r*3'),('calc','r+4'),('output',)],
'ins-2':[('input',),('calc','r*2'),('calc','r-3'),('calc','r*10'),('output',)],
'ins-4':[('move',3),('turn','gauche'),('move',2),('turn','droite'),('move',2)],
'ins-6':[('repeat',3,[('move',2),('turn','droite')])],
'ins-7':[('repeat',4,[('move',2),('turn','gauche')])],
'ins-8':[('move',2),('turn','gauche'),('move',3),('turn','droite'),('move',3)],
'ins-10':[('repeat',4,[('move',1),('turn','gauche'),('move',1),('turn','droite')])],
'ins-11':[('move',2),('turn','gauche'),('move',3),('turn','droite'),('move',4),('turn','droite'),('move',1)],
'ins-14':[('repeat',3,[('move',4),('turn','gauche')])],
'ins-15':[('repeat',5,[('move',1),('turn','gauche'),('move',1),('turn','droite')])],
'cours-chemin':[('repeat',4,[('move',3),('turn','gauche')])],
}
DIRS={'E':(1,0),'N':(0,1),'O':(-1,0),'S':(0,-1)}
ORDRE=['E','N','O','S']
def executer(code,entree=0,state=None):
    if state is None:
        state={'r':Fraction(str(entree)),'x':0,'y':0,'cap':'E','sorties':[],'trace':[(0,0)]}
    for inst in code:
        op=inst[0]
        if op=='calc':
            state['r']=eval(inst[1],{'__builtins__':{}},{'r':state['r']})
        if op=='output':state['sorties'].append(state['r'])
        if op=='move':
            dx,dy=DIRS[state['cap']]
            for _ in range(inst[1]):
                state['x']+=dx;state['y']+=dy
                state['trace'].append((state['x'],state['y']))
        if op=='turn':
            i=ORDRE.index(state['cap'])
            state['cap']=ORDRE[(i+1)%4] if inst[1]=='gauche' else ORDRE[(i-1)%4]
        if op=='repeat':
            for _ in range(inst[1]):executer(inst[2],state=state)
    return state
def lignes(code,depth=0):
    out=[]
    for inst in code:
        op=inst[0]
        if op=='input':out.append((depth,'demander un nombre (entrée)','entree'))
        if op=='output':out.append((depth,'afficher le résultat (sortie)','evenement'))
        if op=='calc':
            expr=inst[1]
            if '+' in expr:txt='ajouter '+expr.split('+')[1]
            elif '-' in expr:txt='retirer '+expr.split('-')[1]
            else:txt='multiplier par '+expr.split('*')[1]
            out.append((depth,txt,'calcul'))
        if op=='move':out.append((depth,f"avancer de {inst[1]} case"+('s' if inst[1]>1 else ''),'mouvement'))
        if op=='turn':out.append((depth,f"tourner d'un quart de tour à {inst[1]}",'mouvement'))
        if op=='repeat':
            out.append((depth,f'répéter {inst[1]} fois','controle'))
            out+=lignes(inst[2],depth+1)
    return out
def verifier_scripts():
    n=0
    for nom,code in SCRIPTS.items():
        s=executer(code,6)
        assert lignes(code),nom
        assert len(set(s['trace']))==len(s['trace']) or nom in ('ins-7','cours-chemin'),nom
        n+=1
    assert executer(SCRIPTS['cours-blocs'],5)['sorties']==[19]
    assert executer(SCRIPTS['ins-2'],7)['sorties']==[110]
    assert executer(SCRIPTS['ins-4'])['trace'][-1]==(5,2)
    s=executer(SCRIPTS['ins-6']);assert s['trace'][-1]==(0,-2) and s['cap']=='N'
    s=executer(SCRIPTS['ins-7']);assert s['trace'][-1]==(0,0) and s['cap']=='E'
    assert executer(SCRIPTS['ins-8'])['trace'][-1]==(5,3)
    s=executer(SCRIPTS['ins-10']);assert s['trace'][-1]==(4,4) and s['cap']=='E'
    assert executer(SCRIPTS['ins-11'])['trace'][-1]==(6,2)
    s=executer(SCRIPTS['ins-14']);assert s['trace'][-1]==(0,4) and s['trace'][0]!=s['trace'][-1]
    s=executer(SCRIPTS['ins-15']);assert s['trace'][-1]==(5,5) and len(s['trace'])-1==10
    s=executer(SCRIPTS['cours-chemin']);assert s['trace'][-1]==(0,0)
    return n
if __name__=='__main__':print(verifier_scripts())
