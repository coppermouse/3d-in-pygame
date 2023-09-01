# 3d-in-pygame

This project renders a 3d-scene in a pygame environment using nothing but Pygame and Python with the exceptions of opencv, numpy, numpy-stl. It also makes us of numba for performance the outcome would work just a a great without it except for the actual performance. At the moment it is not very easy to customize but a decent programmer should not have any problems with it. Be carful if you modify the code, it can freeze and take up a lot of memory if the objects are being rendered in a location where its projections get big which can force you to shut down the computer by turning off the power.

![image](https://github.com/coppermouse/3d-in-pygame/assets/124282214/71b14e8e-a3e9-4a16-a706-676b7edc5490)
*it wouldn't be a true demo if it didn't include utah teapot of course*


## Setup
Recommended setup:
```
cd <to project folder>
python3 -m virtualenv env
source env/bin/active
pip install -r requirements
```

## Run
(Based on the recommended setup above)
```
cd <to project folder>
source env/bin/active
python3 main.py
```

## How to move camera
You can move camera using the W,A,S,D-keys.
A,D rotates it on the Z-axis and W,S moves it up an down on the Z-axis. The Z-axis is what is consider the height on the scene.

## How to "diasable" numba
If you do not want (or can) to use numba you can remove the lines that import it and the decorator above the project method. All this can be done in the `project.py` file. Note this will make it a lot slower to run. Not using numba will make it faster to startup which is good during testing.

## Notes and credits
NOTE: I am the only contributor on this project, the other account ended up here by me entering an invalid email in one of the commits. I have rebased the entire project after I that but account still there. I give it some days, it could be a cache issue.

I do want to give credit to https://github.com/davidpendergast/pygame-utils because my WarpableSurface class was build upon its warp-method. 


