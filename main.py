import pygame
from pygame.locals import *
import pygame.draw as draw
import pygame.sprite as sp
import pool_ball
import pool_table

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.ball1 = pool_ball.PoolBall([0,0], pygame.math.Vector2(0,0))
        self.ball2 = pool_ball.PoolBall([100,300], pygame.math.Vector2(0,1))
        self.ball3 = pool_ball.PoolBall([400,150], pygame.math.Vector2(-1,1))
        self.ball4 = pool_ball.PoolBall([200,300], pygame.math.Vector2(2,2))
        self.table = pygame.transform.scale(pygame.image.load("PoolTable.png"), (round(0.78125 * self.width), round(0.7225 * self.height)))#Table graphic 
        
        self.ball_surf_w = round(0.7047* self.width)
        self.ball_surf_h = round(0.6*self.height)
        
        self.ball_surf = pygame.surface.Surface([self.ball_surf_w, self.ball_surf_h], pygame.SRCALPHA)#Legal area of ball to roll
        
        self.bumper= pool_table.PoolTable(self.ball_surf.get_rect())
        
        self.ball_surf_points = [[95,110],[107,96],[116,105],[302,105],[305,98],
                                 [317,105],[329,98],[332,105],[522,105],[531,96],
                                 [547,110], [538,119], [538,282],[547,291],[531,305], 
                                 [522,296],[332,296],[329,303],[317,296],[305,303],
                                 [302,296], [119,296], [107,305],[95,291],[104,282], [104,119]]
        
        
        
        self.ball_surf_points2 = [[0, 0.08*self.ball_surf_h],[0.03*self.ball_surf_w,0],[0.96*self.ball_surf_w,0],
                                  [self.ball_surf_w,0.07*self.ball_surf_h], [self.ball_surf_w,0.93*self.ball_surf_h],
                                  [0.96*self.ball_surf_w,self.ball_surf_h],[0.03*self.ball_surf_w,self.ball_surf_h],
                                  [0,0.93*self.ball_surf_h]]
        
        self.balls = sp.Group(self.ball1, self.ball2, self.ball3, self.ball4)
        
        #self.table = sp.Group(pool_table.PoolTable())
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        
        
    def on_loop(self,time):
        
        self.balls.update(self.ball_surf.get_rect(),time, self.balls)
        
    def on_render(self):
        
        self._display_surf.fill(pygame.Color("black"))
        self.ball_surf.fill(pygame.SRCALPHA)
        
       
        
        self._display_surf.blit(self.table,(round(0.1094 * self.width),round(0.1375 * self.height)))#Top left corner of the table graphic
        
        
        #pygame.draw.polygon(self.ball_surf, pygame.Color('red'), self.bumper.right_bumper, 1)
        self.balls.draw(self.ball_surf)
        self.bumper.render(self.ball_surf)
        self._display_surf.blit(self.ball_surf, (95,80))#Top left corner of the surface ball can be on
        
        #pygame.draw.line(self._display_surf, pygame.Color('red'), [317,105], [317,296], 1)
        
        #Convex polygons work!
       
        
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