import pygame.math as pm
import source.pool_ball as pb

class CueBall(pb.PoolBall):
    image = None
    def __init__(self, initial_pos, num = 0, initial_vel = pm.Vector2(0,0), friction = 0, color = (255,255,255)):
        pb.PoolBall.__init__(self, initial_pos, num,initial_vel, friction, color)
        
        
        
    
    def update(self, screen_size, current_time, bumpers, pockets, sunk_stack):
        pb.PoolBall.update(self, screen_size, current_time, bumpers, pockets, sunk_stack)
        
        #Watch for issues involving the group collision
        #Perhaps cue_ball should be in the same group as other balls to easily handle collisions
        #between the two types. Difference is cue_ball has interaction with a stick.
    
    