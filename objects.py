import math
import random
from stl import mesh
import numpy as np
from numba.typed import List

def rotate(faces, normals, axis, theta ):

    # I based this code on numpy-stl rotation logic.
    # I wouldn't know how to figure out this math myself.

    # calc rotation matrix
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

    normals[:] = normals[:].dot( rotation_matrix )
    for i in range(3):
        faces[:, i] = faces[:, i].dot( rotation_matrix )

def normal_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm



class Objects:

    def __init__( self ):
        self.faces = None
        self.data = list()

    def add( self, mesh_filename, offset, scale = 4.4 ):
        _mesh = mesh.Mesh.from_file( mesh_filename )


        if mesh_filename == 'box.stl':
            _mesh.rotate( (0,0,1), random.uniform(-1,1)*0.2 )

        faces = _mesh.vectors*scale + offset
        normals = _mesh.normals
        normals = np.array([ normal_vector(c) for c in normals ])

        if self.faces is not None:
            self.faces = np.concatenate( [ self.faces, faces ], axis=0)
            self.normals = np.concatenate( [self.normals, normals ], axis=0)
        else:
            self.faces = faces
            self.normals = normals

        self.data += [0 if mesh_filename == 'box.stl' else 1 ] * len(faces)

        self.data = self.data

        self.fnd = enumerate(zip(self.faces,self.normals,self.data))

    def rotate_world(self,axis, radians):
        rotate( self.faces, self.normals, axis, radians  )


if __name__ == '__main__':
    import pygame
    import time

    objects = Objects()

    objects.add( 'box.stl', [0,100,0])
    objects.add( 'box.stl', [40,100,0])



    FPS = 60

    screen_size = (700,700)
    pygame.init()
    screen = pygame.display.set_mode( 
        screen_size, 
        #pygame.SCALED 
    )
    clock = pygame.time.Clock()

    _quit = False
    while not _quit:

        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                _quit = True
 

        j = time.time()
        for _ in range(1):
            objects.rotate_world()
        print( j - time.time())

        screen.fill(0)

        c = 350
        for face, normal in zip(objects.faces, objects.normals):
            for vertex in face:
                v = vertex
                screen.set_at( [ int( v + c ) for v in [ v[0], v[1] ] ], 'white' )
            polygon = [ [ int( v + c ) for v in [ vertex[0], vertex[1] ] ] for vertex in face   ]
            pygame.draw.polygon( screen, '#FF00FF', polygon )

            m = [ sum([ c[0] for c in polygon ])/3 for i in range(2) ]
            screen.set_at( m, 'white' )
            

            pygame.draw.line( screen, 'green', m, [ int( v*100 + +m[e] ) for e,v in enumerate([ normal[0], normal[1]   ])]    )

        clock.tick( FPS )
        pygame.display.update()


