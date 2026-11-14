"""Original, hand-authored low-resolution stadium props. Build-time Pillow only."""
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[1]/'assets/sprites/scene'
BLUE=(40,80,210);CREAM=(240,240,220)

def save(image,name):image.save(OUT/name,optimize=True)

def props():
 im=Image.new('RGBA',(128,32),(84,103,115,255));d=ImageDraw.Draw(im)
 for y in range(32):
  shade=(108,126,137)if y%8<2 else(66,85,99)if y%8==7 else(86,105,117)
  d.line((0,y,127,y),fill=shade)
 for x in range(0,128,16):d.line((x,0,x,31),fill=(52,69,83));d.point((x+2,3),fill=CREAM);d.point((x+2,27),fill=CREAM)
 save(im,'stadium_roof.png')
 im=Image.new('RGBA',(128,16),(31,46,58,255));d=ImageDraw.Draw(im);d.rectangle((0,0,127,2),fill=CREAM);d.rectangle((0,3,127,7),fill=BLUE)
 for x in range(0,128,16):d.line((x,15,x+8,8,x+16,15),fill=(130,146,154),width=1)
 save(im,'stadium_roof_fascia.png')
 im=Image.new('RGBA',(128,16),(94,104,105,255));d=ImageDraw.Draw(im);d.rectangle((0,0,127,2),fill=(176,184,175));d.line((0,3,127,3),fill=(48,60,64));d.line((0,7,127,7),fill=BLUE)
 for y in (8,12):
  d.line((0,y,127,y),fill=(63,77,81))
  for x in range((y%8)*2,128,16):d.line((x,y,x,y+3),fill=(68,81,83))
 save(im,'stadium_wall.png')

def portrait(kind,roof=False,tiers=1,open_ends=False):
 im=Image.new('RGBA',(320,180),(12,26,38,255));d=ImageDraw.Draw(im)
 for y,c in ((0,(30,54,73)),(28,(43,71,87)),(54,(64,89,95))):d.rectangle((0,y,319,179),fill=c)
 for x,y in ((24,31),(205,20),(265,42)):
  d.rectangle((x,y,x+24,y+4),fill=(115,134,136));d.rectangle((x+6,y-3,x+17,y+5),fill=(115,134,136))
 d.rectangle((0,92,319,179),fill=(24,53,47));d.polygon(((9,123),(162,59),(313,122),(167,177)),fill=(17,37,35))
 top=35 if tiers==2 else 49;extra=10 if kind=='major' else 4 if kind in ('bowl','double') else 0
 outer=((27-extra,91),(161,top-extra),(297+extra,91),(166,155+extra))
 if kind=='local':outer=((58,91),(161,53),(265,91),(166,145))
 if kind=='compact':outer=((43,91),(161,49),(280,91),(166,150))
 inner=((82,92),(161,62),(246,94),(165,132))
 # Far bowl, outer concrete and two visible facade faces.
 d.polygon(outer,fill=(69,88,93));d.polygon((outer[0],outer[3],(outer[3][0],outer[3][1]+12),(outer[0][0],103)),fill=(34,48,55))
 d.polygon((outer[3],outer[2],(outer[2][0],103),(outer[3][0],outer[3][1]+12)),fill=(45,61,66))
 # Four low-resolution seating panels, with stair aisles.
 panels=((outer[0],outer[1],inner[1],inner[0]),(outer[1],outer[2],inner[2],inner[1]),(inner[0],inner[3],outer[3],outer[0]),(inner[3],inner[2],outer[2],outer[3]))
 for index,poly in enumerate(panels):
  if open_ends and index in (1,2):continue
  d.polygon(poly,fill=(34,55,77))
  a,b,c,e=poly
  for row in range(2,9 if tiers==1 else 13):
   t=row/(10 if tiers==1 else 14)
   left=(a[0]+(e[0]-a[0])*t,a[1]+(e[1]-a[1])*t);right=(b[0]+(c[0]-b[0])*t,b[1]+(c[1]-b[1])*t)
   d.line((*left,*right),fill=BLUE if row%3 else CREAM,width=1)
  if tiers==2:
   mid=[((poly[i][0]+poly[(i+3)%4][0])//2,(poly[i][1]+poly[(i+3)%4][1])//2)for i in (0,1)]
   d.line((*mid[0],*mid[1]),fill=(153,166,162),width=3)
 # Pitch diamond and its markings.
 d.polygon(inner,fill=(25,110,65))
 for y in range(66,133,9):
  for yy in range(y,min(133,y+3)):
   hits=[]
   for a,b in zip(inner,(*inner[1:],inner[0])):
    if min(a[1],b[1])<=yy<max(a[1],b[1]):hits.append(a[0]+(b[0]-a[0])*(yy-a[1])/(b[1]-a[1]))
   if len(hits)==2:d.line((round(min(hits)),yy,round(max(hits)),yy),fill=(31,120,70))
 d.line((*inner[0],*inner[1],*inner[2],*inner[3],*inner[0]),fill=(179,204,159),width=1)
 d.line((123,76,204,113),fill=(179,204,159),width=1);d.ellipse((151,88,176,103),outline=(179,204,159))
 d.line((91,91,103,87,110,92,99,97),fill=CREAM,width=2);d.line((222,102,235,97,242,101,230,107),fill=CREAM,width=2)
 # Small pitch-side wall on every variant.
 d.line((*inner[0],*inner[3],*inner[2]),fill=(189,192,175),width=2)
 if roof:
  # Roof panels leave a clear central opening; compact grounds have open corners.
  for index,poly in enumerate(panels):
   if kind=='covered' and index==1:continue
   a,b,c,e=poly;offset=4 if index<2 else 0
   ra=(a[0],a[1]-offset);rb=(b[0],b[1]-offset)
   re=(round(a[0]+(e[0]-a[0])*.62),round(a[1]+(e[1]-a[1])*.62)-offset)
   rc=(round(b[0]+(c[0]-b[0])*.62),round(b[1]+(c[1]-b[1])*.62)-offset)
   d.polygon((ra,rb,rc,re),fill=(103,124,132));d.line((*re,*rc),fill=CREAM,width=2)
   for step in range(1,15):
    t=step/15;d.line((round(ra[0]+(rb[0]-ra[0])*t),round(ra[1]+(rb[1]-ra[1])*t),round(re[0]+(rc[0]-re[0])*t),round(re[1]+(rc[1]-re[1])*t)),fill=(66,89,103))
   if kind=='covered':d.rectangle((outer[index][0]-1,outer[index][1]-1,outer[index][0]+1,outer[index][1]+1),fill=(19,43,44))
 # Floodlight sprites and facade details.
 for x,y in ((35,50),(283,50)):
  d.rectangle((x,y,x+1,99),fill=(138,158,158));d.rectangle((x-6,y-4,x+7,y+1),fill=(35,47,57))
  for n in range(4):d.rectangle((x-5+n*3,y-3,x-4+n*3,y-2),fill=CREAM)
 for x,y in ((102,141),(229,137)):
  d.rectangle((x,y,x+8,y+7),fill=(16,28,33));d.line((x,y,x+8,y),fill=BLUE,width=2)
 save(im,'stadium_'+kind+'.png')

if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True);props()
 for kind,roof,tiers,open_ends in (('local',False,1,True),('compact',False,1,False),('covered',True,1,False),('bowl',True,1,False),('double',True,2,False),('major',True,2,False)):portrait(kind,roof,tiers,open_ends)
