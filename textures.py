import pygame
from warpable_surface import WarpableSurface

def color_surface(s,f,color):
    s = s.copy()
    m = pygame.Surface(s.get_size(),pygame.SRCALPHA)
    m.fill((color.r, color.g, color.b, 255*f))
    s.blit(m,(0,0))
    return s



class Textures:

    def __init__( self ):
        from main import fog_thresholds_strength
        from main import sun_thresholds
        from main import fog

        texture = pygame.image.load('box.png').convert_alpha()
        textures = dict()
        colors = { 'teapot': {} }
        for fog_index, g in enumerate( fog_thresholds_strength ):
            for sun_index, t in enumerate( sun_thresholds ):
                key = ( fog_index, sun_index )
                c = pygame.Color('#112233').lerp(pygame.Color('#444433'),(t[1]+1)/2 )

                # box texture
                mtexture = color_surface( texture, 0.8, c )
                mtexture = color_surface( mtexture, g[1], fog )
                textures[key] = WarpableSurface(mtexture)

                # colors
                colors['teapot'][key] = pygame.Color('#114433').lerp( c, 0.9 )

        self.textures = textures
        self.colors = colors


