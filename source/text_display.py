
import pygame.font as font

class TextDisplay:
    
    def __init__(self, font, text = None, color = (255,0,0), display_time = None):
        
        self. font = font
        self.color = color
        self.text = text
        self.message = self.font.render(self.text,False, self.color)
        
        self.display_time = display_time
        self.draw_timer = 0
        self.next_update_time = 0
        self.draw_text = False
        
    def set_text(self,text):
        self.message = self.font.render(text, False, self.color)
    
    def set_color(self, color):
        self.message = self.font.render(self.text, False, color)
    
    def set_display_time(self, display_time):
        self.display_time = display_time
        
    def get_message(self):
        return self.message
        
    def display(self):
        '''
        Call when a condition is met to display the text
        '''
        self.draw_text = True
    
    def draw(self, display_surface, coords):
        '''
        
        '''
        if self.draw_text == True:
            display_surface.blit(self.message, coords)
        
    def update(self, current_time):
        '''
        If text has a timer, call update. If not, calling update is unnecessary, but harmless.
        '''
        if self.next_update_time < current_time:
            
            #Timer of the text
            if self.display_time == None:
                self.draw_text = True
            
            elif self.draw_timer > self.display_time:
                self.draw_text = False
                self.draw_timer = 0
            
            if self.draw_text == True:
                self.draw_timer += 10
            self.next_update_time += 10
        
        
        