
import pygame
from objects import Objects
import math
from globals import g

objects = None
f = 0

floor_color = '#222225' 

sun_colors = ('#112233', '#444433')
sun_color_factor = 0.8


def setup_scene():
    # make field of boxes and a teapot
    g['camera'] = [0,0,40]
    global objects
    objects = Objects()
    for x in range(4):
        for y in range(4):
            if (x,y) == (2,3):
                tpp = (x*25-99,-180+y*25, -31)
                objects.add( 'teapot.stl', tpp, scale = 0.6)
            bp = (x*25-100,-180+y*25, -40)
            objects.add( 'box.stl', bp)

    return objects


def scene_on_key( key ):
    pass

def scene_while_key( key ):
    from globals import g
    if key == pygame.K_w:
        objects.offset_world([0,0,-1])
        g['camera'][2] += 1
    if key == pygame.K_s:
        objects.offset_world([0,0,1])
        g['camera'][2] -= 1
    if key == pygame.K_a:
        objects.rotate_world( (0,0,1), 0.02 )
    if key == pygame.K_d:
        objects.rotate_world( (0,0,1), -0.02 )
 


def on_scene_update():
    return
    return
    global f
    f += 1
    objects.rotate_world( (0,0,1), math.sin(f/60)*-0.004 )
