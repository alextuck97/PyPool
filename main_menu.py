import pygame.mouse as ms
from menu import Menu
from pygame import MOUSEBUTTONDOWN
from text_display import TextDisplay


class MainMenu(Menu):
    '''
    Main menu class. 
    Will be part of state stack, so needs update, draw, and on_event methods
    
    '''
    def __init__(self, font_dict, surf_wid, surf_hgt):
        Menu.__init__(self, font_dict, surf_wid, surf_hgt)
        
        
        self.title = TextDisplay(self.fonts["stencil_50"], "Pool")
        self.title_size = self.title.get_message().get_size()
        self.title_x = (self.surf_wid - self.title_size[0])//2
        self.title_y = self.surf_hgt // 4
        
        self.play = TextDisplay(self.fonts["stencil_30"], "Play")
        self.play_size = self.play.get_message().get_size()
        self.play_x = (self.surf_wid - self.play_size[0])//2
        self.play_y = self.surf_hgt *2// 5
        
        self.about = TextDisplay(self.fonts["stencil_30"], "About")
        self.about_size = self.about.get_message().get_size()
        self.about_x = (self.surf_wid - self.about_size[0])//2
        self.about_y = self.surf_hgt //2
        
        self.title.display()
        self.play.display()
        self.about.display()
        
        self.hiscores = font_dict["stencil_30"].render("Hi-Scores", False, (255,0,0))
        
    def update(self,time, event_queue):
        '''
        Update color of menu options
        '''
        mouse_pos = ms.get_pos()
        
        self.update_color(mouse_pos, self.play, self.play_x, self.play_y, self.play_size)
        self.update_color(mouse_pos, self.about, self.about_x, self.about_y, self.about_size)
        
        
        return False
        
    
    
    
    def draw(self, display_surface):
        '''
        
        '''
        self.title.draw(display_surface, (self.title_x,self.title_y))
        self.play.draw(display_surface, (self.play_x,self.play_y))
        self.about.draw(display_surface, (self.about_x,self.about_y))
        
        
        
        
    
    
    def on_event(self, event, event_queue):
        
        if event.type == MOUSEBUTTONDOWN:
            
            mouse_pos = ms.get_pos()
            
            if self.check_click(mouse_pos, self.play_x, self.play_y, self.play_size):
                event_queue.put("PUSH_TABLE")
            
            if self.check_click(mouse_pos, self.about_x, self.about_y, self.about_size):
                event_queue.put("PUSH_ABOUT")
            
            
        
        
        return False