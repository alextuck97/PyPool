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
        
        #Points along the circumference of the ball at 45 degrees from center
        self.top_left = pygame.Vector2(self.rect.centerx - (1 / math.sqrt(2)) * self.radius, self.rect.centery - (1 / math.sqrt(2)) * self.radius) 
        self.bottom_left = pygame.Vector2(self.rect.centerx - (1 / math.sqrt(2)) * self.radius, self.rect.centery + (1 / math.sqrt(2)) * self.radius)
        self.top_right = pygame.Vector2(self.rect.centerx + (1 / math.sqrt(2)) * self.radius, self.rect.centery - (1 / math.sqrt(2)) * self.radius)
        self.bottom_right = pygame.Vector2(self.rect.centerx + (1 / math.sqrt(2)) * self.radius, self.rect.centery + (1 / math.sqrt(2)) * self.radius)
        
    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.image.get_rect().width, self.image.get_rect().height)
        
    
    def __recalculate_corner_points(self):
        '''
        Called whenever the balls position is set. Else points are updated with velocity
        '''
        self.top_left = pygame.Vector2(self.rect.centerx - (1 / math.sqrt(2)) * self.radius, self.rect.centery - (1 / math.sqrt(2)) * self.radius) 
        self.bottom_left = pygame.Vector2(self.rect.centerx - (1 / math.sqrt(2)) * self.radius, self.rect.centery + (1 / math.sqrt(2)) * self.radius)
        self.top_right = pygame.Vector2(self.rect.centerx + (1 / math.sqrt(2)) * self.radius, self.rect.centery - (1 / math.sqrt(2)) * self.radius)
        self.bottom_right = pygame.Vector2(self.rect.centerx + (1 / math.sqrt(2)) * self.radius, self.rect.centery + (1 / math.sqrt(2)) * self.radius)
        
    
    def update(self, screen_size, current_time, group, table):#Screen size should be a rect
        if self.next_update_time < current_time:
            
            if self.y + 2*self.radius > screen_size.bottom : 
                self.y = screen_size.bottom - 2*self.radius
                
                self.vel.y = -1 * self.vel.y
                
            elif self.y < 0:
                self.y = 0
                
                self.vel.y = -1 * self.vel.y
            
            self.bumper_collision(table)
            
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
            
            self.__recalculate_corner_points()
            
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
    
    def bumper_collision(self, table):
        '''
        Calculate new velocities after collision with a bumper
        '''
        bumpers = table.get_bumper_coords()
        
        center_ball = pygame.Vector2(self.rect.center)
        
        bumper = bumpers['l']
        #Ball hit bumper when its in the shortest part of the bumper
        self.__left_bumper_collision(bumper, center_ball)
        
        bumper = bumpers['r']
        self.__right_bumper_collision(bumper, center_ball)
        
        for b in ['t1', 't2']:
            bumper = bumpers[b]
            self.__upper_bumper_collision(bumper, center_ball)
            
        for b in ['b1', 'b2']:
            bumper = bumpers[b]
            self.__lower_bumper_collision(bumper, center_ball)
            
    
    def __left_bumper_collision(self, bumper, center_ball):
        '''
        Detect and handle collision with left bumper
        '''
        #Long edge collision
        if center_ball.x - self.radius < bumper[0][0] and (center_ball.y >= bumper[0][1] and center_ball.y <= bumper[1][1]):
            self.vel.x = -1 * self.vel.x
            self.x = bumper[0][0]
        #Collision with upper angled bumper
        elif (center_ball.y < bumper[0][1] and center_ball.y > bumper[3][1]) and (self.bottom_left.x - self.bottom_left.y + bumper[3][1]< 0): 
                                                                                  
            self.vel.x, self.vel.y = self.__angle_bumper_collision(-45, self.vel)
            #Reset x relative to where bottom_left is so x is outside the bumper line
            self.x = self.bottom_left.y - bumper[3][1] + (1 / math.sqrt(2)) * self.radius - self.radius
            
        elif (center_ball.y > bumper[1][1] and center_ball.y < bumper[2][1]) and (self.top_left.y + self.top_left.x - bumper[2][1] < 0):
                                                                                  
            self.vel.x, self.vel.y = self.__angle_bumper_collision(45, self.vel)
            self.x = -1 * self.top_left.y + bumper[2][1] + (1 / math.sqrt(2)) * self.radius - self.radius
        
    def __right_bumper_collision(self, bumper, center_ball):
        '''
        Detect and handle collision with right bumper 
        '''
        #Long edge collision
        if center_ball.x + self.radius > bumper[0][0] and (center_ball.y >= bumper[0][1] and center_ball.y <= bumper[1][1]):
            self.vel.x = -1 * self.vel.x
            self.x = bumper[0][0] - 2*self.radius
                                                                               
                                                                                # y = -x + 466 is equation for upper bumper at default resolution
                                                                                #466 = bumper[0][0] + bumper[0}[1]
        elif (center_ball.y < bumper[0][1] and center_ball.y > bumper[3][1]) and (self.bottom_right.x + self.bottom_right.y - bumper[0][0] - bumper[0][1] > 0):
            self.vel.x, self.vel.y = self.__angle_bumper_collision(45, self.vel)
            self.x = - self.bottom_right.y + bumper[0][0] + bumper[0][1] - self.radius - (1 / math.sqrt(2)) * self.radius
                                                                                  #y = x - 242 is equation for lower bumper at defult resolution
                                                                                  #242 = bumper[2][0] - bumper[2][1]
        elif(center_ball.y > bumper[1][1] and center_ball.y < bumper[2][1]) and (self.top_right.x - self.top_right.y - bumper[2][0] + bumper[2][1] > 0):
            self.vel.x, self.vel.y = self.__angle_bumper_collision(-45, self.vel)
            self.x = self.top_right.y + bumper[2][0] - bumper[2][1] - self.radius - (1 / math.sqrt(2)) * self.radius

    def __upper_bumper_collision(self, bumper, center_ball):
        '''
        Detect and handle collision for upper bumper
        '''
        #Long edge collision
        if center_ball.y - self.radius < bumper[0][1] and (center_ball.x >= bumper[0][0] and center_ball.x <= bumper[1][0]):
            self.vel.y = -1 * self.vel.y
            self.y = bumper[0][1]
                                                                                 #Equation for angled line y = x - bumper[3][0]
        elif (center_ball.x > bumper[3][0] and center_ball.x < bumper[0][0]) and (self.top_right.x - self.top_right.y - bumper[3][0] > 0):
            self.vel.y = -1 * self.vel.y
            self.y = self.top_right.x - bumper[3][0] + (1 / math.sqrt(2)) * self.radius - self.radius
                                                                                     #y = -x + b[2][0]
        elif (center_ball.x > bumper[1][0] and center_ball.x < bumper[2][0]) and (self.top_left.y + self.top_left.x - bumper[2][0] < 0):
            self.vel.y = -1 * self.vel.y
            self.y = bumper[2][0] - self.top_left.x + (1 / math.sqrt(2)) * self.radius - self.radius
    
    def __lower_bumper_collision(self, bumper, center_ball):
        '''
        Collision with lower bumpers
        '''
        
        if center_ball.y + self.radius > bumper[0][1] and (center_ball.x >= bumper[0][0] and center_ball.x <= bumper[1][0]):
            self.vel.y = -1 * self.vel.y
            self.y = bumper[0][1] - 2 * self.radius
                                                                              #y = -x + b[3][0] + b[3][1]
        elif (center_ball.x > bumper[3][0] and center_ball.x < bumper[0][0]) and (self.bottom_right.y + self.bottom_right.x - bumper[3][0] - bumper[3][1] > 0):
            self.vel.y = -1 * self.vel.y
            self.y = bumper[3][0] + bumper[3][1] - self.bottom_right.x - self.radius - (1 / math.sqrt(2)) * self.radius
                                                                                #y = x + b[2][1] - b[2][0]
        elif (center_ball.x > bumper[1][0] and center_ball.x < bumper[2][0]) and (self.bottom_left.y - self.bottom_left.x - bumper[2][1] + bumper[2][0] > 0):
            self.vel.y = -1 * self.vel.y
            self.y = self.bottom_left.x + bumper[2][1] - bumper[2][0] - self.radius - (1 / math.sqrt(2)) * self.radius
            
    def __angle_bumper_collision(self, theta, ball_vel):
        '''
        Calculate the balls velocity of collision with an angled bumper
        Theta is the angle of rotation from the x-axis. An unrotated 
        collision surface is the x-axis, where collisions come from
        the positive y-direction.
        '''
        #Rotate the balls velocity by theta
        vel_x_r = ball_vel.x * math.cos(theta) - ball_vel.y * math.sin(theta)
        vel_y_r = ball_vel.x * math.sin(theta) + ball_vel.y * math.cos(theta)
        
        #Ball is bouncing off a 180 deg surface so only y velocity changes
        new_vel_y_r = -1 * vel_y_r
        
        #Rotate the balls new velocity back to normal coordinates
        new_vel_x = vel_x_r * math.cos(-1 * theta) - new_vel_y_r * math.sin(-1 * theta)
        new_vel_y = vel_x_r * math.sin(-1 * theta) + new_vel_y_r * math.cos(-1 * theta)
       
        return new_vel_x, new_vel_y
        
        
        
        
    
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
    
    
    
    