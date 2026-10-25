"""Scripts par blocs : une syntaxe restreinte, affichée et exécutable pour contrôle."""
SCRIPTS={
'script-01':[('set','x',3),('add','x',5),('mul','x',2),('say','x')],
'script-02':[('input','x'),('add','x',4),('mul','x',3),('say','x')],
'script-03':[('set','x',0),('repeat',4,[('add','x',3)]),('say','x')],
'script-04':[('input','x'),('if','x>=10',[('saytext','grand')],[('saytext','petit')])],
'script-05':[('set','x',2),('repeat',3,[('mul','x',2)]),('say','x')],
'script-06':[('set','s',0),('set','n',1),('repeat',5,[('addvar','s','n'),('add','n',1)]),('say','s')],
'script-07':[('set','x',0),('until','x>=20',[('add','x',6)]),('say','x')],
'script-08':[('repeat',4,[('move',40),('turn',90)])],
'script-09':[('input','x'),('set','y',0),('if','x%3==0',[('set','y',1)],[]),('say','y')],
'script-10':[('set','n',12),('set','d',1),('repeat',12,[('if','n%d==0',[('say','d')],[]),('add','d',1)])],
'script-11':[('set','x',1),('until','x>50',[('mul','x',2)]),('say','x')],
}

def executer(commandes,entrees=()):
    env={}; sorties=[]; input_iter=iter(entrees); moves=[];angle=0;pos=[0.,0.]; compteur=0
    import math
    def bloc(cmds):
        nonlocal angle,compteur
        for c in cmds:
            compteur+=1
            assert compteur<10000,'Boucle non terminée'
            op=c[0]
            if op=='set':env[c[1]]=c[2]
            elif op=='input':env[c[1]]=next(input_iter)
            elif op=='add':env[c[1]]+=c[2]
            elif op=='mul':env[c[1]]*=c[2]
            elif op=='addvar':env[c[1]]+=env[c[2]]
            elif op=='say':sorties.append(env[c[1]])
            elif op=='saytext':sorties.append(c[1])
            elif op=='repeat':
                for _ in range(c[1]):bloc(c[2])
            elif op=='until':
                while not eval(c[1],{'__builtins__':{}},env):bloc(c[2])
            elif op=='if':bloc(c[2] if eval(c[1],{'__builtins__':{}},env) else c[3])
            elif op=='move':
                pos[0]+=c[1]*math.cos(math.radians(angle));pos[1]+=c[1]*math.sin(math.radians(angle));moves.append(tuple(pos))
            elif op=='turn':angle+=c[1]
            else:raise ValueError(op)
    bloc(commandes)
    return env,sorties,pos,angle

def verifier_scripts():
    tests=[('script-01',[],[16]),('script-02',[2],[18]),('script-02',[-4],[0]),
      ('script-03',[],[12]),('script-04',[9],['petit']),('script-04',[10],['grand']),
      ('script-05',[],[16]),('script-06',[],[15]),('script-07',[],[24]),
      ('script-09',[18],[1]),('script-09',[19],[0]),('script-10',[],[1,2,3,4,6,12]),('script-11',[],[64])]
    for nom,inp,out in tests:assert executer(SCRIPTS[nom],inp)[1]==out,nom
    _,_,p,a=executer(SCRIPTS['script-08'])
    assert max(abs(v) for v in p)<1e-9 and a==360
    return len(tests)+1
