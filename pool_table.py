import pygame.surface as srf
import pygame.image as img
import pygame.sprite as sprt
import pygame.draw as drw
import pygame.color as cl

import numpy as np

from pocket import Pocket

from pygame.sprite import Group

class PoolTable():
    image = None
    def __init__(self, ball_surf_rect):
        
        #Bumper prototypes, centered on x axis if LR or y axis if TB
        #Coordinates are so the short wall is first
        self.left_bumper = [np.array([15,-80]),np.array([15,80]),np.array([0,95]),np.array([0,-95])]
        self.right_bumper = [np.array([-15,-80]),np.array([-15,80]),np.array([0,95]),np.array([0,-95])]
        self.top_bumper = [np.array([-80,15]),np.array([80,15]),np.array([95,0]),np.array([-95,0])]
        self.bottom_bumper = [np.array([-80,-15]),np.array([80,-15]),np.array([95,0]),np.array([-95,0])]
            
        self.play_surface = ball_surf_rect
        
        self.bumper_coords = self.generate_bumper_coords(self.play_surface)
        
        self.pockets = Group(self.__initalize_pockets())
    
    def __initalize_pockets(self):
        '''
        
        '''
        corner_size = 17
        wall_size = 12
        
        corner_positions = [([4,0],corner_size), ([-4+self.play_surface.width,0],corner_size),
                     ([4, self.play_surface.height],corner_size),([-4+self.play_surface.width, self.play_surface.height],corner_size)]
        
        wall_positions = [([self.play_surface.width / 2, 0],wall_size), ([self.play_surface.width / 2, self.play_surface.height], wall_size)]
        positions = corner_positions + wall_positions
        
        pockets = [Pocket(pos[0], pos[1]) for pos in positions]
        
        return pockets
        
        
    def draw(self, __display_surface):
        '''
        
        '''
        
        
        coordinates = self.generate_bumper_coords(self.play_surface)#Generate new coordinates in case window resized
        
        for key,item in coordinates.items():
            
            drw.polygon(__display_surface, cl.Color('green'), item, 1) 
            
        self.pockets.draw(__display_surface)
        
        #drw.polygon(__display_surface, cl.Color('green'), self.left_bumper)
        
    def generate_bumper_coords(self,surface_rect):
        
        coord_dict = {}
        
        coord_dict['l'] = [coord + np.array([0, round(surface_rect.height / 2)]) for coord in self.left_bumper]
        
        coord_dict['r'] = [coord + np.array([surface_rect.width -1, round(surface_rect.height / 2)]) for coord in self.right_bumper]

        coord_dict['t1'] = [coord + np.array([round(surface_rect.width * 0.26), 0]) for coord in self.top_bumper]
        coord_dict['t2'] = [coord + np.array([round(surface_rect.width *  0.74), 0]) for coord in self.top_bumper]

        coord_dict['b1'] = [coord + np.array([round(surface_rect.width * 0.26), surface_rect.height -1]) for coord in self.bottom_bumper]
        coord_dict['b2'] = [coord + np.array([round(surface_rect.width * 0.74), surface_rect.height -1]) for coord in self.bottom_bumper]
        
        
        return coord_dict
    
    def get_bumper_coords(self):
        
        return self.bumper_coords
    
    def get_pockets(self):
        return self.pockets
        
        
        
        
        