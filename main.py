# ---------------------------------------- 
# file: main.py
# author: coppermouse
# ----------------------------------------

import pygame
import math
import numpy as np
from numba.typed import List
from textures import Textures
from project import project
from scene import setup_scene
from scene import on_scene_update
from horizon import draw_horizon
FPS = 60

screen_size = ( 700*2, 400*2 )
half_screen_size = [ c//2 for c in screen_size ]

fov = [90,90]

fog = pygame.Color(50,55,60)

# --- thresholds
steps = 30
fog_thresholds_strength = tuple([ tuple(( np.float32(-50-i*6), np.float32(i*(1/steps)) )) for i in range(steps) ] + [(-1000,1)])
fog_thresholds = tuple([ np.float32(-50-i*6) for i in range(steps) ] + [(np.float32(-1000))])

sun_thresholds = [ (i,i/20-1) for i in range(41) ]
# ---

sun_vector = tuple(pygame.math.Vector3((-1,0,0)).rotate( 45, (0,0,1) ))


movie = list()




if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( 
        screen_size, 
        #pygame.SCALED 
    )
    clock = pygame.time.Clock()

    textures = Textures()

    objects = setup_scene()
    fnd = List(objects.fnd)


    _quit = False
    while not _quit:
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                _quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    fov[0] += 1
                if event.key == pygame.K_p:
                    fov[0] -= 1

        fov[1] = fov[0] * ( screen_size[1] / screen_size[0] ) # <--- not sure about this one

        on_scene_update()
        screen.blit( draw_horizon(), (0,0) )

        # draw faces on screen
        polygons = project( 
            objects.faces, 
            tuple(fov), 
            tuple(half_screen_size),
            tuple(fog_thresholds),
            tuple(sun_thresholds),
            tuple(sun_vector),
            fnd,
        )

        for polygon, _type, key in polygons:
            if _type == 0: 
                warped = textures.textures[key].warp( polygon  )
                screen.blit( *warped )
            else:
                color = textures.colors['teapot'][key]
                pygame.draw.polygon( screen, color, polygon )

        # draw overlay map (debug)
        if 0:
            c = 350
            k = math.tan( math.radians(fov[0])/2 )
            f = 600
            pygame.draw.polygon( screen, 'white', [(c-f*k,c-f), (c,c),(c+f*k,c-f)],1 )
            for face in all_faces:
                for vertex in face:
                    v = vertex
                    screen.set_at( [ int( v + c ) for v in [ v[0], v[1] ] ], 'white' )
            pygame.draw.line( screen, 'yellow', pygame.math.Vector2(c,c) + (sun_vector[0]*-100,sun_vector[1]*-100), pygame.math.Vector2(c,c) + (sun_vector[0]*100,sun_vector[1]*100)   )


        #movie.append(screen.copy())


        if len(movie) > 386:
            break


        print(clock.get_fps())
        clock.tick( FPS )
        pygame.display.update()


    _quit = False
    while not _quit:

        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                _quit = True
 

        

        screen.blit( movie[0], (0,0) )

        movie.append(movie.pop(0))

        clock.tick( FPS )
        pygame.display.update()



    pygame.quit()


