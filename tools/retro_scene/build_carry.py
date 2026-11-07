"""Add articulated straight-arm trophy run without redrawing approved base art."""
import json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from PIL import Image
import os
from tools.sprite_lab.build_assets import PixelArtist,player_pose,role_palette
root=Path(__file__).resolve().parents[2];p=root/'assets/sprites/manifest.json';m=json.loads(p.read_text());c=m['characters']['players']
STATE=os.environ.get('SCORER_POSE','CARRY')
a=dict(frames=8,fps=12,loop=True,sheets={},individuals={},contacts={},joints={},contact_frames=[])
for view in c['views']:
 dest=root/('assets/sprites/players/'+STATE.lower())/view;dest.mkdir(parents=True,exist_ok=True)
 sheet=Image.new('P',(c['canvas'][0]*4,c['canvas'][1]*2),0);sheet.putpalette([v for rgb in role_palette('players') for v in rgb]+[0]*(768-48));files=[];joints=[]
 for i in range(8):
  pose=player_pose('RUN',i,8);sx,sy=pose['shoulder'];pose['hands']=[(sx-4.5,sy-12),(sx+4.5,sy-12)] if STATE=='CARRY' else [(sx-2,sy+7),(sx+3,sy+7)]
  artist=PixelArtist('players',view);im=artist.draw(pose);f=dest/f'frame_{i:02d}.png';im.save(f,bits=8,transparency=0);files.append(f.relative_to(root).as_posix());joints.append(artist.joints);sheet.paste(im,(i%4*c['canvas'][0],i//4*c['canvas'][1]))
 f=dest/'sheet.png';sheet.save(f,bits=8,transparency=0);a['sheets'][view]=dict(path=f.relative_to(root).as_posix(),columns=4,rows=2);a['individuals'][view]=files;a['joints'][view]=joints
c['animations'][STATE]=a;p.write_text(json.dumps(m,indent=2)+'\n')
