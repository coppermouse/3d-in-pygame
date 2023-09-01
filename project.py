# ---------------------------------------- 
# file: main.py
# author: coppermouse
# ----------------------------------------

import math
from numba import njit

@njit( fastmath = True )
def project( faces, fov, half_screen_size, fog_thresholds, sun_thresholds, sun_vector, fnd ):

    fx = (1/math.tan(math.radians(fov[0]/2)))
    fy = (1/math.tan(math.radians(fov[1]/2)))
    for e, face_normal_type in sorted(
        fnd, # fnd contain index, faces, normals and data/type 
        key = lambda a:a[1][0][0][1] + a[1][0][0][2]*10 # <-- this solution works good with this demo
                                                        #     but this needs to be adapted to the camera
                                                        #     for a better more universal solution
    ):
        face, normal, _type = face_normal_type

        # -- build projected 2d polygon
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
                polygon.append( ( px, py ) )

            x = faces[e+1][2][0]
            y = faces[e+1][2][1]
            z = faces[e+1][2][2]
            
            # yeah, I note that there is the same code twice here, writting code like this
            # is because performance.
            px = (x/y) * half_screen_size[0] * fx + half_screen_size[0] 
            py = (z/y) * half_screen_size[1] * fy + half_screen_size[1] 
            polygon.append( ( px, py ) )

        else:

            for i in range(3):
                v = face[i]
                x,y,z = v
                px = (x/y) * half_screen_size[0] * fx + half_screen_size[0] 
                py = (z/y) * half_screen_size[1] * fy + half_screen_size[1] 
                polygon.append( ( px, py ) )
        # --

        # check if clockwise or counter-clockwise. if one of these we can skip
        # because that means we see the back of the face.
        v = 0
        for a, b in zip( polygon, polygon[1:] + [polygon[0]] ):
            v += ( b[0] - a[0] ) * ( b[1] + a[1] )
        if v < 0: continue


        # set fog
        for fti in range( len(fog_thresholds) ):
            if face[0][1] > fog_thresholds[fti]:
                break

        # set sun value
        n = normal
        v = sun_vector
        f = n[0]*v[0] + n[1]*v[1] + n[2]*v[2]

        for sti, sun_threshold in enumerate( sun_thresholds ):
            if f < sun_threshold:
                break

        yield  ( polygon, _type, (fti, sti) )


