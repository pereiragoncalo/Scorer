# Original Scorer Press fonts

Scorer Press Display and Scorer Press Pixel are original vector fonts assembled
from hand-drawn5×7 glyph matrices for the game's newspaper. Display joins cells
and adds a forward slant; Pixel uses upright grid letterforms and lowercase.
Latin accents are constructed from combining-mark matrices. CJK and other
supported scripts use the existing Noto fonts rather than missing glyphs.

Source: `tools/fonts/build_press_fonts.py`. Build with:

```
python3 -m tools.fonts.build_press_fonts
```

The font-builder requires fontTools on the development host only. Android loads
the bundled TTF files directly. Fixed font timestamps allow reproducible output.
The complete SIL Open Font License is in `assets/fonts/OFL-ScorerPress.license`.

| File | SHA256 |
| --- | --- |
| ScorerPressPixel.ttf | 7b444f97e96f38e41658a1f48cc2e60581e7489e7727a5c1f366825972d7abe6 |
| ScorerPressDisplay.ttf | c33cf63d8f174503eea9bba468a6fe9f7b240bf69bcb06d7a862fe957ac20e1c |
| OFL-ScorerPress.license | d31ed214bfdbb25bc8ce14ef417214e695f69343e1b9adaa586f629ea0a30dfe |
