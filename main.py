# ---------------------------------------- 
# file: main.py
# author: coppermouse
# ----------------------------------------

import os
import pygame
import math
from numba.typed import List
from textures import Textures
from project import project
from scene import setup_scene
from scene import scene_on_key
from scene import scene_while_key
from scene import on_scene_update
from horizon import draw_horizon
from globals import g

FPS = 60

screen_size = ( 700*2, 400*2 )
half_screen_size = [ c//2 for c in screen_size ]


def get_main_path():
    return os.path.dirname( os.path.realpath(__file__) ) 


def get_sun_vector():
    from scene import sun_vector
    return sun_vector


def get_fog():
    from scene import fog
    return fog


def get_fog_thresholds_strength():
    from scene import fog_thresholds_strength
    return fog_thresholds_strength


def get_fog_thresholds():
    from scene import fog_thresholds
    return fog_thresholds


def get_sun_thresholds():
    from scene import sun_thresholds
    return sun_thresholds


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode( screen_size )
    clock = pygame.time.Clock()

    textures = Textures()
    objects = setup_scene()
    fnd = List( objects.fnd )

    keys_down = set()

    _quit = False
    while not _quit:

        for event in  pygame.event.get():
            
            if event.type == pygame.QUIT:
                _quit = True

            elif event.type == pygame.KEYDOWN:

                scene_on_key( event.key )

                keys_down.add( event.key )

                if event.key == pygame.K_o:
                    fov[0] += 1
                if event.key == pygame.K_p:
                    fov[0] -= 1

            elif event.type == pygame.KEYUP:
                keys_down.discard( event.key )


        for key in keys_down:
            scene_while_key( key )


        g['fov'][1] = g['fov'][0] * ( screen_size[1] / screen_size[0] ) # <--- not sure about this one
                                                                        #      but it looks kind of right
        on_scene_update()

        screen.blit( draw_horizon(), (0,0) )

        # draw faces on screen
        polygons = project( 
            objects.faces, 
            tuple( g['fov'] ), 
            tuple( half_screen_size ),
            tuple( get_fog_thresholds() ),
            tuple( get_sun_thresholds() ),
            tuple( get_sun_vector() ),
            fnd,
        )

        for polygon, _type, key in polygons:

            # this is a very hard coded solution. it works for this first demo...
            if _type == 0: 
                warped = textures.get('box',key)[0].warp( polygon  )
                screen.blit( *warped )
            else:
                color = textures.get( 'teapot', key )[0]
                pygame.draw.polygon( screen, color, polygon )

        # draw overlay map (debug)
        if 0:
            c = 700
            k = math.tan( math.radians( g['fov'][0])/2 )
            pygame.draw.polygon( screen, 'white', [ (0,0), (c,c), (c*2*k,0) ], 1 )
            for face in objects.faces:
                for vertex in face:
                    v = vertex
                    screen.set_at( [ int( v + c ) for v in [ v[0], v[1] ] ], 'white' )
            
            sun_vector_center = svc = pygame.math.Vector2(c,c//2)
            sub_vector_length = svl = -100 # actual its half length
            sv = get_sun_vector()
            pygame.draw.line(
                screen, 'yellow', *[ svc + ( sv[0]*-svl*f, sv[1]*-svl*f ) for f in [-1,1] ] )


        print(clock.get_fps())
        clock.tick( FPS )
        pygame.display.update()


