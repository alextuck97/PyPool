import pygame.sprite as sp
import pygame.mouse as ms
import pygame.draw as drw
import pygame.color as cl
import pygame.math as pm
import cue_ball

class Stick(sp.Sprite):
    '''
    Stick and related functionality
    Initialized with origin of the ball surface for ease of converting
    between display surface coords and ball surface coords. Necessary
    because the stick is drawn to display surface so it may be drawn
    beyond the actual table.
    '''
    def __init__(self, ball_surf_origin):
        sp.Sprite.__init__(self)
        
        self.offset = pm.Vector2(ball_surf_origin)
        
        self.cue_tip_pts = None#Both sets of points initialized in first update
        
        self.stick_pts = None
        
        self.dashed_p1 = None#Both are points used to draw the dashed line extending beyond the cursor
        
        self.dashed_p2 = None
        
        self.next_update_time = 0
        
        self.max_dist = 200
        
    def new_cb_vel(self, ball_coords, mouse_pos):
        '''
        Get the new cue_ball velocity after it is struck.
        '''
        
        tip_x, tip_y =  mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1]
        
        distance = pm.Vector2(ball_coords[0] - tip_x, ball_coords[1] - tip_y)
        
        direction = distance.normalize()
        #The magnitude of the new velocity is a function of the distance between ball and cue tip. 
        #Divide by 50 is arbitrary.
        
        if distance.length() > self.max_dist:#Cap velocity
            magnitude = 10
        else:    
            magnitude = distance.length() / 20
        
        vel = direction * magnitude
        return vel 
    
    def update(self, __display_surface,current_time, play_stick_animation, cue_ball_pos, mouse_pos_on_click):
        '''
        Update position of the stick. The stick is only updated if play stick animation is true.
        '''
        continue_stick_animation = False
        if self.next_update_time < current_time:
            
            
            
            if play_stick_animation == True:
                continue_stick_animation = self.__stick_animation(cue_ball_pos,mouse_pos_on_click)
            else:
                self.__update_stick_coords(cue_ball_pos)
                self.__update_dashed_coords(cue_ball_pos)
            
            
            
            
            
            self.next_update_time += 10
            
        return continue_stick_animation   
            
        
    
    def draw(self, __display_surface, play_stick_animation, cue_ball_pos):
        '''
        Draws stick and related stuff. Uses cue_ball_pos to figure orientation of the stick.
        Dashed line is drawn to display surface so it can extend beyond the table
        '''
        if not play_stick_animation:
            self.__draw_dashed(__display_surface, cue_ball_pos)
        
        self.__draw_stick(__display_surface)

    def __draw_dashed(self, __display_surface, cue_ball_pos):
        '''
        Draws the dashed line from the cursor to the cue ball
        
        Also draws a rough trajectory of the ball. No information given on how for it will travel
        '''
        
        line_30 = self.dashed_p1 - self.dashed_p2#Line for updating dashes
        line_30.scale_to_length(30)
        mouse_pos = pm.Vector2(ms.get_pos() - self.offset)
        drw.circle(__display_surface, (255,255,255), [round(self.dashed_p1.x), round(self.dashed_p1.y)], 8,1)
        
        
        if mouse_pos.distance_to(cue_ball_pos) > self.max_dist:#Limit the distance the stick can be drawn
            line_200 = self.dashed_p1 - self.dashed_p2
            line_200.scale_to_length(200)
            mouse_pos = cue_ball_pos - line_200
        
        #Draw dashed lines until hit the mouse cursor
        while mouse_pos.distance_to(self.dashed_p2 - self.offset) > 15:
            drw.line(__display_surface, (255,255,255), self.dashed_p1, self.dashed_p2, 1)
            self.dashed_p1 = self.dashed_p1 - line_30
            self.dashed_p2 = self.dashed_p2 - line_30
        
        
        
    def __draw_stick(self,__display_surface):
        '''
        Draw the stick
        '''
        
        drw.polygon(__display_surface, (255,255,255), self.cue_tip_pts)#White
        drw.polygon(__display_surface, (131,81,69), self.stick_pts)#Brown color
    
    def __update_dashed_coords(self, cue_ball_pos):
        '''
        Update the two initial points used for drawing the dashed line of the stick
        Offset is the upper-left corner of the table. Used to alternate between ball_surface coords
        and display_surface coords.
        '''
        mouse_pos = pm.Vector2(ms.get_pos() - self.offset)#Change mouse_pos into ball surface coordinates
        
        line_dir = (mouse_pos.x - cue_ball_pos[0], mouse_pos.y - cue_ball_pos[1])#Direction of the line to be drawn
        
        #Prevent a divide by zero error
        if pm.Vector2(line_dir).length() == 0:
            return
        
        #Line of length 15. This is what is actually drawn
        line_15 = pm.Vector2(line_dir)
        line_15.scale_to_length(15)
        
        #Line of length 30. Used the move the line of length 15 to give the dashed line effect
        line_30 = pm.Vector2(line_dir)
        line_30.scale_to_length(30)
        
        #Line of length 60 to be used to draw ball outline on other side of cue ball
        line_80 = pm.Vector2(line_dir)
        line_80.scale_to_length(80)
        
        cue_ball_pos = pm.Vector2(cue_ball_pos) + self.offset#Transfor cueball coords from ball surf into display surface coords
        
        self.dashed_p1 = cue_ball_pos - line_80 #Point 80 units behind cue ball
        
        self.dashed_p2 = self.dashed_p1 + line_15 #Point 15 units behind point 1
    
    def __update_stick_coords(self,cue_ball_pos): 
        '''
        Updates the location of the stick shape for drawing
        
        '''
        mouse_pos = pm.Vector2(ms.get_pos() - self.offset)#Change mouse_pos into ball surface coordinates
        
        line_dir = pm.Vector2(mouse_pos.x - cue_ball_pos[0], mouse_pos.y - cue_ball_pos[1])#Direction of the line to be drawn
        
        if line_dir.length() == 0:
            return
        
        if mouse_pos.distance_to(cue_ball_pos) > self.max_dist:#Limit the distance the stick can be drawn
            line_200 = line_dir
            line_200.scale_to_length(200)
            mouse_pos = cue_ball_pos + line_200
        
        line_15 = line_dir
        
        line_15.scale_to_length(15)
        
        orthogonal = self.__get_orthogonal(line_dir)
        
        orthogonal.scale_to_length(2)
        
        p1 = mouse_pos - orthogonal + self.offset
        p2 = mouse_pos + orthogonal + self.offset
        p3 = p2 - line_15
        p4 = p3 - 2*orthogonal
        
        self.cue_tip_pts = [p1,p2,p3,p4]
        
        line_150 = line_15
        line_150.scale_to_length(150)
          
        
        
        p5 = p1 + line_150
        
        p6 = p2 + line_150
            
        self.stick_pts = [p1,p2,p6,p5]  
        
        
    def __stick_animation(self,cue_ball_pos, mouse_pos_on_click):
        '''
        Move the stick toward the cue_ball. Cue ball begins movement
        after this the stick hits the ball.
        Returns true if this is to be continued, else returns false. Because
        everything is passed by reference, the False return should make 
        pool_table.play_stick_animation false.
        '''
        #Doesnt work. I believe the issue lies in the ordering of events in pool_table.
        direction = pm.Vector2(cue_ball_pos) - pm.Vector2(mouse_pos_on_click) + self.offset
        direction.scale_to_length(5)
        
        disp_surf_cue_ball_pos = self.offset + cue_ball_pos
        
        midpoint = (self.cue_tip_pts[2] + self.cue_tip_pts[3]) / 2
        
        if midpoint.distance_to(disp_surf_cue_ball_pos) <= 5:
            return False
        else:
            
            
            for pt in self.cue_tip_pts:
                pt += direction
            #Only update the last two points in the stick to avoid
            #updating points that are shared in cue_tip_pts. Product of aliasing.
            for pt in self.stick_pts[2:]:
                pt += direction
                
            return True
        
        
        
        
        
    def __get_orthogonal(self, v):
        '''
        Calculate a vector orthogonal to line dir
        '''
        v1 = v.x
        v2 = v.y
        
        
        
        if v2 != 0:#Handle cases where v has a zero. Otherwise, a component of w is arbitrarily selected, and the 
            #dot product is set to 0 and solved.
            w1 = 1
            w2 = -1 * v1 * w1 / v2
        elif v1 != 0:
            w2 = 1
            w1 = -1 * v2 * w2 / v1
        else:#v is the zero vector, return the zero vector
            w1,w2 = 0
            
        return pm.Vector2(w1,w2)
        
        