import pygame
import uuid
import copy
from main.global_constants import screen, SPACING, RED, BLACK, screen_rect
from functions.check_png_overlap import check_png_overlap
from functions.check_line_overlap import check_line_overlap

class Connection:
    def __init__(self):
        self.id = uuid.uuid4()
        self.start_pos = None
        self.end_pos = None
        self.virtual_start_pos = None
        self.virtual_end_pos = None  
        self.color = BLACK

    def get_start_pos_connection(self, hotzone_pos, zoom_factor):
        self.start_pos = hotzone_pos
        self.virtual_start_pos = ((SPACING + zoom_factor) * (self.start_pos[0] / SPACING)), ((SPACING + zoom_factor) * (self.start_pos[1] / SPACING))
 
    def update_end_pos_connection(self, virtual_mouse_pos, zoom_factor): 
        x, y = virtual_mouse_pos
        x = round(x / SPACING) * SPACING
        y = round(y / SPACING) * SPACING
        if abs(self.start_pos[0] - x) > abs(self.start_pos[1] - y):
            self.end_pos = (x, self.start_pos[1])  # Keep the same vertical position
        else:
            self.end_pos = (self.start_pos[0], y)  # Keep the same horizontal position 
        
        self.virtual_end_pos = ((SPACING + zoom_factor) * (self.end_pos[0] / SPACING)), ((SPACING + zoom_factor) * (self.end_pos[1] / SPACING))

    def draw_current_line(self, camera_x, camera_y, comp, conn, wire_color, zoom_factor):

        if self.start_pos and self.end_pos:
            # Check for overlap
            line_is_colliding = check_line_overlap(self.start_pos, self.end_pos, conn) or \
                           check_png_overlap(self.start_pos, self.end_pos, comp)
            color = RED if line_is_colliding else wire_color  # Red if colliding
            self.virtual_start_pos = ((self.start_pos[0] / SPACING) * (SPACING + zoom_factor)), ((self.start_pos[1] / SPACING) * (SPACING + zoom_factor))
            self.virtual_end_pos = ((self.end_pos[0] / SPACING) * (SPACING + zoom_factor)), ((self.end_pos[1] / SPACING) * (SPACING + zoom_factor))
            start_position = self.virtual_start_pos[0] - camera_x, self.virtual_start_pos[1] - camera_y
            end_position = self.virtual_end_pos[0] - camera_x, self.virtual_end_pos[1] - camera_y
            pygame.draw.line(screen, color, start_position, end_position, 3) 

            return line_is_colliding 
        
    def draw(self, color, camera_x, camera_y):   

        start = self.virtual_start_pos[0] - camera_x, self.virtual_start_pos[1] - camera_y
        end = self.virtual_end_pos[0] - camera_x, self.virtual_end_pos[1] - camera_y
        if screen_rect.clipline(start, end):
            pygame.draw.line(screen, color, start, end, 3) 
  
    # Fully independent copy with the same ID
    def copy_with_same_id(self):
        new_instance = copy.deepcopy(self)  # Create a fully independent copy
        new_instance.id = self.id  # Retain the same ID
        return new_instance

    # Fully independent copy with a new ID
    def copy_with_new_id(self):
        new_instance = copy.deepcopy(self)  # Create a fully independent copy
        new_instance.id = uuid.uuid4()  # Assign a new unique ID
        return new_instance
    