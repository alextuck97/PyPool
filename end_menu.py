from menu import Menu
from text_display import TextDisplay
import pygame.mouse as ms
from pygame import MOUSEBUTTONDOWN
import os


class EndMenu(Menu):
    '''
    Menu displayed at the end of the game
    '''
    
    
    def __init__(self,font_dict, surf_wid, surf_hgt, score):
        Menu.__init__(self, font_dict, surf_wid, surf_hgt)
        
        self.game_over = TextDisplay(self.fonts["stencil_50"], "Game Over")
        self.go_size = self.game_over.get_message().get_size()
        self.go_x = (self.surf_wid - self.go_size[0])//2
        self.go_y = self.surf_hgt // 4
        
        self.new_score = score
        self.low_score = self.get_low_score()
        
        self.play_again = TextDisplay(self.fonts["stencil_30"], "Play Again")
        self.pa_size = self.play_again.get_message().get_size()
        self.pa_x = (self.surf_wid - self.pa_size[0])//2
        self.pa_y = self.surf_hgt *2// 5
        
        self.quit = TextDisplay(self.fonts["stencil_30"], "Quit")
        self.q_size = self.quit.get_message().get_size()
        self.q_x = (self.surf_wid - self.q_size[0])//2
        self.q_y = self.surf_hgt //2
        
        #Determines if a new low score was set
        if self.new_score < self.low_score:
            self.ls_message = TextDisplay(self.fonts["stencil_30"], "New low score: " + str(self.new_score))
            self.ls_size = self.ls_message.get_message().get_size()
            self.ls_x = (self.surf_wid - self.ls_size[0])//2
            self.ls_y = self.surf_hgt *2//3
        
        else:
            self.ls_message = TextDisplay(self.fonts["stencil_30"], "Low score: " + str(self.low_score))
            self.ls_size = self.ls_message.get_message().get_size()
            self.ls_x = (self.surf_wid - self.ls_size[0])//2
            self.ls_y = self.surf_hgt *2//3
                
        self.game_over.display()
        self.play_again.display()
        self.quit.display()
        self.ls_message.display()
        
        self.set_low_score()
        
        
    def draw(self, display_surface):
        
        self.game_over.draw(display_surface, (self.go_x, self.go_y))
        self.play_again.draw(display_surface, (self.pa_x, self.pa_y))
        self.quit.draw(display_surface, (self.q_x, self.q_y))
        self.ls_message.draw(display_surface, (self.ls_x, self.ls_y))

    
    def update(self,time, event_queue):
        '''
        Update color of menu options
        '''
        mouse_pos = ms.get_pos()
        
        self.update_color(mouse_pos, self.play_again, self.pa_x, self.pa_y, self.pa_size)
        self.update_color(mouse_pos, self.quit, self.q_x, self.q_y, self.q_size)
        
        
        
        
        
        return False
        
        
    def on_event(self, event, event_queue):
        
        if event.type == MOUSEBUTTONDOWN:
            
            mouse_pos = ms.get_pos()
            
            if self.check_click(mouse_pos, self.pa_x, self.pa_y, self.pa_size):
                event_queue.put("POP")
                event_queue.put("POP")
                event_queue.put("PUSH_TABLE")
            
            if self.check_click(mouse_pos, self.q_x, self.q_y, self.q_size):
                event_queue.put("QUIT")
            
        return False
    
    
    def get_low_score(self):
        '''
        Read through how_to_play.txt to find low score
        '''
        file = open("how_to_play.txt", "r")
        
        line = None
        
        #Read file to seperation string between the rules and the low score
        while line != "###\n":
            line = file.readline()
            
        low_score = file.readline().rstrip()
        
        file.close()
        
        return int(low_score)
    
    def set_low_score(self):
        '''
        Modify how_to_play_txt with new low score
        '''
        original = open("how_to_play.txt", "r")
        new_file = open("temp.txt", "w")
        
        for line in original:
            if line != "###\n":
                new_file.write(line)
            else:
                new_file.write(line)
                break
            
        new_file.write(str(self.new_score))
        
        original.close()
        new_file.close()
        
        os.remove("how_to_play.txt")
        os.rename("temp.txt", "how_to_play.txt")
        
        
        
        
        