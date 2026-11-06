"""Original 8-bit props/fans. Build-time Pillow only; no runtime dependency."""
from pathlib import Path
from PIL import Image,ImageDraw
import math
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/sprites/scene';OUT.mkdir(parents=True,exist_ok=True)
INK=(13,18,28,255);PRIMARY=(40,80,210,255);SECONDARY=(240,240,220,255)
SKINS=((239,181,120,255),(175,113,69,255),(104,64,43,255))
# Eighteen distinct people: three silhouettes, three skin tones, both kit colours.
atlas=Image.new('RGBA',(12*18,18*6))
for frame in range(6):
 for column in range(18):
  style=column%3;skin=SKINS[(column//3)%3];flip=column//9
  shirt,trim=(SECONDARY,PRIMARY) if flip else (PRIMARY,SECONDARY)
  im=Image.new('RGBA',(12,18));d=ImageDraw.Draw(im)
  d.rectangle((4,2,8,6),fill=INK);d.rectangle((5,3,8,5),fill=skin)
  d.point((8,4),fill=INK);d.line((4,2,7,2),fill=INK,width=2)
  if style==2:d.line((4,1,8,1),fill=trim);d.point((9,2),fill=trim)
  d.polygon([(4,6),(8,6),(9,11),(8,13),(3,13),(3,8)],fill=INK)
  d.rectangle((4,7,7,11),fill=shirt);d.line((5,7,5,10),fill=trim)
  if style==1:d.line((4,8,7,8),fill=trim)
  d.rectangle((4,12,7,13),fill=(28,33,48,255));d.line((4,14,4,16),fill=INK,width=2);d.line((7,14,8,16),fill=INK,width=2)
  d.point((3,17),fill=INK);d.line((7,17,9,17),fill=INK)
  if frame<2:
   d.line((3,7,2,11+frame),fill=INK,width=2);d.point((2,12+frame),fill=skin)
   d.line((8,7,9,11-frame),fill=INK,width=2);d.point((9,12-frame),fill=skin)
  else:
   arms=(((3,7),(1,4),(1,1),(8,7),(10,4),(10,1)),((3,7),(1,5),(0,3),(8,7),(10,5),(11,3)),((3,7),(2,3),(3,0),(8,7),(9,3),(8,0)),((3,7),(0,6),(0,3),(8,7),(11,6),(11,3)))
   a,b,c,e,f,g=arms[(frame-2)%4]
   d.line((a,b,c),fill=INK,width=2);d.line((e,f,g),fill=INK,width=2);d.point(c,fill=skin);d.point(g,fill=skin)
   if style==1:d.line((c[0],c[1],g[0],g[1]),fill=trim,width=2)
  atlas.paste(im,(column*12,frame*18))
atlas.save(OUT/'supporters.png')
# Eight independent 16x16 ball frames, with rolling black leather panels.
sheet=Image.new('RGBA',(16*8,16))
for frame in range(8):
 im=Image.new('RGBA',(16,16));d=ImageDraw.Draw(im)
 silhouette=[(5,0),(10,0),(10,1),(12,1),(12,2),(14,2),(14,4),(15,4),(15,11),(14,11),(14,13),(12,13),(12,14),(10,14),(10,15),(5,15),(5,14),(3,14),(3,13),(1,13),(1,11),(0,11),(0,4),(1,4),(1,2),(3,2),(3,1),(5,1)]
 d.polygon(silhouette,fill=INK);d.polygon([(5,1),(10,1),(13,3),(14,5),(14,10),(12,13),(9,14),(5,14),(2,12),(1,9),(1,5),(3,2)],fill=(246,245,221,255))
 angle=frame*math.tau/8
 for radius,start in ((0,0),(6,0),(6,2.1),(6,4.2)):
  x=7.5+radius*math.cos(angle+start);y=7.5+radius*math.sin(angle+start)
  pts=[(round(x+2.3*math.cos(angle+i*math.tau/5)),round(y+2.3*math.sin(angle+i*math.tau/5))) for i in range(5)]
  d.polygon(pts,fill=INK)
 # Clip all panels back to the original ball silhouette.
 mask=Image.new('L',(16,16));ImageDraw.Draw(mask).polygon(silhouette,fill=255);im.putalpha(mask)
 sheet.paste(im,(frame*16,0))
sheet.save(OUT/'ball.png')
# A hand-authored gold cup with separate handles, stem and plinth.
im=Image.new('RGBA',(24,28));d=ImageDraw.Draw(im)
d.line([(5,5),(1,5),(1,11),(6,15)],fill=INK,width=3);d.line([(18,5),(22,5),(22,11),(17,15)],fill=INK,width=3)
d.line([(5,5),(2,5),(2,10),(6,13)],fill=(241,183,37,255),width=1);d.line([(18,5),(21,5),(21,10),(17,13)],fill=(241,183,37,255),width=1)
d.polygon([(4,2),(19,2),(18,13),(15,17),(13,18),(13,22),(19,23),(20,27),(3,27),(4,23),(10,22),(10,18),(7,16),(5,12)],fill=INK)
d.polygon([(5,3),(18,3),(17,12),(14,16),(10,16),(7,13)],fill=(237,172,26,255));d.line([(6,4),(6,10),(9,14)],fill=(255,237,139,255),width=2)
d.rectangle((11,17,12,23),fill=(250,206,62,255));d.rectangle((5,24,18,25),fill=(237,172,26,255));d.rectangle((4,26,19,26),fill=(97,63,27,255))
im.save(OUT/'trophy.png')
print('Original scene sprites: 108 fan cells,8 ball frames,1 trophy')
