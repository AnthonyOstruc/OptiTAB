"""Programmes de calcul et déplacements codés du CM1, avec tests d'exécution."""
from fractions import Fraction
# Programmes de calcul : une entrée lue, au plus deux transformations (CM1).
# Déplacements : cases d'un quadrillage, quarts de tour (vocabulaire spatial).
SCRIPTS={
1:[('input',),('calc','r+2'),('calc','r*4')],
2:[('input',),('calc','r*3'),('calc','r+5')],
3:[('input',),('calc','r*10')],
4:[('input',),('calc','r-4'),('calc','r*2')],
5:[('input',),('calc','r*5'),('calc','r-3')],
6:[('input',),('calc','r+8'),('calc','r+8')],
7:[('move',2),('turn','droite'),('move',3)],
8:[('move',1),('turn','gauche'),('move',2),('turn','droite'),('move',2)],
9:[('move',3),('turn','droite'),('move',1),('turn','droite'),('move',3)],
10:[('move',2),('turn','gauche'),('move',2),('turn','gauche'),('move',1)],
}
DIRS={'E':(1,0),'N':(0,1),'O':(-1,0),'S':(0,-1)}
ORDRE=['E','N','O','S']
def executer(code,entree=0):
    state={'r':Fraction(str(entree)),'x':0,'y':0,'cap':'E','sorties':[],'trace':[(0,0)]}
    for inst in code:
        op=inst[0]
        if op=='input':continue
        if op=='calc':
            state['r']=eval(inst[1],{'__builtins__':{}},{'r':state['r']})
            state['sorties'].append(state['r'])
        if op=='move':
            dx,dy=DIRS[state['cap']]
            state['x']+=dx*inst[1];state['y']+=dy*inst[1]
            state['trace'].append((state['x'],state['y']))
        if op=='turn':
            i=ORDRE.index(state['cap'])
            state['cap']=ORDRE[(i+1)%4] if inst[1]=='gauche' else ORDRE[(i-1)%4]
    return state
def lignes(code,depth=0):
    out=[]
    for inst in code:
        op=inst[0]
        if op=='input':out.append((depth,'choisir un nombre ; le noter','entree'))
        if op=='calc':
            expr=inst[1]
            if '+' in expr:txt='ajouter '+expr.split('+')[1]
            elif '-' in expr:txt='retirer '+expr.split('-')[1]
            else:txt='multiplier par '+expr.split('*')[1]
            out.append((depth,txt,'calcul'))
        if op=='move':out.append((depth,f"avancer de {inst[1]} case"+('s' if inst[1]>1 else ''),'mouvement'))
        if op=='turn':out.append((depth,f"pivoter d'un quart de tour à {inst[1]}",'mouvement'))
    return out
def verifier_scripts():
    n=0
    for num,code in SCRIPTS.items():
        s=executer(code,6)
        if any(i[0]=='calc' for i in code):assert s['sorties'],num
        if any(i[0]=='move' for i in code):assert len(s['trace'])>1,num
        assert lignes(code),num
        n+=1
    assert executer(SCRIPTS[1],6)['sorties'][-1]==32
    assert executer(SCRIPTS[2],6)['sorties'][-1]==23
    assert executer(SCRIPTS[3],7)['sorties'][-1]==70
    assert executer(SCRIPTS[4],9)['sorties'][-1]==10
    assert executer(SCRIPTS[5],8)['sorties'][-1]==37
    assert executer(SCRIPTS[6],4)['sorties'][-1]==20
    assert executer(SCRIPTS[9])['trace'][-1]==(0,-1)
    assert executer(SCRIPTS[10])['trace'][-1]==(1,2)
    return n
if __name__=='__main__':print(verifier_scripts())
