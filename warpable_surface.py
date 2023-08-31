# ---------------------------------------- 
# file: warpable_surface.py
# author: coppermouse
# ----------------------------------------

import pygame
import numpy as np
import cv2

class WarpableSurface():

    def __init__( self, surface ):
        self.surface = surface
        w, h = self.surface.get_size()
        rgb = pygame.surfarray.pixels3d( self.surface )
        alpha = pygame.surfarray.pixels_alpha( self.surface )

        self.surface_corners = np.float32([(0, 0), (0, w), (h, w), (h, 0)])
        self.surface_rgba = np.concatenate((rgb,alpha.reshape((*rgb.shape[0:2], 1))), 2)


    def warp( self,  polygon ):

        # calc polygon rect
        mnx, mxx = float('inf'), -float('inf')
        mny, mxy = float('inf'), -float('inf')
        for p in polygon:
            mnx, mxx, mny, mxy = min(mnx, p[1]), max(mxx, p[1]), min(mny, p[0]), max(mxy, p[0])
        polygon_rect = (int(mnx), int(mny),   int(mxx - mnx),   int(mxy - mny))

        # calc perspective transform (pt)
        pt = perspective_transform = cv2.getPerspectiveTransform(
            src = self.surface_corners, 
            dst = np.float32( [ (p[1] - mnx, p[0] - mny) for p in polygon ] ),
        )

        # make final surface
        warped_rgba = cv2.warpPerspective(
            self.surface_rgba.copy(), pt, 
            dsize = polygon_rect[2:], 
            #flags = cv2.INTER_NEAREST
        )
        
        final = pygame.Surface( warped_rgba.shape[0:2], pygame.SRCALPHA  )

        # blit rgb
        warped_rgb = np.delete(warped_rgba,3,2)
        pygame.surfarray.blit_array( final, warped_rgb )

        # "blit" alpha 
        warped_a = np.delete(warped_rgba,(0,1,2),2)
        flatten_warped_a = warped_a.transpose(2,0,1)
        pygame.surfarray.pixels_alpha(final)[:] = flatten_warped_a

        pr = polygon_rect
        return final, (pr[1],pr[0])


