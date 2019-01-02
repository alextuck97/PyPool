import queue as q
import pool_table as pt
import main_menu as mm
import about_screen as ab
import end_menu as em
import pygame.event as ev
from pygame import QUIT

class StateStack:
    '''
    Class to handle the updating, drawing, and layering of game states.
    Game states are pool table, main menu, end menu, etc.
    '''
    
    
    def __init__(self, width, height, font_dict = None):
        
        self.stack = []
        
        self.surf_wid = width
        
        self.surf_hgt = height
        
        self.event_queue = q.Queue()
        
        self.event_dict = {"PUSH_TABLE" : self.push_table, "POP" : self.pop_stack, "PUSH_MM" : self.push_main_menu, "PUSH_ABOUT" : self.push_about,
                           "PUSH_END_MENU" : self.push_end_menu, "QUIT" : self.quit}
        
        self.font_dict = font_dict
        
    def update(self, current_time):
        '''
        Update states in the stack. 
        If a state update returns False, stop updating 
        '''
        #Update the stack with stack events. i.e. push new states, pop states
        while self.event_queue.qsize() > 0:
            self.event_dict[self.event_queue.get()]()
            
        #Update the states in the stack
        for state in reversed(self.stack):
            if state.update(current_time, self.event_queue) == False:
                break    
        
    def draw(self, display_surface):
        '''
        Draw states in the stack.
        If a state draw returns False, stop drawing
        '''
        
        for state in self.stack:
            state.draw(display_surface)
                
            
    def on_event(self, event):
        '''
        Pass key board events to states until false is returned
        '''
        
        for state in reversed(self.stack):
            if state.on_event(event, self.event_queue) == False:
                break
        
    
    def set_font(self,font_dict):
        self.font_dict = font_dict
        
    def push_state(self, event):
        '''
        State stack events, not key board events
        '''
        self.event_queue.put(event)  
    
    def push_main_menu(self):
        menu = mm.MainMenu(self.font_dict, self.surf_wid, self.surf_hgt)
        self.stack.append(menu)
    
    def push_end_menu(self):
        
        table = None
        #Find the table state so the score can be gotten from it
        for state in reversed(self.stack):
            if type(state) == pt.PoolTable:
                table = state
                break
        endmen = em.EndMenu(self.font_dict, self.surf_wid, self.surf_hgt, table.get_score())
        self.stack.append(endmen)
    
    def push_about(self):
        abscreen = ab.AboutScreen(self.font_dict, self.surf_wid, self.surf_hgt)
        self.stack.append(abscreen)
    
    def push_table(self):
        table = pt.PoolTable(self.font_dict)
        self.stack.append(table)
    
    def pop_stack(self):
        state = self.stack.pop()
        del state
    
    def quit(self):
        ev.post(ev.Event(QUIT))
        
    
    