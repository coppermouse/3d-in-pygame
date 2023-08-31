# ---------------------------------------- 
# file: textures.py
# author: coppermouse
# ----------------------------------------

import pygame
from warpable_surface import WarpableSurface

def color_surface( surface, factor, color ):
    surface = surface.copy()
    color_mask = pygame.Surface( surface.get_size(), pygame.SRCALPHA )
    color_mask.fill( ( color.r, color.g, color.b, 255 * factor ))
    surface.blit( color_mask, (0,0) )
    return surface


class Textures:

    def __init__( self ):

        # Textures at the moment just loads one texture (box) and one color (teapot).
        # This is hard coded. In a later version this should of course be a lot more dynamic
        # and based on some kind of config somewhere.

        from main import get_fog_thresholds_strength
        from main import get_sun_thresholds
        from main import get_fog
        from scene import sun_colors
        from scene import sun_color_factor
        
        sun_color_a, sun_color_b = sun_colors
        fog = get_fog()

        box_texture = pygame.image.load('box.png').convert_alpha()
        teapot_color = '#114433'

        self.textures = { 'box': {} }
        self.colors = { 'teapot': {} }

        # every color and texture stores all its combination of environmental colors (fog and sun)
        for fog_index, fog_threshold_strength in enumerate( get_fog_thresholds_strength() ):
            for sun_index, sun_threshold in enumerate( get_sun_thresholds() ):

                _, fog_strength = fog_threshold_strength

                sun_fog = ( fog_index, sun_index )
                sun_color = pygame.Color(
                    sun_color_a).lerp(pygame.Color(sun_color_b),(sun_threshold+1)/2 )

                # box texture
                texture = color_surface( color_surface(
                    box_texture, sun_color_factor, sun_color ),  fog_strength, fog )
                self.textures['box'][sun_fog] = WarpableSurface( texture )

                # teapot color
                self.colors['teapot'][sun_fog] = pygame.Color( teapot_color ).lerp( 
                    sun_color, sun_color_factor ).lerp( fog, fog_strength )


    def get( self, key, fog_sun ):
        if key == 'teapot':
            return ( self.colors['teapot'][fog_sun], 'color' )
        elif key == 'box':
            return ( self.textures['box'][fog_sun], 'texture' )


