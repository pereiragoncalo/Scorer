"""Shared nearest-neighbour atlas/PNG cache, Kivy only (no runtime Pillow)."""
from collections import OrderedDict
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from sprite_animation import ROOT

DEFAULT_PLAYER = ('2640DA', 'F8F6E4', '2234C6', 'F6F6E0', 'F9FDF1')
DEFAULT_KEEPER = ('44D727', 'E5FAC2', '1E2027', 'F6CF27', 'F9FDF1')

def rgb(value):
    value = value.strip().lstrip('#')
    if len(value) != 6:
        raise ValueError('Use six hexadecimal digits per colour.')
    return tuple(int(value[i:i+2],16) for i in (0,2,4))

def palette_map(manifest, colours, role):
    colours = [rgb(c) for c in colours]
    mapping = {}
    for palette_role, colour, dark in [('shirt',colours[0],False),('shirt_dark',colours[0],True),('secondary',colours[1],False),('shorts',colours[2],False),('shorts_dark',colours[2],True),('socks',colours[3],False),('socks_dark',colours[3],True),('gloves',colours[4],False),('gloves_dark',colours[4],True)]:
        index = manifest['palette_roles'].index(palette_role)
        mapping[tuple(manifest['characters'][role]['source_palette'][index][:3])] = tuple(round(c*.64) for c in colour) if dark else colour
    return mapping

class TextureCache:
    def __init__(self, manifest, limit=24):
        self.manifest, self.limit = manifest, limit
        self.sources, self.entries = {}, OrderedDict()
        self.allocations = 0

    def get(self, path, colours):
        key = (path,tuple(colours))
        if key in self.entries:
            self.entries.move_to_end(key)
            return self.entries[key]
        # At most the finite collection of source PNGs; no per-frame recolouring.
        if path not in self.sources:
            source = CoreImage(str(ROOT/path)).texture
            self.sources[path] = (source.size, bytes(source.pixels), source.tex_coords)
        size, pixels, coords = self.sources[path]
        role = 'goalkeeper' if '/goalkeeper/' in path else 'players'
        mapping = palette_map(self.manifest, colours, role)
        result = bytearray(pixels)
        for offset in range(0,len(result),4):
            if result[offset+3] and tuple(result[offset:offset+3]) in mapping:
                result[offset:offset+3] = bytes(mapping[tuple(result[offset:offset+3])])
        texture = Texture.create(size=size, colorfmt='rgba')
        texture.blit_buffer(bytes(result), colorfmt='rgba', bufferfmt='ubyte')
        # CoreImage PNG coordinates are vertically flipped relative to raw pixels.
        if coords[1] > coords[5]:
            texture.flip_vertical()
        texture.mag_filter = texture.min_filter = 'nearest'
        self.entries[key] = texture
        self.allocations += 1
        if len(self.entries) > self.limit:
            self.entries.popitem(last=False)
        return texture

    def frame(self, character, clip, view, frame, colours):
        sheet = clip['sheets'][view]
        texture = self.get(sheet['path'], colours)
        w,h = character['canvas']
        # Respect source PNG top-to-bottom ordering explicitly through UV coords.
        col,row = frame % sheet['columns'], frame // sheet['columns']
        u0,u1 = col/sheet['columns'], (col+1)/sheet['columns']
        v0,v1 = row/sheet['rows'], (row+1)/sheet['rows']
        base = texture.tex_coords
        bottom,top = base[1],base[5]
        vb = top + (bottom-top)*v1
        vt = top + (bottom-top)*v0
        return texture,(u0,vb,u1,vb,u1,vt,u0,vt)
