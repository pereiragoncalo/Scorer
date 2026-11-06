"""Build approval contact sheets and GIF directly from the shipped PNG frames."""
from PIL import Image,ImageDraw,ImageFont
from .animation import ROOT,load_manifest

OUT=ROOT/'docs/sprite_lab'
GREEN=(20,75,47)
FONT=ImageFont.load_default(size=16)

def sprite(path,scale):
    im=Image.open(ROOT/path).convert('RGBA')
    return im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)

def build():
    OUT.mkdir(exist_ok=True);m=load_manifest()
    # A compact approval board in the format of the user's supplied reference.
    board=Image.new('RGB',(1320,660),(37,42,47));draw=ImageDraw.Draw(board)
    title=ImageFont.load_default(size=22);caption=ImageFont.load_default(size=18)
    draw.text((22,16),'SCORER / SPRITES / REVISION 2',font=title,fill='white')
    selections=[('players',[('RUN',i) for i in (0,1,2,4,5,6)]),
                ('goalkeeper',[('READY',0),('MOVE',2),('LOW_SAVE',3),('DIVE_LEFT',5),('HIGH_SAVE',4),('DIVE_RIGHT',4)])]
    for row,(role,poses) in enumerate(selections):
        character=m['characters'][role]
        draw.text((22,57+row*300),'FIELD PLAYER / RUN' if row==0 else 'GOALKEEPER / DEFENSIVE POSES',font=caption,fill='#a8dbbb')
        for col,(state,frame) in enumerate(poses):
            art=Image.open(ROOT/character['animations'][state]['individuals']['front'][frame]).convert('RGBA')
            art=art.crop(art.getbbox())
            art=art.resize((art.width*5,art.height*5),Image.Resampling.NEAREST)
            board.paste(art,(col*220+(220-art.width)//2,320+row*300-art.height),art)
            draw.text((col*220+12,330+row*300),f'{state}  {frame+1}',font=caption,fill='white')
    board.save(OUT/'reference-revision-2.png')
    for role,c in m['characters'].items():
        w,h=c['canvas'];scale=2;cellw=w*scale+8;cellh=h*scale+26
        sheet=Image.new('RGB',(135+8*cellw,len(c['animations'])*cellh),GREEN);d=ImageDraw.Draw(sheet)
        for row,(state,a) in enumerate(c['animations'].items()):
            d.text((8,row*cellh+22),state,fill='white',font=FONT)
            for i,path in enumerate(a['individuals'][c['views'][0]]):
                im=sprite(path,scale);x=135+i*cellw;y=row*cellh
                sheet.paste(im,(x,y),im);d.text((x+10,y+h*scale+2),str(i+1),fill='#bde4c3',font=FONT)
        sheet.save(OUT/f'{role}-all-frames.png')
    frames=[];states=[list(c['animations']) for c in m['characters'].values()]
    for stateindex in range(max(map(len,states))):
        for tick in range(24):
            im=Image.new('RGB',(1000,440),GREEN);d=ImageDraw.Draw(im)
            d.text((22,12),'SCORER / ORIGINAL 8-BIT SPRITES / APPROVAL PREVIEW',fill='white',font=FONT)
            for index,(role,c) in enumerate(m['characters'].items()):
                state=states[index][stateindex%len(states[index])];a=c['animations'][state];frame=int(tick/24*a['frames'])
                art=sprite(a['individuals'][c['views'][0]][frame],5)
                ax,ay=c['anchor'];center=250+index*500;x=round(center-ax*5);y=round(360-ay*5)
                im.paste(art,(x,y),art)
                d.text((50+index*500,42),f'{role.upper()} / {state}',fill='white',font=FONT)
                d.text((50+index*500,395),f'FRAME {frame+1}/{a["frames"]}',fill='#bde4c3',font=FONT)
            d.line((0,361,1000,361),fill='#5c9164')
            frames.append(im)
    # Exact source colours retained; no quantisation blur or colour interpolation.
    palette=Image.new('RGB',(16*3,1));palette.putdata([tuple(c[:3]) for c in m['source_palette']]+[tuple(c[:3]) for c in m['characters']['goalkeeper']['source_palette']]+[GREEN,(255,255,255),(189,228,195),(92,145,100)]+[(0,0,0)]*12)
    palette=palette.quantize(colors=64,dither=Image.Dither.NONE)
    gifs=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    gifs[0].save(OUT/'animations.gif',save_all=True,append_images=gifs[1:],duration=80,loop=0,optimize=False,disposal=2)
    print('Preview:',OUT/'animations.gif')

if __name__=='__main__':build()
