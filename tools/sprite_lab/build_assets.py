"""Original articulated pixel drawings for Scorer's approval-only sprite lab.

Pillow is a build dependency only. No supersampling, antialiasing, external game
art or game imports. Limbs are redrawn as pixel clusters, not rotated screenshots.
"""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'assets/sprites'
PALETTE=[(0,0,0),(8,14,24),(171,104,49),(242,191,112),(35,25,28),
 (230,38,48),(150,22,37),(251,239,171),(226,226,207),(119,130,126),
 (246,246,224),(157,166,153),(23,31,40),(249,253,241),(255,249,219),(161,188,185)]
ROLES=['transparent','outline','skin_dark','skin','hair','shirt','shirt_dark','secondary','shorts','shorts_dark','socks','socks_dark','boots','gloves','highlight','gloves_dark']
SPECS={'players':dict(canvas=[65,57],origin=[32,50],anchor=[32.5,52.0],views=['back','front']),
       'goalkeeper':dict(canvas=[97,65],origin=[48,56],anchor=[48.5,58.0],views=['front'])}
STATES={'players':{'IDLE':(2,4,True),'RUN':(8,12,True),'DRIBBLE':(8,10,True),'PASS':(6,10,False),'SHOOT':(8,12,False),'TACKLE':(8,11,False),'HEADER':(8,10,False),'FALL':(8,10,False)},
'goalkeeper':{'READY':(4,5,True),'MOVE':(8,11,True),'LOW_SAVE':(6,10,False),'DIVE_LEFT':(8,12,False),'DIVE_RIGHT':(8,12,False),'HIGH_SAVE':(8,11,False),'CATCH':(6,9,False),'RECOVER':(8,10,False)}}

def role_palette(role):
    colours=list(PALETTE)
    if role=='goalkeeper':
        for index,colour in {5:(40,184,133),6:(26,118,85),7:(255,242,174),8:(20,47,55),9:(13,30,35),10:(41,185,134),11:(27,119,86)}.items():colours[index]=colour
    return colours

def mix(a,b,t):return tuple(x+(y-x)*t for x,y in zip(a,b))
def ik(a,b,l1,l2,bend):
    dx,dy=b[0]-a[0],b[1]-a[1];d=max(.05,math.hypot(dx,dy));d2=min(l1+l2-.03,max(abs(l1-l2)+.03,d))
    bx=a[0]+dx*d2/d;by=a[1]+dy*d2/d;ux,uy=(bx-a[0])/d2,(by-a[1])/d2
    along=(l1*l1-l2*l2+d2*d2)/(2*d2);height=math.sqrt(max(0,l1*l1-along*along))
    return (a[0]+ux*along-uy*height*bend,a[1]+uy*along+ux*height*bend),(bx,by)

def base(keeper=False):
    return dict(hip=(0,-16),shoulder=(0,-28),feet=[(-3,0),(3,0)],hands=[(-5,-17),(5,-17)],knees=None,dy=0,head_tilt=0)

