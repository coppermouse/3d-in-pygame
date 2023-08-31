import pygame
import math
from functools import lru_cache

camera_height = -40

def draw_horizon():
    from main import fog_thresholds_strength
    from main import half_screen_size
    from main import fov
    from main import screen_size
    from main import fog
    screen = pygame.Surface( screen_size )


    screen.fill( fog )
    # horizon
    t = fog_thresholds_strength
    for i in range(len(t)-1):
        a = t[i+1][0]
        b = t[i][0]
        c = floor_color = pygame.Color('#222225')
        next_height = (camera_height/a) * half_screen_size[1] * (1/math.tan(math.radians(fov[1]/2))) + half_screen_size[1] 
        this_height = (camera_height/b) * half_screen_size[1] * (1/math.tan(math.radians(fov[1]/2))) + half_screen_size[1] 
        pygame.draw.rect( screen, c.lerp(fog,t[i+1][1]), (0,next_height,2000, this_height - next_height + 1 ))

    return screen
