# PyInstaller single-file Windows build; run through tools/windows/build.py.
import os
from pathlib import Path
from kivy_deps import sdl2,glew,angle
stage=Path(os.environ['SCORER_WINDOWS_STAGE'])
binaries=[]
for directory in dict.fromkeys(sdl2.dep_bins+glew.dep_bins+angle.dep_bins):
    for file in Path(directory).glob('*.dll'):
        binaries.append((str(file),'.'))
a=Analysis([str(stage/'desktop_launcher.py')],pathex=[str(stage)],
           binaries=binaries,datas=[(str(stage/'assets'),'assets')],
           hiddenimports=['kivy.core.window.window_sdl2','kivy.core.image.img_sdl2',
                          'kivy.core.text.text_sdl2','kivy.core.audio.audio_sdl2'],
           excludes=['android','jnius','billing','android_names','tkinter'],
           hookspath=[],runtime_hooks=[],noarchive=False)
pyz=PYZ(a.pure)
exe=EXE(pyz,a.scripts,a.binaries,a.datas,[],name='Scorer-Free',
        debug=False,bootloader_ignore_signals=False,strip=False,upx=False,
        console=False,disable_windowed_traceback=False,
        icon=str(stage/'assets/icon.png'))
