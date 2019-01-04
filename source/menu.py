#import pygame.mouse as ms
#from pygame import MOUSEBUTTONDOWN
#from text_display import TextDisplay

class Menu:
    '''
    Menu base class
    Define methods for clicking on stuff and highlighting things the mouse is over
    '''
    
    def __init__(self, font_dict, surf_wid, surf_hgt):
        
        self.fonts = font_dict
        
        self.surf_wid = surf_wid
        self.surf_hgt = surf_hgt
        
    def update_color(self, mouse_pos, text, text_x, text_y, text_size):
        '''
        Change color of text based on mouse position
        '''
        if mouse_pos[0] > text_x and mouse_pos[0] < text_x + text_size[0] and mouse_pos[1] > text_y and mouse_pos[1] < text_y + text_size[1]:
            text.set_color((255,255,255))

        else:
            text.set_color((255,0,0))
    
    def check_click(self,mouse_pos, text_x, text_y, text_size):
        '''
        Return true if the mouse pos in over the text option
        '''
        if mouse_pos[0] > text_x and mouse_pos[0] < text_x + text_size[0] and mouse_pos[1] > text_y and mouse_pos[1] < text_y + text_size[1]:
             return True   

        else:
            return False