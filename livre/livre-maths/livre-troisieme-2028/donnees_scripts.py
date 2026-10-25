"""Scripts par blocs : une syntaxe restreinte, affichée et exécutable pour contrôle."""
import random

SCRIPTS={
'script-01':[('set','x',3),('add','x',5),('mul','x',2),('say','x')],
'script-02':[('input','x'),('add','x',4),('mul','x',3),('say','x')],
'script-03':[('set','x',0),('repeat',4,[('add','x',3)]),('say','x')],
'script-04':[('input','x'),('if','x>=10',[('saytext','grand')],[('saytext','petit')])],
'script-05':[('set','x',2),('repeat',3,[('mul','x',2)]),('say','x')],
'script-06':[('set','s',0),('set','n',1),('repeat',5,[('addvar','s','n'),('add','n',1)]),('say','s')],
'script-07':[('set','x',0),('until','x>=20',[('add','x',6)]),('say','x')],
'script-08':[('input','x'),('if','x>=10 and x<=20',[('saytext','dans la plage')],[('saytext','hors de la plage')])],
'script-09':[('set','n',12),('set','d',1),('repeat',12,[('if','n%d==0',[('say','d')],[]),('add','d',1)])],
'script-10':[('input','a'),('input','b'),('set','r','a'),('set','q',0),('until','r<b',[('subvar','r','b'),('add','q',1)]),('say','q'),('say','r')],
'script-11':[('set','x',1),('until','x>50',[('mul','x',2)]),('say','x')],
}

# Scripts affichés avec des valeurs à compléter, exécutés ici sous forme complète.
SIMULATION_DE=[('set','succes',0),('repeat',600,[('random','de',1,6),('if','de==6',[('add','succes',1)],[])]),('say','succes')]
SIMULATION_DEUX_DES=[('set','succes',0),('repeat',1000,[('random','d1',1,6),('random','d2',1,6),('if','d1==6 or d2==6',[('add','succes',1)],[])]),('say','succes')]
POLYGONES=[('set','n',3),('until','n>6',[('poly','n',30),('add','n',1)])]
BREVET_B=[('set','c',10),('until','c>25',[('carre','c'),('up',),('movevar','c',5),('down',),('add','c',5)]),('say','c')]

def executer(commandes,entrees=(),graine=2028):
    env={}; sorties=[]; input_iter=iter(entrees); traces=[]; angle=0; pos=[0.,0.]; compteur=0; stylo=[True]
    hasard=random.Random(graine)
    import math
    def avancer(d):
        pos[0]+=d*math.cos(math.radians(angle)); pos[1]+=d*math.sin(math.radians(angle))
        traces.append((stylo[0],d))
    def bloc(cmds):
        nonlocal angle,compteur
        for c in cmds:
            compteur+=1
            assert compteur<200000,'Boucle non terminée'
            op=c[0]
            if op=='set':env[c[1]]=env[c[2]] if isinstance(c[2],str) else c[2]
            elif op=='input':env[c[1]]=next(input_iter)
            elif op=='add':env[c[1]]+=c[2]
            elif op=='mul':env[c[1]]*=c[2]
            elif op=='addvar':env[c[1]]+=env[c[2]]
            elif op=='subvar':env[c[1]]-=env[c[2]]
            elif op=='random':env[c[1]]=hasard.randint(c[2],c[3])
            elif op=='say':sorties.append(env[c[1]])
            elif op=='saytext':sorties.append(c[1])
            elif op=='repeat':
                for _ in range(c[1]):bloc(c[2])
            elif op=='until':
                while not eval(c[1],{'__builtins__':{}},env):bloc(c[2])
            elif op=='if':bloc(c[2] if eval(c[1],{'__builtins__':{}},env) else c[3])
            elif op=='move':avancer(c[1])
            elif op=='movevar':avancer(env[c[1]]+c[2])
            elif op=='turn':angle+=c[1]
            elif op=='up':stylo[0]=False
            elif op=='down':stylo[0]=True
            elif op=='poly':
                k=env[c[1]]
                for _ in range(k):avancer(c[2]);angle+=360/k
            elif op=='carre':
                for _ in range(4):avancer(env[c[1]]);angle+=90
            else:raise ValueError(op)
    bloc(commandes)
    return env,sorties,pos,angle,traces

def verifier_scripts():
    tests=[('script-01',[],[16]),('script-02',[2],[18]),('script-02',[-4],[0]),
      ('script-03',[],[12]),('script-04',[9],['petit']),('script-04',[10],['grand']),
      ('script-05',[],[16]),('script-06',[],[15]),('script-07',[],[24]),
      ('script-08',[9],['hors de la plage']),('script-08',[10],['dans la plage']),
      ('script-08',[20],['dans la plage']),('script-08',[21],['hors de la plage']),
      ('script-09',[],[1,2,3,4,6,12]),('script-10',[23,5],[4,3]),('script-10',[12,4],[3,0]),
      ('script-10',[3,5],[0,3]),('script-11',[],[64])]
    for nom,inp,out in tests:assert executer(SCRIPTS[nom],inp)[1]==out,nom
    n=len(tests)
    # Simulations : fréquences plausibles pour une graine fixée (tests de cohérence, pas de preuve).
    f=executer(SIMULATION_DE)[1][0]/600; assert abs(f-1/6)<0.05,f; n+=1
    f=executer(SIMULATION_DEUX_DES)[1][0]/1000; assert abs(f-11/36)<0.05,f; n+=1
    # Polygones : retour au point de départ et longueur tracée.
    env,_,p,a,tr=executer(POLYGONES)
    assert max(abs(v) for v in p)<1e-9 and env['n']==7 and sum(d for s,d in tr if s)==30*(3+4+5+6); n+=1
    # Sujet B : côtés successifs, longueur tracée et déplacements stylo relevé.
    env,s,p,a,tr=executer(BREVET_B)
    dessin=[d for st,d in tr if st]; saut=[d for st,d in tr if not st]
    assert s==[30] and sum(dessin)==4*(10+15+20+25) and saut==[15,20,25,30]; n+=1
    return n