def player_pose(state,f,n):
    p=base();phase=f/n*math.tau
    if state=='IDLE':
        p['shoulder']=(f,-28-f);p['hands']=[(-5,-17-f),(5,-18+f)]
    elif state in ('RUN','DRIBBLE'):
        dribble=state=='DRIBBLE';stride=4.5 if dribble else 7
        bob=round(abs(math.sin(phase))*1)
        p.update(hip=(1,-14-bob),shoulder=(3 if dribble else 2,-27-bob))
        p['feet']=[(-math.sin(phase)*stride,-max(0,-math.cos(phase))*4),(math.sin(phase)*stride,-max(0,math.cos(phase))*4)]
        swing=4 if dribble else 7
        p['hands']=[(math.sin(phase)*swing-1,-18-math.cos(phase)),(-math.sin(phase)*swing+1,-18+math.cos(phase))]
    elif state in ('PASS','SHOOT'):
        if state=='PASS':
            feet=[(3,0),(-5,-3),(7,-1),(11,-5),(6,-2),(3,0)];leans=[0,-1,1,2,1,0];arms=[2,4,6,5,3,2]
        else:
            feet=[(3,0),(-6,-3),(-10,-8),(10,-2),(16,-9),(17,-13),(9,-5),(3,0)];leans=[0,-1,-3,1,4,6,3,0];arms=[2,4,7,10,9,7,5,2]
        lean=leans[f];p['hip']=(lean*.35,-16+max(0,lean)*.15);p['shoulder']=(lean,-28+max(0,lean)*.2)
        p['feet']=[(-2,0),feet[f]];p['hands']=[(-arms[f],-18-abs(lean)*.6),(arms[f]+2,-21-abs(lean)*.5)]
    elif state=='TACKLE':
        hips=[(0,-16),(1,-12),(4,-8),(7,-5),(8,-4),(4,-8),(1,-13),(0,-16)]
        shoulders=[(0,-28),(2,-24),(8,-19),(12,-13),(14,-12),(6,-20),(2,-25),(0,-28)]
        front=[(3,0),(6,0),(15,-1),(22,-1),(24,0),(14,0),(7,0),(3,0)]
        p.update(hip=hips[f],shoulder=shoulders[f],feet=[(-4,0),front[f]])
        p['hands']=[(-7,-12+f if f<5 else -15),(16,-8) if 2<=f<=4 else (6,-18)]
    elif state=='HEADER':
        lifts=[0,0,-3,-7,-5,0,0,0];p['dy']=lifts[f]
        p['hip']=(0,-13 if f in (1,5) else -16);p['shoulder']=(3 if f in (3,4) else 0,-25 if f in (1,5) else -28)
        p['feet']=[(-4,-2 if f in (2,3,4) else 0),(4,-2 if f in (2,3,4) else 0)]
        p['hands']=[(-8,-21),(9,-21)];p['head_tilt']=20 if f in (3,4) else 0
        if f==7:p=base()
    elif state=='FALL':
        hips=[(0,-16),(2,-12),(6,-7),(8,-3),(4,-5),(0,-9),(0,-13),(0,-16)]
        shoulders=[(1,-28),(8,-23),(16,-13),(20,-5),(11,-13),(-1,-21),(0,-25),(0,-28)]
        feet=[((-3,0),(3,0)),((-5,0),(6,-1)),((-7,-1),(9,-2)),((-5,0),(6,-1)),((-5,0),(9,0)),((-4,0),(5,0)),((-3,0),(4,0)),((-3,0),(3,0))]
        hands=[((-8,-22),(9,-21)),((-6,-15),(17,-17)),((9,-2),(23,-6)),((18,-1),(29,-2)),((0,-1),(19,-1)),((-5,-12),(6,-9)),((-5,-16),(5,-17)),((-5,-17),(5,-17))]
        p.update(hip=hips[f],shoulder=shoulders[f],feet=list(feet[f]),hands=list(hands[f]))
    return p

