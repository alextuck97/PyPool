import pygame.gfxdraw as gfx
import pygame.sprite as sp
import pygame

class Pocket(sp.Sprite):
    image = None
    
    
    def __init__(self, pos, size):
        
        sp.Sprite.__init__(self)
        self.radius = size
        
        
        BALL_IMG = pygame.Surface([2*self.radius,2*self.radius], pygame.SRCALPHA)
        gfx.filled_circle(BALL_IMG, self.radius, self.radius, self.radius, (0,255,0))
        Pocket.image = BALL_IMG
            
        self.image = BALL_IMG
        
        self.x = pos[0]
        self.y = pos[1]
        
        self.rect = self.image.get_rect()
        self.rect.center = pos