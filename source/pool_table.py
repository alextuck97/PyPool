import pygame.draw as drw
import pygame.color as cl
import pygame.math as pm
import pygame.mouse as ms
import pygame
import numpy as np
from source.stick import Stick
from source.cue_ball import CueBall
from source.pocket import Pocket
from source.pool_ball import PoolBall
from source.text_display import TextDisplay
from pygame.sprite import Group


class PoolTable():
    '''
    Class that contains the pool table and all things that happen on it (balls, pockets)
    Initialized with the display surface it is drawn to, and the coordinates of the top left
    corner of the surface, relative to the window.
    '''
    image = None
    def __init__(self, font_dict):
        
        #Bumper prototypes, centered on x axis if LR or y axis if TB
        #Coordinates are so the short wall is first
        self.left_bumper = [np.array([15,-80]),np.array([15,80]),np.array([0,95]),np.array([0,-95])]
        self.right_bumper = [np.array([-15,-80]),np.array([-15,80]),np.array([0,95]),np.array([0,-95])]
        self.top_bumper = [np.array([-80,15]),np.array([80,15]),np.array([95,0]),np.array([-95,0])]
        self.bottom_bumper = [np.array([-80,-15]),np.array([80,-15]),np.array([95,0]),np.array([-95,0])]
        
        self.fonts = font_dict
        
        self.ball_surf_w = 450
        self.ball_surf_h = 225
        self.ball_surf_origin = self.x_orig, self.y_orig = 95,80
        self.ball_surf = pygame.surface.Surface([self.ball_surf_w, self.ball_surf_h], pygame.SRCALPHA)#Legal area of ball to roll
        
        
        #self.ball_surf_origin = ball_surf_origin
        
        self.play_surface = self.ball_surf.get_rect()
        #self.play_surface = ball_surf_rect
        
        self.scratch = TextDisplay(self.fonts["stencil_50"], "Scratch", display_time=750)
        
        self.strokes = 0
        
        self.score = TextDisplay(self.fonts["century_15"], "Strokes: " + str(self.strokes))
        self.score_size = self.score.get_message().get_size()
        self.score.display()
        
        self.bumper_coords = self.generate_bumper_coords(self.play_surface)
        self.pockets = Group(self.__initalize_pockets())
        self.cue_ball = CueBall([375,100], initial_vel=pm.Vector2(0,0), friction = 0.01)
        self.balls = Group(self.__initialize_balls(), self.cue_ball)#care
        self.stick = Stick(self.ball_surf_origin)
        self.update_stick = True
        
        self.sunk_stack = [PoolBall([0,0], num = np.Inf)]#Contains balls sunk and the order they were sunk in. Dummy ball at bottom
        self.last_sunk = None#Flag for top of stack before cue_ball was sunk. In case of scratch, pop down
        #sunk stack until this is hit
        
        self.mouse_pos_on_click = None
        self.play_stick_animation = False
    
    def __initalize_pockets(self):
        '''
        
        '''
        corner_size = 17#Corner pocket radius?
        wall_size = 12#Wall pocket radius?
        
        corner_positions = [([4,0],corner_size), ([-4+self.play_surface.width,0],corner_size),
                     ([4, self.play_surface.height],corner_size),([-4+self.play_surface.width, self.play_surface.height],corner_size)]
        
        wall_positions = [([self.play_surface.width / 2, 0],wall_size), ([self.play_surface.width / 2, self.play_surface.height], wall_size)]
        positions = corner_positions + wall_positions
        
        pockets = [Pocket(pos[0], pos[1]) for pos in positions]
        
        return pockets
       
    
    def __initialize_balls(self):
        '''
        Place balls in the starting triangle
        '''
        ball_list = []
        
        colors  = [(218,135,32),(0,0,255),(255,0,0), (218,112,114),(255,165,0),(34,139,34),(178,34,34), (160,32,240)]
        
        colors += colors
        
        for i in range(1,16):
            ball_list.append(PoolBall([0,0], num = i, color=colors[i]))
            
        self.ball_reracker((110,100), ball_list, 'l')
        
        return ball_list
    
    def ball_reracker(self, head, balls,orientation = 'l'):
        '''
        Return a list of balls in a triangle formation. Used for placing balls on table when a scratch occurs.
        head: point of lead ball
        balls: list of balls to find new positions for 
        orientation: direction from head ball the triangle flows. 'l' = left, 'r' = right
        '''
        if orientation == 'l':
            sign = -1
        elif orientation == 'r':
            sign = 1
        else:
            return
        
        point = head
        
        place = 0#Holds which ball's position is modified next
        
        if len(balls) > 0:
        
            for column in range(1,6):
            
                if column % 2 != 0:#How far off from the center ball the furthest ball is in the column
                    offset = column // 2 
                else:
                    offset = column // 2 - 0.5
                for j in range(0,column):  
                
                    x = point[0] + sign * (column-1) * 15
                    y = point[1] + offset * 16 - j * 16
                
                    balls[place].set_pos(x, y)
                    place += 1
                #Return if place is out of index
                    if len(balls) == place:
                        return balls
        
        return balls
        
    
    def update(self, time, event_queue):
        '''
        
        '''
        #Remove balls from pockets if cue ball is sunk. Balls_still_moving should only be called if cue_ball is sunk.
        if self.cue_ball.get_sunk() and not self.balls_still_moving():
            self.strokes += 1 #Penalty for sinking cue ball
            self.cue_ball_sunk()
        #Movement of balls
        self.balls.update(self.play_surface,time, self.get_bumper_coords(), self.get_pockets(), self.sunk_stack)
        
        self.score.set_text("Score: " + str(self.strokes))
        
        prev_play_stick_animation = self.play_stick_animation
        
        #Stick does not update position if play_stick_animation is false
        if self.update_stick == True:#Flag to prevent stick from updating when end game menu is displayed. Crashes otherwise
            self.play_stick_animation = self.stick.update(self.play_surface,time, self.play_stick_animation, self.cue_ball.get_pos(), self.mouse_pos_on_click)
        
        self.scratch.update(time)
        
        #If the stick animation was playing when update was called, but set to false after stick.update,
        #the cue ball has been struck, so update its velocity.
        if prev_play_stick_animation == True and self.play_stick_animation == False:
            
            vel = self.stick.new_cb_vel(self.cue_ball.get_pos(), self.mouse_pos_on_click)
            self.cue_ball.set_velocity(vel)#Velocity needs to be set after stick animation is over
        
        if not self.cue_ball.get_sunk() and len(self.sunk_stack) > 15:
            event_queue.put("PUSH_END_MENU")
            self.update_stick = False
        
        
        return False  
            
                
            
        
    
    def draw(self, __display_surface):
        '''
        Draws table, balls, pockets
        '''
        __display_surface.fill(pygame.Color("black"))
        
        self.ball_surf.fill((0,220,100))
        
        coordinates = self.generate_bumper_coords(self.play_surface)#Generate new coordinates in case window resized (Resize not implemented)
        
        for key,item in coordinates.items():
            
            drw.polygon(self.ball_surf, cl.Color('black'), item, 1) 
            
        self.pockets.draw(self.ball_surf)
        self.balls.draw(self.ball_surf)
        __display_surface.blit(self.ball_surf, self.ball_surf_origin)
        #__display_surface.blit(self.scratch, (220,170))
        
        self.score.draw(__display_surface, (__display_surface.get_width() - 2* self.score_size[0], self.score_size[1]))
        self.scratch.draw(__display_surface, (220,170))
        
        #Draw stick last so it is drawn above the ball surface
        if not self.balls_still_moving():
            self.stick.draw(__display_surface, self.play_stick_animation, self.cue_ball.get_pos())
        
        
        
    def generate_bumper_coords(self,surface_rect):
        
        coord_dict = {}
        
        coord_dict['l'] = [coord + np.array([0, round(surface_rect.height / 2)]) for coord in self.left_bumper]
        
        coord_dict['r'] = [coord + np.array([surface_rect.width -1, round(surface_rect.height / 2)]) for coord in self.right_bumper]

        coord_dict['t1'] = [coord + np.array([round(surface_rect.width * 0.26), 0]) for coord in self.top_bumper]
        coord_dict['t2'] = [coord + np.array([round(surface_rect.width *  0.74), 0]) for coord in self.top_bumper]

        coord_dict['b1'] = [coord + np.array([round(surface_rect.width * 0.26), surface_rect.height -1]) for coord in self.bottom_bumper]
        coord_dict['b2'] = [coord + np.array([round(surface_rect.width * 0.74), surface_rect.height -1]) for coord in self.bottom_bumper]
        
        
        return coord_dict
    
    def balls_still_moving(self):
        '''
        Return true if a pool ball is still moving
        '''
        
        for ball in self.balls.sprites():
            if ball.get_vel_mag() != 0:
                return True
        
        return False
    
    def get_bumper_coords(self):
        return self.bumper_coords
    
    def get_pockets(self):
        return self.pockets
    
    def get_balls(self):
        return self.balls
    
    def get_sunk(self):
        return self.sunk_stack
    
    def __get_all_sunk(self):
        '''
        Return all balls on sunk stack, except  for dummy at the bortom.
        Testing purposes only.
        '''
        popped_list = []
        
        for i in range(1, len(self.sunk_stack)):
            popped_list.append(self.sunk_stack.pop())
        
        return popped_list
        
    
    def get_sunk_on_turn(self):
        '''
        Returns all balls sunk on a given turn
        '''
        popped_list = []
        while self.sunk_stack[-1].get_num() is not self.last_sunk:
            popped_list.append(self.sunk_stack.pop())
            
        return popped_list
    
    def ball_overlap(self, popped_list):
        '''
        Check if any balls replaced on table overlap balls already on table
        Goes through all the balls and checks if they overlap. Not very efficient.
        
        Not fully Tested. Works in trivial cases.
        '''
        add_to_rerack = []
        
        for new_ball in popped_list:
            ball_center = pm.Vector2(new_ball.x + new_ball.radius, new_ball.y + new_ball.radius)
            
            for existing_ball in self.balls:
                existing_center = pm.Vector2(existing_ball.x + existing_ball.radius, existing_ball.y + existing_ball.radius)
                
                collision_vector = ball_center - existing_center
                
                
                
                #If the balls are pretty close, add the existing ball to the list to be reracked
                if collision_vector.length() < 2* new_ball.radius:
                    self.balls.remove(existing_ball)
                    existing_ball.vel = pm.Vector2(0,0)
                    add_to_rerack.append(existing_ball)
                #If the balls are still overlapped but not by a lot, simply move the existing one out of the way.
                #Will cause a mess if many balls in same place, but that generally will not happen.
                #elif collision_vector.length() < 2 * new_ball.radius:
                 #   collision_vector.scale_to_length(2 * new_ball.radius)
                 #   existing_ball.x = new_ball.x - collision_vector.x
                 #   existing_ball.y = new_ball.y - collision_vector.y
        
        return add_to_rerack 
        
    def cue_ball_sunk(self):
        '''
        Sequence of events that happens when the cue ball is sunk
        '''
        self.scratch.display()
        #popped_list = self.__get_all_sunk()
        popped_list = self.get_sunk_on_turn() 
             
        for ball in popped_list:
            ball.ball_unsunk()
            
        popped_list.remove(self.cue_ball)
        
        #If a cue ball overlaps  if should be taken care of in pool_ball update    
        self.cue_ball.set_pos(300,110)
        
        popped_list = self.ball_reracker([100,110], popped_list, 'l')

        
            
        #continue reracking until its nothing overlaps.
        #Add to rerack is a list that is added to if two balls occupy the same location
        #Otherwise, balls are simply scooted apart     
        while True:
            add_to_rerack = self.ball_overlap(popped_list)
            if len(add_to_rerack) == 0:
                break
            
            popped_list += add_to_rerack
        
            popped_list = self.ball_reracker([100,110], popped_list, 'l')
        
        self.balls.add(popped_list, self.cue_ball)
        
    def get_score(self):
        return self.strokes
    
    def on_event(self, event, event_queue):
        
        #HIt ball with stick
        if event.type == pygame.MOUSEBUTTONDOWN and not self.balls_still_moving():
            self.last_sunk = self.sunk_stack[-1].get_num()
            self.mouse_pos_on_click = ms.get_pos()
            self.play_stick_animation = True
            self.strokes += 1
            
        return False
        
        
        
        
        