# ---------------------------------------- 
# file: objects.py
# author: coppermouse
# ----------------------------------------

import os
import math
import random
from stl import mesh
import numpy as np

# for now we hardcode the two only objects there are like this.
# in a later version this might get defined elsewhere and in a better way
objects = {
    'box': ('box.stl',0), # first argument is the location of the stl file,
                          # second argument is the "type" which is being used to:
                          # 0 = trigon, 1 = quad
                          # 0 = textured box, 1 = teapot color
                          # this needs to be mapped and configed in a smarter way later
    'teapot': ('teapot.stl',1),
}



def rotate( faces, normals, axis, theta ):

    # I based this code on numpy-stl rotation logic.
    # I wouldn't know how to figure out this math myself.

    # --- calc rotation matrix
    axis = np.asarray(axis)
    theta = 0.5 * np.asarray(theta)
    axis = axis / np.linalg.norm(axis)

    a = math.cos(theta)
    b, c, d = - axis * math.sin(theta)
    angles = a, b, c, d
    powers = [x * y for x in angles for y in angles]
    aa, ab, ac, ad = powers[0:4]
    ba, bb, bc, bd = powers[4:8]
    ca, cb, cc, cd = powers[8:12]
    da, db, dc, dd = powers[12:16]

    rotation_matrix = np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
    # ---

    normals[:] = normals[:].dot( rotation_matrix )
    for i in range(3):
        faces[:, i] = faces[:, i].dot( rotation_matrix )


def normal_vector(v):
    n = np.linalg.norm(v)
    if n == 0: return v
    return v / n


class Objects:

    def __init__( self ):
        self.data = list()
        self.faces = np.ndarray( [0,3,3], dtype = np.float64 )
        self.normals = np.ndarray( [0,3], dtype = np.float32 )


    def add( self, object_name, offset, scale, z_rot = 0 ):
        from main import get_main_path
       
        _mesh = mesh.Mesh.from_file( os.path.join( get_main_path(), objects[ object_name ][0] ))
        
        _mesh.rotate( [0,0,1], z_rot )
        faces = _mesh.vectors*scale + offset
        normals = _mesh.normals

        # for some reason the normals are not normalized after load stl...
        # so I normalize them here.
        normals = np.array( [ normal_vector(n) for n in normals ] )

        self.faces = np.concatenate( [ self.faces, faces ], axis = 0 )
        self.normals = np.concatenate( [ self.normals, normals ], axis = 0 )

        self.data += [ objects[ object_name ][1] ] * len(faces)

        self.fnd = enumerate(zip(self.faces,self.normals,self.data))


    def rotate_world( self, axis, radians ):
        rotate( self.faces, self.normals, axis, radians )


    def offset_world( self, offset ):
        self.faces += offset


if __name__ == '__main__':

    # this is a test enviroment for debuging:

    import pygame
    import time

    _objects = Objects()
    _objects.add( 'box', [0,100,0], 10 )

    FPS = 60

    screen_size = (700,700)
    pygame.init()
    screen = pygame.display.set_mode( 
        screen_size, 
    )
    clock = pygame.time.Clock()

    _quit = False
    while not _quit:

        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                _quit = True

        _objects.rotate_world( (0,0,1), 0.01 )

        screen.fill(0)

        c = 350
        for face, normal in zip(_objects.faces, _objects.normals):
            for vertex in face:
                v = vertex
                screen.set_at( [ int( v + c ) for v in [ v[0], v[1] ] ], 'white' )
            polygon = [ [ int( v + c ) for v in [ vertex[0], vertex[1] ] ] for vertex in face   ]
            pygame.draw.polygon( screen, '#FF00FF', polygon )

            m = [ sum([ c[i] for c in polygon ])/3 for i in range(2) ]
            screen.set_at( m, 'white' )
            

            pygame.draw.line( screen, 'green', m, [ 
                int( v*100 + +m[e] ) for e,v in enumerate([ normal[0], normal[1] ])] )

        clock.tick( FPS )
        pygame.display.update()