def keeper_pose(state,f,n):
    p=base(True);p.update(hip=(0,-15),shoulder=(0,-28),feet=[(-5,0),(5,0)],hands=[(-7,-19),(7,-19)])
    if state=='READY':
        shifts=[0,-1,0,1];p['hip']=(shifts[f],-15);p['shoulder']=(shifts[f],-28+(f%2));p['hands']=[(-7+shifts[f],-19),(7+shifts[f],-19-(f%2))]
    elif state=='MOVE':
        phase=f/n*math.tau;p['hip']=(0,-15-round(abs(math.sin(phase))));p['shoulder']=(0,-28-round(abs(math.sin(phase))))
        p['feet']=[(-5-math.sin(phase)*3,-max(0,-math.cos(phase))*2),(5+math.sin(phase)*3,-max(0,math.cos(phase))*2)]
        p['hands']=[(-7,-19+math.sin(phase)),(7,-19-math.sin(phase))]
    elif state in ('DIVE_LEFT','DIVE_RIGHT'):
        hips=[(0,-15),(-1,-12),(3,-16),(7,-19),(10,-17),(12,-11),(11,-5),(9,-3)]
        shoulders=[(0,-28),(0,-25),(6,-28),(14,-28),(21,-22),(24,-14),(23,-7),(21,-5)]
        feet=[((-5,0),(5,0)),((-5,0),(6,0)),((-6,-1),(7,-6)),((-5,-11),(1,-8)),((-4,-9),(0,-5)),((-3,-5),(2,-3)),((-4,0),(1,-1)),((-5,0),(0,-1))]
        hands=[((-7,-19),(7,-19)),((-5,-18),(10,-23)),((13,-34),(17,-32)),((24,-35),(26,-32)),((33,-28),(33,-25)),((36,-20),(36,-18)),((33,-13),(33,-10)),((32,-8),(31,-6))]
        p.update(hip=hips[f],shoulder=shoulders[f],feet=list(feet[f]),hands=list(hands[f]))
        if state=='DIVE_LEFT':
            for key in ('hip','shoulder'):p[key]=(-p[key][0],p[key][1])
            for key in ('feet','hands'):p[key]=[(-x,y) for x,y in p[key]]
    elif state=='LOW_SAVE':
        hips=[(0,-15),(1,-12),(2,-9),(3,-8),(1,-11),(0,-15)]
        shoulders=[(0,-28),(2,-24),(4,-19),(6,-18),(2,-24),(0,-28)]
        hands=[((-7,-19),(7,-19)),((1,-10),(7,-11)),((4,-4),(9,-4)),((6,-3),(10,-3)),((0,-17),(5,-16)),((-6,-19),(6,-19))]
        p.update(hip=hips[f],shoulder=shoulders[f],hands=list(hands[f]),feet=[(-7,0),(5,0)])
    elif state=='HIGH_SAVE':
        heights=[0,0,-2,-5,-7,-4,0,0];p['dy']=heights[f]
        hands=[((-7,-19),(7,-19)),((-7,-28),(7,-28)),((-6,-37),(6,-37)),((-3,-42),(3,-42)),((-2,-42),(2,-42)),((-4,-35),(4,-35)),((-6,-26),(6,-26)),((-7,-19),(7,-19))]
        p['hands']=list(hands[f]);p['feet']=[(-4,-1 if f in (3,4,5) else 0),(4,-2 if f in (3,4,5) else 0)]
        if f==6:p['hip']=(0,-12);p['shoulder']=(0,-25)
    elif state=='CATCH':
        hands=[((-7,-19),(7,-19)),((-7,-26),(7,-26)),((-4,-31),(4,-31)),((-2,-28),(2,-28)),((-2,-24),(2,-24)),((-2,-21),(2,-21))]
        p['hands']=list(hands[f]);p['hip']=(0,-15-(f==2));p['shoulder']=(0,-28-(f==2))
    elif state=='RECOVER':
        hips=[(9,-3),(7,-4),(4,-5),(1,-8),(0,-11),(0,-13),(0,-14),(0,-15)]
        shoulders=[(21,-5),(18,-9),(11,-13),(5,-18),(1,-23),(0,-26),(0,-27),(0,-28)]
        hands=[((32,-8),(31,-6)),((16,-1),(27,-1)),((3,-1),(19,-1)),((-3,-4),(12,-5)),((-5,-12),(9,-13)),((-6,-17),(7,-17)),((-7,-18),(7,-19)),((-7,-19),(7,-19))]
        p.update(hip=hips[f],shoulder=shoulders[f],hands=list(hands[f]),feet=[(-5,0),(4,0)])
    return p

