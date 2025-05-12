import pygame
from main.global_constants import screen, BLACK, SPACING

def create_and_draw_selecting_box(start_pos_selecting_rect, virtual_mouse_pos, camera_offset_x, camera_offset_y, zoom_factor):
    rect_x = min(start_pos_selecting_rect[0], virtual_mouse_pos[0]) 
    rect_y = min(start_pos_selecting_rect[1], virtual_mouse_pos[1])
    rect_width = abs(virtual_mouse_pos[0] - start_pos_selecting_rect[0])
    rect_height = abs(virtual_mouse_pos[1] - start_pos_selecting_rect[1])
    # Create and draw the rectangle
    
    rect_x = (rect_x / SPACING) * (SPACING + zoom_factor) - camera_offset_x
    rect_y = (rect_y / SPACING) * (SPACING + zoom_factor) - camera_offset_y
    rect_width = (rect_width / SPACING) * (SPACING + zoom_factor)
    rect_height = (rect_height / SPACING) * (SPACING + zoom_factor)
    
    selecting_box = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    
    virtual_selecting_box = pygame.Rect(start_pos_selecting_rect[0], start_pos_selecting_rect[1], virtual_mouse_pos[0] - start_pos_selecting_rect[0], virtual_mouse_pos[1] - start_pos_selecting_rect[1])
    
    pygame.draw.rect(screen, BLACK, selecting_box, 1)

    return virtual_selecting_box