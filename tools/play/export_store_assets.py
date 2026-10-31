from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[2];out=r/'release/store';out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(r/'assets/fonts/Barlow-Regular.ttf'),25)
for product,icon,logo in [('free','icon.png','menu_logo.png'),('world','icon_world.png','menu_logo_world.png')]:
 target=out/product;target.mkdir(exist_ok=True)
 im=Image.open(r/'assets'/icon).convert('RGBA');im.resize((512,512),Image.Resampling.LANCZOS).save(target/'icon-512.png',optimize=True)
 # Deterministic export of existing branding, not a fabricated gameplay screenshot.
 bg=Image.open(r/'assets/menu_stadium.png').convert('RGB')
 ratio=max(1024/bg.width,500/bg.height);bg=bg.resize((round(bg.width*ratio),round(bg.height*ratio)),Image.Resampling.LANCZOS)
 left=(bg.width-1024)//2;top=(bg.height-500)//2;bg=bg.crop((left,top,left+1024,top+500))
 layer=Image.new('RGBA',(1024,500),(3,16,23,145));base=Image.alpha_composite(bg.convert('RGBA'),layer)
 mark=Image.open(r/'assets'/logo).convert('RGBA');bbox=mark.getbbox()
 if bbox:mark=mark.crop(bbox)
 scale=min(800/mark.width,190/mark.height);mark=mark.resize((round(mark.width*scale),round(mark.height*scale)),Image.Resampling.LANCZOS)
 base.alpha_composite(mark,((1024-mark.width)//2,110))
 draw=ImageDraw.Draw(base);text='Your striker career starts here' if product=='free' else 'A world of striker careers'
 box=draw.textbbox((0,0),text,font=font);draw.text(((1024-box[2])/2,365),text,font=font,fill=(235,248,248))
 base.convert('RGB').save(target/'feature-1024x500.png',optimize=True)
 for p in target.glob('*.png'):
  with Image.open(p) as image:
   assert image.size==((512,512) if 'icon' in p.name else (1024,500))
  if 'icon' in p.name:assert p.stat().st_size<=1024*1024
metadata={str(p.relative_to(out)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in out.glob('*/*.png')}
(out/'verification.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata,indent=2))
