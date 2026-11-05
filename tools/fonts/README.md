# Scorer Retro

Original retro text typeface, based on the approved alphabet concept. Used by
localized labels, buttons, inputs, popups, canvas HUD, newspaper and coach screens.
The splash overlays retain their original font; the main-menu logo stays an image.
Native CJK/other unsupported scripts retain their existing bundled font fallback.
Names, case, translations and saved data are unchanged.

Rebuild with Python, Pillow, fontTools and skia-pathops installed:

```sh
python tools/fonts/build_retro_font.py
```

Commit the generated TTF, coverage module and OFL licence together. These build
dependencies are not required at game runtime. Source lettering uses explicit pixel
matrices; accented Latin is composed, licensed Barlow symbols are rasterised into
vector pixels. Contours are unioned before export to prevent rendering seams.
