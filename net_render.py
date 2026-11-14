"""Reusable Kivy line meshes, shared verbatim by Scorer 1 and the net lab.

No renderer work advances time. Barycentric lookups/topology/graphics objects are
cached; resting geometry is only reprojected on a camera/viewport change.
"""
import math
from kivy.graphics import Color,Mesh,InstructionGroup,Point,Line
from goal_nets import lattice

class NetRenderer:
    def __init__(self,cloth,mesh='square',low_detail=False):
        self.cloth=cloth;self.kind=mesh;self.low_detail=low_detail
        self.group=InstructionGroup();self.front=InstructionGroup()
        self.group.add(Color(.94,.97,.92,.76,noadd=True));self.front.add(Color(.97,.99,.95,.86,noadd=True))
        self.batches=[];self._stamp=None;self._geometry_stamp=None;self._world=[];self.rebuilds=0
        g=cloth.geometry;cell=.28 if low_detail else .20
        for surface in ('back','left','right'):
            width=g.width if surface=='back' else g.depth
            height=g.path if surface=='back' else g.height
            lookup={};weights=[];edges=[]
            for a,b in lattice(width,height,mesh,cell):
                # Subdivide long square strands; short hexagon edges need no
                # extra vertices. Deformations never interpolate corner-to-corner.
                steps=max(1,math.ceil(math.dist(a,b)/.16))
                for i in range(steps):
                    pair=[]
                    for t in (i/steps,(i+1)/steps):
                        x,z=a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t
                        if surface=='back':uv=(x/width,z/height)
                        else:
                            if g.structure=='box':uv=(x/g.depth,z/g.height)
                            else:
                                u,_=g.uv_at(surface,(-g.width/2,-x,z));top=g.profile(u)[1]
                                if z>top+.00001:break
                                uv=(u,z/max(.00001,top))
                        key=tuple(round(q,7) for q in uv)
                        if key not in lookup:lookup[key]=len(weights);weights.append(cloth.weights(surface,*uv))
                        pair.append(lookup[key])
                    if len(pair)==2:edges.extend(pair)
            # Kivy has a uint16/count limit. Current largest panel is <12000;
            # reject a future pathological topology before touching GLES.
            if len(edges)>24000 or len(weights)>16000:raise ValueError('Net mesh exceeds mobile batch budget')
            mesh_object=Mesh(vertices=[0.]*(len(weights)*4),indices=edges,mode='lines',noadd=True)
            front_object=Mesh(vertices=[0.]*(len(weights)*4),indices=[],mode='lines',noadd=True)
            self.group.add(mesh_object);self.front.add(front_object)
            self.batches.append((weights,edges,mesh_object,front_object))

    def sync(self,project,camera_key,ball=None):
        # Kivy pos/size are mutable ObservableReferenceLists; retain values,
        # never aliases, or an idle mesh silently ignores resize/reposition.
        camera_key=(tuple(camera_key[0]),tuple(camera_key[1]),*camera_key[2:])
        geometry_stamp=(self.cloth.generation,camera_key)
        stamp=(geometry_stamp,ball if self.cloth.contact else None)
        if stamp==self._stamp:return
        self._stamp=stamp
        geometry_changed=geometry_stamp!=self._geometry_stamp
        if geometry_changed:
            self._geometry_stamp=geometry_stamp;self.rebuilds+=1;self._world=[]
        p=self.cloth.positions
        for index,(weights,edges,mesh,front) in enumerate(self.batches):
            if geometry_changed:
                vertices=[];world=[]
                for row in weights:
                    a,b,c,d=row
                    point=tuple(p[a[0]][axis]*a[1]+p[b[0]][axis]*b[1]+p[c[0]][axis]*c[1]+p[d[0]][axis]*d[1] for axis in (0,1,2))
                    world.append(point);x,y=project(*point);vertices.extend((x,y,0.,0.))
                mesh.vertices=vertices;front.vertices=vertices;self._world.append(world)
            else:world=self._world[index]
            overlay=[]
            if ball is not None and self.cloth.contact:
                # Only real strands on the contact's outward hemisphere are
                # drawn over the ball. The remainder stays behind it.
                radius=self.cloth.contact['radius'];normal=self.cloth.contact['normal']
                # Same fixed lateral camera as Scorer: near sheet faces -x,+y.
                near=sum(a*b for a,b in zip(normal,(-46.,52.5,9.5)))>0
                if near:
                    for i in range(0,len(edges),2):
                        a,b=world[edges[i]],world[edges[i+1]];mid=tuple((x+y)/2 for x,y in zip(a,b))
                        if math.dist(mid,ball)<radius+.13:overlay.extend(edges[i:i+2])
            front.indices=overlay

    def draw(self,canvas,project,camera_key,ball=None,foreground=False):
        self.sync(project,camera_key,ball)
        group=self.front if foreground else self.group
        # A newly built group may be auto-added by an active Kivy canvas.
        # Normal groups must remain clearable; noadd=True would keep stale
        # groups across Canvas.clear() and leak/repaint them every frame.
        while group in canvas.children:canvas.remove(group)
        canvas.add(group)

    def debug(self,canvas,project):
        with canvas:
            Color(1,.55,.12,.8)
            for a,b,_,_ in self.cloth.links:
                Line(points=[*project(*self.cloth.positions[a]),*project(*self.cloth.positions[b])],width=.6)
            Color(.4,.9,1,1)
            Point(points=[n for p in self.cloth.positions for n in project(*p)],pointsize=2)
