# ---------------------------------------- 
# file: scene.py
# author: coppermouse
# ----------------------------------------

import random
import pygame
import numpy as np
from objects import Objects
from globals import g

objects = None

floor_color = pygame.Color('#232228')

sun_colors = pygame.Color('#071d42'), pygame.Color('#626648')
sun_color_factor = 0.65
sun_thresholds = [ i/20-1 for i in range(41) ] # should (must?) start at -1 and end at +1

fog = pygame.Color('#434a55')

fog_steps = 30
fog_thresholds_strength = tuple([ tuple(( np.float32(-50-i*6), np.float32(i*(1/fog_steps)) )) for i in range(fog_steps) ] + [(np.float32(-1000),1)])
fog_thresholds = tuple( [ c[0] for c in fog_thresholds_strength ] )

sun_vector = tuple(pygame.math.Vector3( (-1,0,0) ).rotate( 45, ( 0, 0.1, 1 ) ))

def setup_scene():

    global objects
    objects = Objects()

    init_height = 40

    g['camera'] = [ 0, 0, init_height ]

    # make field of boxes and a teapot
    for x in range(4):
        for y in range(4):

            if ( x,y ) == ( 2,3 ):
                tpp = ( x*25-99, -180+y*25, -init_height + 9 )
                objects.add( 'teapot', tpp, scale = 0.6 )

            bp = ( x*25-100, -180+y*25, -init_height )
            objects.add( 'box', bp, scale = 4.4, z_rot = random.uniform(-1,1) * 0.2 )

    return objects


def scene_on_key( key ):
    pass


def scene_while_key( key ):

    if key in ( pygame.K_w, pygame.K_s ):
        f = 1 if key == pygame.K_w else -1
        n = g['camera'][2] + 1 * f

        if 10 > n > 60: return

        objects.offset_world( [ 0, 0, -1*f ] )
        g['camera'][2] = n
        

    if key in ( pygame.K_a, pygame.K_d ):
        f = 1 if key == pygame.K_a else -1

        r = 0.02*f

        n = g['camera-direction'].rotate_rad( r, (0,0,1) )  
        v = n.angle_to( [0,1,0]  )

        if abs(v) > 35: return

        g['camera-direction'] = n
        objects.rotate_world( (0,0,1), r )


def on_scene_update():
    pass