class PixelArtist:
    def __init__(self,role,view):
        self.role=role;self.view=view;spec=SPECS[role];self.image=Image.new('P',spec['canvas'],0)
        self.image.putpalette([c for rgb in role_palette(role) for c in rgb]+[0]*(768-len(PALETTE)*3));self.image.info['transparency']=0
        self.d=ImageDraw.Draw(self.image);self.origin=spec['origin'];self.joints={}
    def point(self,p):return tuple(round(a+b) for a,b in zip(p,self.origin))
    def poly(self,points,color):self.d.polygon([self.point(p) for p in points],fill=color)
    def line(self,points,color,width):self.d.line([self.point(p) for p in points],fill=color,width=width)
    def pixel(self,p,color):self.d.point(self.point(p),fill=color)
    def limb(self,a,j,b,color1,color2,width=3):
        self.line((a,j,b),1,width+2);self.line((a,j),color1,width);self.line((j,b),color2,width)
        self.pixel((j[0]+1,j[1]),color2)
    def draw(self,p):
        keeper=self.role=='goalkeeper';hip=p['hip'];shoulder=p['shoulder'];dy=p.get('dy',0)
        def shift(v):return (v[0],v[1]+dy)
        hip=shift(hip);shoulder=shift(shoulder);feet=list(map(shift,p['feet']));hands=list(map(shift,p['hands']))
        dx,dy2=shoulder[0]-hip[0],shoulder[1]-hip[1];length=max(1,math.hypot(dx,dy2));along=(dx/length,dy2/length);cross=(-along[1],along[0])
        def side(center,offset):return (center[0]+cross[0]*offset,center[1]+cross[1]*offset)
        hips=[side(hip,-2),side(hip,2)];shoulders=[side(shoulder,-3.5),side(shoulder,3.5)]
        # Far leg first. Knees are genuine two-bone bends; ankles never stretch.
        for i in (0,1):
            knee,foot=ik(hips[i],feet[i],8,8,1)
            self.limb(hips[i],knee,foot,9 if i==0 else 8,11 if i==0 else 10,2)
            # Pixel boots: heel, sole, toe and one flat lace highlight.
            x,y=foot;self.poly(((x-1,y-1),(x+2,y-1),(x+4,y+1),(x-1,y+1)),1)
            self.line(((x,y),(x+2,y)),12,1);self.pixel((x+2,y),14)
            self.joints['ankle_'+str(i)]=self.point(foot);self.joints['knee_'+str(i)]=self.point(knee)
        elbows=[];wrists=[]
        for i in (0,1):
            elbow,wrist=ik(shoulders[i],hands[i],6,6,-1 if i==0 else 1);elbows.append(elbow);wrists.append(wrist)
        # Far sleeve/forearm behind the shirt. Full sleeves distinguish the GK.
        self.limb(shoulders[0],elbows[0],wrists[0],6,6 if keeper else 2,2)
        self.hand(wrists[0],keeper,False)
        # Tailored torso with tapered waist, a collar and solid-pixel folds.
        a=side(shoulder,-4);b=side(shoulder,4);c=side(hip,3);d=side(hip,-3)
        self.poly((a,b,c,d),1)
        inner=(mix(a,b,.12),mix(a,b,.88),mix(c,d,.12),mix(c,d,.88));self.poly(inner,5)
        self.line((mix(a,b,.18),mix(d,c,.18)),6,1)
        collar=(shoulder[0]-along[0],shoulder[1]-along[1]);self.line((side(collar,-1),side(collar,1)),7,1)
        self.line((side(hip,-2.5),side(hip,2.5)),8,2)
        # A hand-lettered 9 on the back; a tiny original chest patch on the front.
        center=mix(shoulder,hip,.48)
        pattern=('111','101','111','001','111') if self.view=='back' else ('11','10','11')
        for row,bits in enumerate(pattern):
            for col,bit in enumerate(bits):
                if bit=='1':self.pixel((center[0]+cross[0]*(col-1)-along[0]*(row-1),center[1]+cross[1]*(col-1)-along[1]*(row-1)),7)
        self.limb(shoulders[1],elbows[1],wrists[1],5,5 if keeper else 3,2)
        # Short-sleeve cuff or long-sleeve wrist ribbing.
        cuff=wrists[1] if keeper else mix(shoulders[1],elbows[1],.7)
        self.pixel((cuff[0]-1,cuff[1]),7)
        self.hand(wrists[1],keeper,True)
        self.line((shoulder,(shoulder[0]+along[0]*5,shoulder[1]+along[1]*5)),1,3)
        self.line((shoulder,(shoulder[0]+along[0]*5,shoulder[1]+along[1]*5)),3,1)
        head=(shoulder[0]+along[0]*7,shoulder[1]+along[1]*7)
        stamp=Image.new('P',(6,7),0);stamp.putpalette(self.image.getpalette())
        back=['.1111.','144441','144441','144431','143331','.12331','..111.']
        front=['.1111.','144441','143331','133133','133331','.12331','..111.']
        for y,row in enumerate(back if self.view=='back' else front):
            for x,char in enumerate(row):
                if char!='.':stamp.putpixel((x,y),int(char))
        angle=math.degrees(math.atan2(along[0],-along[1]))*.65+p.get('head_tilt',0)
        if angle:stamp=stamp.rotate(-angle,resample=Image.Resampling.NEAREST,expand=True)
        mask=Image.new('L',stamp.size);mask.putdata([255 if value else 0 for value in stamp.tobytes()])
        hx,hy=self.point(head);self.image.paste(stamp,(hx-stamp.width//2,hy-stamp.height//2),mask)
        self.joints.update(hip=self.point(hip),shoulder=self.point(shoulder),head=self.point(head),wrist_0=self.point(wrists[0]),wrist_1=self.point(wrists[1]))
        return self.image
    def hand(self,p,keeper,near):
        x,y=p
        if keeper:
            self.poly(((x-2,y-1),(x+1,y-2),(x+2,y),(x+1,y+2),(x-2,y+1)),1)
            self.poly(((x-1,y-1),(x+1,y-1),(x+1,y+1),(x-1,y+1)),13 if near else 15)
            self.pixel((x,y-1),14)
        else:
            self.line(((x,y-1),(x,y+1)),1,3);self.line(((x,y-1),(x,y)),3 if near else 2,2)

def build():
    manifest=dict(version=1,approval_status='AWAITING_VISUAL_APPROVAL',original_art=True,nominal_body=[32,40],palette_roles=ROLES,source_palette=[list(c)+[0 if i==0 else 255] for i,c in enumerate(PALETTE)],characters={})
    for role,spec in SPECS.items():
        character=dict(source_palette=[list(c)+[0 if i==0 else 255] for i,c in enumerate(role_palette(role))],canvas=spec['canvas'],anchor=spec['anchor'],nominal_height=40,views=spec['views'],animations={})
        for state,(count,fps,loop) in STATES[role].items():
            entry=dict(frames=count,fps=fps,loop=loop,sheets={},individuals={},contacts={},joints={})
            for view in spec['views']:
                path=DEST/role/state.lower()/view;path.mkdir(parents=True,exist_ok=True)
                cols=min(4,count);rows=math.ceil(count/cols);sheet=Image.new('P',(cols*spec['canvas'][0],rows*spec['canvas'][1]),0);sheet.putpalette([c for rgb in role_palette(role) for c in rgb]+[0]*(768-len(PALETTE)*3));sheet.info['transparency']=0
                files=[];joints=[]
                for f in range(count):
                    pose=player_pose(state,f,count) if role=='players' else keeper_pose(state,f,count)
                    artist=PixelArtist(role,view);image=artist.draw(pose)
                    filename=path/f'frame_{f:02d}.png';image.save(filename,bits=8,transparency=0)
                    files.append(filename.relative_to(ROOT).as_posix());joints.append(artist.joints)
                    sheet.paste(image,((f%cols)*spec['canvas'][0],(f//cols)*spec['canvas'][1]))
                filename=path/'sheet.png';sheet.save(filename,bits=8,transparency=0)
                entry['sheets'][view]=dict(path=filename.relative_to(ROOT).as_posix(),columns=cols,rows=rows)
                entry['individuals'][view]=files;entry['joints'][view]=joints
            entry['contact_frames']={'PASS':[2],'SHOOT':[3],'DRIBBLE':[2,6],'HEADER':[3],'TACKLE':[3],'LOW_SAVE':[3],'DIVE_LEFT':[5],'DIVE_RIGHT':[5],'HIGH_SAVE':[4],'CATCH':[3]}.get(state,[])
            character['animations'][state]=entry
        manifest['characters'][role]=character
    DEST.mkdir(parents=True,exist_ok=True);(DEST/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Original frames:',sum(a['frames']*len(c['views']) for c in manifest['characters'].values() for a in c['animations'].values()))
    return manifest

if __name__=='__main__':build()
