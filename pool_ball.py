import pygame.gfxdraw as gfx
import pygame
import math






class PoolBall(pygame.sprite.Sprite):
    image = None
    
    
    def __init__(self, initial_pos, initial_vel = pygame.math.Vector2(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 8
        if PoolBall.image is None:
            BALL_IMG = pygame.Surface([2*self.radius,2*self.radius], pygame.SRCALPHA)
            gfx.filled_circle(BALL_IMG, self.radius, self.radius, self.radius, (0,255,0))
            PoolBall.image = BALL_IMG
        self.image = PoolBall.image
       
        self.x = float(initial_pos[0])
        self.y = float(initial_pos[1])
       
       
        #Keeps track of balls self has collided with in current frame
        #Used to prevent double updating
        self.prev_collisions = [None]
        
        
        
        self.vel = initial_vel
        self.next_update_time = 0
        
        
    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.image.get_rect().width, self.image.get_rect().height)
        
    
    def update(self, screen_size, current_time, group):#Screen size should be a rect
        if self.next_update_time < current_time:
            
            if self.y + 2*self.radius > screen_size.bottom : 
                self.y = screen_size.bottom - 2*self.radius
                self.vel.y = -1 * self.vel.y
                
            elif self.y < 0:
                self.y = 0
                self.vel.y = -1 * self.vel.y
                
            if self.x < 0:
                self.x = 0
                self.vel.x = -1 * self.vel.x
            
            elif self.x + 2*self.radius > screen_size.right:
                self.x = screen_size.right - 2*self.radius
                self.vel.x = -1 * self.vel.x
            
            for ball in group.sprites():#Check collision between other balls
                self_center = pygame.math.Vector2(self.x + self.radius, self.y + self.radius)
                ball_center = pygame.math.Vector2(ball.x + ball.radius, ball.y + ball.radius)
                
                collision_vector = self_center - ball_center
                
                if self != ball and pygame.math.Vector2.length(collision_vector) < 2 * self.radius:
                    self.vel, ball.vel = self.on_collision(ball)
                    
                    collision_vector.scale_to_length(2 * self.radius)
                    ball.x = self.x - collision_vector.x
                    ball.y = self.y - collision_vector.y
                        
            
            self.y += self.vel.y
            self.x += self.vel.x
            
            self.next_update_time += 10
        else:
            self.prev_collisions.clear()#Nothing was updated, so make sure this is empty
        
    def on_collision(self, ball):
        '''
        Calculate new velocities of self and the ball self collided with
        '''
        center_self = pygame.math.Vector2(self.rect.center)
        center_ball = pygame.math.Vector2(ball.rect.center)
        
        center_vector = pygame.math.Vector2.normalize(center_self - center_ball)
        
        #Returns true if this collision has already been calculated
        if center_vector in self.prev_collisions or -1 * center_vector in self.prev_collisions:
            return self.vel, ball.vel
        
        if center_vector in ball.prev_collisions or -1 * center_vector in ball.prev_collisions:
            return self.vel, ball.vel
        
        
        self.prev_collisions.append(center_vector)
        ball.prev_collisions.append(center_vector)
        
        #Phi is angle between ball centers, relative to standard x axis
        phi = math.radians((center_self - center_ball).angle_to(pygame.math.Vector2(1,0)))
        
        #Theta1 and 2 and angle of ball's velocities, relative to standard x axis
        theta1 = math.radians(self.vel.angle_to(pygame.math.Vector2(1,0)))
        theta2 = math.radians(ball.vel.angle_to(pygame.math.Vector2(1,0)))
        
        #Change initial velocities into different coordinate space
        v_xp1 = self.vel.length() * math.cos(theta1 - phi)
        v_yp1 = self.vel.length() * math.sin(theta1 - phi)
        
        v_xp2 = ball.vel.length() * math.cos(theta2 - phi)
        v_yp2 = ball.vel.length() * math.sin(theta2 - phi)
        
        #Calculate final velocities in the different coordinate space
        u_xp1 = v_xp2
        u_xp2 = v_xp1
        
        u_yp1 = v_yp1
        u_yp2 = v_yp2
        
        #Go back to original coordinates
        u_x1 = u_xp1 * math.cos(phi) - u_yp1 * math.sin(phi)
        u_y1 = -1 * (u_xp1 * math.sin(phi) + u_yp1 * math.cos(phi))
        
        u_x2 = u_xp2 * math.cos(phi) - u_yp2 * math.sin(phi)
        u_y2 = -1 *(u_xp2 * math.sin(phi) + u_yp2 * math.cos(phi))
        
        return  pygame.math.Vector2(u_x1, u_y1),pygame.math.Vector2(u_x2, u_y2)
    
    
    
def ball_init(initial_pos = None):
    '''
    Initialize list of balls to be passed to sprite.Group    
    Accepts list of initial positions
    '''
    
    the_balls = []
    
    
    if initial_pos is None:
        pass
    
    
    for pos in initial_pos:
        ball = PoolBall(pos, pygame.math.Vector2(0,0))
        the_balls.append(ball)
        
    return the_balls
    
    
    
    