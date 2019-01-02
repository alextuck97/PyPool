from menu import Menu
from text_display import TextDisplay
import pygame.mouse as ms
from pygame import MOUSEBUTTONDOWN
import pygame
class AboutScreen(Menu):
    '''
    About screen
    Class that contains information about the game
    '''
    
    
    def __init__(self,font_dict, surf_wid, surf_hgt):
        Menu.__init__(self, font_dict, surf_wid, surf_hgt)
        
        
        
        self.game_rules = self.initialize_instructions("how_to_play.txt")
        
        self.about = TextDisplay(self.fonts["stencil_30"], "About")
        self.about_size = self.about.get_message().get_size()
        self.about_x = (self.surf_wid - self.about_size[0])//2
        self.about_y = self.surf_hgt // 6
        
        self.author = TextDisplay(self.fonts["century_15"], "Pool is a game by Alex Tuck, made with Python and the pygame module")
        self.author_size = self.author.get_message().get_size()
        self.author_x = (self.surf_wid - self.author_size[0])//2
        self.author_y = self.surf_hgt // 4
        
        
        self.how_to_play = TextDisplay(self.fonts["stencil_30"], "How to Play")
        self.htp_size = self.how_to_play.get_message().get_size()
        self.htp_x = (self.surf_wid - self.htp_size[0])//2
        self.htp_y = self.surf_hgt // 3
        
        self.exit = TextDisplay(self.fonts["stencil_20"], "Exit to Main Menu")
        self.exit_size = self.exit.get_message().get_size()
        self.exit_x = (self.surf_wid - self.exit_size[0])//2
        self.exit_y = self.surf_hgt * 3 //5
        
        self.about.display()
        self.author.display()
        self.how_to_play.display()
        self.exit.display()
        
        
    def initialize_instructions(self, file_name):
        '''
        Create texDisplay objects for the games instructions
        '''
        instructions = open(file_name, 'r')
        
        game_rules = []
        
        for line in instructions:
            if line == "###\n":#Denotes end of instructions
                break
            line = line.rstrip()
            text = TextDisplay(self.fonts["century_15"], line)
            text.display()
            game_rules.append(text)
            
        instructions.close()
        
        return game_rules
    
    def draw(self, display_surface):
        
        display_surface.fill(pygame.Color("black"))
        
        self.about.draw(display_surface, (self.about_x, self.about_y))
        self.author.draw(display_surface, (self.author_x, self.author_y))
        self.how_to_play.draw(display_surface, (self.htp_x, self.htp_y))
        
        game_rule_size = self.game_rules[0].get_message().get_size()
        
        game_rule_x = self.surf_wid // 10
        game_rule_y = self.htp_y + (3 * game_rule_size[1]) // 2
        
        for rule in self.game_rules:
            rule.draw(display_surface, (game_rule_x, game_rule_y))
            game_rule_y += game_rule_size[1]
        
        
        self.exit.draw(display_surface, (self.exit_x, self.exit_y))

    
    def update(self,time, event_queue):
        '''
        Update color of menu options
        '''
        mouse_pos = ms.get_pos()
        
        self.update_color(mouse_pos, self.exit, self.exit_x, self.exit_y, self.exit_size)
        
        
        return False
        
        
    def on_event(self, event, event_queue):
        
        if event.type == MOUSEBUTTONDOWN:
            
            mouse_pos = ms.get_pos()
            
            if self.check_click(mouse_pos, self.exit_x, self.exit_y, self.exit_size):
                event_queue.put("POP")
            
            
        
        
        
        return False
        
        
        
            
    