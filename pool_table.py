import pygame.surface as srf
import pygame.image as img
import pygame.sprite as sprt
import pygame.draw as drw
import pygame.color as cl

import numpy as np

class PoolTable():
    image = None
    def __init__(self, ball_surf_rect):
        
        
        self.left_bumper = [np.array([0,-95]),np.array([10,-80]),np.array([10,80]),np.array([0,95])]
        
        
        
        self.right_bumper = [np.array([0,-80]),np.array([10,-95]),np.array([10,95]),np.array([0,80])]
        
        
        
        self.top_bumper = [np.array([-95,0]),np.array([95,0]),np.array([80,10]),np.array([-80,10])]
        
        
        
        self.bottom_bumper = [np.array([-80,0]),np.array([80,0]),np.array([95,10]),np.array([-95,10])]
            
        self.play_surface = ball_surf_rect
        
    def render(self, __display_surface):
        '''
        
        '''
        
        
        coordinates = self.get_bumper_coords(self.play_surface)
        
        for key,item in coordinates.items():
            
            drw.polygon(__display_surface, cl.Color('green'), item, 1) 
        
        #drw.polygon(__display_surface, cl.Color('green'), self.left_bumper)
        
    def get_bumper_coords(self,surface_rect):
        
        coord_dict = {}
        
        coord_dict['l'] = [coord + np.array([0, round(surface_rect.height / 2)]) for coord in self.left_bumper]
        
        coord_dict['r'] = [coord + np.array([surface_rect.width, round(surface_rect.height / 2)]) for coord in self.right_bumper]

        coord_dict['t1'] = [coord + np.array([round(surface_rect.width / 3), 0]) for coord in self.top_bumper]
        coord_dict['t2'] = [coord + np.array([round(surface_rect.width * 2 / 3), 0]) for coord in self.top_bumper]

        coord_dict['b1'] = [coord + np.array([round(surface_rect.width / 3), surface_rect.height]) for coord in self.bottom_bumper]
        coord_dict['b2'] = [coord + np.array([round(surface_rect.width * 2 / 3), surface_rect.height]) for coord in self.bottom_bumper]
        
        
        return coord_dict
        
        
        
        
        