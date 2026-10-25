def e(title,level,intro,q,a):
    qs=q.strip().split('@@');ans=a.strip().split('@@')
    assert len(qs)==len(ans),(title,len(qs),len(ans))
    return dict(title=title,level=level,intro=intro.strip(),q=[s.strip() for s in qs],a=[s.strip() for s in ans])

def c(title,part,tags,goals,pre,course,ex,deco='courbe'):
    assert len(ex)==12,(title,len(ex))
    return dict(title=title,part=part,tags=tags,goals=goals.split('@@'),pre=pre,course=course,ex=ex,deco=deco)
