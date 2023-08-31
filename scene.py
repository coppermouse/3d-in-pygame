
from objects import Objects
import math

objects = None
f = 0

def setup_scene():
    # make field of boxes and a teapot
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


def on_scene_update():
    global f
    f += 1
    objects.rotate_world( (0,0,1), math.sin(f/60)*-0.004 )
