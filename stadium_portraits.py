"""Six image-generated stadium portraits, framed from an immutable source atlas."""
from club_profiles import stadium_variant
from retro_props import SceneTextures
VARIANTS=('local','compact','covered','bowl','double','major')

def portrait(game,capacity,palette):
    if not hasattr(game,'_stadium_portrait_textures'):game._stadium_portrait_textures=SceneTextures(limit=2)
    atlas=game._stadium_portrait_textures.get('stadium_portraits.png',palette)
    index=VARIANTS.index(stadium_variant(capacity));width,height=atlas.width//3,atlas.height//2
    # Texture regions are viewports, not rewritten/cropped source image files.
    region=atlas.get_region((index%3)*width,(1-index//3)*height,width,height)
    region.mag_filter=region.min_filter='nearest'
    return region
