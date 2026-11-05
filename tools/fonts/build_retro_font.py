"""Build original Scorer Retro text lettering; no runtime fontTools/Pillow needed.

Nine-column lowercase matrices follow the approved concept. Capitals/numerals
extend the project's original pixel lettering. Licensed Barlow symbols are
rasterised to this grid. Accented Latin characters have composed pixel outlines.
"""
from pathlib import Path
import sys,unicodedata
from PIL import Image,ImageDraw,ImageFont
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.removeOverlaps import removeOverlaps
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_press_fonts import ART
ROOT=Path(__file__).resolve().parents[2]
CELL=70
LOWER={
'a':'000000000/000000000/000000000/011111100/000001110/011111110/111000110/110000110/111001110/011111110',
'b':'110000000/110000000/110000000/111111100/111001110/110000110/110000110/110000110/111001110/111111100',
'c':'000000000/000000000/000000000/001111110/011000000/110000000/110000000/110000000/011000000/001111110',
'd':'000000110/000000110/000000110/001111110/011001110/110000110/110000110/110000110/011001110/001111110',
'e':'000000000/000000000/000000000/001111100/011001110/110000110/111111110/110000000/011000000/001111110',
'f':'000111100/001100110/001100000/011111100/001100000/001100000/001100000/001100000/001100000/001100000',
'g':'000000000/000000000/000000000/001111110/011001110/110000110/110000110/011001110/001111110/000000110/000000110/011001110/001111100',
'h':'110000000/110000000/110000000/111111100/111001110/110000110/110000110/110000110/110000110/110000110',
'i':'001100000/001100000/000000000/011100000/001100000/001100000/001100000/001100000/001100000/011110000',
'j':'000110000/000110000/000000000/001110000/000110000/000110000/000110000/000110000/000110000/000110000/000110000/110110000/011100000',
'k':'110000000/110000000/110000000/110001100/110011000/110110000/111100000/110110000/110011000/110001100',
'l':'011100000/001100000/001100000/001100000/001100000/001100000/001100000/001100000/001100000/011110000',
'm':'000000000/000000000/000000000/111011100/111111110/110110110/110110110/110110110/110110110/110110110',
'n':'000000000/000000000/000000000/111111100/111001110/110000110/110000110/110000110/110000110/110000110',
'o':'000000000/000000000/000000000/001111100/011001110/110000110/110000110/110000110/011001110/001111100',
'p':'000000000/000000000/000000000/111111100/111001110/110000110/110000110/111001110/111111100/110000000/110000000/110000000/110000000',
'q':'000000000/000000000/000000000/001111110/011001110/110000110/110000110/011001110/001111110/000000110/000000110/000000110/000000110',
'r':'000000000/000000000/000000000/110111000/111100000/111000000/110000000/110000000/110000000/110000000',
's':'000000000/000000000/000000000/011111110/110000000/110000000/011111100/000000110/000000110/111111100',
't':'001100000/001100000/001100000/111111000/001100000/001100000/001100000/001100000/001100110/000111100',
'u':'000000000/000000000/000000000/110000110/110000110/110000110/110000110/110000110/111001110/011111110',
'v':'000000000/000000000/000000000/110000110/110000110/110000110/011001100/011001100/001111000/000110000',
'w':'000000000/000000000/000000000/110000110/110000110/110110110/110110110/110110110/111111110/011011100',
'x':'000000000/000000000/000000000/110000110/011001100/001111000/000110000/001111000/011001100/110000110',
'y':'000000000/000000000/000000000/110000110/110000110/110000110/011001110/001111110/000000110/000000110/000001100/000111000/011110000',
'z':'000000000/000000000/000000000/111111110/000001110/000011100/000110000/001100000/011000000/111111110'}
LOWER={k.strip():v for k,v in LOWER.items()}
MARKS={'\u0300':((1,1),(2,0)),'\u0301':((3,0),(4,1)),'\u0302':((1,0),(2,1),(3,1),(4,0)),
'\u0303':((0,0),(1,1),(2,1),(3,0),(4,0),(5,1)),'\u0308':((1,0),(2,0),(4,0),(5,0)),
'\u0306':((1,1),(2,0),(3,0),(4,1)),'\u030a':((2,0),(1,1),(3,1),(2,2)),
'\u0304':((1,0),(2,0),(3,0),(4,0)),'\u030c':((1,1),(2,0),(3,0),(4,1)),
'\u0307':((2,0),(3,0)),'\u0309':((2,0),(3,1),(3,2))}
ALIASES={'\u00a0':' ','–':'-','—':'-','−':'-','’':"'",'‘':"'",'′':"'",'“':'"','”':'"','…':'.','•':'·'}

def rect(pen,x,y,w=CELL,h=CELL):
    pen.moveTo((x,y));pen.lineTo((x,y+h));pen.lineTo((x+w,y+h));pen.lineTo((x+w,y));pen.closePath()

def symbol(char,font,cmap):
    if ord(char)not in cmap:return None
    im=Image.new('L',(32,40));ImageDraw.Draw(im).text((2,22),char,font=font,fill=255,anchor='ls')
    pen=TTGlyphPen(None)
    for y in range(im.height):
        for x in range(im.width):
            if im.getpixel((x,y))>=96:rect(pen,35+(x-2)*CELL,(21-y)*CELL)
    return pen.glyph(),max(210,round(font.getlength(char))*CELL+70)

