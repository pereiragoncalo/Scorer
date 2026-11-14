"""Cached retro roof sprites and pitch-side low walls; visual geometry only."""
import math
from kivy.graphics import Color,Mesh,Rectangle
from retro_props import cache

def build(game,ctx):
    spec=ctx['ground'];palette=ctx['home_kit'];batches={}
    game.stadium_has_roof=spec.has_roof;game.stadium_wall_height=.55
    def quad(asset,points,tint=(1,1,1,1)):
        texture=cache(game).get(asset,palette)if asset else None
        coords=texture.tex_coords if texture else (0,0,1,0,1,1,0,1)
        vertices,indices=batches.setdefault((asset,tint),([],[]));base=len(vertices)//4
        for i,p in enumerate(points):vertices.extend((*game.project(*p),coords[2*i],coords[2*i+1]))
        indices.extend((base,base+1,base+2,base,base+2,base+3))
    # The wall is outside the pitch and in front of the first row, on both
    # visible stands. A short chamfer joins them without a corner gap.
    h=.55;front=-3.65;side=35.85
    quad('stadium_wall.png',((-36.2,front,0),(35.55,front,0),(35.55,front,h),(-36.2,front,h)))
    quad('stadium_wall.png',((side,-3.95,0),(side,32,0),(side,32,h),(side,-3.95,h)))
    quad('stadium_wall.png',((35.55,front,0),(side,-3.95,0),(side,-3.95,h),(35.55,front,h)))
    cap=(.64,.68,.65,1)
    quad(None,((-36.2,front,h),(35.55,front,h),(35.55,front-.20,h),(-36.2,front-.20,h)),cap)
    quad(None,((side,-3.95,h),(side,32,h),(side+.20,32,h),(side+.20,-3.95,h)),cap)
    if spec.has_roof:
        depth=spec.lower_rows*.85+(3.5+spec.upper_rows*.85 if spec.upper_rows else 0)
        lower=.3+spec.lower_rows*.27
        top=lower+(1.8+spec.upper_rows*.24 if spec.upper_rows else 0)
        inner=depth*.25;outer=depth+.5
        low=lower+(1.8 if spec.upper_rows else 2.4)
        high=top+(2.4 if spec.upper_rows else 3.2)
        front=-4-inner;back=-4-outer
        # Three original nearest-filtered pixel sprites form roof, fascia and
        # walls; no expensive transparent surfaces, scene-time or RNG changes.
        quad('stadium_roof.png',((-36.2,front,low),(36.2,front,low),(36.2,back,high),(-36.2,back,high)))
        quad('stadium_roof_fascia.png',((-36.2,front,low-.4),(36.2,front,low-.4),(36.2,front,low),(-36.2,front,low)))
        quad('stadium_roof.png',((36.2+inner,-4,low),(36.2+inner,32,low),(36.2+outer,32,high),(36.2+outer,-4,high)))
        quad('stadium_roof_fascia.png',((36.2+inner,-4,low-.4),(36.2+inner,32,low-.4),(36.2+inner,32,low),(36.2+inner,-4,low)))
        def corner(r,a,z):return (36.2+r*math.cos(a),-4-r*math.sin(a),z)
        for n in range(12):
            a=n*math.pi/24;b=(n+1)*math.pi/24
            quad('stadium_roof.png',(corner(inner,a,low),corner(inner,b,low),corner(outer,b,high),corner(outer,a,high)))
            quad('stadium_roof_fascia.png',(corner(inner,a,low-.4),corner(inner,b,low-.4),corner(inner,b,low),corner(inner,a,low)))
    game._stadium_architecture=(palette,tuple((asset,tint,vertices,indices)for (asset,tint),(vertices,indices)in batches.items()))

def draw(game):
    palette,batches=game._stadium_architecture
    for asset,tint,vertices,indices in batches:
        Color(*tint)
        if asset:Mesh(texture=cache(game).get(asset,palette),vertices=vertices,indices=indices,mode='triangles')
        else:Mesh(vertices=vertices,indices=indices,mode='triangles')


def draw_city(game):
    if game.stadium_has_roof:return
    texture=cache(game).get('stadium_city.png')
    height=game.height*.42;width=height*texture.width/texture.height
    y=game.y+game.height*.60;x=game.x
    Color(1,1,1,1)
    while x<game.right:
        Rectangle(texture=texture,pos=(x,y),size=(width,height))
        x+=width
