import unittest
import math
from PIL import Image
from tools.sprite_lab.animation import Animation,load_manifest,ROOT

class AssetsTest(unittest.TestCase):
    def test_upright_ink_height_calibration_ignores_transparent_padding(self):
        manifest=load_manifest()
        for role,state in (('players','IDLE'),('goalkeeper','RECOVER')):
            character=manifest['characters'][role]
            clip=character['animations'][state]
            for view in character['views']:
                image=Image.open(ROOT/clip['individuals'][view][-1]).convert('RGBA')
                height=character['anchor'][1]-image.getbbox()[1]
                self.assertEqual(height,character['standing_height_pixels'])

    def test_articulation_keeps_bone_lengths(self):
        from tools.sprite_lab.build_assets import ik
        for target in ((100,-100),(0,0),(3,5),(-9,1)):
            for bend in (-1,1):
                elbow,wrist=ik((0,0),target,6,6,bend)
                self.assertAlmostEqual(math.dist((0,0),elbow),6)
                self.assertAlmostEqual(math.dist(elbow,wrist),6)

    def test_complete_original_assets(self):
        m=load_manifest();total=0
        minimums=((2,6,6,4,6,4,4,4,6,8,6),(2,6,4,6,6,6,4,4))
        for (role,c),minimum in zip(m['characters'].items(),minimums):
            self.assertGreaterEqual(len(c['animations']),11 if role=='players' else 9)
            palette={tuple(v) for v in c['source_palette']}
            from tools.sprite_lab.build_assets import STATES
            required_by_state=dict(zip(STATES[role],minimum))
            for state,a in c['animations'].items():
                required=required_by_state.get(state,2)
                self.assertGreaterEqual(a['frames'],required)
                for view,paths in a['individuals'].items():
                    sheet=Image.open(ROOT/a['sheets'][view]['path']).convert('RGBA')
                    frames=[];w,h=c['canvas'];cols=a['sheets'][view]['columns']
                    for i,path in enumerate(paths):
                        im=Image.open(ROOT/path).convert('RGBA');total+=1
                        pixels=set(zip(*[iter(im.tobytes())]*4))
                        self.assertEqual(im.size,(w,h));self.assertTrue(pixels<=palette)
                        self.assertEqual({p[3] for p in pixels},{0,255})
                        box=im.getbbox();self.assertGreater(box[0],0);self.assertGreater(box[1],0)
                        self.assertLess(box[2],w);self.assertLess(box[3],h)
                        crop=sheet.crop(((i%cols)*w,(i//cols)*h,(i%cols+1)*w,(i//cols+1)*h))
                        self.assertEqual(im.tobytes(),crop.tobytes());frames.append(im.tobytes())
                    self.assertGreaterEqual(len(set(frames)),required,(role,state))
            self.assertEqual(c['anchor'][0],c['canvas'][0]/2)
        self.assertEqual(total,248)
        self.assertEqual(m['approval_status'],'APPROVED')

    def test_clock_and_event_contract(self):
        m=load_manifest();a=Animation(m['characters']['players'],'RUN')
        a.update(.25);self.assertEqual(a.frame,3)
        a.speed=2;a.update(.25);self.assertEqual(a.frame,1)
        a.paused=True;a.update(10);self.assertEqual(a.frame,1)
        a.step(-1);self.assertEqual(a.frame,0)
        a.event('SHOOT');a.paused=False;a.repeat=False;a.update(10)
        self.assertEqual(a.frame,7)
        g=Animation(m['characters']['goalkeeper'],'READY');g.event('DIVE',-1)
        self.assertEqual(g.state,'DIVE_LEFT');g.event('RECOVER');self.assertEqual(g.frame,0)
        with self.assertRaises(ValueError):a.select('NOT_A_GAME_ACTION')

if __name__=='__main__':unittest.main()
