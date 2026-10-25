"""Données des schémas ; coordonnées de dessin sans inférence sur les hypothèses."""
SCHEMAS={}
def schema(nom,points,segments,labels=(),droits=(),extra='',solution=''):
    assert nom not in SCHEMAS,nom
    SCHEMAS[nom]=dict(points=points,segments=segments,labels=labels,droits=droits,extra=extra,solution=solution)
    return nom

def triangle(nom,cotes=('AB','AC','BC'),valeurs=('','',''),droit=True):
    return schema(nom,{'A':(0,0),'B':(5,0),'C':(0,3)},[('A','B'),('B','C'),('C','A')],
      [(a,b,v) for (a,b),v in zip([tuple(c) for c in cotes],valeurs) if v],['A'] if droit else [])
