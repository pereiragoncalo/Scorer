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
        self.cloth=cloth;self.triangles={};self.references={}
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
                        triangles.append(indices);self.references[indices]=reference
            self.triangles[surface]=triangles
        self.candidates=None;self.previous_positions=None;self.refresh()
    def refresh(self,previous=None):
        self.previous_positions=previous
        positions=self.cloth.positions;self.bounds={}
        for surface,triangles in self.triangles.items():
            bounds=[]
            for ia,ib,ic in triangles:
                a,b,c=positions[ia],positions[ib],positions[ic]
                bounds.append((min(a[0],b[0],c[0])-.25,max(a[0],b[0],c[0])+.25,
                               min(a[1],b[1],c[1])-.25,max(a[1],b[1],c[1])+.25,
                               min(a[2],b[2],c[2])-.25,max(a[2],b[2],c[2])+.25))
            if previous is not None:
                for j,(ia,ib,ic) in enumerate(triangles):
                    a,b,c=previous[ia],previous[ib],previous[ic];row=bounds[j]
                    bounds[j]=(min(row[0],a[0]-.25,b[0]-.25,c[0]-.25),max(row[1],a[0]+.25,b[0]+.25,c[0]+.25),
                               min(row[2],a[1]-.25,b[1]-.25,c[1]-.25),max(row[3],a[1]+.25,b[1]+.25,c[1]+.25),
                               min(row[4],a[2]-.25,b[2]-.25,c[2]-.25),max(row[5],a[2]+.25,b[2]+.25,c[2]+.25))
            self.bounds[surface]=bounds
    def select(self,start,end,radius):
        lo=[min(start[a],end[a])-radius for a in range(3)];hi=[max(start[a],end[a])+radius for a in range(3)]
        self.candidates={s:[(ids,b)for ids,b in zip(self.triangles[s],self.bounds[s])if lo[0]<=b[1] and hi[0]>=b[0] and lo[1]<=b[3] and hi[1]>=b[2] and lo[2]<=b[5] and hi[2]>=b[4]]for s in self.triangles}
    def query(self,surface,end,radius,start=None):
        moving=start is not None and self.previous_positions is not None
        start=end if start is None else start
        lo=[min(start[a],end[a])-radius for a in range(3)];hi=[max(start[a],end[a])+radius for a in range(3)]
        travel=sub(end,start);length=math.dist(start,end);best=None
        candidates=self.candidates[surface] if self.candidates is not None else zip(self.triangles[surface],self.bounds[surface])
        for ids,bounds in candidates:
            if lo[0]>bounds[1] or hi[0]<bounds[0] or lo[1]>bounds[3] or hi[1]<bounds[2] or lo[2]>bounds[5] or hi[2]<bounds[4]:continue
            final=[self.cloth.positions[k] for k in ids]
            initial=[self.previous_positions[k] for k in ids] if moving else final
            movement=[sub(b,a)for a,b in zip(initial,final)]
            limit=length+max((math.dist(a,b)for a,b in zip(initial,final)),default=0.)
            t=0. if length>1e-12 or moving else 1.
            for _ in range(32):
                points=[mix(a,b,t) for a,b in zip(initial,final)] if moving else final
                centre=mix(start,end,t);point,bary=closest(centre,*points);distance=math.dist(centre,point)
                if distance<=radius+1e-7:break
                if limit<1e-12:t=2.;break
                t+=(distance-radius)/limit
                if t>1.+1e-8:break
            if t>1.+1e-8 or distance>radius+1e-6:continue
            n=normal(*points)
            if dot(n,self.references[ids])<0:n=tuple(-x for x in n)
            relative=tuple(travel[a]-sum(movement[j][a]*bary[j]for j in range(3))for a in range(3))
            if (length>1e-12 or moving) and dot(relative,n)<=1e-12:continue
            signed=dot(sub(centre,point),n)
            hit=dict(surface=surface,t=min(1.,t),centre=centre,point=point,normal=n,weights=tuple((k,w)for k,w in zip(ids,bary)if w>1e-10),gap=max(0.,radius+signed))
            if best is None or hit['t']<best['t']-1e-8 or abs(hit['t']-best['t'])<1e-8 and hit['gap']>best['gap']:best=hit
        return best
    def first(self,start,end,radius):
        hits=[h for s in self.triangles if (h:=self.query(s,end,radius,start))is not None]
        return min(hits,key=lambda h:h['t']) if hits else None

    def inside(self,position):
        """Parity through the actual folded cloth and the open goal-mouth cap.

        The cap only classifies containment: it is never a collision wall.
        A horizontal ray needs no ground cap because the sphere stays above turf.
        """
        x,y,z=position;x+=1.17e-8;z+=3.31e-8
        hits=[]
        g=self.cloth.geometry
        if -g.width/2<x<g.width/2 and 0<z<g.height and y<0:hits.append(0.)
        for surface,triangles in self.triangles.items():
            for ids,b in zip(triangles,self.bounds[surface]):
                if x<b[0] or x>b[1] or z<b[4] or z>b[5] or b[3]<y:continue
                a,b,c=(self.cloth.positions[i]for i in ids)
                denominator=(b[2]-c[2])*(a[0]-c[0])+(c[0]-b[0])*(a[2]-c[2])
                if abs(denominator)<1e-12:continue
                u=((b[2]-c[2])*(x-c[0])+(c[0]-b[0])*(z-c[2]))/denominator
                v=((c[2]-a[2])*(x-c[0])+(a[0]-c[0])*(z-c[2]))/denominator
                if u< -1e-9 or v< -1e-9 or u+v>1+1e-9:continue
                height=a[1]*u+b[1]*v+c[1]*(1-u-v)
                if height>y+1e-7:hits.append(height)
        hits.sort();unique=[]
        for value in hits:
            if not unique or value-unique[-1]>1e-6:unique.append(value)
        return bool(len(unique)%2)

    def escaped_contact(self,position,radius):
        """Recover an exterior centre against its nearest finite sheet face."""
        if position[1]>0:return None
        rounded=self.cloth.geometry.structure=='rounded'
        if rounded and self.inside(position):return None
        best=None;distance=float('inf')
        for surface,triangles in self.triangles.items():
            for ids,bounds in zip(triangles,self.bounds[surface]):
                dx=max(bounds[0]+.25-position[0],0.,position[0]-bounds[1]+.25)
                dy=max(bounds[2]+.25-position[1],0.,position[1]-bounds[3]+.25)
                dz=max(bounds[4]+.25-position[2],0.,position[2]-bounds[5]+.25)
                if dx*dx+dy*dy+dz*dz>distance*distance:continue
                points=[self.cloth.positions[i]for i in ids];point,bary=closest(position,*points);d=math.dist(position,point)
                if d>=distance:continue
                n=normal(*points)
                if dot(n,self.references[ids])<0:n=tuple(-x for x in n)
                distance=d;best=dict(surface=surface,point=point,normal=n,weights=tuple(zip(ids,bary)),gap=radius+dot(sub(position,point),n))
        if best is None:return None
        if not rounded:return best if best['gap']>radius+1e-6 else None
        # A loose panel can fold past its original outward normal. Select the
        # side that really lies inside the current mesh, not its rest orientation.
        q,n=best['point'],best['normal']
        for sign in (1.,-1.):
            candidate=tuple(q[a]-sign*n[a]*radius for a in range(3))
            candidate=(candidate[0],candidate[1],max(radius,candidate[2]))
            if self.inside(candidate):
                best['normal']=tuple(sign*x for x in n);best['recovered_position']=candidate;return best
        # At a folded seam, bracket the true boundary from a confirmed interior
        # point near the mouth. This still follows the finite deforming sheet.
        g=self.cloth.geometry
        core=next((p for p in ((0.,-.02,min(g.height*.5,max(radius,position[2]))),(-g.width*.2,-.02,g.height*.4),(g.width*.2,-.02,g.height*.4))if self.inside(p)),None)
        if core is None:return None
        lo,hi=0.,1.
        for _ in range(24):
            middle=(lo+hi)/2
            if self.inside(mix(core,position,middle)):lo=middle
            else:hi=middle
        point=mix(core,position,lo);direction=sub(position,core);length=math.sqrt(dot(direction,direction))
        n=tuple(x/max(1e-9,length)for x in direction)
        best['normal']=n;best['recovered_position']=tuple(point[a]-n[a]*radius for a in range(3))
        return best
