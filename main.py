# ---------------------------------------- 
# file: main.py
# author: coppermouse
# ----------------------------------------

import pygame
import math
from stl import mesh
import numpy as np
from numba import njit
from warpable_surface import WarpableSurface

FPS = 60

screen_size = ( 700, 400 )
half_screen_size = [ c//2 for c in screen_size ]
fov = [90,90]

#@njit( fastmath = True )
def project_and_color( faces, pointer_data, fov, half_screen_size ):

    polygons_and_colors = list()

    sorted_faces = sorted( enumerate(faces), key = lambda a : a[1][0][2] ) # sort by z-axis (since that is where the
                                                                           # camera points at) and just pick the first
                                                                           # vertex of the face.
                                                                           # this works good enough and is fast.
    for e, face in sorted_faces:

        quad = False

        #boxes are quads, quads work a bit different
        for pointer, _type in pointer_data:
            if e < pointer: 
                if _type == 'box': 
                    quad = True
                break


        if quad and e % 2 == 1: continue

        polygon = []
        for i in range(3 if not quad else 4):

            if i < 3:
                x = face[i][0]
                y = face[i][1]
                z = face[i][2]
            else:
                x = faces[e+1][2][0]
                y = faces[e+1][2][1]
                z = faces[e+1][2][2]


            fx = (x/z) * half_screen_size[0] * (1/math.tan(math.radians(fov[0]/2))) + half_screen_size[0] 
            fy = (y/z) * half_screen_size[1] * (1/math.tan(math.radians(fov[1]/2))) + half_screen_size[1] 
            polygon.append( (fx,fy) )

        # check if clockwise or counter-clockwise. if one of these we can skip
        # because that means we see the back of the face.
        v = 0
        for a, b in zip( polygon, polygon[1:] + [polygon[0]] ):
            v += ( b[0] - a[0] ) * ( b[1] + a[1] )
        if v > 0: continue

        # calc some kind of "norm" of the face
        surface = np.array( [
            (face[0][0],face[0][1],face[0][2]),
            (face[1][0],face[1][1],face[1][2]),
            (face[2][0],face[2][1],face[2][2]),
        ])
        n = np.array( ( 0.0,) * 3 )

        for i, a in enumerate( surface ):
            b = surface [ ( i + 1 ) % len( surface ), : ]
            n[0] += ( a[1] - b[1] ) * ( a[2] + b[2] ) 
            n[1] += ( a[2] - b[2] ) * ( a[0] + b[0] )
            n[2] += ( a[0] - b[0] ) * ( a[1] + b[1] )
        norm = np.linalg.norm(n)

        # if norm gets zero that is not good. then skip this polygon.
        if norm == 0:
            pass    
        else:

            # (hardcoded colors)
            # find if it is a teapot and if it is have another color
            color = (0,0,0)
            for pointer, _type in pointer_data:
                if e < pointer: 
                    if _type == 'teapot': 
                        color = (100,100,100)
                    if _type == 'box': 
                        color = (0,0,0)
                    break
            color_a, color_b = [color,(30,50,70)]
            
            face_vector = fv = n / norm

            # hardcoded sunvector
            v = ( 0.707, 0.707, 0 )
            
            # color factor
            f = fv[0]*v[0]+fv[1]*v[1]+fv[2]*v[2]
            f = (f+1)/2

            # lerp color by factor
            color_a = np.array( color_a )
            color_b = np.array( color_b )
            vector = color_b - color_a
            color = color_a + vector * f

            polygons_and_colors.append( ( e, polygon, color ) )

    return polygons_and_colors

meshes = list() # <-- NOTE: do not make this into a set, order is relevant
pointer = 0
pointer_data = list()

def make_box( xz ):
    global pointer
    x,z = xz
    _mesh = mesh.Mesh.from_file( 'box.stl' )
    _mesh.vectors *= 4.4
    _mesh.vectors += (x,-40,z)
    meshes.append(_mesh)
    pointer += len(_mesh.vectors)
    pointer_data.append((pointer, 'box'))


def make_teapot( xz ):
    global pointer
    x,z = xz
    _mesh = mesh.Mesh.from_file( 'teapot.stl' )
    _mesh.rotate( (1,0,0), math.pi/2 )
    _mesh.vectors *= 0.6
    _mesh.vectors += (x,-35.5,z+4.5)
    meshes.append(_mesh)
    pointer += len(_mesh.vectors)
    pointer_data.append((pointer, 'teapot'))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( 
        screen_size, 
        pygame.SCALED 
    )
    clock = pygame.time.Clock()

    # make field of boxes and a teapot
    for x in range(2):
        for y in range(2):
            if (x,y) == (2,3):
                #make_teapot((x*25-100,-180+y*25))
                pass
            make_box((x*25-100,-180+y*25))

    texture = WarpableSurface(pygame.image.load('box.png').convert_alpha())

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

        screen.fill(0x112233)

        for _mesh in meshes:
            _mesh.rotate( (0,1,0), 0.001 )

        all_faces = np.concatenate( [ c.vectors for c in meshes  ] , axis=0)

        # draw faces on screen
        for e, polygon, color in project_and_color( all_faces, tuple(pointer_data), tuple(fov), tuple(half_screen_size) ):
            pygame.draw.polygon( screen, color, polygon )

            # only texture if box            
            for pointer, _type in pointer_data:
                if e < pointer: 
                    if _type == 'box': 
                        warped = texture.warp( polygon  )
                        screen.blit( *warped )
                    break

        # horizon
        for i in range(1,20):
            h = (-40/(-200*i)) * half_screen_size[1] * (1/math.tan(math.radians(fov[1]/2))) + half_screen_size[1] 
            pygame.draw.rect( screen, 'blue', (0,h,1000,1))

        # draw overlay map (debug)
        c = 350
        k = math.tan( math.radians(fov[0])/2 )
        f = 600
        pygame.draw.polygon( screen, 'white', [(c-f*k,c-f), (c,c),(c+f*k,c-f)],1 )
        for face in all_faces:
            for vertex in face:
                v = vertex
                screen.set_at( [ int( v + c ) for v in [ v[0], v[2] ] ], 'white' )


        print(clock.get_fps())
        clock.tick( FPS )
        pygame.display.update()

    pygame.quit()


