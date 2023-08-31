import pygame
import math
from functools import lru_cache

camera_height = -40

def draw_horizon():
    from main import fog_thresholds_strength
    from main import half_screen_size
    from globals import g
    from main import screen_size
    from main import fog
    screen = pygame.Surface( screen_size )
    fov = g['fov']
    fy = (1/math.tan(math.radians(fov[1]/2)))
    screen.fill( fog )
    t = fog_thresholds_strength
    c = floor_color = pygame.Color('#222225')
    for i in range(len(t)-1):
        next_height, this_height = [ 
            (camera_height/a[0]) * half_screen_size[1] * fy + half_screen_size[1] 
            for a in [ t[i+1], t[i] ]
        ]
        pygame.draw.rect( screen, c.lerp(fog,t[i+1][1]), (0,next_height,2000, this_height - next_height + 1 ))

    return screen


