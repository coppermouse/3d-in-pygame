# ---------------------------------------- 
# file: main.py
# author: coppermouse
# ----------------------------------------

import time
import pygame
import math
from stl import mesh
import numpy as np
from numba import njit
from warpable_surface import WarpableSurface
import random
from numba.typed import List
from objects import Objects

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

@njit( fastmath = True )
def project_and_color( faces, fov, half_screen_size, fog_thresholds, sun_thresholds, sun_vector, fnd ):

    fx = (1/math.tan(math.radians(fov[0]/2)))
    fy = (1/math.tan(math.radians(fov[1]/2)))
    for e, face in sorted(fnd, key=lambda a:a[1][0][0][1] + a[1][0][0][2]*10   ):
        face, normal, _type = face

        # -- build 2d polygon
        quad = _type == 0
        polygon = []
        if quad:
            if e % 2 == 1: continue

            for i in range(3):

                x = face[i][0]
                y = face[i][1]
                z = face[i][2]

                px = (x/y) * half_screen_size[0] * fx + half_screen_size[0] 
                py = (z/y) * half_screen_size[1] * fy + half_screen_size[1] 
                polygon.append( (px,py) )

            x = faces[e+1][2][0]
            y = faces[e+1][2][1]
            z = faces[e+1][2][2]
            px = (x/y) * half_screen_size[0] * fx + half_screen_size[0] 
            py = (z/y) * half_screen_size[1] * fy + half_screen_size[1] 
            polygon.append( (px,py) )

        else:

            for i in range(3):
                v = face[i]
                x,y,z = v
                px = (x/y) * half_screen_size[0] * fx + half_screen_size[0] 
                py = (z/y) * half_screen_size[1] * fy + half_screen_size[1] 
                polygon.append( (px,py) )
        # --

        # check if clockwise or counter-clockwise. if one of these we can skip
        # because that means we see the back of the face.
        v = 0
        for a, b in zip( polygon, polygon[1:] + [polygon[0]] ):
            v += ( b[0] - a[0] ) * ( b[1] + a[1] )
        if v < 0: continue


        # set fog
        for fti in range(len(fog_thresholds)):
            c = fog_thresholds[fti]
            a = face[0][1]
            if a > c:
                break

        # set sun value
        face_vector = fv = normal
        v = sun_vector
        f = fv[0]*v[0]+fv[1]*v[1]+fv[2]*v[2]


        for sti, sun_threshold in enumerate(sun_thresholds):
            if f < sun_threshold[1]:
                break
            if f < sun_threshold[1]-0.01:
                break
            if f < sun_threshold[1]+0.01:
                break

        yield  ( polygon, _type, fti, sti )



def color_surface(s,f,color):
    s = s.copy()
    m = pygame.Surface(s.get_size(),pygame.SRCALPHA)
    m.fill((color.r, color.g, color.b, 255*f))
    s.blit(m,(0,0))
    return s


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( 
        screen_size, 
        #pygame.SCALED 
    )
    clock = pygame.time.Clock()

    objects = Objects()



    # make field of boxes and a teapot
    for x in range(4):
        for y in range(4):
            if (x,y) == (2,3):
                tpp = (x*25-99,-180+y*25, -31)
                objects.add( 'teapot.stl', tpp, scale = 0.6)
            bp = (x*25-100,-180+y*25, -40)
            objects.add( 'box.stl', bp)

    fnd = List(objects.fnd)

    # make texture and colors
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

    f = 0

    _quit = False
    while not _quit:
        f += 1
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                _quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    fov[0] += 1
                if event.key == pygame.K_p:
                    fov[0] -= 1

        fov[1] = fov[0] * ( screen_size[1] / screen_size[0] ) # <--- not sure about this one

        screen.fill( fog )

        objects.rotate_world( (0,0,1), math.sin(f/60)*-0.004 )

        # horizon
        t = fog_thresholds_strength
        for i in range(len(t)-1):
            a = t[i+1][0]
            b = t[i][0]
            c = floor_color = pygame.Color('#222225')
            next_height = (-40/a) * half_screen_size[1] * (1/math.tan(math.radians(fov[1]/2))) + half_screen_size[1] 
            this_height = (-40/b) * half_screen_size[1] * (1/math.tan(math.radians(fov[1]/2))) + half_screen_size[1] 
            pygame.draw.rect( screen, c.lerp(fog,t[i+1][1]), (0,next_height,2000, this_height - next_height + 1 ))


        # draw faces on screen
        polygons = project_and_color( 
            objects.faces, 
            tuple(fov), 
            tuple(half_screen_size),
            tuple(fog_thresholds),
            tuple(sun_thresholds),
            tuple(sun_vector),
            fnd,
        )

        for polygon, d, t,s in polygons:
            key = (t,s)
       
            _type = d
            if _type == 0: 
                warped = textures[key].warp( polygon  )
                screen.blit( *warped )
            else:
                color = colors['teapot'][key]
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


