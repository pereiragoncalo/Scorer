"""Visible strands clipped to the complete finite cloth panel, including seams."""
from functools import lru_cache
import math
from bisect import bisect_right
from goal_nets import lattice

@lru_cache(maxsize=128)
def panel_strands(g,surface,mesh,cell,path):
    width=g.width if surface=='back' else g.depth
    height=g.path if surface=='back' else g.height
    result=[]
    # Render against the same polygonal edge as the coarse physical cloth.
    # Clipping against the analytic curve leaves an unmeshed strip between
    # that curve and the physical boundary chords, especially at rounded corners.
    profile=tuple(g.profile(u)for u in path)
    depths=tuple(-p[0]for p in profile)
    @lru_cache(maxsize=None)
    def side_point(p):
        x,z=p
        i=max(0,min(len(path)-2,bisect_right(depths,x)-1))
        t=max(0.,min(1.,(x-depths[i])/max(1e-12,depths[i+1]-depths[i])))
        u=path[i]+(path[i+1]-path[i])*t
        top=profile[i][1]+(profile[i+1][1]-profile[i][1])*t
        return u,top-z,max(0.,min(1.,z/top)) if top>1e-8 else 0.
    def uv(p):
        if surface=='back':return p[0]/width,p[1]/height
        if g.structure=='box':return p[0]/g.depth,p[1]/g.height
        u,_,v=side_point(p);return u,v
    def clipped(a,b,level=0):
        if surface=='back' or g.structure=='box':return [(a,b)]
        ca,cb=side_point(a)[1],side_point(b)[1]
        if ca < -1e-8 and cb < -1e-8:return []
        mid=tuple((x+y)*.5 for x,y in zip(a,b))
        if ca>=-1e-8 and cb>=-1e-8:
            # A curved roof may dip below a chord whose endpoints are inside.
            if level<8 and side_point(mid)[1]<-1e-8:return clipped(a,mid,level+1)+clipped(mid,b,level+1)
            return [(a,b)]
        inside,outside=(a,b) if ca>=-1e-8 else (b,a)
        for _ in range(28):
            mid=tuple((x+y)*.5 for x,y in zip(inside,outside))
            if side_point(mid)[1]>=0:inside=mid
            else:outside=mid
        return [(a,inside)] if ca>=-1e-8 else [(inside,b)]
    for a,b in lattice(width,height,mesh,cell):
        steps=max(1,math.ceil(math.dist(a,b)/.16))
        for i in range(steps):
            aa=tuple(a[j]+(b[j]-a[j])*i/steps for j in (0,1))
            bb=tuple(a[j]+(b[j]-a[j])*(i+1)/steps for j in (0,1))
            for left,right in clipped(aa,bb):
                if math.dist(left,right)>1e-8:result.append((uv(left),uv(right)))
    return tuple(result)


def joining_seams(cloth):
    """Both side/rear joins use the shared physical boundary, not an offset line."""
    path=cloth.grids['back'][1]
    return tuple(((edge,a),(edge,b))for edge in (0.,1.)for a,b in zip(path,path[1:]))
