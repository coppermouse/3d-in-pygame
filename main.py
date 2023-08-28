# ---------------------------------------- 
# file: main.py
# author: coppermouse
# ----------------------------------------

import pygame
from stl import mesh
import numpy
import math
from numba import njit

FPS = 60

screen_size = 700 # screen can only be a square atm
half_screen_size = screen_size // 2

@njit( fastmath = True )
def project_and_color( faces ):

    polygons_and_colors = list()
    for face in  sorted( faces, key = lambda a : a[0][2] ): # sort by z-axis (since that is where the
                                                            # camera points at) and just pick the first
                                                            # vertex of the face.
                                                            # this works good enough and is fast.
        polygon = []
        for i in range(3):
            x = face[i][0]
            y = face[i][1]
            z = face[i][2]

            # some hardcoded camera offsets for now
            z -= 25
            y -= 15
            # ---

            a, b = x/z, y/z
            polygon.append( [ r * half_screen_size + half_screen_size for r in (a,b) ] )


        # check if clockwise or counter-clockwise. if one of these we can skip
        # because that means we see the back of the face.
        v = 0
        for a, b in zip( polygon, polygon[1:] + [polygon[0]] ):
            v += ( b[0] - a[0] ) * ( b[1] + a[1] )
        if v > 0: continue

        # calc some kind of "norm" of the face
        surface = numpy.array( [
            (face[0][0],face[0][1],face[0][2]),
            (face[1][0],face[1][1],face[1][2]),
            (face[2][0],face[2][1],face[2][2]),
        ])
        n = numpy.array( ( 0.0,) * 3 )

        for i, a in enumerate( surface ):
            b = surface [ ( i + 1 ) % len( surface ), : ]
            n[0] += ( a[1] - b[1] ) * ( a[2] + b[2] ) 
            n[1] += ( a[2] - b[2] ) * ( a[0] + b[0] )
            n[2] += ( a[0] - b[0] ) * ( a[1] + b[1] )
        norm = numpy.linalg.norm(n)

        # if norm gets zero that is not good. then skip this polygon.
        if norm == 0:
            pass    
        else:
            # hardcoded colors
            color_a, color_b = [(0,20,30),(30,50,70)]
            
            face_vector = fv = n / norm

            # hardcoded sunvector
            v = ( 0.707, 0.707, 0 )
            
            # color factor
            f = fv[0]*v[0]+fv[1]*v[1]+fv[2]*v[2]
            f = (f+1)/2

            # lerp color by factor
            color_a = numpy.array( color_a )
            color_b = numpy.array( color_b )
            vector = color_b - color_a
            color = color_a + vector * f

            polygons_and_colors.append( ( polygon, color ) )

    return polygons_and_colors


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( ( 700, 700 ) )
    clock = pygame.time.Clock()

    faces = mesh.Mesh.from_file( 'teapot.stl' )
    #faces = mesh.Mesh.from_file( 'guy.stl' )
    faces.vectors *= 1.4
    faces.rotate((1,0,0),math.pi/2)
    
    _quit = False
    while not _quit:
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                _quit = True
            elif event.type == pygame.KEYDOWN:
                _quit = True

        faces.rotate( (0,1,0), 0.1 )

        screen.fill(0)
        for polygon, color in project_and_color( faces.vectors ):
            pygame.draw.polygon( screen, color, polygon )

        clock.tick( FPS )
        print(clock.get_fps())

        pygame.display.update()

    pygame.quit()


