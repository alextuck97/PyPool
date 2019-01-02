import pygame
import state_stack as ss
import pool_table

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        
        self.font_dict = {}
        #self.ball_surf_w = round(0.7047* self.width)
        #self.ball_surf_h = round(0.6*self.height)
        
        
        self.state_stack = ss.StateStack(self.width, self.height)
       
        
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        
        if pygame.font.get_init():
            self.font_dict["stencil_50"] = pygame.font.Font("STENCIL.ttf",50)
            self.font_dict["stencil_30"] = pygame.font.Font("STENCIL.ttf",30)
            self.font_dict["stencil_20"] = pygame.font.Font("STENCIL.ttf",20)
            self.font_dict["century_30"] = pygame.font.Font("CENTURY.ttf",30)
            self.font_dict["century_15"] = pygame.font.Font("CENTURY.ttf",15)
            #self.font = pygame.font.Font("STENCIL.ttf",50)
        
        self.state_stack.set_font(self.font_dict)
        
        self.state_stack.push_state("PUSH_MM")
         
        
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        else:
            self.state_stack.on_event(event)
            
        
        
    def on_loop(self,time):
        
        
        self.state_stack.update(time)
        
    def on_render(self):
        
        self._display_surf.fill(pygame.Color("black"))
        
        
        
        
        self.state_stack.draw(self._display_surf)
        
        pygame.display.update()
        
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        clock = pygame.time.Clock()
        
        while( self._running ):
            time = pygame.time.get_ticks()
            
            clock.tick(100)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(time)
            self.on_render()
        self.on_cleanup()
 
        
        
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()