def glyph(char,font,cmap):
    pen=TTGlyphPen(None)
    if char in (' ','\u00a0'):return pen.glyph(),280
    seq=unicodedata.normalize('NFD',char);base=seq[0]
    pattern=LOWER.get(base)
    capital=base in ART and (base.isupper() or base.isdigit())
    if pattern or capital:
        above=any(unicodedata.combining(m)>=230 for m in seq[1:])
        if capital:
            for row,bits in enumerate(ART[base].split('/')):
                for x,bit in enumerate(bits):
                    if bit=='1':rect(pen,35+x*95,(6-row)*100,115,100)
            advance=600;top=700
        else:
            left=min(row.find('1') for row in pattern.split('/') if '1'in row)
            for row,bits in enumerate(pattern.split('/')):
                if above and base in ('i','j') and row<3:continue
                for x,bit in enumerate(bits):
                    if bit=='1':rect(pen,35+(x-left)*CELL,(9-row)*CELL)
            ink=max(row.rfind('1') for row in pattern.split('/'))+1
            advance=(ink-left)*CELL+70;top=490 if base not in 'bdfhkl' else 700
        index=0;base_advance=advance
        for mark in seq[1:]:
            if mark in ('\u0323','\u0327','\u0328'):
                rect(pen,base_advance/2-35,-140)
                if mark!='\u0323':rect(pen,base_advance/2-105,-210)
            elif mark=='\u031b':
                rect(pen,525,top-70);rect(pen,595,top);advance=max(advance,700)
            else:
                points=MARKS.get(mark)
                if points is None:return symbol(char,font,cmap)
                offset=(base_advance-(min(x for x,y in points)+max(x for x,y in points)+1)*CELL)/2
                for x,y in points:rect(pen,offset+x*CELL,top+35+index*210+y*CELL)
                index+=1
        return pen.glyph(),advance
    if unicodedata.combining(char) and char in MARKS:
        for x,y in MARKS[char]:rect(pen,-350+x*CELL,735+y*CELL)
        return pen.glyph(),0
    return symbol(ALIASES.get(char,char),font,cmap)

def build():
    original=ROOT/'assets/fonts/Barlow-Regular.ttf';font=ImageFont.truetype(str(original),14)
    with TTFont(original) as f:cmap=f.getBestCmap()
    chars=set(map(chr,range(32,127)))|set(map(chr,range(0xa0,0x250)))|set(map(chr,range(0x300,0x370)))|set(map(chr,range(0x1e00,0x1f00)))|set(ALIASES)|set(map(chr,range(0x2000,0x2200)))
    for path in (ROOT/'assets/i18n').glob('*.json'):
        chars.update(c for c in path.read_text(encoding='utf8') if ord(c)<0x3000 and not c.isspace())
    glyphs={};metrics={};mapping={}
    for char in sorted(chars):
        result=glyph(char,font,cmap)
        if result is None:continue
        g,advance=result;name=f'uni{ord(char):04X}';glyphs[name]=g;metrics[name]=(advance,35);mapping[ord(char)]=name
    glyphs['.notdef'],advance=glyph('?',font,cmap);metrics['.notdef']=(advance,35)
    order=['.notdef']+sorted(n for n in glyphs if n!='.notdef')
    fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(mapping);fb.setupGlyf(glyphs);fb.setupHorizontalMetrics({name:(metrics[name][0],getattr(g,'xMin',0)) for name,g in glyphs.items()})
    ascent=max(910,max(getattr(g,'yMax',0) for g in glyphs.values()));descent=min(-245,min(getattr(g,'yMin',0) for g in glyphs.values()))
    fb.setupHorizontalHeader(ascent=ascent,descent=descent,lineGap=0)
    fb.setupNameTable(dict(familyName='Scorer Retro',styleName='Regular',fullName='Scorer Retro',psName='ScorerRetro',uniqueFontIdentifier='Scorer Retro 1.0',version='Version 1.0',copyright='Copyright 2026 Scorer Contributors. Symbols: Copyright 2017 The Barlow Project Authors.',licenseDescription='SIL Open Font License 1.1',licenseInfoURL='https://openfontlicense.org/'))
    fb.setupOS2(sTypoAscender=ascent,sTypoDescender=descent,sTypoLineGap=0,usWinAscent=ascent,usWinDescent=-descent,sxHeight=490,sCapHeight=700,achVendID='CLMR')
    fb.setupPost();fb.setupMaxp();fb.setupHead(created=3866140800,modified=3866140800);fb.font.recalcTimestamp=False
    removeOverlaps(fb.font)
    fb.font.save(ROOT/'assets/fonts/ScorerRetro.ttf')
    (ROOT/'retro_glyphs.py').write_text('"""Generated font coverage; see tools/fonts/build_retro_font.py."""\nRETRO_CODEPOINTS=frozenset('+repr(sorted(mapping))+')\n')
    license=(ROOT/'assets/fonts/OFL-Barlow.license').read_text()
    (ROOT/'assets/fonts/OFL-ScorerRetro.license').write_text('Copyright 2026 Scorer Contributors (original Scorer Retro lettering).\n'+'\n'.join(line.rstrip() for line in license.splitlines())+'\n')
    print('Scorer Retro:',len(mapping),'glyphs; ascent/descent:',ascent,descent)
if __name__=='__main__':build()
