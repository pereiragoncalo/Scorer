"""Finite, welded cloth triangles: sphere contact and swept face/edge tests."""
import math

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mix(a,b,t):return tuple(x+(y-x)*t for x,y in zip(a,b))
def closest(p,a,b,c):
    ab,ac,ap=sub(b,a),sub(c,a),sub(p,a);d1,d2=dot(ab,ap),dot(ac,ap)
    if d1<=0 and d2<=0:return a,(1.,0.,0.)
    bp=sub(p,b);d3,d4=dot(ab,bp),dot(ac,bp)
    if d3>=0 and d4<=d3:return b,(0.,1.,0.)
    vc=d1*d4-d3*d2
    if vc<=0 and d1>=0 and d3<=0:
        v=d1/max(1e-20,d1-d3);return mix(a,b,v),(1-v,v,0.)
    cp=sub(p,c);d5,d6=dot(ab,cp),dot(ac,cp)
    if d6>=0 and d5<=d6:return c,(0.,0.,1.)
    vb=d5*d2-d1*d6
    if vb<=0 and d2>=0 and d6<=0:
        w=d2/max(1e-20,d2-d6);return mix(a,c,w),(1-w,0.,w)
    va=d3*d6-d5*d4
    if va<=0 and d4-d3>=0 and d5-d6>=0:
        w=(d4-d3)/max(1e-20,d4-d3+d5-d6);return mix(b,c,w),(0.,1-w,w)
    denom=va+vb+vc
    if abs(denom)<1e-20:return a,(1.,0.,0.)
    v,w=vb/denom,vc/denom
    return tuple(a[i]+ab[i]*v+ac[i]*w for i in range(3)),(1-v-w,v,w)

def normal(a,b,c):
    u,v=sub(b,a),sub(c,a)
    n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);length=math.sqrt(dot(n,n))
    return tuple(x/max(1e-20,length) for x in n)

class ClothContacts:
    def __init__(self,cloth):
        self.cloth=cloth;self.triangles={}
        for surface,(us,vs,grid) in cloth.grids.items():
            triangles=[]
            for j in range(len(vs)-1):
                for i in range(len(us)-1):
                    for indices in ((grid[j][i],grid[j][i+1],grid[j+1][i]),(grid[j+1][i],grid[j][i+1],grid[j+1][i+1])):
                        points=[cloth.rest[k] for k in indices]
                        # The turf hem is ground, never an infinite roof above the ball.
                        if all(p[2]<1e-7 for p in points):continue
                        reference=cloth.geometry.normal(surface,(us[i]+us[i+1])/2,(vs[j]+vs[j+1])/2)
                        if dot(normal(*points),reference)<0:indices=(indices[0],indices[2],indices[1])
                        triangles.append(indices)
            self.triangles[surface]=triangles
        self.candidates=None;self.refresh()
    def refresh(self):
        self.bounds={s:[tuple((min(self.cloth.positions[k][a] for k in ids)-.25,max(self.cloth.positions[k][a] for k in ids)+.25)for a in range(3))for ids in tris]for s,tris in self.triangles.items()}
    def select(self,start,end,radius):
        lo=[min(start[a],end[a])-radius for a in range(3)];hi=[max(start[a],end[a])+radius for a in range(3)]
        self.candidates={s:[(ids,b)for ids,b in zip(self.triangles[s],self.bounds[s])if all(lo[a]<=b[a][1] and hi[a]>=b[a][0]for a in range(3))]for s in self.triangles}
    def query(self,surface,end,radius,start=None):
        start=end if start is None else start
        lo=[min(start[a],end[a])-radius for a in range(3)];hi=[max(start[a],end[a])+radius for a in range(3)]
        length=math.dist(start,end);best=None
        candidates=self.candidates[surface] if self.candidates is not None else zip(self.triangles[surface],self.bounds[surface])
        for ids,bounds in candidates:
            if any(lo[a]>bounds[a][1] or hi[a]<bounds[a][0] for a in range(3)):continue
            points=[self.cloth.positions[k] for k in ids];n=normal(*points)
            if length>1e-12 and dot(sub(end,start),n)<=1e-12:continue
            t=0. if length>1e-12 else 1.
            for _ in range(18):
                centre=mix(start,end,t);point,bary=closest(centre,*points);distance=math.dist(centre,point)
                if distance<=radius+1e-7:break
                if length<1e-12:t=2.;break
                t+=(distance-radius)/length
                if t>1.+1e-8:break
            if t>1.+1e-8 or distance>radius+1e-6:continue
            signed=dot(sub(centre,point),n)
            # A separating sphere on the inner face is handled by the impulse solver.
            hit=dict(surface=surface,t=min(1.,t),centre=centre,normal=n,weights=tuple((k,w)for k,w in zip(ids,bary)if w>1e-10),gap=max(0.,radius+signed))
            if best is None or hit['t']<best['t']-1e-8 or abs(hit['t']-best['t'])<1e-8 and hit['gap']>best['gap']:best=hit
        return best
    def first(self,start,end,radius):
        hits=[h for s in self.triangles if (h:=self.query(s,end,radius,start))is not None]
        return min(hits,key=lambda h:h['t']) if hits else None
