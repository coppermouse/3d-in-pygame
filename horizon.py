# ---------------------------------------- 
# file: horizon.py
# author: coppermouse
# ----------------------------------------

import pygame
import math
from globals import g

def draw_horizon():
    from main import get_fog_thresholds_strength
    from main import half_screen_size
    from main import screen_size
    from main import fog
    from scene import floor_color

    surface = pygame.Surface( screen_size )
    fov = g['fov']
    fy = ( 1 / math.tan( math.radians( fov[1]/2 )))
    surface.fill( fog )
    floor_color = pygame.Color( floor_color )
    camera_height = g['camera'][2]
    t = get_fog_thresholds_strength()
    for i in range(len(t)-1):
        a, b = [ 
            ( -camera_height / d[0] ) * half_screen_size[1] * fy + half_screen_size[1] 
            for d in [ t[i+1], t[i] ]
        ]
        pygame.draw.rect( 
            surface, floor_color.lerp( fog, t[i+1][1] ), ( 0, a, screen_size[0], b - a + 1 ))

    return surface


