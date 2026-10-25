"""Programmes utilisés pour les blocs, les tracés et les tests d'exécution."""
from math import sin,cos,radians
from fractions import Fraction
# Une donnée d'entrée est seulement lue ; pas de variable d'accumulation.
SCRIPTS={
1:[('input',),('say','r+5')],
2:[('input',),('say','3*r+2')],
3:[('input',),('say','3*(r+2)')],
4:[('input',),('say','r*r')],
5:[('move',30),('move',50)],
6:[('input',),('say','2*r+4')],
7:[('repeat',4,[('move',50),('turn',90)])],
8:[('repeat',2,[('move',80),('turn',90),('move',40),('turn',90)])],
9:[('repeat',3,[('move',60),('turn',120)])],
10:[('move',40),('turn',90)],
11:[('repeat',5,[('move',40),('turn',72)])],
12:[('repeat',3,[('move',30),('turn',90),('move',20),('turn',-90)])],
13:[('repeat',3,[('move',50),('turn',90)])],
14:[('input',),('say','r*r*r')],
15:[('input',),('say','4*r')],
}
def executer(code,entree=0):
    state={'r':Fraction(str(entree)),'x':0.,'y':0.,'angle':0.,'sorties':[],'trace':[(0.,0.)]}
    def run(seq):
        for inst in seq:
            op=inst[0]
            if op=='input':continue
            if op=='say':state['sorties'].append(eval(inst[1],{'__builtins__':{}},{'r':state['r']}))
            if op=='move':
                state['x']+=inst[1]*cos(radians(state['angle']))
                state['y']+=inst[1]*sin(radians(state['angle']))
                state['trace'].append((state['x'],state['y']))
            if op=='turn':state['angle']+=inst[1]
            if op=='repeat':
                for _ in range(inst[1]):run(inst[2])
    run(code);return state
def lignes(code,depth=0):
    out=[]
    for inst in code:
        op=inst[0]
        if op=='input':out.append((depth,'demander un nombre ; lire la réponse','entree'))
        if op=='say':
            expr=inst[1].replace('r','réponse').replace('*',r' $\times$ ')
            out.append((depth,'dire ('+expr+')','calcul'))
        if op=='move':out.append((depth,f'avancer de {inst[1]} pas','mouvement'))
        if op=='turn':out.append((depth,f'tourner à {"gauche" if inst[1]>0 else "droite"} de {abs(inst[1])} degrés','mouvement'))
        if op=='repeat':
            out.append((depth,f'répéter {inst[1]} fois','controle'))
            out.extend(lignes(inst[2],depth+1));out.append((depth,'fin de répéter','controle'))
    return out
def verifier_scripts():
    tests=0
    for i,entree,attendu in [(1,7,12),(2,4,14),(3,4,18),(4,5,25),(6,6,16),(14,2,8),(14,3,27),(15,'2.5',10),(15,0,0)]:
        assert executer(SCRIPTS[i],entree)['sorties']==[attendu];tests+=1
    for i,x,y in [(5,80,0),(7,0,0),(8,0,0),(9,0,0),(10,40,0),(11,0,0),(12,90,60),(13,0,50)]:
        s=executer(SCRIPTS[i]);assert abs(s['x']-x)<1e-8 and abs(s['y']-y)<1e-8,(i,s);tests+=1
    mod=[('input',),('say','3*r+4')]
    assert executer(mod,6)['sorties']==[22];tests+=1
    assert executer([('turn',90),('move',40)])['trace'][-1]!=(40.,0.);tests+=1
    assert abs(executer([('repeat',4,[('move',50),('turn',90)])])['y'])<1e-8;tests+=1
    return tests
