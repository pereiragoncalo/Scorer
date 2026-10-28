"""Check real frozen Windows smoke evidence, including nonblank rendering."""
import json
from pathlib import Path
import sys
from PIL import Image


def verify(folder):
    folder=Path(folder)
    data=json.loads((folder/'smoke.json').read_text(encoding='utf8'))
    for key in ('ok','frozen','career_reload','training','free','close_confirmation','match_completed','matchday_dashboard','goal_scene_rendered','settled_ball_behind_keeper','empty_training_stands'):
        if data.get(key) is not True:raise ValueError('Missing Windows smoke check: '+key)
    if data.get('platform')!='win32':raise ValueError('This evidence is not from Windows')
    captures=list(folder.glob('smoke*.png'))
    if not captures:raise ValueError('No Windows screenshot')
    if abs(data.get('goal_width',0)-8.1984)>1e-8 or abs(data.get('goal_height',0)-2.684)>1e-8:raise ValueError('Wrong Windows goal geometry')
    if abs(data.get('goalkeeper_scale',0)-.688)>1e-8:raise ValueError('Wrong Windows keeper scale')
    for path in (captures[0],folder/'goal.png',folder/'training.png'):
        image=Image.open(path).convert('RGB')
        if image.width<640 or image.height<360 or max(high-low for low,high in image.getextrema())<32:
            raise ValueError('Window screenshot is blank or too small')
        colors=image.getcolors(maxcolors=128)
        if colors is not None and len(colors)<64:raise ValueError('No meaningful rendered game image')
    return data


if __name__=='__main__':
    print(json.dumps(verify(sys.argv[1]),indent=2))
