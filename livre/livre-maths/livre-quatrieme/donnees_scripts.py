"""Une seule source pour l'affichage et l'exécution des scripts numériques."""
SCRIPTS={
'script-01':[('set','x',4),('add','x',3),('mul','x',2),('say','x')],
'script-02':[('input','x'),('add','x',-2),('mul','x',4),('say','x')],
'script-03':[('set','x',0),('repeat',3,[('add','x',5)]),('say','x')],
'script-04':[('input','x'),('if','x>=10',[('saytext','grand')],[('saytext','petit')])],
'script-05':[('set','x',3),('repeat',4,[('mul','x',2)]),('say','x')],
'script-06':[('set','s',0),('set','n',1),('repeat',4,[('addvar','s','n'),('add','n',1)]),('say','s')],
'script-07':[('repeat',4,[('move',30),('turn',90)])],
'script-08':[('repeat',2,[('move',50),('turn',90),('move',20),('turn',90)])],
'script-09':[('input','x'),('if','x%2==0',[('saytext','pair')],[('saytext','impair')])],
'script-10':[('add','score',1)],
'script-11':[('repeat',3,[('move',40),('turn',120)])],
'script-12':[('input','contact'),('if','contact==1',[('saytext','Bonjour !')],[('saytext','Je cherche')])],
'script-13':[('input','c'),('repeat',4,[('movevar','c'),('turn',90)])],
'script-14':[('repeat',4,[('set','s',0),('add','s',3)]),('say','s')],
'script-15':[('input','x'),('setexpr','y','3*x+5'),('if','y>0',[('saytext','positif')],[('saytext','nul ou négatif')])]
}

def executer(cmds,entrees=(),initial=None):
    import math
    env=dict(initial or {});out=[];it=iter(entrees);pos=[0.,0.];angle=0.;trace=[];count=0
    def bloc(commands):
        nonlocal angle,count
        for c in commands:
            count+=1
            assert count<10000
            op=c[0]
            if op=='set':env[c[1]]=c[2]
            elif op=='input':env[c[1]]=next(it)
            elif op=='add':env[c[1]]+=c[2]
            elif op=='mul':env[c[1]]*=c[2]
            elif op=='addvar':env[c[1]]+=env[c[2]]
            elif op=='setexpr':env[c[1]]=eval(c[2],{'__builtins__':{}},env)
            elif op=='say':out.append(env[c[1]])
            elif op=='saytext':out.append(c[1])
            elif op=='repeat':
                for _ in range(c[1]):bloc(c[2])
            elif op=='if':bloc(c[2] if eval(c[1],{'__builtins__':{}},env) else c[3])
            elif op in ['move','movevar']:
                v=c[1] if op=='move' else env[c[1]]
                pos[0]+=v*math.cos(math.radians(angle));pos[1]+=v*math.sin(math.radians(angle));trace.append(v)
            elif op=='turn':angle+=c[1]
            else:raise ValueError(op)
    bloc(cmds)
    return env,out,pos,angle,trace

def verifier_scripts():
    from fractions import Fraction
    tests=[
    ('script-01',[],[14]),('script-02',[5],[12]),('script-02',[2],[0]),
    ('script-03',[],[15]),('script-04',[9],['petit']),('script-04',[10],['grand']),
    ('script-05',[],[48]),('script-06',[],[10]),('script-09',[18],['pair']),
    ('script-09',[19],['impair']),('script-12',[1],['Bonjour !']),('script-12',[0],['Je cherche']),
    ('script-14',[],[3]),('script-15',[2],['positif']),('script-15',[-2],['nul ou négatif']),
    ('script-15',[Fraction(-5,3)],['nul ou négatif'])]
    for name,inp,out in tests:assert executer(SCRIPTS[name],inp)[1]==out,name
    for name,inp,per in [('script-07',[],120),('script-08',[],140),('script-11',[],120),('script-13',[25],100)]:
        _,_,pos,angle,trace=executer(SCRIPTS[name],inp)
        assert max(abs(a) for a in pos)<1e-9 and angle==360 and sum(trace)==per,name
    score=0
    for _ in range(5):score=executer(SCRIPTS['script-10'],initial={'score':score})[0]['score']
    assert score==5
    return len(tests)+5
